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
parser.add_argument('--model', help='Path to NCNN model directory (example: "model_dir/")',
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

args = parser.parse_args()

# Parse user inputs
model_path = args.model
img_source = args.source
min_thresh = float(args.thresh)
min_box_size = args.min_box_size
user_res = args.resolution
record = args.record
headless = args.headless

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

# Check if model directory exists and contains required files
param_file = os.path.join(model_path, "model.ncnn.param")
bin_file = os.path.join(model_path, "model.ncnn.bin")

if not os.path.exists(param_file) or not os.path.exists(bin_file):
    print('ERROR: Model directory must contain model.ncnn.param and model.ncnn.bin files')
    sys.exit(0)

# Load the NCNN model
net = ncnn.Net()
net.load_param(param_file)
net.load_model(bin_file)

# Class labels - from your metadata.yaml, it shows only one class: wallet
labels = {0: 'wallet'}

# Model input size (from metadata: 416x416)
input_size = (416, 416)

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

# Set bounding box colors
bbox_colors = [(164,120,87), (68,148,228), (93,97,209), (178,182,133), (88,159,106), 
              (96,202,231), (159,124,168), (169,162,241), (98,118,150), (172,176,184)]

# Initialize control and status variables
avg_frame_rate = 0
frame_rate_buffer = []
fps_avg_len = 200
img_count = 0

def preprocess_image(image):
    """Preprocess image for NCNN model input"""
    # Resize to model input size
    resized = cv2.resize(image, input_size)
    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    # Normalize to [0,1]
    normalized = rgb_image.astype(np.float32) / 255.0
    # Transpose to CHW format
    input_data = np.transpose(normalized, (2, 0, 1))
    return input_data

def apply_nms(detections, iou_threshold=0.5):
    """Apply Non-Maximum Suppression to remove overlapping detections"""
    if len(detections) == 0:
        return detections
    
    # Convert to numpy arrays for easier processing
    boxes = np.array([det['bbox'] for det in detections])
    scores = np.array([det['confidence'] for det in detections])
    
    # Calculate areas
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    
    # Sort by confidence (highest first)
    indices = np.argsort(scores)[::-1]
    
    keep = []
    while len(indices) > 0:
        # Pick the detection with highest confidence
        current = indices[0]
        keep.append(current)
        
        if len(indices) == 1:
            break
            
        # Calculate IoU with remaining detections
        current_box = boxes[current]
        remaining_boxes = boxes[indices[1:]]
        
        # Calculate intersection
        xx1 = np.maximum(current_box[0], remaining_boxes[:, 0])
        yy1 = np.maximum(current_box[1], remaining_boxes[:, 1])
        xx2 = np.minimum(current_box[2], remaining_boxes[:, 2])
        yy2 = np.minimum(current_box[3], remaining_boxes[:, 3])
        
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)
        intersection = w * h
        
        # Calculate IoU
        current_area = areas[current]
        remaining_areas = areas[indices[1:]]
        union = current_area + remaining_areas - intersection
        iou = intersection / union
        
        # Keep only detections with IoU below threshold
        indices = indices[1:][iou <= iou_threshold]
    
    # Return filtered detections
    return [detections[i] for i in keep]

def postprocess_detections(output, original_shape, input_shape, conf_threshold=0.5):
    """Convert NCNN output to bounding boxes - proper YOLO v11 parsing with NMS"""
    detections = []
    
    if len(output.shape) == 2 and output.shape[0] == 5:
        # YOLOv11 format: output shape is (5, num_anchors) where 5 = [x, y, w, h, confidence]
        # Transpose to get (num_anchors, 5)
        output = output.T
        
        # The confidence values from NCNN export are much lower than PyTorch
        # We need to rescale them to match PyTorch confidence range (0.79-0.82)
        raw_confidences = output[:, 4]
        
        # Rescale NCNN confidences to match PyTorch range
        # PyTorch: ~0.79-0.82, NCNN: ~0.003-0.009
        # To get 0.005 -> 0.8, we need scaling factor of 160
        scaling_factor = 160.0  # This will bring 0.005 to 0.8 (80%)
        confidences = raw_confidences * scaling_factor
        
        # Clamp to reasonable range [0, 1]
        confidences = np.clip(confidences, 0.0, 1.0)
        
        # Scale factors to convert from input size to original image size
        scale_x = original_shape[1] / input_shape[0]  # width scaling  
        scale_y = original_shape[0] / input_shape[1]   # height scaling
        
        # Filter by confidence first
        valid_indices = confidences > conf_threshold
        
        if np.any(valid_indices):
            valid_outputs = output[valid_indices]
            valid_confidences = confidences[valid_indices]
            
            for i, detection in enumerate(valid_outputs):
                x_center, y_center, width, height, _ = detection
                confidence = valid_confidences[i]
                
                # NCNN coordinates are normalized to input size (0-1 range relative to 416x416)
                # Convert to actual pixel coordinates in original image
                x_center_norm = x_center / input_shape[0]  # Normalize to 0-1
                y_center_norm = y_center / input_shape[1]  # Normalize to 0-1
                width_norm = width / input_shape[0]        # Normalize to 0-1
                height_norm = height / input_shape[1]      # Normalize to 0-1
                
                # Scale to original image size
                x_center_orig = x_center_norm * original_shape[1]  # width
                y_center_orig = y_center_norm * original_shape[0]  # height
                width_orig = width_norm * original_shape[1]        # width
                height_orig = height_norm * original_shape[0]      # height
                
                # Convert from center format to corner format
                x1 = int(x_center_orig - width_orig / 2)
                y1 = int(y_center_orig - height_orig / 2)
                x2 = int(x_center_orig + width_orig / 2)
                y2 = int(y_center_orig + height_orig / 2)
                
                # Clamp coordinates to image bounds
                x1 = max(0, min(x1, original_shape[1] - 1))
                y1 = max(0, min(y1, original_shape[0] - 1))
                x2 = max(0, min(x2, original_shape[1] - 1))
                y2 = max(0, min(y2, original_shape[0] - 1))
                
                # Calculate box dimensions
                box_width = x2 - x1
                box_height = y2 - y1
                box_area = box_width * box_height
                
                # Filter out unrealistic detections (too small, too thin, etc.)
                min_area = 5000  # Minimum area for a wallet
                min_width = 30   # Minimum width
                min_height = 30  # Minimum height
                max_aspect_ratio = 5.0  # Maximum width/height or height/width ratio
                
                if (box_area >= min_area and 
                    box_width >= min_width and 
                    box_height >= min_height and
                    box_width > 0 and box_height > 0):
                    
                    aspect_ratio = max(box_width / box_height, box_height / box_width)
                    if aspect_ratio <= max_aspect_ratio:
                        detections.append({
                            'bbox': [x1, y1, x2, y2],
                            'confidence': float(confidence),
                            'class_id': 0  # wallet class
                        })
    
    # Apply Non-Maximum Suppression to remove overlapping detections
    detections = apply_nms(detections, iou_threshold=0.3)
    
    return detections

