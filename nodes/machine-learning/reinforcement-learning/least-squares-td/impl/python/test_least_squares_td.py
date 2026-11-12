# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-td/. The authors are listed in prov/6WB7ES.jsonl.

import math
import random
from fractions import Fraction as F

from least_squares_td import lstd, recursive_lstd, solve

PHI = {0: (F(1), F(0)), 1: (F(1), F(1)), 2: (F(1), F(3))}
R = {0: F(0), 1: F(0), 2: F(1)}
P = [[F(1, 2), F(1, 2), F(0)], [F(1, 4), F(1, 2), F(1, 4)], [F(0), F(1, 2), F(1, 2)]]
G = F(9, 10)
# A closed walk whose 8 transitions occur in proportion to mu(s) P(s, s') with mu = (1/4, 1/2, 1/4).
CYCLE = [0, 0, 1, 1, 1, 2, 2, 1, 0]
DATA = [(CYCLE[i], R[CYCLE[i]], CYCLE[i + 1]) for i in range(8)]


def td_fixed_point():
    mu = [F(1, 4), F(1, 2), F(1, 4)]
    a = [[sum(mu[s] * PHI[s][i] * (PHI[s][j] - G * sum(P[s][t] * PHI[t][j] for t in range(3))) for s in range(3)) for j in range(2)] for i in range(2)]
    b = [sum(mu[s] * PHI[s][i] * R[s] for s in range(3)) for i in range(2)]
    return solve(a, b)


def test_lstd_on_full_data_equals_td_fixed_point() -> None:
    assert td_fixed_point() == [F(185, 109), F(70, 109)]
    assert lstd(DATA, PHI.get, 2, G) == [F(185, 109), F(70, 109)]
    assert lstd(DATA * 3, PHI.get, 2, G) == [F(185, 109), F(70, 109)]


def test_recursive_equals_batch_exactly() -> None:
    rng = random.Random(3)
    for _ in range(40):
        d = rng.randint(1, 3)
        phi = {s: [F(rng.randint(-2, 3)) for _ in range(d)] for s in range(4)}
        data = []
        for _ in range(rng.randint(1, 12)):
            s = rng.randrange(4)
            nxt = None if rng.random() < 0.2 else rng.randrange(4)
            data.append((s, F(rng.randint(-3, 3)), nxt))
        g, lam, eps = F(rng.randint(0, 9), 10), F(rng.randint(0, 4), 4), F(rng.randint(1, 5), 7)
        try:
            thetas = recursive_lstd(data, phi.get, d, g, lam, eps)
        except ValueError:
            continue
        for k in (1, len(data)):
            assert thetas[k - 1] == lstd(data[:k], phi.get, d, g, lam, eps)


def test_regularized_value_on_one_cycle() -> None:
    eps = F(1, 100)
    assert lstd(DATA, PHI.get, 2, G, 0, eps) == [F(74200, 44351), F(28600, 44351)]
    assert recursive_lstd(DATA, PHI.get, 2, G, 0, eps)[-1] == [F(74200, 44351), F(28600, 44351)]


def test_lstd_one_is_least_squares_on_returns() -> None:
    rng = random.Random(5)
    phi = {s: [F(1), F(s), F(s * s % 5)] for s in range(5)}
    for _ in range(20):
        data = []
        for _ in range(rng.randint(2, 4)):
            length = rng.randint(1, 5)
            states = [rng.randrange(5) for _ in range(length)]
            for i, s in enumerate(states):
                data.append((s, F(rng.randint(-2, 4)), states[i + 1] if i + 1 < length else None))
        g = F(rng.randint(1, 9), 10)
        # Monte Carlo returns of every visit, then the normal equations of least squares.
        returns, acc = [], F(0)
        for s, r, nxt in reversed(data):
            acc = r + (g * acc if nxt is not None else 0)
            returns.append(acc)
        returns.reverse()
        gram = [[sum(phi[s][i] * phi[s][j] for s, _, _ in data) for j in range(3)] for i in range(3)]
        rhs = [sum(phi[s][i] * ret for (s, _, _), ret in zip(data, returns)) for i in range(3)]
        try:
            expected = solve(gram, rhs)
        except ValueError:
            continue
        assert lstd(data, phi.get, 3, g, 1) == expected


def test_sampled_trajectory_approaches_td_fixed_point() -> None:
    p = [[float(x) for x in row] for row in P]
    phf = {s: [float(x) for x in v] for s, v in PHI.items()}.get
    target = [185 / 109, 70 / 109]
    for seed in range(3):
        rng = random.Random(seed)
        s, data = 0, []
        for _ in range(20000):
            nxt = rng.choices(range(3), weights=p[s])[0]
            data.append((s, float(R[s]), nxt))
            s = nxt
        assert math.dist(lstd(data, phf, 2, 0.9), target) < 0.06


def test_rejects_bad_input() -> None:
    try:
        lstd([(0, F(0), 0)], PHI.get, 2, G)
    except ValueError:
        pass
    else:
        raise AssertionError("one transition gives a singular A")
    try:
        recursive_lstd(DATA, PHI.get, 2, G, 0, 0)
    except ValueError:
        return
    raise AssertionError("epsilon 0 must be rejected")
