# SPDX-License-Identifier: MIT
# Shared helper of the pr2 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Resistive power grids in drop form, and a dense direct solver.

A grid has nodes 0 .. N-1. Each wire between nodes a and b has a conductance
g > 0. A node k can have a pad conductance gpad[k] > 0 to the ideal supply,
and a load current cur[k] >= 0 that it draws to ground. With the drop
x = VDD - v, Kirchhoff's current law gives G x = cur with G = L + diag(gpad),
where L is the weighted Laplacian of the wires.

This module builds grids and matrices and solves dense systems by Gaussian
elimination. It works with float or with fractions.Fraction. It holds no
power grid analysis method of the pr2 pages.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Callable, Dict, List, Optional, Sequence, Tuple


class Grid:
    """Wires as adjacency lists, pad conductances and load currents."""

    def __init__(self, n: int):
        self.n = n
        self.adj: List[Dict[int, object]] = [dict() for _ in range(n)]
        self.gpad: List[object] = [0] * n
        self.cur: List[object] = [0] * n
        self.shape: Optional[Tuple[int, int]] = None

    def add_wire(self, a: int, b: int, g) -> None:
        if a == b or g <= 0:
            raise ValueError("a wire joins two different nodes with g > 0")
        self.adj[a][b] = self.adj[a].get(b, 0) + g
        self.adj[b][a] = self.adj[b].get(a, 0) + g

    def degree(self, k: int):
        """D_k: the sum of all conductances at node k, pad included."""
        return sum(self.adj[k].values()) + self.gpad[k]

    def matrix(self) -> List[List[object]]:
        """The dense matrix G = L + diag(gpad)."""
        zero = self.gpad[0] * 0
        a = [[zero] * self.n for _ in range(self.n)]
        for k in range(self.n):
            a[k][k] = self.degree(k)
            for j, g in self.adj[k].items():
                a[k][j] = a[k][j] - g
        return a

    def every_part_has_a_pad(self) -> bool:
        """True when each connected part of the wire graph holds a pad."""
        seen = [False] * self.n
        for s in range(self.n):
            if seen[s]:
                continue
            stack, part = [s], []
            seen[s] = True
            while stack:
                k = stack.pop()
                part.append(k)
                for j in self.adj[k]:
                    if not seen[j]:
                        seen[j] = True
                        stack.append(j)
            if not any(self.gpad[k] > 0 for k in part):
                return False
        return True


def mesh(
    nx: int,
    ny: int,
    g_h: Callable[[int, int], object],
    g_v: Callable[[int, int], object],
    pads: Dict[int, object],
    cur: Sequence[object],
) -> Grid:
    """An nx by ny mesh. Node (r, c) has the index r * nx + c.

    g_h(r, c) is the wire from (r, c) to (r, c + 1), and g_v(r, c) the wire
    from (r, c) to (r + 1, c).
    """
    grid = Grid(nx * ny)
    grid.shape = (nx, ny)
    for r in range(ny):
        for c in range(nx):
            k = r * nx + c
            if c + 1 < nx:
                grid.add_wire(k, k + 1, g_h(r, c))
            if r + 1 < ny:
                grid.add_wire(k, k + nx, g_v(r, c))
    for k, g in pads.items():
        grid.gpad[k] = g
    grid.cur = list(cur)
    return grid


def random_mesh(nx: int, ny: int, rng: random.Random, exact: bool = True, n_pads: int = 2) -> Grid:
    """A mesh with conductances in {1, ..., 5}, a few pads and loads in {0, ..., 4}."""
    num = Fraction if exact else float
    gh = {(r, c): num(rng.randint(1, 5)) for r in range(ny) for c in range(nx)}
    gv = {(r, c): num(rng.randint(1, 5)) for r in range(ny) for c in range(nx)}
    n = nx * ny
    pads = {k: num(rng.randint(2, 8)) for k in rng.sample(range(n), min(n_pads, n))}
    cur = [num(rng.randint(0, 4)) for _ in range(n)]
    return mesh(nx, ny, lambda r, c: gh[(r, c)], lambda r, c: gv[(r, c)], pads, cur)


def solve(a: Sequence[Sequence[object]], b: Sequence[object]) -> List[object]:
    """Solve a x = b by Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if m[piv][col] == 0:
            raise ZeroDivisionError("singular matrix")
        m[col], m[piv] = m[piv], m[col]
        p = m[col][col]
        for r in range(col + 1, n):
            f = m[r][col] / p
            if f != 0:
                row, top = m[r], m[col]
                for c in range(col, n + 1):
                    row[c] = row[c] - f * top[c]
    x = [m[0][0] * 0] * n
    for r in range(n - 1, -1, -1):
        s = m[r][n]
        for c in range(r + 1, n):
            s = s - m[r][c] * x[c]
        x[r] = s / m[r][r]
    return x


def matvec(a: Sequence[Sequence[object]], x: Sequence[object]) -> List[object]:
    return [sum((row[j] * x[j] for j in range(len(x))), x[0] * 0) for row in a]


def transpose(a: Sequence[Sequence[object]]) -> List[List[object]]:
    return [list(col) for col in zip(*a)]


def matmul(a: Sequence[Sequence[object]], b: Sequence[Sequence[object]]) -> List[List[object]]:
    bt = transpose(b)
    zero = a[0][0] * 0
    out = []
    for row in a:
        nz = [(j, v) for j, v in enumerate(row) if v != 0]
        out.append([sum((v * col[j] for j, v in nz), zero) for col in bt])
    return out
