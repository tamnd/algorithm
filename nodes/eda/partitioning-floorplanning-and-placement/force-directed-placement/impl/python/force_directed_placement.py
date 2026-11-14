# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-directed-placement/. The authors are listed in prov/82M4RX.jsonl.

"""Force-directed placement: zero-force relaxation of springs, with spreading forces.

Pins 0 .. n-1 are the movable cells and pins n, n+1, ... are the fixed pads.
A cell position is the center of the cell, and every pin sits at that center.
Each net becomes springs by the clique model: every pair of its p pins gets w_e / (p - 1).
The spreading force is a simple density difference between neighboring bins, added
to an extra force e_i that grows round by round, as in Kraftwerk.
"""

from fractions import Fraction


def springs(n, nets, weights=None):
    """Adjacency lists {j: w_ij} for the cells, by the clique model."""
    adj = [dict() for _ in range(n)]
    for k, e in enumerate(nets):
        pins = sorted(set(e))
        p = len(pins)
        if p < 2:
            continue
        w = (Fraction(1) if weights is None else Fraction(weights[k])) / (p - 1)
        for a in range(p):
            for b in range(p):
                if a != b and pins[a] < n:
                    adj[pins[a]][pins[b]] = adj[pins[a]].get(pins[b], 0) + w
    return adj


def energy(x, y, adj, pads, ex, ey):
    """Phi = 1/2 sum over springs w_ij |p_i - p_j|^2 - sum_i (ex_i x_i + ey_i y_i).
    A cell-to-cell spring appears in both lists, so it is counted with 1/4 per side."""
    n = len(x)
    total = 0
    for i in range(n):
        for j, w in adj[i].items():
            xj, yj = (x[j], y[j]) if j < n else pads[j - n]
            half = Fraction(1, 4) if j < n else Fraction(1, 2)
            total += half * w * ((x[i] - xj) ** 2 + (y[i] - yj) ** 2)
        total -= ex[i] * x[i] + ey[i] * y[i]
    return total


def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def bin_density(x, y, W, H, X, Y, B):
    """Area of the cells in each bin of side B over [0, X] x [0, Y], divided by B^2.
    A cell of width W_i and height H_i is centered at (x_i, y_i). Each cell visits only its bins."""
    nu, nv = X // B, Y // B
    D = [[Fraction(0)] * nv for _ in range(nu)]
    for i in range(len(x)):
        x0, x1 = x[i] - W[i] / Fraction(2), x[i] + W[i] / Fraction(2)
        y0, y1 = y[i] - H[i] / Fraction(2), y[i] + H[i] / Fraction(2)
        for u in range(max(0, int(x0 // B)), min(nu, int(x1 // B) + 1)):
            ox = min(x1, (u + 1) * B) - max(x0, u * B)
            if ox <= 0:
                continue
            for v in range(max(0, int(y0 // B)), min(nv, int(y1 // B) + 1)):
                oy = min(y1, (v + 1) * B) - max(y0, v * B)
                if oy > 0:
                    D[u][v] += ox * oy / (B * B)
    return D


def overflow(D):
    """Total density above 1 over the bins, in units of bin area."""
    return sum(max(0, d - 1) for col in D for d in col)


def force_directed(n, nets, pads, W, H, X, Y, B, rounds=10, sweeps=20, kappa=Fraction(1, 2),
                   weights=None, start=None, trace=None):
    """Return the cell centers (x, y) after `rounds` rounds of relaxation and spreading.
    If trace is a list, the energy Phi is appended after every single cell move."""
    adj = springs(n, nets, weights)  # @line L1
    for i in range(n):
        if not adj[i]:
            raise ValueError("a cell with no net has no zero-force position")
    if start is None:
        cx = sum(Fraction(p[0]) for p in pads) / len(pads)
        cy = sum(Fraction(p[1]) for p in pads) / len(pads)
        start = [(cx, cy)] * n
    # Fractions stay exact; floats (for long runs) stay floats.
    x = [p[0] if isinstance(p[0], float) else Fraction(p[0]) for p in start]
    y = [p[1] if isinstance(p[1], float) else Fraction(p[1]) for p in start]
    ex = [Fraction(0)] * n  # @line L2
    ey = [Fraction(0)] * n
    deg = [sum(adj[i].values()) for i in range(n)]
    for _ in range(rounds):  # @line L3
        for _ in range(sweeps):  # @line L4
            for i in range(n):  # @line L5
                sx = sum(w * (x[j] if j < n else pads[j - n][0]) for j, w in adj[i].items())
                sy = sum(w * (y[j] if j < n else pads[j - n][1]) for j, w in adj[i].items())
                x[i] = clamp((sx + ex[i]) / deg[i], W[i] / Fraction(2), X - W[i] / Fraction(2))  # @line L6
                y[i] = clamp((sy + ey[i]) / deg[i], H[i] / Fraction(2), Y - H[i] / Fraction(2))
                if trace is not None:
                    trace.append(energy(x, y, adj, pads, ex, ey))
        D = bin_density(x, y, W, H, X, Y, B)  # @line L7
        nu, nv = len(D), len(D[0])

        def at(u, v):
            return D[u][v] if 0 <= u < nu and 0 <= v < nv else Fraction(0)

        for i in range(n):  # @line L8
            u = min(nu - 1, int(x[i] // B))
            v = min(nv - 1, int(y[i] // B))
            ex[i] += kappa * deg[i] * B * (at(u - 1, v) - at(u + 1, v)) / 2  # @line L9
            ey[i] += kappa * deg[i] * B * (at(u, v - 1) - at(u, v + 1)) / 2
    return x, y  # @line L10
