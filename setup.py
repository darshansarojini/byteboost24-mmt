#!/usr/bin/env python
from setuptools import setup

# Read the requirements from the requirements.in file
with open("requirements.in") as f:
    requirements = f.read().splitlines()

setup(
    name="pylib",
    version="0.0.0",
    packages=["pylib"],
    install_requires=requirements,
    author="Matthew Andres Moreno",
    author_email="morenoma@umich.edu",
    description="Byteboost 24 MMT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
