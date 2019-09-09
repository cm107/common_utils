import sys
from ..logger.logger_handler import logger
from .adv_file_utils import delete_all_files_in_extension_list

def delete_files_in_dir_prompt(dir_path: str, extension_list: list):
    answer = input("yes/no: ")
    if answer.lower() == "yes":
        delete_all_files_in_extension_list(dir_path=dir_path, extension_list=extension_list)
    elif answer.lower() == "no":
        logger.warning("Terminating program.")
        sys.exit()
    else:
        logger.error(f"Invalid response: {answer}")
        raise Exception