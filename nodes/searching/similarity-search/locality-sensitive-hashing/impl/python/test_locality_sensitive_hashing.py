# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locality-sensitive-hashing/. The authors are listed in prov/XTR0CK.jsonl.

import random

from locality_sensitive_hashing import LSHIndex, parameters


def hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def bit_family(d: int):
    def draw(rng: random.Random):
        i = rng.randrange(d)
        return lambda s: s[i]

    return draw


class Fixed:
    """A family that hands out the given bit positions in order, for the worked example."""

    def __init__(self, positions: list[int]) -> None:
        self.positions = positions
        self.t = 0

    def __call__(self, rng: random.Random):
        i = self.positions[self.t]
        self.t += 1
        return lambda s: s[i]


P = ["00010111", "11100000", "11010010", "01011011", "00111100", "10110100"]
Q = "10110001"


def test_example() -> None:
    idx = LSHIndex(P, Fixed([0, 3, 1, 6, 2, 7]), 2, 3, hamming)
    assert idx.tables[0][("1", "1")] == [2, 5]
    assert idx.tables[1][("0", "0")] == [4, 5]
    assert idx.query(Q, 2, 1) == 5
    assert idx.candidates(Q) == {2, 4, 5}
    assert idx.query(Q, 1, 1) is None


def test_parameters() -> None:
    assert parameters(10**6, 0.9, 0.8) == (62, 757)


def test_never_returns_a_far_point() -> None:
    rng = random.Random(7)
    for _ in range(200):
        d = 16
        pts = ["".join(rng.choice("01") for _ in range(d)) for _ in range(rng.randint(1, 30))]
        q = "".join(rng.choice("01") for _ in range(d))
        idx = LSHIndex(pts, bit_family(d), rng.randint(1, 4), rng.randint(1, 5), hamming, rng)
        c, r = 2, rng.randint(0, 4)
        got = idx.query(q, c, r)
        if got is not None:
            assert hamming(q, pts[got]) <= c * r
        if min(hamming(q, p) for p in pts) > c * r:
            assert got is None


def test_success_probability() -> None:
    rng = random.Random(2024)
    d, n, r, c = 32, 60, 2, 2
    k, L = parameters(n, 1 - r / d, 1 - c * r / d)
    ok = trials = 0
    for _ in range(300):
        pts = ["".join(rng.choice("01") for _ in range(d)) for _ in range(n)]
        base = pts[rng.randrange(n)]
        flip = set(rng.sample(range(d), r))
        q = "".join(("1" if ch == "0" else "0") if i in flip else ch for i, ch in enumerate(base))
        idx = LSHIndex(pts, bit_family(d), k, L, hamming, rng)
        got = idx.query(q, c, r)
        trials += 1
        ok += got is not None and hamming(q, pts[got]) <= c * r
    assert ok / trials >= 2 / 3 - 1 / 2.718281828


def test_candidates_against_brute_force() -> None:
    rng = random.Random(99)
    for _ in range(500):
        d = 10
        pts = ["".join(rng.choice("01") for _ in range(d)) for _ in range(rng.randint(0, 12))]
        q = "".join(rng.choice("01") for _ in range(d))
        idx = LSHIndex(pts, bit_family(d), 2, 3, hamming, rng)
        want = {i for i, p in enumerate(pts) if any(all(h(p) == h(q) for h in g) for g in idx.g)}
        assert idx.candidates(q) == want
