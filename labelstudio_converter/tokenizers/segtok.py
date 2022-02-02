from typing import List

from segtok.segmenter import split_single
from segtok.tokenizer import split_contractions, word_tokenizer

from labelstudio_converter.tokenizers.tokenizer import Token, Tokenizer


# Implementation based on https://github.com/flairNLP/flair/blob/master/flair/tokenization.py
class SegtokTokenizer(Tokenizer):
    """
    Tokenizer using segtok, a third party library dedicated to rules-based Indo-European languages.
    For further details see: https://github.com/fnl/segtok
    """

    def __init__(self):
        super().__init__()

    def tokenize(self, text: str) -> List[Token]:
        return SegtokTokenizer.run_tokenize(text)

    @staticmethod
    def run_tokenize(text: str) -> List[Token]:
        tokens: List[Token] = []
        words: List[str] = []

        sentences = split_single(text)
        for sentence in sentences:
            contractions = split_contractions(word_tokenizer(sentence))
            words.extend(contractions)

        words = list(filter(None, words))

        # determine offsets for whitespace_after field
        index = text.index
        current_offset = 0
        previous_word_offset = -1
        previous_token = None
        for word in words:
            try:
                word_offset = index(word, current_offset)
                start_position = word_offset
            except ValueError:
                word_offset = previous_word_offset + 1
                start_position = current_offset + 1 if current_offset > 0 else current_offset

            if word:
                token = Token(text=word, start_position=start_position, whitespace_after=True)
                tokens.append(token)

            if (previous_token is not None) and word_offset - 1 == previous_word_offset:
                previous_token.whitespace_after = False

            current_offset = word_offset + len(word)
            previous_word_offset = current_offset - 1
            previous_token = token

        return tokens
