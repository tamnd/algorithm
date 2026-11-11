# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/context-mixing/. The authors are listed in prov/S2R9ZZ.jsonl.

"""Logistic context mixing of bit predictions, in the style of PAQ.

Each model predicts the next bit from its own context. The mixer works in the
logistic domain: it stretches each probability, st(p) = ln(p / (1 - p)), takes
a weighted sum, and squashes the result back, p = 1 / (1 + e^-x). After the
bit y is known, each weight moves by lr * (y - p) * st(p_i), a step of online
gradient descent on the coding cost -ln P(y).

The coder is left out: the functions return the ideal code length, the sum of
-lg P(bit), which a binary arithmetic coder meets to within a few bytes.
"""

import math
import random

P_MIN = 1 / 4096


def stretch(p: float) -> float:
    p = min(max(p, P_MIN), 1 - P_MIN)
    return math.log(p / (1 - p))


def squash(x: float) -> float:
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    e = math.exp(x)
    return e / (1 + e)


class LagModel:
    """Predicts a bit from the bits at the given lags (lags 1..k is an order-k model),
    with an adaptive probability per context. The rate starts at 1/1.5 and falls to
    1/(limit + 0.5), so a new context learns fast and an old one still tracks changes."""

    def __init__(self, lags: tuple[int, ...], limit: int = 30) -> None:
        self.lags = lags
        self.limit = limit
        self.table: dict[tuple[int, ...], list[float]] = {}
        self.history: list[int] = []

    def _ctx(self) -> tuple[int, ...]:
        h = self.history
        return tuple(h[-lag] if lag <= len(h) else 0 for lag in self.lags)

    def predict(self) -> float:
        return self.table.setdefault(self._ctx(), [0.5, 0])[0]

    def update(self, y: int) -> None:
        e = self.table.setdefault(self._ctx(), [0.5, 0])
        e[1] = min(e[1] + 1, self.limit)
        e[0] += (y - e[0]) / (e[1] + 0.5)
        self.history.append(y)


class Mixer:
    def __init__(self, n_inputs: int, lr: float = 0.005, w0: float = 0.3) -> None:
        self.w = [w0] * n_inputs  # @line L1
        self.lr = lr
        self.s: list[float] = []
        self.p = 0.5

    def mix(self, probs: list[float]) -> float:
        self.s = [stretch(p) for p in probs]  # @line L4
        self.p = squash(sum(w * s for w, s in zip(self.w, self.s)))  # @line L5
        self.p = min(max(self.p, P_MIN), 1 - P_MIN)  # @line L6
        return self.p

    def update(self, y: int) -> None:
        err = y - self.p  # @line L8
        self.w = [w + self.lr * err * s for w, s in zip(self.w, self.s)]  # @line L9


def mixed_length(bits: list[int], contexts: list[tuple[int, ...]], lr: float = 0.005) -> float:
    """The ideal code length in bits of the logistic mixture of the lag models."""
    models = [LagModel(c) for c in contexts]
    mixer = Mixer(len(models), lr)
    total = 0.0
    for y in bits:  # @line L2
        p = mixer.mix([m.predict() for m in models])  # @line L3
        total -= math.log2(p if y else 1 - p)  # @line L7
        mixer.update(y)
        for m in models:  # @line L10
            m.update(y)
    return total


def single_length(bits: list[int], lags: tuple[int, ...]) -> float:
    m = LagModel(lags)
    total = 0.0
    for y in bits:
        p = min(max(m.predict(), P_MIN), 1 - P_MIN)
        total -= math.log2(p if y else 1 - p)
        m.update(y)
    return total


def segmented_source(seed: int, seg: int = 3000, rounds: int = 2) -> list[int]:
    """Segments in which different models are best: a copy of the bit 8 places back
    with 5 percent noise, an order-1 chain that mostly alternates, and a biased coin."""
    rng = random.Random(seed)
    bits = [rng.randint(0, 1) for _ in range(8)]
    for _ in range(rounds):
        for _ in range(seg):
            bits.append(bits[-8] ^ int(rng.random() < 0.05))
        for _ in range(seg):
            bits.append(int(rng.random() < (0.07 if bits[-1] else 0.93)))
        for _ in range(seg):
            bits.append(int(rng.random() < 0.04))
    return bits[8:]
