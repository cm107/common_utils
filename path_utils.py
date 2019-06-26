import os, inspect

def get_script_path() -> str:
    caller_script_path = os.path.abspath((inspect.stack()[1])[1])
    return caller_script_path

def get_script_dir() -> str:
    caller_script_path = os.path.abspath((inspect.stack()[1])[1])
    caller_script_dir = os.path.dirname(caller_script_path)
    return caller_script_dir

def get_filelist(dir_path: str) -> list:
    return os.listdir(dir_path)

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

def rel_to_abs_path(rel_path: str):
    return os.path.abspath(rel_path)