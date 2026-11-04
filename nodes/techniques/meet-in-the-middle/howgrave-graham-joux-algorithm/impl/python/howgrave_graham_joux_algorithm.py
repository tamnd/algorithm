# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/howgrave-graham-joux-algorithm/. The authors are listed in prov/ZVD66Y.jsonl.

import itertools
import math
import random


def _list(
    a: list[int], left: list[int], i: int, right: list[int], j: int, r: int, m: int
) -> list[int]:
    """Return the masks x with i ones in left, j ones in right, and sum(a[x]) = r (mod m)."""
    g: dict[int, list[int]] = {}  # @line L12
    for z in itertools.combinations(right, j):
        g.setdefault(sum(a[p] for p in z) % m, []).append(sum(1 << p for p in z))
    out: list[int] = []  # @line L13
    for x in itertools.combinations(left, i):  # @line L14
        mx = sum(1 << p for p in x)
        for mz in g.get((r - sum(a[p] for p in x)) % m, []):
            out.append(mx | mz)
    return out  # @line L15


def _weight_sum(a: list[int], mask: int) -> int:
    return sum(a[p] for p in range(len(a)) if mask >> p & 1)


def howgrave_graham_joux(
    a: list[int],
    t: int,
    w: int,
    rounds: int | None = None,
    rng: random.Random | None = None,
    fallback: bool = True,
) -> list[int] | None:
    """Return the sorted positions of a w-subset of a with sum t, or None if there is none.

    One level of representations: a solution e of weight w with
    floor(w/2) ones in the left half is written as x + y, where x takes
    floor(p/2) of its left ones and floor(q/2) of its right ones. A random
    modular constraint on the sum of x keeps about one of these
    representations. The answer is always correct: after `rounds` random
    rounds, the search falls back to trying all w-subsets. The cost of a
    round is the size of the lists it builds; the bounds on the page are
    heuristic. With fallback=False the search is Monte Carlo: it may
    return None although a solution exists, but a returned set is correct.
    """
    n = len(a)
    if w < 0 or w > n:
        return None
    rng = rng if rng is not None else random.Random()
    rounds = 4 * (n + 1) if rounds is None else rounds
    p, q = w // 2, w - w // 2  # @line L1
    p1, q1 = p // 2, q // 2  # @line L2
    m = math.comb(p, p1) * math.comb(q, q1)  # @line L3
    for _ in range(rounds):  # @line L4
        perm = list(range(n))  # @line L5
        rng.shuffle(perm)
        left, right = perm[: n // 2], perm[n // 2 :]
        r = rng.randrange(m)  # @line L6
        lx = _list(a, left, p1, right, q1, r, m)  # @line L7
        ly = _list(a, left, p - p1, right, q - q1, (t - r) % m, m)  # @line L8
        h: dict[int, list[int]] = {}  # @line L9
        for y in ly:
            h.setdefault(_weight_sum(a, y), []).append(y)
        for x in lx:  # @line L10
            for y in h.get(t - _weight_sum(a, x), []):
                if x & y == 0:
                    e = x | y
                    return [i for i in range(n) if e >> i & 1]
    if not fallback:
        return None
    for c in itertools.combinations(range(n), w):  # @line L11
        if sum(a[i] for i in c) == t:
            return list(c)
    return None
