# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadly-triad/. The authors are listed in prov/4D15PJ.jsonl.

"""Small exact demonstrations of the deadly triad: function approximation, bootstrapping and
off-policy training together can make linear TD diverge, while any two of the three are safe.

All functions work with floats or Fractions. A chain is given by the transition matrix p of the
target policy, expected rewards r and discount gamma; features are the rows x(s).
"""

from fractions import Fraction
from typing import Sequence

Number = float | Fraction


def _dot(u: Sequence, v: Sequence):
    return sum(a * b for a, b in zip(u, v))


def true_values(p: Sequence[Sequence[Number]], r: Sequence[Number], gamma: Number) -> list[Number]:
    """V = (I - gamma P)^(-1) r. A row of P may sum to less than 1 (termination)."""
    n = len(r)
    return solve([[(1 if i == j else 0) - gamma * p[i][j] for j in range(n)] for i in range(n)], r)


def solve(a: Sequence[Sequence[Number]], b: Sequence[Number]) -> list[Number]:
    """Solve a x = b by Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        k = max(range(c, n), key=lambda i: abs(m[i][c]))
        m[c], m[k] = m[k], m[c]
        for i in range(n):
            if i != c and m[i][c] != 0:
                f = m[i][c] / m[c][c]
                m[i] = [u - f * v for u, v in zip(m[i], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def expected_update(
    feats: Sequence[Sequence[Number]],
    p: Sequence[Sequence[Number]],
    r: Sequence[Number],
    gamma: Number,
    d: Sequence[Number],
    w: Sequence[Number],
    alpha: Number,
    targets: Sequence[Number] | None = None,
) -> list[Number]:
    """One expected semi-gradient update w + alpha sum_s d(s) (target(s) - x(s)^T w) x(s).

    With targets None the target bootstraps: r(s) + gamma sum_s' p(s, s') x(s')^T w (expected TD,
    or dynamic programming with linear features). Otherwise the given targets are used (Monte Carlo).
    The weighting d is the distribution of the updates; it is off-policy when it is not the
    on-policy distribution of p.
    """
    n, k = len(feats), len(w)
    v = [_dot(f, w) for f in feats]
    step = [0] * k
    for s in range(n):
        if d[s] == 0:
            continue
        t = targets[s] if targets is not None else r[s] + gamma * sum(p[s][u] * v[u] for u in range(n))
        step = [a + d[s] * (t - v[s]) * x for a, x in zip(step, feats[s])]
    return [wi + alpha * si for wi, si in zip(w, step)]


def w_to_2w_factor(gamma: Number, alpha: Number) -> Number:
    """Off-policy TD on the transition from a state of value w to a state of value 2w, reward 0.

    delta = gamma 2w - w, so w <- w + alpha (2 gamma - 1) w. The factor exceeds 1 when gamma > 1/2.
    """
    return 1 + alpha * (2 * gamma - 1)


def projected_value_iteration(
    feats: Sequence[Sequence[Number]],
    p: Sequence[Sequence[Number]],
    r: Sequence[Number],
    gamma: Number,
    d: Sequence[Number],
    w0: Sequence[Number],
    steps: int,
) -> list[list[Number]]:
    """w_(k+1) = argmin_w sum_s d(s) (x(s)^T w - (r(s) + gamma sum p v_k))^2, exactly. Returns all w_k."""
    n, k = len(feats), len(w0)
    ws = [list(w0)]
    gram = [[sum(d[s] * feats[s][i] * feats[s][j] for s in range(n)) for j in range(k)] for i in range(k)]
    for _ in range(steps):
        v = [_dot(f, ws[-1]) for f in feats]
        t = [r[s] + gamma * sum(p[s][u] * v[u] for u in range(n)) for s in range(n)]
        rhs = [sum(d[s] * feats[s][i] * t[s] for s in range(n)) for i in range(k)]
        ws.append(solve(gram, rhs))
    return ws


def tvr_example(eps: Number) -> tuple[list[list[Number]], list[list[Number]], list[Number]]:
    """Two states with features 1 and 2. State 0 goes to state 1; state 1 stays with probability 1 - eps
    and otherwise terminates. All rewards are 0. Returns (features, p, r)."""
    return [[1], [2]], [[0, 1], [0, 1 - eps]], [0, 0]


def baird_example(gamma: Number = Fraction(99, 100)):
    """Baird's counterexample under the target policy (always solid, to the lower state 6).

    Returns (features, p, r). Upper states 0..5 have value 2 w_i + w_7, the lower state 6 has w_6 + 2 w_7.
    """
    feats = []
    for i in range(6):
        f = [0] * 8
        f[i], f[7] = 2, 1
        feats.append(f)
    feats.append([0] * 6 + [1, 2])
    p = [[0] * 6 + [1] for _ in range(7)]
    return feats, p, [0] * 7
