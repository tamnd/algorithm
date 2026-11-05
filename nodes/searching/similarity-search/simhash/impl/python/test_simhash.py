# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simhash/. The authors are listed in prov/A430AD.jsonl.

import math
import random

from simhash import angle, default_hash, distance, simhash, simhash_gaussian

TABLE = {"the": 0b1010, "cat": 0b0110, "sat": 0b1100, "mat": 0b0011, "dog": 0b1001, "ran": 0b0101}


def test_example() -> None:
    h = TABLE.__getitem__
    a = simhash({"the": 1, "cat": 3, "sat": 1}, 4, h)
    b = simhash({"the": 1, "cat": 3, "mat": 1}, 4, h)
    c = simhash({"dog": 2, "ran": 1}, 4, h)
    assert (a, b, c) == (0b0110, 0b0110, 0b1001)
    assert distance(a, b) == 0 and distance(a, c) == 4
    assert abs(math.degrees(angle({"the": 1, "cat": 3, "sat": 1}, {"the": 1, "cat": 3, "mat": 1})) - 24.62) < 0.01


def test_edges() -> None:
    assert simhash({}, 64) == 0
    assert distance(0, (1 << 64) - 1) == 64
    x = {"a": 1.0, "b": 2.0, "c": 0.5}
    assert simhash(x) == simhash({f: 7 * w for f, w in x.items()})
    assert simhash(x) == simhash(dict(reversed(list(x.items()))))


def oracle(weights, b, h) -> int:
    fp = 0
    for i in range(b):
        pos = sum(w for f, w in weights.items() if (h(f) >> (b - 1 - i)) & 1)
        neg = sum(w for f, w in weights.items() if not (h(f) >> (b - 1 - i)) & 1)
        fp = (fp << 1) | (1 if pos > neg else 0)
    return fp


def test_random_against_oracle() -> None:
    rng = random.Random(11)
    for t in range(600):
        b = rng.choice([1, 4, 8, 16, 64])
        h = default_hash(b, seed=t)
        doc = {f"w{rng.randint(0, 40)}": rng.randint(1, 5) for _ in range(rng.randint(0, 15))}
        assert simhash(doc, b, h) == oracle(doc, b, h)


def test_pm_one_counterexample() -> None:
    x, y = {1: 1.0}, {1: 1.0, 2: 1.0, 3: 1.0}
    rng = random.Random(5)
    disagree = 0
    trials = 4000
    for _ in range(trials):
        bits = {f: rng.getrandbits(1) for f in (1, 2, 3)}
        h = bits.__getitem__
        disagree += distance(simhash(x, 1, h), simhash(y, 1, h))
    assert abs(disagree / trials - 0.25) < 0.03
    assert abs(angle(x, y) / math.pi - 0.3041) < 1e-3


def test_gaussian_variant_matches_angle() -> None:
    x, y = {1: 1.0}, {1: 1.0, 2: 1.0, 3: 1.0}
    total = 0
    seeds = 300
    for s in range(seeds):
        total += distance(simhash_gaussian(x, 64, s), simhash_gaussian(y, 64, s))
    assert abs(total / (64 * seeds) - angle(x, y) / math.pi) < 0.02
