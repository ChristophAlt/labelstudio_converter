import os
from test import FIXTURES_ROOT

from anno_converter.dataset_readers.labelstudio_json import LabelStudioJsonReader
from anno_converter.dataset_writers.flair_conllu import FlairConlluDatasetWriter
from anno_converter.tokenizers.segtok import SegtokTokenizer


def test_write_flair_conllu():
    reader = LabelStudioJsonReader(additional_data_fields=["url"])

    # data_path = os.path.join(FIXTURES_ROOT, "data/labelstudio/data.json")
    data_path = "/home/christoph/Downloads/project-1-at-2021-11-02-07-52-ee6cd262.json"
    documents = reader.read(data_path)

    tokenizer = SegtokTokenizer()
    writer = FlairConlluDatasetWriter(tokenizer=tokenizer)

    writer.write("/home/christoph/Downloads/quote_extraction_20.conllup", documents)
