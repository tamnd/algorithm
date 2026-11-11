# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/context-tree-weighting/. The authors are listed in prov/4VCC2M.jsonl.

"""Binary context tree weighting of depth D (Willems, Shtarkov and Tjalkens).

A context is a tuple of past bits, most recent first: the context of depth d
of x_t is (x_{t-1}, ..., x_{t-d}). The children of a node s are s + (0,) and
s + (1,). Each node keeps the counts a (zeros) and b (ones), the KT estimate
P_e and the weighted probability P_w, both as base-2 logarithms:

    P_w(s) = P_e(s)                                 if s has depth D,
    P_w(s) = 1/2 P_e(s) + 1/2 P_w(s0) P_w(s1)       otherwise.

The bits before x_1 are taken to be zeros, and both sides know this.
The coder turns P_w(root) into conditional probabilities and drives a binary
arithmetic coder (the integer coder of Witten, Neal and Cleary, 32-bit
registers, probabilities quantized to 16 bits).

`block_probability` computes P_w(root) exactly with fractions from the final
counts, as a check of the sequential computation.
"""

import math
import random
from fractions import Fraction

CODE_BITS = 32
TOP = (1 << CODE_BITS) - 1
QTR = 1 << (CODE_BITS - 2)
HALF = 2 * QTR
PROB_BITS = 16
PROB_ONE = 1 << PROB_BITS


def _log2_add(a: float, b: float) -> float:
    """log2(2^a + 2^b)."""
    if a < b:
        a, b = b, a
    return a + math.log2(1.0 + 2.0 ** (b - a))


class CTW:
    """The context tree of depth D with log-domain P_e and P_w at each node."""

    def __init__(self, depth: int) -> None:
        if depth < 0:
            raise ValueError("depth must be at least 0")
        self.depth = depth
        # node -> [a, b, log2 P_e, log2 P_w]; a missing node has [0, 0, 0, 0].
        self.nodes: dict[tuple, list] = {}  # @line L1
        self.past = [0] * depth  # most recent last

    def _path(self) -> list[tuple]:
        ctx = tuple(reversed(self.past[len(self.past) - self.depth:])) if self.depth else ()
        return [ctx[:d] for d in range(self.depth + 1)]

    def _walk(self, x: int, write: bool) -> float:
        """Run the update for bit x from the leaf to the root; return log2 P_w(root)."""
        path = self._path()
        child_pw = 0.0
        for d in range(self.depth, -1, -1):  # @line L6
            s = path[d]
            a, b, pe, pw = self.nodes.get(s, (0, 0, 0.0, 0.0))
            pe += math.log2(((b if x else a) + 0.5) / (a + b + 1))  # @line L7
            if x:
                b += 1
            else:
                a += 1  # @line L8
            if d == self.depth:
                pw = pe  # @line L9
            else:
                other = s + (1 - path[d + 1][d],)
                other_pw = self.nodes[other][3] if other in self.nodes else 0.0
                pw = -1.0 + _log2_add(pe, child_pw + other_pw)  # @line L10
            if write:
                self.nodes[s] = [a, b, pe, pw]
            child_pw = pw
        return child_pw

    def log_pw(self) -> float:
        """log2 P_w of the root for the bits seen so far."""
        return self.nodes[()][3] if () in self.nodes else 0.0

    def prob_one(self) -> float:
        """Pr[next bit = 1] = P_w(root with a 1 added) / P_w(root now)."""
        q0 = self._walk(0, False)  # @line L3
        q1 = self._walk(1, False)
        return 1.0 / (1.0 + 2.0 ** (q0 - q1))  # @line L4

    def update(self, x: int) -> None:
        self._walk(x, True)
        if self.depth:
            self.past = self.past[1:] + [x]


def _quantize(p1: float) -> int:
    """The 16-bit count of a 1 out of PROB_ONE, kept in [1, PROB_ONE - 1]."""
    return min(max(int(p1 * PROB_ONE + 0.5), 1), PROB_ONE - 1)


