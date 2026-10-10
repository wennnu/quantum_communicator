import wordgen

attempts = 5

word = wordgen.get_random_word()
hidden_word = ["_"] * len(word)
guessed_letters = []

while (attempts > 0 and "_" in hidden_word):
    print("\nWord: ", " ".join(hidden_word))
    print("Attempts Remaining: ", attempts)
    print("Guessed Letters:", ", ".join(guessed_letters))

    guess = input("Guess a letter: ").lower()

    if guess in guessed_letters:
        print("You already guessed that")
        continue

    guessed_letters.append(guess)

    if guess in word:
        print("Correct")
        for i in range(len(word)):
            if word[i] == guess:
                hidden_word[i] = guess
    else:
        print("Wrong")
        attempts -= 1

if "_" not in hidden_word:
    print("You win! The word was: ", word)
else:
    print("You lose! The word was: ", word)