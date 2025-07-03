import os
import sys
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Check for prompt argument
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command line argument.")
    sys.exit(1)

# Join all arguments into a single prompt string (to support multi-word prompts)
prompt = " ".join(sys.argv[1:])

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Generate content
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt
)

# Print the response text
print(response.text)

# Print token usage
usage = response.usage_metadata
print(f"\nPrompt tokens: {usage.prompt_token_count}")
print(f"Response tokens: {usage.candidates_token_count}")




#if __name__ == "__main__":
#    main()
