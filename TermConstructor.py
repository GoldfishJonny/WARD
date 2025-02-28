import random

class Alphabet:
    """Represents an alphabet containing consonants and vowels."""
    def __init__(self, consonants, vowels):
        self.consonants = consonants
        self.vowels = vowels

    def get_consonants(self):
        return self.consonants

    def get_vowels(self):
        return self.vowels

class SyllableGenerator:
    """Generates and stores syllables following phonotactic rules."""
    def __init__(self, alphabet, syllable_structures=None):
        self.alphabet = alphabet
        self.syllable_structures = syllable_structures or ["CV", "CVC"]
        self.generated_syllables = set()  # Store unique syllables

    def generate_all_syllables(self):
        """Generate all possible syllables based on available consonants and vowels."""
        for structure in self.syllable_structures:
            if structure == "CV":
                for c in self.alphabet.get_consonants():
                    for v in self.alphabet.get_vowels():
                        syllable = c + v
                        self.generated_syllables.add(syllable)
            elif structure == "CVC":
                for c1 in self.alphabet.get_consonants():
                    for v in self.alphabet.get_vowels():
                        for c2 in self.alphabet.get_consonants():
                            syllable = c1 + v + c2
                            self.generated_syllables.add(syllable)

    def save_syllables(self, file_path):
        """Saves generated syllables to a file."""
        with open(file_path, "w", encoding="utf-8") as file:
            for syllable in self.generated_syllables:
                file.write(syllable + "\n")

class WordStemGenerator:
    """Generates word stems by combining non-repeating syllables."""
    def __init__(self, syllable_generator):
        self.syllable_generator = syllable_generator
        self.restricted_ending_sounds = ['w', 'j', 'h']
        self.generated_words = set()

    def remove_restricted_ending(self, word):
        """Removes /w/, /j/, or /h/ from the end of the word if the next syllable is not a vowel or it's the last syllable."""
        syllables = [word[i:i+2] for i in range(0, len(word), 2)]  # Split word into syllables (CV, CVC)
        modified_word = syllables
        
        # Iterate through syllables and check the last one
        for i in range(len(syllables) - 1, -1, -1):
            syllable = syllables[i]
            if syllable[-1] in self.restricted_ending_sounds:  # Check if ends with w, j, or h
                # If next syllable is not a vowel or it's the last syllable, remove the restricted sound
                if i == len(syllables) - 1 or syllables[i + 1][0] not in self.syllable_generator.alphabet.get_vowels():
                    syllables[i] = syllable[:-1]  # Remove the last character

        return "".join(syllables)

    def generate_word_stem(self, num_syllables=2):
        """Generates a word stem ensuring syllables are not reused in the same order."""
        available_syllables = list(self.syllable_generator.generated_syllables)
        random.shuffle(available_syllables)  # Mix syllables to avoid repetition
        word = "".join(available_syllables[:num_syllables])
        word = self.remove_restricted_ending(word)

        # If the word already exists after modification, rework it
        if word in self.generated_words:
            return self.generate_word_stem(num_syllables)  # Recursively generate a new word

        self.generated_words.add(word)
        return word

    def save_word_stems(self, file_path, num_stems=200):
        """Generates and saves unique word stems with 1, 2, or 3 syllables."""
        used_stems = set()
        with open(file_path, "w", encoding="utf-8") as file:
            for _ in range(num_stems):
                while True:
                    # Randomly choose 1, 2, or 3 syllables for the word stem
                    num_syllables = random.choice([1, 2, 3])
                    stem = self.generate_word_stem(num_syllables)
                    if stem not in used_stems:
                        used_stems.add(stem)
                        file.write(stem + "\n")
                        break

def read_file(file_path):
    """Reads IPA symbols from a file, stripping whitespace and adding checks."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []

# Load consonants and vowels from files
consonants = read_file("consonants.txt")
vowels = read_file("vowels.txt")

# Check if consonants and vowels are loaded correctly
if not consonants:
    print("Error: Consonants list is empty.")
if not vowels:
    print("Error: Vowels list is empty.")

# Construct alphabet
alphabet = Alphabet(consonants, vowels)

# Generate all possible syllables
syllable_generator = SyllableGenerator(alphabet)
syllable_generator.generate_all_syllables()

# Save syllables to file
syllable_generator.save_syllables("syllables.txt")

# Generate 200 word stems with 1, 2, or 3 syllables
word_stem_generator = WordStemGenerator(syllable_generator)
word_stem_generator.save_word_stems("word_stems.txt", num_stems=200)

print("Syllables and 200 word stems generated and saved.")
