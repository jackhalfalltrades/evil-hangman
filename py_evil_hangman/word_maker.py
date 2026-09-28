from __future__ import annotations
from collections import defaultdict # You might find this useful
import os

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

class WordMakerHuman():
    def __init__(self, words_file, verbose):
        # we need to prompt the player for a word, then clear the screen so that player 2 doesn't see the word.
        self.verbose = verbose
        self.words = {} # Make sure that you understand dictionaries. They will be extremely useful for this project.
        with open(words_file) as wordfile:
            for line in wordfile:
                word = line.strip()
                if len(word) > 0:
                    self.words[word] = True # I could have made this a set() instead.

    def reset(self, word_length):
        # Your AI code should not call input() or print().
        question = ""
        while True:
            question = input(f"Please type in your word of length {word_length}: ")
            if question in self.words and len(question) == word_length:
                break
            print("Invalid word.")
        if not self.verbose:
            print("\n" * 100) # Clear the screen
        self.word = question

    def get_valid_word(self):
        return self.word

    def get_amount_of_valid_words(self):
        return 1 # the only possible word is self.word

    def guess(self, guess_letter):
        idx = self.word.find(guess_letter)
        ret = []
        while idx != -1:
            ret.append(idx)
            idx = self.word.find(guess_letter, idx + 1)
        return ret




class WordMakerAI():
    """
    A new WordMakerAI is instantiated every time you launch the game with evil_hangman.py.
    (However, the test harness can make multiple instances.)
    Between games, the reset() function is called. This should clear any internal gamestate that you have.
    The number of guesses, input gathering, winning, losing, etc. is all managed by the GameManager, so you don't
     have to prompt the user at all. All you need to do is keep track of the active dictionary of still-valid words
     in this game.

    Do not assume anything about the lengths of the words. You will be tested on dictionaries with extremely long words.
    """
    def __init__(self, words_file: str, verbose=False):
        # This initializer should read in the words into any data structures you see fit
        # The input format is a file of words separated by newlines
        # Use open() to open the file, and remember to split up words by word length!

        # Feel free to use this parameter to toggle extra print statments. Verbose mode can be turned on via the --verbose flag.
        self.verbose = verbose

        # Use this code if you like.
        """
        with open(words_file) as file_obj:
            for line in file_obj:
                word = line.strip()
                # Use word
        """

        # Preprocess: bucket every word by its length so reset() is O(1).
        self.words_by_length: dict[int, list[str]] = defaultdict(list)
        seen = set()
        with open(words_file) as file_obj:
            for line in file_obj:
                word = line.strip()
                if word and word not in seen:
                    seen.add(word)
                    self.words_by_length[len(word)].append(word)

        self.word_length = 0
        self.valid_words: list[str] = []

    def reset(self, word_length: int) -> None:
        # This function starts a new game with a word length of `word_length`. This will always be called before guess() or get_valid_word() are called.
        # You should try to make this function should be O(1). That is, you shouldn't have to process over the entire dictionary here (find somewhere else to preprocess it)
        # Your AI code should not call input() or print().

        # O(1): just point at the preprocessed bucket. guess() never mutates this
        # list in place (it builds new family lists), so the bucket stays intact.
        self.word_length = word_length
        self.valid_words = self.words_by_length.get(word_length, [])

    def get_valid_word(self) -> str:
        # Get a valid word in the active dictionary, to return when you lose
        # Can return any word, as long as it satisfies the previous guesses

        return self.valid_words[0] if self.valid_words else ""

    def get_amount_of_valid_words(self) -> int:
        # This function gets the total amount of possible words "remaining" (i.e., that satisfy all the guesses since self.reset was last called)
        # This should also be O(1)
        # Note: This is used extensively in the autograder! Be sure to verify that this function works
        # via the provided test cases.
        # You can see this number by running with the verbose flag, i.e. `python3 evil_hangman.py --verbose`

        return len(self.valid_words)

    def get_letter_positions_in_word(self, word: str, guess_letter: str) -> tuple[int, ...]:
        # This function should return the positions of guess_letter in word. For instance:
        #  get_letter_positions_in_word("hello", "l") should return (2, 3). The list should
        #  be sorted ascending and 0-indexed.
        # You can assume that word is lowercase with at least length 1 and guess_letter has exactly length 1 and is a lowercase a-z letter.

        # Note: to convert from a list to a tuple, call tuple() on the list. For instance:
        result = [i for i, ch in enumerate(word) if ch == guess_letter]
        return tuple(result)
        

    def guess(self, guess_letter) -> list[int]:
        # This is the meat of the project. This function is called by the GameManager.
        # Using get_letter_positions_in_word, this function should sort all remaining words
        #  into their respective letter families. Then, it should pick the largest family,
        #  resolving ties by picking the set with fewer guess_letters. If the amount of
        #  guess_letter's are equal, then either set can be picked to become the new active
        #  dictionary.
        # This function should return the positions of where a guess_letter should appear.
        # For instance, if you want an "e" to appear in positions 0 and 2, return [0, 2].
        # Make sure the list is sorted.

        # Here is an example run of guess():
        #  If the guess is "a" and the words left are ["ah", "ai", "bo"], then we should return [0], because
        #  we are picking the family of words with an "a" in the 0th position. If this function decides that the biggest family
        #  has no a's, then we would have returned [].

        # In the case of a tie (multiple families have the same amount of words), we should pick the set of words with fewer guess_letter's.
        #  That is, if the guess is "a" and the words left are ["ah", "hi"], we should return [] (picking the set ["hi"]), 
        #  since ["hi"] and ["ah"] are equal length and "hi" has fewer a's than "ah".
        # Again, if both sets have an equal number of guess_letter's, then it is ok to pick either.
        #  For example, if the guess is "a" and the words left are ["aha", "haa"], you can return either [0, 2] or [1, 2].

        # The order of the returned list should be sorted. You can assume that 'guess_letter' has not been seen yet since the last call to self.reset(),
        #  and that guess_letter has len of 1 and is a lowercase a-z letter.
        
        # Partition the remaining words into families keyed by the positions of guess_letter.
        # Only families that actually occur are created (no 2^n enumeration).
        families: dict[tuple[int, ...], list[str]] = defaultdict(list)
        for word in self.valid_words:
            families[self.get_letter_positions_in_word(word, guess_letter)].append(word)

        if not families:
            return []

        # Largest family wins; ties go to the family revealing the fewest letters
        # (so the empty family () is preferred whenever it is tied for largest).
        best_key = max(families, key=lambda key: (len(families[key]), -len(key)))
        self.valid_words = families[best_key]
        return list(best_key)
