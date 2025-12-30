import warnings

warnings.filterwarnings("ignore", message=r".*non-text parts.*")

from google import genai
from google.genai import types

import gemini
from config import MAX_ITERATIONS, ChatbotSettings


def main() -> str:
    settings = ChatbotSettings()
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=settings.user_prompt)])
    ]
    client: genai.Client = gemini.client(settings)
    has_new_messages = True
    iteration: int = 1
    has_text: bool = False
    result: str = ""
    while has_new_messages and not has_text and iteration < MAX_ITERATIONS:

        response: types.GenerateContentResponse = gemini.generate_content(
            client, settings, messages
        )

        has_text = response.text is not None
        has_new_messages, messages = gemini.update_messages(
            response, settings, messages
        )

        print(f"iteration: {iteration}")
        print(f"response.text: {response.text}")
        print(f"function_calls: {response.function_calls}")
        print(f"has_new_messages: {has_new_messages}")
        iteration += 1

    print(f"loop eneded on iteration: {iteration - 1}")
    result += gemini.handle_response(response, settings)
    print(result)
    return result


if __name__ == "__main__":
    main()
