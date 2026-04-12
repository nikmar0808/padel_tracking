import os
import random
import shutil
from pathlib import Path

from config_training import ANNOT_BATCHES_DIR, MANUAL_ANNOT_DIR, MANUAL_ANNOT_TEMP_DIR, AUTO_ANNOT_TEMP_DIR, AUTO_ANNOT_CORRECTED_DIR, TRNG_LABELS_DIR, TRNG_IMAGES_DIR, VAL_LABELS_DIR, VAL_IMAGES_DIR

def split_dataset(batch_name):
    def copy_corrected_annotations(lbl_src_dir, temp_dir):
        os.makedirs(lbl_src_dir, exist_ok=True)
        files_copied = 0
        # Iterate through all files in the temp folder
        for filename in os.listdir(temp_dir):
            # Filter for .txt files
            if filename.endswith(".txt"):
                temp_path = os.path.join(temp_dir, filename)

                try:
                    shutil.copy(temp_path, lbl_src_dir)
                    print(f"Copied: {filename}")
                    files_copied += 1
                except Exception as e:
                    print(f"Error copying {filename}: {e}")
        print(f"\nTotal files copied: {files_copied} from {temp_corrected_dir} to {lbl_src}")
    
    # Source Image directories
    img_src = Path(ANNOT_BATCHES_DIR) / batch_name
    if batch_name == 'batch_0':
        temp_corrected_dir = Path(MANUAL_ANNOT_TEMP_DIR)
        if not temp_corrected_dir.exists():
            print(f"Warning: Temp corrected directory not found for {batch_name}. Ensure that a folder named temp_manual_corrected exists.")
            return
        # Source Label directories
        lbl_src = Path(MANUAL_ANNOT_DIR) / batch_name
        copy_corrected_annotations(lbl_src, temp_corrected_dir)
    else:
        temp_corrected_dir = Path(AUTO_ANNOT_TEMP_DIR)
        if not temp_corrected_dir.exists():
            print(f"Warning: Temp corrected directory not found for {batch_name}. Ensure that a folder named temp_auto_corrected exists.")
            return
        # Source Label directories
        lbl_src = Path(AUTO_ANNOT_CORRECTED_DIR) / batch_name  # Adjust if you want to include more batches
        copy_corrected_annotations(lbl_src, temp_corrected_dir)

    # Destination directories
    train_img_out = Path(TRNG_IMAGES_DIR)
    val_img_out = Path(VAL_IMAGES_DIR)
    train_lbl_out = Path(TRNG_LABELS_DIR)
    val_lbl_out = Path(VAL_LABELS_DIR)

    # Check if source directories actually exist before proceeding
    if not os.path.exists(img_src) or not os.path.exists(lbl_src):
        print(f"Error: One or both source directories do not exist:\n - {img_src}\n - {lbl_src}")
        print(f"Make sure the batch name is correct (format - batch_n) and that the annotation process has been completed for this batch.")
        return
    
    # Create all output directories
    for d in [train_img_out, val_img_out, train_lbl_out, val_lbl_out]:
        os.makedirs(d, exist_ok=True)

    # Get set of filenames without extensions to find matches
    images = {os.path.splitext(f)[0] for f in os.listdir(img_src) if f.lower().endswith('.png')}
    labels = {os.path.splitext(f)[0] for f in os.listdir(lbl_src) if f.lower().endswith('.txt')}
    
    # Intersect to find pairs that exist in both locations
    matched_pairs = list(images.intersection(labels))
    
    if not matched_pairs:
        print("No matching .PNG and .txt pairs found.")
        return

    random.shuffle(matched_pairs)
    
    # Calculate 80/20 split
    split_idx = int(len(matched_pairs) * 0.8)
    train_list = matched_pairs[:split_idx]
    val_list = matched_pairs[split_idx:]

    def copy_corrected_annotations():
        files_copied = 0
        # Iterate through all files in the source folder
        for filename in os.listdir(AUTO_ANNOT_TEMP_DIR):
            # Filter for .txt files
            if filename.endswith(".txt"):
                src_path = os.path.join(AUTO_ANNOT_TEMP_DIR, filename)
                dst_path = os.path.join(AUTO_ANNOT_CORRECTED_DIR, batch_name, filename)
                
                try:
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied: {filename}")
                    files_copied += 1
                except Exception as e:
                    print(f"Error copying {filename}: {e}")
        
        print(f"\nTask complete. Total files copied: {files_copied}")

    def process_files(file_list, img_dest, lbl_dest):
        for base in file_list:
            # Handle potential PNG case sensitivity
            img_ext = ".png" if os.path.exists(os.path.join(img_src, f"{base}.png")) else ".PNG"
            
            shutil.copy(os.path.join(img_src, base + img_ext), os.path.join(img_dest, base + img_ext))
            shutil.copy(os.path.join(lbl_src, base + ".txt"), os.path.join(lbl_dest, base + ".txt"))

    # Execute copies
    process_files(train_list, train_img_out, train_lbl_out)
    process_files(val_list, val_img_out, val_lbl_out)

    print(f"Split complete: {len(train_list)} pairs in train, {len(val_list)} pairs in val.")

if __name__ == "__main__":
    # Get user input from the terminal
    user_batch_name = input("Enter the batch name (e.g., batch_0): ").strip()
    
    if user_batch_name:
        split_dataset(user_batch_name)
    else:
        print("No batch name entered. Exiting.")