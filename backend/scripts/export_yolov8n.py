from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load an official model

model.export(format='tflite').save('yolov8n.tflite')  # export model