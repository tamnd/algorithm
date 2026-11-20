# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spherical-harmonics-method/. The authors are listed in prov/HXR9T4.jsonl.
"""The P_N (spherical harmonics) equations in slab geometry.

The angular flux is expanded in Legendre polynomials up to degree N (N odd):

    psi(x, mu) = sum_l (2l + 1) / 2 * phi_l(x) P_l(mu),   phi_l = integral of P_l psi over [-1, 1].

So phi_0 is the scalar flux and phi_1 is the current. Multiplying the
transport equation by P_l and integrating gives, for l = 0, ..., N and
isotropic scattering and source,

    (l + 1) / (2l + 1) phi_(l+1)' + l / (2l + 1) phi_(l-1)' + sigma_l phi_l = q delta_(l0),

with phi_(N+1) = 0, sigma_0 = sigma_t - sigma_s and sigma_l = sigma_t for
l >= 1. In matrix form A u' + S u = q e_0.

pn_slab discretizes this with diamond differences on the cell edges and
solves the whole linear system at once with a banded Gaussian
elimination, so scattering needs no iteration. Each face is "vacuum" or
"reflect"; a vacuum face uses the Marshak conditions (half-range odd
moments of the incoming flux are zero) or the Mark conditions (the
incoming flux is zero at the positive roots of P_(N+1)).
"""

import math


def legendre(n: int, x: float):
    """P_n(x) and P_n'(x)."""
    if n == 0:
        return 1.0, 0.0
    p0, p1 = 1.0, x
    for k in range(2, n + 1):
        p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
    return p1, n * (x * p1 - p0) / (x * x - 1.0)


def legendre_all(n: int, x: float):
    """[P_0(x), ..., P_n(x)]."""
    p = [1.0, x][: n + 1]
    for k in range(2, n + 1):
        p.append(((2 * k - 1) * x * p[k - 1] - (k - 1) * p[k - 2]) / k)
    return p


