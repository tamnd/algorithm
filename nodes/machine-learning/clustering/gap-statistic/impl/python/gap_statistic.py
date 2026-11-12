# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gap-statistic/. The authors are listed in prov/BXW1TS.jsonl.
"""The gap statistic of Tibshirani, Walther and Hastie (2001) with k-means as the clusterer.

Gap(k) = mean over b of log W*_kb  -  log W_k, where W*_kb is the dispersion of the b-th
reference data set drawn uniformly over the bounding box of the data ("box") or over the
box aligned with the principal components ("pc").
s_k = sd_k * sqrt(1 + 1/B). Choose the smallest k with Gap(k) >= Gap(k + 1) - s_(k+1).
"""

import random
from math import log, sqrt
from typing import Sequence

Point = list


def sqdist(u: Sequence[float], v: Sequence[float]) -> float:
    return sum((a - b) ** 2 for a, b in zip(u, v))


def pooled_dispersion(points: Sequence[Point], labels: Sequence[int]) -> float:
    """W_k = sum_r D_r / (2 n_r), D_r the sum of squared distances over ordered pairs in cluster r."""
    groups: dict = {}
    for x, c in zip(points, labels):
        groups.setdefault(c, []).append(x)
    total = 0.0
    for g in groups.values():
        dr = sum(sqdist(x, y) for x in g for y in g)
        total += dr / (2 * len(g))
    return total


def kmeans(points: Sequence[Point], k: int, rng: random.Random, restarts: int = 3, iters: int = 100):
    """Lloyd's algorithm from k-means++ seeds; keep the best of a few restarts. Returns labels."""
    n = len(points)
    best, best_cost = None, None
    for _ in range(restarts):
        centers = [list(points[rng.randrange(n)])]
        while len(centers) < k:
            dd = [min(sqdist(x, c) for c in centers) for x in points]
            tot = sum(dd)
            if tot == 0:
                centers.append(list(points[rng.randrange(n)]))
                continue
            r = rng.random() * tot
            acc = 0.0
            for x, w in zip(points, dd):
                acc += w
                if acc >= r:
                    centers.append(list(x))
                    break
            else:
                centers.append(list(points[-1]))
        labels = [-1] * n
        for _ in range(iters):
            new = [min(range(k), key=lambda j: sqdist(x, centers[j])) for x in points]
            if new == labels:
                break
            labels = new
            for j in range(k):
                members = [x for x, c in zip(points, labels) if c == j]
                if members:
                    centers[j] = [sum(col) / len(members) for col in zip(*members)]
        cost = sum(sqdist(x, centers[c]) for x, c in zip(points, labels))
        if best_cost is None or cost < best_cost:
            best, best_cost = labels, cost
    return best


def _jacobi_eigenvectors(a: list, sweeps: int = 50) -> list:
    """Columns of the returned matrix are eigenvectors of the symmetric matrix a (cyclic Jacobi)."""
    d = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(d) for j in range(d) if i != j)
        if off < 1e-24:
            break
        for p in range(d):
            for q in range(p + 1, d):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + sqrt(theta * theta + 1))
                c = 1 / sqrt(t * t + 1)
                s = t * c
                for r in range(d):
                    arp, arq = a[r][p], a[r][q]
                    a[r][p], a[r][q] = c * arp - s * arq, s * arp + c * arq
                for r in range(d):
                    apr, aqr = a[p][r], a[q][r]
                    a[p][r], a[q][r] = c * apr - s * aqr, s * apr + c * aqr
                for r in range(d):
                    vrp, vrq = v[r][p], v[r][q]
                    v[r][p], v[r][q] = c * vrp - s * vrq, s * vrp + c * vrq
    return v


def reference_sampler(points: Sequence[Point], reference: str = "box"):
    """Return a function rng -> one reference data set of the same size as points."""
    n, d = len(points), len(points[0])
    if reference == "box":
        lo = [min(x[t] for x in points) for t in range(d)]
        hi = [max(x[t] for x in points) for t in range(d)]
        return lambda rng: [[rng.uniform(lo[t], hi[t]) for t in range(d)] for _ in range(n)]
    if reference != "pc":
        raise ValueError("reference must be box or pc")
    mean = [sum(x[t] for x in points) / n for t in range(d)]
    xc = [[x[t] - mean[t] for t in range(d)] for x in points]
    cov = [[sum(r[s] * r[t] for r in xc) for t in range(d)] for s in range(d)]
    v = _jacobi_eigenvectors(cov)
    rot = [[sum(r[s] * v[s][t] for s in range(d)) for t in range(d)] for r in xc]
    lo = [min(r[t] for r in rot) for t in range(d)]
    hi = [max(r[t] for r in rot) for t in range(d)]

    def draw(rng: random.Random):
        out = []
        for _ in range(n):
            z = [rng.uniform(lo[t], hi[t]) for t in range(d)]
            out.append([sum(z[t] * v[s][t] for t in range(d)) + mean[s] for s in range(d)])
        return out

    return draw


def gap_statistic(points: Sequence[Point], kmax: int, b: int, rng: random.Random,
                  reference: str = "box", restarts: int = 3):
    """Return (gap, s, k_hat); gap[k - 1] and s[k - 1] belong to k = 1..kmax.

    Cost: (B + 1) * kmax runs of k-means, plus O(n^2 d) per dispersion.
    k_hat is kmax when no k < kmax meets the rule.
    """
    draw = reference_sampler(points, reference)
    refs = [draw(rng) for _ in range(b)]
    gap, sk = [], []
    for k in range(1, kmax + 1):
        logw = log(pooled_dispersion(points, kmeans(points, k, rng, restarts)))
        logs = [log(pooled_dispersion(z, kmeans(z, k, rng, restarts))) for z in refs]
        mean = sum(logs) / b
        sd = sqrt(sum((x - mean) ** 2 for x in logs) / b)
        gap.append(mean - logw)
        sk.append(sd * sqrt(1 + 1 / b))
    return gap, sk, choose_k(gap, sk)


def choose_k(gap: Sequence[float], sk: Sequence[float]) -> int:
    """The smallest k with Gap(k) >= Gap(k + 1) - s_(k+1); kmax if there is none."""
    for k in range(1, len(gap)):
        if gap[k - 1] >= gap[k] - sk[k]:
            return k
    return len(gap)
