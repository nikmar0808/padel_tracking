# padel_tracking
Git Repo for Padel Tracking application

Setup Instructions
------------------
Step 1:
Python, MiniConda installation
Create Project Root Directory - PADEL_TRACKING
PADEL_TRACKING/
│
├── configs/
│
├── core/
│   ├── analytics/
│   ├── data/
│   ├── inference/
│   └── training/
│
├── data/
│   ├── interim/
│   │   └── annotation_batches/
│   │   │   └── batch_0/
│   │   │   └── batch_1/
│   │   │   └── batch_n/
│   │   └── annotations/
│   │   │   └── auto/
│   │   │   │   └── batch_1/
│   │   │   │   └── batch_n/
│   │   │   └── manual/
│   │   │   │   └── batch_0/
│   │   └── extracted_frames/
│   │   └── sampled_frames/
│   │
│   ├── processed/
│   │   ├── images/
│   │   │   └── train/
│   │   │   └── val/
│   │   └── labels/
│   │   │   └── train/
│   │   │   └── val/
│   │
│   ├── raw/
│   │   └── source_videos/
│   │
│   └── annotations/
│
├── models/
│
├── notebooks/
│
├── scripts/
│
├── tests/
│
├── requirements.txt
│
└── README.md

Step 2:
Create venv padel_tracking_env PADEL_TRACKING
Activate environment

pip install packages as per requirements.txt

Usage
-----
It is important to run the below scripts in the specified order
1. Place match videos under raw/source_videos
2. Edit video file name in config_training.py under core/training folder
3. Run extract_frames.py
4. Run sample_frames.py
5. Run create_annotations_batches.py
6. Open https://app.cvat.ai
    a. Create Project - call is "padel_tracking"
       Add Labels - "ball" and "player" of Type "Rectangle" of different colors
       Click Submit & Open
    b. Create Task - call it "padel_ball_player_detection_seed", Select Project "padel_tracking",
       Add files from data/interim/annotation_batches/batch_0
       Under Advanced configuration -> Lexicographical, set Overlap size = 0, Segment size = 500
       Click Submit & Open
    c. Once finished, Go to Tasks and Open the task created
       Click on hyperlinked Job ID under Jobs. This should open the uploaded images.
       Click on the Rectangle Shape from the toolbar on the left hand side
       Select Label "ball", Drawing method "By 2 points" and "Shape" and create tightly bounded boxes around the ball in all images, keep clicking Save on top.
       Select Label "player", Drawing method "By 2 points" and "Track". Create bounded boxes around each player on Frame 1 and skip next few frame to a frame
       where the players have significantly moved outside the bounded boxes and adjust, then again skip and repeat. This method saves a lot of time.
    d. Once finished, Go to Actions and Export task dataset. Once prompted, Download it locally.
7. Extract the zip file data/interim/annotations and rename it to manual_annotations
8. Run prepare_train_val_img_label_folders.py
   data/processed/images/train and data/processed/labels/train folders should each have 240 files from batch_0
   data/processed/images/val and data/processed/labels/val folders should each have 60 files from batch_0
9. Run check_training_dataset.py

START THE SEED TRAINING PROCESS - WHILE THE FIRST RUN MAY FINISH IN 3-4HOURS, LATER RUNS CAN TAKE 10-12 HOURS IF NOT BEING RUN ON A GPU.
EACH SUBSEQUENT RUN TAKES LONGER AND LONGER AS WE INCREASE THE NUMBER OF TRAINING FILES AND EPOCHS.

10. Open train_seed_model.py 
    a. Ensure model = YOLO("yolov8n.pt")
    b. Once finished, Go to runs/detect/ and rename folder "train" to "train_batch0_ball_player"
    c. Under this folder, Go to weights/ and look for the training model file called "best.pt". Rename this is "best_batch0_ball_player.pt".

Once finished, START THE RETRAINING PROCESS. This involves repeating Steps 11-17. Note these are slightly different that the Seed Training Steps.

