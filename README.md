# padel_tracking
Git Repo for Padel Tracking application

![Python Version](https://shields.io)
![Build Status](https://shields.io)
![License](https://shields.io)

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Seed Training Process](#seed-training-process)
- [Retraining Process](#retraining-process)

## Setup Instructions
------------------
### Step 1:
Python, MiniConda installation
Create Project Root Directory - PADEL_TRACKING

~~~text
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
~~~

### Step 2:
Create venv `padel_tracking_env` PADEL_TRACKING  
Activate environment  
`pip install -r requirements.txt`

## Usage
------------------
It is important to run the below scripts in the specified order:
1. Place match videos under `raw/source_videos`
2. Edit video file name in `config_training.py` under `core/training` folder
3. Run `extract_frames.py`
4. Run `sample_frames.py`
5. Run `create_annotations_batches.py`
6. **Open CVAT ([https://app.cvat.ai](https://app.cvat.ai/))**
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
7. Extract the zip file `data/interim/annotations` and rename it to `manual_annotations`
8. Run `prepare_train_val_img_label_folders.py`
   `data/processed/images/train` and `data/processed/labels/train` folders should each have 240 files from batch_0
   `data/processed/images/val` and `data/processed/labels/val` folders should each have 60 files from batch_0
9. Run `check_training_dataset.py`

## Seed Training Process
------------------
**START THE SEED TRAINING PROCESS** - WHILE THE FIRST RUN MAY FINISH IN 3-4 HOURS, LATER RUNS CAN TAKE 10-12 HOURS IF NOT BEING RUN ON A GPU.
EACH SUBSEQUENT RUN TAKES LONGER AND LONGER AS WE INCREASE THE NUMBER OF TRAINING FILES AND EPOCHS.

10. Open `train_seed_model.py` 
    a. Ensure `model = YOLO("yolov8n.pt")`
    b. Once finished, Go to `runs/detect/` and rename folder "train" to "train_batch0_ball_player"
    c. Under this folder, Go to `weights/` and look for the training model file called "best.pt". Rename this is "best_batch0_ball_player.pt".

## Retraining Process
------------------
Once finished, START THE RETRAINING PROCESS. This involves repeating Steps 11-17. Note these are slightly different that the Seed Training Steps.

11. Open `auto_annotate.py` and edit the path of the model to be used
   e.g. for batch_1 - `runs\detect\train_batch0_ball_player\weights\best_batch0_ball_player.pt`
   e.g. for batch_2 - `runs\detect\train_batch1_ball_player\weights\best_batch1_ball_player.pt`
   Run the script and type `batch_n` when prompted for input value at the terminal.
12. Run `build_cvat_annotations_batches.py`
13. **Open CVAT ([https://app.cvat.ai/](https://app.cvat.ai/))**
    a. Create Task - call it "padel_ball_player_detection_batch_n", Select Project "padel_tracking",
       Add files from `data/interim/annotation_batches/batch_n`
       Under Advanced configuration -> Lexicographical, set Overlap size = 0, Segment size = 500
       Click Submit & Open
    b. Once finished, Go to Tasks. Go to Actions of the created task and Click on Upload Annotations
       Select Import Format as "YOLO 1.1" and upload the zip file from `data/interim/annotation_batches/batch_n`
    c. Once finished, Open the task created.
       Click on hyperlinked Job ID under Jobs. This should open the uploaded images.
    d. Verify and Add/Remove/Modify the labels as applicable and Save.
    e. Go to Tasks, Got to Actions of the task and Click on Export Task Dataset
    Select Export Format as "YOLO 1.1" and Click Ok.
    f. On confirmation message, Go to Requests and Click on Three Vertical dots (Action) of that request and Click Download to save the file.
14. Extract the zip file under `data/interim/annotations/` and rename the extracted folder to `temp_auto_corrected`.
       Open `data/interim/annotations/temp_auto_corrected/obj_train_data`, copy the .txt label files
       and paste them inside `data/interim/annotations/auto_corrected/batch_n` folder
15. Run `prepare_train_val_img_label_folders.py`
    `data/processed/images/train` and `data/processed/labels/train` folders should each have 480 files (240 files from batch_0 and 240 files from batch_1)
    `data/processed/images/val` and `data/processed/labels/val` folders should each have 120 files (60 files from batch_0 and 60 files from batch_1)
16. Run `check_training_dataset.py`
17. Open `retrain_model.py`
    a. Ensure
       `model = YOLO(r'runs\detect\train_batch0_ball_player\weights\best_batch0_ball_player.pt')` generated after Step 10.c for training batch1 and batch0 combined.
       `model = YOLO(r'runs\detect\train_batch1_ball_player\weights\best_batch1_ball_player.pt')` generated after Step 18 for training batch2, batch1 and batch0 combined
    b. Once finished, Go to `runs/detect/` and rename folder "train" to "train_batch1_ball_player" or "train_batch2_ball_player" and so on
    c. Under this folder, Go to `weights/` and rename the training model file called "best.pt" to "best_batch1_ball_player.pt", "best_batch2_ball_player.pt" and so on.
    
Repeat Steps 11-17.
