import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Prepare message for the model
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    # Generate content
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    print(response.text)

    if verbose:
        usage = response.usage_metadata
        print(f"\nUser prompt: {user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")



if __name__ == "__main__":
    main()
