# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kmv-sketch/. The authors are listed in prov/CKX5V3.jsonl.

import hashlib
import math
import random

from kmv_sketch import KMV, SCALE, intersection_estimate, jaccard_estimate, unit


def keyed_hash(seed: int):
    key = seed.to_bytes(8, "little")

    def h(x: object) -> int:
        d = hashlib.blake2b(repr(x).encode(), digest_size=8, key=key).digest()
        return int.from_bytes(d, "little")

    return h


def random_table(rng: random.Random):
    """A fully random hash, drawn lazily: each new item gets fresh random bits."""
    table: dict[object, int] = {}

    def h(x: object) -> int:
        if x not in table:
            table[x] = rng.getrandbits(64)
        return table[x]

    return h


def test_worked_example() -> None:
    def at(p: float) -> int:
        return int(p * SCALE) - 1

    table = {"a": at(0.62), "b": at(0.11), "c": at(0.85), "d": at(0.30), "e": at(0.47), "f": at(0.05)}
    s = KMV(3, table.__getitem__)
    s.add_all("abcadebf")
    assert [round(unit(y), 6) for y in s.values()] == [0.05, 0.11, 0.30]
    assert abs(s.estimate() - 2 / 0.30) < 1e-9
    small = KMV(10, table.__getitem__)
    small.add_all("abcadebf")
    assert small.estimate() == 6.0


def test_state_is_the_k_smallest_distinct_hashes() -> None:
    h = keyed_hash(1)
    rng = random.Random(2)
    for _ in range(30):
        k = rng.randrange(2, 40)
        xs = [rng.randrange(3000) for _ in range(rng.randrange(400))]
        s = KMV(k, h)
        s.add_all(xs)
        assert s.values() == sorted({h(x) for x in xs})[:k]


def test_merge_equals_sketch_of_union() -> None:
    h = keyed_hash(3)
    rng = random.Random(4)
    for _ in range(30):
        k = rng.randrange(2, 40)
        xs = [rng.randrange(3000) for _ in range(rng.randrange(400))]
        ys = [rng.randrange(3000) for _ in range(rng.randrange(400))]
        a, b, u = KMV(k, h), KMV(k, h), KMV(k, h)
        a.add_all(xs)
        b.add_all(ys)
        u.add_all(xs + ys + xs)
        assert a.merge(b).values() == u.values()
        assert a.merge(b).estimate() == u.estimate()


def test_estimator_is_unbiased_with_stated_variance() -> None:
    # (k - 1) / v_k is unbiased for d >= k, with variance d (d - k + 1) / (k - 2).
    rng = random.Random(5)
    d, k, trials = 1000, 64, 1500
    ests = []
    for _ in range(trials):
        s = KMV(k, lambda x: rng.getrandbits(64))
        s.add_all(range(d))
        ests.append(s.estimate())
    var = d * (d - k + 1) / (k - 2)
    mean = sum(ests) / trials
    sample_var = sum((e - mean) ** 2 for e in ests) / (trials - 1)
    # Tolerance: the mean within 4 standard errors of d; the sample variance within 20 percent.
    assert abs(mean - d) <= 4 * math.sqrt(var / trials)
    assert abs(sample_var / var - 1) < 0.2
    # The biased estimator k / v_k overshoots by about d / (k - 1).
    assert mean * k / (k - 1) - d > 2 * math.sqrt(var / trials)


def test_intersection_and_jaccard_estimates() -> None:
    rng = random.Random(6)
    k, trials = 64, 600
    a_items = list(range(0, 700))
    b_items = list(range(400, 1000))  # |A n B| = 300, |A u B| = 1000, J = 0.3
    inter, jac = [], []
    for _ in range(trials):
        h = random_table(rng)
        a, b = KMV(k, h), KMV(k, h)
        a.add_all(a_items)
        b.add_all(b_items)
        inter.append(intersection_estimate(a, b))
        jac.append(jaccard_estimate(a, b))
    for vals, truth in ((inter, 300.0), (jac, 0.3)):
        mean = sum(vals) / trials
        sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / (trials - 1))
        # Tolerance: 4 standard errors of the sample mean.
        assert abs(mean - truth) <= 4 * sd / math.sqrt(trials)


def test_exact_when_fewer_than_k() -> None:
    h = keyed_hash(7)
    a, b = KMV(50, h), KMV(50, h)
    a.add_all(range(20))
    b.add_all(range(10, 40))
    assert a.estimate() == 20.0
    assert a.merge(b).estimate() == 40.0
    assert intersection_estimate(a, b) == 10.0
    assert jaccard_estimate(a, b) == 10 / 40
