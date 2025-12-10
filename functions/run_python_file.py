import os
import subprocess

def run_python_file(working_directory, file_path, args = []):
    output, safe = safe_to_run(working_directory, file_path)
    if not safe: return output
    cmd = ['python', file_path]
    for a in args: cmd.append(a)
    result = subprocess.run(cmd, capture_output = True)
    stdout = result.stdout
    stderr = result.stderr
    if len(stderr) > 0: return f'Error: executing Python file: {stderr}'
    else: return f'STDOUT: {stdout}'

def safe_to_run(cwd, fp):
    if not str(fp).endswith('.py'):
        return f'Error: "{fp}" is not a python file,', False
    exp_fp = os.path.expanduser(fp)
    cwd = os.path.expanduser(cwd)
    dirs = os.listdir(cwd)
    if os.path.isfile(exp_fp) and not (fp in dirs):
        return 'Error: The python file you want to run, ' \
            f'"{fp}" is outside the permitted working directory,' \
            ' access is denied!', False
    if fp in dirs: return os.path.join(cwd, fp), True
    return 'Error: The file you want to run, ' \
        f'"{fp}" was not found.', False
