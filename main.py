import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import run_python_file, get_files_info, write_file, get_file_content

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
        types.Content(
            role="user", 
            parts=[
                types.Part(text=user_prompt)
                ]
        ),
    ]

    available_functions = types.Tool(
        function_declarations=[
            get_files_info.schema_get_files_info,
            run_python_file.schema_run_python_file,
            write_file.schema_write_file,
            get_file_content.schema_get_file_content,
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Write or overwrite files
    - Execute Python files with optional arguments

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    def call_function(function_call_part, verbose=False):
        function_name = function_call_part.name
        function_args = function_call_part.args
        working_directory = "./calculator"

        if verbose:
            print(f'Calling function: {function_name}({function_args})')
        else:
            print(f' - Calling function: {function_name}')

        function_mapping = {
            "get_files_info": get_files_info.get_files_info,
            "run_python_file": run_python_file.run_python_file,
            "write_file": write_file.write_file,
            "get_file_content": get_file_content.get_file_content,
        }

        if function_name in function_mapping:
            function_to_call = function_mapping[function_name]
            # add working_directory to function_args
            function_args["working_directory"] = working_directory

            function_result = function_to_call(**function_args)

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

    # --- Output ---

    max_iterations = 20
    count = 0

    while count < max_iterations:
        try:
            if args.verbose:
                print(f"--- Iteration {count + 1} ---")
            
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                    )
            )

            candidates_list = response.candidates

            if response.function_calls:
                # process function calls
                for candidate in candidates_list:
                    # print(f"Candidate content: {candidate.content}")
                    messages.append(candidate.content)

                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose=args.verbose)

                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("Function call failed")

                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

                    messages.append(function_call_result)
            elif response.text  :
                print(f"Final Response: \n{response.text}")
                break  # No more function calls, exit the loop
            else:
                # neither function calls nor final response - something's wrong
                break

            count += 1

        except Exception as e:
            print(f"Error during generation: {str(e)}")
            break
            

    if args.verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()
