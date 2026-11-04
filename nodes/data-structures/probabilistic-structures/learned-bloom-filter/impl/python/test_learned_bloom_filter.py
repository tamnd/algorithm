# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learned-bloom-filter/. The authors are listed in prov/MC3EJT.jsonl.

import hashlib
import random
from collections.abc import Callable

import pytest

from learned_bloom_filter import Key, LearnedBloomFilter

S = [10, 20, 30, 40, 50, 7, 13]
BACKUP = {7: [1, 4], 13: [4, 6], 25: [1, 6], 33: [2, 4], 60: [0, 3]}


def sigma(x: Key) -> float:
    return 0.9 if int(x) % 10 == 0 else 0.2


class FixedLBF(LearnedBloomFilter):
    def _positions(self, key: Key, which: int) -> list[int]:
        return BACKUP[key]


def test_example() -> None:
    f = FixedLBF(S, sigma, 0.5, m_b=8, k_b=2)
    assert f.negatives == [7, 13]
    assert list(f.backup) == [0, 1, 0, 0, 1, 0, 1, 0]
    assert all(f.query(x) for x in S)
    assert f.query(60)  # a false positive of the classifier
    assert f.query(25)  # a false positive of the backup filter
    assert not f.query(33)
    fp_class = [x for x in range(100) if x not in S and sigma(x) >= 0.5]
    assert fp_class == [0, 60, 70, 80, 90]


def test_edges() -> None:
    f = LearnedBloomFilter([], sigma, 0.5, m_b=1, k_b=1)
    assert not f.query(3) and f.query(70)  # an empty set, but the classifier accepts 70
    g = LearnedBloomFilter([1, 2], lambda x: 1.0, 0.5, m_b=4, k_b=2, m_0=64, k_0=3)
    assert g.query(1) and g.query(2) and g.negatives == []
    with pytest.raises(ValueError):
        LearnedBloomFilter([1], sigma, 0.5, m_b=0, k_b=1)
    with pytest.raises(ValueError):
        LearnedBloomFilter([1], sigma, 0.5, m_b=4, k_b=1, m_0=8, k_0=0)


def noisy(seed: int, bias: float) -> Callable[[Key], float]:
    def score(x: Key) -> float:
        d = hashlib.blake2b(repr((seed, x)).encode(), digest_size=8).digest()
        u = int.from_bytes(d, "little") / 2**64
        return min(1.0, u + (bias if int(x) % 3 == 0 else 0.0))

    return score


def test_random_against_oracle() -> None:
    rng = random.Random(2018)
    for _ in range(500):
        keys = rng.sample(range(300), rng.randint(0, 40))
        score = noisy(rng.randrange(10**6), rng.random())
        tau = rng.random()
        m_b, k_b = rng.randint(1, 50), rng.randint(1, 4)
        m_0 = rng.choice([0, rng.randint(1, 80)])
        k_0 = rng.randint(1, 3)
        f = LearnedBloomFilter(keys, score, tau, m_b, k_b, m_0, k_0, seed=rng.randrange(100))
        neg = [x for x in keys if score(x) < tau]
        covered_b = {p for x in neg for p in f._positions(x, 1)}
        covered_0 = {p for x in keys for p in f._positions(x, 0)} if m_0 else set()
        for x in range(320):
            want = x in keys or (
                (not m_0 or set(f._positions(x, 0)) <= covered_0)
                and (score(x) >= tau or set(f._positions(x, 1)) <= covered_b)
            )
            assert f.query(x) == want


def test_rate_formula() -> None:
    keys = list(range(0, 30000, 3)) + list(range(1, 3000, 3))  # mostly multiples of 3
    score = noisy(7, 0.6)
    tau = 0.65
    f = LearnedBloomFilter(keys, score, tau, m_b=8 * 1500, k_b=6, seed=2)
    queries = [x for x in range(30000, 90000) if x % 3 != 0]  # non-keys of D
    fp_c = sum(score(x) >= tau for x in queries) / len(queries)
    eps_b = (sum(f.query(x) for x in queries if score(x) < tau) / sum(score(x) < tau for x in queries))
    total = sum(f.query(x) for x in queries) / len(queries)
    assert abs(total - (fp_c + (1 - fp_c) * eps_b)) < 1e-9
    assert 0.3 < fp_c < 0.4 and eps_b < 0.05
