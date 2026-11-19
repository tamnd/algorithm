# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/glove/. The authors are listed in prov/S7WPYE.jsonl.

import math
import random

from glove import (
    build_vocab,
    cooccurrence,
    cost,
    glove,
    gradient,
    init_params,
    train,
    weight,
)


def planted_corpus(seed=0, sentences=120, length=6):
    """Two clusters: words a* only meet contexts x*, words b* only meet contexts y*."""
    rng = random.Random(seed)
    groups = [([f"a{i}" for i in range(5)], [f"x{i}" for i in range(4)]),
              ([f"b{i}" for i in range(5)], [f"y{i}" for i in range(4)])]
    corpus = []
    for _ in range(sentences):
        words, ctx = groups[rng.randrange(2)]
        corpus.append([rng.choice(words) if k % 2 == 0 else rng.choice(ctx) for k in range(length)])
    return corpus, groups


def cos(u, v):
    return sum(a * b for a, b in zip(u, v)) / math.sqrt(sum(a * a for a in u) * sum(b * b for b in v))


def test_cooccurrence_against_all_position_pairs():
    rng = random.Random(1)
    words = "a b c d e".split()
    corpus = [[rng.choice(words) for _ in range(rng.randint(1, 9))] for _ in range(15)]
    vocab = build_vocab(corpus)
    for window in (1, 2, 3, 10):
        got = cooccurrence(corpus, vocab, window)
        ref = {}
        for sent in corpus:
            for p in range(len(sent)):
                for q in range(len(sent)):
                    if p != q and abs(p - q) <= window:
                        key = (vocab[sent[p]], vocab[sent[q]])
                        ref[key] = ref.get(key, 0.0) + 1.0 / abs(p - q)
        assert set(got) == set(ref)
        assert all(abs(got[k] - ref[k]) < 1e-12 for k in ref)
        assert all(abs(got[(i, j)] - got[(j, i)]) < 1e-12 for i, j in got)


def test_hand_counts():
    vocab = {"the": 0, "cat": 1, "sat": 2}
    x = cooccurrence([["the", "cat", "sat"]], vocab, window=2)
    assert x == {(1, 0): 1.0, (0, 1): 1.0, (2, 1): 1.0, (1, 2): 1.0, (2, 0): 0.5, (0, 2): 0.5}


def test_weight_function():
    assert weight(0.0) == 0.0
    assert weight(100.0) == 1.0 and weight(1000.0) == 1.0
    assert abs(weight(50.0) - 0.5 ** 0.75) < 1e-15
    assert abs(weight(1.0) - 0.0316227766) < 1e-9
    xs = [0.5 * k for k in range(1, 400)]
    assert all(weight(a) <= weight(b) for a, b in zip(xs, xs[1:]))


def test_gradient_against_finite_differences():
    corpus, _ = planted_corpus(seed=2, sentences=10)
    vocab = build_vocab(corpus)
    x = cooccurrence(corpus, vocab, window=3)
    rng = random.Random(3)
    p = init_params(len(vocab), 4, seed=3)
    for key in ("w", "wt"):
        p[key] = [[rng.uniform(-0.5, 0.5) for _ in r] for r in p[key]]
    p["b"] = [rng.uniform(-0.5, 0.5) for _ in p["b"]]
    p["bt"] = [rng.uniform(-0.5, 0.5) for _ in p["bt"]]
    g = gradient(p, x, x_max=4.0)
    h = 1e-6
    checks = [("w", i, k) for i in range(0, len(vocab), 3) for k in range(4)]
    checks += [("wt", i, k) for i in range(1, len(vocab), 3) for k in range(4)]
    checks += [("b", i, None) for i in range(len(vocab))] + [("bt", i, None) for i in range(len(vocab))]
    for key, i, k in checks:
        row = p[key] if k is None else p[key][i]
        idx = i if k is None else k
        old = row[idx]
        row[idx] = old + h
        up = cost(p, x, x_max=4.0)
        row[idx] = old - h
        down = cost(p, x, x_max=4.0)
        row[idx] = old
        num = (up - down) / (2 * h)
        ana = g[key][i] if k is None else g[key][i][k]
        assert abs(num - ana) < 1e-5 * max(1.0, abs(ana))


def test_training_lowers_cost():
    corpus, _ = planted_corpus(seed=4, sentences=60)
    vocab = build_vocab(corpus)
    x = cooccurrence(corpus, vocab, window=2)
    p0 = init_params(len(vocab), 8, seed=4)
    start = cost(p0, x, x_max=10.0)
    _, hist = train(x, len(vocab), 8, epochs=40, seed=4, x_max=10.0)
    assert hist[-1] < 0.2 * start
    assert hist[-1] <= hist[len(hist) // 2]


def test_planted_clusters_come_apart():
    corpus, groups = planted_corpus(seed=5)
    vec = glove(corpus, d=8, window=2, epochs=40, seed=5, x_max=10.0)
    (a, x), (b, y) = groups
    inside = [cos(vec[u], vec[v]) for g in (a, b) for k, u in enumerate(g) for v in g[k + 1:]]
    across = [cos(vec[u], vec[v]) for u in a for v in b]
    assert min(inside) > max(across)
    assert sum(inside) / len(inside) - sum(across) / len(across) > 0.5
