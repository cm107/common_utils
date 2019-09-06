import os, inspect, glob
from .file_utils import dir_exists

def get_script_path() -> str:
    caller_script_path = os.path.abspath((inspect.stack()[1])[1])
    return caller_script_path

def get_script_dir() -> str:
    caller_script_path = os.path.abspath((inspect.stack()[1])[1])
    caller_script_dir = os.path.dirname(caller_script_path)
    return caller_script_dir

def get_filelist(dir_path: str) -> list:
    if not dir_exists:
        raise Exception(f"Directory not found: {dir_path}")
    return os.listdir(dir_path)

def find_path_matching_pattern(filepath_pattern: str) -> list:
    return glob.glob(filepath_pattern)

def get_pathlist(dir_path: str) -> list:
    filename_list = get_filelist(dir_path)
    return construct_pathlist(dir_path, filename_list)

def get_filename(path: str) -> str:
    return path.split('/')[-1]

def get_parent_dir(path: str) -> str:
    return path.split('/')[-2]

def get_rootname_from_filename(filename: str) -> str:
    return filename.split('.')[0]

def get_rootname_from_path(path: str) -> str:
    filename = get_filename(path)
    return get_rootname_from_filename(filename)

def get_extension_from_filename(filename: str) -> str:
    return filename.split('.')[1]

def get_extension_from_path(path: str) -> str:
    filename = get_filename(path)
    return get_extension_from_filename(filename)

def get_dirpath_from_filepath(filepath: str) -> str:
    return '/'.join(filepath.split('/')[:-1])

def construct_pathlist(dir_path: str, filename_list: list):
    return ['{}/{}'.format(dir_path, filename) for filename in filename_list]

def truncate_path(path: str, degree: int) -> str:
    """
    degree  |   result
    ==================
    0       |   full path
    1       |   parent directory
    2       |   parent's parent directory
    ...
    """
    if degree < 0:
        raise IndexError('degree cannot be a negative integer')
    if degree == 0:
        return path
    return '/'.join(path.split('/')[0:-degree])

def rel_to_abs_path(rel_path: str) -> str:
    return os.path.abspath(rel_path)

def get_all_files_of_extension(dir_path: str, extension: str=None) -> list:
    filepaths = get_pathlist(dir_path)
    if extension is not None:
        filepaths_of_extension = []
        for filepath in filepaths:
            ext = get_extension_from_path(filepath)
            if ext == extension:
                filepaths_of_extension.append(filepath)
        filepaths = filepaths_of_extension
    return filepaths

def get_all_files_in_extension_list(dir_path: str, extension_list: list=None) -> list:
    filepaths = get_pathlist(dir_path)
    if extension_list is not None:
        filepaths_of_extension = []
        for filepath in filepaths:
            ext = get_extension_from_path(filepath)
            if ext in extension_list:
                filepaths_of_extension.append(filepath)
        filepaths = filepaths_of_extension
    return filepaths

def file_extension_exists_in_dir(dir_path: str, extension: str) -> bool:
    ext_filepaths = get_all_files_of_extension(dir_path, extension)
    if len(ext_filepaths) > 0:
        return True
    else:
        return False

def get_newest_filepath(dir_path: str, extension: str=None) -> str:
    filepaths = get_all_files_of_extension(dir_path, extension)
    if len(filepaths) > 0:
        return max(filepaths, key=os.path.getctime)
    else:
        return None

def get_next_dump_path(
    dump_dir: str, file_extension: str, label_length: int=6,
    starting_number: int=0, increment: int=1
    ):
    newest_filepath = get_newest_filepath(dump_dir, extension=file_extension)
    next_label_number = \
        int(get_rootname_from_path(newest_filepath)) + increment \
            if newest_filepath is not None else starting_number
    next_label_str = str(next_label_number)
    while len(next_label_str) < label_length:
        next_label_str = '0' + next_label_str
    dump_filename = f'{next_label_str}.{file_extension}'
    dump_path = f'{dump_dir}/{dump_filename}'
    return dump_path
