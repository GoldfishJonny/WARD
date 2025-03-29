# WARD - Word And Root Developer

## Overview

WARD is a library designed to help in the creation and management of words, syllables, and roots. It uses **Neo4j** as a backend database to store letters, syllables, and relationships between them. The library provides an easy-to-use API to generate syllables based on patterns, store them in Neo4j, and fetch them as needed. You can also create and check for existing letters and syllables, providing a powerful foundation for future word and morpheme generation.

## Features

- **Letter Management**: Add, check, and retrieve letters (consonants and vowels) from the database.
- **Syllable Management**: Generate, store, and retrieve syllables. Link syllables to their constituent letters.
- **Pattern-based Syllable Generation**: Generate syllables based on user-defined patterns (e.g., CV, CVC).
- **Database Interaction**: Seamless interaction with Neo4j for all data persistence.

Future plans include the creation of morphemes, roots, and the ability to form words from them.

## Requirements

- Python 3.x
- Neo4j Database

## Installation

1. Install the `ward-lang` package:

    ```bash
    pip install ward-lang
    ```

2. Set up and run a **Neo4j** instance on your local machine or a remote server.

## Future Development

- Morpheme/Root Generation: Build on this system to generate morphemes and roots.

- Word Construction: Combine syllables, roots, and morphemes to generate full words.


