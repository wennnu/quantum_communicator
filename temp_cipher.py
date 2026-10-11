import random
import string

from bb84 import generate_key, EveDetectedError
from module import letter_to_bits, bits_to_letter, xor_bits

ALPHABET = string.ascii_lowercase
MAX_GUESSES = 26
BITS_PER_LETTER = 5
SESSION_KEY_LENGTH = MAX_GUESSES * BITS_PER_LETTER


class RoundCipher:
    def __init__(
        self,
        eve_knowledge=0.25,
        intercept_probability=0.25,
    ):
        self.eve_knowledge = max(0.0, min(1.0, eve_knowledge))

        # Retry if the BB84 sample detects excessive errors.
        # In this game, Eve's interception probability is fixed
        # for a session; retries model establishing a fresh session.
        for _ in range(8):
            try:
                result = generate_key(
                    SESSION_KEY_LENGTH,
                    intercept_probability=intercept_probability,
                )
                break
            except EveDetectedError:
                continue
        else:
            raise RuntimeError(
                "BB84 could not establish a key after repeated "
                "eavesdropping detections. Try a lower interception "
                "probability or a larger test sample."
            )

        self.key = result["key"]
        self.qber = result["qber"]
        self.intercepted_signals = result["eve_intercepts"]

        self.cursor = 0
        self.current_indices = []
        self.current_ciphertext = None

        # Eve initially knows the values of a random fraction
        # of the session's key bits.
        known_count = round(
            len(self.key) * self.eve_knowledge
        )
        known_positions = set(
            random.sample(range(len(self.key)), known_count)
        )

        self.eve_known_bits = {
            i: int(self.key[i])
            for i in known_positions
        }

    def encode_letter(self, letter):
        """Encrypt a letter using the next five session-key bits."""
        if self.cursor + BITS_PER_LETTER > len(self.key):
            raise RuntimeError("The session key has been exhausted.")

        plaintext_bits = letter_to_bits(letter)
        self.current_indices = list(
            range(self.cursor, self.cursor + BITS_PER_LETTER)
        )

        key_bits = self.key[self.cursor:self.cursor + BITS_PER_LETTER]
        ciphertext = xor_bits(plaintext_bits, key_bits)

        self.cursor += BITS_PER_LETTER
        self.current_ciphertext = ciphertext

        return ciphertext

    def decode_letter(self, encoded_code):
        """Alice decrypts the ciphertext using the shared key."""
        if encoded_code != self.current_ciphertext:
            raise ValueError("Unexpected ciphertext.")

        key_bits = "".join(
            self.key[i] for i in self.current_indices
        )
        plaintext_bits = xor_bits(encoded_code, key_bits)
        return bits_to_letter(plaintext_bits)

    def get_possible_letters(self, encoded_code):
        """Return letters consistent with Eve's known key bits."""
        possible = []

        for letter in ALPHABET:
            plaintext_bits = letter_to_bits(letter)
            inferred_key = xor_bits(encoded_code, plaintext_bits)

            if all(
                inferred_key[offset] == str(known_bit)
                for offset, key_index in enumerate(self.current_indices)
                if key_index in self.eve_known_bits
                for known_bit in [self.eve_known_bits[key_index]]
            ):
                possible.append(letter)

        return sorted(possible)

    def get_word_candidates(self, word):
        """
        Eve knows the word length, not the secret word's
        encryption mapping. Start with all letters possible
        at every position.
        """
        return [set(ALPHABET) for _ in word]