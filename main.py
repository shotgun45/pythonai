import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

# Define available functions for the model
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Handle command line arguments
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)

    # Detect --verbose flag
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")

    # Join arguments into prompt
    user_prompt = " ".join(sys.argv[1:])

    # Updated system prompt to instruct the LLM on function usage
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Prepare message for the model
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    # Generate content with system instruction and available functions
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    # Check for function calls in the response
    if hasattr(response, "function_calls") and response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            # Check for function_response in the returned Content
            try:
                function_response = function_call_result.parts[0].function_response.response
            except (AttributeError, IndexError):
                raise RuntimeError("Fatal: No function_response in call_function result!")
            if verbose:
                print(f"-> {function_response}")
    else:
        print(response.text)

    if verbose:
        usage = response.usage_metadata
        print(f"\nUser prompt: {user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

def call_function(function_call_part, verbose=False):
    """
    Handles calling a function by name with provided arguments.
    If verbose is True, prints the function name and arguments.
    Otherwise, prints just the function name.
    Actually calls the function and prints the result.
    """
    # Map function names to actual functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    # Prepare arguments
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_call_part.name}({args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Call the function if it exists
    func = function_map.get(function_call_part.name)
    if func:
        result = func(**args)
        print(f"Result: {result}")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
    else:
        print(f"Error: Function '{function_call_part.name}' not found.")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

if __name__ == "__main__":
    main()
