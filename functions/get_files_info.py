import os

def dir_is_safe(cwd, dir):
    exp_dir = os.path.expanduser(dir)
    cwd = os.path.expanduser(cwd)
    dirs = os.listdir(cwd)
    if dir == '.': return cwd, True
    if os.path.isdir(exp_dir) and not (dir in dirs):
        return 'Error: The directory you want to access, ' \
            f'"{dir}" is outside the permitted working directory,' \
            ' access is denied!', False

    if dir in dirs: return os.path.join(cwd, dir), True
    return 'Error: The directory you want to access, ' \
        f'"{dir}" does not exist!', False

def get_file_details(cwd):
    cwd = os.path.expanduser(cwd)
    dirs = os.listdir(cwd)
    strs = []
    for d in dirs:
        p = os.path.join(cwd, d)
        strs.append(
            f'- {d}: {os.path.getsize(p)} bytes, is_dir={os.path.isdir(p)}\n')
    return ''.join(strs)

def get_files_info(working_directory, directory = '.'):
    content, safe = dir_is_safe(working_directory, directory)
    if not safe: return content
    details = get_file_details(content)
    return details
