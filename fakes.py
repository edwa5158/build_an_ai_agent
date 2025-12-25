class FakeMetadata:
    def __init__(self):
        self.prompt_token_count: int = 0
        self.candidates_token_count: int = 0

class FakeFunctionCall:
    def __init__(self, name: str = "test", args: tuple | None= (1, "2", "three")):
        self.name = name
        self.args = args

class FakeResponse:
    def __init__(
        self,
        prompt_token_count: int = 0,
        candidates_token_count: int = 0,
        response_text: str = "fake response",
        function_calls: list[FakeFunctionCall] | None = None,
    ):
        self.usage_metadata = FakeMetadata()
        self.usage_metadata.prompt_token_count = prompt_token_count
        self.usage_metadata.candidates_token_count = candidates_token_count
        self.function_calls = function_calls
        self.text = response_text
