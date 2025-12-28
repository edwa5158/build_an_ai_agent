from google import genai
from google.genai import types

from config import ChatbotSettings
from gemini import gemini_client, gemini_response, handle_response


def main() -> str:
    settings = ChatbotSettings()

    client: genai.Client = gemini_client(settings)
    response: types.GenerateContentResponse = gemini_response(client, settings)
    result: str = handle_response(response, settings)

    return result


if __name__ == "__main__":
    main()
