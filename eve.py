import string

ALPHABET = string.ascii_lowercase


class Eve:
    def __init__(self, position_candidates, words, cipher):
        self.word_length = len(position_candidates)
        self.words = {
            word.lower()
            for word in words
            if word.isascii() and word.isalpha()
        }
        self.cipher = cipher

        # Keep only the dictionary words of the correct length.
        # Do not assume that the word is known just because a
        # dictionary happens to contain very few matching words.
        self.candidates = {
            word for word in self.words
            if len(word) == self.word_length
        }

        self.observations = []
        self.notes = []

    def observe(self, possible_letters, positions):
        """Record the ciphertext possibilities and Alice's feedback."""
        possible_letters = set(possible_letters) & set(ALPHABET)
        positions = sorted(positions)

        self.observations.append({
            "number": len(self.observations) + 1,
            "possible_letters": possible_letters,
            "positions": positions,
        })

        # Retain words that could explain Alice's response.
        self.candidates = {
            word for word in self.candidates
            if self._matches_feedback(
                word, possible_letters, positions
            )
        }

    @staticmethod
    def _matches_feedback(word, possible_letters, positions):
        reported = set(positions)

        for letter in possible_letters:
            actual = {
                i
                for i, character in enumerate(word, start=1)
                if character == letter
            }

            if actual == reported:
                return True

        return False

    def display(self):
        print("\n" + "=" * 44)
        print("                 EVE'S VIEW")
        print("=" * 44)

        print(f"\nSecret word length: {self.word_length}")
        print(f"Remaining candidate words: {len(self.candidates)}")

        known = len(self.cipher.eve_known_bits)
        total = len(self.cipher.key)
        percent = 100 * known / total if total else 0

        print(
            f"Cipher knowledge: {known}/{total} key bits "
            f"({percent:.1f}%)"
        )

        print("\nPossible plaintext letters per observation:")

        if not self.observations:
            print("(No ciphertexts observed yet.)")

        for observation in self.observations:
            letters = observation["possible_letters"]
            print(
                f"Guess #{observation['number']}: "
                f"{len(letters)} possibilities — "
                + (", ".join(sorted(letters)) or "(none)")
            )

            positions = observation["positions"]
            print(
                "  Alice's response: "
                + (", ".join(map(str, positions)) or "absent")
            )

        print("\nWord candidates:")
        if self.candidates:
            # Do not reveal the candidate word list to the player.
            print(
                f"{len(self.candidates)} words remain consistent "
                "with the observations."
            )
        else:
            print("No dictionary words match the observations.")

        print("\nYour notes:")
        if self.notes:
            for i, note in enumerate(self.notes, start=1):
                print(f"{i}. {note}")
        else:
            print("(No notes yet)")

    def add_note(self):
        note = input(
            "\nEve, add a deduction or note (Enter to skip): "
        ).strip()

        if note:
            self.notes.append(note)

    def final_guess(self):
        while True:
            guess = input(
                f"\nEve, enter your final word guess "
                f"({self.word_length} letters): "
            ).strip().lower()

            if (
                len(guess) == self.word_length
                and all(c in ALPHABET for c in guess)
            ):
                return guess

            print(
                f"Please enter exactly {self.word_length} "
                "English letters."
            )