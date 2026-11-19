# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bertscore/. The authors are listed in prov/T124HA.jsonl.

import math
import random
from itertools import permutations

from bertscore import (
    bertscore,
    bertscore_rescaled,
    idf_from_references,
    normalize,
    rescale,
    similarity_matrix,
    unknown_idf,
)

TOL = 1e-12


def rand_vecs(rng, k, d):
    return [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(k)]


def test_page_example():
    ref = [[1.0, 0.0], [0.0, 2.0]]
    cand = [[3.0, 0.0], [0.6, 0.8], [0.8, -0.6]]
    s = similarity_matrix(ref, cand)
    want = [[1.0, 0.6, 0.8], [0.0, 0.8, -0.6]]
    assert all(abs(s[i][j] - want[i][j]) < TOL for i in range(2) for j in range(3))
    p, r, f = bertscore(ref, cand)
    assert abs(r - 0.9) < TOL
    assert abs(p - 2.6 / 3) < TOL
    assert abs(f - 2 * 0.9 * (2.6 / 3) / (0.9 + 2.6 / 3)) < TOL
    assert abs(f - 0.883019) < 1e-6
    # With idf weights 1 and 3 on the reference tokens, recall is (1 + 3 * 0.8) / 4.
    _, rw, _ = bertscore(ref, cand, ref_weights=[1.0, 3.0])
    assert abs(rw - 0.85) < TOL


def direct(ref, cand, wr=None, wc=None):
    """Recompute P, R and F from the definition, without the module's matrix code."""
    def cos(u, v):
        return sum(a * b for a, b in zip(u, v)) / (math.hypot(*u) * math.hypot(*v))
    wr = wr or [1.0] * len(ref)
    wc = wc or [1.0] * len(cand)
    r = sum(w * max(cos(u, v) for v in cand) for w, u in zip(wr, ref)) / sum(wr)
    p = sum(w * max(cos(u, v) for u in ref) for w, v in zip(wc, cand)) / sum(wc)
    return p, r, 2 * p * r / (p + r)


def test_against_direct_formula():
    rng = random.Random(2020)
    for _ in range(300):
        d = rng.randint(1, 6)
        ref = rand_vecs(rng, rng.randint(1, 6), d)
        cand = rand_vecs(rng, rng.randint(1, 6), d)
        wr = [rng.uniform(0.1, 3.0) for _ in ref]
        wc = [rng.uniform(0.1, 3.0) for _ in cand]
        got = bertscore(ref, cand, wr, wc)
        want = direct(ref, cand, wr, wc)
        if abs(want[0] + want[1]) < 1e-9:
            continue
        assert all(abs(a - b) < 1e-9 for a, b in zip(got, want))
        assert all(-1 - 1e-12 <= x <= 1 + 1e-12 for x in got[:2])


def test_identical_and_invariances():
    rng = random.Random(7)
    for _ in range(100):
        ref = rand_vecs(rng, rng.randint(1, 6), 4)
        p, r, f = bertscore(ref, ref)
        assert abs(p - 1) < 1e-12 and abs(r - 1) < 1e-12 and abs(f - 1) < 1e-12
        cand = rand_vecs(rng, rng.randint(1, 6), 4)
        base = bertscore(ref, cand)
        # Scaling a vector by a positive number changes nothing.
        scaled = [[3.5 * a for a in v] for v in cand]
        assert all(abs(a - b) < 1e-12 for a, b in zip(bertscore(ref, scaled), base))
        # The order of the tokens does not matter once the embeddings are fixed.
        shuffled = cand[:]
        rng.shuffle(shuffled)
        assert all(abs(a - b) < 1e-12 for a, b in zip(bertscore(ref, shuffled), base))
        # Swapping the roles swaps precision and recall.
        p2, r2, f2 = bertscore(cand, ref)
        assert abs(p2 - base[1]) < 1e-12 and abs(r2 - base[0]) < 1e-12


def test_greedy_at_least_optimal_assignment():
    # Greedy matching lets many tokens match one token, so it is never below
    # the best one-to-one matching (Appendix C of the paper compares the two).
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(1, 4)
        m = rng.randint(n, 6)
        ref = rand_vecs(rng, n, 3)
        cand = rand_vecs(rng, m, 3)
        s = similarity_matrix(ref, cand)
        best = max(sum(s[i][perm[i]] for i in range(n)) for perm in permutations(range(m), n)) / n
        _, r, _ = bertscore(ref, cand)
        assert r >= best - 1e-12
        # Equality when every reference token has a different best match.
        argmax = [max(range(m), key=lambda j: s[i][j]) for i in range(n)]
        if len(set(argmax)) == n:
            assert abs(r - best) < 1e-12


def test_f_between_p_and_r():
    rng = random.Random(3)
    for _ in range(200):
        ref = [[abs(x) for x in v] for v in rand_vecs(rng, rng.randint(1, 5), 3)]
        cand = [[abs(x) for x in v] for v in rand_vecs(rng, rng.randint(1, 5), 3)]
        p, r, f = bertscore(ref, cand)
        assert min(p, r) - 1e-12 <= f <= max(p, r) + 1e-12
        assert f <= (p + r) / 2 + 1e-12


def test_idf():
    refs = [["the", "cat", "sat"], ["the", "dog"], ["a", "cat", "cat"]]
    idf = idf_from_references(refs)
    assert abs(idf["the"] - math.log(4 / 3)) < TOL
    assert abs(idf["cat"] - math.log(4 / 3)) < TOL
    assert abs(idf["dog"] - math.log(2)) < TOL
    assert abs(unknown_idf(3) - math.log(4)) < TOL
    # Equal weights give the unweighted score.
    rng = random.Random(5)
    ref = rand_vecs(rng, 4, 3)
    cand = rand_vecs(rng, 5, 3)
    a = bertscore(ref, cand)
    b = bertscore(ref, cand, [2.0] * 4, [2.0] * 5)
    assert all(abs(x - y) < 1e-12 for x, y in zip(a, b))


def test_rescale():
    assert abs(rescale(0.9, 0.8) - 0.5) < TOL
    assert rescale(1.0, 0.83) == 1.0
    assert abs(rescale(0.83, 0.83)) < TOL
    # Rescaling is increasing, so it keeps the ranking of candidates.
    rng = random.Random(13)
    ref = rand_vecs(rng, 4, 3)
    cands = [rand_vecs(rng, 4, 3) for _ in range(20)]
    raw = [bertscore(ref, c)[1] for c in cands]
    res = [bertscore_rescaled(ref, c, (0.8, 0.82, 0.81))[1] for c in cands]
    assert sorted(range(20), key=lambda i: raw[i]) == sorted(range(20), key=lambda i: res[i])


def test_edge_cases():
    assert bertscore([], [[1.0]]) == (0.0, 0.0, 0.0)
    assert normalize([0.0, 0.0]) == [0.0, 0.0]
    # Orthogonal tokens: P = R = 0 and F is set to 0.
    assert bertscore([[1.0, 0.0]], [[0.0, 1.0]]) == (0.0, 0.0, 0.0)
