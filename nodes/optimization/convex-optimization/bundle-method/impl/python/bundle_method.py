# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bundle-method/. The authors are listed in prov/M2Z5AG.jsonl.

"""A proximal bundle method with a two-cut bundle (the aggregate cut and the newest cut).

    minimize f(x) over R^n, for a convex f given by an oracle x -> (f(x), g in the subdifferential).

A cut is stored as (h, g), the affine function y -> h + g^T (y - c) with c the current center, so h is
its value at the center. For a bundle of one or two cuts, the proximal subproblem

    minimize  max(cuts)(y) + ||y - c||^2 / (2 t)

has the dual  max over lambda in [0, 1] of  phi(lambda a + (1 - lambda) b),  phi(h, g) = h - (t/2) ||g||^2,
whose maximizer lambda has a closed form. The aggregate cut (h_a, g_a) = lambda a + (1 - lambda) b
gives the candidate y = c - t g_a and the predicted decrease v = f(c) - h_a + t ||g_a||^2.

Serious step if f(c) - f(y) >= kappa v: move the center to y and restart the bundle with the cut at y.
Null step otherwise: keep the center, and the new bundle is the aggregate cut and the cut at y.
The method stops when v <= eps; then f(c) - f(z) <= eps + sqrt(eps / t) ||z - c|| for every z.

Cost of one iteration: one oracle call and O(n) arithmetic.
"""

from dataclasses import dataclass, field


@dataclass
class BundleResult:
    x: list  # the last center
    fx: object
    history: list = field(default_factory=list)  # one dict per iteration


def dot(u, v):
    return sum(p * q for p, q in zip(u, v))


def best_lambda(a, b, t):
    """Maximizer over [0, 1] of phi(lambda a + (1 - lambda) b) with phi(h, g) = h - (t/2)||g||^2."""
    (ha, ga), (hb, gb) = a, b
    d = [p - q for p, q in zip(ga, gb)]
    dd = dot(d, d)
    if dd == 0:
        return 1 if ha >= hb else 0
    lam = ((ha - hb) / t - dot(d, gb)) / dd
    return min(max(lam, 0), 1)


def proximal_bundle(oracle, x0, t, kappa, eps=0, max_iter=1000) -> BundleResult:
    """oracle(x) returns (f(x), g). t > 0 is the prox parameter and 0 < kappa < 1 the descent fraction."""
    fx, g = oracle(x0)  # @line L1
    center, fc, bundle = list(x0), fx, [(fx, g)]
    res = BundleResult(center, fc)
    for _ in range(max_iter):  # @line L2
        lam = 1 if len(bundle) == 1 else best_lambda(bundle[0], bundle[1], t)  # @line L3
        other = bundle[-1]
        ha = lam * bundle[0][0] + (1 - lam) * other[0]  # @line L4
        ga = [lam * p + (1 - lam) * q for p, q in zip(bundle[0][1], other[1])]
        y = [ci - t * gi for ci, gi in zip(center, ga)]  # @line L5
        v = fc - ha + t * dot(ga, ga)
        step = {"center": center, "fc": fc, "bundle": bundle, "lam": lam, "ha": ha, "ga": ga, "y": y, "v": v}
        res.history.append(step)
        if v <= eps:  # @line L6
            break
        fy, gy = oracle(y)  # @line L7
        step["fy"], step["gy"] = fy, gy
        step["serious"] = fc - fy >= kappa * v  # @line L8
        if step["serious"]:
            center, fc, bundle = y, fy, [(fy, gy)]  # @line L9
        else:  # @line L10
            bundle = [(ha, ga), (fy + dot(gy, [p - q for p, q in zip(center, y)]), gy)]  # @line L11
    res.x, res.fx = center, fc
    return res  # @line L12
