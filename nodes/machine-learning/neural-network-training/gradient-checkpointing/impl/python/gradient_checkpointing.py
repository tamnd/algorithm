# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-checkpointing/. The authors are listed in prov/6X8J45.jsonl.
"""Gradient checkpointing with segments of length k on a chain of layers.

The chain is x_i = tanh(W_i x_(i-1) + b_i) for i = 1..n with the loss
0.5 * ||x_n||^2. backprop_full keeps all inputs x_0..x_(n-1) for the backward
pass. backprop_checkpointed keeps only the segment inputs x_0, x_k, x_2k, ...
and, segment by segment from the last one, recomputes the other inputs of the
segment before running backpropagation through it (Chen et al. 2016). With
k = ceil(sqrt(n)) the peak number of kept states is at most about 2 sqrt(n),
and the recomputation costs n - ceil(n / k) extra layer evaluations.

Both functions return (grads, dx0, stats) where stats counts the layer
evaluations and the largest number of states kept at one time.
"""

import math
from typing import Sequence

Vector = list[float]


def layer(W, b, x: Vector) -> Vector:
    return [math.tanh(sum(w * v for w, v in zip(row, x)) + c) for row, c in zip(W, b)]


def layer_vjp(W, x: Vector, y: Vector, gy: Vector):
    """Backward rule of one layer: given x, y = layer(x) and gy = dL/dy,
    return (dL/dW, dL/db, dL/dx)."""
    d = [g * (1.0 - v * v) for g, v in zip(gy, y)]
    gW = [[di * v for v in x] for di in d]
    gx = [sum(W[i][j] * d[i] for i in range(len(d))) for j in range(len(x))]
    return gW, d, gx


class Counter:
    def __init__(self):
        self.evals = 0
        self.live = 0
        self.peak = 0

    def keep(self, m: int = 1):
        self.live += m
        self.peak = max(self.peak, self.live)

    def drop(self, m: int = 1):
        self.live -= m


def backprop_full(Ws: Sequence, bs: Sequence, x0: Vector):
    n = len(Ws)
    c = Counter()
    xs = [list(x0)]
    c.keep()
    for i in range(n):
        y = layer(Ws[i], bs[i], xs[-1])
        c.evals += 1
        if i < n - 1:
            xs.append(y)
            c.keep()
    g = list(y)  # dL/dx_n for L = 0.5 ||x_n||^2
    grads = [None] * n
    for i in range(n - 1, -1, -1):
        gW, gb, g = layer_vjp(Ws[i], xs[i], y, g)
        grads[i] = (gW, gb)
        if i > 0:
            y = xs[i]
        c.drop()
    return grads, g, c


def backprop_checkpointed(Ws: Sequence, bs: Sequence, x0: Vector, k: int | None = None):
    n = len(Ws)
    if k is None:
        k = max(1, math.isqrt(n - 1) + 1) if n > 1 else 1  # ceil(sqrt(n))
    c = Counter()
    ckpt = {0: list(x0)}
    c.keep()
    x = list(x0)
    for i in range(1, n + 1):  # @line L1
        x = layer(Ws[i - 1], bs[i - 1], x)  # @line L2
        c.evals += 1
        if i % k == 0 and i < n:  # @line L3
            ckpt[i] = x  # @line L3
            c.keep()
    g = list(x)  # @line L4
    grads = [None] * n
    for a in reversed(range(0, n, k)):  # @line L5
        e = min(a + k, n)
        seg = [ckpt[a]]  # the inputs x_a .. x_(e-1) of the layers a+1 .. e
        for i in range(a + 1, e):  # @line L6
            seg.append(layer(Ws[i - 1], bs[i - 1], seg[-1]))  # @line L6
            c.evals += 1
            c.keep()
        y = x if e == n else ckpt[e]  # the output x_e of the segment
        for i in range(e, a, -1):  # @line L7
            xin = seg[i - 1 - a]
            gW, gb, g = layer_vjp(Ws[i - 1], xin, y, g)  # @line L8
            grads[i - 1] = (gW, gb)
            y = xin
        c.drop(len(seg) - 1)  # @line L9
        if e < n:  # the checkpoint x_e is no longer needed
            del ckpt[e]
            c.drop()
    c.drop()  # x_0
    return grads, g, c  # @line L10
