from abc import ABC, abstractmethod
from typing import List


class Token:
    def __init__(
        self,
        text: str,
        idx: int = None,
        whitespace_after: bool = True,
        start_position: int = None,
    ) -> None:
        self.text = text
        self.idx = idx
        self.whitespace_after = whitespace_after

        self.start_pos = start_position
        self.end_pos = start_position + len(text) if start_position is not None else None


class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> List[Token]:
        raise NotImplementedError()
