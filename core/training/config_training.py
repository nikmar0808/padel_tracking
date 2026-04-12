import os
from pathlib import Path

# Root directory of your project
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_DIR = os.path.join(BASE_DIR, 'configs')
VIDEO_DIR = os.path.join(DATA_DIR, 'raw/source_videos')
VIDEO_FILE = os.path.join(VIDEO_DIR, '2022_BCN_FinalM_1.mp4') # Change if named differently

# Frame Extraction constants
EXTRACTED_FRAMES_DIR = os.path.join(DATA_DIR, 'interim/extracted_frames')
SAMPLED_FRAMES_DIR = os.path.join(DATA_DIR, 'interim/sampled_frames')
FPS = 30
WIDTH = 1920
HEIGHT = 1080
BATCH_SIZE = 300

# Annotation path constants
INTERM_DATA_DIR = os.path.join(DATA_DIR, 'interim')
ANNOT_SAMPLES_DIR = os.path.join(INTERM_DATA_DIR, 'annotated_samples')
ANNOT_BATCHES_DIR = os.path.join(INTERM_DATA_DIR, 'annotation_batches')
ANNOT_DIR = os.path.join(INTERM_DATA_DIR, 'annotations')

# Manual Annotation Dataset constants
MANUAL_ANNOT_TEMP_DIR = os.path.join(ANNOT_DIR, 'temp_manual_corrected/obj_train_data')
MANUAL_ANNOT_DIR = os.path.join(ANNOT_DIR, 'manual')

# Auto-Annotation Dataset constants
AUTO_ANNOT_TEMP_DIR = os.path.join(ANNOT_DIR, 'temp_auto_corrected/obj_train_data')
AUTO_ANNOT_CORRECTED_DIR = os.path.join(ANNOT_DIR, 'auto_corrected')
AUTO_ANNOT_DIR = os.path.join(ANNOT_DIR, 'auto')
AUTO_ANNOT_CONFIDENCE_THRESHOLD = 0.05 # Adjust as the Dataset increases in size (e.g., 0.25 for more precision, 0.05 for more recall)
AUTO_ANNOT_IOU_THRESHOLD = 0.3
AUTO_ANNOT_IMAGE_SIZE = 1280

# Training path constants
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
TRNG_IMAGES_DIR = os.path.join(PROCESSED_DATA_DIR, 'images/train')
TRNG_LABELS_DIR = os.path.join(PROCESSED_DATA_DIR, 'labels/train')
VAL_IMAGES_DIR = os.path.join(PROCESSED_DATA_DIR, 'images/val')
VAL_LABELS_DIR = os.path.join(PROCESSED_DATA_DIR, 'labels/val')

# Training Dataset constants
TRNG_DATASET_PATHS = os.path.join(CONFIG_DIR, 'training_dataset.yml') # Paths for training dataset (YOLO format)
SEED_EPOCHS = 40 # Adjust based on needs (e.g., 50 or 100 for better performance)
RETRAIN_EPOCHS = 50 # Adjust based on needs (e.g., 100 or more for better performance)
BATCH_SIZE = 8 # 8 for 16GB RAM with CPU training, can be increased if GPU memory is available (e.g., 16 for 16GB VRAM)
IMG_SIZE = 1280 # Adjust based on needs (e.g., 640 for faster training, 1280 for better accuracy)
DATALOADER_WORKERS = 4 # Adjust based on CPU cores for data loading (e.g., 4 or 6 for 8-core CPU), reduce if CPU starvation occurs or performance worsens