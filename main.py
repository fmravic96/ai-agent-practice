import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    available_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    working_directory = "calculator"
    function_args = {
        "working_directory": working_directory,
        **function_args
    }


    if function_name in available_functions:
        function = available_functions[function_name]

        function_result = function(**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.0-flash-001")


parser = argparse.ArgumentParser(description="Run Gemini model with a prompt.")
parser.add_argument("prompt", type=str, help="Prompt to send to the model.")
parser.add_argument(
    "--verbose", action="store_true", help="Print token usage information."
)
args = parser.parse_args()

client = genai.Client(api_key=api_key)
prompt = args.prompt


if not prompt:
    print("No prompt provided.")
    exit(1)


messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# call generate content 20 times max
for i in range(20):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
        )

        if response.candidates:
            messages += [candidate.content for candidate in response.candidates if candidate.content]

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_response = call_function(function_call_part, verbose=args.verbose)
                if function_response.parts[0].function_response.response:
                    messages.append(types.Content(role="user", parts=function_response.parts))
                    if args.verbose:
                        print(f"-> {function_response.parts[0].function_response.response}")
                else:
                    raise ValueError("Function response is missing.")
                
        if response.text and not response.function_calls:
            print(f"Final response: \n{response.text}")
            break

    except Exception as e:
        print(f"Error occurred: {e}")

if args.verbose:
    if response.usage_metadata is not None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    else:
        print("Token usage information is not available.")
