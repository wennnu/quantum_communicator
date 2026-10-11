import random
import string

from pathlib import Path

from temp_cipher import RoundCipher
from eve import Eve


MAX_ATTEMPTS = 5
EVE_KNOWLEDGE = 0.25
ALPHABET = set(string.ascii_lowercase)

WORD_FILE = Path(__file__).with_name("words.txt")


def load_words():
    """Read the word bank from words.txt."""
    if not WORD_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {WORD_FILE}. "
            "Place words.txt beside game.py."
        )

    with WORD_FILE.open(encoding="utf-8") as file:
        words = {
            line.strip().lower()
            for line in file
            if line.strip().isalpha()
            and line.strip().isascii()
        }

    if not words:
        raise ValueError("words.txt contains no valid words.")

    return sorted(words)


def clear_screen():
    """Clear a typical terminal before changing player views."""
    print("\033[2J\033[H", end="", flush=True)


def display_word(pattern):
    print("Word: " + " ".join(pattern))


def get_bob_guess(guessed_letters):
    """Ask Bob for a valid, previously unguessed letter."""
    while True:
        guess = input("\nBob, guess a letter: ").strip().lower()

        if len(guess) != 1 or guess not in ALPHABET:
            print("Please enter one English letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        return guess


def display_bob_screen(pattern, guessed_letters, attempts):
    """Display the actual Hangman board to Bob."""
    print("=" * 38)
    print("             BOB'S VIEW")
    print("=" * 38)

    display_word(pattern)

    print(
        "\nGuessed letters: "
        + (
            ", ".join(sorted(guessed_letters))
            if guessed_letters else "(none)"
        )
    )

    print(f"Wrong guesses remaining: {attempts}")


def play_round(words):
    # Alice chooses the secret word and creates a fresh cipher.
    word = random.choice(words)
    cipher = RoundCipher(EVE_KNOWLEDGE)
    print(word) # TEMP

    position_candidates = cipher.get_word_candidates(word)
    eve = Eve(position_candidates, words)

    # Only Bob receives the actual Hangman board.
    pattern = ["_"] * len(word)
    guessed_letters = set()
    attempts = MAX_ATTEMPTS

    while attempts > 0 and "_" in pattern:
        clear_screen()

        display_bob_screen(
            pattern,
            guessed_letters,
            attempts,
        )

        # 1. Bob chooses a plaintext letter.
        guess = get_bob_guess(guessed_letters)
        guessed_letters.add(guess)

        # 2. Bob encrypts his guess.
        encoded_guess = cipher.encode_letter(guess)

        # 3. Eve sees only the possible plaintext letters.
        #    The encoded bits and actual guess stay hidden.
        possible_letters = cipher.get_possible_letters(
            encoded_guess
        )

        # 4. Alice decodes Bob's message.
        #
        # This simulation uses the original guess as the
        # decoded letter because encoding/decoding is exact.
        # If RoundCipher exposes a decode method, call it here.
        received_letter = cipher.decode_letter(encoded_guess)

        # 5. Alice checks the letter against her secret word.
        #    Positions are numbered starting at 1.
        positions = [
            index
            for index, letter in enumerate(word, start=1)
            if letter == received_letter
        ]

        # 6. Bob receives the actual Hangman result.
        if positions:
            for position in positions:
                pattern[position - 1] = received_letter

            correct = True
        else:
            attempts -= 1
            correct = False

        # 7. Eve receives only the candidate letters and
        #    Alice's response. Never pass her the actual guess
        #    or Bob's Hangman pattern.
        eve.observe(possible_letters, positions)

        # 8. Display Eve's independent deductions.
        clear_screen()
        eve.display()

        if positions:
            print(
                "\nAlice confirmed that the encrypted "
                "guess occurs at position(s): "
                + ", ".join(map(str, positions))
                + "."
            )
        else:
            print("\nAlice confirmed that the letter is absent.")

        print(f"Bob has {attempts} wrong guesses remaining.")

        eve.add_note()

        input("\nPress Enter to pass the turn back to Bob...")

    clear_screen()

    # Determine the winner of the Hangman phase.
    if "_" in pattern:
        print("Bob ran out of attempts!")
        print(f"Alice's word was: {word}")
        print("Eve wins!")
        return "eve"

    print("Bob solved Hangman!")
    print("Eve gets one final guess.")

    # Eve makes her guess using her observations and notes.
    eve.display()
    eve_guess = eve.final_guess()

    if eve_guess == word:
        print("\nEve guessed correctly. Eve wins!")
        return "eve"

    print(f"\nEve guessed incorrectly. The word was {word}.")
    print("Bob wins!")
    return "bob"


def main():
    words = load_words()
    scores = {"bob": 0, "eve": 0}

    print(f"Loaded {len(words)} words from words.txt.")

    while True:
        winner = play_round(words)
        scores[winner] += 1

        print("\n" + "=" * 24)
        print("         SCORE")
        print("=" * 24)
        print(f"Bob: {scores['bob']}")
        print(f"Eve: {scores['eve']}")

        again = input("\nPlay again? (y/n): ").strip().lower()

        if again != "y":
            break

    print("\nThanks for playing Quantum Hangman!")


# if __name__ == "__main__":
#     main()