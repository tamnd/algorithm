# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiplicative-attention/. The authors are listed in prov/E826M9.jsonl.

"""Global and local attention of Luong, Pham and Manning (2015), for one decoder step.

The decoder state h_t of the current step is compared with the source states
hs_1 .. hs_S by one of three scores:

    dot      h_t . hs_s
    general  h_t^T W_a hs_s
    concat   v_a^T tanh(W_a [h_t; hs_s])

The weights are the softmax of the scores, the context is c = sum_s a_s hs_s,
and the attentional state is h~ = tanh(W_c [c; h_t]).

Local attention looks only at the source positions s with |s - p| <= D, where
the positions are numbered 1 .. S. local-m uses p = t. local-p uses
p = S * sigmoid(v_p^T tanh(W_p h_t)) and multiplies each weight by the
Gaussian exp(-(s - p)^2 / (2 sigma^2)) with sigma = D / 2. As in the paper,
the weights are not normalized again after this product.

The states and the weights are given (outputs and parameters of a network);
this module does not train them. Vectors are lists of floats and a matrix is
a list of rows.
"""

import math
from typing import List, Optional, Sequence, Tuple

from nlslog import softmax

Vector = List[float]
Matrix = Sequence[Sequence[float]]


def matvec(a: Matrix, x: Sequence[float]) -> Vector:
    """Return the product of the matrix a and the vector x."""
    return [math.fsum(r * y for r, y in zip(row, x)) for row in a]


def dot(x: Sequence[float], y: Sequence[float]) -> float:
    """Return the dot product of x and y."""
    return math.fsum(a * b for a, b in zip(x, y))


def score(kind: str, ht: Sequence[float], hs: Sequence[float], Wa: Optional[Matrix] = None,
          va: Optional[Sequence[float]] = None) -> float:
    """Return the score of the source state hs for the decoder state ht."""
    if kind == "dot":
        return dot(ht, hs)
    if kind == "general":
        return dot(ht, matvec(Wa, hs))
    if kind == "concat":
        return dot(va, [math.tanh(x) for x in matvec(Wa, list(ht) + list(hs))])
    raise ValueError("kind must be 'dot', 'general' or 'concat'")


def sigmoid(x: float) -> float:
    """Return 1 / (1 + exp(-x)) without overflow."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    z = math.exp(x)
    return z / (1.0 + z)


def aligned_position(ht: Sequence[float], S: int, Wp: Matrix, vp: Sequence[float]) -> float:
    """Return p = S * sigmoid(v_p^T tanh(W_p h_t)), a real number in [0, S]."""
    return S * sigmoid(dot(vp, [math.tanh(x) for x in matvec(Wp, ht)]))


def attention(ht: Sequence[float], Hs: Sequence[Sequence[float]], kind: str = "dot",
              Wa: Optional[Matrix] = None, va: Optional[Sequence[float]] = None,
              local: Optional[str] = None, t: Optional[int] = None, D: int = 10,
              Wp: Optional[Matrix] = None, vp: Optional[Sequence[float]] = None
              ) -> Tuple[Vector, Vector, Optional[float]]:
    """Return (context c, weights a over all S positions, aligned position p or None).

    local is None (global attention), "m" (local-m, needs t) or "p" (local-p,
    needs Wp and vp). Positions outside the window get the weight 0.
    """
    S = len(Hs)
    if S == 0:
        raise ValueError("attention needs at least one source state")
    p = None
    if local is None:  # @line L1
        window = list(range(1, S + 1))
    else:
        if local == "m":  # @line L2
            p = float(t)
        elif local == "p":
            p = aligned_position(ht, S, Wp, vp)
        else:
            raise ValueError("local must be None, 'm' or 'p'")
        window = [s for s in range(1, S + 1) if abs(s - p) <= D]
        if not window:
            raise ValueError("the window holds no source position")
    e = []
    for s in window:  # @line L3
        e.append(score(kind, ht, Hs[s - 1], Wa, va))  # @line L4
    w = softmax(e)  # @line L5
    if local == "p":  # @line L6
        sigma = D / 2
        w = [x * math.exp(-((s - p) ** 2) / (2 * sigma * sigma)) for x, s in zip(w, window)]
    a = [0.0] * S
    for x, s in zip(w, window):
        a[s - 1] = x
    c = [math.fsum(a[j] * Hs[j][i] for j in range(S)) for i in range(len(Hs[0]))]  # @line L7
    return c, a, p


def attentional_state(c: Sequence[float], ht: Sequence[float], Wc: Matrix) -> Vector:
    """Return h~ = tanh(W_c [c; h_t])."""
    return [math.tanh(x) for x in matvec(Wc, list(c) + list(ht))]  # @line L8


def step(ht, Hs, Wc, **kw) -> Tuple[Vector, Vector, Vector]:
    """Return (h~, c, a) for one decoder step."""
    c, a, _ = attention(ht, Hs, **kw)
    return attentional_state(c, ht, Wc), c, a  # @line L9


def backward_general(g: Sequence[float], ht: Sequence[float], Hs: Sequence[Sequence[float]],
                     Wa: Matrix, Wc: Matrix):
    """Return the gradients (d h_t, d Hs, d W_a, d W_c) of L = g . h~ for global general attention."""
    c, a, _ = attention(ht, Hs, "general", Wa)
    x = list(c) + list(ht)
    ht_tilde = attentional_state(c, ht, Wc)
    dz = [gi * (1 - y * y) for gi, y in zip(g, ht_tilde)]
    dWc = [[dzi * xj for xj in x] for dzi in dz]
    dx = [math.fsum(Wc[i][j] * dz[i] for i in range(len(dz))) for j in range(len(x))]
    dh = len(Hs[0])
    dc, dht = dx[:dh], dx[dh:]
    gamma = [dot(dc, hs) for hs in Hs]
    mean = math.fsum(ai * gi for ai, gi in zip(a, gamma))
    de = [ai * (gi - mean) for ai, gi in zip(a, gamma)]
    dHs = [[a[s] * v for v in dc] for s in range(len(Hs))]
    WtH = [matvec(Wa, hs) for hs in Hs]  # W_a hs_s
    WTh = [math.fsum(Wa[i][j] * ht[i] for i in range(len(ht))) for j in range(dh)]  # W_a^T h_t
    for s in range(len(Hs)):
        for i in range(len(ht)):
            dht[i] += de[s] * WtH[s][i]
        for j in range(dh):
            dHs[s][j] += de[s] * WTh[j]
    dWa = [[math.fsum(de[s] * ht[i] * Hs[s][j] for s in range(len(Hs))) for j in range(dh)]
           for i in range(len(ht))]
    return dht, dHs, dWa, dWc
