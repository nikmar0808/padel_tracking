import cv2
import os
from config_training import VIDEO_FILE, EXTRACTED_FRAMES_DIR, FPS

def extract_frames_opencv(video_filename, output_folder, target_fps=FPS):
    print(f"✅ Start! Extracting frames to {output_folder}")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_filename)
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_filename}")
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
        if int(frame_count * (target_fps / orig_fps)) >= saved_count:
            # Save frame BEFORE incrementing to start frame filename at 000000 in order to match BALL, POSE, and SHOT data
            # in CSV and JSON files which also start at 000000 
            filename = os.path.join(output_folder, f"frame_{saved_count:06d}.png")
            cv2.imwrite(filename, frame)
            saved_count += 1 # Increment for the next loop
            if saved_count % 1000 == 0:
                print(f"🖼️ Saved {saved_count} mens frames...")
        frame_count += 1

    cap.release()
    print(f"✅ Finished! Extracted {saved_count} frames to {output_folder}")

if __name__ == "__main__":
    # Start with the Men's Final
    extract_frames_opencv(VIDEO_FILE, EXTRACTED_FRAMES_DIR)
    print(f"{'='*50}")
    # Then process the Women's Final
    