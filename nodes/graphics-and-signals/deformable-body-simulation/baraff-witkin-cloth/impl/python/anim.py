# SPDX-License-Identifier: MIT
# Shared helper of the graphics-and-signals animation and simulation pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small vectors, matrices, polar decomposition, quaternions and transforms.

This file is copied byte for byte into each impl/python folder that needs it.
It holds no method of a page: no curve, no skinning, no integrator step, no
collision test and no solver of a page. The method of each page lives in its
slug file.

Conventions (prompts/graphics-ext.md, "Mathematical conventions"):
- Vectors are tuples. Functions accept lists too and return tuples.
- Matrices are lists of rows, and a matrix acts on a column vector on the
  left: x' = M x.
- Quaternions use the Hamilton convention, scalar first, q = (w, x, y, z)
  with i j = k. A unit quaternion q rotates v by v' = q (0, v) q*.
- The log of a unit quaternion (cos phi, sin phi u) is (0, phi u), and the
  rotation angle is 2 phi. q_exp is the inverse map.
- Angles are in radians.
"""

import math

# Below this angle on the sphere of R^4, slerp uses normalized linear
# interpolation (nlerp), which avoids the division by sin(W).
SLERP_SMALL_ANGLE = 1e-6


# ---------------------------------------------------------------- vectors


def add(a, b):
    """Return a + b."""
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    """Return a - b."""
    return tuple(x - y for x, y in zip(a, b))


def scale(a, s):
    """Return s a for a number s."""
    return tuple(s * x for x in a)


def dot(a, b):
    """Return the dot product of a and b."""
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    """Return the cross product of two 3D vectors."""
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def cross2(a, b):
    """Return the scalar 2D cross product a_x b_y - a_y b_x."""
    return a[0] * b[1] - a[1] * b[0]


def norm(a):
    """Return the Euclidean length of a."""
    return math.sqrt(sum(x * x for x in a))


def normalize(a):
    """Return a / |a|. Raise ValueError for the zero vector."""
    n = norm(a)
    if n == 0.0:
        raise ValueError("cannot normalize the zero vector")
    return tuple(x / n for x in a)


def lerp(a, b, t):
    """Return (1 - t) a + t b."""
    return tuple((1 - t) * x + t * y for x, y in zip(a, b))


# ---------------------------------------------------------------- matrices


def zeros(n, m=None):
    """Return the n by m zero matrix (n by n if m is None)."""
    if m is None:
        m = n
    return [[0.0] * m for _ in range(n)]


def eye(n):
    """Return the n by n identity matrix."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def mul(a, b):
    """Return the matrix product a b."""
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a, x):
    """Return the vector a x as a tuple."""
    return tuple(sum(p * q for p, q in zip(row, x)) for row in a)


def transpose(a):
    """Return the transpose of a."""
    return [list(col) for col in zip(*a)]


def _lu(a):
    """Gaussian elimination with partial pivoting on a copy of a square a.

    Return (lu, perm, sign), or None if a pivot is exactly zero.
    """
    n = len(a)
    lu = [list(map(float, row)) for row in a]
    perm = list(range(n))
    sign = 1.0
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(lu[i][k]))
        if lu[p][k] == 0.0:
            return None
        if p != k:
            lu[k], lu[p] = lu[p], lu[k]
            perm[k], perm[p] = perm[p], perm[k]
            sign = -sign
        piv = lu[k][k]
        for i in range(k + 1, n):
            f = lu[i][k] / piv
            lu[i][k] = f
            if f != 0.0:
                rk = lu[k]
                ri = lu[i]
                for j in range(k + 1, n):
                    ri[j] -= f * rk[j]
    return lu, perm, sign


def det(a):
    """Return the determinant of a square matrix."""
    n = len(a)
    if n == 1:
        return a[0][0]
    if n == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if n == 3:
        return (
            a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
        )
    r = _lu(a)
    if r is None:
        return 0.0
    lu, _, sign = r
    d = sign
    for i in range(n):
        d *= lu[i][i]
    return d


