## secret = [1,2,3,1]
## guess = [0,1,1,1]
# hashmap of secret : {"1":2,"2":1,"3":1}. loop through guesses:
# guess[0] = 0, cow = 0, bull = 0
# guess[1] = 1, update hashmap {"1":1,"2":1,"3":1}, cow = 1, bull = 0
# guess[2] = 1, update hashmap {"1":0,"2":1,"3":1}, cow = 2, bull = 0
# guess[3] = 1, update hashmap {"1":-1,"2":1,"3":1}, cow = 1, bull = 1

from collections import Counter
class Solution:
    def getHint(self, secret: str, guess: str) -> str:
        h = Counter(secret)
        bulls = 0
        cows = 0

        for index,ch in enumerate(guess):
            if ch in h:
                if ch == secret[index]:
                    bulls = bulls + 1
                    # h[ch] <=0 : - 1 : because the previous guess index was used to add 1 cow 
                    # h[ch] > 0 : ignore
                    cows = cows - int(h[ch]<=0)
                else:
                    # h[ch] > 0: + 1
                    # h[ch] <= 0: ignore
                    cows = cows + int(h[ch]>0)
                h[ch] = h[ch] - 1
        return "{}A{}B".format(bulls,cows) 