import os
from pathlib import Path

# Root directory of your project
BASE_DIR = Path(__file__).parent.parent

# Path definitions
DATA_DIR = os.path.join(BASE_DIR, 'data')
LABEL_DIR = os.path.join(DATA_DIR, 'Labels')
ANNOT_DIR = os.path.join(DATA_DIR, 'Annotations')
FRAME_DIR = os.path.join(DATA_DIR, 'Frames')
VIDEO_DIR = os.path.join(DATA_DIR, 'Source_Videos')

# Dataset constants
FPS = 30
WIDTH = 1920
HEIGHT = 1080

# File names (Verify these match your actual files!)
MENS_SHOTS = os.path.join(LABEL_DIR, '2022_BCN_FinalM_1_shots.csv')
MENS_BALL = os.path.join(ANNOT_DIR, '2022_BCN_FinalM_1_ball.json')
MENS_POSE = os.path.join(ANNOT_DIR, '2022_BCN_FinalM_1_pose.json')
MENS_HOMOGRAPHY = os.path.join(ANNOT_DIR, '2022_BCN_FinalM_1_homography.json')
MENS_VIDEO = os.path.join(VIDEO_DIR, '2022_BCN_FinalM_1.mp4') # Change if named differently
WOMENS_SHOTS = os.path.join(LABEL_DIR, '2022_BCN_FinalF_1_shots.csv')
WOMENS_BALL = os.path.join(ANNOT_DIR, '2022_BCN_FinalF_1_ball.json')
WOMENS_POSE = os.path.join(ANNOT_DIR, '2022_BCN_FinalF_1_pose.json')
WOMENS_HOMOGRAPHY = os.path.join(ANNOT_DIR, '2022_BCN_FinalF_1_homography.json')
WOMENS_VIDEO = os.path.join(VIDEO_DIR, '2022_BCN_FinalF_1.mp4') # Change if named differently