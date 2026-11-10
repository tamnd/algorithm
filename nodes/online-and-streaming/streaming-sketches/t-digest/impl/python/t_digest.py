# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-digest/. The authors are listed in prov/ND6BPW.jsonl.
"""The merging t-digest of Dunning and Ertl (2019).

The digest is a list of centroids (mean, weight), sorted by mean. New values go
to a buffer. When the buffer is full, the buffer and the centroids are sorted
together and merged left to right: a run of neighbors becomes one centroid as
long as its quantile interval [q0, q] has k(q) - k(q0) <= 1, where k is the
scale function. Queries interpolate linearly between the centroids.

The values may be floats or fractions.Fraction. With Fraction and the scale
function k0 all arithmetic is exact, which the tests use for the attack.
"""

from __future__ import annotations

import math
from fractions import Fraction


class Scale:
    """A scale function k(q) for compression delta, with its inverse."""

    def __init__(self, name: str, delta: float) -> None:
        self.name = name
        self.delta = delta

    def k(self, q):
        if self.name == "k0":
            return Fraction(self.delta) * q / 2 if isinstance(q, Fraction) else self.delta * q / 2
        q = min(max(float(q), 0.0), 1.0)
        return self.delta / (2 * math.pi) * math.asin(2 * q - 1)

    def k_inv(self, k):
        if self.name == "k0":
            return 2 * k / Fraction(self.delta) if isinstance(k, Fraction) else 2 * k / self.delta
        k = min(max(k, -self.delta / 4), self.delta / 4)
        return (math.sin(2 * math.pi * k / self.delta) + 1) / 2


class TDigest:
    """A merging t-digest. Weights are integers; means are weighted averages."""

    def __init__(self, delta: float, scale: str = "k1", buffer_size: int | None = None) -> None:
        self.delta = delta
        self.scale = Scale(scale, delta)
        self.buffer_size = buffer_size or max(1, 5 * math.ceil(delta))
        self.means: list = []
        self.weights: list[int] = []
        self.buffer: list = []
        self.n = 0
        self.xmin = None
        self.xmax = None

    def insert(self, x, w: int = 1) -> None:
        """Add the value x with weight w."""
        self.buffer.append((x, w))  # @line L1
        self.n += w
        self.xmin = x if self.xmin is None or x < self.xmin else self.xmin
        self.xmax = x if self.xmax is None or x > self.xmax else self.xmax
        if len(self.buffer) >= self.buffer_size:  # @line L2
            self.compress()

    def compress(self) -> None:
        """Algorithm 1 of Dunning and Ertl: one left-to-right merging pass."""
        items = sorted(list(zip(self.means, self.weights)) + self.buffer, key=lambda t: t[0])  # @line L3
        self.buffer = []
        if not items:
            return
        total = sum(w for _, w in items)
        exact = isinstance(items[0][0], Fraction)
        q0 = Fraction(0) if exact else 0.0
        q_limit = self.scale.k_inv(self.scale.k(q0) + 1)  # @line L4
        means, weights = [], []
        m, w = items[0]
        for x, v in items[1:]:
            q = q0 + (Fraction(w + v, total) if exact else (w + v) / total)  # @line L5
            if q <= q_limit:  # @line L6
                m = m + (x - m) * (Fraction(v, w + v) if exact else v / (w + v))
                w += v
            else:  # @line L7
                means.append(m)
                weights.append(w)
                q0 = q0 + (Fraction(w, total) if exact else w / total)
                q_limit = self.scale.k_inv(self.scale.k(q0) + 1)
                m, w = x, v
        means.append(m)  # @line L8
        weights.append(w)
        self.means, self.weights = means, weights

    def merge(self, other: "TDigest") -> None:
        """Add all centroids and buffered values of another digest, then compress."""
        other.compress()
        for m, w in zip(other.means, other.weights):
            self.buffer.append((m, w))
            self.n += w
        for x in (other.xmin, other.xmax):
            if x is not None:
                self.xmin = x if self.xmin is None or x < self.xmin else self.xmin
                self.xmax = x if self.xmax is None or x > self.xmax else self.xmax
        self.compress()

    def _points(self) -> list:
        """The knots of the interpolated CDF: (xmin, 0), (c_i, W_<i + w_i/2), (xmax, n)."""
        self.compress()
        pts = [(self.xmin, 0)]
        before = 0
        for m, w in zip(self.means, self.weights):
            pts.append((m, before + Fraction(w, 2)))  # @line L9
            before += w
        pts.append((self.xmax, self.n))
        return pts

    def rank(self, x):
        """Estimate of the number of values <= x, by linear interpolation."""
        if self.n == 0 or x < self.xmin:
            return 0
        if x >= self.xmax:
            return self.n
        pts = self._points()
        for (a, ra), (b, rb) in zip(pts, pts[1:]):
            if a <= x < b:
                return ra + (rb - ra) * (x - a) / (b - a)
        return self.n

    def query(self, phi: float):
        """Estimate of the phi-quantile, the inverse of the interpolated CDF."""
        if self.n == 0:
            raise ValueError("empty digest")
        target = phi * self.n
        pts = self._points()
        for (a, ra), (b, rb) in zip(pts, pts[1:]):
            if ra <= target <= rb:  # @line L10
                if rb == ra:
                    return a
                return a + (b - a) * (target - ra) / (rb - ra)
        return self.xmax

    def k_sizes(self) -> list:
        """k(q_right) - k(q_left) for each centroid of the compressed digest."""
        self.compress()
        out, before = [], 0
        for w in self.weights:
            out.append(self.scale.k((before + w) / self.n) - self.scale.k(before / self.n))
            before += w
        return out

    def check_invariant(self) -> None:
        """Weights add up to n, means are sorted, and at most ceil(delta) centroids remain."""
        self.compress()
        assert sum(self.weights) == self.n
        assert all(a <= b for a, b in zip(self.means, self.means[1:]))
        assert len(self.means) <= math.ceil(self.delta)
        if self.means:
            assert self.xmin <= self.means[0] and self.means[-1] <= self.xmax


