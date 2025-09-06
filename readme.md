cd /home/pi/Downloads/Moppy/ml_pipeline/src/utils && python yolo_detect_ncnn.py --model=/home/pi/Downloads/Moppy/ml_pipeline/src/model/best_ncnn_model --source=wallet.mp4 --headless --thresh=0.7

cd /home/pi/Downloads/Moppy/ml_pipeline/src/utils && python yolo_detect_ncnn.py --model=/home/pi/Downloads/Moppy/ml_pipeline/src/model/best_ncnn_model --source=captured_frame.jpg --headless --thresh=0.7


cd /home/pi/Downloads/Moppy/ml_pipeline/src/utils && python yolo_detect.py --model=/home/pi/Downloads/Moppy/ml_pipeline/src/model/best.pt --source=captured_frame.jpg --headless --thresh=0.7

cd /home/pi/Downloads/Moppy/ml_pipeline/src/utils && python yolo_detect.py --model=/home/pi/Downloads/Moppy/ml_pipeline/src/model/best.pt --source=wallet.mp4 --headless --thresh=0.7


working:

python yolo_detect.py --model=/home/pi/Downloads/Moppy/ml_pipeline/src/model/best.pt --source=wallet.mp4 --headless --thresh=0.7 2>&1 | head -5