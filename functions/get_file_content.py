import os
from config import Config

def get_file_content(working_directory, file_path):
    cfg = Config()
    content, safe = file_is_safe(working_directory, file_path)
    if not safe: return content
    with open(content, 'r') as f:
        file_content_string = f.read(cfg.MAX_CHARS)
        return file_content_string

def file_is_safe(cwd, fp):
    exp_fp = os.path.expanduser(fp)
    cwd = os.path.expanduser(cwd)
    dirs = os.listdir(cwd)
    if os.path.isfile(exp_fp) and not (fp in dirs):
        return 'Error: The file you want to read, ' \
            f'"{fp}" is outside the permitted working directory,' \
            ' access is denied!', False

    if fp in dirs: return os.path.join(cwd, fp), True
    return 'Error: The file you want to access, ' \
        f'"{fp}" was not found or is not a regular file.', False

