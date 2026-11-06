# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sieve-of-atkin/. The authors are listed in prov/GPR00G.jsonl.

from math import isqrt


def sieve_of_atkin(n: int) -> list[int]:
    """Return the increasing list of all primes p <= n (the basic mod 12 sieve of Atkin).

    Precondition: n is an integer (n < 2 gives []).
    Cost: Theta(n) word operations and n + 1 flags of memory.
    """
    if n < 2:  # @line L1
        return []
    flag = bytearray(n + 1)  # @line L2
    x = 1
    while 4 * x * x + 1 <= n:  # @line L3
        y = 1
        while True:
            m = 4 * x * x + y * y
            if m > n:
                break
            if m % 12 == 1 or m % 12 == 5:
                flag[m] ^= 1
            y += 1
        x += 1
    x = 1
    while 3 * x * x + 1 <= n:  # @line L4
        y = 1
        while True:
            m = 3 * x * x + y * y
            if m > n:
                break
            if m % 12 == 7:
                flag[m] ^= 1
            y += 1
        x += 1
    x = 2
    while 2 * x * x + 2 * x - 1 <= n:  # @line L5
        y = x - 1  # 3x^2 - y^2 grows as y falls, so start at the smallest value
        while y >= 1:
            m = 3 * x * x - y * y
            if m > n:
                break
            if m % 12 == 11:
                flag[m] ^= 1
            y -= 1
        x += 1
    for r in range(5, isqrt(n) + 1):  # @line L6
        if flag[r]:  # @line L7
            sq = r * r
            for k in range(sq, n + 1, sq):
                flag[k] = 0
    out = [p for p in (2, 3) if p <= n]  # @line L8
    out.extend(m for m in range(5, n + 1) if flag[m])
    return out
