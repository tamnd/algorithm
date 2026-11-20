# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/localized-orthogonal-decomposition/. The authors are listed in prov/DNA9DW.jsonl.
"""Localized orthogonal decomposition (Malqvist and Peterseim 2014) in 1D.

Model problem: -(a u')' = f on (0, 1), u(0) = u(1) = 0, with a rough
coefficient a >= alpha > 0 and no assumption of periodicity or scale
separation.

The fine mesh has N = M n cells (one value a[j] per cell) and the coarse
mesh M elements. V_h is the fine P1 space, V_H the coarse P1 space, both
with zero boundary values. The quasi-interpolation is I_H = E_H o Pi_H:
Pi_H is the L2 projection onto P1 on each coarse element (discontinuous),
and E_H takes the mean of the two one-sided values at each interior coarse
node. The fine-scale space is W = {w in V_h : I_H w = 0}.

For each coarse element K and each vertex i of K, the element corrector
q_{K,i} in W(U) solves

    a(q_{K,i}, w) = a_K(lambda_i, w)   for every w in W(U),

where U is the patch of k layers of coarse elements around K (k = None:
the whole domain) and a_K is the energy restricted to K. The constraint
I_H w = 0 is imposed by Lagrange multipliers. The multiscale basis is
lambda_i - sum over K of q_{K,i}, and the method is the Galerkin method in
its span.

The patch problems are solved by dense Gaussian elimination (scimat.solve),
with all right sides of one patch in one call. This is for small checks;
a real code uses sparse solvers.
"""

from scimat import solve


def _cell_moments(v0, v1, t0, t1, h):
    """Exact integral over one fine cell of v * t, with v and t linear on the cell."""
    return h * (2 * v0 * t0 + v0 * t1 + v1 * t0 + 2 * v1 * t1) / 6


def interpolation_rows(N, M):
    """The functionals I_H(.)(x_i) for the interior coarse nodes i = 1 .. M - 1.

    Returns a list of M - 1 rows; row i - 1 has N + 1 coefficients, one per
    fine nodal value.
    """
    n = N // M
    h, H = 1.0 / N, 1.0 / M
    rows = []
    for i in range(1, M):
        row = [0.0] * (N + 1)
        # p_r on element i - 1 and p_l on element i, each with weight 1/2
        for e, side in ((i - 1, "r"), (i, "l")):
            for c in range(n):
                t0, t1 = c / n, (c + 1) / n
                j = e * n + c
                for node, (v0, v1) in ((j, (1.0, 0.0)), (j + 1, (0.0, 1.0))):
                    m_r = _cell_moments(v0, v1, t0, t1, h)
                    m_l = _cell_moments(v0, v1, 1 - t0, 1 - t1, h)
                    p = (2 / H) * (2 * m_r - m_l) if side == "r" else (2 / H) * (2 * m_l - m_r)
                    row[node] += p / 2
        rows.append(row)
    return rows


def coarse_hat(N, M, i):
    """Fine nodal values of the coarse hat function of node i."""
    n = N // M
    v = [0.0] * (N + 1)
    for j in range(max(0, (i - 1) * n), min(N, (i + 1) * n) + 1):
        v[j] = max(0.0, 1 - abs(j - i * n) / n)
    return v


def energy(a, v, w, cells=None):
    """a(v, w) over the given fine cells (all cells if None)."""
    N = len(a)
    if cells is None:
        cells = range(N)
    return sum(a[c] * (v[c + 1] - v[c]) * (w[c + 1] - w[c]) * N for c in cells)


