import os, sys
from shutil import rmtree, copyfile

def dir_exists(url: str):
    return os.path.isdir(url)

def file_exists(url: str):
    return os.path.isfile(url)

def delete_file(url: str):
    os.unlink(url)

def delete_dir(dir_path: str):
    rmtree(dir_path)

def make_dir(dir_path: str):
    os.mkdir(dir_path)

def delete_all_files_in_dir(dir_path: str):
    print('Are you sure that you want to delete of of the files in {}?'.format(dir_path))
    consent = input('yes/no: ')
    if consent != 'yes':
        print('Program terminated')
        sys.exit()
    names = os.listdir(dir_path)
    for name in names:
        path = os.path.join(dir_path, name)
        if file_exists(path):
            delete_file(path)
        else:
            delete_dir(path)
        print('Deleted {}'.format(path.split('/')[-1]))

def init_dir(dir_path: str):
    dir_name = dir_path.split('/')[-1]
    if not dir_exists(dir_path):
        make_dir(dir_path)
        print("Created directory {}".format(dir_name))
    else:
        delete_all_files_in_dir(dir_path)
        print("All files have been deleted from directory {}".format(dir_name))
    print('Directory {} has been initialized'.format(dir_name))

def copy_file(src_path: str, dest_path: str):
    copyfile(src_path, dest_path)
    src_preview = '/'.join(src_path.split('/')[-3:])
    dest_preview = '/'.join(dest_path.split('/')[-3:])
    print('Copied {} to {}'.format(src_preview, dest_preview))
