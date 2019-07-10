from .file_utils import move_file, delete_existing_file
from .path_utils import get_next_dump_path, get_extension_from_path, \
    get_pathlist, get_all_files_of_extension

def move_to_dump_dir(
    src_path: str, dump_dir: str, label_length: int=6,
    silent: bool=False
    ):
    file_extension = get_extension_from_path(src_path)
    dump_path = get_next_dump_path(
        dump_dir=dump_dir,
        file_extension=file_extension,
        label_length=label_length,
        starting_number=0,
        increment=1
    )
    move_file(src_path=src_path, dest_path=dump_path, silent=silent)

def move_all_to_dump_dir(
    src_dir: str, dump_dir: str, label_length: int=6,
    silent: bool=False
    ):
    src_pathlist = get_pathlist(src_dir)
    for src_path in src_pathlist:
        move_to_dump_dir(
            src_path=src_path,
            dump_dir=dump_dir,
            label_length=label_length,
            silent=silent
        )

def delete_all_files_of_extension(dir_path: str, extension: str):
    filepaths = get_all_files_of_extension(dir_path, extension)
    if len(filepaths) > 0:
        for filepath in filepaths:
            delete_existing_file(filepath)
            print(f'Deleted {filepath}')
