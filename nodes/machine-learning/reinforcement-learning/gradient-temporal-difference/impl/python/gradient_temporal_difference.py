# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-temporal-difference/. The authors are listed in prov/065TYG.jsonl.

"""Gradient temporal-difference learning with linear features: TDC and GTD2, on- and off-policy.

A sample is (x, rho, r, x_next): the features of the state, the importance ratio pi(a|s) / mu(a|s)
of the action taken, the reward and the features of the next state. Both methods minimize the
mean squared projected Bellman error MSPBE(theta) = (b - A theta)^T C^(-1) (b - A theta), with
A = E[rho x (x - gamma x')^T], b = E[rho r x] and C = E[x x^T].
"""

import random
from fractions import Fraction
from typing import Callable, Sequence

Vector = list[float]
Sample = tuple[Sequence[float], float, float, Sequence[float]]


def _dot(u: Sequence, v: Sequence):
    return sum(a * b for a, b in zip(u, v))


def gradient_td(
    sample: Callable[[random.Random], Sample],
    theta0: Sequence[float],
    gamma: float,
    alpha: Callable[[int], float],
    beta: Callable[[int], float],
    steps: int,
    rng: random.Random,
    variant: str = "tdc",
) -> tuple[Vector, Vector]:
    """Run TDC or GTD2 for `steps` samples. Returns (theta, w). O(d) time per step."""
    if variant not in ("tdc", "gtd2"):
        raise ValueError("variant must be 'tdc' or 'gtd2'")
    d = len(theta0)
    theta, w = list(theta0), [0.0] * d  # @line L1
    for k in range(steps):  # @line L2
        x, rho, r, x_next = sample(rng)  # @line L3
        delta = r + gamma * _dot(x_next, theta) - _dot(x, theta)  # @line L4
        xw = _dot(x, w)
        a, b = alpha(k), beta(k)
        if variant == "tdc":  # @line L5
            theta = [t + a * rho * (delta * xi - gamma * xn * xw) for t, xi, xn in zip(theta, x, x_next)]
        else:  # @line L6
            theta = [t + a * rho * (xi - gamma * xn) * xw for t, xi, xn in zip(theta, x, x_next)]
        w = [wi + b * rho * (delta - xw) * xi for wi, xi in zip(w, x)]  # @line L7
    return theta, w  # @line L8


def off_policy_semi_gradient_td(
    sample: Callable[[random.Random], Sample],
    theta0: Sequence[float],
    gamma: float,
    alpha: Callable[[int], float],
    steps: int,
    rng: random.Random,
) -> Vector:
    """Semi-gradient TD(0) weighted by rho, for comparison: theta += alpha rho delta x."""
    theta = list(theta0)
    for k in range(steps):
        x, rho, r, x_next = sample(rng)
        delta = r + gamma * _dot(x_next, theta) - _dot(x, theta)
        theta = [t + alpha(k) * rho * delta * xi for t, xi in zip(theta, x)]
    return theta


def expected_matrices(
    features: Sequence[Sequence], d_state: Sequence, p_target: Sequence[Sequence], rewards: Sequence, gamma
) -> tuple[list[list], list, list[list], list[list]]:
    """A, b, C and E = E[rho x' x^T] when states are drawn from d_state and pi has transitions p_target.

    E[rho f(s, s')] over mu equals the expectation of f under the target transitions, so
    A = X^T D (I - gamma P) X, b = X^T D r, C = X^T D X and E = X^T P^T D X.
    """
    n, d = len(features), len(features[0])
    px = [[sum(p_target[s][t] * features[t][k] for t in range(n)) for k in range(d)] for s in range(n)]
    a = [[sum(d_state[s] * features[s][i] * (features[s][j] - gamma * px[s][j]) for s in range(n)) for j in range(d)] for i in range(d)]
    b = [sum(d_state[s] * features[s][i] * rewards[s] for s in range(n)) for i in range(d)]
    c = [[sum(d_state[s] * features[s][i] * features[s][j] for s in range(n)) for j in range(d)] for i in range(d)]
    e = [[sum(d_state[s] * px[s][i] * features[s][j] for s in range(n)) for j in range(d)] for i in range(d)]
    return a, b, c, e


def expected_step(theta, w, a, b, c, e, gamma, alpha, beta, variant: str = "tdc"):
    """One step of the mean ODE of TDC or GTD2, or of semi-gradient TD if variant is 'td'."""
    d = len(theta)
    res = [b[i] - _dot(a[i], theta) for i in range(d)]  # E[rho delta x]
    if variant == "td":
        return [theta[i] + alpha * res[i] for i in range(d)], w
    cw = [_dot(c[i], w) for i in range(d)]
    if variant == "tdc":
        ew = [_dot(e[i], w) for i in range(d)]
        new_theta = [theta[i] + alpha * (res[i] - gamma * ew[i]) for i in range(d)]
    else:
        new_theta = [theta[i] + alpha * sum(a[j][i] * w[j] for j in range(d)) for i in range(d)]
    new_w = [w[i] + beta * (res[i] - cw[i]) for i in range(d)]
    return new_theta, new_w


def baird(rng_unused=None):
    """Baird's counterexample: 7 states, 8 weights, gamma = 0.99, all rewards 0.

    Returns (features, sample). States 0 to 5 are the upper states with value 2 w_i + w_7;
    state 6 is the lower state with value w_6 + 2 w_7. From any state the behavior policy takes
    the dashed action with probability 6/7 (to a uniform upper state) and the solid action with
    probability 1/7 (to state 6). The target policy always takes solid. States are drawn uniformly.
    """
    feats = []
    for i in range(6):
        f = [0.0] * 8
        f[i], f[7] = 2.0, 1.0
        feats.append(f)
    feats.append([0.0] * 6 + [1.0, 2.0])

    def sample(rng: random.Random) -> Sample:
        s = rng.randrange(7)
        if rng.random() < 6 / 7:
            return feats[s], 0.0, 0.0, feats[rng.randrange(6)]
        return feats[s], 7.0, 0.0, feats[6]

    return feats, sample


BAIRD_THETA0 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 10.0, 1.0]


def as_fractions(m):
    return [[Fraction(x) for x in row] for row in m]