class _Encoder:
    def __init__(self) -> None:
        self.low, self.high, self.pending = 0, TOP, 0
        self.bits: list[int] = []

    def _emit(self, b: int) -> None:
        self.bits.append(b)
        self.bits.extend([1 - b] * self.pending)
        self.pending = 0

    def encode(self, lo: int, hi: int) -> None:
        r = self.high - self.low + 1
        self.high = self.low + ((r * hi) >> PROB_BITS) - 1
        self.low = self.low + ((r * lo) >> PROB_BITS)
        while True:
            if self.high < HALF:
                self._emit(0)
            elif self.low >= HALF:
                self._emit(1)
                self.low -= HALF
                self.high -= HALF
            elif self.low >= QTR and self.high < HALF + QTR:
                self.pending += 1
                self.low -= QTR
                self.high -= QTR
            else:
                break
            self.low = 2 * self.low
            self.high = 2 * self.high + 1

    def finish(self) -> bytes:
        self.pending += 1
        self._emit(0 if self.low < QTR else 1)
        bits = self.bits + [0] * (-len(self.bits) % 8)
        return bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))


class _Decoder:
    def __init__(self, data: bytes) -> None:
        self.data, self.pos = data, 0
        self.low, self.high, self.value = 0, TOP, 0
        for _ in range(CODE_BITS):
            self.value = 2 * self.value + self._bit()

    def _bit(self) -> int:
        i = self.pos
        self.pos += 1
        return (self.data[i >> 3] >> (7 - (i & 7))) & 1 if i < 8 * len(self.data) else 0

    def decode(self, c1: int) -> int:
        r = self.high - self.low + 1
        split = (r * (PROB_ONE - c1)) >> PROB_BITS
        if self.value - self.low < split:
            x, lo, hi = 0, 0, PROB_ONE - c1
        else:
            x, lo, hi = 1, PROB_ONE - c1, PROB_ONE
        self.high = self.low + ((r * hi) >> PROB_BITS) - 1
        self.low = self.low + ((r * lo) >> PROB_BITS)
        while True:
            if self.high < HALF:
                pass
            elif self.low >= HALF:
                self.low -= HALF
                self.high -= HALF
                self.value -= HALF
            elif self.low >= QTR and self.high < HALF + QTR:
                self.low -= QTR
                self.high -= QTR
                self.value -= QTR
            else:
                break
            self.low = 2 * self.low
            self.high = 2 * self.high + 1
            self.value = 2 * self.value + self._bit()
        return x


def encode(bits: list[int], depth: int) -> bytes:
    model = CTW(depth)
    enc = _Encoder()
    for x in bits:  # @line L2
        if x not in (0, 1):
            raise ValueError("CTW here codes bits")
        c1 = _quantize(model.prob_one())
        if x:
            enc.encode(PROB_ONE - c1, PROB_ONE)  # @line L5
        else:
            enc.encode(0, PROB_ONE - c1)
        model.update(x)
    return enc.finish()  # @line L11


def decode(code: bytes, n: int, depth: int) -> list[int]:
    model = CTW(depth)
    dec = _Decoder(code)
    out: list[int] = []
    for _ in range(n):  # @line L12
        c1 = _quantize(model.prob_one())  # @line L13
        x = dec.decode(c1)  # @line L14
        out.append(x)
        model.update(x)  # @line L15
    return out


def ideal_length(bits: list[int], depth: int) -> float:
    """-log2 P_w(root) after all bits: the code length that CTW aims at."""
    model = CTW(depth)
    for x in bits:
        model.update(x)
    return -model.log_pw()


def _counts(bits: list[int], depth: int) -> dict[tuple, list[int]]:
    padded = [0] * depth + list(bits)
    counts: dict[tuple, list[int]] = {}
    for t in range(depth, len(padded)):
        ctx = tuple(reversed(padded[t - depth:t]))
        for d in range(depth + 1):
            counts.setdefault(ctx[:d], [0, 0])[padded[t]] += 1
    return counts


