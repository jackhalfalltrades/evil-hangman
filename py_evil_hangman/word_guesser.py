from collections import defaultdict

class GameState():
    def __init__(self, guesses, word_length, verbose):
        self.word_length = word_length
        self.guessed = []
        self.guesses = guesses # starting number of guesses
        self.done_letters = 0
        self.word = ["-"] * word_length
        self.verbose = verbose
    def print_state(self, wordsRemaining):
        wrStr = "" if not self.verbose else f" ({wordsRemaining} words remain)"
        print(f"\nYou have {self.guesses} incorrect guesses left{wrStr}.")
        print("Used letters: {}".format(" ".join(self.guessed)))
        print("Word: {}".format("".join(self.word)))


# an abstract class defining the word guesser interface
class WordGuesser():
    def __init__(self, guesses, words_file, verbose):
        self.verbose = verbose
        self.guesses = guesses
    def reset(self, word_length):
        self.state = GameState(self.guesses, word_length, self.verbose)
    def get_guess(self):
        # return the next best guess
        # use self.gamestate to inquire about the current status of the game
        raise NotImplementedError # Subclasses should override this method

class WordGuesserHuman(WordGuesser):
    def get_guess(self):
            while True:
                inp = input("Enter guess: ").lower()
                if len(inp) != 1 or inp in self.state.guessed or not inp.isalpha():
                    print("Invalid guess.")
                else:
                    break
            return inp
 
# NOT REQUIRED! This is only for Karma.
class WordGuesserAI():
    """
    A minimax "reflex" guesser. It keeps every dictionary word bucketed by length, and on each
    turn rebuilds the candidate set purely from the visible GameState (revealed pattern + used
    letters). It then assumes the word-maker is adversarial (as WordMakerAI is) and picks the
    letter whose *worst-case* family is smallest, i.e. the letter that best splits the space.
    """
    FALLBACK_ORDER = "etaoinshrdlcumwfgypbvkjxqz"

    def __init__(self, guesses, words_file, verbose):
        self.verbose = verbose
        self.guesses = guesses
        self.words_by_length = defaultdict(list)
        seen = set()
        with open(words_file) as wordfile:
            for line in wordfile:
                word = line.strip().lower()
                if word and word.isalpha() and word not in seen:
                    seen.add(word)
                    self.words_by_length[len(word)].append(word)

    def reset(self, word_length):
        self.state = GameState(self.guesses, word_length, self.verbose)

    def _candidates(self):
        guessed = set(self.state.guessed)
        pattern = self.state.word
        result = []
        for word in self.words_by_length.get(self.state.word_length, []):
            for ch, shown in zip(word, pattern):
                if shown == "-":
                    if ch in guessed:  # a guessed letter would already have been revealed here
                        break
                elif ch != shown:
                    break
            else:
                result.append(word)
        return result

    def get_guess(self):
        guessed = set(self.state.guessed)
        candidates = self._candidates()
        unguessed = [c for c in self.FALLBACK_ORDER if c not in guessed]

        if not candidates:
            return unguessed[0]

        best_letter, best_score = None, None
        for letter in unguessed:
            families = defaultdict(int)
            hits = 0
            for word in candidates:
                key = tuple(i for i, ch in enumerate(word) if ch == letter)
                families[key] += 1
                if key:
                    hits += 1
            if hits == 0:
                continue  # guaranteed miss, never useful
            worst = max(families.values())
            # Prefer small worst-case family; if the worst case is a miss, that's costlier.
            miss_is_worst = families.get((), 0) == worst
            score = (worst, miss_is_worst, -hits)
            if best_score is None or score < best_score:
                best_letter, best_score = letter, score

        if best_letter is None:  # only possible if every remaining letter misses everything
            return unguessed[0]
        if self.verbose:
            print(f"[AI] {len(candidates)} candidates; guessing '{best_letter}'")
        return best_letter
