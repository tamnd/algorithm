# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiscale-finite-element-method/. The authors are listed in prov/6V214F.jsonl.
"""The multiscale finite element method (Hou and Wu 1997) in 1D.

Model problem: -(a(x) u')' = f on (0, 1), u(0) = u(1) = 0, with a rough
coefficient a >= alpha > 0.

The fine mesh has N = M n cells of size h = 1 / N, with one value a[j] of
the coefficient on cell j. The coarse mesh has M elements; coarse element
e holds the fine cells e n .. e n + n - 1. f is given by its values at the
N + 1 fine nodes and is used through its P1 interpolant, so every integral
below is exact.

On each coarse element the basis function of the right vertex solves the
local problem -(a phi')' = 0 with phi = 0 at the left end and 1 at the
right end, by fine P1 elements. The basis function of the left vertex is
1 - phi. The coarse Galerkin problem in the span of these functions has M - 1
unknowns.

Cost: Theta(N) for the local solves and the element integrals, and
Theta(M) for the coarse solve. Fraction input gives exact output.
"""

from scisparse import thomas


def _fine_cell_load(h, f_left, f_right):
    """Exact integrals of the P1 interpolant of f against the two hat functions of one fine cell."""
    return h * (2 * f_left + f_right) / 6, h * (f_left + 2 * f_right) / 6


def local_basis(a_local, h, kind="msfem"):
    """Nodal values phi_0 .. phi_n of the right-vertex basis function on one coarse element.

    kind = "msfem": the discrete solution of -(a phi')' = 0, phi(0) = 0, phi(n h) = 1.
    kind = "linear": phi_k = k / n, the standard P1 basis (for comparison).
    """
    n = len(a_local)
    if kind == "linear":
        return [type(h)(k) / n for k in range(n + 1)]
    if n == 1:
        return [0 * h, 1 + 0 * h]
    sub = [0] + [-a_local[k - 1] / h for k in range(2, n)]                    # @line L2
    diag = [(a_local[k - 1] + a_local[k]) / h for k in range(1, n)]           # @line L2
    sup = [-a_local[k] / h for k in range(1, n - 1)] + [0]                    # @line L2
    rhs = [0 * h] * (n - 2) + [a_local[n - 1] / h]                            # @line L2
    inner = thomas(sub, diag, sup, rhs)                                       # @line L2
    return [0 * h] + inner + [1 + 0 * h]


def msfem_1d(a, f, M, kind="msfem"):
    """Solve -(a u')' = f, u(0) = u(1) = 0, with M coarse elements.

    a: list of N fine cell values, N a multiple of M.
    f: list of N + 1 nodal values of f on the fine mesh.
    Returns (U, u_fine): U the M + 1 coarse nodal values and u_fine the
    N + 1 fine nodal values of the multiscale solution.
    """
    N = len(a)
    if N % M != 0 or len(f) != N + 1:
        raise ValueError("need len(a) = M n and len(f) = len(a) + 1")
    n = N // M
    zero = 0 * a[0] * f[0]
    h = (1 + zero) / N
    diag = [zero] * (M + 1)
    off = [zero] * M
    F = [zero] * (M + 1)
    basis = []
    for e in range(M):                                                        # @line L1
        lo = e * n
        phi = local_basis(a[lo:lo + n], h, kind)                              # @line L2
        basis.append(phi)
        # psi_right = phi and psi_left = 1 - phi, so psi_left' = -phi'
        k_e = sum(a[lo + k] * (phi[k + 1] - phi[k]) ** 2 / h for k in range(n))  # @line L3
        f_left, f_right = zero, zero
        for k in range(n):                                                    # @line L3
            b0, b1 = _fine_cell_load(h, f[lo + k], f[lo + k + 1])             # @line L3
            f_right += phi[k] * b0 + phi[k + 1] * b1                          # @line L3
            f_left += (1 - phi[k]) * b0 + (1 - phi[k + 1]) * b1               # @line L3
        diag[e] += k_e                                                        # @line L4
        diag[e + 1] += k_e                                                    # @line L4
        off[e] -= k_e                                                         # @line L4
        F[e] += f_left                                                        # @line L4
        F[e + 1] += f_right                                                   # @line L4
    # Dirichlet conditions: the unknowns are U_1 .. U_(M-1).
    m = M - 1
    inner = thomas([zero] + off[1:m], diag[1:M], off[1:m] + [zero], F[1:M]) if m > 0 else []  # @line L5
    U = [zero] + inner + [zero]
    u_fine = [zero] * (N + 1)
    for e in range(M):                                                        # @line L6
        phi = basis[e]                                                        # @line L6
        for k in range(n + 1):                                                # @line L6
            u_fine[e * n + k] = U[e] * (1 - phi[k]) + U[e + 1] * phi[k]       # @line L6
    return U, u_fine


def fine_solve_1d(a, f):
    """Reference: the fine P1 solution of the same problem on all N cells."""
    N = len(a)
    zero = 0 * a[0] * f[0]
    h = (1 + zero) / N
    load = [zero] * (N + 1)
    for j in range(N):
        b0, b1 = _fine_cell_load(h, f[j], f[j + 1])
        load[j] += b0
        load[j + 1] += b1
    sub = [zero] + [-a[j - 1] / h for j in range(2, N)]
    diag = [(a[j - 1] + a[j]) / h for j in range(1, N)]
    sup = [-a[j] / h for j in range(1, N - 1)] + [zero]
    return [zero] + thomas(sub, diag, sup, load[1:N]) + [zero]


def energy_norm(a, v):
    """sqrt of the sum over fine cells of a[j] ((v[j+1] - v[j]) / h)^2 h, in float."""
    N = len(a)
    return sum(float(a[j]) * float(v[j + 1] - v[j]) ** 2 * N for j in range(N)) ** 0.5
