import random
import string

ALPHABET = string.ascii_lowercase
ALL_CODES = [f"{n:05b}" for n in range(32)]


class RoundCipher:
    def __init__(self, eve_knowledge=0.25):
        """
        eve_knowledge = fraction of the alphabet Eve can
        eliminate for each encrypted character.

        Example:
            0.25 -> approximately 20 candidates remain
            0.50 -> approximately 13 candidates remain
            0.75 -> approximately 7 candidates remain
        """
        self.eve_knowledge = max(0.0, min(1.0, eve_knowledge))

        # Every letter gets a unique 5-bit code this round.
        codes = random.sample(ALL_CODES, len(ALPHABET))
        self.encode_map = dict(zip(ALPHABET, codes))
        self.decode_map = {
            code: letter for letter, code in self.encode_map.items()
        }

        # Determine how many letters Eve can rule out.
        eliminated_count = round(
            len(ALPHABET) * self.eve_knowledge
        )
        candidate_count = len(ALPHABET) - eliminated_count

        # Each ciphertext has a fixed candidate set.
        # Its true plaintext letter is always included.
        self.candidates_by_code = {}

        for letter, code in self.encode_map.items():
            other_letters = [
                candidate
                for candidate in ALPHABET
                if candidate != letter
            ]

            other_count = candidate_count - 1
            selected = random.sample(other_letters, other_count)

            self.candidates_by_code[code] = set(
                selected + [letter]
            )

    def encode_letter(self, letter):
        """Encrypt a plaintext letter."""
        return self.encode_map[letter.lower()]

    def decode_letter(self, encoded_code):
        """Alice decrypts a letter."""
        return self.decode_map[encoded_code]

    def get_possible_letters(self, encoded_code):
        """
        Eve sees candidate letters, not the encoded bits.
        """
        return sorted(self.candidates_by_code[encoded_code])

    def get_word_candidates(self, word):
        """
        Return Eve's initial candidate letters for each
        character in Alice's encrypted word.
        """
        return [
            set(self.get_possible_letters(self.encode_letter(letter)))
            for letter in word.lower()
        ]