def gauss_legendre(n: int):
    """Nodes in increasing order and weights of the n-point Gauss-Legendre rule on [-1, 1]."""
    nodes, weights = [0.0] * n, [0.0] * n
    for i in range((n + 1) // 2):
        x = math.cos(math.pi * (i + 0.75) / (n + 0.5))
        for _ in range(100):
            p, dp = legendre(n, x)
            step = p / dp
            x -= step
            if abs(step) < 1e-16:
                break
        p, dp = legendre(n, x)
        w = 2.0 / ((1.0 - x * x) * dp * dp)
        nodes[n - 1 - i], weights[n - 1 - i] = x, w
        nodes[i], weights[i] = -x, w
    return nodes, weights


def moment_matrix(n: int):
    """The (n + 1) x (n + 1) streaming matrix A of the P_n equations."""
    a = [[0.0] * (n + 1) for _ in range(n + 1)]
    for l in range(n + 1):
        if l + 1 <= n:
            a[l][l + 1] = (l + 1) / (2 * l + 1)
        if l >= 1:
            a[l][l - 1] = l / (2 * l + 1)
    return a


def half_range_moments(n: int):
    """H[m][l] = integral of P_m(mu) P_l(mu) over [0, 1], for m, l <= n (exact by Gauss quadrature)."""
    xs, ws = gauss_legendre(n + 1)
    h = [[0.0] * (n + 1) for _ in range(n + 1)]
    for x, w in zip(xs, ws):
        p = legendre_all(n, (x + 1.0) / 2.0)
        for m in range(n + 1):
            for l in range(n + 1):
                h[m][l] += 0.5 * w * p[m] * p[l]
    return h


def solve_sparse(rows, rhs):
    """Gaussian elimination with partial pivoting; rows is a list of dicts (column -> value).

    With the lower bandwidth kl (row i has no entry left of column i - kl), the
    pivot is searched in the rows k to k + kl, and the work is O(n kl^2)."""
    n = len(rows)
    rows = [dict(r) for r in rows]
    rhs = list(rhs)
    kl = max(i - min(r) for i, r in enumerate(rows))
    for k in range(n):
        top = min(n, k + kl + 1)
        p = max(range(k, top), key=lambda i: abs(rows[i].get(k, 0.0)))
        if rows[p].get(k, 0.0) == 0.0:
            raise ValueError("singular system")
        rows[k], rows[p] = rows[p], rows[k]
        rhs[k], rhs[p] = rhs[p], rhs[k]
        piv = rows[k][k]
        for i in range(k + 1, top):
            v = rows[i].get(k, 0.0)
            if v != 0.0:
                f = v / piv
                ri = rows[i]
                for j, a in rows[k].items():
                    ri[j] = ri.get(j, 0.0) - f * a
                del ri[k]
                rhs[i] -= f * rhs[k]
    x = [0.0] * n
    for k in range(n - 1, -1, -1):
        s = rhs[k] - sum(a * x[j] for j, a in rows[k].items() if j > k)
        x[k] = s / rows[k][k]
    return x


def _face_rows(n, face, bc, sign):
    """Rows (lists of coefficients of the n + 1 moments) of the conditions at one face.

    sign = +1 for the left face (incoming mu > 0), -1 for the right face (incoming mu < 0)."""
    out = []
    if face == "reflect":
        for l in range(1, n + 1, 2):
            out.append([1.0 if m == l else 0.0 for m in range(n + 1)])
    elif bc == "mark":
        mus, _ = gauss_legendre(n + 1)
        for mu in mus[(n + 1) // 2:]:
            p = legendre_all(n, sign * mu)
            out.append([(2 * l + 1) / 2.0 * p[l] for l in range(n + 1)])
    else:
        h = half_range_moments(n)
        for m in range(1, n + 1, 2):
            out.append([(2 * l + 1) / 2.0 * h[m][l] * (sign ** l) for l in range(n + 1)])
    return out


def pn_slab(n, sigma_t, sigma_s, q, dx, left="vacuum", right="vacuum", bc="marshak"):
    """Solve the slab P_n equations (n odd) with diamond differences.

    Returns a dict with phi (cell averages of the scalar flux), moments (the
    n + 1 moments at each of the M + 1 edges) and the leakages."""
    if n % 2 == 0:
        raise ValueError("n must be odd")
    m = len(dx)
    k = n + 1
    a = moment_matrix(n)  # @line L1
    rows, rhs = [], []
    for coeffs in _face_rows(n, left, bc, 1):  # @line L2
        rows.append({l: c for l, c in enumerate(coeffs) if c != 0.0})
        rhs.append(0.0)
    for j in range(m):
        for l in range(k):  # @line L3
            sig = sigma_t[j] - (sigma_s[j] if l == 0 else 0.0)
            row = {}
            for c in range(k):
                if a[l][c] != 0.0:
                    row[j * k + c] = row.get(j * k + c, 0.0) - a[l][c] / dx[j]
                    row[(j + 1) * k + c] = row.get((j + 1) * k + c, 0.0) + a[l][c] / dx[j]
            row[j * k + l] = row.get(j * k + l, 0.0) + sig / 2.0
            row[(j + 1) * k + l] = row.get((j + 1) * k + l, 0.0) + sig / 2.0
            rows.append(row)
            rhs.append(q[j] if l == 0 else 0.0)
    for coeffs in _face_rows(n, right, bc, -1):  # @line L4
        rows.append({m * k + l: c for l, c in enumerate(coeffs) if c != 0.0})
        rhs.append(0.0)
    u = solve_sparse(rows, rhs)  # @line L5
    moments = [u[i * k:(i + 1) * k] for i in range(m + 1)]
    phi = [(moments[j][0] + moments[j + 1][0]) / 2.0 for j in range(m)]  # @line L6
    return {"phi": phi, "moments": moments, "leak_left": -moments[0][1], "leak_right": moments[m][1]}


def angular_flux(moments, mu):
    """psi(mu) = sum (2l + 1) / 2 phi_l P_l(mu) from the moments at one point."""
    p = legendre_all(len(moments) - 1, mu)
    return sum((2 * l + 1) / 2.0 * v * p[l] for l, v in enumerate(moments))


def pn_determinant(n, c, kappa):
    """det(S - kappa A) for sigma_t = 1 and the scattering ratio c, by the three-term recurrence."""
    d_prev, d = 1.0, 1.0 - c
    for l in range(1, n + 1):
        d_prev, d = d, d - kappa * kappa * l * l / ((2 * l + 1) * (2 * l - 1)) * d_prev
    return d


def pn_decay_constant(n, c):
    """The smallest kappa > 0 with det(S - kappa A) = 0 (sigma_t = 1): solutions exp(-kappa x) of the infinite medium P_n equations."""
    mus, _ = gauss_legendre(n + 1)
    lo, hi = 0.0, 1.0 / mus[-1]
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if pn_determinant(n, c, mid) > 0.0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def sn_slab(n, sigma_t, sigma_s, q, dx, left="vacuum", right="vacuum", tol=1e-13, max_iter=10000):
    """Reference S_n solution with diamond differences by source iteration.

    The reflected values are lagged by one iteration. Returns (phi, leak_left, leak_right)."""
    mus, ws = gauss_legendre(n)
    m = len(dx)
    phi = [0.0] * m
    back_l = {mu: 0.0 for mu in mus if mu > 0}
    back_r = dict(back_l)
    leak_l = leak_r = 0.0
    for _ in range(max_iter):
        src = [(sigma_s[j] * phi[j] + q[j]) / 2.0 for j in range(m)]
        new = [0.0] * m
        leak_l = leak_r = 0.0
        for mu, w in zip(mus, ws):
            psi = 0.0
            if mu < 0 and right == "reflect":
                psi = back_r[-mu]
            if mu > 0 and left == "reflect":
                psi = back_l[mu]
            cells = range(m) if mu > 0 else range(m - 1, -1, -1)
            for j in cells:
                a = 2.0 * abs(mu) / dx[j]
                c = (src[j] + a * psi) / (sigma_t[j] + a)
                psi = 2.0 * c - psi
                new[j] += w * c
            if mu > 0:
                leak_r += w * mu * psi
                if right == "reflect":
                    back_r[mu] = psi
            else:
                leak_l += w * abs(mu) * psi
                if left == "reflect":
                    back_l[-mu] = psi
        change = max(abs(a - b) for a, b in zip(new, phi))
        phi = new
        if change <= tol * max(phi):
            break
    return phi, (0.0 if left == "reflect" else leak_l), (0.0 if right == "reflect" else leak_r)
