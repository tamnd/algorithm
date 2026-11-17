# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/intelligent-scissors/. The authors are listed in prov/EF89RD.jsonl.

"""Intelligent scissors (live wire) of Mortensen and Barrett (1995).

Pixel p = v * w + u is (u, v) with the gray value img[v][u]. Each pixel links
to its 8 neighbors. The directed local cost of the link p -> q is

    l(p, q) = wZ fZ(q) + wG fG(q) s(p, q) + wD fD(p, q),

with wZ = 0.43, wG = 0.43 and wD = 0.14 as printed in the paper, the
Laplacian zero-crossing cost fZ, the gradient magnitude cost fG, the scale
s = 1 for diagonal and 1 / sqrt(2) for horizontal or vertical links, and the
gradient direction cost fD. live_wire is the 2D dynamic programming search of
the paper, which is Dijkstra's algorithm from the seed point.
"""

import heapq
import math

STEPS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


def _at(img, u, v):
    h, w = len(img), len(img[0])
    return img[min(max(v, 0), h - 1)][min(max(u, 0), w - 1)]


def gradients(img):
    """Central differences with replicated borders: Iu, Iv and G = sqrt(Iu^2 + Iv^2)."""
    h, w = len(img), len(img[0])
    iu = [[(_at(img, u + 1, v) - _at(img, u - 1, v)) / 2.0 for u in range(w)] for v in range(h)]
    iv = [[(_at(img, u, v + 1) - _at(img, u, v - 1)) / 2.0 for u in range(w)] for v in range(h)]
    g = [[math.hypot(iu[v][u], iv[v][u]) for u in range(w)] for v in range(h)]
    return iu, iv, g


def laplacian(img):
    """The 4-neighbor discrete Laplacian with replicated borders."""
    h, w = len(img), len(img[0])
    return [[_at(img, u + 1, v) + _at(img, u - 1, v) + _at(img, u, v + 1) + _at(img, u, v - 1)
             - 4 * img[v][u] for u in range(w)] for v in range(h)]


def zero_crossing_cost(lap):
    """fZ(q) = 0 if the Laplacian changes sign between q and a 4-neighbor r and q is the one closer to zero."""
    h, w = len(lap), len(lap[0])
    fz = [[1.0] * w for _ in range(h)]
    for v in range(h):
        for u in range(w):
            a = lap[v][u]
            for du, dv in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                uu, vv = u + du, v + dv
                if 0 <= uu < w and 0 <= vv < h:
                    b = lap[vv][uu]
                    if a * b < 0 and abs(a) <= abs(b):
                        fz[v][u] = 0.0
    return fz


def local_costs(img, wz=0.43, wg=0.43, wd=0.14):
    """Return adj[p] = list of (q, l(p, q)) for the 8-connected pixel graph."""
    h, w = len(img), len(img[0])
    iu, iv, g = gradients(img)
    gmax = max(max(row) for row in g)
    fz = zero_crossing_cost(laplacian(img))  # @line L10
    dvec = []
    for v in range(h):
        for u in range(w):
            gg = g[v][u]
            dvec.append((iv[v][u] / gg, -iu[v][u] / gg) if gg > 0 else (0.0, 0.0))
    adj = [[] for _ in range(w * h)]
    for v in range(h):
        for u in range(w):
            p = v * w + u
            for du, dv in STEPS:
                uu, vv = u + du, v + dv
                if not (0 <= uu < w and 0 <= vv < h):
                    continue
                q = vv * w + uu
                fg = 1.0 - g[vv][uu] / gmax if gmax > 0 else 1.0  # @line L11
                scale = 1.0 if du != 0 and dv != 0 else 1.0 / math.sqrt(2.0)
                length = math.hypot(du, dv)
                link = (du / length, dv / length)
                dp = dvec[p]
                if dp[0] * link[0] + dp[1] * link[1] < 0:
                    link = (-link[0], -link[1])
                dq = dvec[q]
                a = max(-1.0, min(1.0, dp[0] * link[0] + dp[1] * link[1]))
                b = max(-1.0, min(1.0, link[0] * dq[0] + link[1] * dq[1]))
                fd = 2.0 / (3.0 * math.pi) * (math.acos(a) + math.acos(b))  # @line L12
                adj[p].append((q, wz * fz[vv][uu] + wg * fg * scale + wd * fd))  # @line L13
    return adj


def live_wire(adj, seed):
    """Least total cost g and back pointers from the seed to every pixel (Dijkstra)."""
    n = len(adj)
    g = [math.inf] * n
    back = [None] * n
    expanded = [False] * n
    g[seed] = 0.0  # @line L1
    active = [(0.0, seed)]
    while active:  # @line L2
        gq, q = heapq.heappop(active)  # @line L3
        if expanded[q] or gq > g[q]:
            continue
        expanded[q] = True  # @line L4
        for r, cost in adj[q]:  # @line L5
            if expanded[r]:
                continue
            gtmp = gq + cost  # @line L6
            if gtmp < g[r]:  # @line L7
                g[r] = gtmp  # @line L8
                back[r] = q
                heapq.heappush(active, (gtmp, r))
    return g, back  # @line L9


def path_to(back, seed, t):
    """Follow the back pointers from the free point t to the seed; return the path seed ... t."""
    path = [t]
    while path[-1] != seed:
        nxt = back[path[-1]]
        if nxt is None:
            raise ValueError("t is not reachable from the seed")
        path.append(nxt)
    return path[::-1]


def path_cost(adj, path):
    total = 0.0
    for p, q in zip(path, path[1:]):
        total += dict(adj[p])[q]
    return total


def bellman_ford(adj, seed):
    """Reference shortest path costs, O(n m)."""
    n = len(adj)
    g = [math.inf] * n
    g[seed] = 0.0
    for _ in range(n - 1):
        changed = False
        for p in range(n):
            if g[p] == math.inf:
                continue
            for q, c in adj[p]:
                if g[p] + c < g[q] - 1e-15:
                    g[q] = g[p] + c
                    changed = True
        if not changed:
            break
    return g


def quantize(adj, levels):
    """Round each link cost to an integer in 0 .. levels, as the paper does for its bucket queue."""
    return [[(q, int(round(c * levels))) for q, c in row] for row in adj]


def live_wire_buckets(adj_int, seed, cmax):
    """Dijkstra with a circular bucket queue for integer costs in 0 .. cmax (Dial's method)."""
    n = len(adj_int)
    g = [math.inf] * n
    back = [None] * n
    done = [False] * n
    nb = cmax + 1
    buckets = [[] for _ in range(nb)]
    g[seed] = 0
    buckets[0].append(seed)
    left, cur = 1, 0
    while left:
        while not buckets[cur % nb]:
            cur += 1
        q = buckets[cur % nb].pop()
        left -= 1
        if done[q] or g[q] != cur:
            continue
        done[q] = True
        for r, c in adj_int[q]:
            if not done[r] and cur + c < g[r]:
                g[r] = cur + c
                back[r] = q
                buckets[(cur + c) % nb].append(r)
                left += 1
    return g, back
