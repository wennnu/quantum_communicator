import random
import string

from bb84 import generate_key, EveDetectedError
from module import letter_to_bits, bits_to_letter, xor_bits

ALPHABET = string.ascii_lowercase
BITS_PER_LETTER = 5
MAX_GUESSES = 26


class RoundCipher:
    def __init__(
        self,
        word_length,
        eve_knowledge=0.25,
        intercept_probability=0.25,
    ):
        if not 1 <= word_length <= 26:
            raise ValueError("Word length must be between 1 and 26.")

        self.word_length = word_length
        self.eve_knowledge = max(0.0, min(1.0, eve_knowledge))

        # Reserve separate key segments for Alice's word and Bob's guesses.
        self.word_key_length = word_length * BITS_PER_LETTER
        self.guess_key_start = self.word_key_length
        self.guess_key_length = MAX_GUESSES * BITS_PER_LETTER
        self.session_key_length = (
            self.word_key_length + self.guess_key_length
        )

        # Establish a BB84 session, retrying if excessive errors are detected.
        for _ in range(8):
            try:
                result = generate_key(
                    self.session_key_length,
                    intercept_probability=intercept_probability,
                )
                break
            except EveDetectedError:
                continue
        else:
            raise RuntimeError(
                "BB84 could not establish a key after repeated "
                "eavesdropping detections."
            )

        self.key = result["key"]
        self.qber = result["qber"]
        self.intercepted_signals = result["eve_intercepts"]

        # Eve learns a random fraction of the actual session-key bits.
        known_count = round(
            len(self.key) * self.eve_knowledge
        )
        known_positions = set(
            random.sample(range(len(self.key)), known_count)
        )

        self.eve_known_bits = {
            index: int(self.key[index])
            for index in known_positions
        }

        # Bob's guesses use their own part of the key.
        self.guess_cursor = self.guess_key_start
        self.current_indices = []
        self.current_ciphertext = None

    def encrypt_word(self, word):
        """
        Encrypt Alice's secret word.

        Returns one (ciphertext, key_indices) pair per character.
        Eve receives these pairs, not the plaintext word.
        """
        if len(word) != self.word_length:
            raise ValueError("Unexpected secret-word length.")

        encrypted_word = []

        for position, letter in enumerate(word):
            start = position * BITS_PER_LETTER
            indices = list(
                range(start, start + BITS_PER_LETTER)
            )

            key_bits = "".join(self.key[i] for i in indices)
            ciphertext = xor_bits(
                letter_to_bits(letter),
                key_bits,
            )

            encrypted_word.append((ciphertext, indices))

        return encrypted_word

    def encode_letter(self, letter):
        """Encrypt Bob's next guess with a fresh five-bit key segment."""
        if self.guess_cursor + BITS_PER_LETTER > len(self.key):
            raise RuntimeError("The guess-key segment has been exhausted.")

        start = self.guess_cursor
        self.current_indices = list(
            range(start, start + BITS_PER_LETTER)
        )

        key_bits = "".join(
            self.key[i] for i in self.current_indices
        )

        ciphertext = xor_bits(
            letter_to_bits(letter),
            key_bits,
        )

        self.guess_cursor += BITS_PER_LETTER
        self.current_ciphertext = ciphertext

        return ciphertext

    def decode_letter(self, encoded_code):
        """Alice decrypts Bob's ciphertext using the shared key."""
        if encoded_code != self.current_ciphertext:
            raise ValueError("Unexpected ciphertext.")

        key_bits = "".join(
            self.key[i] for i in self.current_indices
        )

        plaintext_bits = xor_bits(encoded_code, key_bits)
        return bits_to_letter(plaintext_bits)

    def get_possible_letters_for_block(self, ciphertext, key_indices):
        """
        Find plaintext letters consistent with Eve's known key bits
        for one particular encrypted character.
        """
        possible = set()

        for letter in ALPHABET:
            plaintext_bits = letter_to_bits(letter)
            inferred_key = xor_bits(ciphertext, plaintext_bits)

            consistent = all(
                inferred_key[offset] == str(
                    self.eve_known_bits[key_index]
                )
                for offset, key_index in enumerate(key_indices)
                if key_index in self.eve_known_bits
            )

            if consistent:
                possible.add(letter)

        return possible

    def get_possible_letters(self, encoded_code):
        """Infer possible plaintext letters for Bob's latest guess."""
        return self.get_possible_letters_for_block(
            encoded_code,
            self.current_indices,
        )

    def get_word_candidates(self, encrypted_word):
        """Infer independent candidate letters for every word position."""
        return [
            self.get_possible_letters_for_block(ciphertext, indices)
            for ciphertext, indices in encrypted_word
        ]

    def try_learn_current_key_bits(self, probability):
        """
        Give Eve a probability of learning the key bits used
        for Bob's current encrypted guess.

        Returns True if Eve learns this block.
        """
        probability = max(0.0, min(1.0, probability))

        if random.random() >= probability:
            return False

        for index in self.current_indices:
            self.eve_known_bits[index] = int(self.key[index])

        return True