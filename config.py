import argparse
import os

from dotenv import load_dotenv

from log_decorator import logger, set_log_options

MAX_CHARACTERS_TO_READ: int = 10_000
WORKING_DIRECOTRY: str = "./calculator"


@logger()
def get_api_key()->str:
    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api key not found")
    return api_key


class ChatbotSettings:
    def __init__(self):
        def parse_inputs():
            parser = argparse.ArgumentParser(description="Chatbot")
            parser.add_argument("user_prompt", type=str, help="User prompt")
            parser.add_argument(
                "--verbose", action="store_true", help="Enable verbose output"
            )
            return parser.parse_args()

        args = parse_inputs()

        self.verbose = args.verbose
        self.user_prompt = args.user_prompt
        self.model = "gemini-2.5-flash-lite"
        self.api_key: str = get_api_key()
        set_log_options(verbose=self.verbose)
        if self.verbose:
            print("\n" + "-" * 50)
            print(f"verbose: {self.verbose}")
            print(f"user_prompt: {self.user_prompt}")
            print("-" * 50 + "\n")