def correctors(a, M, k):
    """All element correctors q_{K,i}. Returns a dict (e, i) -> fine nodal values."""
    N = len(a)
    n = N // M
    rows = interpolation_rows(N, M)
    jobs = {}
    for e in range(M):                                                         # @line L1
        lo_e, hi_e = (0, M - 1) if k is None else (max(0, e - k), min(M - 1, e + k))  # @line L2
        for i in (e, e + 1):
            if 1 <= i <= M - 1:
                jobs.setdefault((lo_e, hi_e), []).append((e, i))
    out = {}
    for (lo_e, hi_e), items in jobs.items():
        nodes = list(range(lo_e * n + 1, (hi_e + 1) * n))                      # @line L3
        cons = [i for i in range(max(1, lo_e), min(M - 1, hi_e + 1) + 1)]      # @line L3
        p, q = len(nodes), len(cons)
        pos = {j: r for r, j in enumerate(nodes)}
        S = [[0.0] * (p + q) for _ in range(p + q)]                            # @line L3
        for r, j in enumerate(nodes):                                          # @line L3
            S[r][r] = (a[j - 1] + a[j]) * N                                    # @line L3
            if j - 1 in pos:
                S[r][pos[j - 1]] = -a[j - 1] * N                               # @line L3
            if j + 1 in pos:
                S[r][pos[j + 1]] = -a[j] * N                                   # @line L3
        for s, i in enumerate(cons):                                           # @line L3
            for r, j in enumerate(nodes):                                      # @line L3
                S[p + s][r] = S[r][p + s] = rows[i - 1][j]                     # @line L3
        rhs = [[0.0] * len(items) for _ in range(p + q)]
        for col, (e, i) in enumerate(items):                                   # @line L3
            lam = coarse_hat(N, M, i)
            for c in range(e * n, (e + 1) * n):                                # a_K(lambda_i, phi_j)
                d = (lam[c + 1] - lam[c]) * N * a[c]
                if c in pos:
                    rhs[pos[c]][col] -= d                                      # @line L3
                if c + 1 in pos:
                    rhs[pos[c + 1]][col] += d                                  # @line L3
        sol = solve(S, rhs)                                                    # @line L3
        for col, (e, i) in enumerate(items):
            v = [0.0] * (N + 1)
            for r, j in enumerate(nodes):
                v[j] = sol[r][col]
            out[(e, i)] = v
    return out


def lod_1d(a, f, M, k):
    """Solve -(a u')' = f with the LOD basis on M coarse elements and patches of k layers.

    a: N fine cell values, f: N + 1 fine nodal values. k = None gives the
    ideal method with global correctors. Returns (U, u, basis).
    """
    N = len(a)
    q = correctors(a, M, k)
    basis = []
    for i in range(1, M):                                                      # @line L4
        phi = coarse_hat(N, M, i)                                              # @line L4
        for (e, ii), v in q.items():                                           # @line L4
            if ii == i:
                phi = [x - y for x, y in zip(phi, v)]                          # @line L4
        basis.append(phi)
    load = fine_load(f)
    A = [[energy(a, bi, bj) for bj in basis] for bi in basis]                  # @line L5
    F = [sum(bi[j] * load[j] for j in range(N + 1)) for bi in basis]           # @line L5
    U = solve(A, F) if basis else []                                           # @line L5
    u = [sum(U[m] * basis[m][j] for m in range(M - 1)) for j in range(N + 1)]  # @line L6
    return U, u, basis


def fine_load(f):
    """Exact integrals of the P1 interpolant of f against the fine hat functions."""
    N = len(f) - 1
    h = 1.0 / N
    load = [0.0] * (N + 1)
    for c in range(N):
        load[c] += h * (2 * f[c] + f[c + 1]) / 6
        load[c + 1] += h * (f[c] + 2 * f[c + 1]) / 6
    return load


def fine_solve(a, f):
    """Reference: the fine P1 solution."""
    N = len(a)
    load = fine_load(f)
    A = [[0.0] * (N - 1) for _ in range(N - 1)]
    for r in range(N - 1):
        j = r + 1
        A[r][r] = (a[j - 1] + a[j]) * N
        if r > 0:
            A[r][r - 1] = -a[j - 1] * N
        if r < N - 2:
            A[r][r + 1] = -a[j] * N
    return [0.0] + solve(A, load[1:N]) + [0.0]


def p1_solve(a, f, M):
    """Standard coarse P1 with exact element integrals of a (for comparison)."""
    N = len(a)
    basis = [coarse_hat(N, M, i) for i in range(1, M)]
    load = fine_load(f)
    A = [[energy(a, bi, bj) for bj in basis] for bi in basis]
    F = [sum(bi[j] * load[j] for j in range(N + 1)) for bi in basis]
    U = solve(A, F)
    return [sum(U[m] * basis[m][j] for m in range(M - 1)) for j in range(N + 1)]
