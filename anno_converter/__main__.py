import argparse
import logging

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
    "--input-format",
    required=True,
    type=str,
    choices=["labelstudio_json"],
    help="format of the input dataset",
)
parser.add_argument(
    "--output-format",
    type=str,
    default="flair_conll",
    choices=["flair_conll"],
    help="format the annotated dataset is stored",
)
parser.add_argument(
    "--n-jobs",
    type=int,
    default=1,
    help="the number of request jobs to run in parallel",
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

    convert_file(
        input_file=args.input_file,
        output_file=args.output_file,
        input_format=args.input_format,
        output_format=args.output_format,
        n_jobs=args.n_jobs,
        debug=args.debug,
    )


if __name__ == "__main__":
    main()
