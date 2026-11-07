# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-wiedemann-algorithm/. The authors are listed in prov/0EQBTW.jsonl.

import random

from block_wiedemann_algorithm import apply_vector, block_wiedemann_kernel, minimal_generator


def rank_mod_p(dense, p):
    m = [row[:] for row in dense]
    n = len(m[0]) if m else 0
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, len(m)) if m[i][c] % p), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = pow(m[r][c], -1, p)
        for i in range(len(m)):
            if i != r and m[i][c] % p:
                f = m[i][c] * inv % p
                m[i] = [(x - f * y) % p for x, y in zip(m[i], m[r])]
        r += 1
    return r


def to_dense(rows, n):
    d = [[0] * n for _ in rows]
    for i, r in enumerate(rows):
        for j, a in r:
            d[i][j] = a
    return d


def random_sparse(rng, n, p, per_row):
    return [sorted((j, rng.randrange(1, p)) for j in rng.sample(range(n), min(per_row, n))) for _ in range(n)]


def make_singular(rng, rows, n, p):
    rows = [list(r) for r in rows]
    if n == 1:
        return [[]]
    i, k = rng.sample(range(n), 2)
    c = rng.randrange(1, p)
    di, dk = dict(rows[i]), dict(rows[k])
    comb = {j: (di.get(j, 0) + c * dk.get(j, 0)) % p for j in set(di) | set(dk)}
    rows[i] = sorted((j, v) for j, v in comb.items() if v)
    rows[k] = rows[k]
    t = rng.randrange(n)
    if t not in (i, k):
        rows[t] = list(rows[i])  # sometimes a second dependency
    return rows


def check_kernel(rows, n, p, u):
    assert len(u) == n and any(u)
    assert all(0 <= x < p for x in u)
    assert not any(apply_vector(rows, u, p))


def test_generator_property() -> None:
    rng = random.Random(1994)
    for _ in range(40):
        p = rng.choice([2, 3, 101, 65521])
        s = rng.randint(1, 3)
        n = rng.randint(1, 10)
        a = random_sparse(rng, n, p, 3)
        x = [[rng.randrange(p) for _ in range(s)] for _ in range(n)]
        v = [[rng.randrange(p) for _ in range(s)] for _ in range(n)]
        seq = []
        for _ in range(2 * (-(-n // s)) + 4):
            seq.append([[sum(x[r][i] * v[r][c] for r in range(n)) % p for c in range(s)] for i in range(s)])
            v = [[sum(val * v[j][c] for j, val in row) % p for c in range(s)] for row in a]
        gens = minimal_generator(seq, s, p)
        assert gens and [d for d, _ in gens] == sorted(d for d, _ in gens)
        big_l = len(seq)
        for d, f in gens:
            assert any(any(fj) for fj in f)
            for i in range(big_l - d):
                for r in range(s):
                    assert sum(seq[i + j][r][c] * f[j][c] for j in range(d + 1) for c in range(s)) % p == 0


def test_edges() -> None:
    assert block_wiedemann_kernel([], 0, 7) is None
    u = block_wiedemann_kernel([[]], 1, 7)
    assert u is not None and u[0] != 0
    assert block_wiedemann_kernel([[(0, 3)]], 1, 7) is None
    zero = [[] for _ in range(5)]
    check_kernel(zero, 5, 2, block_wiedemann_kernel(zero, 5, 2, s=2))
    a = [[(1, 1)], [(0, 1)], []]  # zero row and zero column
    check_kernel(a, 3, 5, block_wiedemann_kernel(a, 3, 5, s=2))
    nilp = [[(i + 1, 1)] if i + 1 < 6 else [] for i in range(6)]  # shift matrix, A^5 != 0
    check_kernel(nilp, 6, 101, block_wiedemann_kernel(nilp, 6, 101, s=2))


def test_random_singular_and_nonsingular() -> None:
    rng = random.Random(2002)
    found = total = 0
    for trial in range(500):
        p = [2, 3, 101, 65521][trial % 4]
        s = [1, 2, 4][trial % 3]
        n = rng.randint(1, 16)
        a = random_sparse(rng, n, p, rng.randint(1, 4))
        if rng.random() < 0.6:
            a = make_singular(rng, a, n, p)
        singular = rank_mod_p(to_dense(a, n), p) < n
        u = block_wiedemann_kernel(a, n, p, s=s, seed=trial, tries=3)
        if not singular:
            assert u is None
        else:
            total += 1
            if u is not None:
                check_kernel(a, n, p, u)
                found += 1
            elif p > 3:
                raise AssertionError((p, s, n))
    assert found >= 0.95 * total


def test_larger() -> None:
    rng = random.Random(7)
    for p, s in ((2, 8), (65521, 4)):
        n = 120
        a = make_singular(rng, random_sparse(rng, n, p, 5), n, p)
        check_kernel(a, n, p, block_wiedemann_kernel(a, n, p, s=s, seed=1))


def test_example() -> None:
    from block_wiedemann_algorithm import apply_block
    p, n, s = 7, 4, 2
    dense = [[1, 2, 0, 1], [0, 1, 3, 0], [1, 3, 3, 1], [2, 0, 0, 1]]
    rows = [[(j, a) for j, a in enumerate(r) if a] for r in dense]
    x = [[1, 0], [0, 1], [0, 0], [0, 0]]
    z = [[0, 0], [0, 0], [1, 0], [0, 1]]
    v = apply_block(rows, z, p)
    assert v == [[0, 1], [3, 0], [3, 1], [0, 1]]
    seq = []
    for _ in range(8):
        seq.append([[sum(x[r][a] * v[r][c] for r in range(n)) % p for c in range(s)] for a in range(s)])
        v = apply_block(rows, v, p)
    assert seq[:4] == [[[0, 1], [3, 0]], [[6, 2], [5, 3]], [[2, 4], [3, 4]], [[6, 5], [4, 0]]]
    d, f = minimal_generator(seq, s, p)[0]
    assert (d, f) == (1, [[6, 1], [5, 2]])
    az = apply_block(rows, z, p)
    u = [(z[r][0] * 6 + z[r][1] * 1 + az[r][0] * 5 + az[r][1] * 2) % p for r in range(n)]
    assert u == [2, 1, 2, 3] and not any(apply_vector(rows, u, p))
