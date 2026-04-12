import os
import shutil
from pathlib import Path
from ultralytics import YOLO
from config_training import (
    ANNOT_BATCHES_DIR, AUTO_ANNOT_DIR, AUTO_ANNOT_CONFIDENCE_THRESHOLD, 
    AUTO_ANNOT_IOU_THRESHOLD, AUTO_ANNOT_IMAGE_SIZE
)

def annotate_batch(batch_name):
    if batch_name == 'batch_0':
        print("Batch 0 is reserved for manual annotation. Skipping auto-annotation for this batch.")
        return
    # 1. Configuration
    model = YOLO(r'runs\detect\train_batch2_ball_player\weights\best_batch2_ball_player.pt')
    input_base = ANNOT_BATCHES_DIR
    output_base = AUTO_ANNOT_DIR
    conf_threshold = AUTO_ANNOT_CONFIDENCE_THRESHOLD
    iou_threshold = AUTO_ANNOT_IOU_THRESHOLD
    image_size = AUTO_ANNOT_IMAGE_SIZE

    # 2. Identify target batches
    all_folders = [f for f in os.listdir(input_base) if os.path.isdir(os.path.join(input_base, f))]
    # target_batches = [f for f in all_folders if f.lower().startswith('batch_') 
    #                   and f.lower() != 'batch_0' and f.lower() != 'batch_1'
    #                   and f.lower() != 'batch_2' and f.lower() != 'batch_3' and f.lower() != 'batch_4' 
    #                   and f.lower() != 'batch_5' and f.lower() != 'batch_6' and f.lower() != 'batch_7' 
    #                   and f.lower() != 'batch_8' and f.lower() != 'batch_9' and f.lower() != 'batch_10' 
    #                   and f.lower() != 'batch_11' and f.lower() != 'batch_12' and f.lower() != 'batch_13' and f.lower() != 'batch_14' and f.lower() != 'batch_15'
    #                   and f.lower() != 'batch_16' and f.lower() != 'batch_17']
    target_batches = [f for f in all_folders if f.lower().endswith(batch_name.lower())]
    
    # 3. Process each batch
    for batch_name in sorted(target_batches):
        batch_input_dir = os.path.abspath(os.path.join(input_base, batch_name))
        batch_output_dir = os.path.abspath(os.path.join(output_base, batch_name))
            # Check if source directories actually exist before proceeding
        if not os.path.exists(batch_input_dir):
            print(f"Error: Source directory does not exist:\n - {batch_input_dir}")
            print(f"Make sure the batch name is correct (format - batch_n)")
            return
        os.makedirs(batch_output_dir, exist_ok=True)
        
        print(f"--- Auto-annotating {batch_name} ---")
        
        # Run prediction
        results = model.predict(
            source=batch_input_dir, 
            conf=conf_threshold,
            iou=iou_threshold,
            imgsz=image_size,
            save_txt=True, 
            project='temp_yolo_out', 
            name='current_batch',
            exist_ok=True
        )
        
        # FIX: Get the actual save directory from the first result object in the list
        # Use .resolve() to handle absolute pathing correctly on Windows
        actual_predict_dir = Path(results[0].save_dir).resolve()
        temp_label_dir = actual_predict_dir / 'labels'
        
        all_images = [img for img in os.listdir(batch_input_dir) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(f"Found {len(all_images)} images. Matching labels from {temp_label_dir}...")

        for img_name in all_images:
            # Use .stem to avoid issues with double extensions (e.g. image.1.jpg)
            label_filename = Path(img_name).stem + ".txt"
            source_label = temp_label_dir / label_filename
            target_label = os.path.join(batch_output_dir, label_filename)
            print(f"Processing {img_name} -> {label_filename} -> source_label.exists(): {source_label.exists()}")
            if source_label.exists():
                shutil.move(str(source_label), target_label)
            else:
                # Create an empty file for 1:1 parity
                with open(target_label, 'w') as f:
                    pass

        print(f"Completed {batch_name}. Labels stored at {batch_output_dir}")

        # Cleanup the temp directory after the loop
        if os.path.exists('temp_yolo_out'):
            shutil.rmtree('temp_yolo_out')

if __name__ == "__main__":
    # Get user input from the terminal
    user_batch_name = input("Enter the batch name (e.g., batch_1): ").strip()
    
    if user_batch_name:
        annotate_batch(user_batch_name)
    else:
        print("No batch name entered. Exiting.")
