import os
import cv2
from config import TRNG_IMAGES_DIR, TRNG_LABELS_DIR, VAL_IMAGES_DIR, VAL_LABELS_DIR

image_dirs = [
    TRNG_IMAGES_DIR,
    VAL_IMAGES_DIR
]

label_dirs = [
    TRNG_LABELS_DIR,
    VAL_LABELS_DIR
]

errors = 0
total_images = 0
total_labels = 0


def check_label_file(label_path, img_width, img_height):

    global errors
    global total_labels

    with open(label_path, "r") as f:
        lines = f.readlines()

    if len(lines) == 0:
        print(f"⚠️ WARNING: empty label file -> {label_path}")

    for line in lines:

        total_labels += 1

        parts = line.strip().split()

        if len(parts) != 5:
            print(f"❌ ERROR: invalid label format -> {label_path}")
            errors += 1
            continue

        cls, x, y, w, h = map(float, parts)

        if cls != 0:
            print(f"⚠️ WARNING: unexpected class id in {label_path}")

        if not (0 <= x <= 1 and 0 <= y <= 1):
            print(f"❌ ERROR: center outside image -> {label_path}")
            errors += 1

        if not (0 < w <= 1 and 0 < h <= 1):
            print(f"❌ ERROR: invalid box size -> {label_path}")
            errors += 1


for image_dir, label_dir in zip(image_dirs, label_dirs):

    print(f"\nChecking folder: {image_dir}")

    for img_name in os.listdir(image_dir):

        if not img_name.endswith((".PNG", ".jpg", ".jpeg")):
            continue

        total_images += 1

        img_path = os.path.join(image_dir, img_name)

        label_name = os.path.splitext(img_name)[0] + ".txt"
        label_path = os.path.join(label_dir, label_name)

        image = cv2.imread(img_path)

        if image is None:
            print(f"❌ ERROR: cannot read image -> {img_path}")
            errors += 1
            continue

        h, w = image.shape[:2]

        if not os.path.exists(label_path):
            print(f"⚠️ WARNING: missing label -> {label_name}")
            continue

        check_label_file(label_path, w, h)


print("\n-----------------------------------")
print(f"✅ Total images checked: {total_images}")
print(f"✅ Total labels checked: {total_labels}")
print(f"✅ Total errors: {errors}")
print("-----------------------------------")

if errors == 0:
    print("✅ DATASET CHECK PASSED")
else:
    print("❌ DATASET HAS ERRORS - FIX BEFORE TRAINING")