# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counterfeit-coin-problem/. The authors are listed in prov/ASZJ2T.jsonl.
"""The counterfeit coin problem with a balance scale.

N coins, numbered 0 to N - 1, look the same. One is counterfeit and is either
heavier or lighter than the others. A weighing compares two sets of coins of
the same size and says which pan is heavier, or that they balance. The task is
to find the counterfeit coin and say whether it is heavy or light.
"""

from functools import lru_cache
from itertools import product

LEFT, RIGHT, EQUAL = "L", "R", "="


def weigh(left, right, fake, heavy):
    """The result of putting coins `left` against coins `right`."""
    assert len(left) == len(right) and not set(left) & set(right)
    if fake in left:
        return LEFT if heavy else RIGHT
    if fake in right:
        return RIGHT if heavy else LEFT
    return EQUAL


def twelve_adaptive(scale):
    """Solve 12 coins in 3 weighings. scale(left, right) returns L, R or =.

    Returns (coin, heavy) where heavy is True for a heavy coin.
    """
    first = scale([0, 1, 2, 3], [4, 5, 6, 7])
    if first == EQUAL:
        # the fake is among 8 to 11; coins 0 to 7 are genuine
        second = scale([8, 9, 10], [0, 1, 2])
        if second == EQUAL:
            third = scale([11], [0])
            return 11, third == LEFT
        heavy = second == LEFT
        third = scale([8], [9])
        if third == EQUAL:
            return 10, heavy
        return (8 if (third == LEFT) == heavy else 9), heavy
    # first pan heavy: 0..3 possibly heavy and 4..7 possibly light (or the reverse)
    if first == LEFT:
        hv, lt = [0, 1, 2, 3], [4, 5, 6, 7]
    else:
        hv, lt = [4, 5, 6, 7], [0, 1, 2, 3]
    # weigh h0 h1 l0 against h2 l1 g (g = 8 is genuine)
    second = scale([hv[0], hv[1], lt[0]], [hv[2], lt[1], 8])
    if second == EQUAL:
        # fake is hv[3] (heavy) or lt[2], lt[3] (light)
        third = scale([lt[2]], [lt[3]])
        if third == EQUAL:
            return hv[3], True
        return (lt[3] if third == LEFT else lt[2]), False
    if second == LEFT:
        # hv[0] or hv[1] heavy, or lt[1] light
        third = scale([hv[0]], [hv[1]])
        if third == EQUAL:
            return lt[1], False
        return (hv[0] if third == LEFT else hv[1]), True
    # second == RIGHT: hv[2] heavy or lt[0] light
    third = scale([hv[2]], [8])
    if third == EQUAL:
        return lt[0], False
    return hv[2], True


def dyson_labels(n_coins=12, w=3):
    """Labels for a non-adaptive scheme: one ternary word per coin (Dyson's method).

    Words with all digits equal are left out. Of each pair (x, its negation
    mod 3) one word is taken, so that in every position each digit is used by
    the same number of coins. Returns a list of n_coins words, or None.
    """
    words = [t for t in product(range(3), repeat=w) if len(set(t)) > 1]
    pairs, seen = [], set()
    for t in words:
        neg = tuple((-x) % 3 for x in t)
        if t not in seen and neg not in seen:
            pairs.append((t, neg))
            seen.update((t, neg))
    for choice in product((0, 1), repeat=len(pairs)):
        chosen = [p[c] for p, c in zip(pairs, choice)][:n_coins]
        if len(chosen) < n_coins:
            return None
        if all(sum(1 for t in chosen if t[i] == 1) == sum(1 for t in chosen if t[i] == 2)
               for i in range(w)):
            return chosen
    return None


def nonadaptive_plan(labels):
    """Weighing i puts the coins with digit 1 in position i left and those with digit 2 right."""
    w = len(labels[0])
    return [([c for c, t in enumerate(labels) if t[i] == 1], [c for c, t in enumerate(labels) if t[i] == 2])
            for i in range(w)]


def nonadaptive_decode(labels, results):
    """Read the coin from the results: L is digit 1, R is digit 2, = is digit 0."""
    word = tuple({EQUAL: 0, LEFT: 1, RIGHT: 2}[r] for r in results)
    for c, t in enumerate(labels):
        if t == word:
            return c, True
        if tuple((-x) % 3 for x in t) == word:
            return c, False
    return None


def solvable(n_coins, w, extra_genuine=0, heavy_only=False):
    """Exhaustive search over all adaptive strategies (by class counts).

    With heavy_only=True the fake coin is known to be heavy, and only the coin
    must be found.

    True when some strategy of at most w weighings always finds the fake coin
    and its type. Coins are only told apart by what is known about them: unknown
    (u), possibly heavy only (h), possibly light only (l), or genuine (g).
    """

    @lru_cache(maxsize=None)
    def unknown(u, g, w):
        cases = 2 * u
        if cases <= 1:
            return True
        if w == 0 or cases > 3 ** w:
            return False
        for u1 in range(u + 1):
            for u2 in range(u - u1 + 1):
                if u1 + u2 == 0 or abs(u1 - u2) > g:
                    continue
                if not known(u1, u2, g + u - u1 - u2, w - 1):
                    continue
                if unknown(u - u1 - u2, g + u1 + u2, w - 1):
                    return True
        return False

    @lru_cache(maxsize=None)
    def known(h, l, g, w):
        if h < l:
            h, l = l, h
        g = min(g, h + l)
        cases = h + l
        if cases <= 1:
            return True
        if w == 0 or cases > 3 ** w:
            return False
        t = 3 ** (w - 1)
        for h1 in range(h + 1):
            for h2 in range(h - h1 + 1):
                for l1 in range(l + 1):
                    if h2 + l1 > t:
                        break
                    for l2 in range(l - l1 + 1):
                        if h1 + l2 > t:
                            break
                        if cases - h1 - h2 - l1 - l2 > t:
                            continue
                        if abs(h1 + l1 - h2 - l2) > g:
                            continue
                        # every coin that drops out of the suspects is genuine
                        hh, ll = h - h1 - h2, l - l1 - l2
                        if (known(h1, l2, g + cases - h1 - l2, w - 1)
                                and known(h2, l1, g + cases - h2 - l1, w - 1)
                                and known(hh, ll, g + cases - hh - ll, w - 1)):
                            return True
        return False

    if heavy_only:
        return known(n_coins, 0, extra_genuine, w)
    return unknown(n_coins, extra_genuine, w)


def solvable_counts(w, extra_genuine=0):
    """All numbers of coins from 1 to 3^w that w weighings can solve."""
    return [n for n in range(1, 3 ** w + 1) if solvable(n, w, extra_genuine)]
