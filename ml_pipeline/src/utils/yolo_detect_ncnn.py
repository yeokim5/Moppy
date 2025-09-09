import os
import sys
import argparse
import glob
import time

import cv2
import numpy as np
import ncnn

# Define and parse user input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model', help='Path to NCNN model directory (example: "model/best_ncnn_model")',
                    required=True)
parser.add_argument('--source', help='Image source, can be image file ("test.jpg"), \
                    image folder ("test_dir"), video file ("testvid.mp4"), index of USB camera ("usb0"), or index of Picamera ("picamera0")', 
                    required=True)
parser.add_argument('--thresh', help='Minimum confidence threshold for displaying detected objects (example: "0.4")',
                    default=0.5)
parser.add_argument('--min_box_size', help='Minimum box size (width x height) in pixels to display (example: "100x100")',
                    default=None)
parser.add_argument('--resolution', help='Resolution in WxH to display inference results at (example: "640x480"), \
                    otherwise, match source resolution',
                    default=None)
parser.add_argument('--record', help='Record results from video or webcam and save it as "demo1.avi". Must specify --resolution argument to record.',
                    action='store_true')
parser.add_argument('--headless', help='Run without display (useful for headless systems)',
                    action='store_true')
parser.add_argument('--capture_all', help='Save every frame as image file, not just detected frames (true/false)',
                    type=str, default='false')
parser.add_argument('--debug_confidence', help='Print all detection confidences, even below threshold (true/false)',
                    type=str, default='false')

args = parser.parse_args()

# Parse user inputs
model_path = args.model
img_source = args.source
min_thresh = float(args.thresh)
min_box_size = args.min_box_size
user_res = args.resolution
record = args.record
headless = args.headless
capture_all = args.capture_all.lower() == 'true'
debug_confidence = args.debug_confidence.lower() == 'true'

# Parse minimum box size if provided
min_box_width = None
min_box_height = None
if min_box_size:
    try:
        min_box_width, min_box_height = map(int, min_box_size.split('x'))
        print(f"Minimum box size filter: {min_box_width}x{min_box_height} pixels")
    except:
        print("Error: min_box_size must be in format 'widthxheight' (e.g., '100x100')")
        sys.exit(1)

# Check if model directory exists
if not os.path.exists(model_path):
    print('ERROR: Model path is invalid or model was not found. Make sure the model path was entered correctly.')
    sys.exit(0)