def kt_exact(a: int, b: int) -> Fraction:
    """The KT block probability of a zeros and b ones."""
    p = Fraction(1)
    for i in range(a):
        p *= Fraction(2 * i + 1, 2)
    for j in range(b):
        p *= Fraction(2 * j + 1, 2)
    for k in range(a + b):
        p /= k + 1
    return p


def kt_log2(a: int, b: int) -> float:
    """log2 of the KT block probability, through the gamma function."""
    half = math.lgamma(0.5)
    return (math.lgamma(a + 0.5) + math.lgamma(b + 0.5) - 2 * half - math.lgamma(a + b + 1)) / math.log(2)


def block_probability(bits: list[int], depth: int) -> Fraction:
    """P_w(root) computed exactly from the final counts by the recursion."""
    counts = _counts(bits, depth)

    def pw(s: tuple) -> Fraction:
        if s not in counts:
            return Fraction(1)
        pe = kt_exact(*counts[s])
        if len(s) == depth:
            return pe
        return (pe + pw(s + (0,)) * pw(s + (1,))) / 2

    return pw(())


def best_tree_cost(bits: list[int], depth: int) -> float:
    """min over pruned trees S of (description bits of S + sum over leaves of -log2 P_e).

    A node of depth below D costs 1 bit, as a leaf or as an inner node; a node of
    depth D costs nothing. Nodes that no context reached have P_w = 1 and cost 0.
    CTW satisfies -log2 P_w(root) <= this value.
    """
    counts = _counts(bits, depth)

    def cost(s: tuple) -> float:
        if s not in counts:
            return 0.0
        leaf = -kt_log2(*counts[s])
        if len(s) == depth:
            return leaf
        return 1.0 + min(leaf, cost(s + (0,)) + cost(s + (1,)))

    return cost(())


def tree_source_sample(leaves: dict[tuple, float], n: int, seed: int) -> list[int]:
    """n bits from a tree source: leaves maps a context (most recent first) to Pr[1]."""
    rng = random.Random(seed)
    depth = max(len(s) for s in leaves)
    past = [0] * depth
    out = []
    for _ in range(n):
        ctx = tuple(reversed(past[len(past) - depth:]))
        theta = next(p for s, p in leaves.items() if ctx[:len(s)] == s)
        x = 1 if rng.random() < theta else 0
        out.append(x)
        past = past[1:] + [x]
    return out


def source_length(bits: list[int], leaves: dict[tuple, float], ml: bool = False) -> float:
    """-log2 of the probability of bits under the tree source, with the given or the ML parameters."""
    depth = max(len(s) for s in leaves)
    padded = [0] * depth + list(bits)
    cnt = {s: [0, 0] for s in leaves}
    for t in range(depth, len(padded)):
        ctx = tuple(reversed(padded[t - depth:t]))
        s = next(s for s in leaves if ctx[:len(s)] == s)
        cnt[s][padded[t]] += 1
    total = 0.0
    for s, (a, b) in cnt.items():
        theta = b / (a + b) if ml and a + b else leaves[s]
        if a:
            total -= a * math.log2(1 - theta)
        if b:
            total -= b * math.log2(theta)
    return total


def gamma(z: float) -> float:
    """The parameter cost of a leaf with z symbols in the bound of WST: z if z < 1, else 1/2 lg z + 1."""
    return z if z < 1 else 0.5 * math.log2(z) + 1


def redundancy_bound(leaves: dict[tuple, float], depth: int, n: int) -> float:
    """Gamma_D(S) + |S| gamma(n / |S|), the bound on -log2 P_w - (-log2 P_a) of WST."""
    size = len(leaves)
    model_cost = 2 * size - 1 - sum(1 for s in leaves if len(s) == depth)
    return model_cost + size * gamma(n / size)
