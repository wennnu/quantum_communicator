import random

def get_random_word():
    with open("words.txt", "r") as file:
        words = file.read().splitlines()
    return random.choice(words)