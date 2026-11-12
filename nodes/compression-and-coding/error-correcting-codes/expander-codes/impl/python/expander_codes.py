# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expander-codes/. The authors are listed in prov/D5Z0XF.jsonl.

"""Expander codes of Sipser and Spielman (1996) with parity checks.

A (c, d)-biregular bipartite graph has n variable nodes of degree c and
m = n c / d check nodes of degree d. The code is every word whose bits sum
to 0 at each check. The graph is an (A, delta) expander when every set S of
at most A variables has |N(S)| >= delta c |S| neighbors. If 3/4 < delta < 1, the
flip decoder below corrects every error pattern of weight at most
(2 delta - 1) A, with a number of flips at most c times the weight.
"""

import random
from fractions import Fraction
from typing import List, Optional, Sequence, Tuple


def array_graph(p: int, c: int) -> List[List[int]]:
    """Check lists of the array construction: n = p^2 variables (b, x) and
    c p checks (a, r); check (a, r) holds the variables with x = r + a b
    mod p. For prime p two variables share at most one check."""
    return [[b * p + (r + a * b) % p for b in range(p)] for a in range(c) for r in range(p)]


def random_biregular(n: int, c: int, d: int, rng: random.Random) -> List[List[int]]:
    """Check lists of a random (c, d)-biregular graph with no double edges:
    a shuffled list of n c variable stubs cut into checks of size d, then
    random swaps until no check holds a variable twice."""
    stubs = [j for j in range(n) for _ in range(c)]
    rng.shuffle(stubs)
    while True:
        bad = [q for q in range(n * c) if stubs[q] in stubs[(q // d) * d:q]]
        if not bad:
            return [stubs[i * d:(i + 1) * d] for i in range(n * c // d)]
        q, r = rng.choice(bad), rng.randrange(n * c)
        a, b = q // d, r // d
        if a != b and stubs[r] not in stubs[a * d:(a + 1) * d] and stubs[q] not in stubs[b * d:(b + 1) * d]:
            stubs[q], stubs[r] = stubs[r], stubs[q]


def variable_lists(checks: Sequence[Sequence[int]], n: int) -> List[List[int]]:
    var: List[List[int]] = [[] for _ in range(n)]
    for i, row in enumerate(checks):
        for j in row:
            var[j].append(i)
    return var


def expansion_profile(var: Sequence[Sequence[int]], smax: int) -> List[Optional[int]]:
    """By brute force over every set S of 1..smax variables: entry s is the
    least |N(S)| with |S| = s. Neighbor sets are bit masks."""
    n = len(var)
    masks = [sum(1 << i for i in v) for v in var]
    best: List[Optional[int]] = [None] * (smax + 1)

    def grow(start: int, size: int, mask: int) -> None:
        for j in range(start, n):
            mk = mask | masks[j]
            k = bin(mk).count("1")
            cur = best[size + 1]
            if cur is None or k < cur:
                best[size + 1] = k
            if size + 1 < smax:
                grow(j + 1, size + 1, mk)

    grow(0, 0, 0)
    return best


def guaranteed_radius(profile: Sequence[Optional[int]], c: int) -> Tuple[int, int, Fraction]:
    """The best (radius, A, delta) the theorem gives from a measured profile:
    over A with delta_A = min over s <= A of profile[s] / (c s) strictly
    between 3/4 and 1, the radius is floor((2 delta_A - 1) A)."""
    best = (0, 0, Fraction(0))
    delta = Fraction(1)
    for a in range(1, len(profile)):
        size = profile[a]
        if size is None:
            break
        delta = min(delta, Fraction(size, c * a))
        if delta <= Fraction(3, 4):
            break
        if delta == 1:
            continue  # the theorem needs delta < 1: equal columns pass delta = 1 at A = 1
        radius = int((2 * delta - 1) * a)
        if radius > best[0]:
            best = (radius, a, delta)
    return best


def flip_decode(checks: Sequence[Sequence[int]], n: int, word: Sequence[int],
                max_flips: Optional[int] = None) -> Tuple[List[int], int]:
    """Sipser and Spielman's sequential decoder: while some variable has more
    unsatisfied than satisfied checks, flip it. Returns (word, flips).
    Each flip lowers the number of unsatisfied checks by at least 1."""
    var = variable_lists(checks, n)
    w = list(word)  # @line L1
    unsat = [sum(w[j] for j in row) & 1 for row in checks]  # @line L2
    bad = [sum(unsat[i] for i in var[j]) for j in range(n)]
    todo = [j for j in range(n) if 2 * bad[j] > len(var[j])]  # @line L3
    flips = 0
    limit = sum(unsat) if max_flips is None else max_flips
    while todo and flips < limit:
        j = todo.pop()
        if 2 * bad[j] <= len(var[j]):  # @line L4
            continue
        w[j] ^= 1  # @line L5
        flips += 1
        for i in var[j]:
            unsat[i] ^= 1  # @line L6
            step = 1 if unsat[i] else -1
            for k in checks[i]:
                bad[k] += step  # @line L7
                if 2 * bad[k] > len(var[k]):
                    todo.append(k)
    return w, flips  # @line L8
