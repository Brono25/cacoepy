from setuptools import setup, find_packages
import pathlib

ROOT = pathlib.Path(__file__).parent
README = (ROOT / "README.md").read_text()

with open(ROOT / "requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="cacoepy",
    version="1.0.0",
    description="A Python module for aligning mispronounced phonemes.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Bronston Ashford",
    author_email="bronston.a@gmail.com",
    url="https://github.com/Brono25/cacoepy.git",
    packages=find_packages(where="src"),
    package_dir={"": "cacoepy"},
    include_package_data=True,
    package_data={
        "": ["data/*.json"],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
