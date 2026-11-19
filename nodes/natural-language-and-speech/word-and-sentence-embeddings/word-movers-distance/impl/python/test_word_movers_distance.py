# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-movers-distance/. The authors are listed in prov/ZXZK9R.jsonl.

import math
import random
from fractions import Fraction
from itertools import permutations

import pytest

from word_movers_distance import euclidean, knn, nbow, rwmd, transport, wcd, wmd, wmd_with_flow

V = {
    "obama": [1.0, 0.0],
    "president": [1.2, 0.1],
    "speaks": [0.0, 1.0],
    "greets": [0.2, 1.1],
    "media": [-1.0, 0.0],
    "press": [-1.1, -0.2],
    "illinois": [0.0, -1.0],
    "chicago": [0.1, -1.3],
}
STOP = {"the", "to", "in"}
D1 = "obama speaks to the media in illinois".split()
D2 = "the president greets the press in chicago".split()
D3 = "the president speaks".split()


def random_vocab(rng, size, dim):
    return {f"w{i}": [rng.gauss(0.0, 1.0) for _ in range(dim)] for i in range(size)}


def random_doc(rng, vocab, length):
    words = list(vocab)
    return [rng.choice(words) for _ in range(length)]


def check_flow(T, d1, d2):
    for i, row in enumerate(T):
        assert sum(row) == d1[i]
        assert all(x >= 0 for x in row)
    for j in range(len(d2)):
        assert sum(T[i][j] for i in range(len(T))) == d2[j]


def test_nbow():
    words, d = nbow(["a", "b", "a", "the", "zzz"], {"a": [1.0], "b": [2.0], "the": [0.0]}, {"the"})
    assert words == ["a", "b"]
    assert d == [Fraction(2, 3), Fraction(1, 3)]
    with pytest.raises(ValueError):
        nbow(["the"], {"the": [0.0]}, {"the"})


def test_page_example():
    dist, w1, w2, T = wmd_with_flow(D1, D2, V, STOP)
    assert w1 == ["obama", "speaks", "media", "illinois"]
    assert dist == pytest.approx((3 * math.sqrt(0.05) + math.sqrt(0.1)) / 4)
    assert dist == pytest.approx(0.2468, abs=1e-4)
    assert T == [[Fraction(1, 4) if i == j else 0 for j in range(4)] for i in range(4)]
    assert wcd(D1, D2, V, STOP) == pytest.approx(0.125)
    dist3, _, w3, T3 = wmd_with_flow(D1, D3, V, STOP)
    assert w3 == ["president", "speaks"]
    assert dist3 == pytest.approx(0.8164, abs=1e-4)
    assert T3 == [[Fraction(1, 4), 0], [0, Fraction(1, 4)], [0, Fraction(1, 4)], [Fraction(1, 4), 0]]


def test_assignment_case_matches_brute_force_over_permutations():
    rng = random.Random(1)
    for n in range(1, 7):
        vocab = random_vocab(rng, 2 * n, 3)
        words = list(vocab)
        a, b = words[:n], words[n:]
        best = min(math.fsum(euclidean(vocab[a[i]], vocab[b[p[i]]]) for i in range(n)) for p in permutations(range(n)))
        assert wmd(a, b, vocab) == pytest.approx(best / n, abs=1e-12)


def test_transport_matches_brute_force_on_integer_vertices():
    # With supplies (2, 1) and demands (1, 1, 1), every vertex of the polytope is listed below.
    rng = random.Random(2)
    for _ in range(30):
        cost = [[rng.uniform(0, 5) for _ in range(3)] for _ in range(2)]
        candidates = []
        for j in range(3):
            row1 = [1 if k == j else 0 for k in range(3)]
            row0 = [1 - x for x in row1]
            candidates.append(math.fsum(row0[k] * cost[0][k] + row1[k] * cost[1][k] for k in range(3)))
        total, flow = transport([2, 1], [1, 1, 1], cost)
        assert total == pytest.approx(min(candidates), abs=1e-12)
        assert [sum(r) for r in flow] == [2, 1]
        assert [flow[0][j] + flow[1][j] for j in range(3)] == [1, 1, 1]


def test_one_dimensional_closed_form():
    # On the line, the earth mover's distance is the integral of |F1 - F2|.
    rng = random.Random(3)
    for _ in range(20):
        vocab = {f"w{i}": [rng.uniform(-3, 3)] for i in range(8)}
        a = random_doc(rng, vocab, rng.randint(1, 6))
        b = random_doc(rng, vocab, rng.randint(1, 6))
        wa, da = nbow(a, vocab)
        wb, db = nbow(b, vocab)
        pts = sorted({vocab[w][0] for w in wa + wb})
        integral = 0.0
        for left, right in zip(pts, pts[1:]):
            f1 = sum(float(f) for w, f in zip(wa, da) if vocab[w][0] <= left)
            f2 = sum(float(f) for w, f in zip(wb, db) if vocab[w][0] <= left)
            integral += abs(f1 - f2) * (right - left)
        assert wmd(a, b, vocab) == pytest.approx(integral, abs=1e-9)


def test_flow_is_feasible_and_bounds_hold():
    rng = random.Random(4)
    vocab = random_vocab(rng, 12, 4)
    for _ in range(40):
        a = random_doc(rng, vocab, rng.randint(1, 7))
        b = random_doc(rng, vocab, rng.randint(1, 7))
        dist, w1, w2, T = wmd_with_flow(a, b, vocab)
        check_flow(T, nbow(a, vocab)[1], nbow(b, vocab)[1])
        assert wcd(a, b, vocab) <= dist + 1e-12
        assert rwmd(a, b, vocab) <= dist + 1e-12
        assert wmd(b, a, vocab) == pytest.approx(dist, abs=1e-12)


def test_metric_axioms():
    rng = random.Random(5)
    vocab = random_vocab(rng, 10, 3)
    docs = [random_doc(rng, vocab, rng.randint(1, 5)) for _ in range(8)]
    for a in docs:
        assert wmd(a, a, vocab) == pytest.approx(0.0, abs=1e-12)
        assert wmd(a, list(reversed(a)) + a, vocab) == pytest.approx(0.0, abs=1e-12)
    for a in docs:
        for b in docs:
            for c in docs:
                assert wmd(a, c, vocab) <= wmd(a, b, vocab) + wmd(b, c, vocab) + 1e-9


def test_knn_with_pruning_equals_brute_force():
    rng = random.Random(6)
    vocab = random_vocab(rng, 15, 3)
    docs = [random_doc(rng, vocab, rng.randint(2, 6)) for _ in range(25)]
    query = random_doc(rng, vocab, 4)
    brute = sorted((wmd(query, d, vocab), i) for i, d in enumerate(docs))
    for k in (1, 3, 5):
        got, exact = knn(query, docs, vocab, k)
        assert [i for _, i in got] == [i for _, i in brute[:k]]
        assert exact <= len(docs)
    _, exact = knn(query, docs, vocab, 1)
    assert exact < len(docs)


def test_bad_input():
    with pytest.raises(ValueError):
        transport([1, 1], [3], [[0.0], [0.0]])
    with pytest.raises(ValueError):
        transport([-1, 2], [1], [[0.0], [0.0]])
