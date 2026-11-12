# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/representer-theorem/. The authors are listed in prov/BWRZ8V.jsonl.

import math
import random

from representer_theorem import (
    distance_to_span,
    dot,
    kernel,
    logistic_gradient_descent,
    logistic_objective,
    phi,
    ridge_dual,
    ridge_in_feature_space,
)

XS = [(0.0, 0.0), (1.0, 0.5), (-0.5, 1.0), (0.8, -1.2)]
YS = [1.0, -1.0, 1.0, -1.0]


def test_feature_map_matches_kernel() -> None:
    rng = random.Random(1)
    for _ in range(50):
        x = (rng.uniform(-2, 2), rng.uniform(-2, 2))
        z = (rng.uniform(-2, 2), rng.uniform(-2, 2))
        assert math.isclose(dot(phi(x), phi(z)), kernel(x, z), rel_tol=1e-12)


def test_ridge_minimizer_lies_in_the_span_and_matches_the_dual() -> None:
    basis = [phi(x) for x in XS]
    for lam in (0.01, 0.5, 3.0):
        w = ridge_in_feature_space(XS, YS, lam)
        assert distance_to_span(w, basis) < 1e-9
        alpha = ridge_dual(XS, YS, lam)
        w2 = [sum(a * b[k] for a, b in zip(alpha, basis)) for k in range(6)]
        assert all(abs(u - v) < 1e-9 for u, v in zip(w, w2))


def test_logistic_minimizer_from_outside_the_span_ends_in_the_span() -> None:
    basis = [phi(x) for x in XS]
    rng = random.Random(1971)
    w0 = [rng.uniform(-3, 3) for _ in range(6)]
    assert distance_to_span(w0, basis) > 0.1
    w = logistic_gradient_descent(XS, YS, lam=0.2, w0=w0, steps=4000, eta=0.05)
    assert distance_to_span(w, basis) < 1e-8
    # Projecting a non-span point onto the span lowers the objective.
    perp = [1.0, 0.0, 0.0, 0.0, 0.0, -1.0]
    r = distance_to_span(perp, basis)
    assert r > 0.1
    w_bad = [a + 0.5 * b for a, b in zip(w, perp)]
    assert logistic_objective(w_bad, XS, YS, 0.2) > logistic_objective(w, XS, YS, 0.2)


def test_without_a_strictly_increasing_regularizer_minimizers_can_leave_the_span() -> None:
    # g = 0: any w that interpolates is a minimizer of the squared loss alone.
    xs = XS[:3]
    ys = YS[:3]
    basis = [phi(x) for x in xs]
    w_span = ridge_in_feature_space(xs, ys, 1e-12)  # an interpolant in the span
    # find a vector orthogonal to the three features: the null space of a 3 x 6 system
    v = [0.0] * 6
    for trial in range(6):
        e = [1.0 if k == trial else 0.0 for k in range(6)]
        if distance_to_span(e, basis) > 0.1:
            # e minus its projection onto the span
            q = []
            for b in basis:
                u = list(b)
                for f in q:
                    c = dot(u, f)
                    u = [a - c * t for a, t in zip(u, f)]
                n = math.sqrt(dot(u, u))
                q.append([a / n for a in u])
            v = list(e)
            for f in q:
                c = dot(v, f)
                v = [a - c * t for a, t in zip(v, f)]
            break
    w_other = [a + b for a, b in zip(w_span, v)]
    assert distance_to_span(w_other, basis) > 0.1
    for x, y in zip(xs, ys):
        assert abs(dot(w_other, phi(x)) - y) < 1e-6  # same zero loss
