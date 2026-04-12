from datetime import datetime
import os
import torch

# The Ultralytics YOLO framework automatically imports and utilizes PyTorch modules to build our model.
# It is the default engine used for all training, model definitions, and tensor operations.
from ultralytics import YOLO
from config_training import TRNG_DATASET_PATHS, RETRAIN_EPOCHS, IMG_SIZE, BATCH_SIZE, DATALOADER_WORKERS

print("Starting retraining at timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Force the CPU to use more "Physical" power for math operations.
# Optimize Intel CPU Math Performance by targeting the 6 Performance Cores (P-Cores) for matrix math,
# which can significantly speed up training on CPU.
# This can help speed up training but be mindful of the increased power consumption and heat generation.
# Using 8 threads to fully saturate 6 P-Cores and utilize E-core headroom.
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["MKL_NUM_THREADS"] = "8"
torch.set_num_threads(8)
torch.set_num_interop_threads(8) # Enables parallel task scheduling across multiple CPU cores, which can further improve performance during data loading and training on CPU.

def train_model():
    
    model = YOLO(r'runs\detect\train_batch2_ball_player\weights\best_batch2_ball_player.pt')

    model.train(
        # Essential Paths and Hyperparameters
        data=TRNG_DATASET_PATHS,

        # Baseline Stability
        epochs=RETRAIN_EPOCHS,
        batch=BATCH_SIZE, # 8 for 16GB RAM with CPU training, can be increased if GPU memory is available (e.g., 16 for 16GB VRAM)
        device=0 if torch.cuda.is_available() else 'cpu',
        
        # Performance Tuning for  CPU Training and better usage
        workers=DATALOADER_WORKERS,  # Force 4 parallel image loaders, reduce if CPU starvation occurs or performance worsens
        cache=False, # True if there is RAM headroom to leverage and store the dataset in memory for faster access, False to read from disk each epoch (safer for large datasets)
        amp=False,   # Disable Mixed Precision (AMP is for GPUs; can be slower on CPU)

        # THE SPEED FIX:
        # Standard training forces every image into a square (padding your rectangular images with empty black space).
        # rect=True allows the CPU to process the images in their native rectangular aspect ratio.
        rect=True, # Disable square resizing and padding, which can significantly speed up training on CPU by avoiding unnecessary computations on padded areas, especially for rectangular images. This allows the model to learn from the actual content of the images without being slowed down by processing large amounts of empty space.

        # High Resolution for small ball detection
        imgsz=IMG_SIZE,
        mosaic=1.0, # Mosaic augmentation works by stitching four images together, which forces the model to learn to find the ball at different scales and in different positions
        iou=0.7, # Higher IoU threshold for positive anchor assignment during retraining to focus on harder examples and improve precision, can be dropped to 0.5 during inference for better recall

        project="padel_tracking",
        name="train_batch3_ball_player"
    )

    print("Model saved to:", model.__dir__())

if __name__ == '__main__':
    train_model()
    print("Retraining complete! at timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