def lopsided_attack(delta: int, rounds: int) -> tuple[TDigest, list]:
    """Nested lopsided insertions in the style of Cormode, Mishra, Ross and Vesely (2021).

    Returns the digest (scale k0, exact Fractions) and the stream fed to it.
    Start with 20 delta integers around 0 and attack the centroid with mean c
    just below 0. Each round looks at the gap between c and the next stream
    value above c, and inserts one batch into it: v values just above c, which
    fill the attacked centroid, then one value at a quarter of the gap, then
    w2 - 1 equal values at three quarters of the gap. The last two parts form
    a new full centroid whose mean lies below almost all of its items. The new
    centroid is attacked in the next round.
    """
    t = TDigest(delta, scale="k0", buffer_size=10**9)
    stream: list = []
    n0 = 20 * delta
    for i in range(-n0 // 2, n0 - n0 // 2):
        t.insert(Fraction(i))
        stream.append(Fraction(i))
    t.compress()
    idx = max(i for i, m in enumerate(t.means) if m < 0)
    c = t.means[idx]
    for _ in range(rounds):
        w, total = t.weights[idx], t.n
        batch = (4 * total - w * delta) // (delta - 4)  # makes v + w2 two caps minus w
        cap = 2 * (total + batch) // delta
        v = max(cap - w, 0)
        w2 = batch - v
        nxt = min(x for x in stream if x > c)
        gap = nxt - c
        values = [c + gap / 1000] * v + [c + gap / 4] + [c + gap * 3 / 4] * (w2 - 1)
        for x in values:
            t.insert(x)
            stream.append(x)
        t.compress()
        inside = [i for i, m in enumerate(t.means) if c < m < nxt]
        if not inside:
            break
        idx = inside[-1]
        c = t.means[idx]
    return t, stream


def max_rank_error(t: TDigest, stream: list) -> float:
    """The largest |estimated rank - true rank| / n over the means and the midpoints after them."""
    import bisect

    data = sorted(stream)
    worst = 0
    for m in t.means:
        j = bisect.bisect_right(data, m)
        probes = [m] + ([(m + data[j]) / 2] if j < len(data) else [])
        for x in probes:
            worst = max(worst, abs(t.rank(x) - bisect.bisect_right(data, x)))
    return float(worst) / len(data)
