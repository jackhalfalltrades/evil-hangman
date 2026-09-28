from py_evil_hangman.word_maker import WordMakerAI
import pytest

# To test, you will probably find it easiest to make your own simplified dictionary.txt.

def test_get_letter_positions_in_word():
    wm = WordMakerAI("dictionary.txt")
    wm.reset(5)
    assert wm.get_letter_positions_in_word("hello", "l") == (2, 3)

def test_letters_remaining():
    wm = WordMakerAI("dictionary.txt")
    wm.reset(5)
    to_guess = "aeiou"
    for letter in list(to_guess):
        wm.guess(letter)
    assert wm.get_amount_of_valid_words() == 287

def test_blackbox():
    wm = WordMakerAI("dictionary.txt")
    wm.reset(6)
    to_guess = "asdfghjklzxcvbnmrpw"
    for letter in list(to_guess):
        wm.guess(letter)
    assert wm.get_valid_word() in ['petite', 'peyote', 'piquet', 'putout', 'puttee']
    assert sorted(wm.guess("e")) == [1, 5]
    assert wm.guess("t") == [4]
    assert wm.get_amount_of_valid_words() == 1
    assert wm.get_valid_word() == "peyote"
    
    # Do the same thing again to make sure that reset() works
    wm.reset(6)
    assert wm.get_amount_of_valid_words() != 1
    to_guess = "asdfghjklzxcvbnmrpwet"
    for letter in list(to_guess):
        wm.guess(letter)
    assert wm.get_amount_of_valid_words() == 1
    assert wm.get_valid_word() == "peyote"
