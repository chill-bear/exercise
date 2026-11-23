from collections import defaultdict
from pdb import set_trace
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

test =Solution()
res = test.getHint("1231","0111")
print(f"{res} is result")

#1,2,3,1
#0,1,1,1