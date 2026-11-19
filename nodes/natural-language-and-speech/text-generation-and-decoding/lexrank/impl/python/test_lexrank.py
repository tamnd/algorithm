# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lexrank/. The authors are listed in prov/EFQYD8.jsonl.

import math
import random
from fractions import Fraction

from lexrank import (
    idf_from_sentences,
    idf_modified_cosine,
    lexrank,
    lexrank_matrix,
    lexrank_summarize,
    power_method,
)


def stationary_exact(b, d):
    """Solve p = M^T p with sum(p) = 1 exactly, for M = d/n J + (1 - d) B (Fractions)."""
    n = len(b)
    m = [[d / n + (1 - d) * b[i][j] for j in range(n)] for i in range(n)]
    # Rows of the system: sum_i M[i][j] p_i - p_j = 0 for j < n - 1, and sum p = 1.
    rows = []
    for j in range(n - 1):
        rows.append([m[i][j] - (1 if i == j else 0) for i in range(n)] + [Fraction(0)])
    rows.append([Fraction(1)] * n + [Fraction(1)])
    for c in range(n):
        p = next(r for r in range(c, n) if rows[r][c] != 0)
        rows[c], rows[p] = rows[p], rows[c]
        for r in range(n):
            if r != c and rows[r][c] != 0:
                f = rows[r][c] / rows[c][c]
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[c])]
    return [rows[i][n] / rows[i][i] for i in range(n)]


def page_example():
    text = [
        "the storm hit the coast",
        "the storm flooded the coast roads",
        "flooded roads closed schools",
        "schools reopened after the storm",
    ]
    return [s.split() for s in text]


def threshold_graph(sentences, t, idf):
    n = len(sentences)
    return [[1 if i == j or idf_modified_cosine(sentences[i], sentences[j], idf) > t else 0
             for j in range(n)] for i in range(n)]


def test_cosine_formula():
    idf = {"a": 1.0, "b": 2.0, "c": 0.5}
    x = ["a", "b", "b"]
    y = ["b", "c"]
    num = 2 * 1 * 4.0
    nx = math.sqrt(1.0 + (2 * 2.0) ** 2)
    ny = math.sqrt(4.0 + 0.25)
    assert abs(idf_modified_cosine(x, y, idf) - num / (nx * ny)) < 1e-12
    assert abs(idf_modified_cosine(x, x, idf) - 1.0) < 1e-12
    assert idf_modified_cosine(["z"], x, idf) == 0.0
    assert idf_modified_cosine([], x, idf) == 0.0


def test_page_example():
    s = page_example()
    idf = idf_from_sentences(s)
    assert abs(idf["the"] - math.log(4 / 3)) < 1e-12
    assert abs(idf["hit"] - math.log(4)) < 1e-12
    assert abs(idf_modified_cosine(s[0], s[1], idf) - 0.3912) < 1e-4
    assert abs(idf_modified_cosine(s[1], s[2], idf) - 0.3847) < 1e-4
    assert abs(idf_modified_cosine(s[2], s[3], idf) - 0.1236) < 1e-4
    assert abs(idf_modified_cosine(s[0], s[3], idf) - 0.0698) < 1e-4
    assert idf_modified_cosine(s[0], s[2], idf) == 0.0
    b = lexrank_matrix(s, 0.1)
    assert b == [[0.5, 0.5, 0.0, 0.0], [1 / 3, 1 / 3, 1 / 3, 0.0],
                 [0.0, 1 / 3, 1 / 3, 1 / 3], [0.0, 0.0, 0.5, 0.5]]
    p, it = power_method(b, 0.15, 1e-8)
    want = [Fraction(43, 206), Fraction(30, 103), Fraction(30, 103), Fraction(43, 206)]
    assert all(abs(x - float(y)) < 1e-8 for x, y in zip(p, want))
    one, _ = power_method(b, 0.15, 0.0, max_iter=1)
    step = [Fraction(103, 480), Fraction(137, 480), Fraction(137, 480), Fraction(103, 480)]
    assert all(abs(x - float(y)) < 1e-12 for x, y in zip(one, step))
    assert lexrank_summarize(s, 1) == [1]
    assert lexrank_summarize(s, 2) == [1, 2]
    pc = lexrank(s, continuous=True)
    assert abs(sum(pc) - 1) < 1e-9 and pc[1] > pc[2] > pc[0] > pc[3]


