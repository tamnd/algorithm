# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grabcut/. The authors are listed in prov/KQQ4Z2.jsonl.

"""GrabCut hard segmentation (Rother, Kolmogorov and Blake, 2004).

The image is a list of rows of pixels; a pixel is a number (gray) or a tuple
(color). The trimap has the same shape with 0 for fixed background (T_B), 1
for fixed foreground (T_F) and 2 for unknown pixels (T_U). A rectangle drawn
by the user gives the trimap rect_trimap(w, h, rect): 0 outside, 2 inside.

The energy is E(alpha, k, theta) = sum_n D(alpha_n, k_n, theta, z_n) + V(alpha)
with the data term of a full-covariance Gaussian mixture per label,

    D = -log pi + 1/2 log det S + 1/2 (z - mu)^T S^-1 (z - mu) + eps/2 tr S^-1,

and the contrast-sensitive smoothness term on the 8-neighborhood,

    V = gamma * sum over neighbor pairs (m, n) of [alpha_m != alpha_n] exp(-beta ||z_m - z_n||^2) / dist(m, n).

The last term of D is the expected change of the quadratic term when each
color gets a noise of variance eps per channel. It makes the learned
covariance S = sample covariance + eps I the exact minimizer in step 2, so
every step of the iteration lowers the same energy and no covariance is
singular. The minimum cut is Edmonds-Karp on the unknown pixels.
"""

import math
import random
from collections import deque
from typing import List, Optional, Sequence, Tuple

Color = Tuple[float, ...]


def rect_trimap(w: int, h: int, rect: Tuple[int, int, int, int]) -> List[List[int]]:
    """Trimap for the half-open rectangle (x0, y0, x1, y1): unknown inside, background outside."""
    x0, y0, x1, y1 = rect
    return [[2 if x0 <= x < x1 and y0 <= y < y1 else 0 for x in range(w)] for y in range(h)]


def _colors(img) -> List[Color]:
    return [tuple(float(v) for v in p) if isinstance(p, (tuple, list)) else (float(p),) for row in img for p in row]


