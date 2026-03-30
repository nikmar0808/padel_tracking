import pandas as pd
import numpy as np
import json
import os
from config import MENS_BALL, MENS_SHOTS, MENS_POSE, WOMENS_BALL, WOMENS_SHOTS, WOMENS_POSE

# Since we have the Labels (CSV) and Annotations (JSON) working, we can build the Mapping Logic. 
# This is the most complex part of the AI pipeline because it translates raw data into a format our model can understand.
# 
# This Unified Data Validator is the "Brain" of our AI pipeline. It will prove that for any given frame (like frame_000022.PNG), 
# we have all the ingredients ready for training: the Shot Type, the Player Skeleton, and the Ball Position.
# The output will be a structured dictionary that can be easily fed into a training loop later on.

# This script "glues" your CSV and JSON data together. 
# where we ensure that every frame we want to train on has the correct labels and annotations.
# Note: The PadelTracker100 dataset uses 'file_name' in the CSV to link to 'image_id' in the JSON.


def get_mens_training_sample(target_frame):
    # --- 1. Load Shot Event (CSV) ---
    if not os.path.exists(MENS_SHOTS):
        return "CSV Missing"
    
    df = pd.read_csv(MENS_SHOTS, sep=';')
    shot_row = df[df['file_name'] == target_frame]
    
    if shot_row.empty:
        return f"Frame {target_frame} not found in CSV."

    # Safely extract the first matching row's values
    is_hit = shot_row.iloc[0]['has_shot']
    category = shot_row.iloc[0]['category']

    # --- 2. Load Ball Position (JSON) ---
    ball_coords = None
    if os.path.exists(MENS_BALL):
        with open(MENS_BALL, 'r') as f:
            ball_data = json.load(f)
        
        # PadelTracker100: Find ball annotation where image_id matches frame name
        ball_anno = next((item for item in ball_data['annotations'] 
                         if str(item.get('image_id')) in target_frame), None)
        
        if ball_anno and 'bbox' in ball_anno:
            bx, by, bw, bh = ball_anno['bbox']
            ball_coords = (bx + bw/2, by + bh/2) # Center of the ball

    # --- 3. Load Player Pose (JSON) ---
    player_keypoints = None
    if os.path.exists(MENS_POSE):
        with open(MENS_POSE, 'r') as f:
            pose_data = json.load(f)
            
        player_anno = next((item for item in pose_data['annotations'] 
                           if str(item.get('image_id')) in target_frame), None)
        
        if player_anno:
            # Reshape flat list [x,y,v, x,y,v...] into [[x,y,v], ...]
            player_keypoints = np.array(player_anno['keypoints']).reshape(-1, 3)

    # --- Print Summary Report ---
    print(f"\n--- 📊 Padel Analysis: {target_frame} ---")
    print(f"Action: {category} | Impact Recorded: {'💥 YES' if is_hit == 1 else 'No'}")
    
    if ball_coords:
        print(f"Ball: ✅ Detected at x={ball_coords[0]:.1f}, y={ball_coords[1]:.1f}")
    else:
        print("Ball: ❌ Not in frame")

    if player_keypoints is not None:
        print(f"Player: ✅ {len(player_keypoints)} Keypoints Found")
    else:
        print("Player: ❌ Pose data missing")

    return {
        "shot_type": category,
        "is_hit": is_hit,
        "ball_xy": ball_coords,
        "skeleton": player_keypoints
    }

def get_womens_training_sample(target_frame):
    # --- 1. Load Shot Event (CSV) ---
    if not os.path.exists(WOMENS_SHOTS):
        return "CSV Missing"
    
    df = pd.read_csv(WOMENS_SHOTS, sep=';')
    shot_row = df[df['file_name'] == target_frame]
    
    if shot_row.empty:
        return f"Frame {target_frame} not found in CSV."

    # Safely extract the first matching row's values
    is_hit = shot_row.iloc[0]['has_shot']
    category = shot_row.iloc[0]['category']

    # --- 2. Load Ball Position (JSON) ---
    ball_coords = None
    if os.path.exists(WOMENS_BALL):
        with open(WOMENS_BALL, 'r') as f:
            ball_data = json.load(f)
        
        # PadelTracker100: Find ball annotation where image_id matches frame name
        ball_anno = next((item for item in ball_data['annotations'] 
                         if str(item.get('image_id')) in target_frame), None)
        
        if ball_anno and 'bbox' in ball_anno:
            bx, by, bw, bh = ball_anno['bbox']
            ball_coords = (bx + bw/2, by + bh/2) # Center of the ball

    # --- 3. Load Player Pose (JSON) ---
    player_keypoints = None
    if os.path.exists(WOMENS_POSE):
        with open(WOMENS_POSE, 'r') as f:
            pose_data = json.load(f)
            
        player_anno = next((item for item in pose_data['annotations'] 
                           if str(item.get('image_id')) in target_frame), None)
        
        if player_anno:
            # Reshape flat list [x,y,v, x,y,v...] into [[x,y,v], ...]
            player_keypoints = np.array(player_anno['keypoints']).reshape(-1, 3)

    # --- Print Summary Report ---
    print(f"\n--- 📊 Padel Analysis: {target_frame} ---")
    print(f"Action: {category} | Impact Recorded: {'💥 YES' if is_hit == 1 else 'No'}")
    
    if ball_coords:
        print(f"Ball: ✅ Detected at x={ball_coords[0]:.1f}, y={ball_coords[1]:.1f}")
    else:
        print("Ball: ❌ Not in frame")

    if player_keypoints is not None:
        print(f"Player: ✅ {len(player_keypoints)} Keypoints Found")
    else:
        print("Player: ❌ Pose data missing")

    return {
        "shot_type": category,
        "is_hit": is_hit,
        "ball_xy": ball_coords,
        "skeleton": player_keypoints
    }

if __name__ == "__main__":
    # Testing with your verified Frame 22
    data_mens = get_mens_training_sample("frame_000022.PNG")
    print(f"{'='*50}")
    data_womens = get_womens_training_sample("frame_000045.PNG")
    print(f"{'='*50}")