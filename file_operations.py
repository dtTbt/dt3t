import shutil
import json
import os
import rarfile

from sundries import *


def move_files_and_delete_subfolders(folder_path):
    '''
    Input:
        folder_path (str) - The path of the folder where files and subfolders need to be processed.
    Output:
        None
    Func:
        Moves files from subfolders to the specified folder while handling naming conflicts, and then deletes empty
        subfolders within the specified folder.
    '''
    folder_path = uniform_path_format(folder_path)
    # Move files to the specified folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            dest_path = os.path.join(folder_path, file)
            if os.path.exists(dest_path):
                # Rename the file to avoid conflicts
                file_name, file_extension = os.path.splitext(file)
                counter = 1
                while os.path.exists(dest_path):
                    new_file_name = f"{file_name}_{counter}{file_extension}"
                    dest_path = os.path.join(folder_path, new_file_name)
                    counter += 1
            shutil.move(file_path, dest_path)
    # Delete empty subfolders
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def get_most_recent_subfolder(folder_path):
    '''
    Input:
        folder_path: A string representing the path of the folder.
    Output:
        most_recent_subfolder: A string representing the name of the most recent subfolder within the given folder.
    Func:
        This function takes a folder path as input and returns the name of the most recent subfolder within that folder.
        It first retrieves all the subfolders within the specified folder path. If no subfolders are found, it returns
        None. Otherwise, it identifies the most recent subfolder by comparing their creation times using the os.path.
        getctime function. Finally, it returns the name of the most recent subfolder.
    '''
    folder_path = uniform_path_format(folder_path)
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    if not subfolders:
        return None
    most_recent_subfolder = max(subfolders, key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
    return most_recent_subfolder


def modify_yolov8_dataset_first_number(folder_path, Al, Bl):
    '''
    for yolov8 format datasets
    ["1", "2"] -> ["3", "4"]
    '''
    folder_path = uniform_path_format(folder_path)
    folder_name = ["train", "test", "valid"]
    for name in folder_name:
        labels_pth = os.path.join(folder_path, name, "labels")
        # Get a list of all files in the folder
        file_list = os.listdir(labels_pth)
        # Iterate over each file
        for file_name in file_list:
            if file_name.endswith('.txt'):
                file_path = os.path.join(labels_pth, file_name)
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                if len(lines) == 0:
                    continue
                # Modify the first number in each line
                modified_lines = []
                for line in lines:
                    numbers = line.strip().split()
                    for A, B in zip(Al, Bl):
                        if numbers[0] == A:
                            numbers[0] = B
                            modified_lines.append(' '.join(numbers) + '\n')
                            break
                # Save the modified lines back to the file
                with open(file_path, 'w') as file:
                    file.writelines(modified_lines)


def modify_autodl_gpu_txt_file(path):
    path = uniform_path_format(path)
    try:
        # Read the contents of the file
        with open(path, 'r') as file:
            lines = file.readlines()
        # Parse the contents and extract the required values
        port = lines[0].split('-p ')[1].split(' ')[0]
        username = lines[0].split('@')[0].split(' ')[-1]
        address = lines[0].split('@')[1].split('\n')[0]
        password = lines[1]
        # Modify the contents
        modified_content = f"Address:\n{address}\n\nPort:\n{port}\n\nUsername:\n{username}\n\nPassword:\n{password}"
        # Write the modified contents back to the file
        with open(path, 'w') as file:
            file.write(modified_content)
        print(f"File '{path}' successfully modified.")
    except FileNotFoundError:
        print(f"File '{path}' not found.")


def remove_empty_lines(file_path):
    """
    Removes empty lines from a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        None
    """
    file_path = uniform_path_format(file_path)
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove empty lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Write the non-empty lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(non_empty_lines)


def save_code_blocks_as_py(ipynb_file_path):
    """
    Saves the contents of all code blocks in an IPython Notebook (.ipynb) file as a .py file.

    Args:
        ipynb_file_path (str): The path to the IPython Notebook file.
    """
    ipynb_file_path = uniform_path_format(ipynb_file_path)
    # Read the contents of the .ipynb file
    with open(ipynb_file_path, 'r') as file:
        notebook = json.load(file)

    # Extract code from code cells
    code_blocks = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            code_blocks.append(''.join(cell['source']))

    # Create a new .py file path
    ipynb_file_name = os.path.basename(ipynb_file_path)
    py_file_name = os.path.splitext(ipynb_file_name)[0] + '_py.py'
    py_file_path = os.path.join(os.path.dirname(ipynb_file_path), py_file_name)
    py_file_path = uniform_path_format(py_file_path)
    # Write code blocks to the .py file
    with open(py_file_path, 'w') as file:
        file.write('\n\n'.join(code_blocks))

    print(f"Code blocks saved to {py_file_path}")


def delete_certain_kind_in_yolov8_dataset(folder_path, kind):
    """
    delete certain kind of images and labels in yolov8 dataset

    Args:
        folder_path (str): The path of the dataset.
        kind (list of str): The kinds of images and labels to be deleted.
            For example, if kind = ["1", "2"], then all images and labels with "1" or "2" as the first character
            in the label file will be deleted.
    """
    folder_name = ["train", "test", "valid"]
    for name in folder_name:
        labels_pth = os.path.join(folder_path, name, "labels")
        images_pth = os.path.join(folder_path, name, "images")
        file_names = os.listdir(labels_pth)
        for file_name in file_names:
            flg = 0
            file_path = os.path.join(labels_pth, file_name)
            with open(file_path, "r") as file:
                lines = file.readlines()
            if len(lines) == 0:
                flg = 1
            for kd in kind:
                for line in lines:
                    if line[0] == kd:
                        flg = 1
                        break
            if flg == 1:
                image_pth = os.path.join(images_pth, file_name[:-4] + ".jpg")
                os.remove(image_pth)
                os.remove(file_path)


def delete_all_files(folder_path):
    """
    Deletes all files within a folder.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        None
    """
    try:
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)
        print(f"All files in '{folder_path}' have been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")

