# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/colinear-chaining/. The authors are listed in prov/H5YXHD.jsonl.

import random

from colinear_chaining import brute_force, colinear_chain, is_chain

# The page example: (x1, x2, y1, y2, w)
EXAMPLE = [
    (0, 4, 2, 6, 5),      # A
    (3, 8, 10, 15, 6),    # B
    (6, 9, 8, 11, 4),     # C
    (11, 15, 12, 16, 5),  # D
    (12, 14, 20, 22, 3),  # E
    (17, 22, 18, 23, 6),  # F
]


def test_page_example() -> None:
    score, chain = colinear_chain(EXAMPLE)
    assert score == 20
    assert chain == [0, 2, 3, 5]
    assert brute_force(EXAMPLE) == 20


def test_empty_and_single() -> None:
    assert colinear_chain([]) == (0, [])
    assert colinear_chain([(1, 1, 1, 1, 7)]) == (7, [0])


def test_touching_is_not_colinear() -> None:
    # equal end and start coordinates do not chain (strict precedence)
    frags = [(0, 5, 0, 5, 3), (5, 9, 6, 9, 4)]
    assert colinear_chain(frags) == (4, [1])
    frags = [(0, 5, 0, 5, 3), (6, 9, 5, 9, 4)]
    assert colinear_chain(frags) == (4, [1])
    frags = [(0, 5, 0, 5, 3), (6, 9, 6, 9, 4)]
    assert colinear_chain(frags) == (7, [0, 1])


def test_lis_reduction() -> None:
    seq = [1, 2, 10, 4, 5, 8, 6, 7, 9, 3]
    frags = [(i, i, a, a, 1) for i, a in enumerate(seq)]
    score, chain = colinear_chain(frags)
    assert score == 7
    assert [seq[i] for i in chain] == [1, 2, 4, 5, 6, 7, 9]


def random_frags(rng: random.Random, n: int, span: int) -> list:
    out = []
    for _ in range(n):
        x1 = rng.randrange(span)
        y1 = rng.randrange(span)
        out.append((x1, x1 + rng.randrange(4), y1, y1 + rng.randrange(4), rng.randrange(1, 10)))
    return out


def test_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(300):
        frags = random_frags(rng, rng.randrange(1, 9), rng.choice([6, 15, 40]))
        score, chain = colinear_chain(frags)
        assert is_chain(frags, chain)
        assert sum(frags[i][4] for i in chain) == score
        assert score == brute_force(frags)


def test_larger_against_quadratic() -> None:
    rng = random.Random(2)
    for _ in range(8):
        frags = random_frags(rng, 200, 400)
        n = len(frags)
        order = sorted(range(n), key=lambda f: frags[f][0])
        best = {}
        for g in order:
            b = 0
            for f in best:
                if frags[f][1] < frags[g][0] and frags[f][3] < frags[g][2]:
                    b = max(b, best[f])
            best[g] = b + frags[g][4]
        score, chain = colinear_chain(frags)
        assert score == max(best.values())
        assert is_chain(frags, chain)
