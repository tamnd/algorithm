# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/post-randomization-method/. The authors are listed in prov/4VVPMW.jsonl.
import itertools
import random
from fractions import Fraction as F

import pytest

from post_randomization_method import (
    check_matrix,
    counts,
    estimate,
    invariant_matrix,
    ldp_ratio,
    pram,
    solve,
    transpose_times,
)

P3 = [[F(4, 5), F(1, 10), F(1, 10)], [F(1, 10), F(4, 5), F(1, 10)], [F(0), F(1, 5), F(4, 5)]]
RR = [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]


class Fixed:
    def __init__(self, us):
        self.us = list(us)

    def random(self) -> float:
        return self.us.pop(0)


def det(a):
    """The Leibniz formula, independent of the elimination in solve."""
    size = len(a)
    total = F(0)
    for perm in itertools.permutations(range(size)):
        inv = sum(1 for i in range(size) for j in range(i + 1, size) if perm[i] > perm[j])
        term = F(-1) ** inv
        for i in range(size):
            term *= a[i][perm[i]]
        total += term
    return total


def cramer(a, b):
    d = det(a)
    if d == 0:
        return None
    out = []
    for c in range(len(a)):
        m = [[b[i] if j == c else a[i][j] for j in range(len(a))] for i in range(len(a))]
        out.append(det(m) / d)
    return out


def random_matrix(rng, size):
    rows = []
    for _ in range(size):
        w = [rng.randint(0, 6) for _ in range(size)]
        if sum(w) == 0:
            w[rng.randrange(size)] = 1
        rows.append([F(x, sum(w)) for x in w])
    return rows


def test_page_example() -> None:
    assert transpose_times(P3, [50, 30, 20]) == [43, 33, 24]
    released = [0] * 45 + [1] * 31 + [2] * 24
    assert estimate(released, P3) == [F(370, 7), F(190, 7), F(20)]
    assert estimate([0] * 43 + [1] * 33 + [2] * 24, P3) == [50, 30, 20]
    r = invariant_matrix(RR, [60, 20])
    assert r == [[F(4, 5), F(1, 5)], [F(3, 5), F(2, 5)]]
    assert transpose_times(r, [60, 20]) == [60, 20]
    assert ldp_ratio(RR) == 3
    assert ldp_ratio(r) == 2
    assert ldp_ratio(P3) is None


def test_sampling_boundaries() -> None:
    # Row 0 of P3 has the cumulative sums 4/5, 9/10, 1.
    assert pram([0, 0, 0, 0, 0], P3, Fixed([0.0, 0.79, 0.8, 0.85, 0.9])) == [0, 0, 1, 1, 2]
    # A zero entry is never chosen.
    assert pram([2, 2], P3, Fixed([0.0, 0.19])) == [1, 1]
    assert pram([], P3, Fixed([])) == []


def test_bad_matrix() -> None:
    with pytest.raises(ValueError):
        check_matrix([[F(1, 2), F(1, 3)], [F(1, 2), F(1, 2)]])
    with pytest.raises(ValueError):
        check_matrix([[F(3, 2), F(-1, 2)], [F(0), F(1)]])
    with pytest.raises(ValueError):
        check_matrix([[F(1)], [F(1)]])
    assert solve([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]], [1, 1]) is None
    assert estimate([0, 1], [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]) is None


def test_against_oracles() -> None:
    rng = random.Random(1998)
    for _ in range(600):
        size = rng.randint(1, 3)
        p = random_matrix(rng, size)
        t = [rng.randint(0, 9) for _ in range(size)]
        pt = [[p[k][l] for k in range(size)] for l in range(size)]
        t_star = [rng.randint(0, 9) for _ in range(size)]
        released = [l for l in range(size) for _ in range(t_star[l])]
        rng.shuffle(released)
        assert counts(released, size) == t_star
        assert estimate(released, p) == cramer(pt, t_star)
        if det(pt) != 0:
            expected = transpose_times(p, t)
            assert solve(pt, expected) == t
        if sum(t) > 0:
            r = invariant_matrix(p, t)
            assert all(sum(row) == 1 and min(row) >= 0 for row in r)
            assert transpose_times(r, t) == t
        ratio = ldp_ratio(p)
        pairs = [(p[a][l], p[b][l]) for a in range(size) for b in range(size) for l in range(size)]
        if any(x > 0 and y == 0 for x, y in pairs):
            assert ratio is None
        else:
            assert ratio == max([F(1)] + [x / y for x, y in pairs if y > 0])


def test_sampling_matches_inverse_cdf() -> None:
    rng = random.Random(4)
    for _ in range(500):
        size = rng.randint(1, 4)
        p = random_matrix(rng, size)
        values = [rng.randrange(size) for _ in range(rng.randint(0, 8))]
        seed = rng.randrange(10**9)
        got = pram(values, p, random.Random(seed))
        twin = random.Random(seed)
        want = []
        for k in values:
            u = twin.random()
            cum = list(itertools.accumulate(p[k]))
            want.append(min(l for l in range(size) if cum[l] > u))
        assert got == want


def test_frequencies() -> None:
    # 2000 draws from row 0 of P3. By the Hoeffding inequality, each frequency is
    # within 0.05 of its probability except with probability 2 exp(-10) < 1e-4.
    out = pram([0] * 2000, P3, random.Random(77))
    for l, p in enumerate(P3[0]):
        assert abs(out.count(l) / 2000 - float(p)) < 0.05
    # The estimate from a large release is close to the truth.
    truth = [0] * 1000 + [1] * 600 + [2] * 400
    t_hat = estimate(pram(truth, P3, random.Random(5)), P3)
    assert all(abs(float(a) - b) < 60 for a, b in zip(t_hat, [1000, 600, 400]))