def _lu_solve(lu, perm, b):
    n = len(lu)
    y = [float(b[perm[i]]) for i in range(n)]
    for i in range(n):
        s = y[i]
        row = lu[i]
        for j in range(i):
            s -= row[j] * y[j]
        y[i] = s
    for i in range(n - 1, -1, -1):
        s = y[i]
        row = lu[i]
        for j in range(i + 1, n):
            s -= row[j] * y[j]
        y[i] = s / row[i]
    return y


def solve(a, b):
    """Solve a x = b by Gaussian elimination with partial pivoting.

    b is a vector (returns a list) or a matrix given as a list of rows
    (returns a list of rows, one column of x per column of b).
    Raise ValueError if a is singular.
    """
    r = _lu(a)
    if r is None:
        raise ValueError("singular matrix")
    lu, perm, _ = r
    if len(b) > 0 and isinstance(b[0], (list, tuple)):
        cols = [_lu_solve(lu, perm, col) for col in zip(*b)]
        return [list(row) for row in zip(*cols)]
    return _lu_solve(lu, perm, b)


def inv(a):
    """Return the inverse of a square matrix. Raise ValueError if singular."""
    return solve(a, eye(len(a)))


# ---------------------------------------------------------------- polar decomposition


def rot2(theta):
    """Return the 2 by 2 rotation matrix by the angle theta."""
    c, s = math.cos(theta), math.sin(theta)
    return [[c, -s], [s, c]]


def _frob(a):
    return math.sqrt(sum(x * x for row in a for x in row))


def _sym_eig3(s):
    """Eigenvalues and eigenvectors of a symmetric 3 by 3 matrix (cyclic Jacobi).

    Return (values, vectors), where vectors[k] is the unit eigenvector of
    values[k].
    """
    a = [list(map(float, row)) for row in s]
    v = eye(3)
    for _ in range(50):
        off = a[0][1] ** 2 + a[0][2] ** 2 + a[1][2] ** 2
        if off <= 1e-30 * (sum(a[i][i] ** 2 for i in range(3)) + 1e-300):
            break
        for p, q in ((0, 1), (0, 2), (1, 2)):
            if a[p][q] == 0.0:
                continue
            theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
            t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
            c = 1.0 / math.sqrt(t * t + 1.0)
            sn = t * c
            for k in range(3):
                akp, akq = a[k][p], a[k][q]
                a[k][p] = c * akp - sn * akq
                a[k][q] = sn * akp + c * akq
            for k in range(3):
                apk, aqk = a[p][k], a[q][k]
                a[p][k] = c * apk - sn * aqk
                a[q][k] = sn * apk + c * aqk
            for k in range(3):
                vkp, vkq = v[k][p], v[k][q]
                v[k][p] = c * vkp - sn * vkq
                v[k][q] = sn * vkp + c * vkq
    values = [a[i][i] for i in range(3)]
    vectors = [tuple(v[k][i] for k in range(3)) for i in range(3)]
    return values, vectors


def polar(f, tol=1e-14, max_iter=100):
    """Return (R, S) with F = R S, det R = +1 and S symmetric.

    2 by 2: closed form. R = rot2(theta) with theta = atan2(f10 - f01, f00 + f11),
    the rotation that maximizes trace(R^T F), and S = R^T F.
    3 by 3: the Newton iteration X <- (X + X^(-T)) / 2 of Higham (1986), with
    the scaling gamma = (|X^(-1)|_F / |X|_F)^(1/2) while the relative change
    is above 1e-2. It stops when the relative change in the Frobenius norm is
    at most tol, or after max_iter steps. The iteration gives the orthogonal
    polar factor U. If det U < 0 (det F < 0), R = U (I - 2 v v^T) for the unit
    eigenvector v of the smallest eigenvalue of U^T F, so that det R = +1.
    If det F > 0, S is symmetric positive definite. If det F < 0, S is
    symmetric with one negative eigenvalue. Raise ValueError for a singular
    3 by 3 F.
    """
    n = len(f)
    if n == 2:
        theta = math.atan2(f[1][0] - f[0][1], f[0][0] + f[1][1])
        r = rot2(theta)
        s = mul(transpose(r), f)
        s01 = 0.5 * (s[0][1] + s[1][0])
        s[0][1] = s[1][0] = s01
        return r, s
    if n != 3:
        raise ValueError("polar supports 2 by 2 and 3 by 3 matrices")
    x = [list(map(float, row)) for row in f]
    change = float("inf")
    for _ in range(max_iter):
        xi = inv(x)
        if change > 1e-2:
            g = math.sqrt(_frob(xi) / _frob(x))
        else:
            g = 1.0
        xit = transpose(xi)
        y = [[0.5 * (g * x[i][j] + xit[i][j] / g) for j in range(3)] for i in range(3)]
        change = _frob([[y[i][j] - x[i][j] for j in range(3)] for i in range(3)]) / _frob(y)
        x = y
        if change <= tol:
            break
    u = x
    s = mul(transpose(u), f)
    s = [[0.5 * (s[i][j] + s[j][i]) for j in range(3)] for i in range(3)]
    if det(u) < 0.0:
        values, vectors = _sym_eig3(s)
        k = min(range(3), key=lambda i: values[i])
        v = vectors[k]
        h = [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] for j in range(3)] for i in range(3)]
        u = mul(u, h)
        s = mul(h, s)
        s = [[0.5 * (s[i][j] + s[j][i]) for j in range(3)] for i in range(3)]
    return u, s


