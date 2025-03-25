from neo4j import GraphDatabase
import sys

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

# if len(sys.argv) > 1:
#     NEO4J_URI = sys.argv[1]
#     NEO4J_USER = sys.argv[1]
#     NEO4J_PASSWORD = sys.argv[2]

def read_file(file_path):
    """Reads IPA symbols from a file, stripping whitespace and adding checks."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []

class WEIN_Agent:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    def close(self):
        self.driver.close()

    def create_letter(self, letter, type):
        with self.driver.session() as session:
            if not self.letter_exists(letter):
                CREATE_LETTER = "CREATE (l:Letter {letter: $letter, type: $type}) RETURN l"
                session.run(CREATE_LETTER, letter=letter)

    
    def letter_exists(self, letter):
        with self.driver.session() as session:
            result = session.run("MATCH (l:Letter) WHERE l.letter = $letter RETURN l", letter=letter)
            return result.single() is not None


    def create_syllable(self, syllable):
        with self.driver.session() as session:
            if not self.syllable_exists(syllable):
                CREATE_SYLLABLE = "CREATE (s:Syllable {syllable: $syllable}) RETURN s"
                session.run(CREATE_SYLLABLE, syllable=syllable)
            letters = list(syllable)
            for letter in letters:
                # cannot create relationship if letter does not exist
                if not self.letter_exists(letter):
                    # return error
                    return
                session.run("MATCH (s:Syllable {syllable: $syllable}) MATCH (l:Letter {letter: $letter}) CREATE (s)-[:HAS_LETTER]->(l)", syllable=syllable, letter=letter)
    
    def syllable_exists(self, syllable):
        with self.driver.session() as session:
            result = session.run("MATCH (s:Syllable) WHERE s.syllable = $syllable RETURN s", syllable=syllable)
            return result.single() is not None
    
    def generate_alphabet(self, consonants, vowels):
        consonants = read_file(consonants)
        vowels = read_file(vowels)
        with self.driver.session() as session:
            for consonant in consonants:
                c = self.create_letter(consonant, )
            for vowel in vowels:
                self.create_letter(vowel)

    

if __name__ == "__main__":
    agent = WEIN_Agent()
    ka = agent.create_syllable("ka")
    print(ka)