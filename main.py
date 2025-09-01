import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_functions import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [OPTION]')
        print('Example: python main.py "How do I fix a calculator app?"')
        print("Options:")
        print("  --verbose        show prompt metadata")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Returns a list of responses
    response_content = generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    # TODO iterate response.candidates and add each candidate.content to messages list

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}\n")

    if not response.function_calls:
        return response.text

    # Call functions and store them in list of parts function_responses
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        # If results are empty raise exception
        if (
            not function_call_result.parts[0].function_response.response
            or not function_call_result.parts
        ):
            raise Exception ("Error: Function call result empty")
        elif verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    # TODO: convert function_responses list of parts (single message with role = "tool") to message with role = "user"
    # TODO: append this message to messages
    
    if not function_responses:
        raise Exception("No function responses generated, exiting.")
    
    return function_responses

if __name__ == "__main__":
    main()
