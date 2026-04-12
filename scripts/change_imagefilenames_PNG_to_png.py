from pathlib import Path

root = Path("data/interim/annotation_batches")

for img in root.rglob("*.PNG"):
    new_name = img.with_suffix(".png")
    img.rename(new_name)
    print(f"{img.name} -> {new_name.name}")