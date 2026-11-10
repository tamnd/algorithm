# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kll-sketch/. The authors are listed in prov/1FW1M3.jsonl.

import bisect
import math
import random
from fractions import Fraction

from kll_sketch import KLLSketch, k_for


class ScriptedBits:
    """A stand-in for random.Random that returns a fixed list of bits."""

    def __init__(self, bits: list[int]) -> None:
        self.bits = bits
        self.i = 0

    def getrandbits(self, _: int) -> int:
        b = self.bits[self.i]
        self.i += 1
        return b


def build(stream: list, k: int, rng) -> KLLSketch:
    s = KLLSketch(k, rng)
    for x in stream:
        s.insert(x)
        s.check_invariant()
    return s


def test_worked_example() -> None:
    stream = [9, 2, 14, 5, 11, 7, 1, 16, 4, 12, 6, 15, 3, 10, 8, 13]
    s = build(stream, 5, ScriptedBits([0, 1, 0, 1, 0]))
    assert s.levels == [[10, 13], [3], [4, 9, 16]]
    assert s.compactions == [4, 1, 0]
    assert [s.rank(x) for x in range(1, 17)] == [0, 0, 2, 6, 6, 6, 6, 6, 10, 11, 11, 11, 12, 12, 12, 16]
    assert s.variance_bound() == 8
    assert [s.query(r) for r in (4, 8, 12)] == [4, 9, 13]


def test_unbiased_exactly_by_enumeration() -> None:
    rng = random.Random(3)
    for trial in range(25):
        n = rng.randint(1, 14)
        k = rng.randint(2, 5)
        stream = [rng.randint(0, 9) for _ in range(n)]
        m = sum(build(stream, k, ScriptedBits([0] * 64)).compactions)
        assert m <= 12
        total = {x: Fraction(0) for x in range(-1, 11)}
        second = Fraction(0)
        for mask in range(1 << m):
            bits = [(mask >> i) & 1 for i in range(m)]
            s = build(stream, k, ScriptedBits(bits))
            for x in total:
                total[x] += s.rank(x)
            err = s.rank(4) - sum(1 for y in stream if y <= 4)
            second += err * err
            v = s.variance_bound()
        for x, t in total.items():
            assert t / (1 << m) == sum(1 for y in stream if y <= x)
        assert second / (1 << m) <= v  # the variance is at most the proxy V


def test_error_distribution_seeded() -> None:
    n, k, trials = 2000, 40, 120
    rng = random.Random(2016)
    data_rng = random.Random(7)
    stream = [data_rng.random() for _ in range(n)]
    data = sorted(stream)
    probe = data[n // 2 - 1]
    errors = []
    v_max = 0
    for _ in range(trials):
        s = build_fast(stream, k, rng)
        errors.append(s.rank(probe) - n // 2)
        v_max = max(v_max, s.variance_bound())
        assert s.size() <= 3 * k + 2 * len(s.levels)
    mean = sum(errors) / trials
    var = sum(e * e for e in errors) / trials
    assert abs(mean) <= 4 * math.sqrt(v_max / trials)
    assert var <= 1.5 * v_max
    for t in (1, 1.5, 2, 2.5):
        thr = t * math.sqrt(v_max)
        bad = sum(1 for e in errors if abs(e) >= thr)
        assert bad / trials <= 2 * math.exp(-t * t / 2) + 0.05
    assert v_max <= 16 * n * n / (k * k)


def build_fast(stream: list, k: int, rng: random.Random) -> KLLSketch:
    s = KLLSketch(k, rng)
    for x in stream:
        s.insert(x)
    s.check_invariant()
    return s


def test_failure_rate_against_delta() -> None:
    eps, delta = 0.1, 0.2
    k = k_for(eps, delta)
    n, trials = 3000, 40
    rng = random.Random(99)
    stream = list(range(n))
    random.Random(1).shuffle(stream)
    fails = 0
    for _ in range(trials):
        s = build_fast(stream, k, rng)
        worst = max(abs(s.rank(x) - (x + 1)) for x in range(0, n, 97))
        if worst > eps * n:
            fails += 1
    assert fails / trials <= delta


def test_quantiles_merge_and_edges() -> None:
    rng = random.Random(5)
    s = KLLSketch(8, rng)
    s.insert(42)
    assert s.query(1) == 42 and s.rank(41) == 0 and s.rank(42) == 1
    for trial in range(500):
        k = rng.randint(2, 30)
        a = [rng.randint(0, 50) for _ in range(rng.randint(1, 60))]
        b = [rng.randint(0, 50) for _ in range(rng.randint(1, 60))]
        sa, sb = build_fast(a, k, rng), build_fast(b, k, rng)
        sa.merge(sb)
        sa.check_invariant()
        assert sa.n == len(a) + len(b)
        data = sorted(a + b)
        r = rng.randint(1, sa.n)
        v = sa.query(r)
        assert v in data
        # the deterministic part: weights add up and the rank is within the worst-case sum
        worst = sum(m << h for h, m in enumerate(sa.compactions))
        assert abs(sa.rank(v) - bisect.bisect_right(data, v)) <= worst
