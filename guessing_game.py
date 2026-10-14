"""A small, dependency-free number guessing game for the terminal."""

import random
from collections.abc import Callable


DIFFICULTIES = {
    "1": ("Easy", 10),
    "2": ("Medium", 7),
    "3": ("Hard", 5),
}


def choose_difficulty(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[..., None] = print,
) -> tuple[str, int]:
    """Prompt until the player selects a difficulty."""
    while True:
        print_fn("\nChoose a difficulty:")
        for key, (name, attempts) in DIFFICULTIES.items():
            print_fn(f"  {key}. {name} ({attempts} attempts)")
        choice = input_fn("> ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print_fn("Please enter 1, 2, or 3.")


def play_round(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[..., None] = print,
    rng: random.Random | None = None,
) -> bool:
    """Play one round. Return True if the player guesses correctly."""
    if rng is None:
        rng = random

    difficulty, max_attempts = choose_difficulty(input_fn, print_fn)
    answer = rng.randint(1, 100)
    print_fn(f"\n{difficulty}: I'm thinking of a number from 1 to 100.")
    print_fn(f"You have {max_attempts} guesses.")

    for attempt in range(1, max_attempts + 1):
        while True:
            raw_guess = input_fn(f"Guess {attempt}/{max_attempts}: ").strip()
            try:
                guess = int(raw_guess)
            except ValueError:
                print_fn("Enter a whole number from 1 to 100.")
                continue
            if 1 <= guess <= 100:
                break
            print_fn("Your guess must be between 1 and 100.")

        if guess == answer:
            print_fn(f"Correct! You got it in {attempt} {'guess' if attempt == 1 else 'guesses'}.")
            return True
        if guess < answer:
            print_fn("Too low!")
        else:
            print_fn("Too high!")

    print_fn(f"Out of guesses! The number was {answer}.")
    return False


def main() -> None:
    """Run rounds until the player chooses to stop."""
    print("Welcome to Number Hunt!")
    wins = 0
    rounds = 0

    while True:
        rounds += 1
        if play_round():
            wins += 1
        while True:
            again = input("\nPlay again? (y/n): ").strip().lower()
            if again in {"y", "yes"}:
                break
            if again in {"n", "no"}:
                print(f"\nFinal score: {wins}/{rounds} rounds won. Thanks for playing!")
                return
            print("Please enter y or n.")


if __name__ == "__main__":
    main()
