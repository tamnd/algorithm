# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/galil-seiferas/. The authors are listed in prov/7W7A4V.jsonl.

import itertools
import random

from galil_seiferas import factorize, galil_seiferas


def oracle(t, p) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t[s : s + len(p)] == p]


def smallest_period(w) -> int:
    for d in range(1, len(w) + 1):
        if all(w[i] == w[i + d] for i in range(len(w) - d)):
            return d
    return len(w)


def reach(v, p: int) -> int:
    length = p
    while length < len(v) and v[length] == v[length - p]:
        length += 1
    return length


def prefix_periods(v, k: int) -> list[int]:
    return [
        p
        for p in range(1, len(v) + 1)
        if reach(v, p) >= k * p and smallest_period(v[:p]) == p
    ]


def structured(rng: random.Random, depth: int) -> str:
    if depth == 0:
        return "".join(rng.choice("ab") for _ in range(rng.randint(1, 3)))
    w = structured(rng, depth - 1)
    return w * rng.randint(1, 6) + structured(rng, depth - 1)[: rng.randint(0, 3)]


def check_factorization(x: str, k: int) -> None:
    stats: dict = {}
    s, p1, q1 = factorize(x, k, stats)
    v = x[s:]
    assert len(v) >= 1
    pps = prefix_periods(v, k)
    assert len(pps) <= 1 and (not pps or pps[0] == p1), (x, k)
    assert reach(v, p1) == p1 + q1, (x, k)
    assert smallest_period(v[: p1 + q1]) == p1, (x, k)
    assert stats["exit"] != "L27", (x, k)  # the guard never fires on these inputs


def test_example() -> None:
    assert factorize("gcagagag") == (0, 7, 1)
    stats: dict = {}
    assert galil_seiferas("gcatcgcagagagtatacagtacg", "gcagagag", stats=stats) == [5]
    assert stats["comparisons"] == 21


def test_factorization_with_parse() -> None:
    p = "aaaab" * 4
    assert factorize(p) == (1, 5, 14)
    stats: dict = {}
    assert galil_seiferas("a" + p + "aaaabb", p, stats=stats) == [1, 6]
    assert stats["comparisons"] == 30


def test_factorization_exhaustive() -> None:
    for k in (3, 4, 5):
        for sigma, top in (("ab", 13), ("abc", 8)):
            for length in range(1, top):
                for w in itertools.product(sigma, repeat=length):
                    check_factorization("".join(w), k)
    rng = random.Random(7)
    for _ in range(3000):
        x = structured(rng, rng.randint(1, 3))[:80]
        for k in (3, 4):
            check_factorization(x, k)


def test_edges() -> None:
    assert galil_seiferas("abc", "") == [0, 1, 2, 3]
    assert galil_seiferas("", "") == [0]
    assert galil_seiferas("", "a") == []
    assert galil_seiferas("ab", "abc") == []
    assert galil_seiferas("a" * 10, "a" * 4) == list(range(7))
    assert galil_seiferas("a" * 10, "baaa") == []
    assert galil_seiferas([1, 2, 1, 2, 1], [1, 2, 1]) == [0, 2]


def test_periodic_input_is_linear() -> None:
    stats: dict = {}
    assert galil_seiferas("a" * 1000, "a" * 10, stats=stats) == list(range(991))
    assert stats["comparisons"] == 1000
    p = "aaaab" * 4
    t = "aaaab" * 200
    assert galil_seiferas(t, p, stats=stats) == oracle(t, p)
    assert stats["comparisons"] <= 5 * len(t)


def test_comparison_bound() -> None:
    rng = random.Random(3)
    for _ in range(1500):
        x = structured(rng, rng.randint(1, 3))[:40]
        t = (x * rng.randint(1, 5))[rng.randint(0, 5) :] + structured(rng, 2)
        t = "".join(c if rng.random() > 0.03 else rng.choice("ab") for c in t) * 2
        for k in (3, 4, 5):
            stats: dict = {}
            assert galil_seiferas(t, x, k, stats) == oracle(t, x)
            if len(x) <= len(t):
                assert stats["comparisons"] <= 5 * len(t), (t, x, k)
    for n in range(1, 11):
        for m in range(1, min(n, 5) + 1):
            for t in itertools.product("ab", repeat=n):
                for p in itertools.product("ab", repeat=m):
                    stats = {}
                    assert galil_seiferas(t, p, stats=stats) == oracle(t, p)
                    assert stats["comparisons"] <= 5 * n


def test_random_against_oracle() -> None:
    rng = random.Random(20240607)
    for sigma in ("a", "ab", "abcd"):
        for _ in range(700):
            n = rng.randint(0, 40)
            m = rng.randint(0, 12)
            t = "".join(rng.choice(sigma) for _ in range(n))
            p = "".join(rng.choice(sigma) for _ in range(m))
            if rng.random() < 0.3 and n:
                start = rng.randint(0, n - 1)
                p = t[start : start + m]
            for k in (3, 4):
                assert galil_seiferas(t, p, k) == oracle(t, p), (t, p, k)


def test_long_pattern() -> None:
    p = list(range(5000))
    assert factorize(p) == (0, 5000, 0)
    t = [-1] * 100 + p + [7] * 50 + p
    assert galil_seiferas(t, p) == [100, 5150]