import zipfile

def extract_files(folder_path, password=None):
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        extract_dir_tmp = os.path.join(folder_path, "tmp")
        if not os.path.exists(extract_dir_tmp):
            os.mkdir(extract_dir_tmp)
        if password == None:
            if file_name[-3:] == 'rar':
                with rarfile.RarFile(file_path, 'r') as rar:
                    rar.extractall(extract_dir_tmp)
            elif file_name[-3:] == 'zip':
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir_tmp)
            else:
                print(f'{file_path}不是zip或rar文件')
        else:
            if file_name[-3:] == 'rar':
                with rarfile.RarFile(file_path, 'r', password=password) as rar:
                    rar.extractall(extract_dir_tmp)
            elif file_name[-3:] == 'zip':
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir_tmp, pwd=password.encode('utf-8'))
            else:
                print(f'{file_path}不是zip或rar文件')

        flg = 0
        files_num = len(os.listdir(extract_dir_tmp))
        if files_num == 0:
            shutil.rmtree(extract_dir_tmp)
        while True:
            files_tmp = os.listdir(extract_dir_tmp)
            if len(files_tmp) == 1:
                file_name_tmp = files_tmp[0]
                file_path_tmp = os.path.join(extract_dir_tmp, file_name_tmp)
                if os.path.isdir(file_path_tmp):
                    continue
                    file_path_new = os.path.join(extract_dir_tmp, file_name[:-4])
                    os.rename(file_path_tmp, file_path_new)
                    shutil.move(file_path_new, folder_path)
                    flg = 1
                    break
        if flg == 0:
            folder_path_new = os.path.join(folder_path, file_name[:-4])
            os.rename(extract_dir_tmp, folder_path_new)