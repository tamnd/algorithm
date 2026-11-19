# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ibm-model-3/. The authors are listed in prov/2CTGQ5.jsonl.

import math
import random
from collections import defaultdict
from fractions import Fraction as F
from itertools import product

from ibm_model_3 import (
    NULL,
    all_alignments,
    em_step,
    expected_counts,
    hill_climb,
    log_likelihood,
    log_prob,
    neighbours,
    pegged_set,
    prob,
    start_alignment,
    structure_prob,
    uniform_params,
    viterbi_brute,
)


def normalize(d, group):
    tot = defaultdict(float)
    for k, v in d.items():
        tot[group(k)] += v
    return {k: v / tot[group(k)] for k, v in d.items()}


def random_params(rng, corpus, phi_max=2, exact=False):
    p = uniform_params(corpus, phi_max)
    draw = (lambda: F(rng.randint(1, 9))) if exact else (lambda: rng.random() + 0.01)
    for key in ("t", "n", "d"):
        p[key] = {k: draw() for k in p[key]}
    p["t"] = normalize(p["t"], lambda k: k[1])
    p["n"] = normalize(p["n"], lambda k: k[1])
    p["d"] = normalize(p["d"], lambda k: k[1:])
    p["p1"] = F(1, 5) if exact else 0.2
    return p


def random_pair(rng, mmax, lmax):
    m, l = rng.randint(2, mmax), rng.randint(1, lmax)
    return [f"f{rng.randrange(3)}" for _ in range(m)], [f"e{rng.randrange(3)}" for _ in range(l)]


def test_equation_32_by_hand() -> None:
    # e = x, f = a b, a = (1, 0): phi_1 = 1, phi_0 = 1, m = 2
    p = {"t": {("a", "x"): F(1, 2), ("b", NULL): F(1, 3)},
         "n": {(1, "x"): F(2, 5)},
         "d": {(1, 1, 1, 2): F(3, 4)},
         "p1": F(1, 10)}
    # C(1, 1) p0^0 p1^1 * 1! n(1 | x) * t(a | x) t(b | NULL) * d(1 | 1, 1, 2)
    assert prob(["a", "b"], ["x"], (1, 0), p) == F(1, 10) * F(2, 5) * F(1, 2) * F(1, 3) * F(3, 4)
    # two null words need at least four words: C(m - 2, 2) = 0 for m = 3
    p["t"][("c", NULL)] = F(1, 3)
    p["n"][(1, "x")] = F(1)
    assert prob(["b", "c", "a"], ["x"], (0, 0, 1), p) == 0


def test_deficiency() -> None:
    # Sum Equation 32 (without t, whose rows sum to 1 over f) over every length and alignment,
    # and compare with the success probability of the generative story; the gap is the mass
    # the story puts on two words in one position, which is not a string.
    e = ["x", "y"]
    phi_max, p1 = 2, F(1, 4)
    n = {(0, "x"): F(1, 4), (1, "x"): F(1, 2), (2, "x"): F(1, 4),
         (0, "y"): F(1, 3), (1, "y"): F(1, 3), (2, "y"): F(1, 3)}
    mmax = 2 * len(e) * phi_max
    d = {}
    for m in range(1, mmax + 1):
        for i in (1, 2):
            w = {j: F(1 + (j == i) + (j == 2 * i), 1) for j in range(1, m + 1)}
            tot = sum(w.values())
            for j in range(1, m + 1):
                d[(j, i, 2, m)] = w[j] / tot
    params = {"t": {}, "n": n, "d": d, "p1": p1}
    total = F(0)
    for m in range(0, mmax + 1):
        for a in all_alignments(m, len(e)):
            total += structure_prob(a, e, m, params)
    story = F(0)
    for phi in product(range(phi_max + 1), repeat=len(e)):
        pphi = n[(phi[0], "x")] * n[(phi[1], "y")]
        words = [i for i in (1, 2) for _ in range(phi[i - 1])]
        k = len(words)
        for phi0 in range(k + 1):
            m = k + phi0
            pn = math.comb(k, phi0) * p1 ** phi0 * (1 - p1) ** (k - phi0)
            for pos in product(range(1, m + 1), repeat=k):
                if len(set(pos)) == k:
                    pd = F(1)
                    for i, j in zip(words, pos):
                        pd *= d[(j, i, 2, m)]
                    story += pphi * pn * pd
    assert total == story
    assert total < 1
    assert float(1 - total) > 0.1
    # the hand case: one target word with fertility 2, no null words, d(j | 1, 1, 2) = 1/2;
    # the two words land in the same position with probability 1/2
    hand = {"t": {}, "n": {(2, "x"): F(1)}, "d": {(1, 1, 1, 2): F(1, 2), (2, 1, 1, 2): F(1, 2)}, "p1": F(0)}
    assert sum(structure_prob(a, ["x"], 2, hand) for a in all_alignments(2, 1)) == F(1, 2)


