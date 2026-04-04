import numpy as np
import cv2
import matplotlib.pyplot as plt
from scripts.padel100.data_mapper import get_mens_training_sample, get_womens_training_sample

# 1. Load your CUSTOM Homography Matrix
H = np.load('my_court_homography.npy')

def get_mens_metric_pos(pixel_x, pixel_y):
    # Transform [pixel_x, pixel_y] -> [meters_x, meters_y]
    point = np.array([[[pixel_x, pixel_y]]], dtype=np.float32)
    metric = cv2.perspectiveTransform(point, H)
    return metric[0][0]

def get_womens_metric_pos(pixel_x, pixel_y):
    # Transform [pixel_x, pixel_y] -> [meters_x, meters_y]
    point = np.array([[[pixel_x, pixel_y]]], dtype=np.float32)
    metric = cv2.perspectiveTransform(point, H)
    return metric[0][0]

# 2. Track the player for 500 frames
path_x, path_y = [], []
print("📍 Calculating player movement...")

for i in range(100, 600):
    frame_name = f"mens_frame_{i:06d}.PNG"
    data = get_mens_training_sample(frame_name)
    
    if data['skeleton'] is not None:
        # Use the "Ankle" keypoints (usually indices 15 and 16 in COCO)
        # We take the average of the feet as the ground position
        left_foot = data['skeleton'][15]
        right_foot = data['skeleton'][16]
        
        avg_x = (left_foot[0] + right_foot[0]) / 2
        avg_y = (left_foot[1] + right_foot[1]) / 2
        
        # Convert to Meters
        mx, my = get_mens_metric_pos(avg_x, avg_y)
        path_x.append(mx)
        path_y.append(my)

# 3. Plot the Heatmap
plt.figure(figsize=(6, 10))
plt.hist2d(path_x, path_y, bins=[20, 40], range=[[0, 10], [0, 20]], cmap='hot')
plt.colorbar(label='Time Spent (Frames)')
plt.title("Player Heatmap (Meters)")
plt.xlabel("Width (m)")
plt.ylabel("Length (m)")
plt.show()
