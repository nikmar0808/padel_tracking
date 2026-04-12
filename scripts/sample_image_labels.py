import os
import cv2
import random
from config_scripts import TRNG_IMAGES_DIR, TRNG_LABELS_DIR, ANNOT_SAMPLES_DIR

images_dir = TRNG_IMAGES_DIR
labels_dir = TRNG_LABELS_DIR
output_dir = ANNOT_SAMPLES_DIR

os.makedirs(output_dir, exist_ok=True)

images = os.listdir(images_dir)

sample_images = random.sample(images, 20)

for img_name in sample_images:

    img_path = os.path.join(images_dir, img_name)
    label_path = os.path.join(labels_dir, img_name.replace(".PNG", ".txt"))

    image = cv2.imread(img_path)

    height, width, _ = image.shape

    if os.path.exists(label_path):

        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:

            cls, x, y, w, h = map(float, line.split())

            x_center = int(x * width)
            y_center = int(y * height)

            box_width = int(w * width)
            box_height = int(h * height)

            x1 = int(x_center - box_width / 2)
            y1 = int(y_center - box_height / 2)
            x2 = int(x_center + box_width / 2)
            y2 = int(y_center + box_height / 2)

            cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)

    save_path = os.path.join(output_dir, img_name)

    cv2.imwrite(save_path, image)

print("Saved annotated samples to:", output_dir)