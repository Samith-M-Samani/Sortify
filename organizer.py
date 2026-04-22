import os
import shutil
from config.file_types import FILE_TYPES, DEFAULT_FOLDER
from database import log_action, is_file_reverted


def organize_file(file_path, destination_root):

    file_name = os.path.basename(file_path)

    # If this file was previously reverted, keep it out of normal flow by moving it to "ignored"
    if is_file_reverted(file_name):
        ignored_folder = os.path.join(os.path.dirname(file_path), "ignored")
        os.makedirs(ignored_folder, exist_ok=True)
        new_path = os.path.join(ignored_folder, file_name)
        shutil.move(file_path, new_path)
        log_action(file_name, file_path, new_path, "ignored")
        return new_path

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


def revert_file(current_path, original_path):
    os.makedirs(os.path.dirname(original_path), exist_ok=True)
    shutil.move(current_path, original_path)
    log_action(os.path.basename(current_path), current_path, original_path, "reverted")
    return original_path