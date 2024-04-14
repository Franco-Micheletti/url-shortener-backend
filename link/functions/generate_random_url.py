"""
Generate random url module
"""
import string
import random


def generate_random_url(total_chars):
    """
    Function to generate a short url with random characters.
    """
    if not isinstance(total_chars, int):
        return "The total chars must a integer"
    if total_chars <= 0:
        return "The total chars can't be cero or a negative value"
    if total_chars > 10:
        return "The total chars can't be higher than 10"

    random_url = ""
    letters = list(string.ascii_letters)
    numbers = list(range(0, 9))
    all_chars = letters + numbers

    for x in range(total_chars):
        ran_choice = str(random.choice(all_chars))
        random_url += ran_choice

    return random_url
