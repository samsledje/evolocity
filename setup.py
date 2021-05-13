from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="evolocity",
    version="0.0.1",
    python_requires=">=3.6",
    install_requires=[
        l.strip() for l in Path("requirements.txt").read_text("utf-8").splitlines()
    ],
    packages=find_packages(),
    author="Brian Hie",
    author_email="brianhie@stanford.edu",
    description="Evolutionary velocity with protein language models",
    license="MIT",
    url="https://github.com/brianhie/evolocity",
    download_url="https://github.com/brianhie/evolocity",
    keywords=[
        "evolution",
        "velocity",
        "evolocity",
        "protein",
        "language model",
    ],
)
