
###################
# Zac McCullough
# mccul157@msu.edu
# 1/28
###################

"""Technology demonstrator of regex"""

##########
# imports
##########

import re
from typing import List


######################
# function definitions
######################

def extract_questions(msg: str) -> List[str]:
    temp = msg
    results = []
    while len(temp) > 0:
        x = re.search('[^\.!]*?(\?)', temp)
        # \. means literal period
        # ^\. means negated set
        # ! is a regular ! for matching
        # [^\.!] Means don't match . or !
        # * means match 0 or more .s or !s before
        # ? lazy so it needs to match as few as possible (minimizer)
        # () is a capture group for matching
        # \? is escaped question mark for matching
        # ergo this matches all smallest spaces that end in a question mark and start
        # at a period or exclamation point
        if x is not None and x.group():
            results.append(x.group())
            temp = temp[x.span()[1]:]
        else:
            break
    return results


def __main__() -> None:
    input_text = ['question?', ' This is a question?', 'Multiple? Questions?', 'This? is a very comp? long multique!,']
    for text in input_text:
        print(extract_questions(text))


__main__()


