class Hangman:
    def __init__(self, word, max_wrong=6):
        self.word = word.upper()
        self.max_wrong = max_wrong
        self.guessed = set()
        self.wrong_guesses = set()
        self.state = "IN_PROGRESS"

    def guess(self, letter):
        letter = letter.upper()

        if len(letter) != 1 or not letter.isalpha():
            return "INVALID"

        if self.state != "IN_PROGRESS":
            return "GAME_OVER"

        if letter in self.guessed:
            return "DUPLICATE"

        self.guessed.add(letter)

        if letter not in self.word:
            self.wrong_guesses.add(letter)
            result = "INCORRECT"
        else:
            result = "CORRECT"

        if all(c in self.guessed for c in self.word):
            self.state = "WON"
        elif len(self.wrong_guesses) >= self.max_wrong:
            self.state = "LOST"

        return result

    def display(self):
        return " ".join(
            c if c in self.guessed else "_"
            for c in self.word
        )
    
game = Hangman("APPLE", 3)

print(game.display())  # _ _ _ _ _

print(game.guess("P"))  # CORRECT
print(game.display())  # _ P P _ _

print(game.guess("P"))  # DUPLICATE
print(game.guess("Z"))  # INCORRECT

print(game.state)       # IN_PROGRESS

# 写cli：
def main():
    word = "APPLE"
    game = Hangman(word, max_wrong=6)

    print("Welcome to Hangman!")

    while game.state == "IN_PROGRESS":
        print(f"\nWord: {game.display()}")
        print(f"Wrong guesses: {', '.join(sorted(game.wrong_guesses))}")
        print(f"Attempts left: {game.max_wrong - len(game.wrong_guesses)}")

        letter = input("Guess a letter: ").strip()

        result = game.guess(letter)
        print(f"Result: {result}")

    # Game finished
    if game.state == "WON":
        print(f"\nYou won! The word was {game.word}")
    else:
        print(f"\nYou lost! The word was {game.word}")


if __name__ == "__main__":
    main()