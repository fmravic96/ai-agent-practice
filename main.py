import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


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


response = client.models.generate_content(model=model_name, contents=messages)

if args.verbose:
    if response.usage_metadata is not None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    else:
        print("Token usage information is not available.")