def test_neighbours() -> None:
    a = (1, 0, 1)
    nb = neighbours(a, 2)
    # moves: 3 positions times 2 other values; swaps: the pairs with different values
    assert len(nb) == 3 * 2 + 2
    assert all(sum(x != y for x, y in zip(a, b)) in (1, 2) for b in nb)
    assert all(b[1] == 2 for b in neighbours(a, 2, peg=(2, 2)))


def test_exact_e_step_and_em() -> None:
    corpus = [(["a", "b"], ["x"]), (["a", "c", "b"], ["x", "y"])]
    p = uniform_params(corpus)
    c = expected_counts(corpus, p)
    # every source word gives one unit of count to t, and every real target word one unit to n
    assert sum(c["t"].values()) == 5
    assert sum(c["n"].values()) == 3
    p2 = em_step(corpus, p)
    for key, group in (("t", lambda k: k[1]), ("n", lambda k: k[1]), ("d", lambda k: k[1:])):
        sums = defaultdict(F)
        for k, v in p2[key].items():
            assert 0 <= v <= 1
            sums[group(k)] += v
        assert set(sums.values()) == {F(1)}
    assert 0 < p2["p1"] < 1
    # exact EM never decreases the likelihood (floats for more rounds)
    rng = random.Random(31)
    for _ in range(3):
        corpus = [random_pair(rng, 3, 2) for _ in range(3)]
        q = random_params(rng, corpus)
        hist = [log_likelihood(corpus, q)]
        for _ in range(6):
            q = em_step(corpus, q)
            hist.append(log_likelihood(corpus, q))
        assert all(y >= x - 1e-9 for x, y in zip(hist, hist[1:]))


def test_hill_climbing_and_pegging_against_brute_force() -> None:
    rng = random.Random(32)
    stuck = 0
    for _ in range(80):
        f, e = random_pair(rng, 4, 3)
        p = random_params(rng, [(f, e)])
        best, pbest = viterbi_brute(f, e, p)
        a = hill_climb(f, e, start_alignment(f, e, p), p)
        pa = prob(f, e, a, p)
        assert pa <= pbest
        assert all(prob(f, e, b, p) <= pa for b in neighbours(a, len(e)))  # a local maximum
        stuck += pa < pbest
        s = pegged_set(f, e, p)
        assert max(prob(f, e, b, p) for b in s) == pbest
    # hill climbing alone stops below the best alignment in some cases; pegging recovers them here
    assert stuck >= 3


def test_pegged_counts_equal_exact_on_tiny_pairs() -> None:
    # for m = 2 and l = 1 the set S contains every alignment, so the two E steps agree
    rng = random.Random(33)
    corpus = [(["a", "b"], ["x"]), (["b", "b"], ["x"])]
    p = random_params(rng, corpus, exact=True)
    assert pegged_set(["a", "b"], ["x"], p) == set(all_alignments(2, 1))
    assert expected_counts(corpus, p, exact=True) == expected_counts(corpus, p, exact=False)


def test_log_prob_long_sentence() -> None:
    m = 200
    f = [f"f{j % 50}" for j in range(m)]
    e = [f"e{j % 50}" for j in range(m)]
    a = tuple(range(1, m + 1))
    vf = sorted(set(f))
    p = {"t": {(x, y): 1 / 50 for x in vf for y in sorted(set(e))},
         "n": {(1, y): 0.5 for y in set(e)},
         "d": {(j, j, m, m): 0.5 for j in range(1, m + 1)},
         "p1": 0.1}
    assert prob(f, e, a, p) == 0.0
    want = m * (math.log(0.9) + math.log(0.5) + math.log(1 / 50) + math.log(0.5))
    assert math.isclose(log_prob(f, e, a, p), want, rel_tol=1e-12)
    small = (["a", "b"], ["x"])
    q = random_params(random.Random(34), [small])
    for al in all_alignments(2, 1):
        w = prob(*small, al, q)
        assert (w == 0 and log_prob(*small, al, q) == -math.inf) or math.isclose(log_prob(*small, al, q), math.log(w))
