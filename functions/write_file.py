import os

def write_file(working_directory, file_path, content):
    output, safe = safe_to_write(working_directory, file_path)
    if not safe: return output
    with open(output, 'w') as f:
        f.write(content)

def safe_to_write(cwd, fp):
    exp_fp = os.path.expanduser(fp)
    cwd = os.path.expanduser(cwd)
    dirs = os.listdir(cwd)
    if os.path.isfile(exp_fp) and not (fp in dirs):
        return 'Error: The file you want to write to, ' \
            f'"{fp}" is outside the permitted working directory,' \
            ' access is denied!', False

    return os.path.join(cwd, fp), True
