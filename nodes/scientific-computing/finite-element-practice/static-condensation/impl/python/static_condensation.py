# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/static-condensation/. The authors are listed in prov/G6BEQJ.jsonl.

"""Static condensation of element interior unknowns.

An element has a symmetric positive definite stiffness K and a load F on
its local unknowns, split into interior ones I (used by this element only)
and boundary ones B (shared with neighbors). Static condensation replaces
the element by the Schur complement

    S = K_BB - K_BI K_II^{-1} K_IB,    g = F_B - K_BI K_II^{-1} F_I,

assembles only S and g, solves for the boundary unknowns u_B, and then
recovers u_I = K_II^{-1} (F_I - K_IB u_B) element by element. The result is
exactly the solution of the full system: this is block Gaussian elimination
in a chosen order, not an approximation.

Cost per element with i interior and b boundary unknowns: O(i^3 + i^2 b + i b^2)
(dense Cholesky of K_II and b + 1 solves).
"""

import scimat


def condense(K, F, interior):
    """Return (boundary, S, g, XK, XF) for the local interior index list.

    boundary lists the other local indices in order. XK = K_II^{-1} K_IB and
    XF = K_II^{-1} F_I are kept for the recovery.
    """
    n = len(K)
    inner = list(interior)
    boundary = [r for r in range(n) if r not in set(inner)]  # @line L1
    if not inner:
        return boundary, [[K[r][s] for s in boundary] for r in boundary], [F[r] for r in boundary], [], []
    Kii = [[K[r][s] for s in inner] for r in inner]
    low = scimat.cholesky(Kii)  # one factorization, b + 1 right sides
    cols = [scimat.cholesky_solve(low, [K[r][s] for r in inner]) for s in boundary]  # @line L2
    XK = [[cols[c][a] for c in range(len(boundary))] for a in range(len(inner))]
    XF = scimat.cholesky_solve(low, [F[r] for r in inner])
    S = [[K[r][s] - sum(K[r][inner[a]] * XK[a][c] for a in range(len(inner)))  # @line L3
          for c, s in enumerate(boundary)] for r in boundary]
    g = [F[r] - sum(K[r][inner[a]] * XF[a] for a in range(len(inner))) for r in boundary]
    return boundary, S, g, XK, XF  # @line L4


def recover(XK, XF, uB):
    """Return the interior values u_I = XF - XK u_B."""
    return [XF[a] - sum(XK[a][c] * uB[c] for c in range(len(uB))) for a in range(len(XF))]  # @line L7


def solve_condensed(ndof, elements, fixed):
    """Solve the assembled problem by static condensation.

    elements: list of (dofs, K, F, interior) with dofs the global numbers of
    the local unknowns and interior the local indices to condense (their
    global numbers must not appear in any other element). fixed: dict of
    global unknown -> prescribed value. Return the full global solution.
    """
    data = []
    S_glob = scimat.zeros(ndof)
    g_glob = [0.0] * ndof
    used = set()
    for dofs, K, F, interior in elements:
        boundary, S, g, XK, XF = condense(K, F, interior)
        gb = [dofs[r] for r in boundary]
        for a, r in enumerate(gb):  # @line L5
            g_glob[r] += g[a]
            used.add(r)
            for c, s in enumerate(gb):
                S_glob[r][s] += S[a][c]
        data.append((dofs, interior, gb, XK, XF))
    free = sorted(r for r in used if r not in fixed)
    rhs = [g_glob[r] - sum(S_glob[r][s] * v for s, v in fixed.items()) for r in free]
    x = scimat.solve([[S_glob[r][s] for s in free] for r in free], rhs) if free else []  # @line L6
    u = [0.0] * ndof
    for r, v in fixed.items():
        u[r] = v
    for r, v in zip(free, x):
        u[r] = v
    for dofs, interior, gb, XK, XF in data:
        uI = recover(XK, XF, [u[r] for r in gb])
        for a, r in enumerate(interior):
            u[dofs[r]] = uI[a]
    return u  # @line L8


def solve_full(ndof, elements, fixed):
    """Solve the same problem by assembling every unknown (the reference)."""
    A = scimat.zeros(ndof)
    b = [0.0] * ndof
    for dofs, K, F, _ in elements:
        for r, gr in enumerate(dofs):
            b[gr] += F[r]
            for s, gs in enumerate(dofs):
                A[gr][gs] += K[r][s]
    free = [r for r in range(ndof) if r not in fixed]
    rhs = [b[r] - sum(A[r][s] * v for s, v in fixed.items()) for r in free]
    x = scimat.solve([[A[r][s] for s in free] for r in free], rhs)
    u = [0.0] * ndof
    for r, v in fixed.items():
        u[r] = v
    for r, v in zip(free, x):
        u[r] = v
    return u


def p2_element(h, f=1.0):
    """Return (K, F) of the 1D P2 element for -u'' = f (f constant), unknowns (left, right, middle)."""
    K = [[7 / (3 * h), 1 / (3 * h), -8 / (3 * h)],
         [1 / (3 * h), 7 / (3 * h), -8 / (3 * h)],
         [-8 / (3 * h), -8 / (3 * h), 16 / (3 * h)]]
    F = [f * h / 6, f * h / 6, 2 * f * h / 3]
    return K, F


def p2_mesh(n, f=1.0):
    """Return (ndof, elements) for n equal P2 elements on [0, 1]; vertices 0..n, midpoints n+1..2n."""
    h = 1.0 / n
    elements = []
    for e in range(n):
        K, F = p2_element(h, f)
        elements.append(([e, e + 1, n + 1 + e], K, F, [2]))
    return 2 * n + 1, elements
