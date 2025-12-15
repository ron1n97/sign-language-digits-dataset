import os
from pathlib import Path
import zipfile

# Путь к папке test
TEST_DIR = Path("test")
# Имя выходного zip файла
ZIP_NAME = "test_dataset.zip"

def zip_test_folder(test_dir: Path, zip_name: str):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(test_dir):
            for file in files:
                # игнорируем скрытые файлы и системные файлы
                if file.startswith('.') or file.startswith('._'):
                    continue
                file_path = Path(root) / file
                # сохраняем относительный путь внутри zip
                arcname = file_path.relative_to(test_dir.parent)
                zipf.write(file_path, arcname)
    print(f"[INFO] Папка {test_dir} сжата в {zip_name}")

if __name__ == "__main__":
    if not TEST_DIR.exists():
        print(f"[ERROR] Папка {TEST_DIR} не найдена")
    else:
        zip_test_folder(TEST_DIR, ZIP_NAME)
