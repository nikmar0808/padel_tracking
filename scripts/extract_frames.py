import cv2
import os
from config import MENS_VIDEO, WOMENS_VIDEO, VIDEO_DIR, FRAME_DIR

def extract_mens_frames_opencv(video_filename, output_folder, target_fps=30):
    video_path = os.path.join(VIDEO_DIR, video_filename)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_path}")
        return

    # Get original video properties
    orig_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"🎥 Original Video FPS: {orig_fps}")

    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calculate if we should keep this frame to match target_fps
        # If original is 60 and target is 30, we save every 2nd frame
        if int(frame_count * (target_fps / orig_fps)) > saved_count:
            saved_count += 1
            filename = os.path.join(output_folder, f"mens_frame_{saved_count:06d}.png")
            cv2.imwrite(filename, frame)
            
            if saved_count % 1000 == 0:
                print(f"🖼️ Saved {saved_count} frames...")
        
        frame_count += 1

    cap.release()
    print(f"✅ Finished! Extracted {saved_count} frames to {output_folder}")

def extract_womens_frames_opencv(video_filename, output_folder, target_fps=30):
    video_path = os.path.join(VIDEO_DIR, video_filename)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_path}")
        return

    # Get original video properties
    orig_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"🎥 Original Video FPS: {orig_fps}")

    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calculate if we should keep this frame to match target_fps
        # If original is 60 and target is 30, we save every 2nd frame
        if int(frame_count * (target_fps / orig_fps)) > saved_count:
            saved_count += 1
            filename = os.path.join(output_folder, f"womens_frame_{saved_count:06d}.png")
            cv2.imwrite(filename, frame)
            
            if saved_count % 1000 == 0:
                print(f"🖼️ Saved {saved_count} frames...")
        
        frame_count += 1

    cap.release()
    print(f"✅ Finished! Extracted {saved_count} frames to {output_folder}")

if __name__ == "__main__":
    # Start with the Men's Final
    extract_mens_frames_opencv(MENS_VIDEO, FRAME_DIR)
    print(f"{'='*50}")
    # Then process the Women's Final
    extract_womens_frames_opencv(WOMENS_VIDEO, FRAME_DIR)
    print(f"{'='*50}")
    
