"""Tool declarations exposed to the LLM runtime.

This module defines `available_functions`, which is a `google.genai.types.Tool`
containing the function declarations the model is allowed to call.
"""

from google.genai import types
from functions.schemas import schema_get_files_info

available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)

