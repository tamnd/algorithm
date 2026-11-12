# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/psipred/. The authors are listed in prov/RQVJG1.jsonl.

"""The forward pass of a PSIPRED-style two-stage window network.

Stage 1 reads a window of w profile rows centred on each residue. Each row
gives 20 inputs, the logistic of the raw PSSM values, and one extra input
that is 1 when the window position falls off the chain end (then the 20
inputs are 0). Stage 2 reads a window of w stage-1 outputs (3 values) with
the same extra input. Both stages have one hidden layer. All units are
logistic. PSIPRED uses w = 15, 75 hidden units in stage 1 and 60 in stage 2.

The weights here are not PSIPRED's weights. They are any numbers the caller
gives, for example random numbers from a seeded generator. Training is not
part of this module.
"""

from math import exp
import random

STATES = "HEC"


def logistic(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + exp(-x))
    z = exp(x)
    return z / (1.0 + z)


class Layer:
    """A dense layer: out = logistic(W in + b), with W given as rows."""

    def __init__(self, W: list, b: list):
        self.W, self.b = W, b

    def forward(self, x: list) -> list:
        return [logistic(sum(w * v for w, v in zip(row, x)) + bias) for row, bias in zip(self.W, self.b)]


class WindowNet:
    """Window w, f features per position (plus the end flag), hidden size h, 3 outputs."""

    def __init__(self, w: int, f: int, hidden: Layer, out: Layer):
        assert w % 2 == 1
        self.w, self.f, self.hidden, self.out = w, f, hidden, out

    def forward(self, rows: list) -> list:
        """Return the 3 outputs at each position.

        The hidden pre-activation at centre j is the bias plus, for each window
        offset o, block o of the weights times the features of row j + o - w // 2.
        For a window position off the chain, the block adds only the weight
        of the end flag, because the other inputs are 0. The input vector of
        length w (f + 1) is never built.
        """
        n, w, f, half = len(rows), self.w, self.f, self.w // 2
        H = len(self.hidden.b)
        W = self.hidden.W
        outs = []
        for j in range(n):  # @line L1
            pre = list(self.hidden.b)  # @line L2
            for o in range(w):  # @line L3
                p = j + o - half  # @line L4
                base = o * (f + 1)
                if 0 <= p < n:  # @line L5
                    r = rows[p]
                    for u in range(H):
                        Wu = W[u]
                        pre[u] += sum(Wu[base + c] * r[c] for c in range(f))
                else:  # @line L6
                    for u in range(H):
                        pre[u] += W[u][base + f]
            hid = [logistic(v) for v in pre]  # @line L7
            outs.append(self.out.forward(hid))  # @line L8
        return outs  # @line L9


def window_input(rows: list, j: int, w: int, f: int) -> list:
    """The full input vector of length w (f + 1) for centre j."""
    half, x = w // 2, []
    for o in range(w):
        p = j + o - half
        if 0 <= p < len(rows):
            x.extend(rows[p])
            x.append(0.0)
        else:
            x.extend([0.0] * f)
            x.append(1.0)
    return x


def random_net(w: int, f: int, h: int, rng: random.Random, scale: float = 0.3) -> WindowNet:
    """A window network with weights drawn uniformly from [-scale, scale]."""
    n_in = w * (f + 1)
    hid = Layer([[rng.uniform(-scale, scale) for _ in range(n_in)] for _ in range(h)],
                [rng.uniform(-scale, scale) for _ in range(h)])
    out = Layer([[rng.uniform(-scale, scale) for _ in range(h)] for _ in range(3)],
                [rng.uniform(-scale, scale) for _ in range(3)])
    return WindowNet(w, f, hid, out)


def psipred_forward(pssm: list, net1: WindowNet, net2: WindowNet) -> tuple:
    """Run both stages on a PSSM (n rows of 20 raw scores).

    Returns (stage-1 outputs, stage-2 outputs, predicted states).
    """
    rows = [[logistic(v) for v in r] for r in pssm]  # @line L10
    s1 = net1.forward(rows)  # @line L11
    s2 = net2.forward(s1)  # @line L12
    pred = "".join(STATES[max(range(3), key=lambda k: (o[k], -k))] for o in s2)  # @line L13
    return s1, s2, pred  # @line L14
