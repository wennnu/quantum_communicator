import string

ALPHABET = string.ascii_lowercase
LENGTH = 5


def letter_to_bits(letter):
    """Convert a letter a-z to its five-bit index."""
    letter = letter.lower()

    if letter not in ALPHABET:
        raise ValueError("Expected one English letter.")

    return format(ALPHABET.index(letter), "05b")


def bits_to_letter(bits):
    """Convert a five-bit value back to a letter."""
    if len(bits) != LENGTH or any(b not in "01" for b in bits):
        raise ValueError("Expected exactly five binary digits.")

    index = int(bits, 2)

    if index >= len(ALPHABET):
        raise ValueError("Invalid letter encoding.")

    return ALPHABET[index]


def xor_bits(left, right):
    """XOR two equal-length binary strings."""
    if len(left) != len(right):
        raise ValueError("Bit strings must have equal length.")

    return "".join(
        "1" if a != b else "0"
        for a, b in zip(left, right)
    )