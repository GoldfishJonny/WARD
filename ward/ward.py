from neo4j import GraphDatabase
import random

class WARD:
    """
    Word And Root Development (WARD) class for generating words and roots.
    ...
    Attributes
    ----------
    uri : str
        URI for the Neo4j database.
    user : str
        Username for the Neo4j database.
    password : str
        Password for the Neo4j database.
    driver : GraphDatabase.driver
        Neo4j driver object.
    
    Methods
    -------
    close()
        Closes the connection to the Neo4j database.

    create_letter(letter, type)
        Creates a letter node in Neo4j if it doesn't already exist.

    letter_exists(letter)
        Checks if a letter exists in Neo4j.

    generate_alphabet(consonants, vowels)
        Reads consonants and vowels from lists and stores them in Neo4j.

    get_letters_from_type(letter_type)
        Fetches consonants or vowels from Neo4j.
    
    get_letters()
        Fetches letters from Neo4j.

    create_syllable(syllable)
        Creates a syllable node in Neo4j and links it to its letters.

    syllable_exists(syllable)
        Checks if a syllable exists in Neo4j.
    
    get_syllables()
        Fetches syllables from Neo4j.
    
    get_syllable(syllable)
        Fetches a specific syllable from Neo4j.

    generate_syllables(pattern, count)
        Generates syllables based on a pattern.
    
    get_syllable_count()
        Returns the number of syllables in the database.
    
    delete_syllables()
        Deletes all syllables in the database.
    
    delete_syllable(syllable)
        Deletes a specific syllable from the database.
    
    delete_letters()
        Deletes all letters in the database.
    
    delete_letter(letter)
        Deletes a specific letter from the database.
    """
    def __init__(self, uri: str, user: str , password: str):
        """
        Parameters
        ----------
        uri : str
            URI for the Neo4j database.
        user : str
            Username for the Neo4j database.
        password : str
            Password for the Neo4j database.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        """Closes the connection to the Neo4j database."""
        self.driver.close()

    def create_letter(self, letter: str, type: str):
        """Creates a letter node in Neo4j if it doesn't already exist.

        If the letter already exists, this function does nothing.

        Parameters
        ----------
        letter : str
            The letter to be created.
        type : str
            The type of the letter, either "consonant" or "vowel".
        """
        with self.driver.session() as session:
            if not self.letter_exists(letter):
                CREATE_LETTER = "MERGE (l:Letter {letter: $letter, type: $type}) RETURN l"
                session.run(CREATE_LETTER, letter=letter, type=type)

    def letter_exists(self, letter: str) -> bool:
        """Checks if a letter exists in Neo4j.
        
        If the letter exists, this function returns True. Otherwise, it returns False.

        Parameters
        ----------
        letter : str
            The letter to check for existence.
        """
        with self.driver.session() as session:
            result = session.run("MATCH (l:Letter) WHERE l.letter = $letter RETURN l", letter=letter)
            return True if result.single() else False
    
    def generate_alphabet(self, consonants: list, vowels: list):
        """Reads consonants and vowels from lists and stores them in Neo4j.
    
        Parameters
        ----------
        consonants : list
            A list of consonants.
        vowels : list
            A list of vowels.
        """
        for letters in consonants + vowels:
            letter_type = "consonant" if letters in consonants else "vowel"
            self.create_letter(letters, letter_type)

    def get_letters(self):
        """Fetches letters from Neo4j."""
        with self.driver.session() as session:
            result = session.run("MATCH (l:Letter) RETURN l.letter")
            return [record["l.letter"] for record in result]

    def get_letters_from_type(self, letter_type):
        """Fetches consonants or vowels from Neo4j.
        
        Parameters
        ----------
        letter_type : str
            The type of letters to fetch, either "consonant" or "vowel".
        """
        with self.driver.session() as session:
            result = session.run("MATCH (l:Letter) WHERE l.type = $type RETURN l.letter", type=letter_type)
            return [record["l.letter"] for record in result]
        
    def create_syllable(self, syllable: str):
        """Creates a syllable node in Neo4j and links it to its letters.
        
        If any of the letters in the syllable do not exist, this function does nothing.
        
        Parameters
        ----------
        syllable : str
            The syllable to be created.
        """
        with self.driver.session() as session:
            letters = list(syllable)
            existing_letters = self.get_letters()
            if not all(letter in existing_letters for letter in letters):
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
    
    def syllable_exists(self, syllable: str) -> bool:
        """Checks if a syllable exists in Neo4j.
        
        If the syllable exists, this function returns True. Otherwise, it returns False.
        
        Parameters
        ----------
        syllable : str
            The syllable to check for existence.
        """
        with self.driver.session() as session:
            result = session.run("MATCH (s:Syllable) WHERE s.syllable = $syllable RETURN s", syllable=syllable)
            return True if result.single() else False
    
    def get_syllables(self):
        """Fetches syllables from Neo4j."""
        with self.driver.session() as session:
            result = session.run("MATCH (s:Syllable) RETURN s.syllable")
            return [record["s.syllable"] for record in result]
    
    def get_syllable(self, syllable: str):
        """Fetches a specific syllable from Neo4j.
        
        Parameters
        ----------
        syllable : str"""
        with self.driver.session() as session:
            result = session.run("MATCH (s:Syllable {syllable: $syllable}) RETURN s.syllable", syllable=syllable)
            return result.single()["s.syllable"]
    
    def set_syllables(self, syllables: list):
        """Sets syllables in the database.
        
        If a syllable already exists, this function does nothing.
        
        Parameters
        ----------
        syllables : list
            A list of syllables to be set in the database.
        """
        for syllable in syllables:
            if not self.syllable_exists(syllable):
                self.create_syllable(syllable)
    
    def set_syllable(self, syllable: str):
        """Sets a syllable in the database.
        
        If the syllable already exists, this function does nothing.
        
        Parameters
        ----------
        syllable : str
            The syllable to be set in the database.
        """
        if not self.syllable_exists(syllable):
            self.create_syllable(syllable)
        
    def generate_syllables(self, patterns: list =["CV"], count = 100, rule_function=None):
        """Generates syllables based on a pattern.

        If there are no consonants or vowels in the database, this function does nothing.
        If a rule function is provided, it will be used to filter out syllables that do not meet the rule.

        Parameters
        ----------
        patterns : list
            A list of patterns to generate syllables from.
        count : int
            The number of syllables to generate.
        rule_function : function
            A function that takes a letter as input and returns True or False.
        """
        consonants = self.get_letters_from_type("consonant")
        vowels = self.get_letters_from_type("vowel")

        if not consonants or not vowels:
            print("Error: No consonants or vowels found in the database.")
            return
        
        generated_syllables = set()

        while len(generated_syllables) < count:
            pattern = random.choice(patterns)
            syllable = "".join([random.choice(consonants) if letter == "C" else random.choice(vowels) for letter in pattern])
        
            
            if syllable in generated_syllables:
                continue

            if rule_function is None or rule_function(syllable):
                generated_syllables.add(syllable)
                self.create_syllable(syllable)
    
    def get_syllable_count(self):
        """Returns the number of syllables in the database."""
        with self.driver.session() as session:
            result = session.run("MATCH (s:Syllable) RETURN COUNT(s) AS count")
            return result.single()["count"]
    
    def delete_syllables(self):
        """Deletes all syllables in the database."""
        with self.driver.session() as session:
            session.run("MATCH (s:Syllable) DETACH DELETE s")
    
    def delete_syllable(self, syllable: str):
        """Deletes a specific syllable from the database.
        
        Parameters
        ----------
        syllable : str
            The syllable to delete.
        """
        with self.driver.session() as session:
            session.run("MATCH (s:Syllable {syllable: $syllable}) DETACH DELETE s", syllable=syllable)
    
    def delete_letters(self):
        """Deletes all letters in the database."""
        with self.driver.session() as session:
            session.run("MATCH (l:Letter) DETACH DELETE l")
    
    def delete_letter(self, letter: str):
        """Deletes a specific letter from the database.
        
        Parameters
        ----------
        letter : str
            The letter to delete.
        """
        with self.driver.session() as session:
            session.run("MATCH (l:Letter {letter: $letter}) DETACH DELETE l", letter=letter)