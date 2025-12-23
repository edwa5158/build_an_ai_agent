
class FakeMetadata():
    prompt_token_count: int = 0
    candidates_token_count: int = 0

class FakeResponse():
    def __init__(self, prompt_token_count: int = 0, candidates_token_count: int = 0, response_text: str = "fake response"):
        self.usage_metadata = FakeMetadata()
        self.usage_metadata.prompt_token_count = prompt_token_count
        self.usage_metadata.candidates_token_count = candidates_token_count
        self.text = response_text

