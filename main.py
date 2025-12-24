import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from fakes import FakeMetadata, FakeResponse
from log_decorator import logger
from prompts import system_prompt


class ChatbotSettings:
    def __init__(self):
        def parse_inputs():
            parser = argparse.ArgumentParser(description="Chatbot")
            parser.add_argument("user_prompt", type=str, help="User prompt")
            parser.add_argument(
                "--verbose", action="store_true", help="Enable verbose output"
            )
            parser.add_argument(
                "--debug", action="store_true", help="Skip the api call for debugging"
            )
            return parser.parse_args()

        args = parse_inputs()

        self.verbose = args.verbose
        self.debug_mode = args.debug
        self.user_prompt = args.user_prompt

        if self.verbose or self.debug_mode:
            print("\n" + "-" * 50)
            print(f"verbose: {self.verbose}")
            print(f"debug_mode: {self.debug_mode}")
            print(f"user_prompt: {self.user_prompt}")
            print("-" * 50 + "\n")


def gemini_client(debug_mode: bool = False):
    def get_api_key():
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key is None:
            raise RuntimeError("api key not found")
        return api_key

    model = "gemini-2.5-flash-lite"
    key = get_api_key()
    if not debug_mode:
        client = genai.Client(api_key=key)

    def gemini_response(messages: list[types.Content]):
        if not debug_mode:
            # print("Not running in debug mode.")
            # print(system_prompt)
            config=types.GenerateContentConfig(system_instruction=system_prompt)
            # print(f"config.system_instruction: {config.system_instruction}")
            response = client.models.generate_content(
                model=model,
                contents=messages,
                config=config,
            )
            # response = None
        else:
            print("Running in DEBUG mode.")
            response = FakeResponse(
                prompt_token_count=69,
                candidates_token_count=96,
                response_text="I'M JUST A ROBOT",
            )
        return response

    return gemini_response


def main():
    settings = ChatbotSettings()
    messages = [
        types.Content(role="user", parts=[types.Part(text=settings.user_prompt)])
    ]

    # gemini = logger(settings.debug_mode, settings.verbose)(gemini_client)
    # response = gemini(settings.debug_mode)(messages=messages)
    response = gemini_client(settings.debug_mode)(messages)
     
    if response is None or response.usage_metadata is None:
        raise RuntimeError(
            "the response did not contain usage metadata (likely a failed API request)"
        )
        
    else:
        if settings.verbose:
            print(f"User prompt: {settings.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        print(f"RESPONSE: {response.text}")

if __name__ == "__main__":
    main()