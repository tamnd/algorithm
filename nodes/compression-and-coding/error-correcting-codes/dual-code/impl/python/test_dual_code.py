# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-code/. The authors are listed in prov/WBZ251.jsonl.

import random
from itertools import product

from dual_code import dual_generator, inner, is_self_dual, is_self_orthogonal, rref

G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]


def span(g, q):
    k, n = len(g), len(g[0])
    return {tuple(sum(m[i] * g[i][j] for i in range(k)) % q for j in range(n)) for m in product(range(q), repeat=k)}


def weights(g, q=2):
    out = {}
    for c in span(g, q):
        w = sum(1 for x in c if x)
        out[w] = out.get(w, 0) + 1
    return dict(sorted(out.items()))


def golay24():
    g = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]  # 1 + x^2 + x^4 + x^5 + x^6 + x^10 + x^11
    rows = []
    for i in range(12):
        row = [0] * 23
        for j, b in enumerate(g):
            row[i + j] = b
        rows.append(row + [sum(row) % 2])
    return rows


def test_hamming_dual_is_simplex():
    d = dual_generator(G74)
    assert len(d) == 3
    assert weights(d) == {0: 1, 4: 7}
    assert is_self_orthogonal(d) and not is_self_dual(d)
    assert not is_self_orthogonal(G74)


def test_extended_hamming_self_dual():
    ext = [row + [sum(row) % 2] for row in G74]
    assert is_self_dual(ext)
    assert weights(ext) == {0: 1, 4: 14, 8: 1}
    assert span(dual_generator(ext), 2) == span(ext, 2)


def test_extended_golay_self_dual():
    g = golay24()
    assert len(rref(g, 2)[1]) == 12
    assert is_self_dual(g)
    assert weights(g) == {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}


def test_small_examples():
    assert is_self_dual([[1, 1]])
    assert is_self_dual([[1, 0, 1, 1], [0, 1, 1, 2]], 3)  # the ternary tetracode
    assert not is_self_dual([[1, 1, 1]])
    rep = [[1, 1, 1, 1]]
    d = dual_generator(rep)
    assert span(d, 2) == {v for v in product(range(2), repeat=4) if sum(v) % 2 == 0}


def test_random_codes_against_brute_force():
    rng = random.Random(33)
    done = 0
    while done < 150:
        q = rng.choice([2, 2, 3])
        n = rng.randint(2, 8 if q == 2 else 5)
        k = rng.randint(1, n)
        g = [[rng.randrange(q) for _ in range(n)] for _ in range(k)]
        if len(rref(g, q)[1]) < k:
            continue
        d = dual_generator(g, q)
        assert len(d) == n - k
        want = {v for v in product(range(q), repeat=n) if all(inner(list(v), row, q) == 0 for row in g)}
        got = span(d, q) if d else {(0,) * n}
        assert got == want
        if d:
            assert span(dual_generator(d, q), q) == span(g, q)
        done += 1