def neighbor_pairs(w: int, h: int) -> List[Tuple[int, int, float]]:
    """Each 8-neighbor pair once, as (index, index, distance)."""
    pairs = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            for dx, dy in ((1, 0), (0, 1), (1, 1), (-1, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and ny < h:
                    pairs.append((i, ny * w + nx, math.hypot(dx, dy)))
    return pairs


def _sq(a: Color, b: Color) -> float:
    return sum((u - v) * (u - v) for u, v in zip(a, b))


def contrast_beta(z: Sequence[Color], pairs) -> float:
    """beta = 1 / (2 <||z_m - z_n||^2>) over the neighbor pairs, 0 for a flat image."""
    if not pairs:
        return 0.0
    mean = sum(_sq(z[i], z[j]) for i, j, _ in pairs) / len(pairs)
    return 1.0 / (2.0 * mean) if mean > 0 else 0.0


def pair_weights(z, pairs, gamma: float) -> List[float]:
    beta = contrast_beta(z, pairs)
    return [gamma / d * math.exp(-beta * _sq(z[i], z[j])) for i, j, d in pairs]


# ---- Gaussian components -------------------------------------------------


def _cholesky(a: List[List[float]]) -> List[List[float]]:
    d = len(a)
    low = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            low[i][j] = math.sqrt(s) if i == j else s / low[j][j]
    return low


def _solve_lower(low, b):
    x = []
    for i in range(len(b)):
        x.append((b[i] - sum(low[i][t] * x[t] for t in range(i))) / low[i][i])
    return x


class Gaussian:
    """One mixture component: weight pi, mean mu and covariance S."""

    def __init__(self, pi: float, mu: Color, cov: List[List[float]], eps: float):
        self.pi, self.mu, self.cov, self.eps = pi, mu, cov, eps
        self.low = _cholesky(cov)
        self.logdet = 2.0 * sum(math.log(self.low[i][i]) for i in range(len(mu)))
        d = len(mu)
        # tr S^-1 = ||L^-1||_F^2, column by column.
        self.trinv = sum(sum(v * v for v in _solve_lower(self.low, [1.0 if t == c else 0.0 for t in range(d)])) for c in range(d))

    def cost(self, z: Color) -> float:
        y = _solve_lower(self.low, [a - b for a, b in zip(z, self.mu)])
        return -math.log(self.pi) + 0.5 * self.logdet + 0.5 * sum(v * v for v in y) + 0.5 * self.eps * self.trinv


def fit_gaussian(points: Sequence[Color], total: int, eps: float) -> Gaussian:
    m, d = len(points), len(points[0])
    mu = tuple(sum(p[t] for p in points) / m for t in range(d))
    cov = [[sum((p[a] - mu[a]) * (p[b] - mu[b]) for p in points) / m + (eps if a == b else 0.0) for b in range(d)] for a in range(d)]
    return Gaussian(m / total, mu, cov, eps)


def learn(z, alpha, k, n_comp: int, eps: float, old=None):
    """Step 2: for each label, the weights, means and covariances of its
    components. A component with no pixels gets weight 0 (None). A label with
    no pixels keeps its old model, since the energy does not depend on it."""
    theta = []
    for a in (0, 1):
        members = [n for n in range(len(z)) if alpha[n] == a]
        if not members:
            theta.append(old[a] if old is not None else [None] * n_comp)
            continue
        model = []
        for c in range(n_comp):
            pts = [z[n] for n in members if k[n] == c]
            model.append(fit_gaussian(pts, len(members), eps) if pts else None)
        theta.append(model)
    return theta


def data_cost(theta, a: int, kc: int, z: Color) -> float:
    g = theta[a][kc]
    return math.inf if g is None else g.cost(z)


def best_component(theta, a: int, z: Color) -> Tuple[float, int]:
    """(min over k of D(a, k, theta, z), the first k that reaches it)."""
    best, arg = math.inf, 0
    for c, g in enumerate(theta[a]):
        if g is not None:
            v = g.cost(z)
            if v < best:
                best, arg = v, c
    return best, arg


def assign(z, alpha, theta) -> List[int]:
    """Step 1: give each pixel the component of its own label with the lowest cost."""
    return [best_component(theta, alpha[n], z[n])[1] for n in range(len(z))]


def energy(z, alpha, k, theta, pairs, weights) -> float:
    e = sum(data_cost(theta, alpha[n], k[n], z[n]) for n in range(len(z)))
    return e + sum(wt for (i, j, _), wt in zip(pairs, weights) if alpha[i] != alpha[j])


# ---- Minimum cut ---------------------------------------------------------


def _max_flow_source_side(cap: List[dict], s: int, t: int) -> List[bool]:
    """Edmonds-Karp on the residual capacities cap[u][v]; returns the nodes
    reachable from s in the final residual graph."""
    tiny = 1e-12
    while True:
        parent = [-1] * len(cap)
        parent[s] = s
        queue = deque([s])
        while queue and parent[t] < 0:
            u = queue.popleft()
            for v, c in cap[u].items():
                if c > tiny and parent[v] < 0:
                    parent[v] = u
                    queue.append(v)
        if parent[t] < 0:
            return [p >= 0 for p in parent]
        push, v = math.inf, t
        while v != s:
            push = min(push, cap[parent[v]][v])
            v = parent[v]
        v = t
        while v != s:
            u = parent[v]
            cap[u][v] -= push
            cap[v][u] = cap[v].get(u, 0.0) + push
            v = u


def segment(z, trimap_flat, theta, pairs, weights) -> List[int]:
    """Step 3: the labeling of T_U with the least energy min_k E, by a minimum
    s-t cut. Source side means foreground."""
    unknown = [n for n in range(len(z)) if trimap_flat[n] == 2]
    node = {n: 2 + t for t, n in enumerate(unknown)}
    u0 = {n: best_component(theta, 0, z[n])[0] for n in unknown}
    u1 = {n: best_component(theta, 1, z[n])[0] for n in unknown}
    cap: List[dict] = [dict() for _ in range(2 + len(unknown))]
    for (i, j, _), wt in zip(pairs, weights):
        if i in node and j in node:
            cap[node[i]][node[j]] = cap[node[i]].get(node[j], 0.0) + wt
            cap[node[j]][node[i]] = cap[node[j]].get(node[i], 0.0) + wt
        elif i in node or j in node:
            n, m = (i, j) if i in node else (j, i)
            # A fixed neighbor with label a charges wt when alpha_n != a.
            if trimap_flat[m] == 0:
                u1[n] += wt
            else:
                u0[n] += wt
    for n in unknown:
        low = min(u0[n], u1[n])
        if u0[n] == math.inf and u1[n] == math.inf:
            raise ValueError("both models are empty")
        a0 = u0[n] - low if u0[n] < math.inf else 1e300
        a1 = u1[n] - low if u1[n] < math.inf else 1e300
        cap[0][node[n]] = a0  # paid when n is background (sink side)
        cap[node[n]][1] = a1  # paid when n is foreground (source side)
    side = _max_flow_source_side(cap, 0, 1)
    alpha = [0 if trimap_flat[n] == 0 else 1 for n in range(len(z))]
    for n in unknown:
        alpha[n] = 1 if side[node[n]] else 0
    return alpha


# ---- Initialization ------------------------------------------------------


def kmeans(points: Sequence[Color], n_comp: int, rng: random.Random, rounds: int = 10) -> List[int]:
    """Lloyd's k-means from distinct random seeds, for the initial components."""
    distinct = sorted(set(points))
    centers = rng.sample(distinct, min(n_comp, len(distinct)))
    lab = [0] * len(points)
    for _ in range(rounds):
        lab = [min(range(len(centers)), key=lambda c: (_sq(p, centers[c]), c)) for p in points]
        new = []
        for c in range(len(centers)):
            own = [p for p, q in zip(points, lab) if q == c]
            new.append(tuple(sum(v) / len(own) for v in zip(*own)) if own else centers[c])
        if new == centers:
            break
        centers = new
    return lab


def grabcut(img, trimap, rng: random.Random, n_comp: int = 5, gamma: float = 50.0, eps: float = 1.0, max_iter: int = 20, tol: float = 1e-9):
    """Return (alpha, energies): the 0/1 labels as rows, and the energy after
    the initialization and after each of steps 1, 2 and 3 of every round."""
    h, w = len(img), len(img[0])
    z = _colors(img)
    tri = [v for row in trimap for v in row]
    pairs = neighbor_pairs(w, h)
    weights = pair_weights(z, pairs, gamma)
    alpha = [0 if v == 0 else 1 for v in tri]  # @line L1
    k = [0] * len(z)
    for a in (0, 1):  # @line L2
        idx = [n for n in range(len(z)) if alpha[n] == a]
        if idx:
            for n, c in zip(idx, kmeans([z[n] for n in idx], n_comp, rng)):
                k[n] = c
    theta = learn(z, alpha, k, n_comp, eps)
    energies = [energy(z, alpha, k, theta, pairs, weights)]
    for _ in range(max_iter):  # @line L3
        k = assign(z, alpha, theta)  # @line L4
        energies.append(energy(z, alpha, k, theta, pairs, weights))
        theta = learn(z, alpha, k, n_comp, eps, theta)  # @line L5
        energies.append(energy(z, alpha, k, theta, pairs, weights))
        alpha = segment(z, tri, theta, pairs, weights)  # @line L6
        k = [best_component(theta, alpha[n], z[n])[1] for n in range(len(z))]  # @line L7
        energies.append(energy(z, alpha, k, theta, pairs, weights))
        if energies[-1] >= energies[-4] - tol:  # @line L8
            break
    return [alpha[y * w:(y + 1) * w] for y in range(h)], energies  # @line L9
