# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beso-method/. The authors are listed in prov/0GMFJK.jsonl.

"""Bidirectional evolutionary structural optimization (BESO), soft-kill form.

The structure is a network of axial bars on a line. Bar e joins the nodes
i and j, has the length L_e, the area A_e and the Young's modulus 1. Its design
variable x_e is 1 (solid) or xmin (void), and its stiffness is
x_e^p A_e / L_e. The method minimizes the compliance f^T u for a target
volume, after Huang and Xie (2007, 2009). All arithmetic is exact (Fraction).
"""

from fractions import Fraction as F


class Network:
    def __init__(self, nnodes, bars, fixed, loads):
        """bars: list of (i, j, L, A). fixed: node indices. loads: {node: force}."""
        self.nnodes = nnodes
        self.bars = [(i, j, F(L), F(A)) for i, j, L, A in bars]
        self.fixed = set(fixed)
        self.loads = {k: F(v) for k, v in loads.items()}

    def volume(self, e):
        return self.bars[e][2] * self.bars[e][3]


def gauss_solve(a, b):
    """Solve a x = b exactly by Gaussian elimination with row pivoting."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, n):
            if m[r][col] != 0:
                t = m[r][col] / m[col][col]
                for c in range(col, n + 1):
                    m[r][c] -= t * m[col][c]
    x = [F(0)] * n
    for r in range(n - 1, -1, -1):
        s = m[r][n] - sum(m[r][c] * x[c] for c in range(r + 1, n))
        x[r] = s / m[r][r]
    return x


def solve(net, x, p):
    """Displacements of all nodes and the compliance f^T u."""
    free = [k for k in range(net.nnodes) if k not in net.fixed]
    pos = {k: t for t, k in enumerate(free)}
    n = len(free)
    k = [[F(0)] * n for _ in range(n)]
    for e, (i, j, L, A) in enumerate(net.bars):
        s = x[e] ** p * A / L
        for a, b, sign in ((i, i, 1), (j, j, 1), (i, j, -1), (j, i, -1)):
            if a in pos and b in pos:
                k[pos[a]][pos[b]] += sign * s
    f = [net.loads.get(node, F(0)) for node in free]
    uf = gauss_solve(k, f)
    u = [F(0)] * net.nnodes
    for node, t in pos.items():
        u[node] = uf[t]
    c = sum(net.loads.get(node, F(0)) * u[node] for node in range(net.nnodes))
    return u, c


def sensitivities(net, x, u, p):
    """alpha_e = (1/2) x_e^(p-1) u_e^T k0 u_e / v_e, the strain energy per
    unit volume of the solid bar, scaled by x_e^(p-1) for a void bar."""
    out = []
    for e, (i, j, L, A) in enumerate(net.bars):
        d = u[i] - u[j]
        out.append(x[e] ** (p - 1) * (A / L) * d * d / 2 / (A * L))
    return out


def update(net, x, alpha, target, ar_max, xmin):
    """Lines L8 to L10: a new 0/1 design of volume at most target.

    The elements are ranked by alpha. The solid set is the longest prefix of
    the ranking whose volume is at most the target. If more than ar_max of
    the elements would turn from void to solid, only the best ar_max of them
    are added, and the solid elements fill the rest of the volume.
    """
    n = len(x)
    order = sorted(range(n), key=lambda e: (-alpha[e], e))
    chosen, vol = [], F(0)
    for e in order:  # @line L8
        if vol + net.volume(e) > target:
            break
        chosen.append(e)
        vol += net.volume(e)
    added = [e for e in chosen if x[e] != 1]
    limit = max(1, int(ar_max * n))  # at least one, so small models can add an element
    if len(added) > limit:  # @line L9
        added = added[:limit]
        chosen, vol = list(added), sum((net.volume(e) for e in added), F(0))
        for e in order:
            if x[e] == 1:
                if vol + net.volume(e) > target:
                    break
                chosen.append(e)
                vol += net.volume(e)
    keep = set(chosen)
    return [F(1) if e in keep else xmin for e in range(n)]  # @line L10


def beso(net, target_volume, er=F(1, 50), p=3, xmin=F(1, 1000), ar_max=F(1, 50), tau=F(1, 1000), window=5, maxit=200):
    """Run BESO from the full design. Return (x, history), where history is a
    list of (target volume, volume, compliance) per iteration."""
    n = len(net.bars)
    x = [F(1)] * n  # @line L1
    total = sum(net.volume(e) for e in range(n))
    vt = total
    prev = None
    hist = []
    for it in range(maxit):  # @line L2
        u, c = solve(net, x, p)  # @line L3
        vol = sum(net.volume(e) for e in range(n) if x[e] == 1)
        hist.append((vt, vol, c))
        cs = [h[2] for h in hist]
        if vt == target_volume and len(cs) >= 2 * window:  # @line L4
            a, b = sum(cs[-window:]), sum(cs[-2 * window:-window])
            if abs(a - b) <= tau * a:
                break
        alpha = sensitivities(net, x, u, p)  # @line L5
        if prev is not None:
            alpha = [(a + b) / 2 for a, b in zip(alpha, prev)]  # @line L6
        prev = alpha
        vt = max(F(target_volume), vt * (1 - er))  # @line L7
        x = update(net, x, alpha, vt, ar_max, xmin)
    return x, hist  # @line L11


def parallel_bars(lengths, areas, force=1):
    """Bars between a wall (node 0) and a rigid plate. The plate is modeled by
    giving every bar the same end node 1, which carries the load."""
    bars = [(0, 1, L, A) for L, A in zip(lengths, areas)]
    return Network(2, bars, [0], {1: force})


def series_bars(lengths, areas, force=1):
    """A chain of bars from a wall, loaded at the free end."""
    bars = [(e, e + 1, L, A) for e, (L, A) in enumerate(zip(lengths, areas))]
    return Network(len(bars) + 1, bars, [0], {len(bars): force})


def brute_force(net, target_volume, p=3, xmin=F(1, 1000)):
    """The best 0/1 design with volume at most the target, by enumeration."""
    n = len(net.bars)
    best = None
    for mask in range(1 << n):
        vol = sum(net.volume(e) for e in range(n) if mask >> e & 1)
        if vol > target_volume:
            continue
        x = [F(1) if mask >> e & 1 else xmin for e in range(n)]
        _, c = solve(net, x, p)
        if best is None or c < best[0]:
            best = (c, mask)
    return best
