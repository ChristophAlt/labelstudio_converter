from bisect import bisect_left, bisect_right
from typing import Dict, List, Tuple

import conllu

from anno_converter.dataset_writers.dataset_writer import DatasetWriter
from anno_converter.document import BinaryRelation, Document, LabeledSpan
from anno_converter.tokenizers.tokenizer import Tokenizer


def char_to_token_span(start_char: int, end_char: int, token_starts: List[int]) -> Tuple[int, int]:
    new_start = bisect_right(token_starts, start_char) - 1
    new_end = bisect_left(token_starts, end_char)

    return new_start, new_end


class FlairConlluDatasetWriter(DatasetWriter):
    def __init__(
        self, tokenizer: Tokenizer, entity_field: str = "entities", relation_field: str = "relations"
    ) -> None:
        self.tokenizer = tokenizer
        self.entity_field = entity_field
        self.relation_field = relation_field

    def _split_documents_by_paragraph(self, documents: List[Document], delimiter: str = "\n\n") -> List[Document]:
        par_documents: List[Document] = []
        for document in documents:
            text = document.text

            par_start = 0
            for par_idx, par_text in enumerate(text.split(delimiter), start=1):
                par_end = par_start + len(par_text)

                par_document = Document(text=par_text, doc_id=document.id)

                par_document.metadata.update(document.metadata)
                par_document.metadata["paragraph_id"] = str(par_idx)

                id_to_annotation: Dict[str, LabeledSpan] = {}
                for entity in document.annotations(name=self.entity_field):
                    if entity.start < par_start or entity.end > par_end:
                        continue

                    annotation = LabeledSpan(
                        start=entity.start - par_start, end=entity.end - par_start, label=entity.label
                    )
                    annotation.metadata.update(entity.metadata)
                    id_to_annotation[entity.metadata["id"]] = annotation
                    par_document.add_annotation(self.entity_field, annotation)

                for relation in document.annotations(self.relation_field):
                    head_id = relation.head.metadata["id"]
                    tail_id = relation.tail.metadata["id"]
                    if head_id in id_to_annotation and tail_id in id_to_annotation:
                        annotation = BinaryRelation(
                            head=id_to_annotation[head_id], tail=id_to_annotation[tail_id], label=relation.label
                        )
                        par_document.add_annotation(self.relation_field, annotation)

                par_documents.append(par_document)
                par_start = par_end + len(delimiter)

        return par_documents

    def write(self, path: str, documents: List[Document]) -> None:
        with open(path, mode="w", encoding="utf-8") as out_file:
            # write CoNLL-U Plus header
            out_file.write("# global.columns = id form ner\n")

            for document in self._split_documents_by_paragraph(documents):

                tokens = self.tokenizer.tokenize(document.text)

                metadata = {
                    "document_id": document.id,
                    "text": document.text,
                }

                metadata.update(document.metadata)

                entities = list(sorted(document.annotations(name=self.entity_field), key=lambda e: e.start))

                token_starts = list(sorted([token.start_pos for token in tokens]))

                tags = ["O"] * len(tokens)
                for entity in entities:
                    start_idx, end_idx = char_to_token_span(entity.start, entity.end, token_starts)
                    for i in range(start_idx, end_idx):
                        if i == start_idx:
                            tags[i] = "B-" + entity.label
                        else:
                            tags[i] = "I-" + entity.label

                token_dicts = []
                for idx, (token, tag) in enumerate(zip(tokens, tags), start=1):
                    token_dicts.append(
                        {
                            "id": str(idx),
                            "form": token.text,
                            "ner": tag,
                        }
                    )

                relations = []
                for relation in document.annotations(self.relation_field):
                    head = relation.head
                    tail = relation.tail

                    head_start_idx, head_end_idx = char_to_token_span(head.start, head.end, token_starts)
                    tail_start_idx, tail_end_idx = char_to_token_span(tail.start, tail.end, token_starts)

                    relations.append((head_start_idx, head_end_idx, tail_start_idx, tail_end_idx, relation.label))

                metadata["relations"] = "|".join(
                    [
                        ";".join([str(head_start + 1), str(head_end), str(tail_start + 1), str(tail_end), relation])
                        for head_start, head_end, tail_start, tail_end, relation in relations
                    ]
                )

                token_list = conllu.TokenList(tokens=token_dicts, metadata=metadata)

                out_file.write(token_list.serialize())
