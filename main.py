import os
import shutil
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
import argparse
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def clear_target_directory(target):
    try:
        for root, dirs, files in os.walk(target):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
        logging.info(f"Cleared contents of target directory: {target}")
    except Exception as e:
        logging.error(f"Error clearing target directory contents: {e}")
        raise


def remove_isrc_tag(file_path):
    try:
        if file_path.endswith(".mp3"):
            audio = EasyID3(file_path)
            if "isrc" in audio:
                del audio["isrc"]
                audio.save()
                logging.debug(f"Removed isrc tag from {file_path}.")
        elif file_path.endswith(".mp4"):
            video = MP4(file_path)
            if "----:com.apple.iTunes:ISRC" in video:
                del video["----:com.apple.iTunes:ISRC"]
                video.save()
                logging.debug(f"Removed isrc tag from {file_path}.")
    except Exception as e:
        print(f"Error removing ISRC tag from {file_path}: {e}")


def sync_files(source, target):
    logging.info(f"Copy files from `{source}` to `{target}`.")
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        target_path = os.path.join(target, relative_path)

        if not os.path.exists(target_path):
            logging.debug(f"Creating folder {target_path}.")
            os.makedirs(target_path)

        for file in files:
            if file.endswith((".mp3", ".mp4", ".jpg", ".png")):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_path, file)

                if file.endswith((".mp3", ".mp4")):
                    remove_isrc_tag(source_file)

                logging.info(f"Copy `{source_file}` to `{target_file}`.")
                shutil.copy2(source_file, target_file)


def main(source, target):
    clear_target_directory(target)
    sync_files(source, target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync music files from source to target directory."
    )

    parser.add_argument("--source", type=str, required=True, help="Source directory")
    # Make sure to always use single, quotes for the target directory,
    # double quotes may not work for network locations
    parser.add_argument("--target", type=str, required=True, help="Target directory")
    args = parser.parse_args()

    main(args.source, args.target)
