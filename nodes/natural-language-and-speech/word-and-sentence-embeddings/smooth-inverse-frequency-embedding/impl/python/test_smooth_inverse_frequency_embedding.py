# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smooth-inverse-frequency-embedding/. The authors are listed in prov/V5GPPB.jsonl.

import math
import random

import pytest

from smooth_inverse_frequency_embedding import (
    dot,
    first_singular_vector,
    norm,
    remove_projection,
    sif_embeddings,
    sif_weight,
    weighted_average,
    word_probabilities,
)

P = {"the": 0.05, "a": 0.04, "cat": 1e-4, "dog": 1e-4, "sat": 5e-4, "ran": 5e-4}
V = {
    "the": [1.0, 1.0, 0.0],
    "a": [1.0, 0.8, 0.2],
    "cat": [0.2, 0.0, 1.0],
    "dog": [0.0, 0.2, 1.0],
    "sat": [0.5, -1.0, 0.0],
    "ran": [0.3, -1.0, 0.3],
}
S = ["the cat sat".split(), "a dog ran".split(), "the dog sat".split()]


def rand_vec(rng, d):
    return [rng.gauss(0.0, 1.0) for _ in range(d)]


def test_weights():
    assert sif_weight(1e-3, 1e-3) == pytest.approx(0.5)
    assert sif_weight(0.0, 1e-3) == 1.0
    assert sif_weight(0.05) == pytest.approx(1 / 51)
    ps = [0.0, 1e-5, 1e-4, 1e-3, 1e-2, 0.1]
    ws = [sif_weight(p) for p in ps]
    assert all(x > y for x, y in zip(ws, ws[1:]))
    with pytest.raises(ValueError):
        sif_weight(0.1, 0.0)


def test_word_probabilities():
    p = word_probabilities([["a", "b", "a"], ["c", "a"]])
    assert p == {"a": 0.6, "b": 0.2, "c": 0.2}
    assert math.fsum(p.values()) == pytest.approx(1.0)


def test_page_example():
    avg = weighted_average(S[0], V, P, 1e-3, 3)
    w_the, w_cat, w_sat = 1 / 51, 1 / 1.1, 1 / 1.5
    expected = [(w_the * x + w_cat * y + w_sat * z) / 3 for x, y, z in zip(V["the"], V["cat"], V["sat"])]
    assert avg == pytest.approx(expected)
    assert avg == pytest.approx([0.1783, -0.2157, 0.3030], abs=1e-4)
    out, u = sif_embeddings(S, V, P)
    assert u == pytest.approx([0.3168, -0.4503, 0.8348], abs=1e-4)
    assert out[0] == pytest.approx([0.0495, -0.0326, -0.0364], abs=1e-4)
    for v in out:
        assert dot(u, v) == pytest.approx(0.0, abs=1e-12)


def test_unknown_words_are_skipped_and_an_empty_sentence_is_zero():
    assert weighted_average(["zzz"], V, P, 1e-3, 3) == [0.0, 0.0, 0.0]
    assert weighted_average(["cat", "zzz"], V, P, 1e-3, 3) == pytest.approx([x / 1.1 for x in V["cat"]])
    # A word with a vector but no probability gets the weight 1.
    assert weighted_average(["new"], {"new": [2.0, 0.0]}, {}, 1e-3, 2) == [2.0, 0.0]


def test_first_singular_vector_is_an_eigenvector_and_maximizes_the_energy():
    rng = random.Random(1)
    X = [rand_vec(rng, 5) for _ in range(12)]
    u, sigma = first_singular_vector(X)
    assert norm(u) == pytest.approx(1.0)
    G = [[math.fsum(r[i] * r[j] for r in X) for j in range(5)] for i in range(5)]
    Gu = [dot(row, u) for row in G]
    assert Gu == pytest.approx([sigma**2 * x for x in u], abs=1e-8)
    energy = math.fsum(dot(r, u) ** 2 for r in X)
    for _ in range(200):
        r = rand_vec(rng, 5)
        nr = norm(r)
        r = [x / nr for x in r]
        assert math.fsum(dot(row, r) ** 2 for row in X) <= energy + 1e-9


def test_removal_gives_orthogonal_vectors_and_is_idempotent():
    rng = random.Random(2)
    u = rand_vec(rng, 4)
    nu = norm(u)
    u = [x / nu for x in u]
    for _ in range(20):
        v = rand_vec(rng, 4)
        w = remove_projection(v, u)
        assert dot(w, u) == pytest.approx(0.0, abs=1e-12)
        assert remove_projection(w, u) == pytest.approx(w, abs=1e-12)
        assert norm(w) <= norm(v) + 1e-12


def test_planted_common_direction_is_found_and_removed():
    rng = random.Random(3)
    d = 6
    c0 = [1.0, -1.0, 2.0, 0.0, 0.5, 1.0]
    n0 = norm(c0)
    c0 = [x / n0 for x in c0]
    vocab = {f"w{i}": [3.0 * x + 0.3 * y for x, y in zip(c0, rand_vec(rng, d))] for i in range(30)}
    sentences = [[f"w{rng.randrange(30)}" for _ in range(5)] for _ in range(40)]
    p = word_probabilities(sentences)
    out, u = sif_embeddings(sentences, vocab, p)
    assert abs(dot(u, c0)) > 0.99
    before = [weighted_average(s, vocab, p, 1e-3, d) for s in sentences]
    # Before the removal all sentence vectors point the same way; after it they do not.
    cos_before = [dot(a, b) / (norm(a) * norm(b)) for a, b in zip(before, before[1:])]
    cos_after = [dot(a, b) / (norm(a) * norm(b)) for a, b in zip(out, out[1:])]
    assert min(cos_before) > 0.9
    assert sum(cos_after) / len(cos_after) < 0.5


def test_identical_sentences_become_zero_without_centering():
    vecs = {"x": [1.0, 2.0], "y": [0.5, -1.0]}
    out, u = sif_embeddings([["x", "y"], ["x", "y"], ["y", "x"]], vecs, {"x": 0.01, "y": 0.02})
    for v in out:
        assert v == pytest.approx([0.0, 0.0], abs=1e-12)


def test_all_zero_sentences_raise():
    with pytest.raises(ValueError):
        sif_embeddings([["zzz"]], V, P)
