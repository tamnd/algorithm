# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-cell-method/. The authors are listed in prov/DX2BFW.jsonl.
"""The finite cell method for a 1D bar.

The physical bar is (0, a) with stiffness E, load f and u(0) = 0, and its
end x = a is free or carries a point load P. It is embedded in the cells of
(0, L), L > a. The fictitious part (a, L) gets the stiffness alpha E and no
load. The basis is the p-version basis of integrated Legendre polynomials,
continuous across cells. Cut cells are integrated either by splitting them
exactly at x = a, or by recursive bisection toward x = a with the
coefficient taken at each Gauss point, as the method does in 2D and 3D.
"""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from ig2kit import gauss_legendre, solve_dense


def shapes(xi: float, p: int) -> Tuple[List[float], List[float]]:
    """Values and xi-derivatives of the p + 1 shape functions on [-1, 1].

    N_0 = (1 - xi)/2 and N_1 = (1 + xi)/2 are the nodal modes. For k = 2..p,
    N_k = (P_k - P_{k-2}) / (2k - 1), the integral of the Legendre polynomial
    P_{k-1} from -1; it vanishes at both ends, and its derivative is P_{k-1}.
    """
    leg = [1.0, xi]
    for k in range(2, p + 1):
        leg.append(((2 * k - 1) * xi * leg[-1] - (k - 1) * leg[-2]) / k)
    val = [(1 - xi) / 2, (1 + xi) / 2]
    der = [-0.5, 0.5]
    for k in range(2, p + 1):
        val.append((leg[k] - leg[k - 2]) / (2 * k - 1))
        der.append(leg[k - 1])
    return val, der


class FiniteCellBar:
    def __init__(
        self,
        length: float,
        ncell: int,
        p: int,
        a: float,
        alpha: float,
        f: Callable[[float], float],
        E: float = 1.0,
        P: float = 0.0,
        depth: Optional[int] = None,
        ng: Optional[int] = None,
    ):
        self.L, self.p, self.a, self.alpha, self.f, self.E, self.P = length, p, a, alpha, f, E, P
        self.depth = depth  # None: split cut cells at a; an integer: bisect that many times
        self.ng = ng or p + 3
        self.x = [length * c / ncell for c in range(ncell + 1)]
        # Keep only the cells that hold some material (L1).
        self.cells = [c for c in range(ncell) if self.x[c] < a]
        nc = len(self.cells)
        # Dofs: vertex k has dof k - 1 (vertex 0 is fixed by u(0) = 0), then p - 1 inner modes per cell.
        self.ndof = nc + nc * (p - 1)

    def dofs(self, c: int) -> List[Optional[int]]:
        nc, p = len(self.cells), self.p
        left = None if c == 0 else c - 1
        inner = [nc + c * (p - 1) + k for k in range(p - 1)]
        return [left, c] + inner

    def subcells(self, x0: float, x1: float) -> List[Tuple[float, float]]:
        a = self.a
        if not (x0 < a < x1):
            return [(x0, x1)]
        if self.depth is None:
            return [(x0, a), (a, x1)]  # @line L2
        leaves, todo = [], [(x0, x1, 0)]
        while todo:
            s0, s1, d = todo.pop()
            if s0 < a < s1 and d < self.depth:
                m = 0.5 * (s0 + s1)
                todo += [(s0, m, d + 1), (m, s1, d + 1)]
            else:
                leaves.append((s0, s1))
        return sorted(leaves)

    def assemble(self):
        n, p = self.ndof, self.p
        K = [[0.0] * n for _ in range(n)]
        F = [0.0] * n
        gx, gw = gauss_legendre(self.ng)
        for c in self.cells:  # @line L1
            x0, x1 = self.x[c], self.x[c + 1]
            h = x1 - x0
            ke = [[0.0] * (p + 1) for _ in range(p + 1)]
            fe = [0.0] * (p + 1)
            for s0, s1 in self.subcells(x0, x1):
                for t, w in zip(gx, gw):  # @line L3
                    x = 0.5 * (s0 + s1) + 0.5 * (s1 - s0) * t
                    wt = 0.5 * (s1 - s0) * w
                    xi = 2 * (x - x0) / h - 1
                    val, der = shapes(xi, p)
                    dN = [d * 2 / h for d in der]
                    k = self.E if x < self.a else self.alpha * self.E  # @line L4
                    for i in range(p + 1):
                        for j in range(p + 1):
                            ke[i][j] += k * dN[i] * dN[j] * wt  # @line L5
                        if x < self.a:
                            fe[i] += self.f(x) * val[i] * wt
            if x0 < self.a < x1 and self.P:
                val, _ = shapes(2 * (self.a - x0) / h - 1, p)
                for i in range(p + 1):
                    fe[i] += self.P * val[i]
            dof = self.dofs(self.cells.index(c))
            for i, gi in enumerate(dof):  # @line L6
                if gi is None:
                    continue  # @line L7
                F[gi] += fe[i]
                for j, gj in enumerate(dof):
                    if gj is not None:
                        K[gi][gj] += ke[i][j]
        return K, F

    def solve(self) -> List[float]:
        K, F = self.assemble()
        self.coef = solve_dense(K, F)  # @line L8
        return self.coef

    def value(self, x: float, nd: int = 0) -> float:
        """u_h(x) (nd = 0) or u_h'(x) (nd = 1) for x in the active cells."""
        for idx, c in enumerate(self.cells):
            x0, x1 = self.x[c], self.x[c + 1]
            if x0 <= x <= x1:
                h = x1 - x0
                val, der = shapes(2 * (x - x0) / h - 1, self.p)
                row = val if nd == 0 else [d * 2 / h for d in der]
                return sum(r * self.coef[g] for r, g in zip(row, self.dofs(idx)) if g is not None)
        raise ValueError("x is outside the active cells")

    def errors(self, exact: Callable, dexact: Callable, samples: int = 400) -> Tuple[float, float]:
        """(largest |u_h - u| on [0, a], energy norm error on (0, a)); measured, not proved."""
        a = self.a
        emax = max(abs(self.value(a * k / samples) - exact(a * k / samples)) for k in range(samples + 1))
        gx, gw = gauss_legendre(12)
        en = 0.0
        pts = sorted({min(xc, a) for xc in self.x} | {a})
        for s0, s1 in zip(pts, pts[1:]):
            for t, w in zip(gx, gw):
                x = 0.5 * (s0 + s1) + 0.5 * (s1 - s0) * t
                en += self.E * (self.value(x, 1) - dexact(x)) ** 2 * 0.5 * (s1 - s0) * w
        return emax, en**0.5


