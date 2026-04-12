import shutil
import zipfile
from pathlib import Path

from config_training import ANNOT_BATCHES_DIR, AUTO_ANNOT_DIR


ANNOT_BATCHES_DIR = Path(ANNOT_BATCHES_DIR)
AUTO_ANNOT_DIR = Path(AUTO_ANNOT_DIR)

CLASS_NAMES = ["ball","player"]

TEMP_DIR = Path("temp_cvat_dataset")


def reset_temp():
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)

    TEMP_DIR.mkdir()


def create_metadata():

    # obj.names
    with open(TEMP_DIR / "obj.names", "w") as f:
        for name in CLASS_NAMES:
            f.write(name + "\n")

    # obj.data
    with open(TEMP_DIR / "obj.data", "w") as f:
        f.write(f"classes = {len(CLASS_NAMES)}\n")
        f.write("names = obj.names\n")
        f.write("train = train.txt\n")


def copy_labels_and_create_train(batch_dir):

    train_dir = TEMP_DIR / "obj_train_data"
    train_dir.mkdir()

    train_list = []

    images = list(batch_dir.glob("*.png"))

    label_batch_dir = AUTO_ANNOT_DIR / batch_dir.name

    copied = 0
    missing = 0

    for img in images:

        label_path = label_batch_dir / f"{img.stem}.txt"

        if label_path.exists():

            dest = train_dir / label_path.name
            shutil.copy(label_path, dest)

            train_list.append(f"obj_train_data/{label_path.name}")

            copied += 1

        else:
            missing += 1

    print(f"Images: {len(images)}")
    print(f"Labels copied: {copied}")
    print(f"Labels missing: {missing}")

    # create train.txt
    with open(TEMP_DIR / "train.txt", "w") as f:
        for line in train_list:
            f.write(line + "\n")


def create_zip(batch_dir):

    zip_path = batch_dir / f"{batch_dir.name}_cvat_import.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:

        for file in TEMP_DIR.rglob("*"):
            z.write(file, file.relative_to(TEMP_DIR))

    print(f"Created ZIP: {zip_path}")


def process_batch(batch_dir):

    print("\n---------------------------")
    print(f"Processing {batch_dir.name}")

    reset_temp()

    create_metadata()

    copy_labels_and_create_train(batch_dir)

    create_zip(batch_dir)


def main():

    batches = sorted([d for d in ANNOT_BATCHES_DIR.iterdir() if d.is_dir()])

    print(f"Found {len(batches)} batches")

    for batch in batches:

        if batch.name == "batch_0":
            print("Skipping batch_0 (manual) for now...")
            continue

        process_batch(batch)

    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)

    print("\nAll batches completed.")


if __name__ == "__main__":
    main()