from ultralytics import YOLO
from scripts.config import BATCH_SIZE, EPOCHS, IMG_SIZE, TRNG_DATASET_PATHS

model = YOLO("yolov8n.pt")

model.train(
    data=TRNG_DATASET_PATHS,
    epochs=EPOCHS,
    imgsz=IMG_SIZE,
    batch=BATCH_SIZE
)