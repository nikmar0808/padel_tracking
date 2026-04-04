import os
import cv2
from config import EXTRACTED_FRAMES_DIR, SAMPLED_FRAMES_DIR

input_folder = EXTRACTED_FRAMES_DIR
output_folder = SAMPLED_FRAMES_DIR

os.makedirs(output_folder, exist_ok=True)

sample_rate = 10   # keep 1 frame every 10 frames

frames = sorted(os.listdir(input_folder))

for i, frame_name in enumerate(frames):
    
    if i % sample_rate == 0:
        
        src = os.path.join(input_folder, frame_name)
        dst = os.path.join(output_folder, frame_name)

        img = cv2.imread(src)
        cv2.imwrite(dst, img)
        print(f"✅ Sampled {frame_name} to {dst}")