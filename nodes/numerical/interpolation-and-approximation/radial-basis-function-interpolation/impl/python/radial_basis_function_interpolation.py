# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radial-basis-function-interpolation/. The authors are listed in prov/QJTKQ6.jsonl.

"""Radial basis function interpolation with an optional polynomial tail.

s(x) = sum_j c_j phi(|x - x_j|) + sum_k d_k p_k(x), with
s(x_i) = y_i and sum_j c_j p_k(x_j) = 0 for every tail monomial p_k.

Points are tuples of coordinates. In one dimension with the kernels
"linear" (r) and "cubic" (r^3), Fraction data give exact results.
"""

import math


def _gaussian(r, eps):
    return math.exp(-(eps * r) ** 2)


def _multiquadric(r, eps):
    return math.sqrt(1 + (eps * r) ** 2)


def _inverse_multiquadric(r, eps):
    return 1 / math.sqrt(1 + (eps * r) ** 2)


def _thin_plate(r, eps):
    return 0 if r == 0 else r * r * math.log(r)


def _linear(r, eps):
    return r


def _cubic(r, eps):
    return r * r * r


KERNELS = {
    "gaussian": (_gaussian, -1),
    "inverse_multiquadric": (_inverse_multiquadric, -1),
    "multiquadric": (_multiquadric, 0),
    "linear": (_linear, 0),
    "thin_plate": (_thin_plate, 1),
    "cubic": (_cubic, 1),
}
# second entry: the least polynomial degree that makes the system
# uniquely solvable for all distinct points (conditional positive
# definiteness order minus one); -1 means no tail is needed.


def _dist(a, b):
    if len(a) == 1:
        return abs(a[0] - b[0])
    return math.sqrt(sum((u - v) * (u - v) for u, v in zip(a, b)))


def _monomials(dim, degree):
    """Exponent tuples of total degree <= degree, in graded order."""
    out = []
    for total in range(degree + 1):
        stack = [((), total)]
        while stack:
            prefix, left = stack.pop()
            if len(prefix) == dim - 1:
                out.append(prefix + (left,))
                continue
            for e in range(left, -1, -1):
                stack.append((prefix + (e,), left - e))
    return out


def _mono_eval(x, e):
    v = 1
    for xi, ei in zip(x, e):
        v = v * xi ** ei
    return v


def _solve(M, b):
    """Gaussian elimination with partial pivoting; ValueError if singular."""
    n = len(M)
    A = [row[:] + [bi] for row, bi in zip(M, b)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(A[r][c]))
        if A[piv][c] == 0:
            raise ValueError("singular interpolation matrix")
        A[c], A[piv] = A[piv], A[c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            if f != 0:
                for k in range(c, n + 1):
                    A[r][k] -= f * A[c][k]
    x = [0] * n
    for r in range(n - 1, -1, -1):
        s = A[r][n] - sum(A[r][k] * x[k] for k in range(r + 1, n))
        x[r] = s / A[r][r]
    return x


def rbf_fit(points, values, kernel="thin_plate", eps=1.0, degree=None):
    """Return a model (kernel, eps, points, c, exponents, d) for rbf_eval.

    degree is the total degree of the polynomial tail; None picks the
    least degree that guarantees solvability for the kernel, and -1
    means no tail. Raises ValueError for repeated points or a
    singular system.
    """
    if kernel not in KERNELS:
        raise ValueError("unknown kernel")
    phi, need = KERNELS[kernel]
    n = len(points)
    if n == 0 or n != len(values):
        raise ValueError("need equally many points and values, at least one")
    dim = len(points[0])
    if len(set(tuple(p) for p in points)) != n:
        raise ValueError("repeated points")
    if degree is None:
        degree = need
    exps = _monomials(dim, degree) if degree >= 0 else []
    m = len(exps)
    A = [[phi(_dist(points[i], points[j]), eps) for j in range(n)]
         for i in range(n)]                                       # @line L1
    P = [[_mono_eval(points[i], e) for e in exps] for i in range(n)]  # @line L2
    zero = values[0] * 0
    M = [A[i] + P[i] for i in range(n)]
    M += [[P[i][k] for i in range(n)] + [zero] * m for k in range(m)]
    sol = _solve(M, list(values) + [zero] * m)                    # @line L3
    return (kernel, eps, [tuple(p) for p in points], sol[:n], exps, sol[n:])  # @line L4


def rbf_eval(model, x):
    """Evaluate the fitted interpolant at the point x."""
    kernel, eps, pts, c, exps, d = model
    phi = KERNELS[kernel][0]
    s = sum(cj * phi(_dist(x, pj), eps) for cj, pj in zip(c, pts))
    s += sum(dk * _mono_eval(x, e) for dk, e in zip(d, exps))   # @line L5
    return s
