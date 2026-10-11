import random
import string
from pathlib import Path

from temp_cipher import RoundCipher
from eve import Eve

MAX_ATTEMPTS = 5
EVE_KNOWLEDGE = 0.40
EVE_INTERCEPT_PROBABILITY = 0
ALPHABET = set(string.ascii_lowercase)

WORD_FILE = Path(__file__).with_name("words.txt")


def load_words():
    if not WORD_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {WORD_FILE}. "
            "Place words.txt beside game.py."
        )

    with WORD_FILE.open(encoding="utf-8") as file:
        words = {
            line.strip().lower()
            for line in file
            if line.strip().isalpha() and line.strip().isascii()
        }

    if not words:
        raise ValueError("words.txt contains no valid words.")

    return sorted(words)


def clear_screen():
    print("\033[2J\033[H", end="", flush=True)


def display_word(pattern):
    print("Word: " + " ".join(pattern))


def get_bob_guess(guessed_letters):
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
    print("=" * 38)
    print("             BOB'S VIEW")
    print("=" * 38)
    display_word(pattern)

    print(
        "\nGuessed letters: "
        + (", ".join(sorted(guessed_letters)) or "(none)")
    )
    print(f"Wrong guesses remaining: {attempts}")


def play_round(words):
    word = random.choice(words)

    # Alice's word and Bob's guesses use disjoint key segments.
    cipher = RoundCipher(
        word_length=len(word),
        eve_knowledge=EVE_KNOWLEDGE,
        intercept_probability=EVE_INTERCEPT_PROBABILITY,
    )

    # Eve sees the encrypted word, not the plaintext word.
    encrypted_word = cipher.encrypt_word(word)
    position_candidates = cipher.get_word_candidates(encrypted_word)

    eve = Eve(position_candidates, words, cipher)

    pattern = ["_"] * len(word)
    guessed_letters = set()
    attempts = MAX_ATTEMPTS

    print("\nBB84 session established.")
    print(f"Sampled quantum bit error rate: {cipher.qber:.1%}")
    print(
        "A fresh five-bit key segment will be used for each guess."
    )
    input("\nPress Enter to begin Hangman...")

    while attempts > 0 and "_" in pattern:
        clear_screen()
        display_bob_screen(pattern, guessed_letters, attempts)

        guess = get_bob_guess(guessed_letters)
        guessed_letters.add(guess)

        # Bob encrypts his guess. Eve only receives the ciphertext.
        ciphertext = cipher.encode_letter(guess)

        # Eve gets a chance to learn this guess's key block.
        eve_learned = cipher.try_learn_current_key_bits(
            EVE_INTERCEPT_PROBABILITY
        )

        if eve_learned:
            print("\nEve successfully learned the current key block!")
        else:
            print("\nEve failed to learn the current key block.")

        possible_letters = cipher.get_possible_letters(ciphertext)

        # Alice decrypts the guess and checks her secret word.
        received_letter = cipher.decode_letter(ciphertext)

        positions = [
            index
            for index, letter in enumerate(word, start=1)
            if letter == received_letter
        ]

        if positions:
            for position in positions:
                pattern[position - 1] = received_letter

            print("\nAlice confirms the letter is present at position(s): "                
                + ", ".join(map(str, positions))
                + "."
            )

        else:
            attempts -= 1
            print("\nAlice confirms the letter is absent.")

        # Eve receives the ciphertext's candidate letters and
        # Alice's public response, but not Bob's plaintext guess.
        eve.observe(possible_letters, positions)

        clear_screen()
        eve.update_info(pattern)
        eve.display()

        if positions:
            print(
                "\nAlice confirmed position(s): "
                + ", ".join(map(str, positions))
                + "."
            )
        else:
            print("\nAlice confirmed: letter absent.")

        print(f"Bob has {attempts} wrong guesses remaining.")
        eve.add_note()

        input("\nPress Enter to pass the turn back to Bob...")

    clear_screen()

    if "_" in pattern:
        print("Bob ran out of attempts!")
        print(f"Alice's word was: {word}")
        print("Eve wins!")
        return "eve"

    print("Bob solved Hangman!")
    print("Eve gets one final guess.")

    eve.update_info(pattern)
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
        try:
            winner = play_round(words)
        except RuntimeError as error:
            print(f"\nCould not establish a usable BB84 session: {error}")
            print("This round could not be played.")

            again = input("\nTry again? (y/n): ").strip().lower()
            if again == "y":
                continue
            break

        scores[winner] += 1

        print("\n" + "=" * 24)
        print("         SCORE")
        print("=" * 24)
        print(f"Bob: {scores['bob']}")
        print(f"Eve: {scores['eve']}")

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            break
        clear_screen()

    print("\nThanks for playing Quantum Hangman!")