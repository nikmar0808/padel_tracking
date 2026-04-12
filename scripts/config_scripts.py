import os
from pathlib import Path

# Root directory of your project
BASE_DIR = Path(__file__).parent.parent

# Path definitions
PADEL100_LABEL_DIR = os.path.join(BASE_DIR, 'data/raw/labels')
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_DIR = os.path.join(BASE_DIR, 'configs')

VIDEO_DIR = os.path.join(DATA_DIR, 'raw/source_videos')

# Frame Extraction constants
EXTRACTED_FRAMES_DIR = os.path.join(DATA_DIR, 'interim/extracted_frames')
SAMPLED_FRAMES_DIR = os.path.join(DATA_DIR, 'interim/sampled_frames')
FPS = 30
WIDTH = 1920
HEIGHT = 1080

# Annotation path constants
INTERM_DATA_DIR = os.path.join(DATA_DIR, 'interim')
ANNOT_SAMPLES_DIR = os.path.join(INTERM_DATA_DIR, 'annotated_samples')
ANNOT_BATCHES_DIR = os.path.join(INTERM_DATA_DIR, 'annotation_batches')
MANUAL_ANNOT_DIR = os.path.join(INTERM_DATA_DIR, 'annotations/manual')
AUTO_ANNOT_DIR = os.path.join(INTERM_DATA_DIR, 'annotations/auto')

# Auto-Annotation Dataset constants
AUTO_ANNOT_CONFIDENCE_THRESHOLD = 0.05 # Adjust as the Dataset increases in size (e.g., 0.25 for more precision, 0.05 for more recall)
AUTO_ANNOT_IOU_THRESHOLD = 0.3
AUTO_ANNOT_IMAGE_SIZE = 1280


# File names (Verify these match your actual files!)
# MENS_SHOTS = os.path.join(PADEL100_LABEL_DIR, '2022_BCN_FinalM_1_shots.csv')
# MENS_BALL = os.path.join(ANNOT_DIR, '2022_BCN_FinalM_1_ball.json')
# MENS_POSE = os.path.join(ANNOT_DIR, '2022_BCN_FinalM_1_pose.json')
# MENS_HOMOGRAPHY = os.path.join(ANNOT_DIR, '2022_BCN_FinalM_1_homography.json')
# MENS_VIDEO = os.path.join(VIDEO_DIR, '2022_BCN_FinalM_1.mp4') # Change if named differently
# WOMENS_SHOTS = os.path.join(PADEL100_LABEL_DIR, '2022_BCN_FinalF_1_shots.csv')
# WOMENS_BALL = os.path.join(ANNOT_DIR, '2022_BCN_FinalF_1_ball.json')
# WOMENS_POSE = os.path.join(ANNOT_DIR, '2022_BCN_FinalF_1_pose.json')
# WOMENS_HOMOGRAPHY = os.path.join(ANNOT_DIR, '2022_BCN_FinalF_1_homography.json')
# WOMENS_VIDEO = os.path.join(VIDEO_DIR, '2022_BCN_FinalF_1.mp4') # Change if named differently