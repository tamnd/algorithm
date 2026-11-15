# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/colbert/. The authors are listed in prov/26Y1DV.jsonl.

import math
import random

from colbert import (
    candidates,
    dot,
    end_to_end,
    exhaustive_top_k,
    maxsim_score,
    missed_bound,
    normalize,
    pairwise_loss,
    pairwise_loss_gradient,
)

Q = [[1.0, 0.0], [0.0, 1.0]]
DOCS = [[[0.8, 0.6], [0.6, 0.8]], [[1.0, 0.0]], [[0.0, 1.0]]]


def random_unit(rng, d):
    return normalize([rng.gauss(0, 1) for _ in range(d)])


def random_case(rng, n_docs=6, d=4):
    q = [random_unit(rng, d) for _ in range(rng.randint(1, 4))]
    docs = [[random_unit(rng, d) for _ in range(rng.randint(1, 5))] for _ in range(n_docs)]
    return q, docs


def test_page_example():
    assert [round(maxsim_score(Q, d), 12) for d in DOCS] == [1.6, 1.0, 1.0]
    assert exhaustive_top_k(Q, DOCS, 1) == [0]
    # With k' = 1 each query vector finds a one-token document first, and
    # document 0, the true best, is never a candidate.
    assert candidates(Q, DOCS, 1) == [1, 2]
    assert end_to_end(Q, DOCS, 1, 1) == [1]
    assert candidates(Q, DOCS, 2) == [0, 1, 2]
    assert end_to_end(Q, DOCS, 2, 1) == [0]


def test_maxsim_against_double_loop():
    rng = random.Random(1)
    for _ in range(200):
        q, docs = random_case(rng)
        for d in docs:
            total = 0.0
            for qi in q:
                best = -math.inf
                for dj in d:
                    s = 0.0
                    for a, b in zip(qi, dj):
                        s += a * b
                    if s > best:
                        best = s
                total += best
            assert abs(maxsim_score(q, d) - total) < 1e-12


def test_full_candidate_set_gives_exhaustive_result():
    rng = random.Random(2)
    for _ in range(200):
        q, docs = random_case(rng)
        n_tokens = sum(len(d) for d in docs)
        assert candidates(q, docs, n_tokens) == list(range(len(docs)))
        for k in (1, 3, len(docs)):
            assert end_to_end(q, docs, n_tokens, k) == exhaustive_top_k(q, docs, k)


def test_superset_of_true_top_k_is_enough():
    rng = random.Random(3)
    hits = 0
    for _ in range(300):
        q, docs = random_case(rng)
        k = 2
        truth = exhaustive_top_k(q, docs, k)
        for k_prime in (1, 2, 3):
            if set(truth) <= set(candidates(q, docs, k_prime)):
                hits += 1
                assert end_to_end(q, docs, k_prime, k) == truth
    assert hits > 0


def test_missed_bound_certifies_the_result():
    assert abs(missed_bound(Q, DOCS, 1) - 2.0) < 1e-12
    rng = random.Random(6)
    certified = 0
    for _ in range(300):
        q, docs = random_case(rng)
        exact = {i: maxsim_score(q, d) for i, d in enumerate(docs)}
        for k_prime in (1, 2, 4):
            cand = candidates(q, docs, k_prime)
            b = missed_bound(q, docs, k_prime)
            assert all(exact[i] <= b + 1e-12 for i in range(len(docs)) if i not in cand)
            k = 2
            got = end_to_end(q, docs, k_prime, k)
            if len(got) == k and exact[got[-1]] > b:
                certified += 1
                assert got == exhaustive_top_k(q, docs, k)
    assert certified > 0


def test_ties_by_document_id():
    q = [[1.0, 0.0]]
    docs = [[[0.0, 1.0]], [[1.0, 0.0]], [[1.0, 0.0]]]
    assert exhaustive_top_k(q, docs, 2) == [1, 2]
    assert end_to_end(q, docs, 3, 2) == [1, 2]


def test_pairwise_loss_gradient_by_finite_differences():
    rng = random.Random(4)
    h = 1e-6
    checked = 0
    for _ in range(50):
        q, docs = random_case(rng, n_docs=2)
        pos, neg = docs
        # Skip cases where some max is close to a tie, so the argmax is unique.
        gaps = []
        for qi in q:
            for d in (pos, neg):
                vals = sorted((dot(qi, dj) for dj in d), reverse=True)
                if len(vals) > 1:
                    gaps.append(vals[0] - vals[1])
        if gaps and min(gaps) < 1e-3:
            continue
        g = pairwise_loss_gradient(q, pos, neg)
        for i in range(len(q)):
            for c in range(len(q[i])):
                old = q[i][c]
                q[i][c] = old + h
                up = pairwise_loss(q, pos, neg)
                q[i][c] = old - h
                down = pairwise_loss(q, pos, neg)
                q[i][c] = old
                assert abs((up - down) / (2 * h) - g[i][c]) < 1e-6
        checked += 1
    assert checked > 20


def test_score_bounds_for_unit_vectors():
    rng = random.Random(5)
    for _ in range(100):
        q, docs = random_case(rng)
        for d in docs:
            assert -len(q) - 1e-12 <= maxsim_score(q, d) <= len(q) + 1e-12
        # A document that contains every query vector gets the top score n.
        assert abs(maxsim_score(q, q) - len(q)) < 1e-12
