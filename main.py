import os 
from dotenv import load_dotenv
from google import genai




def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print("Prompt tokens:", prompt_tokens)
    print("Response tokens:", response_tokens)
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
