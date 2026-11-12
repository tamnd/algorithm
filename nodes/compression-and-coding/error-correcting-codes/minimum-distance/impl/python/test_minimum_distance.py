# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-distance/. The authors are listed in prov/PFEGKF.jsonl.

import itertools
import random

from minimum_distance import (
    correction_radius, decode, detect, detection_guarantee, distance, linear_code, minimum_distance,
)

HAMMING_7_4 = linear_code([[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]], 2)
EXT_HAMMING_8_4 = [c + (sum(c) % 2,) for c in HAMMING_7_4]
REPETITION_5 = [(0,) * 5, (1,) * 5]
# a ternary [4, 2, 3] code (the tetracode)
TETRACODE = linear_code([[1, 0, 1, 1], [0, 1, 1, 2]], 3)


def random_code(rng: random.Random, n: int, m: int, q: int) -> list:
    words = set()
    while len(words) < m:
        words.add(tuple(rng.randrange(q) for _ in range(n)))
    return sorted(words)


def add(c, e, q):
    return tuple((a + b) % q for a, b in zip(c, e))


def patterns(n, w, q):
    """All error patterns of weight exactly w over Z_q."""
    for pos in itertools.combinations(range(n), w):
        for vals in itertools.product(range(1, q), repeat=w):
            e = [0] * n
            for p, v in zip(pos, vals):
                e[p] = v
            yield tuple(e)


def test_known_minimum_distances() -> None:
    assert minimum_distance(HAMMING_7_4) == 3
    assert minimum_distance(EXT_HAMMING_8_4) == 4
    assert minimum_distance(REPETITION_5) == 5
    assert minimum_distance(TETRACODE) == 3
    assert detection_guarantee(3) == 2 and correction_radius(3) == 1 and correction_radius(4) == 1


def check_code(code, q) -> None:
    n, d = len(code[0]), minimum_distance(code)
    t = correction_radius(d)
    for c in code:
        # detection of every pattern of weight 1 .. d - 1
        for w in range(1, d):
            for e in patterns(n, w, q):
                assert detect(code, add(c, e, q))
        # correction of every mix of t' errors and e erasures with 2 t' + e < d
        for ne in range(0, d):
            for erased in itertools.combinations(range(n), ne):
                rest = [i for i in range(n) if i not in erased]
                for te in range(0, (d - 1 - ne) // 2 + 1):
                    for pos in itertools.combinations(rest, te):
                        for vals in itertools.product(range(1, q), repeat=te):
                            r = list(c)
                            for p, v in zip(pos, vals):
                                r[p] = (r[p] + v) % q
                            for p in erased:
                                r[p] = None
                            assert decode(code, r, d) == c
    assert t == (d - 1) // 2


def test_guarantees_exhaustive_on_small_codes() -> None:
    check_code(HAMMING_7_4, 2)
    check_code(EXT_HAMMING_8_4, 2)
    check_code(REPETITION_5, 2)
    check_code(TETRACODE, 3)
    rng = random.Random(42)
    for _ in range(20):  # codes that are not linear
        code = random_code(rng, 6, rng.randrange(2, 6), 2)
        check_code(code, 2)


def test_guarantees_are_tight() -> None:
    for code, q in ((HAMMING_7_4, 2), (EXT_HAMMING_8_4, 2), (REPETITION_5, 2), (TETRACODE, 3)):
        d = minimum_distance(code)
        x, y = next((a, b) for a, b in itertools.combinations(code, 2) if distance(a, b) == d)
        # d errors can turn x into y: not detected
        assert not detect(code, y)
        # d erasures on the positions where x and y differ leave two candidates
        diff = [i for i in range(len(x)) if x[i] != y[i]]
        r = [None if i in diff else x[i] for i in range(len(x))]
        assert decode(code, r, d) is None
        # t + 1 errors: move from x toward y by t + 1 positions; the decoder fails or errs
        t = (d - 1) // 2
        r = list(x)
        for i in diff[: t + 1]:
            r[i] = y[i]
        assert decode(code, tuple(r), d) != x


def test_example_on_the_page() -> None:
    code = EXT_HAMMING_8_4
    c = code[5]
    r = list(c)
    r[0] ^= 1          # one error
    r[3] = None        # one erasure: 2 * 1 + 1 = 3 < 4
    assert decode(code, r, 4) == c
    r2 = list(c)
    r2[0] ^= 1
    r2[1] ^= 1         # two errors: detected (2 <= d - 1) but not corrected
    assert detect(code, tuple(r2)) and decode(code, r2, 4) is None
