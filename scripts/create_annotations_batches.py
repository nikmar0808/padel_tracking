import os
import shutil
from config import SAMPLED_FRAMES_DIR, ANNOT_BATCHES_DIR

source = SAMPLED_FRAMES_DIR
target = ANNOT_BATCHES_DIR

batch_size = 300

os.makedirs(target, exist_ok=True)

files = sorted(os.listdir(source))

for i in range(0, len(files), batch_size):

    batch = files[i:i+batch_size]

    batch_folder = os.path.join(target, f"batch_{i//batch_size}")

    os.makedirs(batch_folder, exist_ok=True)

    for file in batch:
        shutil.copy(
            os.path.join(source, file),
            os.path.join(batch_folder, file)
        )