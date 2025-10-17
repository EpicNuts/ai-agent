import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- Get the API Key for use in the Client ---
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    # --- Define the Commandline arguments ---
    parser = argparse.ArgumentParser(description="Generate text using Gemini API")
    parser.add_argument("prompt", nargs="*", help="Input text to generate a response for")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--model", "-m", default="gemini-2.0-flash-001", help="Model to use for generation")

    args = parser.parse_args()

    # --- Access the Arguments ---
    user_prompt = " ".join(args.prompt)
    model_name = args.model

    if not user_prompt:
        print("Please provide input text as command line arguments.")
        sys.exit(1)

    if args.verbose:
        print(f"Using model: {model_name}")
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
    )

    # --- Output ---
    print(response.text)

    if args.verbose:    
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}' )
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}' )

if __name__ == "__main__":
    main()
