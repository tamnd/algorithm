# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ehrlich-loopless-combinations/. The authors are listed in prov/3PVRP2.jsonl.

from collections.abc import Iterator
from math import comb

UP, DOWN, DONE = 0, 1, 2


def _revolving_door_loopless(n: int, k: int, tests: list[int] | None) -> Iterator[tuple[int, ...]]:
    """The main algorithm for n > k > 1. Yield (c_k, ..., c_1) in revolving door order."""
    c = [0] * (k + 2)  # c[0] is not used
    for i in range(1, k + 1):  # @line L1
        c[i] = i - 1
    c[k + 1] = n
    j = k + 1
    odd = k % 2 == 1
    while True:  # @line L2
        yield tuple(c[k:0:-1])  # @line L3
        count = 0
        if j >= 3 + odd:  # @line L4: the jump
            j = j - 1 - ((j - k) % 2 == 0)
            s = UP
        elif odd and c[1] + 1 < c[2]:  # @line L5
            c[1] += 1
            j = 1
            s = DONE
        elif not odd and c[1] > 0:  # @line L6
            c[1] -= 1
            j = 1
            s = DONE
        else:  # @line L7
            j = 2
            s = DOWN if odd else UP
        while s != DONE:  # @line L8
            count += 1
            if s == DOWN and c[j] >= j:  # @line L9
                c[j] = c[j - 1]
                c[j - 1] = j - 2
                s = DONE
            elif s == DOWN:  # @line L10
                j += 1
                s = UP
            elif c[j] + 1 < c[j + 1]:  # @line L11
                c[j - 1] = c[j]
                c[j] += 1
                s = DONE
            else:  # @line L12
                j += 1
                s = DOWN
                if j > k:
                    if tests is not None:
                        tests.append(count)
                    return
        if tests is not None:
            tests.append(count)


def revolving_door(n: int, k: int, tests: list[int] | None = None) -> Iterator[tuple[int, ...]]:
    """Yield the k-subsets of {0, ..., n-1} as decreasing tuples, in revolving door order.

    If tests is a list, append to it the number of passes of the inner loop for each step.
    """
    if k < 0 or k > n:
        return
    if k == 0 or k == n:
        yield tuple(range(k - 1, -1, -1))
        return
    if k == 1:
        for x in range(n):
            yield (x,)
        return
    yield from _revolving_door_loopless(n, k, tests)


def revolving_door_rank(c: tuple[int, ...]) -> int:
    """Rank of (c_k, ..., c_1) in revolving door order, by the alternating number system."""
    k = len(c)
    total = 0
    for pos, value in enumerate(c):  # value is c_i with i = k - pos
        i = k - pos
        total += (-1) ** (k - i) * comb(value + 1, i)
    return total - (k % 2)
