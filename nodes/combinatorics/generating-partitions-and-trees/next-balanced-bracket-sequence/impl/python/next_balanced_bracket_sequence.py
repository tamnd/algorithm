# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-balanced-bracket-sequence/. The authors are listed in prov/BRK0H7.jsonl.

from collections.abc import Iterator


def next_balanced(s: list[str]) -> bool:
    """Turn the balanced bracket sequence s into the next one in lexicographic order.

    The order uses '(' < ')'. The list s is changed in place. Return True
    if s had a successor. If s is the last sequence "()()...()", leave it
    unchanged and return False.
    """
    m = len(s)
    d = 0  # @line L1
    for i in range(m - 1, -1, -1):  # @line L2
        if s[i] == ")":  # @line L3
            d += 1
        else:
            d -= 1  # @line L4: d is now the height before position i
            if d > 0:  # @line L5
                s[i] = ")"  # @line L6
                p = (m - 1 - i - d + 1) // 2  # @line L7: opening brackets after i
                for t in range(i + 1, i + 1 + p):  # @line L8
                    s[t] = "("
                for t in range(i + 1 + p, m):  # @line L9
                    s[t] = ")"
                return True  # @line L10
    return False  # @line L11


def balanced_sequences(n: int) -> Iterator[str]:
    """Yield every balanced sequence of n bracket pairs, in lexicographic order."""
    if n < 0:
        raise ValueError("n must be non-negative")
    s = ["("] * n + [")"] * n
    while True:
        yield "".join(s)
        if not next_balanced(s):
            return