# ---------------------------------------------------------------- quaternions


def q_mul(p, q):
    """Return the Hamilton product p q."""
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    )


def q_conj(q):
    """Return the conjugate (w, -x, -y, -z)."""
    return (q[0], -q[1], -q[2], -q[3])


def q_dot(p, q):
    """Return the dot product of p and q as vectors of R^4."""
    return p[0] * q[0] + p[1] * q[1] + p[2] * q[2] + p[3] * q[3]


def q_normalize(q):
    """Return q / |q|."""
    n = math.sqrt(q_dot(q, q))
    if n == 0.0:
        raise ValueError("cannot normalize the zero quaternion")
    return (q[0] / n, q[1] / n, q[2] / n, q[3] / n)


def q_from_axis_angle(axis, angle):
    """Return the unit quaternion of the rotation by angle about axis (any length)."""
    u = normalize(axis)
    s = math.sin(0.5 * angle)
    return (math.cos(0.5 * angle), s * u[0], s * u[1], s * u[2])


def q_to_mat3(q):
    """Return the 3 by 3 rotation matrix of a unit quaternion."""
    w, x, y, z = q
    return [
        [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
    ]


def q_rotate(q, v):
    """Return the vector part of q (0, v) q* for a unit quaternion q."""
    r = q_mul(q_mul(q, (0.0, v[0], v[1], v[2])), q_conj(q))
    return (r[1], r[2], r[3])


def q_log(q):
    """Return the log of a nonzero quaternion as a 4-tuple (ln|q|, phi u).

    For a unit quaternion (cos phi, sin phi u) this is (0, phi u), with
    phi = atan2(|v|, w) in [0, pi]. For a real q the vector part is zero.
    """
    n = math.sqrt(q_dot(q, q))
    if n == 0.0:
        raise ValueError("log of the zero quaternion")
    vn = math.sqrt(q[1] * q[1] + q[2] * q[2] + q[3] * q[3])
    lw = math.log(n)
    if vn == 0.0:
        return (lw, 0.0, 0.0, 0.0)
    phi = math.atan2(vn, q[0])
    f = phi / vn
    return (lw, f * q[1], f * q[2], f * q[3])


def q_exp(q):
    """Return exp(q) = e^w (cos|v|, sin|v| v / |v|) for q = (w, v)."""
    vn = math.sqrt(q[1] * q[1] + q[2] * q[2] + q[3] * q[3])
    ew = math.exp(q[0])
    if vn == 0.0:
        return (ew, 0.0, 0.0, 0.0)
    f = ew * math.sin(vn) / vn
    return (ew * math.cos(vn), f * q[1], f * q[2], f * q[3])


def slerp(q0, q1, t):
    """Spherical linear interpolation of unit quaternions on the short arc.

    If q0 . q1 < 0, q1 is replaced by -q1 (the same rotation). The angle W
    comes from atan2(|q1 - q0|, |q1 + q0|). Below SLERP_SMALL_ANGLE the
    normalized linear interpolation is returned. See
    robotics/rigid-body-motion/spherical-linear-interpolation.
    """
    if q_dot(q0, q1) < 0.0:
        q1 = (-q1[0], -q1[1], -q1[2], -q1[3])
    a = math.sqrt(sum((y - x) ** 2 for x, y in zip(q0, q1)))
    b = math.sqrt(sum((y + x) ** 2 for x, y in zip(q0, q1)))
    w = 2.0 * math.atan2(a, b)
    if w < SLERP_SMALL_ANGLE:
        return q_normalize(tuple((1 - t) * x + t * y for x, y in zip(q0, q1)))
    s = math.sin(w)
    c0 = math.sin((1 - t) * w) / s
    c1 = math.sin(t * w) / s
    return tuple(c0 * x + c1 * y for x, y in zip(q0, q1))


def q_from_mat3(r):
    """Return the unit quaternion, with w >= 0, of a 3 by 3 rotation matrix.

    Shepperd's method: take the largest of the trace, r00, r11 and r22, and
    divide by the component that it gives. See
    robotics/rigid-body-motion/shepperd-method.
    """
    t = r[0][0] + r[1][1] + r[2][2]
    k = max(range(4), key=lambda i: (t, r[0][0], r[1][1], r[2][2])[i])
    if k == 0:
        w = math.sqrt(1.0 + t) / 2.0
        f = 4.0 * w
        q = (w, (r[2][1] - r[1][2]) / f, (r[0][2] - r[2][0]) / f, (r[1][0] - r[0][1]) / f)
    elif k == 1:
        x = math.sqrt(max(0.0, 1.0 + 2.0 * r[0][0] - t)) / 2.0
        f = 4.0 * x
        q = ((r[2][1] - r[1][2]) / f, x, (r[1][0] + r[0][1]) / f, (r[0][2] + r[2][0]) / f)
    elif k == 2:
        y = math.sqrt(max(0.0, 1.0 + 2.0 * r[1][1] - t)) / 2.0
        f = 4.0 * y
        q = ((r[0][2] - r[2][0]) / f, (r[1][0] + r[0][1]) / f, y, (r[2][1] + r[1][2]) / f)
    else:
        z = math.sqrt(max(0.0, 1.0 + 2.0 * r[2][2] - t)) / 2.0
        f = 4.0 * z
        q = ((r[1][0] - r[0][1]) / f, (r[0][2] + r[2][0]) / f, (r[2][1] + r[1][2]) / f, z)
    if q[0] < 0.0:
        q = (-q[0], -q[1], -q[2], -q[3])
    return q


# ---------------------------------------------------------------- transforms


def make_T(r, t):
    """Return the homogeneous (d + 1) by (d + 1) matrix [[R, t], [0, 1]] for d = len(t)."""
    d = len(t)
    m = [[float(r[i][j]) for j in range(d)] + [float(t[i])] for i in range(d)]
    m.append([0.0] * d + [1.0])
    return m


def T_mul(a, b):
    """Return the product a b of two homogeneous transforms."""
    return mul(a, b)


def T_inv(m):
    """Return the inverse of an affine homogeneous transform [[A, t], [0, 1]].

    The result is [[A^(-1), -A^(-1) t], [0, 1]]; A may hold a scale.
    """
    d = len(m) - 1
    a = [row[:d] for row in m[:d]]
    t = [m[i][d] for i in range(d)]
    ai = inv(a)
    ti = matvec(ai, t)
    return make_T(ai, tuple(-x for x in ti))


def T_apply(m, p):
    """Apply a homogeneous transform to a point p and return a tuple."""
    d = len(m) - 1
    return tuple(sum(m[i][j] * p[j] for j in range(d)) + m[i][d] for i in range(d))


# ---------------------------------------------------------------- derivatives


def num_grad(f, x, h=1e-6):
    """Return the gradient of a scalar f at x by central differences of step h."""
    x = list(x)
    g = []
    for i in range(len(x)):
        xi = x[i]
        x[i] = xi + h
        fp = f(x)
        x[i] = xi - h
        fm = f(x)
        x[i] = xi
        g.append((fp - fm) / (2.0 * h))
    return g
