# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-u-turn-sampler/. The authors are listed in prov/1360ZZ.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from no_u_turn_sampler import naive_tree, no_u_turn_sampler


def ess(xs):
    """Effective sample size by Geyer's initial positive sequence."""
    n = len(xs)
    m = sum(xs) / n
    c = [x - m for x in xs]
    var = sum(v * v for v in c) / n
    if var == 0:
        return 1.0

    def rho(k):
        return sum(c[i] * c[i + k] for i in range(n - k)) / (n * var)

    tau, k = -1.0, 0
    while k + 1 < n:
        g = rho(k) + rho(k + 1)
        if g <= 0:
            break
        tau += 2 * g
        k += 2
    return n / max(tau, 1e-9)


def check_mean(xs, mu, sd):
    # the sample mean has standard error about sd / sqrt(ESS)
    assert abs(sum(xs) / len(xs) - mu) < 5 * sd / math.sqrt(ess(xs))


def std_normal(q):
    return -0.5 * sum(v * v for v in q)


def std_normal_grad(q):
    return [-v for v in q]


def stretched(q):
    # exact Fraction arithmetic: N(0, diag(1, 1/4))
    return -(q[0] * q[0] + 4 * q[1] * q[1]) / 2


def stretched_grad(q):
    return [-q[0], -4 * q[1]]


def directions_from(position, depth):
    # bit k of the position inside the final tree says whether the start is in the right half
    return [-1 if (position >> k) & 1 else 1 for k in range(depth)]


def test_same_candidates_from_every_candidate() -> None:
    # condition C.4 of Hoffman and Gelman: the tree and the set C do not depend on which point of C started it
    # some states fall outside the slice, and some runs exclude a last half that has an inner U-turn
    q0, p0 = [F(1), F(1, 2)], [F(1, 3), F(-1)]
    log_u = stretched(q0) - (p0[0] ** 2 + p0[1] ** 2) / 2 - F(1, 50)
    runs = [(eps, dirs) for eps in (F(1, 4), F(1, 2)) for dirs in ([1, 1, -1], [-1, 1, 1], [1, -1, -1], [-1, -1, -1])]
    for eps, dirs in runs:
        states, cand, depth = naive_tree(stretched, stretched_grad, q0, p0, log_u, eps, dirs)
        assert len(cand) >= 2 and len(cand) < len(states)
        lo = min(states)
        for c in cand:
            qc, pc = states[c]
            dc = directions_from(c - lo, depth)
            states_c, cand_c, depth_c = naive_tree(stretched, stretched_grad, qc, pc, log_u, eps, dc)
            assert depth_c == depth
            assert {i + c for i in cand_c} == cand
            assert all(states_c[i - c] == states[i] for i in cand)


def test_example_tree_from_page() -> None:
    # N(0, 1), q = 0, p = 1, eps = 1/2, directions -1, +1, +1: the third half has a U-turn inside
    log_u = -0.5 + math.log(0.5)
    states, cand, depth = naive_tree(std_normal, std_normal_grad, [0.0], [1.0], log_u, 0.5, [-1, 1, 1])
    assert depth == 3 and sorted(states) == list(range(-1, 7))
    assert cand == {-1, 0, 1, 2}
    assert abs(states[2][0][0] - 0.875) < 1e-12 and abs(states[3][1][0] - 0.0546875) < 1e-12


def efficient_selection(cands, size, m):
    """Law of the state chosen by Algorithm 3 from start m, for candidate positions cands in [0, size)."""
    dist = {m: F(1)}
    n = 1
    k = 1
    while k < size:
        sibling = (m // k) * k ^ k
        new = [x for x in cands if sibling <= x < sibling + k]
        if new:
            prob = min(F(1), F(len(new), n))
            dist = {x: (1 - prob) * w for x, w in dist.items()}
            for x in new:
                dist[x] = dist.get(x, F(0)) + prob / len(new)
        n += len(new)
        k *= 2
    return dist


def test_progressive_sampling_keeps_uniform_exactly() -> None:
    # the biased progressive sampling of the top level leaves the uniform law on C invariant
    rng = random.Random(6)
    for _ in range(200):
        size = 2 ** rng.randint(1, 5)
        cands = {x for x in range(size) if rng.random() < 0.6} or {0}
        total = {x: F(0) for x in cands}
        for m in cands:
            for x, w in efficient_selection(cands, size, m).items():
                total[x] += w
        assert all(t == 1 for t in total.values())


def test_standard_normal_moments() -> None:
    rng = random.Random(1)
    chain, depths = no_u_turn_sampler(std_normal, std_normal_grad, [2.0], 0.2, 3000, rng)
    xs = [x[0] for x in chain]
    check_mean(xs, 0.0, 1.0)
    check_mean([x * x for x in xs], 1.0, math.sqrt(2))
    # the trajectory stops near half a period, pi / 0.2 = 16 steps, so depth is mostly 3 to 5
    assert 3 <= sum(depths) / len(depths) <= 5


def test_correlated_gaussian() -> None:
    rho = 0.95
    det_s = 1 - rho * rho

    def log_t(q):
        return -(q[0] ** 2 - 2 * rho * q[0] * q[1] + q[1] ** 2) / (2 * det_s)

    def grad(q):
        return [-(q[0] - rho * q[1]) / det_s, -(q[1] - rho * q[0]) / det_s]

    rng = random.Random(2)
    chain, depths = no_u_turn_sampler(log_t, grad, [0.0, 0.0], 0.15, 2000, rng)
    for i in range(2):
        xs = [x[i] for x in chain]
        check_mean(xs, 0.0, 1.0)
        check_mean([v * v for v in xs], 1.0, math.sqrt(2))
    check_mean([x[0] * x[1] for x in chain], rho, math.sqrt(1 + rho * rho))


def test_heavier_than_gaussian_target() -> None:
    # logistic density: mean 0, variance pi^2 / 3
    def log_t(q):
        return -q[0] - 2 * math.log1p(math.exp(-q[0])) if q[0] > 0 else q[0] - 2 * math.log1p(math.exp(q[0]))

    def grad(q):
        return [-math.tanh(q[0] / 2)]

    rng = random.Random(3)
    chain, _ = no_u_turn_sampler(log_t, grad, [0.0], 0.3, 3000, rng)
    xs = [x[0] for x in chain]
    check_mean(xs, 0.0, math.pi / math.sqrt(3))
    check_mean([x * x for x in xs], math.pi**2 / 3, 7.0)


def test_max_depth_is_respected() -> None:
    rng = random.Random(4)
    chain, depths = no_u_turn_sampler(std_normal, std_normal_grad, [0.0], 0.01, 50, rng, max_depth=3)
    assert max(depths) == 3


def test_bad_inputs() -> None:
    rng = random.Random(5)
    with pytest.raises(ValueError):
        no_u_turn_sampler(std_normal, std_normal_grad, [0.0], 0.0, 10, rng)
    with pytest.raises(ValueError):
        no_u_turn_sampler(std_normal, std_normal_grad, [0.0], 0.1, 10, rng, max_depth=0)
