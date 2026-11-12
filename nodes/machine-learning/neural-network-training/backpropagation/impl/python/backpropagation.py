# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backpropagation/. The authors are listed in prov/7N4K94.jsonl.
"""Backpropagation for a multilayer perceptron with the squared loss.

The network has layers l = 1..L with weights W[l] (n_l x n_(l-1)), biases b[l]
and elementwise activations acts[l] in {"tanh", "relu", "sigmoid", "identity"}.
The loss on one example is 0.5 * ||a_L - y||^2. backprop returns the gradient of
that loss with respect to every W[l] and b[l] by the delta recursion
delta_(l-1) = (W_l^T delta_l) * f'_(l-1)(z_(l-1)).

Cost per example: about 3P multiply-adds for P weights, and memory for the
pre-activations and activations of all layers. Lists are 0-based: W[0] is W_1.
"""

import math
import random
from typing import Sequence

Matrix = list[list[float]]
Vector = list[float]


def act(name: str, z: float) -> float:
    if name == "tanh":
        return math.tanh(z)
    if name == "relu":
        return z if z > 0 else 0.0
    if name == "sigmoid":
        return 1.0 / (1.0 + math.exp(-z))
    return z


def act_prime(name: str, z: float) -> float:
    """The derivative; ReLU uses the convention f'(0) = 0."""
    if name == "tanh":
        t = math.tanh(z)
        return 1.0 - t * t
    if name == "relu":
        return 1.0 if z > 0 else 0.0
    if name == "sigmoid":
        s = 1.0 / (1.0 + math.exp(-z))
        return s * (1.0 - s)
    return 1.0


def forward(W: Sequence[Matrix], b: Sequence[Vector], acts: Sequence[str], x: Vector):
    """Return the lists zs and as_ (as_[0] is the input)."""
    a = list(x)
    zs, as_ = [], [a]
    for Wl, bl, f in zip(W, b, acts):
        z = [sum(w * v for w, v in zip(row, a)) + c for row, c in zip(Wl, bl)]
        a = [act(f, t) for t in z]
        zs.append(z)
        as_.append(a)
    return zs, as_


def loss(W, b, acts, x: Vector, y: Vector) -> float:
    _, as_ = forward(W, b, acts, x)
    return 0.5 * sum((p - q) ** 2 for p, q in zip(as_[-1], y))


def backprop(W: Sequence[Matrix], b: Sequence[Vector], acts: Sequence[str], x: Vector, y: Vector):
    """Return (gW, gb): the gradients of 0.5 * ||a_L - y||^2 for one example."""
    L = len(W)
    a = list(x)  # @line L1
    zs, as_ = [], [a]
    for l in range(L):  # @line L2
        z = [sum(w * v for w, v in zip(row, a)) + c for row, c in zip(W[l], b[l])]  # @line L3
        a = [act(acts[l], t) for t in z]  # @line L4
        zs.append(z)
        as_.append(a)
    delta = [(p - q) * act_prime(acts[-1], t) for p, q, t in zip(as_[-1], y, zs[-1])]  # @line L5
    gW: list[Matrix] = [[] for _ in range(L)]
    gb: list[Vector] = [[] for _ in range(L)]
    for l in range(L - 1, -1, -1):  # @line L6
        prev = as_[l]
        gW[l] = [[d * v for v in prev] for d in delta]  # @line L7
        gb[l] = list(delta)  # @line L7
        if l > 0:  # @line L8
            back = [sum(W[l][i][j] * delta[i] for i in range(len(delta))) for j in range(len(prev))]
            delta = [s * act_prime(acts[l - 1], t) for s, t in zip(back, zs[l - 1])]  # @line L8
    return gW, gb  # @line L9


def batch_gradient(W, b, acts, X: Sequence[Vector], Y: Sequence[Vector]):
    """The gradient of the mean loss over a batch."""
    n = len(X)
    sW = [[[0.0] * len(r) for r in Wl] for Wl in W]
    sb = [[0.0] * len(bl) for bl in b]
    for x, y in zip(X, Y):
        gW, gb = backprop(W, b, acts, x, y)
        for l in range(len(W)):
            for i in range(len(W[l])):
                sb[l][i] += gb[l][i] / n
                for j in range(len(W[l][i])):
                    sW[l][i][j] += gW[l][i][j] / n
    return sW, sb


def init(sizes: Sequence[int], rng: random.Random, scale: float = 1.0):
    """Weights uniform in [-scale, scale] / sqrt(fan_in), biases 0."""
    W, b = [], []
    for m, n in zip(sizes[:-1], sizes[1:]):
        r = scale / math.sqrt(m)
        W.append([[rng.uniform(-r, r) for _ in range(m)] for _ in range(n)])
        b.append([0.0] * n)
    return W, b


def train(W, b, acts, X, Y, eta: float, steps: int) -> float:
    """Full batch gradient descent; returns the final mean loss."""
    for _ in range(steps):
        gW, gb = batch_gradient(W, b, acts, X, Y)
        for l in range(len(W)):
            for i in range(len(W[l])):
                b[l][i] -= eta * gb[l][i]
                for j in range(len(W[l][i])):
                    W[l][i][j] -= eta * gW[l][i][j]
    return sum(loss(W, b, acts, x, y) for x, y in zip(X, Y)) / len(X)
