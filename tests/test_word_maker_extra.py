import pytest
from py_evil_hangman.word_maker import WordMakerAI

HANDOUT_WORDS = ["ally", "beta", "cool", "deal", "else", "flew", "good", "hope", "ibex"]


@pytest.fixture
def small_dict(tmp_path):
    def make(words):
        path = tmp_path / "words.txt"
        path.write_text("\n".join(words) + "\n")
        return str(path)
    return make


def test_handout_example(small_dict):
    wm = WordMakerAI(small_dict(HANDOUT_WORDS))
    wm.reset(4)
    assert wm.get_amount_of_valid_words() == 9
    assert wm.guess("e") == []          # ---- (3 words) beats every other family
    assert wm.get_amount_of_valid_words() == 3
    assert wm.guess("o") == [1, 2]       # -OO- (cool, good) beats ---- (ally)
    assert wm.get_amount_of_valid_words() == 2
    assert wm.get_valid_word() in ("cool", "good")


def test_tie_prefers_fewer_letters(small_dict):
    wm = WordMakerAI(small_dict(["ah", "hi"]))
    wm.reset(2)
    assert wm.guess("a") == []
    assert wm.get_valid_word() == "hi"


def test_tie_equal_letter_count_either(small_dict):
    wm = WordMakerAI(small_dict(["aha", "haa"]))
    wm.reset(3)
    assert wm.guess("a") in ([0, 2], [1, 2])
    assert wm.get_amount_of_valid_words() == 1


def test_docstring_example(small_dict):
    wm = WordMakerAI(small_dict(["ah", "ai", "bo"]))
    wm.reset(2)
    assert wm.guess("a") == [0]
    assert wm.get_amount_of_valid_words() == 2


def test_position_matters_not_just_count(small_dict):
    wm = WordMakerAI(small_dict(["beer", "here", "deer"]))
    wm.reset(4)
    assert wm.guess("e") == [1, 2]
    assert wm.get_amount_of_valid_words() == 2


def test_missing_length_and_long_words(small_dict):
    long_word = "a" * 500 + "b"
    wm = WordMakerAI(small_dict(["cat", long_word]))
    wm.reset(7)
    assert wm.get_amount_of_valid_words() == 0
    assert wm.guess("a") == []
    wm.reset(501)
    assert wm.guess("b") == [500]
    assert wm.get_valid_word() == long_word


def test_reset_restores_full_bucket(small_dict):
    wm = WordMakerAI(small_dict(HANDOUT_WORDS))
    wm.reset(4)
    wm.guess("e")
    wm.guess("o")
    wm.reset(4)
    assert wm.get_amount_of_valid_words() == 9


def test_letter_positions():
    wm = WordMakerAI.__new__(WordMakerAI)
    assert wm.get_letter_positions_in_word("banana", "a") == (1, 3, 5)
    assert wm.get_letter_positions_in_word("banana", "z") == ()
