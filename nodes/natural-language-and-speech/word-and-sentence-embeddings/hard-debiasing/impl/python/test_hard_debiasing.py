# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hard-debiasing/. The authors are listed in prov/92204H.jsonl.

import math
import random

import pytest

from hard_debiasing import (
    bias_subspace,
    direct_bias,
    dot,
    equalize,
    hard_debias,
    neutralize,
    norm,
    normalize,
    project,
    top_eigenvectors,
    within_set_covariance,
)

PAGE = {
    "she": [0.6, 0.8, 0.0],
    "he": [-0.6, 0.8, 0.0],
    "woman": [0.8, 0.0, 0.6],
    "man": [-0.8, 0.0, 0.6],
    "nurse": [0.28, 0.96, 0.0],
    "doctor": [-0.36, 0.48, 0.8],
    "grandmother": [0.48, 0.6, 0.64],
    "grandfather": [-0.6, 0.64, 0.48],
}


def rand_vec(rng, d):
    return [rng.gauss(0.0, 1.0) for _ in range(d)]


def close(a, b, tol=1e-9):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def test_page_example():
    W, B = hard_debias(PAGE, [["she", "he"], ["woman", "man"]], ["nurse", "doctor"], [["grandmother", "grandfather"]])
    assert close(B[0], [1.0, 0.0, 0.0])
    assert close(W["nurse"], [0.0, 1.0, 0.0])
    assert close(W["doctor"], [0.0, 0.48 / math.sqrt(0.8704), 0.8 / math.sqrt(0.8704)])
    s = math.sqrt(1 - 0.62**2 - 0.56**2)
    assert close(W["grandmother"], [s, 0.62, 0.56])
    assert close(W["grandfather"], [-s, 0.62, 0.56])
    assert dot(PAGE["nurse"], PAGE["grandmother"]) == pytest.approx(0.7104)
    assert dot(PAGE["nurse"], PAGE["grandfather"]) == pytest.approx(0.4464)
    assert dot(W["nurse"], W["grandmother"]) == pytest.approx(0.62)
    assert dot(W["nurse"], W["grandfather"]) == pytest.approx(0.62)
    assert direct_bias([PAGE["nurse"], PAGE["doctor"]], B[0]) == pytest.approx(0.32)
    assert direct_bias([W["nurse"], W["doctor"]], B[0]) == pytest.approx(0.0, abs=1e-12)


def test_pair_covariance_is_a_quarter_of_the_difference_outer_products():
    rng = random.Random(1)
    pairs = [[rand_vec(rng, 4), rand_vec(rng, 4)] for _ in range(5)]
    C = within_set_covariance(pairs)
    for a in range(4):
        for b in range(4):
            expected = math.fsum((p[0][a] - p[1][a]) * (p[0][b] - p[1][b]) for p in pairs) / 4
            assert C[a][b] == pytest.approx(expected, abs=1e-12)


def test_eigenvectors_satisfy_the_eigen_equation_and_maximize_the_rayleigh_quotient():
    rng = random.Random(2)
    sets = [[rand_vec(rng, 5) for _ in range(rng.randint(2, 4))] for _ in range(6)]
    C = within_set_covariance(sets)
    vecs, vals = top_eigenvectors(C, 3)
    assert vals[0] >= vals[1] >= vals[2] >= 0
    for v, lam in zip(vecs, vals):
        Cv = [dot(row, v) for row in C]
        assert close(Cv, [lam * x for x in v], 1e-8)
        assert norm(v) == pytest.approx(1.0)
    for i in range(3):
        for j in range(i + 1, 3):
            assert dot(vecs[i], vecs[j]) == pytest.approx(0.0, abs=1e-8)
    for _ in range(100):
        r = normalize(rand_vec(rng, 5))
        assert dot(r, [dot(row, r) for row in C]) <= vals[0] + 1e-9