def test_exact_stationary_threshold():
    rng = random.Random(457)
    vocab = ["w%d" % i for i in range(7)]
    d = Fraction(3, 20)
    for _ in range(500):
        n = rng.randint(1, 5)
        s = [[rng.choice(vocab) for _ in range(rng.randint(0, 5))] for _ in range(n)]
        t = rng.choice([0.0, 0.1, 0.2, 0.3])
        idf = idf_from_sentences(s)
        a = threshold_graph(s, t, idf)
        b_exact = [[Fraction(x, sum(row)) for x in row] for row in a]
        b = lexrank_matrix(s, t, idf)
        assert all(abs(b[i][j] - float(b_exact[i][j])) < 1e-15 for i in range(n) for j in range(n))
        p, _ = power_method(b, 0.15, 1e-12)
        want = stationary_exact(b_exact, d)
        assert abs(sum(want) - 1) == 0
        assert all(abs(x - float(y)) < 1e-9 for x, y in zip(p, want))
        assert abs(sum(p) - 1) < 1e-12 and all(x > 0 for x in p)


def test_degree_centrality_when_d_is_zero():
    # On a connected symmetric graph with self loops, the stationary distribution
    # of B is proportional to the degrees.
    rng = random.Random(22)
    vocab = list("abcde")
    done = 0
    while done < 150:
        n = rng.randint(2, 6)
        s = [[rng.choice(vocab) for _ in range(rng.randint(1, 4))] for _ in range(n)]
        idf = idf_from_sentences(s)
        a = threshold_graph(s, 0.1, idf)
        seen, stack = {0}, [0]
        while stack:
            u = stack.pop()
            for v in range(n):
                if a[u][v] and v not in seen:
                    seen.add(v)
                    stack.append(v)
        if len(seen) < n:
            continue
        done += 1
        deg = [sum(row) for row in a]
        p, _ = power_method(lexrank_matrix(s, 0.1, idf), 0.0, 1e-13, max_iter=100000)
        assert all(abs(x - y / sum(deg)) < 1e-6 for x, y in zip(p, deg))


def test_continuous_rows_and_sum():
    rng = random.Random(9)
    vocab = ["v%d" % i for i in range(6)]
    for _ in range(200):
        n = rng.randint(1, 5)
        s = [[rng.choice(vocab) for _ in range(rng.randint(0, 5))] for _ in range(n)]
        b = lexrank_matrix(s, continuous=True)
        for i in range(n):
            assert abs(sum(b[i]) - 1) < 1e-12
            for j in range(n):
                assert b[i][j] >= 0
        p = lexrank(s, continuous=True, eps=1e-12)
        assert abs(sum(p) - 1) < 1e-9
        # The fixed point equation holds.
        q = [0.15 / n + 0.85 * sum(b[i][j] * p[i] for i in range(n)) for j in range(n)]
        assert all(abs(x - y) < 1e-9 for x, y in zip(p, q))


def test_power_method_rate():
    # The 1-norm error shrinks at least by the factor 1 - d per step.
    rng = random.Random(5)
    vocab = list("abcdef")
    for _ in range(100):
        s = [[rng.choice(vocab) for _ in range(rng.randint(1, 4))] for _ in range(5)]
        b = lexrank_matrix(s, 0.1)
        star, _ = power_method(b, 0.15, 1e-14, max_iter=100000)
        prev = None
        for t in range(1, 8):
            p, _ = power_method(b, 0.15, 0.0, max_iter=t)
            err = sum(abs(x - y) for x, y in zip(p, star))
            if prev is not None:
                assert err <= 0.85 * prev + 1e-12
            prev = err


def test_empty_input():
    assert lexrank([]) == []
    assert lexrank_summarize([], 3) == []
