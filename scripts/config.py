import os
from pathlib import Path

# Root directory of your project
BASE_DIR = Path(__file__).parent.parent

# Path definitions
PADEL100_LABEL_DIR = os.path.join(BASE_DIR, 'data/raw/labels')
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_DIR = os.path.join(BASE_DIR, 'configs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

VIDEO_DIR = os.path.join(DATA_DIR, 'raw/source_videos')
EXTRACTED_FRAMES_DIR = os.path.join(DATA_DIR, 'interim/extracted_frames')
SAMPLED_FRAMES_DIR = os.path.join(DATA_DIR, 'interim/sampled_frames')
ANNOT_DIR = os.path.join(DATA_DIR, 'annotations')
ANNOT_BATCHES_DIR = os.path.join(DATA_DIR, 'interim/annotation_batches')
ANNOT_SAMPLES_DIR = os.path.join(DATA_DIR, 'interim/annotated_samples')

TRNG_IMAGES_DIR = os.path.join(DATA_DIR, 'processed/images/train')
TRNG_LABELS_DIR = os.path.join(DATA_DIR, 'processed/labels/train')
VAL_IMAGES_DIR = os.path.join(DATA_DIR, 'processed/images/val')
VAL_LABELS_DIR = os.path.join(DATA_DIR, 'processed/labels/val')

# Extracted Frames constants
FPS = 30
WIDTH = 1920
HEIGHT = 1080

# Training constants
TRNG_DATASET_PATHS = os.path.join(CONFIG_DIR, 'training_dataset.yml') # Paths for training dataset (YOLO format)
EPOCHS = 40 # Adjust based on needs (e.g., 50 or 100 for better performance)
BATCH_SIZE = 8 # Adjust based on GPU memory (e.g., 16 for 16GB VRAM)
IMG_SIZE = 1280 # Adjust based on needs (e.g., 640 for faster training, 1280 for better accuracy)

# File names (Verify these match your actual files!)
MENS_SHOTS = os.path.join(PADEL100_LABEL_DIR, '2022_BCN_FinalM_1_shots.csv')
MENS_BALL = os.path.join(ANNOT_DIR, '2022_BCN_FinalM_1_ball.json')
MENS_POSE = os.path.join(ANNOT_DIR, '2022_BCN_FinalM_1_pose.json')
MENS_HOMOGRAPHY = os.path.join(ANNOT_DIR, '2022_BCN_FinalM_1_homography.json')
MENS_VIDEO = os.path.join(VIDEO_DIR, '2022_BCN_FinalM_1.mp4') # Change if named differently
WOMENS_SHOTS = os.path.join(PADEL100_LABEL_DIR, '2022_BCN_FinalF_1_shots.csv')
WOMENS_BALL = os.path.join(ANNOT_DIR, '2022_BCN_FinalF_1_ball.json')
WOMENS_POSE = os.path.join(ANNOT_DIR, '2022_BCN_FinalF_1_pose.json')
WOMENS_HOMOGRAPHY = os.path.join(ANNOT_DIR, '2022_BCN_FinalF_1_homography.json')
WOMENS_VIDEO = os.path.join(VIDEO_DIR, '2022_BCN_FinalF_1.mp4') # Change if named differently