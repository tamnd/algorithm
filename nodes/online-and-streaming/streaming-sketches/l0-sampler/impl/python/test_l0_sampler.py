# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l0-sampler/. The authors are listed in prov/QSH7SV.jsonl.

import itertools
import random
from collections import Counter

from l0_sampler import EMPTY, FAIL, MANY, P, ZERO, L0Sampler, decode

UPDATES = [(2, 3), (5, 1), (7, 2), (4, -1), (5, -1), (6, 5), (6, -5)]


def test_worked_example() -> None:
    s = L0Sampler(8, 0.5, random.Random(0))
    assert s.copies == 2 and s.levels == 5
    assert [s.level_of(0, i) for i in range(1, 9)] == [1, 2, 1, 0, 3, 1, 1, 1]
    for i, d in UPDATES:
        s.update(i, d)
    x = {2: 3, 4: -1, 7: 2}
    s.check_invariant(x)
    assert [(c.a, c.b) for c in s.cells[0]] == [(4, 16), (5, 20), (3, 6), (0, 0), (0, 0), (0, 0)]
    z = s.zs[0]
    # levels 0 and 1 have B / A = 4, an integer in range, but the fingerprint rejects them
    assert decode(4, 16, s.cells[0][0].c, 8, z) == MANY
    assert decode(5, 20, s.cells[0][1].c, 8, z) == MANY
    assert s.cells[0][3].c == 0  # coordinate 5 went up and down again
    assert s.query() == (2, 3)


def test_one_sparse_test_exactly() -> None:
    # Every vector in {-1, 0, 1, 2}^5 and every base z modulo the prime 101.
    q, n = 101, 5
    for y in itertools.product([-1, 0, 1, 2], repeat=n):
        nz = [(i + 1, v) for i, v in enumerate(y) if v]
        wrong = 0
        for z in range(q):
            a = sum(v for _, v in nz)
            b = sum(i * v for i, v in nz)
            c = sum(v * pow(z, i, q) for i, v in nz) % q
            r = decode(a, b, c, n, z, q)
            if not nz:
                assert r == ZERO
            elif len(nz) == 1:
                assert r == nz[0]
            elif r != MANY:
                wrong += 1
        assert wrong <= n  # at most n bad bases out of q, the bound n / q


def test_edges() -> None:
    s = L0Sampler(10, 0.1, random.Random(3))
    assert s.query() == EMPTY
    s.update(10, -7)
    assert s.query() == (10, -7)
    s.update(10, 7)
    assert s.query() == EMPTY
    s.check_invariant({})


def test_random_turnstile_streams() -> None:
    rng = random.Random(2011)
    fails = 0
    for trial in range(500):
        n = rng.randint(1, 200)
        s = L0Sampler(n, 0.05, random.Random(trial))
        x: dict = {}
        for _ in range(rng.randint(0, 40)):
            i = rng.randint(1, n)
            d = rng.choice([-3, -2, -1, 1, 2, 3])
            s.update(i, d)
            x[i] = x.get(i, 0) + d
        if rng.random() < 0.3:  # delete everything again
            for i, v in list(x.items()):
                s.update(i, -v)
                x[i] = 0
        if trial < 40:
            s.check_invariant(x)
        r = s.query()
        support = {i for i, v in x.items() if v}
        if not support:
            assert r == EMPTY
        elif r == FAIL:
            fails += 1
        else:
            i, v = r
            assert i in support and x[i] == v
    assert fails <= 0.05 * 500


def test_linearity() -> None:
    rng = random.Random(9)
    a = L0Sampler(50, 0.1, random.Random(1))
    b = a.copy_empty()
    xa, xb = Counter(), Counter()
    for _ in range(30):
        i, d = rng.randint(1, 50), rng.choice([-1, 1, 2])
        a.update(i, d)
        xa[i] += d
        j, e = rng.randint(1, 50), rng.choice([-1, 1, 2])
        b.update(j, e)
        xb[j] += e
    a.add(b)
    total = {i: xa[i] + xb[i] for i in set(xa) | set(xb)}
    a.check_invariant(total)
    r = a.query()
    assert r == FAIL or total[r[0]] == r[1]


def test_output_is_close_to_uniform() -> None:
    support = [3, 17, 42, 77, 99]
    counts: Counter = Counter()
    for seed in range(1500):
        s = L0Sampler(100, 0.05, random.Random(seed))
        for i in support:
            s.update(i, 1)
        s.update(50, 4)
        s.update(50, -4)
        r = s.query()
        if r != FAIL:
            counts[r[0]] += 1
    total = sum(counts.values())
    assert set(counts) <= set(support)
    for i in support:
        assert abs(counts[i] / total - 0.2) <= 0.04
    assert P > 10**18
