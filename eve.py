import string

ALPHABET = set(string.ascii_lowercase)


class Eve:
    def __init__(self, position_candidates, words, cipher):
        self.word_length = len(position_candidates)
        self.cipher = cipher

        # Preserve the candidates inferred from the encrypted word.
        # Do not reset them to the entire alphabet.
        self.position_candidates = [
            set(candidates) & ALPHABET
            for candidates in position_candidates
        ]

        self.observations = []
        self.notes = []
        self.partial_word = ""

    def observe(self, possible_letters, positions):
        """
        Record the candidate plaintext letters for Bob's encrypted
        guess and Alice's public feedback.

        Eve never receives Bob's plaintext guess directly.
        """
        possible_letters = set(possible_letters) & ALPHABET
        positions = sorted(set(positions))

        observation = {
            "number": len(self.observations) + 1,
            "possible_letters": possible_letters.copy(),
            "positions": positions.copy(),
        }
        self.observations.append(observation)

        if not possible_letters:
            return

        if positions:
            # A character reported at a position must be consistent
            # with both the word ciphertext and Bob's guess ciphertext.
            for position in positions:
                index = position - 1

                if 0 <= index < self.word_length:
                    self.position_candidates[index] &= possible_letters

            # All reported positions contain the same guessed letter.
            # Intersect their candidate sets to see whether the
            # identity of that letter can now be determined.
            actual_candidates = possible_letters.copy()

            for position in positions:
                index = position - 1

                if 0 <= index < self.word_length:
                    actual_candidates &= self.position_candidates[index]

            # Show candidates consistent with both the guess ciphertext
            # and Alice's reported hit positions.
            observation["possible_letters"] = actual_candidates.copy()

            for position in positions:
                index = position - 1

                if 0 <= index < self.word_length:
                    self.position_candidates[index] &= actual_candidates

            if len(actual_candidates) == 1:
                actual_letter = next(iter(actual_candidates))
                reported = set(positions)

                # Alice reports every occurrence of the letter.
                # Other positions cannot contain that letter.
                for index, candidates in enumerate(
                    self.position_candidates, start=1
                ):
                    if index not in reported:
                        candidates.discard(actual_letter)

        elif len(possible_letters) == 1:
            # Alice says the guess is absent. If Eve can identify
            # the exact letter, she can eliminate it everywhere.
            actual_letter = next(iter(possible_letters))

            for candidates in self.position_candidates:
                candidates.discard(actual_letter)

    def display(self):
        print("\n" + "=" * 44)
        print("                 EVE'S VIEW")
        print("=" * 44)

        print(f"\nSecret word length: {self.word_length}")

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
            letters = sorted(observation["possible_letters"])
            positions = observation["positions"]

            print(
                f"Guess #{observation['number']}: "
                f"{len(letters)} possibilities — "
                + (", ".join(letters) if letters else "(none)")
            )

            print(
                "  Alice's response: "
                + (
                    ", ".join(map(str, positions))
                    if positions
                    else "absent"
                )
            )

        print("\nPossible letters at each word position:")

        for index, candidates in enumerate(
            self.position_candidates, start=1
        ):
            if(self.partial_word[index-1]!="_"):
                letters = sorted(candidates)

                print(
                    f"Position {index}: "
                    + (", ".join(letters) if letters else "(none)")
                )

        print("\nYour notes:")

        if self.notes:
            for index, note in enumerate(self.notes, start=1):
                print(f"{index}. {note}")
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
                and all(letter in ALPHABET for letter in guess)
            ):
                return guess

            print(
                f"Please enter exactly {self.word_length} "
                "English letters."
            )
    
    def update_info(self, partial_word):
        self.partial_word = partial_word