from labelstudio_converter.dataset_readers.labelstudio_json import LabelStudioJsonReader
from labelstudio_converter.dataset_writers.flair_conllu import FlairConlluDatasetWriter
from labelstudio_converter.tokenizers.segtok import SegtokTokenizer


def convert_file(
    input_file: str,
    output_file: str,
    output_format: str,
) -> None:
    reader = LabelStudioJsonReader(additional_data_fields=["url"])

    documents = reader.read(input_file)

    if output_format == "flair_conllu":
        tokenizer = SegtokTokenizer()
        writer = FlairConlluDatasetWriter(tokenizer=tokenizer)

    writer.write(output_file, documents)
