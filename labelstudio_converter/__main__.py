import argparse
import logging
import os

from anno_converter.convert import convert_file

parser = argparse.ArgumentParser()  # pylint: disable=invalid-name
parser.add_argument(
    "--input-file",
    required=True,
    type=str,
    help="path containing the dataset to be converted",
)
parser.add_argument(
    "--output-file",
    required=True,
    type=str,
    help="path to store the converted dataset",
)
parser.add_argument(
    "--output-format",
    type=str,
    default="flair_conllu",
    choices=["flair_conllu"],
    help="format the annotated dataset is stored",
)
parser.add_argument(
    "--debug",
    action="store_true",
    default=False,
    help="enable debug logging",
)


def main():
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=log_level)

    if not os.path.exists(args.input_file):
        raise FileNotFoundError("input file '{}' does not exist.".format(args.input_file))

    convert_file(
        input_file=args.input_file,
        output_file=args.output_file,
        output_format=args.output_format,
    )


if __name__ == "__main__":
    main()
