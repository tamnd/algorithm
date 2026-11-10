# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossy-counting/. The authors are listed in prov/1P92W2.jsonl.

import random
from collections import Counter
from fractions import Fraction

import pytest

from lossy_counting import LossyCounting


def harmonic(b: int) -> Fraction:
    return sum((Fraction(1, i) for i in range(1, b + 1)), Fraction(0))


def check(lc: LossyCounting, freq: Counter, universe) -> None:
    n, w = lc.n, lc.w
    b_cur = -(-n // w)
    done = n // w  # completed buckets
    for x in lc.f:
        assert lc.f[x] >= 1
        assert lc.delta[x] <= b_cur - 1
        assert lc.f[x] <= freq[x] <= lc.f[x] + lc.delta[x]
    for x in set(universe) | set(freq):
        est = lc.estimate(x)
        assert est <= freq[x] <= lc.upper(x)
        assert freq[x] - est <= n // w
        if x not in lc.f:
            assert freq[x] <= done
    # Space: w * H_B right after a pruning, plus at most the entries of the open bucket.
    if n % w == 0:
        assert len(lc) <= w * harmonic(done)
    else:
        assert len(lc) <= w * harmonic(done) + (n - done * w)
    for s in (Fraction(1, 2), Fraction(1, 5), Fraction(1, 10), Fraction(2, w + 1)):
        if s <= Fraction(1, w):
            continue  # the guarantee needs a support s larger than eps
        rep = set(lc.report(s))
        for x, c in freq.items():
            if c >= s * n:
                assert x in rep
            if c < (s - Fraction(1, w)) * n:
                assert x not in rep


def run_and_check(stream, w):
    lc = LossyCounting(w=w)
    freq = Counter()
    universe = set(stream)
    for x in stream:
        lc.update(x)
        freq[x] += 1
        check(lc, freq, universe)
    return lc, freq


def test_example() -> None:
    lc, freq = run_and_check(list("abacabdab"), 3)
    assert lc.f == {"a": 4}
    assert lc.delta == {"a": 0}
    assert lc.estimate("b") == 0 and freq["b"] == 3  # low by exactly 9 // 3
    lc2 = LossyCounting(w=3)
    lc2.extend("abacabda")  # stop before the last pruning
    assert lc2.f == {"d": 1, "a": 4} and lc2.delta == {"d": 2, "a": 0}


def test_width_from_eps() -> None:
    assert LossyCounting(Fraction(1, 3)).w == 3
    assert LossyCounting(Fraction(2, 7)).w == 4
    assert LossyCounting(0.1).w == 10
    assert LossyCounting(1).w == 1
    with pytest.raises(ValueError):
        LossyCounting(0)
    with pytest.raises(ValueError):
        LossyCounting()


def test_edges() -> None:
    run_and_check([], 3)
    run_and_check([1], 1)
    run_and_check([1, 2, 3, 1, 1], 1)
    run_and_check([5] * 40, 4)
    run_and_check(list(range(40)), 4)


def adversarial_streams(w):
    yield list(range(w + 1)) * 8  # round robin, each item just misses the pruning
    yield [i % (2 * w) for i in range(12 * w)]
    yield [0] * (3 * w) + list(range(1, 6 * w))  # heavy first, then all new
    yield list(range(1, 6 * w)) + [0] * (3 * w)  # heavy last
    # Item j occurs once in each of the buckets j, j+1, ...: entries pile up.
    s = []
    for b in range(1, 10):
        s.extend(range(b))
        s.extend(1000 + 100 * b + i for i in range(max(0, w - b)))
    yield s


def test_adversarial_streams() -> None:
    for w in range(1, 8):
        for s in adversarial_streams(w):
            run_and_check(s, w)


def test_seeded_streams_every_query() -> None:
    rng = random.Random(1234)
    for _ in range(250):
        w = rng.randrange(1, 9)
        n = rng.randrange(1, 30)
        m = rng.randrange(0, 80)
        weights = [rng.random() ** 4 for _ in range(n)]
        s = rng.choices(range(n), weights=weights, k=m)
        run_and_check(s, w)


def test_space_on_a_longer_stream() -> None:
    rng = random.Random(7)
    w = 20
    lc = LossyCounting(w=w)
    for t in range(4000):
        # A mix of a few heavy items and a long tail of new items.
        lc.update(rng.randrange(5) if rng.random() < 0.3 else rng.randrange(10**6))
        if lc.n % w == 0:
            assert len(lc) <= w * harmonic(lc.n // w)
    assert len(lc) < 4000 // 4
