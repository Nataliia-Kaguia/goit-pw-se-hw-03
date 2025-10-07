import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# --- Функція для копіювання одного файлу ---
def copy_file(file_path: Path, target_root: Path):
    if file_path.is_file():
        ext = file_path.suffix.lower().lstrip('.')  # наприклад "jpg", "png"
        if not ext:
            ext = "no_extension"  # якщо файл без розширення

        target_dir = target_root / ext
        target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / file_path.name
        shutil.copy2(file_path, target_file)
        print(f"✅ Скопійовано: {file_path} → {target_file}")

# --- Рекурсивний обхід папок ---
def process_directory(source_dir: Path, target_root: Path, executor: ThreadPoolExecutor):
    for item in source_dir.iterdir():
        if item.is_dir():
            # кожну папку обробляємо в окремому потоці
            executor.submit(process_directory, item, target_root, executor)
        elif item.is_file():
            executor.submit(copy_file, item, target_root)

# --- Основна функція ---
def main():
    if len(sys.argv) < 2:
        print("❌ Використання: python sorter.py <source_dir> [target_dir]")
        sys.exit(1)

    source_dir = Path(sys.argv[1])
    target_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"❌ Директорія {source_dir} не існує або не є директорією")
        sys.exit(1)

    target_root.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Починаємо сортування файлів із: {source_dir}")
    print(f"📁 Результат буде у: {target_root}")

    with ThreadPoolExecutor() as executor:
        process_directory(source_dir, target_root, executor)

    print("✅ Сортування завершено!")

if __name__ == "__main__":
    main()
