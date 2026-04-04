import cv2
import numpy as np
import os
from config import FRAME_DIR

# 1. Define the real-world court size (Standard Padel: 10m x 20m)
# We map pixels to these coordinates
COURT_METERS = np.float32([
    [0, 0],   # Top Left
    [10, 0],  # Top Right
    [10, 20], # Bottom Right
    [0, 20]   # Bottom Left
])

clicked_pts = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_pts.append([x, y])
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Calibrate Court", img)
        if len(clicked_pts) == 4:
            print("✅ 4 Corners selected!")

# Load your first extracted frame
img_path = os.path.join(FRAME_DIR, 'mens_frame_000000.PNG')
img = cv2.imread(img_path)

if img is None:
    print(f"❌ Could not find {img_path}")
else:
    print("Click the 4 corners: Top-Left, Top-Right, Bottom-Right, Bottom-Left")
    cv2.imshow("Calibrate Court", img)
    cv2.setMouseCallback("Calibrate Court", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(clicked_pts) == 4:
        # 2. Calculate the Homography Matrix
        src_pts = np.float32(clicked_pts)
        H, status = cv2.findHomography(src_pts, COURT_METERS)
        
        # 3. Save the matrix for future use
        np.save('my_court_homography.npy', H)
        print("💾 Matrix saved as 'my_court_homography.npy'")
