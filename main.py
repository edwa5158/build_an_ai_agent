import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from fakes import FakeMetadata, FakeResponse

class ChatbotSettings():
    def __init__(self):
        def parse_inputs():
            parser = argparse.ArgumentParser(description="Chatbot")
            parser.add_argument("user_prompt", type=str, help="User prompt")
            parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
            parser.add_argument("--debug", action="store_true", help="Skip the api call for debugging")
            return parser.parse_args()
        args = parse_inputs()
        
        self.verbose = args.verbose
        self.debug_mode = args.debug
        self.user_prompt = args.user_prompt

        if self.verbose: 
            print("\n" + "-"*50)
            print(f"verbose: {self.verbose}")
            print(f"debug_mode: {self.debug_mode}")
            print(f"user_prompt: {self.user_prompt}")
            print("-"*50 + "\n")

def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api key not found")
    return api_key

def gemini_client(debug_mode: bool = False):
    model = "gemini-2.5-flash"
    key = get_api_key()
    if not debug_mode:
        client = genai.Client(api_key = key)
    
    def gemini_response(messages):
        if not debug_mode:
            response = client.models.generate_content(model = model , contents = messages)
        else:
            response = FakeResponse(prompt_token_count=69, candidates_token_count=96)
        return response
    return gemini_response

def main():
    settings = ChatbotSettings()

    messages = [types.Content(role="user", parts=[types.Part(text=settings.user_prompt)])]
    response = gemini_client(settings.debug_mode)(messages=messages)
    
    if (response.usage_metadata is not None) and settings.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("the response did not contain usage metadata (likely a failed API request)")
    print(response.text)

if __name__ == "__main__":
    main()

