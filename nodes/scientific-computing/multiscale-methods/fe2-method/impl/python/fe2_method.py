# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fe2-method/. The authors are listed in prov/6626AA.jsonl.
"""The FE2 method (Feyel 1999) for a nonlinear 1D bar.

Macro problem: a bar on (0, 1) with -(sigma)' = b, u(0) = 0, u(1) = g, where
the stress-strain law of the bar is not known in closed form. P1 elements
on M macro elements, one Gauss point (the midpoint) per element.

Micro problem (the RVE): one period of the microstructure, n micro cells of
length eta = 1 / n with stiffness c[j] and the law

    sigma_j(e) = c[j] e + d e^3,

which is convex in e for c[j] > 0, d >= 0. For a macro strain E the micro
strain is e_j = E + (w[j+1] - w[j]) / eta with a periodic fluctuation w,
w[0] = w[n] = 0. Equilibrium (equal stress in all cells) is solved by
Newton's method with the Thomas algorithm. The macro stress is the mean
micro stress, and the macro tangent is the consistent tangent
<k> - b^T K^-1 b from static condensation of the fluctuation.

Cost: each macro Newton step solves M RVE problems of n - 1 unknowns.
"""

from scisparse import thomas


def micro_law(c, d, e):
    """Stress and tangent of one micro cell."""
    return c * e + d * e ** 3, c + 3 * d * e ** 2


def solve_rve(c, d, E, tol=1e-13, maxit=50):
    """Solve the RVE problem for the mean strain E.

    Returns (Sigma, C, w, iterations): mean stress, consistent tangent,
    fluctuation at the n + 1 micro nodes and the number of micro Newton steps.
    """
    n = len(c)
    eta = 1.0 / n
    w = [0.0] * (n + 1)
    it = 0
    while True:
        strain = [E + (w[j + 1] - w[j]) / eta for j in range(n)]               # @line L4
        s, k = zip(*(micro_law(c[j], d, strain[j]) for j in range(n)))         # @line L4
        # residual of node m: the stress jump s[m-1] - s[m]
        r = [s[m - 1] - s[m] for m in range(1, n)]                             # @line L4
        if n == 1 or max(abs(v) for v in r) <= tol * max(1.0, max(abs(v) for v in s)) or it >= maxit:  # @line L4
            break
        sub = [0.0] + [-k[m - 1] / eta for m in range(2, n)]                   # @line L4
        diag = [(k[m - 1] + k[m]) / eta for m in range(1, n)]                  # @line L4
        sup = [-k[m] / eta for m in range(1, n - 1)] + [0.0]                   # @line L4
        dw = thomas(sub, diag, sup, r)                                         # @line L4
        for m in range(1, n):                                                  # @line L4
            w[m] -= dw[m - 1]                                                  # @line L4
        it += 1
    sigma = sum(s) / n                                                         # @line L5
    # Consistent tangent by static condensation of the fluctuation unknowns:
    # C = <k> - b^T K^-1 b, with K the micro stiffness and b its coupling to E.
    C = sum(k) / n                                                             # @line L5
    if n > 1:
        sub = [0.0] + [-k[m - 1] / eta for m in range(2, n)]                   # @line L5
        diag = [(k[m - 1] + k[m]) / eta for m in range(1, n)]                  # @line L5
        sup = [-k[m] / eta for m in range(1, n - 1)] + [0.0]                   # @line L5
        bvec = [k[m - 1] - k[m] for m in range(1, n)]                          # @line L5
        y = thomas(sub, diag, sup, bvec)                                       # @line L5
        C -= sum(bvec[i] * y[i] for i in range(n - 1)) / (n * eta)             # @line L5
    return sigma, C, w, it


def fe2_bar(c, d, M, g, b, tol=1e-12, maxit=50):
    """FE2 solve of the macro bar. Returns (U, Sigma, iterations)."""
    H = 1.0 / M
    U = [g * i * H for i in range(M + 1)]                                      # @line L1
    it = 0
    while True:                                                                # @line L2
        sig, tan = [], []
        for e in range(M):                                                     # @line L3
            E = (U[e + 1] - U[e]) / H                                          # @line L3
            s, C, _, _ = solve_rve(c, d, E)                                    # @line L4
            sig.append(s)                                                      # @line L5
            tan.append(C)                                                      # @line L5
        r = [sig[i - 1] - sig[i] - b * H for i in range(1, M)]                 # @line L6
        if M == 1 or max(abs(v) for v in r) <= tol or it >= maxit:             # @line L8
            break
        sub = [0.0] + [-tan[i - 1] / H for i in range(2, M)]                   # @line L6
        diag = [(tan[i - 1] + tan[i]) / H for i in range(1, M)]                # @line L6
        sup = [-tan[i] / H for i in range(1, M - 1)] + [0.0]                   # @line L6
        dU = thomas(sub, diag, sup, r)                                         # @line L7
        for i in range(1, M):                                                  # @line L7
            U[i] -= dU[i - 1]                                                  # @line L7
        it += 1
    return U, sig, it                                                          # @line L9


def fine_bar(c, d, periods, g, b, tol=1e-12, maxit=50):
    """Reference: the bar with the microstructure resolved, `periods` copies of c, by P1 Newton."""
    cells = [cj for _ in range(periods) for cj in c]
    N = len(cells)
    h = 1.0 / N
    u = [g * j * h for j in range(N + 1)]
    for _ in range(maxit):
        s, k = zip(*(micro_law(cells[j], d, (u[j + 1] - u[j]) / h) for j in range(N)))
        r = [s[j - 1] - s[j] - b * h for j in range(1, N)]
        if max(abs(v) for v in r) <= tol:
            break
        sub = [0.0] + [-k[j - 1] / h for j in range(2, N)]
        diag = [(k[j - 1] + k[j]) / h for j in range(1, N)]
        sup = [-k[j] / h for j in range(1, N - 1)] + [0.0]
        du = thomas(sub, diag, sup, r)
        for j in range(1, N):
            u[j] -= du[j - 1]
    return u
