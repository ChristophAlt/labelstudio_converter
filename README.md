# Labelstudio Converter

## 🚀&nbsp;&nbsp;Quickstart

```sh
pip install git+ssh://git@github.com/ChristophAlt/labelstudio_converter.git
```

```sh
python labelstudio_converter \
    --input-file <INPUT FILE> \
    --output-file <OUTPUT FILE> \
    --output-format flair_conllu
```

## Development
```sh
# Install dependencies
pipenv install --dev

# Setup pre-commit and pre-push hooks
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```

## Credits
This package was created with Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.
