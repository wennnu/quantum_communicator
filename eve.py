import string


class Eve:
    def __init__(self, position_candidates, words):
        """
        position_candidates:
            A list of sets, one per secret-word position.
            Each set contains the letters consistent with
            Eve's initial partial knowledge of that position.

        words:
            The dictionary Eve is allowed to use.
        """
        self.word_length = len(position_candidates)

        self.initial_position_candidates = [
            set(letters) & set(string.ascii_lowercase)
            for letters in position_candidates
        ]

        self.position_candidates = [
            letters.copy()
            for letters in self.initial_position_candidates
        ]

        self.observations = []
        self.notes = []

        # Keep only dictionary words consistent with Eve's
        # initial knowledge of every encrypted character.
        self.candidates = {
            word.lower()
            for word in words
            if len(word) == self.word_length
            and all(
                word[i].lower() in self.position_candidates[i]
                for i in range(self.word_length)
            )
        }

        self._refresh_position_candidates()

    def _refresh_position_candidates(self):
        """Derive possible letters from surviving candidate words."""
        if not self.candidates:
            self.position_candidates = [
                set() for _ in range(self.word_length)
            ]
            return

        self.position_candidates = [
            {word[i] for word in self.candidates}
            for i in range(self.word_length)
        ]

    @staticmethod
    def _matches_feedback(word, possible_letters, positions):
        """
        Check whether at least one possible plaintext letter
        could explain Alice's observed response.

        Positions are numbered starting at 1.
        """
        reported_positions = set(positions)

        for letter in possible_letters:
            actual_positions = {
                i
                for i, character in enumerate(word, start=1)
                if character == letter
            }

            if actual_positions == reported_positions:
                return True

        return False

    def observe(self, possible_letters, positions):
        """
        Record the ciphertext candidates and Alice's feedback.
        Never receives Bob's actual plaintext guess.
        """
        possible_letters = set(possible_letters)
        positions = sorted(positions)

        self.observations.append({
            "number": len(self.observations) + 1,
            "possible_letters": possible_letters,
            "positions": positions,
        })

        # A word survives if at least one candidate plaintext
        # letter could have produced Alice's exact response.
        self.candidates = {
            word
            for word in self.candidates
            if self._matches_feedback(
                word,
                possible_letters,
                positions,
            )
        }

        self._refresh_position_candidates()

    def display(self):
        print("\n" + "=" * 44)
        print("                 EVE'S VIEW")
        print("=" * 44)

        print(f"\nSecret word length: {self.word_length}")
        print(f"Remaining candidate words: {len(self.candidates)}")

        if self.observations:
            latest = self.observations[-1]

            print(f"\nLatest observation: #{latest['number']}")
            print(
                "Possible plaintext letters: "
                + (
                    ", ".join(sorted(latest["possible_letters"]))
                    or "(none)"
                )
            )

            if latest["positions"]:
                print(
                    "Alice reported positions: "
                    + ", ".join(map(str, latest["positions"]))
                )
            else:
                print("Alice reported: letter absent")

        print("\nPossible letters at each position:")

        for i, letters in enumerate(
            self.position_candidates, start=1
        ):
            print(
                f"Position {i}: "
                + (", ".join(sorted(letters)) or "(none)")
            )

        print("\nObservation history:")

        for observation in self.observations:
            possible = ", ".join(
                sorted(observation["possible_letters"])
            ) or "(none)"

            positions = (
                ", ".join(map(str, observation["positions"]))
                or "absent"
            )

            print(
                f"#{observation['number']}: "
                f"candidates [{possible}], "
                f"Alice's response: {positions}"
            )

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
                and all(c in string.ascii_lowercase for c in guess)
            ):
                return guess

            print(
                f"Please enter exactly {self.word_length} "
                "English letters."
            )