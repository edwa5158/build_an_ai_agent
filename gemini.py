from typing import Callable

from google import genai
from google.genai import types

from config import ChatbotSettings
from functions.call_function import available_functions, call_function
from log_decorator import logger
from prompts import system_prompt


# @logger()
def client(settings: ChatbotSettings) -> genai.Client:
    return genai.Client(api_key=settings.api_key)


# @logger()
def generate_content(
    client: genai.Client, settings: ChatbotSettings, messages: list[types.Content]
) -> types.GenerateContentResponse:
    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
    response = client.models.generate_content(
        model=settings.model,
        contents=messages,
        config=config,
    )
    return response


# @logger()
def update_messages(
    response: types.GenerateContentResponse,
    settings: ChatbotSettings,
    messages: list[types.Content],
) -> tuple[bool, list[types.Content]]:

    updated_messages: list[types.Content] = messages.copy()
    if (response is None) or (response.usage_metadata is None):
        raise RuntimeError(
            "the response did not contain usage metadata (likely a failed API request)"
        )
    new_messages: list[types.Content] = []

    # add model messages to the conversation history
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                new_messages.append(candidate.content)

    # add function call results
    function_results = []
    if response.function_calls:
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

            function_results.append(function_call_result)

        updated_messages.extend(function_results)
    return len(updated_messages) > len(messages), updated_messages


# @logger()
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
            result += f"User prompt: {settings.user_prompt}"
            result += (
                "\n" + f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
            )
            result += (
                "\n"
                + f"Response tokens: {response.usage_metadata.candidates_token_count}"
            )

        result += "\n\n" + f"RESPONSE: {response.text}"
        result += "\n\n" + "FUNCTION CALLS: "
        function_results = []
        if not response.function_calls:
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
        return result
