# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rainbow-table/. The authors are listed in prov/W2QHWJ.jsonl.

import math
import random

from rainbow_table import HellmanTables, RainbowTable, build_rainbow, rainbow_success, toy_oneway

N_BITS = 18
T = 64  # chain length
M = 64  # chains per Hellman table; m t^2 = N
ELL = 64  # Hellman tables; the rainbow table has M * ELL chains


def f(x: int) -> int:
    return toy_oneway(x, N_BITS)


def test_rainbow_against_hellman_same_memory() -> None:
    rng = random.Random(2003)
    rt = build_rainbow(f, N_BITS, M * ELL, T, random.Random(1))
    ht = HellmanTables(f, N_BITS, M, T, ELL, random.Random(2))
    assert rt.f_calls == ht.f_calls == M * T * ELL  # same precomputation
    assert len(rt.ends) <= M * ELL
    rt.f_calls = ht.f_calls = 0
    trials = 80
    ok_r = ok_h = 0
    for _ in range(trials):
        y = f(rng.randrange(1 << N_BITS))
        xr = rt.lookup(y)
        xh = ht.lookup(y)
        if xr is not None:
            assert f(xr) == y
            ok_r += 1
        if xh is not None:
            assert f(xh) == y
            ok_h += 1
    # Oechslin's formula is the chance that the point x itself is covered; a
    # lookup of y = f(x) may also find another preimage of y, so it succeeds more often.
    p = rainbow_success(N_BITS, M * ELL, T)
    assert ok_r / trials >= p - 4 * math.sqrt(p * (1 - p) / trials)
    # comparable success, but far fewer table lookups and fewer calls of f
    assert ok_r >= ok_h - 12
    assert rt.lookups * 10 < ht.lookups
    assert rt.f_calls < ht.f_calls


def test_coverage_matches_oechslin_formula() -> None:
    n, t, m = 16, 32, 1024
    g = lambda x: toy_oneway(x, n, key=11)  # noqa: E731
    fracs, kept = [], []
    for seed in range(5):
        rng = random.Random(seed)
        starts = [rng.randrange(1 << n) for _ in range(m)]
        rt = RainbowTable(g, n, t)
        covered_all, covered_kept = set(), set()
        for s in starts:
            rt.add_chain(s)
            x = s
            for j in range(t):
                covered_all.add(x)
                x = rt.reduce(j, g(x))
        for s in rt.ends.values():
            x = s
            for j in range(t):
                covered_kept.add(x)
                x = rt.reduce(j, g(x))
        fracs.append(len(covered_all) / (1 << n))
        kept.append(len(covered_kept) / (1 << n))
    mean = sum(fracs) / len(fracs)
    # the formula counts all m chains; keeping one chain per end point loses the
    # columns before the merge of the dropped chains
    assert abs(mean - rainbow_success(n, m, t)) < 0.01
    assert sum(kept) / len(kept) < mean


def test_lookup_cost_of_a_miss() -> None:
    # a point not in the table costs t(t-1)/2 calls of f plus false alarms, and t lookups
    rt = build_rainbow(f, N_BITS, 16, T, random.Random(3))
    rt.f_calls = rt.lookups = rt.false_alarms = 0
    y = f(12345)
    if rt.lookup(y) is None:
        assert rt.lookups == T
        assert rt.f_calls >= T * (T - 1) // 2


def test_invariant_and_model() -> None:
    rng = random.Random(9)
    n, t = 12, 8
    g = lambda x: toy_oneway(x, n, key=3)  # noqa: E731
    rt = RainbowTable(g, n, t)
    model: dict[int, int] = {}  # end -> start, by direct computation
    for _ in range(500):
        s = rng.randrange(1 << n)
        x = s
        for j in range(t):
            x = (g(x) ^ (j * 0x9E3779B1)) & ((1 << n) - 1)
        added = rt.add_chain(s)
        assert added == (x not in model)
        model.setdefault(x, s)
        assert rt.ends == model
    assert rt.check_invariant()
    # every point on a stored chain (columns 0 .. t-1) is found
    for end, start in list(rt.ends.items())[:50]:
        x = start
        for j in range(t):
            z = rt.lookup(g(x))
            assert z is not None and g(z) == g(x)
            x = rt.reduce(j, g(x))


def test_success_formula_edges() -> None:
    assert rainbow_success(10, 0, 5) == 0.0
    assert abs(rainbow_success(10, 1, 1) - 1 / 1024) < 1e-12
