# import bb84
import string
from module import Cipher
# import wordgen
import random

MAX_ATTEMPTS = 5
EVE_DECODE_PROBABILITY = 0.25

ALPHABET = set(string.ascii_lowercase)

def display_word(hidden_word):
    # Display the letters Bob has discovered so far.
    print("\nWord: " + " ".join(hidden_word))

def get_bob_guess(guessed_letters):
    # Get a valid letter that Bob has not guessed yet
    while True:
        guess = input("\nGuess a letter: ").strip().lower()

        if len(guess) != 1 or guess not in ALPHABET:
            print("Please input a letter")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter")
            continue

        return guess

# def get_eve_guess(word_length):
#     # Get Eve's final word guess
#     while True:
#         guess = input(f"Eve, enter your final guess ({word_length} letters)").strip().lower()

#         if len(guess) != word_length or not guess.isalpha():
#             print(f"Please enter a word of exactly {word_length} letters")
#             continue

#         return guess

def get_eve_guess(word_length):
    while True:
        guess = input(
            f"\nEve, enter your final guess"
            f"({word_length} letters):"
        ).strip().lower()

        if (
            len(guess) != word_length
            or not guess.isalpha()
            or not guess.isascii()
        ):
            print(
                f"Please enter an English word"
                f"of exactly {word_length} letters."
            )
            continue
        return guess

def eve_intercepts(bob_guess):
    """
    Simplified interception

    Returns:
        transmitted guess (the letter alice receives)
        intercepted (if eve successfully decodes it or not)
    placeholder for actual quantum simulation
    """

    if random.random() >= EVE_DECODE_PROBABILITY:
        return bob_guess, False

    alternatives = [
        letter for letter in string.ascii_lowercase
        if letter != bob_guess
    ]

    transmitted_guess = random.choices(alternatives)
    return transmitted_guess, True

def reveal_letter(word, hidden_word, letter):
    # Reveal every occurence of a letter in the word
    found = False

    for index, actual_letter in enumerate(word):
        if actual_letter == letter:
            hidden_word[index] = letter
            found = True

    return found

def get_random_word():
    with open("words.txt", "r") as file:
        words = file.read().splitlines()
    return random.choice(words)

def play_round():
    word = get_random_word().strip().lower()

    hidden_word = ["_"] * len(word)

    bob_guessed_letters = set()
    eve_observations = []

    attempts = MAX_ATTEMPTS

    print("\nQUANTUM HANGMAN")
    print(f"Word length: {len(word)}")
    display_word(hidden_word)
    print(f"Wrong guesses remaining: {attempts}")

    # Bob plays until he solves the word or runs out of attempts
    while attempts > 0 and "_" in hidden_word:
        bob_guess = get_bob_guess(bob_guessed_letters)
        bob_guessed_letters.add(bob_guess)

        # Eve intercepts bobs message
        transmitted_guess, intercepted = eve_intercepts(bob_guess)

        if intercepted:
            print("eve successfully intercepted the message")
            print("the transmitted letter may have been altered")
        else:
            print("eve failed to decode bobs letter")

        correct = reveal_letter(
            word,
            hidden_word,
            transmitted_guess
        )

        # Store info for eves interface
        # In the full game these should be restricted to what eve actually sees
        eve_observations.append({
            "intercepted": intercepted,
            "transmitted_letter": transmitted_guess,
            "result": correct,
        })

        if correct:
            print("alice reports a correct letter")
        else:
            print("alice reports an incorrect letter")
            attempts -= 1

        display_word(hidden_word)
        print(f"wrong guesses remaining: {attempts}")

    #bob loses if the word is unsolved
    if "_" in hidden_word:
        print("\nBob ran out of attempts")
        print(f"Alices word was: {word}")
        print("Eve wins!")
        return "eve"

    # bob solved the word
    print("\nBob solved the word")
    print("Eve gets one final guess")

    eve_guess = get_eve_guess(len(word))

    if eve_guess == word:
        print("Eve guessed the word correctly!")
        print("Eve wins!")
        return "eve"

    print("Eve's guess was incorrect.")
    print(f"Alice's word was: {word}")
    print("Bob wins")
    return "bob"


# def play_round():
#     word = wordgen.get_random_word().strip().lower()

#     hidden_word = ["_"] * len(word)

#     # Game state
#     bob_guessed_letters = set()
#     attempts = MAX_ATTEMPTS

#     print("\nQUANTUM HANGMAN")
#     print(f"Word length: {len(word)}")
#     display_word(hidden_word)
#     print(f"Bob has {attempts} guesses remaining")

#     # Game loop
#     while attempts > 0 and "_" in hidden_word:
#         bob_guess = get_bob_guess(bob_guessed_letters)
#         bob_guessed_letters.add(bob_guess)

#         # TODO QUANTUM:
#         # 1. Encode bob_guess
#         # 2. Generate bob basis
#         # 3. Simulate Eve intercepting transmission
#         # 4. Determine whether Eve deciphers guess correctly
#         # 5. If Eve can alter guess, resolve here
#         # 6. Update eves partial cipher and info

#         # for now the game uses bobs guess
#         transmitted_guess = bob_guess

#         # check the guess
#         if transmitted_guess in word:
#             print("Correct")
#             for i, letter in enumerate(word):
#                 if letter == transmitted_guess:
#                     hidden_word[i] = letter

#         else:
#             print("Wrong")
#             attempts -= 1

#         # TODO QUANTUM:
#         # send the guess outcome and update game state to Eve
#         # Update Eves display and partial cipher

#         display_word(hidden_word)
#         print(f"Wrong guesses remaining: {attempts}")

#     # Bob runs out of attempts
#     if "_" in hidden_word:
#         print("\nBob ran out of attempts")
#         print(f"Alice's word was: {word}")
#         print("Eve wins")
#         return "eve"

#     # Bob solevs the word
#     print("\nBob solved the hangman")
#     print(f"The word was: {word}")

#     # TODO QUANTUM:
#     # Give Eve access to her partial cipher
#     # Allow her final guess

#     eve_guess = get_eve_guess(len(word))

#     if eve_guess == word:
#         print("Eve guessed correctly")
#         print("Eve wins")
#         return "eve"

#     print("Eve couldn't guess correctly")
#     print("Bob wins")
#     return "bob"

def main():
    bob_wins = 0
    eve_wins = 0

    while True:
        winner = play_round()

        if winner == "bob":
            bob_wins += 1
        else:
            eve_wins += 1

        print("\nSCORE")
        print(f"Bob: {bob_wins}")
        print(f"Eve: {eve_wins}")

        play_again = input("Play again? (y/n): ")
        if play_again.strip().lower() != "y":
            break

    print("\nThanks for playing")

if __name__ == "__main__":
    main()

from html import window

def host():
    pass

def join():
    pass

    #MAIN MENU
        #host or join
        #if host
            #select to play as bob or eve
        #if join
            #connect to first available socket
            #play as whoever is available (bob or eve)
    #GAME
        #generate word
        #generate cipher
        #send cipher to bob
        #send partial cipher to eve
        #if bob
            #show hangman
            #show keyboard
            #gray out guessed letters
            #show underscores/guessed letters
            #send each guess
        #if eve
            #show bobs encoded guesses
            #show underscores and encoded partial word
            #show partial information
    #END
        #if bob ran out of guesses
            #bob loses
            #eve wins
        #if bob guessed correctly
            #eve submits one final guess
                #if eves guess is correct
                    #bob loses
                    #eve wins
                #else
                    #bob wins
                    #eve loses
        #play again?
