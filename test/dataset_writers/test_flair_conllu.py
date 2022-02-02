import os
from test import FIXTURES_ROOT

from labelstudio_converter.dataset_readers.labelstudio_json import LabelStudioJsonReader
from labelstudio_converter.dataset_writers.flair_conllu import FlairConlluDatasetWriter
from labelstudio_converter.tokenizers.segtok import SegtokTokenizer


def test_write_flair_conllu(tmp_path):
    reader = LabelStudioJsonReader(additional_data_fields=["url"])

    data_path = os.path.join(FIXTURES_ROOT, "data/labelstudio/data.json")
    documents = reader.read(data_path)

    tokenizer = SegtokTokenizer()
    writer = FlairConlluDatasetWriter(tokenizer=tokenizer)

    writer.write(os.path.join(tmp_path, "test.conllu"), documents)
