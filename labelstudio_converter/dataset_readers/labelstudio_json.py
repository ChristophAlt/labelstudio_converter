import json
from typing import Dict, List, Optional

from labelstudio_converter.dataset_readers.dataset_reader import DatasetReader
from labelstudio_converter.document import BinaryRelation, Document, LabeledSpan


class LabelStudioJsonReader(DatasetReader):
    def __init__(self, doc_id_field: Optional[str] = None, additional_data_fields: Optional[List[str]] = None) -> None:
        self.doc_id_field = doc_id_field
        self.additional_data_fields = additional_data_fields or []

    def read(self, path: str) -> List[Document]:
        with open(path, "r", encoding="utf-8") as data_file:
            data = json.load(data_file)

        documents: List[Document] = []
        for instance in data:
            assert "data" in instance, "instance has no field 'data'."

            text = instance["data"]["text"]

            doc_id = str(instance["id"]) if self.doc_id_field is None else instance["data"][self.doc_id_field]

            document = Document(text=text, doc_id=doc_id)

            for field in self.additional_data_fields:
                field_value = instance["data"].get(field)
                if field_value is not None:
                    document.metadata[field] = field_value

            assert "annotations" in instance, "instance has no field 'annotations'."

            annotations_by_annotator = instance["annotations"]
            if not annotations_by_annotator:
                continue

            # we use the annotations of the first annotator
            annotations = annotations_by_annotator[0]

            # make sure 'labels' (labeled spans) appear before 'relations'
            annotation_results = sorted(annotations["result"], key=lambda a: a["type"])

            id_to_annotation: Dict[str, LabeledSpan] = {}
            for annotation in annotation_results:
                annotation_type = annotation["type"]

                if annotation_type == "labels":
                    annotation_id = annotation["id"]
                    start = annotation["value"]["start"]
                    end = annotation["value"]["end"]
                    labels = annotation["value"]["labels"]

                    if len(labels) > 0:
                        annotation = LabeledSpan(
                            start=start,
                            end=end,
                            label=labels if len(labels) > 1 else labels[0],
                            metadata={"id": annotation_id},
                        )
                        document.add_annotation("entities", annotation)
                        id_to_annotation[annotation_id] = annotation

                elif annotation_type == "relation":
                    from_id = annotation["from_id"]
                    to_id = annotation["to_id"]
                    labels = annotation["labels"]

                    # TODO: log relations without labels
                    if len(labels) > 0:
                        annotation = BinaryRelation(
                            head=id_to_annotation[from_id],
                            tail=id_to_annotation[to_id],
                            label=labels if len(labels) > 1 else labels[0],
                        )
                        document.add_annotation("relations", annotation)

                else:
                    raise Exception("unknown annotation type '{}'" % annotation_type)

            documents.append(document)

        return documents