def test_planted_direction_is_recovered():
    rng = random.Random(3)
    g = normalize([1.0, 2.0, -1.0, 0.5, 0.0, 1.0])
    pairs = []
    for _ in range(10):
        base = rand_vec(rng, 6)
        noise = [0.05 * x for x in rand_vec(rng, 6)]
        pairs.append([[b + x + gi for b, x, gi in zip(base, noise, g)], [b - gi for b, gi in zip(base, g)]])
    B = bias_subspace(pairs, 1)
    assert abs(dot(B[0], g)) > 0.99


def test_neutralize_gives_unit_vectors_with_no_bias_component():
    rng = random.Random(4)
    sets = [[rand_vec(rng, 5), rand_vec(rng, 5)] for _ in range(4)]
    for k in (1, 2):
        B = bias_subspace(sets, k)
        for _ in range(20):
            w = neutralize(rand_vec(rng, 5), B)
            assert norm(w) == pytest.approx(1.0)
            assert all(abs(dot(w, b)) < 1e-12 for b in B)
            assert direct_bias([w], B[0]) == pytest.approx(0.0, abs=1e-12)


def test_equalize_makes_every_neutral_word_equidistant():
    rng = random.Random(5)
    sets = [[normalize(rand_vec(rng, 6)), normalize(rand_vec(rng, 6))] for _ in range(4)]
    for k in (1, 2):
        B = bias_subspace(sets, k)
        for size in (2, 3):
            E = [normalize(rand_vec(rng, 6)) for _ in range(size)]
            out = equalize(E, B)
            for e in out:
                assert norm(e) == pytest.approx(1.0)
            for _ in range(10):
                w = neutralize(rand_vec(rng, 6), B)
                dots = [dot(w, e) for e in out]
                assert max(dots) - min(dots) < 1e-12
                dists = [norm([x - y for x, y in zip(w, e)]) for e in out]
                assert max(dists) - min(dists) < 1e-12
        out = equalize(sets[0], B)
        # For a pair the two bias components are opposite.
        assert close(project(out[0], B), [-x for x in project(out[1], B)], 1e-12)


def test_equalize_rejects_a_degenerate_set():
    B = [[1.0, 0.0, 0.0]]
    with pytest.raises(ValueError):
        equalize([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], B)


def test_bias_stays_recoverable_after_debiasing():
    # The Gonen and Goldberg effect on a toy: the words also differ along h, a
    # direction that the defining pairs do not show, so neutralize leaves it.
    rng = random.Random(6)
    d = 8
    g = [1.0] + [0.0] * (d - 1)
    h = [0.0, 1.0] + [0.0] * (d - 2)
    vectors = {}
    pairs = []
    for i in range(6):
        base = rand_vec(rng, d)
        base[0] = 0.0
        vectors[f"f{i}"] = [b + 2 * gi for b, gi in zip(base, g)]
        vectors[f"m{i}"] = [b - 2 * gi for b, gi in zip(base, g)]
        pairs.append([f"f{i}", f"m{i}"])
    labels = {}
    for i in range(40):
        side = 1 if i % 2 == 0 else -1
        v = [0.4 * x for x in rand_vec(rng, d)]
        v = [x + side * (gi + 1.5 * hi) for x, gi, hi in zip(v, g, h)]
        vectors[f"n{i}"] = v
        labels[f"n{i}"] = side
    neutral = list(labels)
    W, B = hard_debias(vectors, pairs, neutral, [], k=1)
    assert abs(B[0][0]) > 0.99
    assert direct_bias([W[w] for w in neutral], B[0]) < 1e-12
    correct = 0
    for w in neutral:
        others = [u for u in neutral if u != w]
        nearest = max(others, key=lambda u: dot(W[w], W[u]))
        correct += labels[nearest] == labels[w]
    assert correct / len(neutral) >= 0.9


def test_input_is_not_changed():
    copy = {w: list(v) for w, v in PAGE.items()}
    hard_debias(PAGE, [["she", "he"]], ["nurse"], [["grandmother", "grandfather"]])
    assert PAGE == copy
