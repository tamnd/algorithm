# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/penn-treebank-tokenization/. The authors are listed in prov/BK6WGY.jsonl.

"""Penn Treebank word tokenization, after the sed script of Robert MacIntyre (1995).

The input is one sentence on one line. The rules run in a fixed order, each on
the whole string, as in the sed script; then the string is split at spaces.
Double quotes become `` (open) and '' (close). Clitics such as 's, 're and
n't become separate tokens, so "can't" gives "ca" and "n't". Only a period at
the end of the line is split off; a period inside the sentence stays with
its word, as in "Mr." or "3.5". Brackets are kept as they are; the treebank
files later wrote them as -LRB-, -RRB- and so on, which this file does not do.
"""

import re
from typing import List, Tuple

Rule = Tuple["re.Pattern[str]", str]


def _rules(pairs: List[Tuple[str, str]]) -> List[Rule]:
    return [(re.compile(p), r) for p, r in pairs]


OPEN_QUOTES = _rules([
    (r'^"', r"`` "),
    (r'([ (\[{<])"', r"\1 `` "),
])
PUNCT = _rules([
    (r"\.\.\.", r" ... "),
    (r"[,;:@#$%&]", r" \g<0> "),
])
FINAL_PERIOD = _rules([
    (r"""([^.])(\.)([\])}>"']*)[ \t]*$""", r"\1 \2\3 "),
])
BRACKETS = _rules([
    (r"[?!]", r" \g<0> "),
    (r"[\]\[(){}<>]", r" \g<0> "),
    (r"--", r" -- "),
])
CLOSE_QUOTES = _rules([
    (r'"', r" '' "),
])
CLITICS = _rules([
    (r"([^'])' ", r"\1 ' "),
    (r"'([sSmMdD]) ", r" '\1 "),
    (r"'ll ", r" 'll "),
    (r"'re ", r" 're "),
    (r"'ve ", r" 've "),
    (r"n't ", r" n't "),
    (r"'LL ", r" 'LL "),
    (r"'RE ", r" 'RE "),
    (r"'VE ", r" 'VE "),
    (r"N'T ", r" N'T "),
])
SPECIAL_WORDS = _rules([
    (r" ([Cc])annot ", r" \1an not "),
    (r" ([Dd])'ye ", r" \1' ye "),
    (r" ([Gg])imme ", r" \1im me "),
    (r" ([Gg])onna ", r" \1on na "),
    (r" ([Gg])otta ", r" \1ot ta "),
    (r" ([Ll])emme ", r" \1em me "),
    (r" ([Mm])ore'n ", r" \1ore 'n "),
    (r" '([Tt])is ", r" '\1 is "),
    (r" '([Tt])was ", r" '\1 was "),
    (r" ([Ww])anna ", r" \1an na "),
])


def _apply(rules: List[Rule], x: str) -> str:
    for pattern, repl in rules:
        x = pattern.sub(repl, x)
    return x


def ptb_stages(x: str) -> List[str]:
    """Return the string after each line L1 to L9 of the pseudocode, in order.

    Precondition: x is one sentence with no line break. Cost: O(len(x)) for
    each of the 29 substitutions, so O(len(x)) in all, because no rule makes
    the string more than a constant factor longer.
    """
    if "\n" in x or "\r" in x:
        raise ValueError("one sentence per line: the input has a line break")
    out = []
    x = _apply(OPEN_QUOTES[:1], x)  # @line L1
    out.append(x)
    x = _apply(OPEN_QUOTES[1:], x)  # @line L2
    out.append(x)
    x = _apply(PUNCT, x)  # @line L3
    out.append(x)
    x = _apply(FINAL_PERIOD, x)  # @line L4
    out.append(x)
    x = _apply(BRACKETS, x)  # @line L5
    out.append(x)
    x = " " + x + " "  # @line L6
    out.append(x)
    x = _apply(CLOSE_QUOTES, x)  # @line L7
    out.append(x)
    x = _apply(CLITICS, x)  # @line L8
    out.append(x)
    x = _apply(SPECIAL_WORDS, x)  # @line L9
    out.append(x)
    return out


def ptb_tokenize(x: str) -> List[str]:
    """Split one English sentence into Penn Treebank tokens.

    Precondition: x is one sentence with no line break. Cost: O(len(x)).
    """
    return ptb_stages(x)[-1].split()  # @line L10
