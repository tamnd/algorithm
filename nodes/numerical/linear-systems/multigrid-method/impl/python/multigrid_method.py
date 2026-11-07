# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multigrid-method/. The authors are listed in prov/ZXX910.jsonl.

"""Geometric multigrid V-cycles for the model problem -u'' = f on (0, 1), u(0) = u(1) = 0.

The grid on level l has n_l = 2^l - 1 interior points and spacing h_l = 1/2^l;
A_l = tridiag(-1, 2, -1) / h_l^2. Restriction is full weighting, prolongation
is linear interpolation, and the coarsest level (one unknown) is solved exactly.
The V-cycle is written as two loops over the levels, without recursion.
Values may be floats or Fractions (with a Fraction omega).
"""

import math
from fractions import Fraction


def level_of(n: int) -> int:
    """L with n = 2^L - 1, or ValueError."""
    L = (n + 1).bit_length() - 1
    if n < 1 or (1 << L) - 1 != n:
        raise ValueError("n must be 2^L - 1 with L >= 1, got %d" % n)
    return L


def apply_a(u: list, h2inv) -> list:
    """A u for A = tridiag(-1, 2, -1) / h^2 with zero boundary values; 4n flops."""
    n = len(u)
    return [(2 * u[i] - (u[i - 1] if i > 0 else 0) - (u[i + 1] if i < n - 1 else 0)) * h2inv
            for i in range(n)]


def residual(f: list, u: list, h2inv) -> list:
    au = apply_a(u, h2inv)
    return [fi - ai for fi, ai in zip(f, au)]


def smooth(u: list, f: list, h2inv, sweeps: int, kind: str = "jacobi", omega=None) -> list:
    """sweeps of weighted Jacobi (default omega 2/3) or forward Gauss-Seidel."""
    n = len(u)
    if kind == "jacobi":
        w = Fraction(2, 3) if omega is None and isinstance(u[0], Fraction) else (2 / 3 if omega is None else omega)
        for _ in range(sweeps):
            r = residual(f, u, h2inv)
            u = [ui + w * ri / (2 * h2inv) for ui, ri in zip(u, r)]
        return u
    if kind == "gs":
        u = list(u)
        h2 = 1 / h2inv
        for _ in range(sweeps):
            for i in range(n):
                s = f[i] * h2 + (u[i - 1] if i > 0 else 0) + (u[i + 1] if i < n - 1 else 0)
                u[i] = s / 2
        return u
    raise ValueError("unknown smoother " + kind)


def restrict(r: list) -> list:
    """Full weighting: coarse i <- (r[2i] + 2 r[2i+1] + r[2i+2]) / 4."""
    return [(r[2 * i] + 2 * r[2 * i + 1] + r[2 * i + 2]) / 4 for i in range((len(r) - 1) // 2)]


def prolong(c: list) -> list:
    """Linear interpolation from n_c to 2 n_c + 1 points."""
    nf = 2 * len(c) + 1
    zero = c[0] * 0
    e = [zero] * nf
    for i, ci in enumerate(c):
        e[2 * i + 1] = ci
    for j in range(0, nf, 2):
        left = c[j // 2 - 1] if j // 2 - 1 >= 0 else zero
        right = c[j // 2] if j // 2 < len(c) else zero
        e[j] = (left + right) / 2
    return e


def v_cycle(u: list, f: list, nu1: int = 2, nu2: int = 1, kind: str = "jacobi", omega=None) -> list:
    """One V(nu1, nu2)-cycle for A_L u = f on the finest level L; returns the new u."""
    L = level_of(len(f))
    us, fs = {L: list(u)}, {L: list(f)}
    for l in range(L, 1, -1):  # @line L3
        h2inv = 4 ** l
        us[l] = smooth(us[l], fs[l], h2inv, nu1, kind, omega)  # @line L4
        fs[l - 1] = restrict(residual(fs[l], us[l], h2inv))  # @line L5
        us[l - 1] = [fs[l - 1][0] * 0] * len(fs[l - 1])
    us[1] = [fs[1][0] / (2 * 4)]  # @line L6
    for l in range(2, L + 1):  # @line L7
        e = prolong(us[l - 1])
        us[l] = [a + b for a, b in zip(us[l], e)]  # @line L8
        us[l] = smooth(us[l], fs[l], 4 ** l, nu2, kind, omega)  # @line L9
    return us[L]


def multigrid(f: list, u0: list | None = None, tol: float = 1e-10, maxiter: int = 100,
              nu1: int = 2, nu2: int = 1, kind: str = "jacobi", omega=None,
              history: list | None = None) -> tuple[list, int, bool]:
    """Repeat V-cycles until ||f - A u||_2 <= tol ||f||_2. Returns (u, cycles, converged)."""
    n = len(f)
    L = level_of(n)
    u = list(u0) if u0 is not None else [f[0] * 0] * n  # @line L1
    nf = math.sqrt(sum(float(v) ** 2 for v in f)) or 1.0
    for it in range(1, maxiter + 1):  # @line L2
        u = v_cycle(u, f, nu1, nu2, kind, omega)
        rn = math.sqrt(sum(float(v) ** 2 for v in residual(f, u, 4 ** L)))
        if history is not None:
            history.append(rn / nf)
        if not rn < 1e300:
            return u, it, False
        if rn <= tol * nf:  # @line L10
            return u, it, True
    return u, maxiter, False  # @line L11


def jacobi_damping(n: int, k: int, omega: float) -> float:
    """Factor by which one weighted Jacobi sweep multiplies the k-th sine mode: 1 - 2 omega sin^2(k pi / (2(n+1)))."""
    return 1 - 2 * omega * math.sin(k * math.pi / (2 * (n + 1))) ** 2
