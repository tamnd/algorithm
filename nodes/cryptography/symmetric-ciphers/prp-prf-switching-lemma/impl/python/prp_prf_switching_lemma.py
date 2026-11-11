# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prp-prf-switching-lemma/. The authors are listed in prov/7NPNRH.jsonl.
"""Exact numbers for the PRP/PRF switching lemma on tiny block lengths.

For study only. Nothing here encrypts data, and nothing is constant time.

The value best_advantage(n, q) is the largest advantage of any adaptive
adversary that makes q queries and tries to tell a random permutation of
n-bit strings from a random function of n-bit strings. It is computed by
dynamic programming over all transcripts, with exact fractions.
Cost: about (2^n)^(2q) transcript steps, so only for tiny n and q.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import permutations, product


def switching_bound(n: int, q: int) -> Fraction:
    """The bound q(q - 1) / 2^(n + 1) of the lemma."""
    return Fraction(q * (q - 1), 2 ** (n + 1))


def collision_probability(n: int, q: int) -> Fraction:
    """The probability that q distinct queries to a random function give some equal answers."""
    big = 2 ** n
    p = Fraction(1)
    for i in range(q):
        p *= Fraction(big - i, big)
    return 1 - p


@lru_cache(maxsize=None)
def best_advantage(n: int, q: int) -> Fraction:
    """max over adaptive deterministic adversaries with q queries of Pr[A^rho = 1] - Pr[A^pi = 1]."""
    big = 2 ** n

    def value(trans: tuple[tuple[int, int], ...], p_rf: Fraction, p_rp: Fraction) -> Fraction:
        if len(trans) == q:
            return max(p_rf - p_rp, Fraction(0))  # output 1 exactly when the function is more likely
        seen = dict(trans)
        used = set(seen.values())
        best = Fraction(0)
        for x in range(big):  # the adversary may pick any next query, a repeated one too
            total = Fraction(0)
            for y in range(big):
                if x in seen:
                    if y != seen[x]:
                        continue
                    a, b = p_rf, p_rp
                else:
                    a = p_rf / big
                    b = Fraction(0) if y in used else p_rp / (big - len(used))
                total += value(trans + ((x, y),), a, b)
            best = max(best, total)
        return best

    return value((), Fraction(1), Fraction(1))


def bellare_rogaway_example() -> tuple[Fraction, Fraction]:
    """The adversary of Bellare and Rogaway (2006) with n = 2.

    It asks f(0); it outputs 1 if f(0) = 0. Else it asks f(1) and outputs 1 if f(1) = 1.
    Return Pr[A^pi = 1] and Pr[A^rho = 1 | the answers are distinct].
    """

    def run(f: tuple[int, ...]) -> tuple[int, bool]:
        if f[0] == 0:
            return 1, True
        return int(f[1] == 1), f[1] != f[0]

    perms = list(permutations(range(4)))
    p_pi = Fraction(sum(run(p)[0] for p in perms), len(perms))
    funcs = list(product(range(4), repeat=4))
    dist = [run(f) for f in funcs]
    n_dist = sum(1 for _, d in dist if d)
    n_one = sum(1 for out, d in dist if d and out == 1)
    return p_pi, Fraction(n_one, n_dist)
