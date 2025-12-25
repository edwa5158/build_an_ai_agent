import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from fakes import FakeResponse
from log_decorator import logger, set_log_options
from prompts import system_prompt
from functions.available_functions import available_functions


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

        set_log_options(debug_mode=self.debug_mode, verbose=self.verbose)
        if self.verbose or self.debug_mode:
            print("\n" + "-" * 50)
            print(f"verbose: {self.verbose}")
            print(f"debug_mode: {self.debug_mode}")
            print(f"user_prompt: {self.user_prompt}")
            print("-" * 50 + "\n")


@logger()
def gemini_client(debug_mode: bool = False):
    def get_api_key():
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key is None:
            raise RuntimeError("api key not found")
        return api_key

    key = get_api_key()
    if not debug_mode:
        client = genai.Client(api_key=key)

    @logger()
    def gemini_response(prompt: str, model: str):
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)])
        ]
        config = types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
        if not debug_mode:
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
    model = "gemini-2.5-flash-lite"
    responder = gemini_client(settings.debug_mode)
    result: str = "\n\n"
    response = responder(settings.user_prompt, model)

    if (response is None) or (response.usage_metadata is None):
        raise RuntimeError(
            "the response did not contain usage metadata (likely a failed API request)"
        )

    else:
        if settings.verbose:
            print(f"User prompt: {settings.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        result += f"RESPONSE: {response.text}"
        result += "\n\nFUNCTION CALLS: "
        if response.function_calls:
            for function_call in response.function_calls:
                result += f"\n\t{function_call.name}({function_call.args})"

        print(result)

if __name__ == "__main__":
    main()