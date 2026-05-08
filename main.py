import os
import shutil
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
import argparse
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

SUPPORTED_EXTENSIONS = (".mp3", ".mp4", ".m4a", ".jpg", ".png")


def is_supported_file(file_name):
    return file_name.endswith(SUPPORTED_EXTENSIONS)


def should_copy_file(source_file, target_file):
    return not os.path.exists(target_file)


def prune_target_directory(source, target):
    try:
        source_directories = set()
        source_files = set()

        for root, _, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            source_directories.add(relative_path)

            for file_name in files:
                if is_supported_file(file_name):
                    source_files.add(os.path.join(relative_path, file_name))

        for root, dirs, files in os.walk(target, topdown=False):
            relative_path = os.path.relpath(root, target)

            for file_name in files:
                target_file = os.path.join(root, file_name)
                target_relative_file = os.path.join(relative_path, file_name)

                if not is_supported_file(file_name):
                    continue

                if target_relative_file not in source_files:
                    logging.info(f"Remove `{target_file}`.")
                    os.remove(target_file)

            if relative_path == ".":
                continue

            if relative_path not in source_directories:
                logging.info(f"Remove `{root}`.")
                shutil.rmtree(root)
                continue

            if not os.listdir(root):
                logging.info(f"Remove empty directory `{root}`.")
                os.rmdir(root)
    except Exception as e:
        logging.error(f"Error syncing target directory contents: {e}")
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


def copy_supported_files(source, target):
    logging.info(f"Copy files from `{source}` to `{target}`.")
    for root, _, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        target_path = os.path.join(target, relative_path)

        if not os.path.exists(target_path):
            logging.debug(f"Creating folder {target_path}.")
            os.makedirs(target_path)

        for file in files:
            if is_supported_file(file):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_path, file)

                if file.endswith((".mp3", ".mp4")):
                    remove_isrc_tag(source_file)

                if not should_copy_file(source_file, target_file):
                    logging.debug(f"Skip unchanged file `{target_file}`.")
                    continue

                logging.info(f"Copy `{source_file}` to `{target_file}`.")
                shutil.copy2(source_file, target_file)


def main(source, target):
    prune_target_directory(source, target)
    copy_supported_files(source, target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync music files from source to target directory."
    )

    parser.add_argument(
        "--source", "-Source", dest="source", type=str, required=True, help="Source directory"
    )
    # Make sure to always use single, quotes for the target directory,
    # double quotes may not work for network locations
    parser.add_argument(
        "--target", "-Target", dest="target", type=str, required=True, help="Target directory"
    )
    args = parser.parse_args()

    main(args.source, args.target)
