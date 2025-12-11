from google.genai import types,

schema_get_files_info = types.FunctionDeclaration(
    name = 'get_files_info',
    description = 'Lists files in the specified directory along ith their sizes, constrained to the working directory.',
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            'directory': types.Schema(
                type = types.Type.STRING,
                description = 'The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.'
            )
        }
    )
)

schema_get_file_content = types.FunctionDeclaration(
    name = 'get_file_content',
    description = 'Gets the contents of a specific file in the wokring directory, function is constrained to the working directory.',
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            'file_path': types.Schema(
                type = types.Type.STRING,
                description = 'The path to the file selected by user. If not provided, list files using get_files_info and try to guess.'
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name = 'run_python_file',
    description = 'Executes and runs a specific file in the working directory, with or without extra arguments. This function is constrained to the working directory.',
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            'file_path': types.Schema(
                type = types.Type.STRING,
                description = 'The path to the file selected by user to be executed. If not provided, do nothing.'
            ),
            'args': types.Schema(
                type = types.Type.LIST,
                description = 'Arguements that need to be passed to program for execution. If not provided, execute without it.'
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name = 'write_file',
    description = 'Writes given generated content to a specific file in the working directory, if the file doenst exist it will create it. function is constrained to the working directory.',
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            'file_path': types.Schema(
                type = types.Type.STRING,
                description = 'The path to the file you want to write. If get_files_info, shows the file doesnt exist it would be created.'
            ),
            'content': types.Schema(
                type = types.Type.LIST,
                description = 'Generated content to be written on to the specified file by user or agent.'
            )
        }
    )
)
