from collections import defaultdict

class Solution:
    def getHint(self, secret: str, guess: str) -> str:
        ha = defaultdict(int)
        bulls = cows = 0

        for idx, sh in enumerate(secret):
            print(ha)
            g = guess[idx]
            if sh == g: 
                bulls += 1
            else:
                cows += int(ha[sh] < 0) + int(ha[g] > 0)
                ha[sh] += 1
                ha[g] -= 1
                
        return "{}A{}B".format(bulls, cows)
    

def play_game():
    secret = "1231"
    max_attempts = 5
    solution = Solution()

    for attempt in range(max_attempts):
        guess = input("Enter your guess: ")

        result = solution.getHint(secret, guess)
        print(result)

        if result == "4A0B":
            print("Congratulations! You won!")
            return

    print("Game Over!")
    print(f"The secret was {secret}")


if __name__ == "__main__":
    play_game()