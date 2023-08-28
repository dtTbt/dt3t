import os
import platform
import time


def uniform_path_format(path):
    '''
    Input:
        path (str) - A file path.
    Output:
        formatted_path (str) - The file path in linux format.
    '''

    def convert_to_unix_path(windows_path):
        unix_path = windows_path.replace('\\', '/')
        return unix_path

    if '\\' in path:  # Windows format
        return convert_to_unix_path(path)
    else:  # Linux format
        return path


def shutdown_if_linux_not_windows(tim):
    '''
    Input:
        tim - The duration in seconds to sleep before checking the platform.
    Func:
        This function checks the platform and shuts down the system if it is running on Linux and not on Windows.
        It first sleeps for the specified duration, allowing for any pending operations to complete. Then it checks
        the platform using the `platform.system()` function. If the system is identified as Linux and not Windows,
        it executes the shutdown command using `os.system('shutdown -h now')`, which shuts down the system immediately.
    '''
    time.sleep(tim)
    if platform.system() == 'Linux' and platform.system() != 'Windows':
        os.system('shutdown -h now')
