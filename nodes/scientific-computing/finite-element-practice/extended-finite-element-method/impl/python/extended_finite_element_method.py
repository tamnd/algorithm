# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-finite-element-method/. The authors are listed in prov/R1XMNZ.jsonl.

"""Extended finite element method (XFEM) for a one-dimensional bar.

Solves -(E u')' = f on (0, L) with u(0) = u0 and u(L) = uL and an interface
at x = c that may lie anywhere inside an element:

    kind "crack":     a cohesive crack, E u' = k [u] on both sides, [E u'] = 0
                      (Heaviside enrichment, shifted so that it is 0 at the nodes),
    kind "interface": a material interface, [u] = 0 and [E u'] = 0
                      (ridge enrichment of Moes and coauthors 2003),
    kind "none":      standard linear elements on the same mesh, no enrichment.

E is E1 to the left of c and E2 to the right. The mesh never moves with c.
"""

import math

import scimat

GAUSS2 = [(-1 / math.sqrt(3), 1.0), (1 / math.sqrt(3), 1.0)]


class XFEM1D:
    def __init__(self, nodes, c, kind, E1, E2, f=None, u0=0.0, uL=0.0, k=None):
        self.x = list(nodes)
        self.c, self.kind, self.E1, self.E2 = c, kind, E1, E2
        n = len(self.x)
        f = f or (lambda t: 0.0)
        cut = next(e for e in range(n - 1) if self.x[e] < c < self.x[e + 1]) if kind != "none" else None  # @line L1
        self.cut = cut
        self.enriched = [cut, cut + 1] if cut is not None else []
        self.ndof = n + len(self.enriched)
        kmat = scimat.zeros(self.ndof)
        rhs = [0.0] * self.ndof
        for e in range(n - 1):
            a, b = self.x[e], self.x[e + 1]
            pieces = [(a, c), (c, b)] if a < c < b else [(a, b)]  # @line L2
            for (p, q) in pieces:
                for t, w in GAUSS2:
                    xq = (p + q) / 2 + t * (q - p) / 2
                    wq = w * (q - p) / 2
                    dofs, vals, ders = self._functions(e, xq)  # @line L3
                    ex = E1 if xq < c else E2
                    for i, vi, di in zip(dofs, vals, ders):
                        rhs[i] += wq * vi * f(xq)
                        for j, dj in zip(dofs, ders):
                            kmat[i][j] += wq * ex * di * dj  # @line L4
        if kind == "crack":
            # cohesive term k [u][v] at x = c; the jump of the shifted Heaviside term is N_I(c)
            jumps = [(n + m, self._hat(cut, node, c)) for m, node in enumerate(self.enriched)]
            for i, ji in jumps:
                for j, jj in jumps:
                    kmat[i][j] += k * ji * jj  # @line L5
        # Dirichlet values at the two ends (all enrichments vanish at the nodes)
        fixed = {0: u0, n - 1: uL}
        free = [d for d in range(self.ndof) if d not in fixed]
        a_ff = [[kmat[i][j] for j in free] for i in free]
        b_f = [rhs[i] - sum(kmat[i][j] * v for j, v in fixed.items()) for i in free]
        sol = scimat.solve(a_ff, b_f)  # @line L6
        self.u = [0.0] * self.ndof
        for d, v in fixed.items():
            self.u[d] = v
        for d, v in zip(free, sol):
            self.u[d] = v
        self.stiffness = kmat

    def _hat(self, e, node, xq):
        a, b = self.x[e], self.x[e + 1]
        return (b - xq) / (b - a) if node == e else (xq - a) / (b - a)

    def _enrichment(self, xq, node):
        """Return (psi, psi') of the enrichment function attached to the node, at xq."""
        if self.kind == "crack":
            h = 1.0 if xq > self.c else 0.0
            hn = 1.0 if self.x[node] > self.c else 0.0
            return h - hn, 0.0
        # ridge: sum_I N_I |phi_I| - |sum_I N_I phi_I| on the cut element, phi = x - c
        a, b = self.x[self.cut], self.x[self.cut + 1]
        na, nb = (b - xq) / (b - a), (xq - a) / (b - a)
        psi = na * abs(a - self.c) + nb * abs(b - self.c) - abs(xq - self.c)
        dpsi = (abs(b - self.c) - abs(a - self.c)) / (b - a) - (1.0 if xq > self.c else -1.0)
        return psi, dpsi

    def _functions(self, e, xq):
        """Return the global dofs, values and derivatives of the nonzero functions at xq in element e."""
        a, b = self.x[e], self.x[e + 1]
        h = b - a
        dofs = [e, e + 1]
        vals = [(b - xq) / h, (xq - a) / h]
        ders = [-1 / h, 1 / h]
        if e == self.cut:
            for m, node in enumerate(self.enriched):
                psi, dpsi = self._enrichment(xq, node)
                nv, nd = vals[m], ders[m]
                dofs.append(len(self.x) + m)
                vals.append(nv * psi)
                ders.append(nd * psi + nv * dpsi)
        return dofs, vals, ders

    def value(self, xq):
        """Return (u_h(xq), u_h'(xq)); at xq = c the left limit is taken."""
        e = max(0, min(len(self.x) - 2, next((i for i in range(len(self.x) - 1) if xq <= self.x[i + 1]), len(self.x) - 2)))
        dofs, vals, ders = self._functions(e, xq)
        u = sum(self.u[d] * v for d, v in zip(dofs, vals))  # @line L7
        du = sum(self.u[d] * v for d, v in zip(dofs, ders))
        return u, du  # @line L8

    def energy_error(self, du_exact):
        """Return the energy norm error sqrt(int E (u_h' - u')^2) by splitting every element at c."""
        total = 0.0
        for e in range(len(self.x) - 1):
            a, b = self.x[e], self.x[e + 1]
            pieces = [(a, self.c), (self.c, b)] if a < self.c < b else [(a, b)]
            for p, q in pieces:
                for t, w in GAUSS2:
                    xq = (p + q) / 2 + t * (q - p) / 2
                    dofs, _, ders = self._functions(e, xq)
                    duh = sum(self.u[d] * v for d, v in zip(dofs, ders))
                    ex = self.E1 if xq < self.c else self.E2
                    total += w * (q - p) / 2 * ex * (duh - du_exact(xq)) ** 2
        return math.sqrt(total)


def exact_piecewise_linear(c, E1, E2, u0, uL, L=1.0, k=None):
    """Return (u, du, sigma) of the exact solution for f = 0, with an optional cohesive crack."""
    compliance = c / E1 + (L - c) / E2 + (1 / k if k else 0.0)
    sigma = (uL - u0) / compliance
    jump = sigma / k if k else 0.0

    def u(x):
        if x <= c:
            return u0 + sigma / E1 * x
        return u0 + sigma / E1 * c + jump + sigma / E2 * (x - c)

    def du(x):
        return sigma / E1 if x < c else sigma / E2

    return u, du, sigma
