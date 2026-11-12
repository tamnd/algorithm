# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baum-welch-algorithm/. The authors are listed in prov/X13Y7R.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import product

from baum_welch_algorithm import baum_welch, baum_welch_step, posteriors, random_parameters


def joint(pi, A, B, obs, q):
    p = pi[q[0]] * B[q[0]][obs[0]]
    for t in range(1, len(obs)):
        p *= A[q[t - 1]][q[t]] * B[q[t]][obs[t]]
    return p


def brute_step(pi, A, B, seqs):
    """Re-estimation by enumeration of all N^T state paths, in exact arithmetic."""
    n, m = len(pi), len(B[0])
    s = [F(0)] * n
    e = [[F(0)] * n for _ in range(n)]
    f = [[F(0)] * m for _ in range(n)]
    for obs in seqs:
        paths = list(product(range(n), repeat=len(obs)))
        w = {q: joint(pi, A, B, obs, q) for q in paths}
        z = sum(w.values())
        for q, p in w.items():
            r = p / z
            s[q[0]] += r
            for t in range(len(obs) - 1):
                e[q[t]][q[t + 1]] += r
            for t, o in enumerate(obs):
                f[q[t]][o] += r
    norm = lambda row: [x / sum(row) for x in row]
    return norm(s), [norm(r) for r in e], [norm(r) for r in f]


def as_float(x):
    return [as_float(y) for y in x] if isinstance(x, list) else float(x)


def close(x, y, tol=1e-12):
    if isinstance(x, list):
        return len(x) == len(y) and all(close(a, b, tol) for a, b in zip(x, y))
    return math.isclose(x, y, rel_tol=tol, abs_tol=tol)


def test_one_step_matches_enumeration() -> None:
    pi = [F(1, 2), F(1, 2)]
    A = [[F(7, 10), F(3, 10)], [F(2, 10), F(8, 10)]]
    B = [[F(9, 10), F(1, 10)], [F(2, 10), F(8, 10)]]
    seqs = [[0, 0, 1, 0]]
    ref = brute_step(pi, A, B, seqs)
    got = baum_welch_step(as_float(pi), as_float(A), as_float(B), seqs)
    for r, g in zip(ref, got[:3]):
        assert close(as_float(r), g)
    assert math.isclose(got[3], math.log(0.04911505), rel_tol=1e-12)
    # the worked example on the page
    assert close(got[0], [0.8770, 0.1230], 5e-4)
    assert close(got[1], [[0.6697, 0.3303], [0.4186, 0.5814]], 5e-4)
    assert close(got[2], [[0.8827, 0.1173], [0.4950, 0.5050]], 5e-4)
    _, _, _, hist = baum_welch(as_float(pi), as_float(A), as_float(B), seqs, iterations=1, tol=0.0)
    assert close(hist, [-3.013590, -2.169387], 1e-6)


def test_random_steps_match_enumeration() -> None:
    rng = random.Random(1970)
    for _ in range(40):
        n, m = rng.randint(1, 3), rng.randint(1, 3)
        pi = [F(rng.randint(1, 4)) for _ in range(n)]
        pi = [x / sum(pi) for x in pi]
        A = [[F(rng.randint(1, 4)) for _ in range(n)] for _ in range(n)]
        A = [[x / sum(r) for x in r] for r in A]
        B = [[F(rng.randint(1, 4)) for _ in range(m)] for _ in range(n)]
        B = [[x / sum(r) for x in r] for r in B]
        seqs = [[rng.randrange(m) for _ in range(rng.randint(2, 4))] for _ in range(rng.randint(1, 3))]
        ref = brute_step(pi, A, B, seqs)
        got = baum_welch_step(as_float(pi), as_float(A), as_float(B), seqs)
        for r, g in zip(ref, got[:3]):
            assert close(as_float(r), g, 1e-10)


def test_posteriors_sum_to_one() -> None:
    rng = random.Random(5)
    pi, A, B = random_parameters(3, 4, rng)
    obs = [rng.randrange(4) for _ in range(50)]
    gamma, xi_sum, _ = posteriors(pi, A, B, obs)
    assert all(math.isclose(sum(g), 1.0, rel_tol=1e-12) for g in gamma)
    assert math.isclose(sum(map(sum, xi_sum)), len(obs) - 1, rel_tol=1e-12)


def sample(pi, A, B, T, rng):
    def draw(row):
        return rng.choices(range(len(row)), weights=row)[0]

    q, out = draw(pi), []
    for _ in range(T):
        out.append(draw(B[q]))
        q = draw(A[q])
    return out


def test_likelihood_never_decreases_and_rows_stay_stochastic() -> None:
    true = ([0.6, 0.4], [[0.9, 0.1], [0.2, 0.8]], [[0.7, 0.2, 0.1], [0.1, 0.3, 0.6]])
    for seed in range(8):
        rng = random.Random(seed)
        seqs = [sample(*true, 60, rng) for _ in range(3)]
        n = rng.randint(2, 3)
        pi, A, B, hist = baum_welch(*random_parameters(n, 3, rng), seqs, iterations=60, tol=0.0)
        assert len(hist) == 61
        for a, b in zip(hist, hist[1:]):
            assert b >= a - 1e-9 * abs(a)
        assert hist[-1] > hist[0]
        for row in [pi, *A, *B]:
            assert all(x >= 0 for x in row)
            assert math.isclose(sum(row), 1.0, rel_tol=1e-12)


def test_zeros_stay_zero() -> None:
    rng = random.Random(11)
    pi = [1.0, 0.0, 0.0]
    A = [[0.5, 0.5, 0.0], [0.0, 0.5, 0.5], [0.0, 0.0, 1.0]]  # left-to-right model
    B = [[0.6, 0.4], [0.3, 0.7], [0.5, 0.5]]
    seqs = [[rng.randrange(2) for _ in range(12)] for _ in range(4)]
    pi2, A2, B2, hist = baum_welch(pi, A, B, seqs, iterations=20, tol=0.0)
    assert pi2[1] == pi2[2] == 0.0
    for i in range(3):
        for j in range(3):
            if A[i][j] == 0.0:
                assert A2[i][j] == 0.0


def test_symmetric_start_is_stuck_at_a_stationary_point() -> None:
    # Equal emission rows: every state looks the same, so EM can never split them.
    # The fixed point is the i.i.d. model; a random start does better. EM finds only local optima.
    rng = random.Random(3)
    true = ([0.5, 0.5], [[0.95, 0.05], [0.05, 0.95]], [[0.9, 0.1], [0.1, 0.9]])
    seqs = [sample(*true, 200, rng)]
    sym = ([0.5, 0.5], [[0.5, 0.5], [0.5, 0.5]], [[0.5, 0.5], [0.5, 0.5]])
    _, _, Bs, hs = baum_welch(*sym, seqs, iterations=30)
    freq = sum(seqs[0]) / len(seqs[0])
    assert close(Bs[0], [1 - freq, freq], 1e-12) and close(Bs[1], Bs[0], 1e-12)
    _, _, _, hr = baum_welch(*random_parameters(2, 2, random.Random(4)), seqs, iterations=200)
    assert hr[-1] > hs[-1] + 10.0
