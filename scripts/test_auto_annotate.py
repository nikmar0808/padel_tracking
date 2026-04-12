from ultralytics import YOLO

model = YOLO(r'runs\detect\train\weights\best.pt')

results = model.predict(
    source="data/interim/annotation_batches/batch_1",
    conf=0.05,
    iou=0.3,
    imgsz=1280,
    save_txt=True
)