11. Open auto_annotate.py and edit the path of the model to be used
   e.g. for batch_1 - runs\detect\train_batch0_ball_player\weights\best_batch0_ball_player.pt
   e.g. for batch_2 - runs\detect\train_batch1_ball_player\weights\best_batch1_ball_player.pt
   Run the script and type batch_n when prompted for input value at the terminal.
12. Run build_cvat_annotations_batches.py
13. Open https://app.cvat.ai.
    a. Create Task - call it "padel_ball_player_detection_batch_n", Select Project "padel_tracking",
       Add files from data/interim/annotation_batches/batch_n
       Under Advanced configuration -> Lexicographical, set Overlap size = 0, Segment size = 500
       Click Submit & Open
    b. Once finished, Go to Tasks. Go to Actions of the created task and Click on Upload Annotations
       Select  Import Format as "YOLO 1.1" and upload the zip file from data/interim/annotation_batches/batch_n
    c. Once finished, Open the task created.
       Click on hyperlinked Job ID under Jobs. This should open the uploaded images.
    d. Verify and Add/Remove/Modify the labels as applicable and Save.
    e. Go to Tasks, Got to Actions of the task and Click on Export Task Dataset
    Select Export Format as "YOLO 1.1" and Click Ok.
    f. On confirmation message, Go to Requests and Click on Three Vertical dots (Action) of that request and Click Download to save the file.
14. Extract the zip file under data/interim/annotations/ and rename the extracted folder to temp_auto_corrected.
       Open data/interim/annotations/temp_auto_corrected/obj_train_data, copy the .txt label files
       and paste them inside data/interim/annotations/auto_corrected/batch_n folder
15. Run prepare_train_val_img_label_folders.py
    data/processed/images/train and data/processed/labels/train folders should each have 480 files (240 files from batch_0 and 240 files from batch_1)
    data/processed/images/val and data/processed/labels/val folders should each have 120 files (60 files from batch_0 and 60 files from batch_1)
16. Run check_training_dataset.py
17. Open retrain_model.py
    a. Ensure
       model = YOLO(r'runs\detect\train_batch0_ball_player\weights\best_batch0_ball_player.pt') generated after Step 10.c for training batch1 and batch0 combined.cz
       model = YOLO(r'runs\detect\train_batch1_ball_player\weights\best_batch1_ball_player.pt') generated after Step 18 for training batch2, batch1 and batch0 combined
    b. Once finished, Go to runs/detect/ and rename folder "train" to "train_batch1_ball_player" or "train_batch2_ball_player" and so on
    c. Under this folder, Go to weights/ and rename the training model file called "best.pt" to "best_batch1_ball_player.pt", "best_batch2_ball_player.pt" and so on.
    
Repeat Steps 11-17.

Notes for performance improvements for laptop with Core i7-13620H CPU, no dedicated NVDIA GPU

Training on an Intel i7-13620H without a dedicated NVIDIA GPU, means the system defaults to the CPU for YOLO training. The "Shared GPU Memory" seen in Task Manager (7.8GB) is system RAM that the Intel UHD Graphics chip could use for display tasks, but standard YOLO frameworks (like Ultralytics) cannot use this shared memory for training out-of-the-box. [1, 2]

To bridge this gap and optimize our computer vision performance, we should switch to tools designed for Intel hardware. [3]

## 1. Enable Intel-Specific Training Optimizations
Standard PyTorch is built for NVIDIA GPUs. To utilize your Intel hardware efficiently, install the Intel Extension for PyTorch (IPEX). [2] 

* What it does: It allows PyTorch to use "AVX-512" and "AMX" instructions on your i7-13620H, which are specifically designed to speed up AI math on the CPU.
* Installation: You typically need a specific version of PyTorch. Follow the Intel Installation Guide to match your environment.