# NCNN Model Loading
class NCNNYolo:
    def __init__(self, model_path, target_size=416, num_threads=4):
        self.target_size = target_size
        self.num_threads = num_threads
        
        # Initialize NCNN network
        self.net = ncnn.Net()
        self.net.opt.use_vulkan_compute = False
        self.net.opt.num_threads = num_threads
        
        # Load model files
        param_path = os.path.join(model_path, "model.ncnn.param")
        bin_path = os.path.join(model_path, "model.ncnn.bin")
        
        if not os.path.exists(param_path):
            # List files in directory to help debug
            files = os.listdir(model_path)
            print(f"Files in model directory: {files}")
            print(f"ERROR: Could not find NCNN model files in {model_path}")
            sys.exit(1)
        
        print(f"Loading NCNN model from: {param_path}, {bin_path}")
        ret = self.net.load_param(param_path)
        if ret != 0:
            print(f"ERROR: Failed to load param file: {param_path}")
            sys.exit(1)
            
        ret = self.net.load_model(bin_path)
        if ret != 0:
            print(f"ERROR: Failed to load model file: {bin_path}")
            sys.exit(1)
        
        print("NCNN model loaded successfully!")
        
        # Define class names (adjust based on your model)
        self.class_names = {0: 'wallet'}
    
    def preprocess(self, image):
        """Preprocess image for NCNN inference"""
        h, w = image.shape[:2]
        
        # Calculate scaling factor
        scale = self.target_size / max(h, w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # Resize image
        resized = cv2.resize(image, (new_w, new_h))
        
        # Pad image to target size
        top = (self.target_size - new_h) // 2
        bottom = self.target_size - new_h - top
        left = (self.target_size - new_w) // 2
        right = self.target_size - new_w - left
        
        padded = cv2.copyMakeBorder(resized, top, bottom, left, right, 
                                  cv2.BORDER_CONSTANT, value=(114, 114, 114))
        
        # NCNN expects BGR format, so we don't need to convert
        # Create NCNN Mat directly from BGR image
        mat_in = ncnn.Mat.from_pixels(padded, ncnn.Mat.PixelType.PIXEL_BGR, self.target_size, self.target_size)
        
        # Normalize (0-1 range)
        mean_vals = [0.0, 0.0, 0.0]
        norm_vals = [1/255.0, 1/255.0, 1/255.0]
        mat_in.substract_mean_normalize(mean_vals, norm_vals)
        
        return mat_in, scale, left, top
    
    def postprocess(self, output, scale, left, top, conf_threshold=0.25, nms_threshold=0.45, debug_mode=False):
        """Post-process NCNN output to get detections"""
        detections = []
        
        print(f"Output shape: h={output.h}, w={output.w}, c={output.c}")  # Debug info
        
        # NCNN YOLO output is transposed: shape is (5, num_detections) or (6, num_detections)
        # Row 0: x_center, Row 1: y_center, Row 2: width, Row 3: height, Row 4: confidence
        num_detections = output.w
        
        for i in range(num_detections):
            # Get values for this detection (column i)
            x_center = output.row(0)[i]  
            y_center = output.row(1)[i]  
            width = output.row(2)[i]     
            height = output.row(3)[i]    
            confidence = output.row(4)[i]
            
            # Debug: show all detections if debug mode is enabled
            if debug_mode and i < 10:  # Show first 10 detections for debugging
                print(f"Detection {i}: confidence={confidence:.3f}, x={x_center:.1f}, y={y_center:.1f}, w={width:.1f}, h={height:.1f}")
            
            # Skip low confidence detections
            if confidence < conf_threshold:
                continue
            
            # Debug: print raw values for first detection
            if len(detections) == 0:  # Print for first valid detection only
                print(f"Raw values: x_center={x_center:.3f}, y_center={y_center:.3f}, width={width:.3f}, height={height:.3f}, conf={confidence:.3f}")
                print(f"Target size: {self.target_size}, Scale: {scale:.3f}, Left: {left}, Top: {top}")
            
            # The coordinates might already be in pixel space (not normalized)
            # Let's try treating them as pixel coordinates directly
            x_center_px = x_center
            y_center_px = y_center  
            width_px = width
            height_px = height
            
            # Convert center format to corner format on padded image
            x1_padded = x_center_px - width_px / 2
            y1_padded = y_center_px - height_px / 2
            x2_padded = x_center_px + width_px / 2
            y2_padded = y_center_px + height_px / 2
            
            # Remove padding offset and scale back to original image
            x1 = (x1_padded - left) / scale
            y1 = (y1_padded - top) / scale
            x2 = (x2_padded - left) / scale
            y2 = (y2_padded - top) / scale
            
            # For single class (wallet), class_id = 0
            class_id = 0
            
            detections.append({
                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                'confidence': confidence,
                'class_id': class_id,
                'class_name': self.class_names.get(class_id, 'unknown')
            })
        
        # Apply NMS
        detections = self.apply_nms(detections, nms_threshold)
        return detections
    
    def apply_nms(self, detections, nms_threshold):
        """Apply Non-Maximum Suppression"""
        if not detections:
            return []
        
        # Sort by confidence
        detections.sort(key=lambda x: x['confidence'], reverse=True)
        
        keep = []
        while detections:
            current = detections.pop(0)
            keep.append(current)
            
            # Remove overlapping detections
            detections = [det for det in detections if self.calculate_iou(current['bbox'], det['bbox']) < nms_threshold]
        
        return keep
    
    def calculate_iou(self, box1, box2):
        """Calculate Intersection over Union"""
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        
        if x2 <= x1 or y2 <= y1:
            return 0.0
        
        intersection = (x2 - x1) * (y2 - y1)
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0
    
    def predict(self, image, conf_threshold=0.5, debug_mode=False):
        """Run inference on image"""
        # Preprocess
        mat_in, scale, left, top = self.preprocess(image)
        
        # Run inference
        ex = self.net.create_extractor()
        ex.input("in0", mat_in)  # Common input name for YOLO models
        
        mat_out = ncnn.Mat()
        ex.extract("out0", mat_out)  # Common output name for YOLO models
        
        # Post-process
        detections = self.postprocess(mat_out, scale, left, top, conf_threshold=conf_threshold, debug_mode=debug_mode)
        
        return detections

# Load the NCNN model
model = NCNNYolo(model_path)
labels = model.class_names

# Parse input to determine if image source is a file, folder, video, or USB camera
img_ext_list = ['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG','.bmp','.BMP']
vid_ext_list = ['.avi','.mov','.mp4','.mkv','.wmv']

if os.path.isdir(img_source):
    source_type = 'folder'
elif os.path.isfile(img_source):
    _, ext = os.path.splitext(img_source)
    if ext in img_ext_list:
        source_type = 'image'
    elif ext in vid_ext_list:
        source_type = 'video'
    else:
        print(f'File extension {ext} is not supported.')
        sys.exit(0)
elif 'usb' in img_source:
    source_type = 'usb'
    usb_idx = int(img_source[3:])
elif 'picamera' in img_source:
    source_type = 'picamera'
    picam_idx = int(img_source[8:])
else:
    print(f'Input {img_source} is invalid. Please try again.')
    sys.exit(0)

# Parse user-specified display resolution
resize = False
if user_res:
    resize = True
    resW, resH = int(user_res.split('x')[0]), int(user_res.split('x')[1])

# Check if recording is valid and set up recording
if record:
    if source_type not in ['video','usb']:
        print('Recording only works for video and camera sources. Please try again.')
        sys.exit(0)
    if not user_res:
        print('Please specify resolution to record video at.')
        sys.exit(0)
    
    # Set up recording
    record_name = 'demo1.avi'
    record_fps = 30
    recorder = cv2.VideoWriter(record_name, cv2.VideoWriter_fourcc(*'MJPG'), record_fps, (resW,resH))

# Load or initialize image source
if source_type == 'image':
    imgs_list = [img_source]
elif source_type == 'folder':
    imgs_list = []
    filelist = glob.glob(img_source + '/*')
    for file in filelist:
        _, file_ext = os.path.splitext(file)
        if file_ext in img_ext_list:
            imgs_list.append(file)
elif source_type == 'video' or source_type == 'usb':
    if source_type == 'video': cap_arg = img_source
    elif source_type == 'usb': cap_arg = usb_idx
    cap = cv2.VideoCapture(cap_arg)

    # Set camera or video resolution if specified by user
    if user_res:
        ret = cap.set(3, resW)
        ret = cap.set(4, resH)

elif source_type == 'picamera':
    from picamera2 import Picamera2
    cap = Picamera2()
    cap.configure(cap.create_video_configuration(main={"format": 'RGB888', "size": (resW, resH)}))
    cap.start()

# Set bounding box colors (using the Tableu 10 color scheme)
bbox_colors = [(164,120,87), (68,148,228), (93,97,209), (178,182,133), (88,159,106), 
              (96,202,231), (159,124,168), (169,162,241), (98,118,150), (172,176,184)]

# Initialize control and status variables
avg_frame_rate = 0
frame_rate_buffer = []
fps_avg_len = 200
img_count = 0
frame_counter = 0  # Counter for all frames when capture_all is enabled

# Begin inference loop
while True:
    t_start = time.perf_counter()

    # Load frame from image source
    if source_type == 'image' or source_type == 'folder':
        if img_count >= len(imgs_list):
            print('All images have been processed. Exiting program.')
            sys.exit(0)
        img_filename = imgs_list[img_count]
        frame = cv2.imread(img_filename)
        img_count = img_count + 1
    
    elif source_type == 'video':
        ret, frame = cap.read()
        if not ret:
            print('Reached end of the video file. Exiting program.')
            break
    
    elif source_type == 'usb':
        ret, frame = cap.read()
        if (frame is None) or (not ret):
            print('Unable to read frames from the camera. This indicates the camera is disconnected or not working. Exiting program.')
            break

    elif source_type == 'picamera':
        frame = cap.capture_array()
        if (frame is None):
            print('Unable to read frames from the Picamera. This indicates the camera is disconnected or not working. Exiting program.')
            break

    # Resize frame to desired display resolution
    if resize == True:
        frame = cv2.resize(frame,(resW,resH))

    # Run NCNN inference on frame
    detections = model.predict(frame, conf_threshold=min_thresh, debug_mode=debug_confidence)

    # Initialize variable for basic object counting example
    object_count = 0

    # Go through each detection and draw bounding boxes
    for detection in detections:
        bbox = detection['bbox']
        confidence = detection['confidence']
        class_name = detection['class_name']
        class_id = detection['class_id']
        
        xmin, ymin, xmax, ymax = bbox
        
        # Calculate box dimensions
        box_width = xmax - xmin
        box_height = ymax - ymin
        box_area = box_width * box_height

        # Check if detection meets both confidence and size criteria
        meets_confidence = confidence > min_thresh
        meets_size = True
        
        if min_box_width and min_box_height:
            meets_size = (box_width >= min_box_width) and (box_height >= min_box_height)

        # Draw box if both confidence and size thresholds are met
        if meets_confidence and meets_size:
            color = bbox_colors[class_id % 10]
            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 3)

            # Enhanced label with size information
            label = f'{class_name}: {int(confidence*100)}% ({box_width}x{box_height})'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            label_ymin = max(ymin, labelSize[1] + 10)
            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), color, cv2.FILLED)
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Basic example: count the number of objects in the image
            object_count = object_count + 1
            
            # Print detection info to console
            print(f"WALLET DETECTED! {class_name} (Confidence: {confidence:.3f}, Size: {box_width}x{box_height}, Area: {box_area})")

    # Save image based on capture_all setting or detection
    should_save = capture_all or object_count > 0
    
    if should_save:
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        if capture_all:
            # Save all frames with frame counter
            if source_type == 'image' or source_type == 'folder':
                filename = f"ncnn_frame_{timestamp}_img{img_count}_frame{frame_counter:06d}.jpg"
            else:
                filename = f"ncnn_frame_{timestamp}_frame{frame_counter:06d}.jpg"
            
            if object_count > 0:
                print(f"💾 SAVED: {filename} - {object_count} wallet(s) detected!")
            else:
                print(f"📸 SAVED: {filename} - no detections")
        else:
            # Original behavior: save only when objects detected
            if source_type == 'image' or source_type == 'folder':
                filename = f"ncnn_wallet_detected_{timestamp}_img{img_count}.jpg"
            else:
                filename = f"ncnn_wallet_detected_{timestamp}.jpg"
            
            print(f"💾 SAVED: {filename} - {object_count} wallet(s) detected!")
        
        cv2.imwrite(filename, frame)

    # Calculate and draw framerate (if using video, USB, or Picamera source)
    if source_type == 'video' or source_type == 'usb' or source_type == 'picamera':
        cv2.putText(frame, f'FPS: {avg_frame_rate:0.2f}', (10,20), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,255), 2)
    
    # Display detection results
    if not headless:
        cv2.putText(frame, f'Number of objects: {object_count}', (10,40), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,255), 2)
        cv2.imshow('NCNN YOLO detection results',frame)
    else:
        if debug_confidence:
            print(f"Frame {frame_counter:06d} processed - Objects detected: {object_count}, Threshold: {min_thresh}")
        else:
            print(f"Frame processed - Objects detected: {object_count}")
    
    if record: recorder.write(frame)

    # Handle user input
    if not headless:
        if source_type == 'image' or source_type == 'folder':
            key = cv2.waitKey()
        elif source_type == 'video' or source_type == 'usb' or source_type == 'picamera':
            key = cv2.waitKey(5)
        
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('s') or key == ord('S'):
            cv2.waitKey()
        elif key == ord('p') or key == ord('P'):
            cv2.imwrite('capture.png',frame)
    else:
        if source_type == 'image' or source_type == 'folder':
            pass
        else:
            pass
    
    # Increment frame counter for capture_all feature
    frame_counter += 1
    
    # Calculate FPS for this frame
    t_stop = time.perf_counter()
    frame_rate_calc = float(1/(t_stop - t_start))

    # Append FPS result to frame_rate_buffer
    if len(frame_rate_buffer) >= fps_avg_len:
        temp = frame_rate_buffer.pop(0)
        frame_rate_buffer.append(frame_rate_calc)
    else:
        frame_rate_buffer.append(frame_rate_calc)

    # Calculate average FPS for past frames
    avg_frame_rate = np.mean(frame_rate_buffer)

# Clean up
print(f'Average pipeline FPS: {avg_frame_rate:.2f}')
if source_type == 'video' or source_type == 'usb':
    cap.release()
elif source_type == 'picamera':
    cap.stop()
if record: recorder.release()
if not headless:
    cv2.destroyAllWindows()
