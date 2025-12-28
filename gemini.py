from typing import Callable

from google import genai
from google.genai import types

from config import ChatbotSettings
from functions.call_function import available_functions, call_function
from log_decorator import logger
from prompts import system_prompt


@logger()
def gemini_client(settings: ChatbotSettings) -> genai.Client:
    return genai.Client(api_key=settings.api_key)


@logger()
def gemini_response(
    client: genai.Client, settings: ChatbotSettings
) -> types.GenerateContentResponse:
    messages = [
        types.Content(role="user", parts=[types.Part(text=settings.user_prompt)])
    ]
    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
    response = client.models.generate_content(
        model=settings.model,
        contents=messages,
        config=config,
    )
    return response


@logger()
def handle_response(
    response: types.GenerateContentResponse, settings: ChatbotSettings
) -> str:
    result: str = "\n\n"

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
        function_results = []
        if not response.function_calls:
            print(result)
            return result

        for function_call in response.function_calls:
            function_call_result: types.Content = call_function(
                function_call, settings.verbose
            )
            parts = function_call_result.parts
            if not parts:
                raise Exception(
                    f"Function call missing expected result parts for: {function_call.name}({function_call.args})"
                )
            function_response = (
                parts[0].function_response.response
                if parts[0].function_response
                else None
            )
            if not function_response:
                raise Exception(
                    f"Function call `{function_call.name}({function_call.args})` has no response."
                )

            function_results.append(parts[0])
            if settings.verbose:
                result += f"\n\t{function_response}"

        print(result)
        return result
