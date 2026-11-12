# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/photon-map/. The authors are listed in prov/JNG669.jsonl.

"""Jensen's photon map: a left-balanced kd-tree of photons stored in a flat array.

The node at array index i (1-based) has its children at 2i and 2i + 1, so the tree needs no
pointers. Each node stores one photon and the axis of its splitting plane.
"""

import heapq
import math
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Photon:
    position: tuple[float, float, float]
    power: float
    direction: tuple[float, float, float] = (0.0, 0.0, -1.0)  # the direction the photon travelled


def left_size(n: int) -> int:
    """Number of nodes in the left subtree of a left-balanced (complete) tree with n nodes."""
    if n <= 1:
        return 0
    h = n.bit_length() - 1  # 2^h <= n < 2^(h+1)
    last = n - ((1 << h) - 1)  # nodes on the last, partly filled level
    half = 1 << (h - 1)
    return (half - 1) + min(last, half)


def _select(a: list[Photon], lo: int, hi: int, k: int, axis: int) -> None:
    """Rearrange a[lo:hi] so that a[k] has rank k - lo by coordinate axis, with smaller or equal
    values before it and larger or equal values after it (quickselect, Hoare partition)."""
    while hi - lo > 1:
        pivot = a[(lo + hi - 1) // 2].position[axis]
        i, j = lo, hi - 1
        while i <= j:
            while a[i].position[axis] < pivot:
                i += 1
            while a[j].position[axis] > pivot:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        if k <= j:
            hi = j + 1
        elif k >= i:
            lo = i
        else:
            return


class PhotonMap:
    def __init__(self, photons: Sequence[Photon]) -> None:
        a = list(photons)
        n = len(a)
        self.n = n
        self.heap: list[Photon | None] = [None] * (n + 1)
        self.axis = [0] * (n + 1)
        stack = [(1, 0, n)]  # @line L1
        while stack:  # @line L2
            node, lo, hi = stack.pop()
            if hi <= lo:
                continue
            lows = [min(p.position[d] for p in a[lo:hi]) for d in range(3)]  # @line L3
            highs = [max(p.position[d] for p in a[lo:hi]) for d in range(3)]
            axis = max(range(3), key=lambda d: highs[d] - lows[d])
            mid = lo + left_size(hi - lo)  # @line L4
            _select(a, lo, hi, mid, axis)  # @line L5
            self.heap[node] = a[mid]  # @line L6
            self.axis[node] = axis
            stack.append((2 * node, lo, mid))  # @line L7
            stack.append((2 * node + 1, mid + 1, hi))

    def k_nearest(self, x: Sequence[float], k: int, max_radius: float = math.inf) -> list[tuple[float, Photon]]:
        """The k photons nearest to x within max_radius, as (squared distance, photon), nearest first."""
        found: list[tuple[float, int]] = []  # max-heap by squared distance: entries (-d2, node)
        d2max = max_radius * max_radius  # @line L8
        stack = [(1, 0.0)]  # (node, a lower bound on the squared distance from x to its region)
        while stack:  # @line L9
            node, bound = stack.pop()
            if node > self.n or bound >= d2max:  # @line L10
                continue
            p = self.heap[node]
            assert p is not None
            axis = self.axis[node]
            delta = x[axis] - p.position[axis]  # @line L11
            near, far = (2 * node, 2 * node + 1) if delta < 0 else (2 * node + 1, 2 * node)
            stack.append((far, max(bound, delta * delta)))  # @line L12
            stack.append((near, bound))
            d2 = sum((x[d] - p.position[d]) ** 2 for d in range(3))  # @line L13
            if d2 < d2max:
                if len(found) < k:
                    heapq.heappush(found, (-d2, node))
                    if len(found) == k:
                        d2max = -found[0][0]  # @line L14
                else:
                    heapq.heapreplace(found, (-d2, node))
                    d2max = -found[0][0]
        out = sorted((-nd2, node) for nd2, node in found)
        return [(d2, self.heap[node]) for d2, node in out]  # type: ignore[misc]

    def in_radius(self, x: Sequence[float], radius: float) -> list[Photon]:
        """All photons with distance to x less than radius."""
        r2 = radius * radius
        out = []
        stack = [(1, 0.0)]
        while stack:
            node, bound = stack.pop()
            if node > self.n or bound >= r2:
                continue
            p = self.heap[node]
            assert p is not None
            axis = self.axis[node]
            delta = x[axis] - p.position[axis]
            near, far = (2 * node, 2 * node + 1) if delta < 0 else (2 * node + 1, 2 * node)
            stack.append((far, max(bound, delta * delta)))
            stack.append((near, bound))
            if sum((x[d] - p.position[d]) ** 2 for d in range(3)) < r2:
                out.append(p)
        return out

    def density_estimate(self, x: Sequence[float], k: int, max_radius: float = math.inf) -> tuple[float, float, int]:
        """Jensen's estimate of the power per unit area at x from the k nearest photons.

        Return (sum of power / (pi r^2), r, the number of photons used), where r is the distance
        to the farthest photon used (or 0 if there are none).
        """
        near = self.k_nearest(x, k, max_radius)
        if not near:
            return 0.0, 0.0, 0
        r2 = near[-1][0]
        if r2 == 0.0:
            return math.inf, 0.0, len(near)
        return sum(p.power for _, p in near) / (math.pi * r2), math.sqrt(r2), len(near)
