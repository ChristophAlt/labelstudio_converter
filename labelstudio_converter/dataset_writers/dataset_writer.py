from abc import ABC, abstractmethod
from typing import List

from labelstudio_converter.document import Document


class DatasetWriter(ABC):
    @abstractmethod
    def write(self, path: str, documents: List[Document]) -> None:
        raise NotImplementedError()
