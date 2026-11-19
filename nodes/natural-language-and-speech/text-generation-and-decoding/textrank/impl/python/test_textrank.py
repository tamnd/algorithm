# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/textrank/. The authors are listed in prov/FCW45A.jsonl.

import math
import random

from textrank import (
    cooccurrence_graph,
    overlap_similarity,
    similarity_matrix,
    textrank_keywords,
    textrank_scores,
    textrank_summarize,
    weighted_pagerank,
)


def solve(a, b):
    """Solve a x = b by Gaussian elimination with partial pivoting."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c] / m[c][c]
                for k in range(c, n + 1):
                    m[r][k] -= f * m[c][k]
    return [m[i][n] / m[i][i] for i in range(n)]


def exact_scores(w, d):
    """The fixed point of WS = (1 - d) + d M WS, from the linear system (I - d M) WS = (1 - d) 1."""
    n = len(w)
    out = [sum(row) for row in w]
    a = [[(1.0 if i == j else 0.0) - (d * w[j][i] / out[j] if out[j] > 0 else 0.0)
          for j in range(n)] for i in range(n)]
    return solve(a, [1.0 - d] * n)


def page_example():
    text = [
        "the cat sat on the mat",
        "the dog sat on the log",
        "a cat and a dog met",
        "birds fly south",
    ]
    return [s.split() for s in text]


def test_similarity_formula():
    a = "the cat sat on the mat".split()
    b = "the dog sat on the log".split()
    # Shared distinct words: the, sat, on.
    assert abs(overlap_similarity(a, b) - 3 / (2 * math.log(6))) < 1e-12
    assert overlap_similarity(a, "birds fly south".split()) == 0.0
    # Two one-word sentences: the denominator is log 1 + log 1 = 0.
    assert overlap_similarity(["sun"], ["sun"]) == 0.0
    assert overlap_similarity([], ["sun"]) == 0.0
    # Case is ignored, and repeats count once in the numerator.
    assert abs(overlap_similarity(["The", "the"], ["the", "x"]) - 1 / (2 * math.log(2))) < 1e-12


def test_page_example():
    s = page_example()
    w = similarity_matrix(s)
    assert abs(w[0][1] - 0.837166) < 1e-6
    assert abs(w[0][2] - 0.279055) < 1e-6
    assert abs(w[1][2] - 0.279055) < 1e-6
    assert all(w[3][j] == 0.0 for j in range(4))
    # By symmetry WS = (x, x, y, 0.15) with x = 0.15 + 0.85 (3/4 x + 1/2 y) and
    # y = 0.15 + 0.85 (1/4 x + 1/4 x), so x = 0.21375 / 0.181875.
    x = 0.21375 / 0.181875
    y = 0.15 + 0.425 * x
    ws, it = weighted_pagerank(w, 0.85, 1e-4)
    assert it == 7
    assert all(abs(a - b) < 1e-4 for a, b in zip(ws, [x, x, y, 0.15]))
    assert abs(x - 1.175258) < 1e-6 and abs(y - 0.649485) < 1e-6
    first, _ = weighted_pagerank(w, 0.85, 0.0, max_iter=1)
    assert all(abs(a - b) < 1e-12 for a, b in zip(first, [1.2125, 1.2125, 0.575, 0.15]))
    assert textrank_summarize(s, 2) == [0, 1]


def test_log_base_does_not_matter():
    # Scaling every weight by the same factor leaves w[j][i] / out(j) unchanged.
    s = page_example()
    w = similarity_matrix(s)
    w10 = [[x * math.log(10) for x in row] for row in w]
    a, _ = weighted_pagerank(w, 0.85, 1e-12)
    b, _ = weighted_pagerank(w10, 0.85, 1e-12)
    assert all(abs(x - y) < 1e-12 for x, y in zip(a, b))


def test_page_example_unequal():
    s = page_example()
    s[2] = "a cat and a dog met on the mat".split()
    ws = textrank_scores(s, 0.85, 1e-12)
    ex = exact_scores(similarity_matrix(s), 0.85)
    assert all(abs(x - y) < 1e-9 for x, y in zip(ws, ex))
    assert textrank_summarize(s, 1) == [0]


def test_fixed_point_and_sum():
    rng = random.Random(2004)
    vocab = ["w%d" % i for i in range(8)]
    for _ in range(500):
        n = rng.randint(1, 6)
        s = [[rng.choice(vocab) for _ in range(rng.randint(0, 6))] for _ in range(n)]
        w = similarity_matrix(s)
        for i in range(n):
            assert w[i][i] == 0.0
            for j in range(n):
                assert w[i][j] == w[j][i] >= 0.0
        d = rng.choice([0.5, 0.85, 0.9])
        ws, it = weighted_pagerank(w, d, 1e-11)
        ex = exact_scores(w, d)
        assert all(abs(x - y) < 1e-8 for x, y in zip(ws, ex))
        # Columns of M sum to 1 for vertices with edges, so the scores sum to n
        # when no vertex is isolated; an isolated vertex keeps 1 - d.
        iso = [i for i in range(n) if sum(w[i]) == 0.0]
        for i in iso:
            assert abs(ws[i] - (1 - d)) < 1e-12
        if not iso:
            assert abs(sum(ws) - n) < 1e-8
        assert all(x >= 1 - d - 1e-12 for x in ws)


def test_stopping_rule_bound():
    # After a stop with change delta, the 1-norm error is at most d / (1 - d) * delta.
    rng = random.Random(7)
    vocab = list("abcdefg")
    for _ in range(200):
        s = [[rng.choice(vocab) for _ in range(rng.randint(2, 6))] for _ in range(5)]
        w = similarity_matrix(s)
        eps = 1e-3
        ws, _ = weighted_pagerank(w, 0.85, eps)
        ex = exact_scores(w, 0.85)
        err = sum(abs(x - y) for x, y in zip(ws, ex))
        assert err <= 0.85 / 0.15 * eps + 1e-12


def test_cooccurrence_graph_against_brute_force():
    rng = random.Random(11)
    vocab = ["n%d" % i for i in range(5)] + ["of", "the"]
    cand = lambda t: not t.lower() in ("of", "the")
    for _ in range(300):
        toks = [rng.choice(vocab) for _ in range(rng.randint(0, 12))]
        win = rng.randint(2, 5)
        words, w = cooccurrence_graph(toks, cand, win)
        seq = [t.lower() for t in toks if cand(t)]
        assert sorted(words) == sorted(set(seq))
        for a in range(len(words)):
            for b in range(len(words)):
                near = any(seq[i] == words[a] and seq[j] == words[b] and 0 < abs(i - j) < win
                           for i in range(len(seq)) for j in range(len(seq)))
                assert (w[a][b] == 1.0) == (near and a != b)


def test_keywords_join_adjacent():
    toks = "Matlab code for plotting ambiguity functions".split()
    cand = lambda t: t.lower() in {"matlab", "code", "plotting", "ambiguity", "functions"}
    kw = textrank_keywords(toks, cand, window=2)
    # Five vertices on a path; T = 1, the top vertex is the second one (code).
    assert kw == ["code"]
    toks2 = "linear constraints over natural numbers and linear constraints".split()
    cand2 = lambda t: t.lower() in {"linear", "constraints", "natural", "numbers"}
    kw2 = textrank_keywords(toks2, cand2, window=2)
    assert all(k in ("linear", "constraints", "linear constraints", "natural", "numbers") for k in kw2)
    assert textrank_keywords([], cand2) == []
