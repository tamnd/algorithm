# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latent-semantic-analysis/. The authors are listed in prov/A919QT.jsonl.

import math
import random

import pytest

from latent_semantic_analysis import (
    cosine,
    fold_in,
    jacobi_eigh,
    lsa_search,
    reconstruct,
    term_document_matrix,
    tfidf,
    truncated_svd,
)

VOCAB = ["human", "interface", "computer", "user", "system", "response", "time", "EPS", "survey",
         "trees", "graph", "minors"]
DOCS = [
    ["human", "interface", "computer"],
    ["computer", "user", "system", "response", "time", "survey"],
    ["interface", "user", "system", "EPS"],
    ["human", "system", "system", "EPS"],
    ["user", "response", "time"],
    ["trees"],
    ["trees", "graph"],
    ["trees", "graph", "minors"],
    ["graph", "minors", "survey"],
]


def correlation(x: list, y: list) -> float:
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    num = sum((p - mx) * (q - my) for p, q in zip(x, y))
    return num / math.sqrt(sum((p - mx) ** 2 for p in x) * sum((q - my) ** 2 for q in y))


def test_deerwester_singular_values() -> None:
    a = term_document_matrix(DOCS, VOCAB)
    sig, _, _ = truncated_svd(a, 9)
    expected = [3.34, 2.54, 2.35, 1.64, 1.50, 1.31, 0.85, 0.56, 0.36]
    assert [round(s, 2) for s in sig] == expected
    assert sum(s * s for s in sig) == pytest.approx(31.0)  # the squared Frobenius norm of A


def test_eckart_young_errors_equal_discarded_singular_values() -> None:
    rng = random.Random(1)
    for a in [term_document_matrix(DOCS, VOCAB), [[rng.random() for _ in range(5)] for _ in range(7)]]:
        full, _, _ = truncated_svd(a, len(a[0]))
        for k in range(1, len(full)):
            sig, u, v = truncated_svd(a, k)
            ak = reconstruct(sig, u, v)
            r = [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, ak)]
            frob2 = sum(x * x for row in r for x in row)
            assert frob2 == pytest.approx(sum(s * s for s in full[k:]), abs=1e-9)
            rtr = [[sum(r[i][p] * r[i][q] for i in range(len(r))) for q in range(len(r[0]))] for p in range(len(r[0]))]
            spectral = math.sqrt(max(jacobi_eigh(rtr)[0][0], 0.0))
            assert spectral == pytest.approx(full[k], abs=1e-7)


def test_factors_are_orthonormal() -> None:
    sig, u, v = truncated_svd(term_document_matrix(DOCS, VOCAB), 4)
    for cols in (u, v):
        for s in range(4):
            for t in range(4):
                dot = sum(row[s] * row[t] for row in cols)
                assert dot == pytest.approx(1.0 if s == t else 0.0, abs=1e-10)


def test_folding_in_a_column_gives_its_row_of_v() -> None:
    a = term_document_matrix(DOCS, VOCAB)
    sig, u, v = truncated_svd(a, 3)
    for j in range(len(DOCS)):
        col = [a[i][j] for i in range(len(VOCAB))]
        assert fold_in(col, sig, u) == pytest.approx(v[j], abs=1e-10)


def test_query_human_computer_interaction() -> None:
    a = term_document_matrix(DOCS, VOCAB)
    sig, u, _ = truncated_svd(a, 2)
    q = [1.0 if t in ("human", "computer") else 0.0 for t in VOCAB]
    q_hat = fold_in(q, sig, u)
    assert [abs(x) for x in q_hat] == pytest.approx([0.1382, 0.0276], abs=1e-4)
    ranking = lsa_search(DOCS, VOCAB, 2, ["human", "computer", "interaction"])
    top5 = {j for j, _ in ranking[:5]}
    assert top5 == {0, 1, 2, 3, 4}  # all c documents rank above all m documents
    scores = dict(ranking)
    assert scores[2] > 0.9 and scores[4] > 0.9  # c3 and c5 share no word with the query
    raw = [cosine([a[i][j] for i in range(len(VOCAB))], q) for j in range(len(DOCS))]
    assert raw[2] == 0.0 and raw[4] == 0.0


def test_reduced_space_links_terms_that_never_co_occur() -> None:
    a = term_document_matrix(DOCS, VOCAB)
    sig, u, v = truncated_svd(a, 2)
    a2 = reconstruct(sig, u, v)
    human, user, minors = 0, 3, 11
    assert correlation(a[human], a[user]) == pytest.approx(-0.378, abs=1e-3)
    assert correlation(a2[human], a2[user]) == pytest.approx(0.939, abs=1e-3)
    assert correlation(a2[human], a2[minors]) == pytest.approx(-0.831, abs=1e-3)


def test_tfidf_weights_and_search() -> None:
    a = tfidf(term_document_matrix([["x", "y"], ["x", "z"], ["x", "y", "y"]], ["x", "y", "z"]))
    assert a[0] == [0.0, 0.0, 0.0]  # a term in every document carries no information
    assert a[1][2] == pytest.approx(2 * math.log(1.5))
    ranking = lsa_search(DOCS, VOCAB, 2, ["graph", "trees"], weighting="tfidf")
    assert {j for j, _ in ranking[:4]} == {5, 6, 7, 8}