def stiffness_parts(bar: FiniteCellBar) -> Tuple[List[List[float]], List[List[float]]]:
    """(K0, K1) with K(alpha) = K0 + alpha K1: the physical and the fictitious stiffness."""
    keep = bar.alpha
    bar.alpha = 0.0
    K0, _ = bar.assemble()
    bar.alpha = 1.0
    Kt, _ = bar.assemble()
    bar.alpha = keep
    K1 = [[t - s for t, s in zip(rt, r0)] for rt, r0 in zip(Kt, K0)]
    return K0, K1


def extension_constant(bar: FiniteCellBar, iters: int = 300) -> float:
    """C_ext = max over the discrete space of a1(v, v) / a0(v, v), the largest eigenvalue of K0^-1 K1."""
    K0, K1 = stiffness_parts(bar)
    n = len(K0)
    v = [1.0 + 0.01 * i for i in range(n)]
    lam = 0.0
    for _ in range(iters):
        w = solve_dense(K0, [sum(K1[i][j] * v[j] for j in range(n)) for i in range(n)])
        nw = max(abs(t) for t in w)
        lam = nw / max(abs(t) for t in v)
        v = [t / nw for t in w]
    return lam


def condition_estimate(K: List[List[float]], iters: int = 200) -> float:
    """Ratio of the largest to the smallest eigenvalue of an SPD matrix by power and inverse iteration."""
    n = len(K)

    def norm(v):
        return sum(t * t for t in v) ** 0.5

    v = [1.0 + 0.1 * i for i in range(n)]
    lmax = 0.0
    for _ in range(iters):
        w = [sum(K[i][j] * v[j] for j in range(n)) for i in range(n)]
        lmax = norm(w) / norm(v)
        v = [t / norm(w) for t in w]
    v = [1.0 + 0.1 * i for i in range(n)]
    lmin_inv = 0.0
    for _ in range(iters):
        w = solve_dense(K, v)
        lmin_inv = norm(w) / norm(v)
        v = [t / norm(w) for t in w]
    return lmax * lmin_inv
