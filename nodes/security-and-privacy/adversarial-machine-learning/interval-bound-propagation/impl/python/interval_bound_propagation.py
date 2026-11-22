# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-bound-propagation/. The authors are listed in prov/2WWJMG.jsonl.

"""Interval bound propagation (IBP) for feed-forward ReLU networks.

A network is a list of affine layers (W, b). A ReLU follows every layer except the
last one, so the logits are z = W_K relu(... relu(W_1 x + b_1) ...) + b_K. IBP pushes
a box through the layers in center and radius form. The bounds hold for every input
of the box, in exact arithmetic. With floats they can be off by rounding; a verifier
that must be sound on floats rounds outward (interval arithmetic).

The models in the tests are synthetic networks built from a fixed seed.
"""

from typing import Sequence

Vector = list[float]
Layer = tuple[list[list[float]], list[float]]


def layers_from_net(net: dict) -> list[Layer]:
    """The two layers of a tiny_relu_net dict of mlkit. Cost O(h d + k h)."""
    return [([list(r) for r in net["W1"]], list(net["b1"])), ([list(r) for r in net["W2"]], list(net["b2"]))]


def forward(layers: Sequence[Layer], x: Sequence[float]) -> Vector:
    """The logits of the network at x. Cost O(sum of the layer sizes)."""
    a = list(x)
    for k, (w, b) in enumerate(layers):
        a = [sum(wi * ai for wi, ai in zip(row, a, strict=True)) + bi for row, bi in zip(w, b, strict=True)]
        if k < len(layers) - 1:
            a = [max(v, 0.0) for v in a]
    return a


def interval_bound_propagation(layers: Sequence[Layer], lower: Sequence[float], upper: Sequence[float]) -> tuple[Vector, Vector]:
    """Lower and upper bounds of the outputs of the last layer over the box [lower, upper].

    Precondition: lower[j] <= upper[j] for every input j, and the layer sizes match.
    Every output f(x) of the network for x in the box satisfies l <= f(x) <= u.
    Cost O(N) for N weights in total, one matrix-vector product per layer for the
    center and one for the radius.
    """
    lo, hi = list(lower), list(upper)  # @line L1
    last = len(layers) - 1
    for k, (w, b) in enumerate(layers):  # @line L2
        mu = [(h + l) / 2.0 for l, h in zip(lo, hi, strict=True)]  # @line L3
        r = [(h - l) / 2.0 for l, h in zip(lo, hi, strict=True)]  # @line L3
        mu2 = [sum(wi * m for wi, m in zip(row, mu, strict=True)) + bi for row, bi in zip(w, b, strict=True)]  # @line L4
        r2 = [sum(abs(wi) * s for wi, s in zip(row, r, strict=True)) for row in w]  # @line L5
        lo = [m - s for m, s in zip(mu2, r2, strict=True)]  # @line L6
        hi = [m + s for m, s in zip(mu2, r2, strict=True)]  # @line L6
        if k < last:  # @line L7
            lo = [max(v, 0.0) for v in lo]  # @line L8
            hi = [max(v, 0.0) for v in hi]  # @line L8
    return lo, hi  # @line L9


def margin_layers(layers: Sequence[Layer], y: int) -> list[Layer]:
    """Fold the margins z_y - z_j, for j != y, into the last layer. Cost O(k h)."""
    w, b = layers[-1]
    rows = [[a - c for a, c in zip(w[y], w[j], strict=True)] for j in range(len(w)) if j != y]
    consts = [b[y] - b[j] for j in range(len(b)) if j != y]
    return [*layers[:-1], (rows, consts)]


def input_box(x: Sequence[float], epsilon: float) -> tuple[Vector, Vector]:
    """The box B_infinity(x, epsilon) intersected with [0, 1]^d. Cost O(d)."""
    return [max(a - epsilon, 0.0) for a in x], [min(a + epsilon, 1.0) for a in x]


def certify_ibp(layers: Sequence[Layer], x: Sequence[float], y: int, epsilon: float) -> tuple[bool, Vector]:
    """Try to certify that the label y is the only argmax on B_infinity(x, epsilon) in [0, 1]^d.

    Returns (certified, l) with l the lower bounds of the margins z_y - z_j, j != y,
    in the order of j. A True answer is a proof in exact arithmetic; a False answer
    proves nothing. Precondition: epsilon >= 0, x in [0, 1]^d, 0 <= y < k.
    Cost O(N) for N weights in total.
    """
    lower, upper = input_box(x, epsilon)  # @line L10
    spec = margin_layers(layers, y)  # @line L11
    lo, _ = interval_bound_propagation(spec, lower, upper)  # @line L12
    return all(v > 0.0 for v in lo), lo  # @line L13
