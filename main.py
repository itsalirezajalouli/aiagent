import argparse
import os
import textwrap
from dotenv import load_dotenv
from functions.get_file_content import get_file_content
from prompts import system_prompt
from google.genai import types, Client
from functions.get_files_info import get_files_info


class Colors:
    green = '\033[92m'
    red = '\033[91m'
    cyan = '\033[96m'
    reset = '\033[0m'
    bold = '\033[1m'

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')

client = Client(api_key = api_key)
MODEL_NAME = 'gemini-2.5-flash'

def main():
    colors = Colors()
    parser = setup_parser()
    args = parser.parse_args()

    messages = [types.Content(role = 'user',
                              parts = [types.Part(text = args.user_prompt)])]

    schema_get_files_info = types.FunctionDeclaration(
        name = 'get_files_info',
        description = 'Lists files in the specified directory along with their sizes, constrained to the working directory.',
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
        description = 'Gets the contents of a specific file in the specified directory, constrained to the working directory.',
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

    available_funcs = types.Tool(
        function_declarations = [schema_get_files_info,
                                 schema_get_file_content],
    )
    config = types.GenerateContentConfig(tools = [available_funcs],
                                         system_instruction = system_prompt)

    response = client.models.generate_content(
        model = MODEL_NAME,
        contents = messages,
        config = config,
    )

    get_response(config, response)


    # TUI display
    display_input(args, colors)

    display_response(response, colors)

    if args.verbose: monitor_usage(response, colors)

def setup_parser():
    parser = argparse.ArgumentParser(description = 'Chatbot')
    parser.add_argument('user_prompt', type = str, help = 'User prompt')
    parser.add_argument('--verbose', action = 'store_true',
                        help = 'Enable verbose output')
    return parser

def display_input(args, colors):
    print()
    wraped_prompt = textwrap.wrap(args.user_prompt.capitalize(), width = 69)
    print(f'{colors.bold}{colors.green}-> Prompt:{colors.reset} ', end = '')
    for line in wraped_prompt: print(line)
    print()
    print(colors.red, 80 * '-', '\n')

def display_response(response, colors):
    if response.text is not None:
        print(f'{colors.bold}{colors.cyan}-> Response:{colors.reset} ', end = '')
        wraped_response = textwrap.wrap(response.text, width = 67)
        for line in wraped_response: print(line)
        print()

def monitor_usage(response, colors):
    if response.usage_metadata is not None:
        print(colors.red, 80 * '-', '\n')
        print(f'{colors.bold}{colors.red}-> Prompt tokens:{colors.reset}',
                response.usage_metadata.prompt_token_count)
        print(f'{colors.bold}{colors.red}-> Response tokens:{colors.reset}',
                response.usage_metadata.candidates_token_count)
        print()

def get_response(config, response, extra = ''):
    if response.function_calls is not None:
        for fc in response.function_calls: 
            print(f'Calling function: {fc.name}({fc.args})')
            if fc.name == 'get_files_info': 
                if fc.args is not None:
                    result = get_files_info(os.getcwd(), fc.args.get('directory', '.'))
                    messages = [types.Content(role = 'user',
                                            parts = [types.Part(
                                            text = f'result of calling get_files_info was: {result}')])]
                    response = client.models.generate_content(
                        model = MODEL_NAME, contents = messages, config = config,
                    )
            if fc.name == 'get_file_content': 
                print(response.text)
                if fc.args is not None:
                    result = get_file_content(
                        os.getcwd(),
                        fc.args['file_path'])
                    messages = [types.Content(
                        role = 'user', parts = [types.Part(
                        text = f'result of get_file_content was: {result}')])]
                    response = client.models.generate_content(
                        model = MODEL_NAME, contents = messages, config = config,
                    )


if __name__ == "__main__":
    main()
