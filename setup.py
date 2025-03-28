from setuptools import setup, find_packages

setup(
    name="ward-lang",  # Package name
    version="0.0.1",  # Version
    packages=find_packages(),
    install_requires=[
        "neo4j",
    ],
    author="GoldfishJonny",
    description="WARD:(Word And Root Development) A modular library for word and morpheme construction.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GoldfishJonny/WARD",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)