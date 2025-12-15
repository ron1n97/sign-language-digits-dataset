import os
from pathlib import Path
from PIL import Image
import shutil

SRC_ROOT = Path(".")          # где лежат train/valid/test
DST_ROOT = Path("final_dataset")   # куда сохранить объединённый датасет
IMAGE_SIZE = (224, 224)
IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}

DST_ROOT.mkdir(parents=True, exist_ok=True)

def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMG_EXTENSIONS

def process_image(src_path: Path, dst_path: Path):
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(src_path) as img:
            img = img.convert("RGB")
            img = img.resize(IMAGE_SIZE, Image.BILINEAR)
            img.save(dst_path, format="JPEG", quality=95)
    except Exception as e:
        print(f"[ERROR] {src_path}: {e}")

def main():
    for split in ["train", "valid", "test"]:
        split_dir = SRC_ROOT / split
        if not split_dir.exists():
            print(f"[WARN] {split_dir} не существует, пропускаю")
            continue

        for class_dir in split_dir.iterdir():
            if not class_dir.is_dir():
                continue

            class_name = class_dir.name
            dst_class_dir = DST_ROOT / class_name

            for img_path in class_dir.rglob("*"):
                if not is_image(img_path):
                    continue

                # чтобы избежать конфликтов имён файлов
                dst_name = f"{split}_{img_path.name}"
                dst_path = dst_class_dir / dst_name

                process_image(img_path, dst_path)

    print("Готово.")

if __name__ == "__main__":
    main()
