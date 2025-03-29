from ward import WARD

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"
W = WARD(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
W.create_letter("a", "vowel")
W.create_letter("b", "consonant")
W.create_syllable("ab")
W.create_syllable("ba")
W.create_morpheme(["ab", "ba"])
