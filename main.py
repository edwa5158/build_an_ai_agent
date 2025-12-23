import os
from dotenv import load_dotenv
from google import genai
import argparse

def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api key not found")
    return api_key

def parse_inputs():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    return parser.parse_args()

def main():
    args = parse_inputs()
    client = genai.Client(api_key = get_api_key())
    model = "gemini-2.5-flash"
    contents = args.user_prompt
    
    response = client.models.generate_content(model = model , contents = contents)
    if response.usage_metadata is not None:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("the response did not contain usage metadata (likely a failed API request)")
    print(response.text)

if __name__ == "__main__":
    main()

