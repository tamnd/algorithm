# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-inverse/. The authors are listed in prov/7S6RR0.jsonl.
"""The approximate inverse of Louis and Maass for A x = y.

Pick a mollifier e_p (a smooth bump of width gamma centered at the point p,
with integral 1). Solve the adjoint equation A^T psi_p = e_p once for the
reconstruction kernel psi_p. Then for any data y,

    x_gamma(p) = <y, psi_p> = <A x, psi_p> = <x, A^T psi_p> = <x, e_p>,

which is the mollified solution at p. The kernels depend on A and on the
mollifier only, so they are computed once and used for every data set.

In the discrete form the adjoint equation may have no exact solution, so
psi_p minimizes ||A^T psi - e_p||^2 + beta ||psi||^2, which gives
psi_p = (A A^T + beta I)^(-1) A e_p. With beta = 0 and A square and
nonsingular this is psi_p = A^(-T) e_p.
"""

from imgla import matvec, solve


def hat_mollifier(grid, p, gamma, h):
    """Discrete hat e(t) = (1 / gamma) max(0, 1 - |t - p| / gamma), scaled so h sum e = 1."""
    e = [max(0.0, 1.0 - abs(t - p) / gamma) for t in grid]
    s = h * sum(e)
    return [v / s for v in e]


def kernels(a, mollifiers, beta=0.0):
    """The reconstruction kernels psi_p, one per mollifier row e_p."""
    m = len(a)
    aat = [[sum(p * q for p, q in zip(a[i], a[j])) + (beta if i == j else 0.0)
            for j in range(m)] for i in range(m)]
    rhs = [matvec(a, e) for e in mollifiers]  # @line L2
    cols = solve(aat, [list(r) for r in zip(*rhs)])  # @line L3
    return [list(c) for c in zip(*cols)]  # @line L4


def apply_kernels(psis, y):
    """x_gamma(p) = <y, psi_p> for each kernel."""
    return [sum(p * q for p, q in zip(psi, y)) for psi in psis]  # @line L6


def approximate_inverse(a, mollifiers, ys, beta=0.0):
    """Reconstruct every data set in ys with the same kernels."""
    psis = kernels(a, mollifiers, beta)  # @line L1
    return [apply_kernels(psis, y) for y in ys]  # @line L5


def _integral(ys, h, a, b):
    """int_a^b of the piecewise linear interpolant of the samples ys[j] = y(j h)."""
    def value(t):
        j = min(int(t / h), len(ys) - 2)
        w = t / h - j
        return (1.0 - w) * ys[j] + w * ys[j + 1]

    knots = [a] + [j * h for j in range(int(a / h) + 1, int(b / h) + 1) if a < j * h < b] + [b]
    return sum(0.5 * (t1 - t0) * (value(t0) + value(t1)) for t0, t1 in zip(knots, knots[1:]))


def integration_estimate(ys, h, p, gamma):
    """Closed-form approximate inverse for (A x)(s) = int_0^s x with the hat mollifier.

    The kernel is psi = -e_p', so x_gamma(p) = (1 / gamma^2) [int_p^{p+gamma} y -
    int_{p-gamma}^p y]. ys holds samples of y at s_j = j h, j = 0, ..., N, and the
    integrals use their piecewise linear interpolant. It needs gamma <= p and
    p + gamma <= 1.
    """
    return (_integral(ys, h, p, p + gamma) - _integral(ys, h, p - gamma, p)) / (gamma * gamma)


def integration_kernel_norm(gamma):
    """||psi||_{L^2} = sqrt(2) gamma^(-3/2) for the hat mollifier."""
    return (2.0 / gamma ** 3) ** 0.5
