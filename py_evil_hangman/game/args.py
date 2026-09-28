import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--dictionary-file", type=str, default="dictionary.txt", help="Path to the dictionary file."
    )
    parser.add_argument(
        "-g", "--guesses", type=int, default="10", help="How many guesses you get."
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose info (words left).")
    parser.add_argument("-k", "--karma", action="store_true", help="Run the WordGuesserAI (Karma)")

    return parser.parse_args()
