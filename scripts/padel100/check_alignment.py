import cv2
import matplotlib.pyplot as plt
import os
from scripts.padel100.data_mapper import get_mens_training_sample, get_womens_training_sample
from config import FRAME_DIR

def verify_mens_visual_sync(frame_num):
    frame_name = f"mens_frame_{frame_num:06d}.png"
    img_path = os.path.join(FRAME_DIR, frame_name)
    
    if not os.path.exists(img_path):
        print(f"❌ Still waiting for {frame_name} to be extracted...")
        return

    # 1. Get our synced data
    data = get_mens_training_sample(frame_name)
    
    # 2. Load the actual extracted image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 3. Draw Ball (Yellow)
    if data['ball_xy']:
        bx, by = map(int, data['ball_xy'])
        cv2.circle(img, (bx, by), 10, (255, 255, 0), -1)

    # 4. Draw Skeleton (Cyan)
    if data['skeleton'] is not None:
        for pt in data['skeleton']:
            x, y, v = map(int, pt)
            if v > 0: # Only draw if visible
                cv2.circle(img, (x, y), 6, (0, 255, 255), -1)

    plt.figure(figsize=(12, 8))
    plt.imshow(img)
    plt.title(f"SYNC CHECK: {frame_name} | Label: {data['shot_type']}")
    plt.axis('off')
    plt.show()

def verify_womens_visual_sync(frame_num):
    frame_name = f"womens_frame_{frame_num:06d}.png"
    img_path = os.path.join(FRAME_DIR, frame_name)
    
    if not os.path.exists(img_path):
        print(f"❌ Still waiting for {frame_name} to be extracted...")
        return

    # 1. Get our synced data
    data = get_womens_training_sample(frame_name)
    
    # 2. Load the actual extracted image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 3. Draw Ball (Yellow)
    if data['ball_xy']:
        bx, by = map(int, data['ball_xy'])
        cv2.circle(img, (bx, by), 10, (255, 255, 0), -1)

    # 4. Draw Skeleton (Cyan)
    if data['skeleton'] is not None:
        for pt in data['skeleton']:
            x, y, v = map(int, pt)
            if v > 0: # Only draw if visible
                cv2.circle(img, (x, y), 6, (0, 255, 255), -1)

    plt.figure(figsize=(12, 8))
    plt.imshow(img)
    plt.title(f"SYNC CHECK: {frame_name} | Label: {data['shot_type']}")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    verify_mens_visual_sync(22)
    print(f"{'='*50}")
    verify_womens_visual_sync(100)
    print(f"{'='*50}")
