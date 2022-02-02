from setuptools import find_packages, setup

setup(
    name="labelstudio_converter",
    version="0.0.1",
    description="Convert Label Studio annotation files to other formats.",
    author="Christoph Alt",
    author_email="christoph.alt@posteo.de",
    url="https://github.com/ChristophAlt/labelstudio_converter",
    install_requires=["conllu>=4.4.0", "segtok>=1.5.10"],
    packages=find_packages(),
)
