import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_functions import available_functions, call_function
from config import MAX_ITERS


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
    
    # Form final output string
    final_response = []
    final_response.append("Final response:")

    # Loop max 20 times 
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_response_text = generate_content(client, messages, verbose)
            if final_response_text:
                final_response.append(final_response_text)
                print("\n".join(final_response))
                break
        except Exception as e:
            print(f"Error generating response: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}\n")

    # Iterate over response.candidates and add each candidate.content to messages list with role "model"
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

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

    if not function_responses:
        raise Exception("No function responses generated, exiting.")
    
    # append function response to messages with role "user"
    messages.append(types.Content(parts=function_responses, role="user"))

if __name__ == "__main__":
    main()
