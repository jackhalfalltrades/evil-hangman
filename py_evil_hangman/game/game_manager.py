from py_evil_hangman.word_maker import WordMakerAI, WordMakerHuman
from py_evil_hangman.word_guesser import WordGuesserAI, WordGuesserHuman

HUMAN_MIN_WORD_LEN = 2
HUMAN_MAX_WORD_LEN = 20

class GameManager():
    def __init__(self, ai, words_file, guesses, verbose, karma_mode):
        self.starting = guesses
        if ai:
            self.word_maker = WordMakerAI(words_file, verbose)
        else:
            self.word_maker = WordMakerHuman(words_file, verbose)
        if karma_mode:
            self.word_guesser = WordGuesserAI(guesses, words_file, verbose)
        else:
            self.word_guesser = WordGuesserHuman(guesses, words_file, verbose)
        self.ai = ai
        self.verbose = verbose

    def control_loop(self):
        while True:
            print("Let's play hangman!")
            while True:
                numS = input(f"How many characters should my word be? ({HUMAN_MIN_WORD_LEN}-{HUMAN_MAX_WORD_LEN}): ")
                try:
                    num = int(numS)
                    if num >= HUMAN_MIN_WORD_LEN and num <= HUMAN_MAX_WORD_LEN: break
                except:
                    pass
            self.run_game(num)
            ans = input("Would you like to play again? (y/n):")
            while ans not in ["y", "n"]:
                ans = input("Would you like to play again? (y/n):")
            if ans == "n": break

    def run_game(self, word_length):
        self.word_maker.reset(word_length)
        self.word_guesser.reset(word_length)

        while True:
            if self.word_guesser.state.guesses == 0:
                print(f"You lose! The word was {self.word_maker.get_valid_word()}.")
                break
            self.word_guesser.state.print_state(self.word_maker.get_amount_of_valid_words())
            inp = self.word_guesser.get_guess()
            letter_positions = self.word_maker.guess(inp)
            letter_count = len(letter_positions)
            s = "s" if letter_count != 1 else ""
            print(f"Found {letter_count} '{inp}'{s}")

            self.word_guesser.state.guesses -= 1 if letter_count == 0 else 0
            self.word_guesser.state.guessed.append(inp)
            for i in letter_positions:
                self.word_guesser.state.word[i] = inp

            self.word_guesser.state.done_letters += letter_count
            if self.word_guesser.state.done_letters == word_length:
                left = self.starting - self.word_guesser.state.guesses
                es = "es" if left != 1 else ""
                print(f"You win in {left} incorrect guess{es}!")
                print("The word was {}".format("".join(self.word_guesser.state.word)))
                break
