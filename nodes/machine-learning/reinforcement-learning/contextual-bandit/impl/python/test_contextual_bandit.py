# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contextual-bandit/. The authors are listed in prov/FHH31V.jsonl.

import random
from fractions import Fraction

from contextual_bandit import LinUCB, LinearInstance, dot, identity, mat_vec, run_linucb, sherman_morrison


def inverse(M):
    """Gauss-Jordan inversion with exact Fractions."""
    d = len(M)
    aug = [list(row) + [Fraction(int(i == j)) for j in range(d)] for i, row in enumerate(M)]
    for c in range(d):
        p = next(r for r in range(c, d) if aug[r][c] != 0)
        aug[c], aug[p] = aug[p], aug[c]
        piv = aug[c][c]
        aug[c] = [v / piv for v in aug[c]]
        for r in range(d):
            if r != c and aug[r][c] != 0:
                f = aug[r][c]
                aug[r] = [a - f * b for a, b in zip(aug[r], aug[c])]
    return [row[d:] for row in aug]


def test_sherman_morrison_matches_direct_inverse_exactly() -> None:
    rng = random.Random(11)
    for d in (1, 2, 3, 5):
        A = identity(d, Fraction(1))
        A_inv = identity(d, Fraction(1))
        for _ in range(12):
            x = [Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(d)]
            A = [[A[i][j] + x[i] * x[j] for j in range(d)] for i in range(d)]
            A_inv = sherman_morrison(A_inv, x)
            assert A_inv == inverse(A)


def test_policy_state_is_ridge_regression_exactly() -> None:
    rng = random.Random(12)
    k, d = 3, 3
    pol = LinUCB(k, d, 0, one=Fraction(1))
    data = {a: [] for a in range(k)}
    for _ in range(30):
        xs = [[Fraction(rng.randint(-3, 3), 2) for _ in range(d)] for _ in range(k)]
        a = pol.choose(xs)
        r = Fraction(rng.randint(0, 10), 10)
        pol.update(a, xs[a], r)
        data[a].append((xs[a], r))
    for a in range(k):
        A = identity(d, Fraction(1))
        b = [Fraction(0)] * d
        for x, r in data[a]:
            A = [[A[i][j] + x[i] * x[j] for j in range(d)] for i in range(d)]
            b = [bi + r * xi for bi, xi in zip(b, x)]
        assert pol.A_inv[a] == inverse(A)
        assert pol.b[a] == b


def test_trace_of_the_page() -> None:
    thetas = [[1.0, 0.0], [0.4, 0.6]]
    seq = [[1.0, 0.0], [0.0, 1.0], [0.0, 1.0], [1.0, 0.0], [0.6, 0.8], [0.0, 1.0]]
    pol = LinUCB(2, 2, 1.0)
    arms, scores = [], []
    for x in seq:
        scores.append([round(v, 3) for v in pol.scores([x, x])])
        a = pol.choose([x, x])
        pol.update(a, x, dot(thetas[a], x))
        arms.append(a)
    assert arms == [0, 0, 1, 0, 1, 1]
    assert scores[4] == [1.063, 1.065]
    assert [[round(v, 3) for v in row] for row in pol.A_inv[1]] == [[0.771, -0.102], [-0.102, 0.288]]
    assert [round(v, 3) for v in mat_vec(pol.A_inv[1], pol.b[1])] == [0.153, 0.468]


def test_regret_is_sublinear_on_a_seeded_instance() -> None:
    n, k, d = 4000, 5, 6
    lin = [0.0, 0.0]
    uni = [0.0, 0.0]
    for s in range(3):
        inst = LinearInstance(k, d, n, random.Random(s))
        cr = inst.regret(run_linucb(inst.contexts, inst.reward, k, d, n, 1.0))
        lin[0] += cr[999]
        lin[1] += cr[n - 1]
        rng = random.Random(100 + s)
        cu = inst.regret([rng.randrange(k) for _ in range(n)])
        uni[0] += cu[999]
        uni[1] += cu[n - 1]
    # Four times the rounds: the uniform policy has about four times the regret, LinUCB much less.
    assert 3.5 < uni[1] / uni[0] < 4.5
    assert lin[1] / lin[0] < 1.5
    assert lin[1] < uni[1] / 50
