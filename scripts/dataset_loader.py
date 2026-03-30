import pandas as pd
import json
import os
from config import MENS_SHOTS, MENS_POSE, WOMENS_SHOTS, WOMENS_POSE

def get_mens_shot_details(frame_name):
    # 1. Load the CSV
    df = pd.read_csv(MENS_SHOTS, sep=';')
    
    # 2. Find the specific frame info
    frame_info = df[df['file_name'] == frame_name]
    
    if frame_info.empty:
        return "Frame not found in CSV"

    shot_type = frame_info.iloc[0]['category']
    is_shot = frame_info.iloc[0]['has_shot']

    # 3. Load the JSON for player coordinates
    with open(MENS_POSE, 'r') as f:
        pose_data = json.load(f)
    
    # Find the pose that matches this frame_name (image_id)
    # PadelTracker100 uses image_id to link frames to poses
    matching_pose = next((item for item in pose_data['annotations'] 
                         if item["image_id"] == frame_name), None)

    return {
        "frame": frame_name,
        "is_shot": is_shot,
        "type": shot_type,
        "has_pose": matching_pose is not None
    }

def get_womens_shot_details(frame_name):
    # 1. Load the CSV
    df = pd.read_csv(WOMENS_SHOTS, sep=';')
    
    # 2. Find the specific frame info
    frame_info = df[df['file_name'] == frame_name]
    
    if frame_info.empty:
        return "Frame not found in CSV"

    shot_type = frame_info.iloc[0]['category']
    is_shot = frame_info.iloc[0]['has_shot']

    # 3. Load the JSON for player coordinates
    with open(WOMENS_POSE, 'r') as f:
        pose_data = json.load(f)
    
    # Find the pose that matches this frame_name (image_id)
    # PadelTracker100 uses image_id to link frames to poses
    matching_pose = next((item for item in pose_data['annotations'] 
                         if item["image_id"] == frame_name), None)

    return {
        "frame": frame_name,
        "is_shot": is_shot,
        "type": shot_type,
        "has_pose": matching_pose is not None
    }

# Test it for a known shot frame (from the previous output)
# Note: Make sure "frame_000022.PNG" is actually a frame with a shot in the CSVs for accurate testing
# If not, replace "frame_000022.PNG" with a frame name that has a shot event in the CSVs
# This will print the details for that specific frame, including whether it's a shot and if pose data exists for it
#
# Currently, frame_000022.PNG does not exist on the computer.
# It only exists as a row in the CSV file (the label). To actually "see" the image, we have to create it from the source video once we get permission to download it.
# 
# The "Missing Link" in the PadelTracker100 Setup:
#
# 1. Labels (we have these): The CSV and JSON files tell us that at "Frame 22," a player is performing a Serve.
# 2. Video (we are waiting for this): The 2022 Barcelona Master Final .mp4 file.
# 3. Extraction (The step we need to do next): we will use FFmpeg to "chop" that video into thousands of individual images.
# 
# Once we have the video, we can run a script to extract frames like this:
# ffmpeg -i 2022_BCN_FinalM_1.mp4 -vf "select=not(mod(n\,30))" -vsync vfr Frames/frame_%06d.PNG
# or
# ffmpeg -i data/Source_Videos/mens_final.mp4 -vf "fps=30" -q:v 2 data/Frames/frame_%06d.png
# Note: The above FFmpeg command assumes the video is named "2022_BCN_FinalM_1.mp4" and is located in the correct directory as specified in config.py.
# Adjust the command if the video has a different name or location.

# What this command does:
# -vf "fps=30": It ensures that for every 1 second of video, it creates exactly 30 images. This is critical because our CSV says the shot is at "Frame 22." If we extract at 60 FPS,
#  Frame 22 would be the wrong moment!
# frame_%06d.png: It names the files frame_000001.png, frame_000002.png, etc.


# This command extracts one frame every second (since the video is 30 FPS) and saves them as PNGs in the Frames directory. The naming convention will be frame_000001.PNG, 
# frame_000002.PNG, etc.
# After we have the frames, we can run this dataset_loader.py script to check if the frame names in the CSV match the actual image files and if the pose data is linked correctly.
# 
print(get_mens_shot_details("frame_000022.PNG"))
print(f"{'='*50}")
print(get_womens_shot_details("frame_000045.PNG"))
print(f"{'='*50}")