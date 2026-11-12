# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backpropagation-through-time/. The authors are listed in prov/W0KS2M.jsonl.
"""Backpropagation through time for an Elman recurrent network.

The network is
    h_t = tanh(W h_(t-1) + U x_t + b),   o_t = V h_t + c,
with the loss L = sum_t 0.5 * ||o_t - y_t||^2. Parameters are a dict with the
keys "W" (H x H), "U" (H x D), "b" (H), "V" (O x H) and "c" (O).

bptt unrolls the network over the whole sequence, keeps all T + 1 hidden
states, and sweeps back once: Theta(T (H^2 + HD + OH)) time, Theta(T H) memory.
truncated_bptt cuts the sequence into chunks of k steps, carries the hidden
state forward across chunks and the error signal not at all: Theta(k H) memory.
"""

import math
from typing import Sequence

Vector = list[float]
Matrix = list[list[float]]


def matvec(M: Matrix, v: Vector) -> Vector:
    return [sum(m * x for m, x in zip(row, v)) for row in M]


def matTvec(M: Matrix, v: Vector) -> Vector:
    """M^T v."""
    out = [0.0] * len(M[0])
    for row, s in zip(M, v):
        for j, m in enumerate(row):
            out[j] += m * s
    return out


def add_outer(G: Matrix, u: Vector, v: Vector) -> None:
    """G += u v^T in place."""
    for i, s in enumerate(u):
        row = G[i]
        for j, x in enumerate(v):
            row[j] += s * x


def zeros_like(p: dict) -> dict:
    g = {}
    for k, v in p.items():
        g[k] = [[0.0] * len(r) for r in v] if isinstance(v[0], list) else [0.0] * len(v)
    return g


def step(p: dict, h: Vector, x: Vector) -> Vector:
    a = [s + t + c for s, t, c in zip(matvec(p["W"], h), matvec(p["U"], x), p["b"])]
    return [math.tanh(z) for z in a]


def output(p: dict, h: Vector) -> Vector:
    return [s + c for s, c in zip(matvec(p["V"], h), p["c"])]


def loss(p: dict, h0: Vector, xs: Sequence[Vector], ys: Sequence[Vector]) -> float:
    h, total = list(h0), 0.0
    for x, y in zip(xs, ys):
        h = step(p, h, x)
        total += 0.5 * sum((o - t) ** 2 for o, t in zip(output(p, h), y))
    return total


def bptt(p: dict, h0: Vector, xs: Sequence[Vector], ys: Sequence[Vector]):
    """Return (grads, dh0, stored): the exact gradient of the loss, dL/dh_0,
    and the number of hidden state vectors kept for the backward sweep."""
    T = len(xs)
    hs = [list(h0)]
    os = [None]
    for t in range(1, T + 1):  # @line L1
        hs.append(step(p, hs[t - 1], xs[t - 1]))  # @line L2
        os.append(output(p, hs[t]))  # @line L2
    g = zeros_like(p)  # @line L3
    r = [0.0] * len(h0)  # @line L3
    for t in range(T, 0, -1):  # @line L4
        e = [o - y for o, y in zip(os[t], ys[t - 1])]  # @line L5
        add_outer(g["V"], e, hs[t])  # @line L5
        g["c"] = [s + d for s, d in zip(g["c"], e)]  # @line L5
        r = [s + d for s, d in zip(r, matTvec(p["V"], e))]  # @line L6
        delta = [s * (1.0 - h * h) for s, h in zip(r, hs[t])]  # @line L7
        add_outer(g["W"], delta, hs[t - 1])  # @line L8
        add_outer(g["U"], delta, xs[t - 1])  # @line L8
        g["b"] = [s + d for s, d in zip(g["b"], delta)]  # @line L8
        r = matTvec(p["W"], delta)  # @line L9
    return g, r, len(hs)  # @line L10


def truncated_bptt(p: dict, h0: Vector, xs: Sequence[Vector], ys: Sequence[Vector], k: int):
    """Truncated BPTT with window k: run bptt on each chunk of k steps,
    starting from the hidden state the previous chunk ended in, held constant.
    Return (grads, h_T, peak), where peak is the largest number of hidden
    vectors kept at one time (min(k, T) + 1)."""
    g = zeros_like(p)
    h, peak = list(h0), 0
    for s in range(0, len(xs), k):
        cx, cy = xs[s:s + k], ys[s:s + k]
        gc, _, stored = bptt(p, h, cx, cy)
        peak = max(peak, stored)
        for key, val in gc.items():
            if isinstance(val[0], list):
                for row, add in zip(g[key], val):
                    for j, a in enumerate(add):
                        row[j] += a
            else:
                g[key] = [u + a for u, a in zip(g[key], val)]
        for x in cx:
            h = step(p, h, x)
    return g, h, peak
