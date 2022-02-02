import os
from test import FIXTURES_ROOT

from labelstudio_converter.dataset_readers.labelstudio_json import LabelStudioJsonReader


def test_read_labelstudio_json():
    reader = LabelStudioJsonReader(additional_data_fields=["url"])

    data_path = os.path.join(FIXTURES_ROOT, "data/labelstudio/data.json")
    documents = reader.read(data_path)

    assert len(documents) == 2