## 2. Optimize for Integrated GPU (iGPU) with OpenVINO [4] 
While standard YOLO training is CPU-heavy, you can technically offload parts of the workload or perform high-speed testing on your integrated Intel UHD Graphics using the OpenVINO toolkit.

* Export for Performance: Once you have a base model, export it to the OpenVINO format to run it up to 3x faster on your laptop's CPU and iGPU compared to standard PyTorch.
* Usage:

from ultralytics import YOLOmodel = YOLO("yolo11n.pt")
model.export(format="openvino") # This optimizes the model for your i7-13620H

[2, 5, 6] 

## 3. Increase "VRAM" via BIOS or Intel Settings [7] for Inference (not for Model Training)
Since your Task Manager shows only 0.8GB being used, you can force the system to permit more RAM for the GPU, though this primarily helps with inference (running the model) rather than the actual training process. [8] 

* Intel Graphics Command Center: Check the "Shared GPU Memory Override" feature in newer [Intel Graphics Drivers](https://www.intel.com/content/www/us/en/support/articles/000101789/graphics.html). This allows you to balance memory between the CPU and GPU.
* BIOS Allocation: Restart your laptop and enter the BIOS (usually F2 or Del). Look for "Integrated Graphics Share Memory" or "DVMT Pre-Allocated" and set it to a higher value (e.g., 512MB or 1024MB) to ensure the hardware is ready for larger datasets. [9, 10, 11] 

## 4. Training Parameter Adjustments
Without a dedicated GPU, your primary bottleneck is Memory Bandwidth. [12] 

* Batch Size: Keep it small (e.g., batch=8 or batch=16). Large batches on a CPU cause "cache thrashing," which slows down training significantly.
* Half Precision: Use half=True during testing/inference. Modern Intel CPUs can handle 16-bit floats (FP16) much faster than standard 32-bit.
* Workers: On your i7-13620H (which has 10 cores), set workers=4 or 8 in your training script. Setting this too high on a CPU-only setup can actually slow you down by creating too much management overhead. [3, 10, 13] 

Would you like the PowerShell commands to verify if your current Python environment is correctly seeing the Intel optimization libraries?

[1] [https://www.youtube.com](https://www.youtube.com/watch?v=_YnlcbO-Eag)
[2] [https://github.com](https://github.com/ultralytics/ultralytics/issues/19821)
[3] [https://www.youtube.com](https://www.youtube.com/watch?v=AvFh-oTGDaw)
[4] [https://learnopencv.com](https://learnopencv.com/running-openvino-models-on-intel-integrated-gpu/)
[5] [https://www.youtube.com](https://www.youtube.com/watch?v=kONm9nE5_Fk)
[6] [https://www.ultralytics.com](https://www.ultralytics.com/blog/achieve-faster-inference-speeds-ultralytics-yolov8-openvino)
[7] [https://www.intel.com](https://www.intel.com/content/www/us/en/support/articles/000041253/graphics.html)
[8] [https://superuser.com](https://superuser.com/questions/1729847/how-do-i-change-shared-system-memory-for-gpu-in-windows-11-without-bios)
[9] [https://www.intel.com](https://www.intel.com/content/www/us/en/support/articles/000101789/graphics.html)
[10] [https://learn.microsoft.com](https://learn.microsoft.com/en-us/answers/questions/5706477/how-to-increase-dedicated-video-memory)
[11] [https://www.wikihow.com](https://www.wikihow.com/Increase-Dedicated-Video-RAM-on-Windows-Laptops-with-Intel-Graphics)
[12] [https://www.quora.com](https://www.quora.com/How-can-I-increase-the-shared-graphics-memory-of-my-integrated-graphics-card-in-my-laptop-My-current-video-memory-is-32-MB-But-I-have-8-GB-of-RAM-so-I-have-no-problem-even-if-I-have-to-share-3-5-GB-of-RAM-Is-there)
[13] [https://docs.ultralytics.com](https://docs.ultralytics.com/guides/model-training-tips/)
