# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-bound-propagation/. The authors are listed in prov/2XBS61.jsonl.

"""Linear bound propagation in the style of CROWN for feed-forward ReLU networks.

A network is a list of affine layers (W, b), with a ReLU after every layer except the
last. Each unstable ReLU, with pre-activation bounds l < 0 < u, is bounded above by the
chord u (z - l) / (u - l) and below by alpha z, with alpha = 1 if u >= -l and 0 if not
(the adaptive choice of Zhang et al. 2018). A backward pass turns a linear objective
of one layer into a linear function of the input, which is then minimized over the
input box in closed form. The bounds hold in exact arithmetic; floats add rounding.

The models in the tests are synthetic networks built from a fixed seed.
"""

from typing import Sequence

Vector = list[float]
Matrix = list[list[float]]
Layer = tuple[list[list[float]], list[float]]


def layers_from_net(net: dict) -> list[Layer]:
    """The two layers of a tiny_relu_net dict of mlkit. Cost O(h d + k h)."""
    return [([list(r) for r in net["W1"]], list(net["b1"])), ([list(r) for r in net["W2"]], list(net["b2"]))]


def forward(layers: Sequence[Layer], x: Sequence[float]) -> Vector:
    """The outputs of the last layer at x. Cost O(sum of the layer sizes)."""
    a = list(x)
    for k, (w, b) in enumerate(layers):
        a = [sum(wi * ai for wi, ai in zip(row, a, strict=True)) + bi for row, bi in zip(w, b, strict=True)]
        if k < len(layers) - 1:
            a = [max(v, 0.0) for v in a]
    return a


def relaxation(l: float, u: float) -> tuple[float, float, float, float]:
    """(upper slope, upper intercept, lower slope, lower intercept) of relu on [l, u].

    Precondition l <= u. Every z in [l, u] has
    lower slope * z + lower intercept <= relu(z) <= upper slope * z + upper intercept.
    """
    if u <= 0.0:
        return 0.0, 0.0, 0.0, 0.0
    if l >= 0.0:
        return 1.0, 0.0, 1.0, 0.0
    s = u / (u - l)
    alpha = 1.0 if u >= -l else 0.0
    return s, -s * l, alpha, 0.0


def backward_bound(layers: Sequence[Layer], k: int, lam: Matrix, bounds: Sequence[tuple[Vector, Vector]],
                   lower: Sequence[float], upper: Sequence[float]) -> Vector:
    """Lower bounds of the rows of lam times z_k over the box, where z_k is the output of layer k (0-based).

    bounds[j] holds (l, u) for the pre-activations of layer j, for every j < k.
    Precondition: lower <= upper, and the sizes match. Cost O(r N) for r rows and N
    weights in the layers 0 .. k.
    """
    a = [list(row) for row in lam]  # @line L1
    c = [0.0] * len(a)  # @line L1
    for j in range(k, -1, -1):  # @line L2
        w, b = layers[j]
        for r, row in enumerate(a):  # @line L3
            c[r] += sum(ai * bi for ai, bi in zip(row, b, strict=True))  # @line L3
        a = [[sum(row[i] * w[i][t] for i in range(len(w))) for t in range(len(w[0]))] for row in a]  # @line L4
        if j > 0:  # @line L5
            lj, uj = bounds[j - 1]
            for i in range(len(lj)):  # @line L6
                su, iu, sl, il = relaxation(lj[i], uj[i])  # @line L7
                for r, row in enumerate(a):  # @line L8
                    if row[i] >= 0.0:  # @line L9
                        c[r] += row[i] * il  # @line L9
                        row[i] *= sl  # @line L9
                    else:  # @line L10
                        c[r] += row[i] * iu  # @line L10
                        row[i] *= su  # @line L10
    out = []
    for r, row in enumerate(a):  # @line L11
        out.append(c[r] + sum(ai * (lo if ai >= 0.0 else hi) for ai, lo, hi in zip(row, lower, upper, strict=True)))  # @line L11
    return out  # @line L12


def linear_bound_propagation(layers: Sequence[Layer], lower: Sequence[float], upper: Sequence[float],
                             spec: Matrix) -> Vector:
    """Lower bounds of spec times the network output, over the box [lower, upper].

    The pre-activation bounds of each hidden layer are computed first, by the same
    backward pass with the identity and its negation as objectives.
    Precondition: lower <= upper; spec has as many columns as the last layer has rows.
    Cost O(K n N) for K layers, n units per layer at most and N weights in total.
    """
    bounds: list[tuple[Vector, Vector]] = []
    for k in range(len(layers) - 1):  # @line L13
        n = len(layers[k][0])
        eye = [[1.0 if i == t else 0.0 for t in range(n)] for i in range(n)]
        neg = [[-v for v in row] for row in eye]
        lo = backward_bound(layers, k, eye, bounds, lower, upper)  # @line L14
        hi = [-v for v in backward_bound(layers, k, neg, bounds, lower, upper)]  # @line L14
        bounds.append((lo, hi))  # @line L14
    return backward_bound(layers, len(layers) - 1, spec, bounds, lower, upper)  # @line L15


def margin_spec(k: int, y: int) -> Matrix:
    """The rows e_y - e_j for j != y, so that spec times z is the vector of margins. Cost O(k^2)."""
    return [[(1.0 if t == y else 0.0) - (1.0 if t == j else 0.0) for t in range(k)] for j in range(k) if j != y]


def certify_crown(layers: Sequence[Layer], x: Sequence[float], y: int, epsilon: float) -> tuple[bool, Vector]:
    """Try to certify that y is the only argmax on B_infinity(x, epsilon) in [0, 1]^d.

    Returns (certified, l) with l the lower bounds of z_y - z_j for j != y. True is a
    proof in exact arithmetic; False proves nothing. Cost as linear_bound_propagation.
    """
    lower = [max(a - epsilon, 0.0) for a in x]
    upper = [min(a + epsilon, 1.0) for a in x]
    lo = linear_bound_propagation(layers, lower, upper, margin_spec(len(layers[-1][0]), y))
    return all(v > 0.0 for v in lo), lo
