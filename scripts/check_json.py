import json
import os
import numpy as np
import matplotlib.pyplot as plt
from config import MENS_POSE, WOMENS_POSE, WIDTH, HEIGHT

def verify_mens_json():
    if not os.path.exists(MENS_POSE):
        print(f"❌ Error: JSON not found at {MENS_POSE}")
        return

    with open(MENS_POSE, 'r') as f:
        data = json.load(f)

    # Grab the very first annotation
    # Note: JSON structure is usually {'annotations': [...], 'images': [...]}
    annotations = data.get('annotations', [])
    
    if not annotations:
        print("❌ JSON loaded but no annotations found.")
        return

    first_player = annotations[0]
    keypoints = first_player['keypoints'] # [x1, y1, v1, x2, y2, v2...]
    
    # Reshape the flat list into [x, y, visibility]
    kp_array = np.array(keypoints).reshape(-1, 3)
    
    # Create a blank black image
    canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    # Plotting
    plt.figure(figsize=(12, 7))
    plt.imshow(canvas)
    # Scatter plot the x and y coordinates
    plt.scatter(kp_array[:, 0], kp_array[:, 1], c='cyan', s=50, edgecolors='white')
    
    plt.title(f"Skeleton Check: Image ID {first_player.get('image_id')}")
    plt.axis('off')
    plt.show()
    
    print(f"✅ Successfully visualized {len(kp_array)} keypoints for the first player!")

def verify_womens_json():
    if not os.path.exists(WOMENS_POSE):
        print(f"❌ Error: JSON not found at {WOMENS_POSE}")
        return

    with open(WOMENS_POSE, 'r') as f:
        data = json.load(f)

    # Grab the very first annotation
    # Note: JSON structure is usually {'annotations': [...], 'images': [...]}
    annotations = data.get('annotations', [])
    
    if not annotations:
        print("❌ JSON loaded but no annotations found.")
        return

    first_player = annotations[0]
    keypoints = first_player['keypoints'] # [x1, y1, v1, x2, y2, v2...]
    
    # Reshape the flat list into [x, y, visibility]
    kp_array = np.array(keypoints).reshape(-1, 3)
    
    # Create a blank black image
    canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    # Plotting
    plt.figure(figsize=(12, 7))
    plt.imshow(canvas)
    # Scatter plot the x and y coordinates
    plt.scatter(kp_array[:, 0], kp_array[:, 1], c='cyan', s=50, edgecolors='white')
    
    plt.title(f"Skeleton Check: Image ID {first_player.get('image_id')}")
    plt.axis('off')
    plt.show()
    
    print(f"✅ Successfully visualized {len(kp_array)} keypoints for the first player!")

if __name__ == "__main__":
    verify_mens_json()
    print(f"{'='*50}")
    verify_womens_json()
    print(f"{'='*50}")