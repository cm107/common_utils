import os, sys, subprocess
from shutil import rmtree, copyfile
from distutils.dir_util import copy_tree

def dir_exists(url: str):
    return os.path.isdir(url)

def file_exists(url: str):
    return os.path.isfile(url)

def link_exists(url: str):
    return os.path.islink(url)

def delete_file(url: str):
    os.unlink(url)

def delete_existing_file(url: str):
    if file_exists(url):
        delete_file(url)
    else:
        raise Exception(f"Error: Failed to delete {url}. File doesn't exist.")

def delete_file_if_exists(url: str):
    if file_exists(url):
        delete_file(url)

def delete_dir(dir_path: str):
    rmtree(dir_path)

def delete_existing_dir(url: str):
    if dir_exists(url):
        delete_dir(url)
    else:
        raise Exception(f"Error: Failed to delete {url}. Directory doesn't exist.")

def delete_dir_if_exists(url: str):
    if dir_exists(url):
        delete_dir(url)

def make_dir(dir_path: str):
    os.mkdir(dir_path)

def make_dir_if_not_exists(dir_path: str):
    if not dir_exists(dir_path):
        make_dir(dir_path)

def delete_all_files_in_dir(dir_path: str, ask_permission: bool=True):
    if ask_permission:
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

def init_dir(dir_path: str, ask_permission: bool=True):
    dir_name = dir_path.split('/')[-1]
    if not dir_exists(dir_path):
        make_dir(dir_path)
        print("Created directory {}".format(dir_name))
    else:
        delete_all_files_in_dir(dir_path, ask_permission)
        print("All files have been deleted from directory {}".format(dir_name))
    print('Directory {} has been initialized'.format(dir_name))

def copy_file(src_path: str, dest_path: str, silent: bool=False):
    copyfile(src_path, dest_path)
    if not silent:
        src_preview = '/'.join(src_path.split('/')[-3:])
        dest_preview = '/'.join(dest_path.split('/')[-3:])
        print('Copied {} to {}'.format(src_preview, dest_preview))

def copy_dir(src_path: str, dest_path: str, silent: bool=False):
    copy_tree(src_path, dest_path)
    if not silent:
        src_preview = '/'.join(src_path.split('/')[-3:])
        dest_preview = '/'.join(dest_path.split('/')[-3:])
        print('Copied {} to {}'.format(src_preview, dest_preview))

def move_file(src_path: str, dest_path: str, silent: bool=False):
    copy_file(src_path, dest_path, silent=True)
    delete_file(src_path)
    if not silent:
        src_preview = '/'.join(src_path.split('/')[-3:])
        dest_preview = '/'.join(dest_path.split('/')[-3:])
        print('Moved {} to {}'.format(src_preview, dest_preview))

def move_dir(src_path: str, dest_path: str, silent: bool=False):
    copy_dir(src_path, dest_path, silent=True)
    delete_dir(src_path)
    if not silent:
        src_preview = '/'.join(src_path.split('/')[-3:])
        dest_preview = '/'.join(dest_path.split('/')[-3:])
        print('Moved {} to {}'.format(src_preview, dest_preview))

def create_softlink(src_path: str, dst_path: str):
    print(f'dst_path={dst_path}')
    if link_exists(dst_path):
        print('Flag')
        delete_file(dst_path)
    subprocess.run(f"ln -s {src_path} {dst_path}", shell=True)
