from abc import ABC, abstractmethod
from typing import List

from labelstudio_converter.document import Document


class DatasetReader(ABC):
    @abstractmethod
    def read(self, path: str) -> List[Document]:
        raise NotImplementedError()
