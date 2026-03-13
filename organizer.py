import os
import shutil
from config.file_types import FILE_TYPES, DEFAULT_FOLDER
from database import log_action


def organize_file(file_path, destination_root):

    file_name = os.path.basename(file_path)
    ext = os.path.splitext(file_name)[1].lower()

    target_folder = DEFAULT_FOLDER

    for folder, extensions in FILE_TYPES.items():
        if ext in extensions:
            target_folder = folder
            break

    destination_folder = os.path.join(destination_root, target_folder)

    os.makedirs(destination_folder, exist_ok=True)

    new_path = os.path.join(destination_folder, file_name)

    shutil.move(file_path, new_path)

    log_action(file_name, file_path, new_path, "moved")

    return new_path