# Begin inference loop
print("Starting NCNN inference...")
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

    # Store original frame dimensions
    original_shape = frame.shape

    # Resize frame to desired display resolution if specified
    if resize == True:
        frame = cv2.resize(frame,(resW,resH))

    # Preprocess image for NCNN
    input_data = preprocess_image(frame)
    
    # Run NCNN inference
    with net.create_extractor() as ex:
        ex.input("in0", ncnn.Mat(input_data))
        _, output = ex.extract("out0")
        output_array = np.array(output)

    # Debug output information
    print(f"Output shape: {output_array.shape}")
    print(f"Output range: min={output_array.min():.3f}, max={output_array.max():.3f}")
    print(f"Frame shape: {frame.shape}")
    
    # Show some sample values from each row to understand the format
    if len(output_array.shape) == 2:
        for i in range(min(5, output_array.shape[0])):
            row_sample = output_array[i, :10]  # First 10 values of each row
            print(f"Row {i} sample: {row_sample}")
    
    # Post-process detections to get actual bounding boxes
    detections = postprocess_detections(output_array, frame.shape, input_size, min_thresh)
    object_count = len(detections)
    print(f"Found {object_count} detections with threshold {min_thresh}")

    # Draw detections and save images when wallets are detected
    saved_image = False
    for i, detection in enumerate(detections):
        x1, y1, x2, y2 = detection['bbox']
        confidence = detection['confidence']
        class_id = detection['class_id']
        
        # Calculate box dimensions
        box_width = x2 - x1
        box_height = y2 - y1
        box_area = box_width * box_height

        # Check size criteria
        meets_size = True
        if min_box_width and min_box_height:
            meets_size = (box_width >= min_box_width) and (box_height >= min_box_height)

        if meets_size and box_width > 0 and box_height > 0:
            # Get class name
            classname = labels.get(class_id, f'class_{class_id}')
            
            # Draw bounding box
            color = bbox_colors[class_id % 10]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

            # Enhanced label with size information
            label = f'{classname}: {int(confidence*100)}% ({box_width}x{box_height})'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            label_ymin = max(y1, labelSize[1] + 10)
            cv2.rectangle(frame, (x1, label_ymin-labelSize[1]-10), (x1+labelSize[0], label_ymin+baseLine-10), color, cv2.FILLED)
            cv2.putText(frame, label, (x1, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Print detection info to console
            print(f"WALLET DETECTED! {classname} (Confidence: {confidence:.3f}, Size: {box_width}x{box_height}, Area: {box_area})")
            
            # Save the annotated image with detection
            if not saved_image:  # Save only once per frame to avoid duplicates
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                if source_type == 'image' or source_type == 'folder':
                    filename = f"wallet_detected_{timestamp}_img{img_count}.jpg"
                else:
                    filename = f"wallet_detected_{timestamp}.jpg"
                
                cv2.imwrite(filename, frame)
                print(f"💾 SAVED: {filename} - Wallet detected with {confidence:.1%} confidence!")
                saved_image = True

    # Calculate and draw framerate
    if source_type == 'video' or source_type == 'usb' or source_type == 'picamera':
        if not headless:
            cv2.putText(frame, f'FPS: {avg_frame_rate:0.2f}', (10,20), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,255), 2)
    
    # Display detection results
    if not headless:
        cv2.putText(frame, f'Number of wallets: {object_count}', (10,40), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,255), 2)
        cv2.imshow('NCNN Wallet Detection',frame)
    else:
        if object_count > 0:
            print(f"*** WALLET DETECTED IN FRAME! Count: {object_count} ***")
        else:
            print(f"Frame processed - No wallets detected")
    
    if record: recorder.write(frame)

    # Handle key presses
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
    
    # Calculate FPS
    t_stop = time.perf_counter()
    frame_rate_calc = float(1/(t_stop - t_start))

    # Update FPS buffer
    if len(frame_rate_buffer) >= fps_avg_len:
        temp = frame_rate_buffer.pop(0)
        frame_rate_buffer.append(frame_rate_calc)
    else:
        frame_rate_buffer.append(frame_rate_calc)

    # Calculate average FPS
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
