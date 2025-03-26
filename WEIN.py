from neo4j import GraphDatabase
import sys
import random

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"


def read_file(file_path):
    """Reads IPA symbols from a file, stripping whitespace and adding checks."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []

class WEIN:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    def close(self):
        self.driver.close()

    def create_letter(self, letter, type):
        """Creates a letter node in Neo4j if it doesn't already exist."""
        with self.driver.session() as session:
            if not self.letter_exists(letter):
                CREATE_LETTER = "MERGE (l:Letter {letter: $letter, type: $type}) RETURN l"
                session.run(CREATE_LETTER, letter=letter, type=type)

    def letter_exists(self, letter):
        """Checks if a letter exists in Neo4j."""
        with self.driver.session() as session:
            result = session.run("MATCH (l:Letter) WHERE l.letter = $letter RETURN l", letter=letter)
            return result.single() is not None

    def create_syllable(self, syllable):
        """Creates a syllable node in Neo4j and links it to its letters."""
        with self.driver.session() as session:
            letters = list(syllable)
            for letter in letters:
                if not self.letter_exists(letter):
                    return
                
            if not self.syllable_exists(syllable):
                CREATE_SYLLABLE = "MERGE (s:Syllable {syllable: $syllable}) RETURN s"
                session.run(CREATE_SYLLABLE, syllable=syllable)

            for letter in letters:
                session.run(
                    """
                    MATCH (s:Syllable {syllable: $syllable})
                    MATCH (l:Letter {letter: $letter})
                    MERGE (s)-[:HAS_LETTER]->(l)
                    """, 
                    syllable=syllable,
                      letter=letter)
    
    def syllable_exists(self, syllable):
        """Checks if a syllable exists in Neo4j."""
        with self.driver.session() as session:
            result = session.run("MATCH (s:Syllable) WHERE s.syllable = $syllable RETURN s", syllable=syllable)
            return result.single() is not None
    
    def generate_alphabet(self, consonants, vowels):
        """Reads consonants and vowels from files and stores them in Neo4j."""
        consonants = read_file(consonants)
        vowels = read_file(vowels)

        for consonant in consonants:
            c = self.create_letter(consonant, "consonant")
        for vowel in vowels:
            s = self.create_letter(vowel, "vowel")

    def get_letters(self, letter_type):
        """Fetches consonants or vowels from Neo4j."""
        with self.driver.session() as session:
            result = session.run("MATCH (l:Letter) WHERE l.type = $type RETURN l.letter", type=letter_type)
            return [record["l.letter"] for record in result]
        
    def generate_syllables(self, pattern="CV", count=100):
        consonants = self.get_letters("consonant")
        vowels = self.get_letters("vowel")

        if not consonants or not vowels:
            print("Error: No consonants or vowels found in the database.")
            return
        
        for _ in range(count):
            syllable = ""
            for char in pattern:
                if char == "C":
                    syllable += random.choice(consonants)
                elif char == "V":
                    syllable += random.choice(vowels)
                print(f"Generated syllable: {syllable}")
                self.create_syllable(syllable)


