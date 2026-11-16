# SPDX-License-Identifier: MIT
# Shared helper of the robotics pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small linear algebra, rotations, poses and quaternions for the robotics pages.

Conventions (Lynch and Park, Modern Robotics, 2017):
- A matrix is a list of rows. A vector is a flat list.
- hat3(w) is the skew-symmetric matrix [w], so that [w] x = w x x.
- A twist or screw is a 6-vector (omega, v), angular part first.
  hat6(V) is the 4x4 matrix [[[omega], v], [0, 0]].
- A pose T is the 4x4 matrix [[R, p], [0, 1]].
- so3_exp and so3_log use exponential coordinates w = omega_hat * theta,
  with theta = |w| in [0, pi] for so3_log.
- se3_exp and se3_log use 6-vectors (w, v) = S * theta.
- Quaternions are Hamilton, scalar first: q = (w, x, y, z), with i j = k.
- Angles are in radians.

The helper holds no algorithm of a robotics page except the four maps
so3_exp, so3_log, se3_exp and se3_log. The pages so3-logarithm-map and
se3-exponential-map hold their own complete versions with comments.
"""

import math

# Below this angle, the coefficient functions of the exponential and the
# logarithm are evaluated by their Taylor series. The first omitted term
# of each series is of order theta^6 and is below 3e-16 for theta < 1e-2;
# it also multiplies [w] or [w]^2, which are small. Above the threshold,
# the closed forms such as (1 - cos(theta)) / theta^2 lose at most about
# 1e-16 / theta^2 to cancellation, which [w] or [w]^2 brings to 1e-14.
SERIES_THETA = 1e-2

# Above pi - NEAR_PI, so3_log takes the axis from the symmetric part of R
# (which is (R + I) / 2 at theta = pi) and not from the skew part.
NEAR_PI = 1e-2

# A pivot whose magnitude is at most PIVOT_TOL times the largest entry of
# the matrix makes solve, inv and pinv_right raise ValueError.
PIVOT_TOL = 1e-12


# ---------------------------------------------------------------- matrices


def zeros(n, m):
    """Return the n by m zero matrix."""
    return [[0.0] * m for _ in range(n)]


def eye(n):
    """Return the n by n identity matrix."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def _is_matrix(a):
    return len(a) > 0 and isinstance(a[0], list)


def add(a, b):
    """Return a + b for two vectors or two matrices of the same shape."""
    if _is_matrix(a):
        return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
    return [x + y for x, y in zip(a, b)]


def sub(a, b):
    """Return a - b for two vectors or two matrices of the same shape."""
    if _is_matrix(a):
        return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
    return [x - y for x, y in zip(a, b)]


def scale(a, s):
    """Return s * a for a vector or a matrix a and a number s."""
    if _is_matrix(a):
        return [[s * x for x in row] for row in a]
    return [s * x for x in a]


def transpose(a):
    """Return the transpose of the matrix a."""
    return [list(col) for col in zip(*a)]


def mul(a, b):
    """Return the matrix product a b."""
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a, x):
    """Return the product of the matrix a and the vector x."""
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def dot(x, y):
    """Return the dot product of two vectors."""
    return sum(p * q for p, q in zip(x, y))


def norm(x):
    """Return the Euclidean norm of a vector."""
    return math.sqrt(dot(x, x))


def cross(a, b):
    """Return the cross product a x b of two 3-vectors."""
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def _max_abs(a):
    return max((abs(x) for row in a for x in row), default=0.0)


def solve(a, b):
    """Solve a x = b by Gaussian elimination with partial pivoting.

    a is a square matrix. b is a vector or a matrix with one column per
    right-hand side; the result has the same shape as b. Raise ValueError
    if a pivot is at most PIVOT_TOL times the largest entry of a.
    """
    n = len(a)
    vec = not _is_matrix(b)
    rhs = [[x] for x in b] if vec else [list(row) for row in b]
    m = [list(map(float, row)) + list(map(float, r)) for row, r in zip(a, rhs)]
    k = len(rhs[0]) if rhs else 0
    tol = PIVOT_TOL * _max_abs(a)
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[piv][c]) <= tol or m[piv][c] == 0.0:
            raise ValueError("matrix is singular to working precision")
        m[c], m[piv] = m[piv], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            if f != 0.0:
                row_r, row_c = m[r], m[c]
                for j in range(c, n + k):
                    row_r[j] -= f * row_c[j]
    x = [[0.0] * k for _ in range(n)]
    for r in range(n - 1, -1, -1):
        for j in range(k):
            s = m[r][n + j] - sum(m[r][i] * x[i][j] for i in range(r + 1, n))
            x[r][j] = s / m[r][r]
    return [row[0] for row in x] if vec else x


def inv(a):
    """Return the inverse of the square matrix a (see solve for errors)."""
    return solve(a, eye(len(a)))


def det(a):
    """Return the determinant of the square matrix a by elimination."""
    n = len(a)
    m = [list(map(float, row)) for row in a]
    d = 1.0
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[piv][c] == 0.0:
            return 0.0
        if piv != c:
            m[c], m[piv] = m[piv], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for j in range(c, n):
                m[r][j] -= f * m[c][j]
    return d


def cholesky(a):
    """Return the lower triangular L with a = L L^T.

    a must be symmetric positive definite. Raise ValueError if a diagonal
    entry of the factor is not positive.
    """
    n = len(a)
    low = zeros(n, n)
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite")
                low[i][i] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    return low


def pinv_right(j):
    """Return the right pseudoinverse J^T (J J^T)^(-1) of a J with full row rank."""
    jt = transpose(j)
    return mul(jt, inv(mul(j, jt)))


# ---------------------------------------------------------------- hat and vee


def hat3(w):
    """Return the 3x3 skew-symmetric matrix [w] of a 3-vector w."""
    return [
        [0.0, -w[2], w[1]],
        [w[2], 0.0, -w[0]],
        [-w[1], w[0], 0.0],
    ]


def vee3(m):
    """Return the 3-vector w of a skew-symmetric matrix m = [w]."""
    return [m[2][1], m[0][2], m[1][0]]


def hat6(v):
    """Return the 4x4 matrix [V] = [[[omega], v], [0, 0]] of V = (omega, v)."""
    w = hat3(v[:3])
    return [
        [w[0][0], w[0][1], w[0][2], v[3]],
        [w[1][0], w[1][1], w[1][2], v[4]],
        [w[2][0], w[2][1], w[2][2], v[5]],
        [0.0, 0.0, 0.0, 0.0],
    ]


def vee6(m):
    """Return the 6-vector (omega, v) of a 4x4 matrix [V]."""
    return [m[2][1], m[0][2], m[1][0], m[0][3], m[1][3], m[2][3]]


# ---------------------------------------------------------------- rotations


def rot_x(a):
    """Return the rotation by a radians about the x axis."""
    c, s = math.cos(a), math.sin(a)
    return [[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]]


def rot_y(a):
    """Return the rotation by a radians about the y axis."""
    c, s = math.cos(a), math.sin(a)
    return [[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]]


def rot_z(a):
    """Return the rotation by a radians about the z axis."""
    c, s = math.cos(a), math.sin(a)
    return [[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]


def rpy(roll, pitch, yaw):
    """Return R = Rz(yaw) Ry(pitch) Rx(roll)."""
    return mul(rot_z(yaw), mul(rot_y(pitch), rot_x(roll)))


def so3_exp(w):
    """Return exp([w]) for exponential coordinates w = omega_hat * theta.

    Rodrigues' formula in the form I + A [w] + B [w]^2 with
    A = sin(theta) / theta and B = (1 - cos(theta)) / theta^2.
    """
    t = norm(w)
    if t < SERIES_THETA:
        t2 = t * t
        a = 1.0 - t2 / 6.0 + t2 * t2 / 120.0
        b = 0.5 - t2 / 24.0 + t2 * t2 / 720.0
    else:
        a = math.sin(t) / t
        b = (1.0 - math.cos(t)) / (t * t)
    k = hat3(w)
    k2 = mul(k, k)
    return [[(1.0 if i == j else 0.0) + a * k[i][j] + b * k2[i][j] for j in range(3)] for i in range(3)]


def so3_log(r):
    """Return w = omega_hat * theta with exp([w]) = r and theta in [0, pi].

    theta = atan2(|s|, c), where c = (trace(r) - 1) / 2 = cos(theta) and
    s = vee(r - r^T) / 2 = sin(theta) omega_hat. For theta below
    SERIES_THETA, w = s (1 + theta^2 / 6 + 7 theta^4 / 360). For theta
    above pi - NEAR_PI, the axis comes from the symmetric part
    ((r + r^T) / 2 - c I) / (1 - c) = omega_hat omega_hat^T, and its sign
    from s. At theta = pi both signs are valid; the sign is then chosen so
    that the largest component of the axis is positive.
    """
    c = (r[0][0] + r[1][1] + r[2][2] - 1.0) / 2.0
    c = max(-1.0, min(1.0, c))
    s = [(r[2][1] - r[1][2]) / 2.0, (r[0][2] - r[2][0]) / 2.0, (r[1][0] - r[0][1]) / 2.0]
    sn = norm(s)
    t = math.atan2(sn, c)
    if t < SERIES_THETA:
        t2 = t * t
        f = 1.0 + t2 / 6.0 + 7.0 * t2 * t2 / 360.0
        return [f * x for x in s]
    if t <= math.pi - NEAR_PI:
        return [t / sn * x for x in s]
    b = [[(r[i][j] + r[j][i]) / 2.0 - (c if i == j else 0.0) for j in range(3)] for i in range(3)]
    # b = (1 - c) omega_hat omega_hat^T. Its column k with the largest
    # diagonal entry is (1 - c) omega_k omega_hat, with omega_k^2 >= 1/3.
    k = max(range(3), key=lambda i: b[i][i])
    col = [b[i][k] for i in range(3)]
    axis = [x / norm(col) for x in col]
    if dot(axis, s) < 0.0 or (dot(axis, s) == 0.0 and axis[k] < 0.0):
        axis = [-x for x in axis]
    return [t * x for x in axis]


# ---------------------------------------------------------------- poses


def make_T(r, p):
    """Return the 4x4 pose [[r, p], [0, 1]]."""
    return [
        [r[0][0], r[0][1], r[0][2], p[0]],
        [r[1][0], r[1][1], r[1][2], p[1]],
        [r[2][0], r[2][1], r[2][2], p[2]],
        [0.0, 0.0, 0.0, 1.0],
    ]


def _rp(t):
    return [row[:3] for row in t[:3]], [t[0][3], t[1][3], t[2][3]]


def T_inv(t):
    """Return the inverse [[R^T, -R^T p], [0, 1]] of a pose t."""
    r, p = _rp(t)
    rt = transpose(r)
    return make_T(rt, [-x for x in matvec(rt, p)])


def T_apply(t, x):
    """Return R x + p, the image of the point x under the pose t."""
    r, p = _rp(t)
    return add(matvec(r, x), p)


def se3_exp(xi):
    """Return exp([xi]) for a 6-vector xi = (w, v) = S * theta.

    The rotation is so3_exp(w). The translation is G v with
    G = I + B [w] + C [w]^2, B = (1 - cos(theta)) / theta^2 and
    C = (theta - sin(theta)) / theta^3, theta = |w|. For w = 0 this is a
    translation by v.
    """
    w, v = xi[:3], xi[3:]
    t = norm(w)
    if t < SERIES_THETA:
        t2 = t * t
        b = 0.5 - t2 / 24.0 + t2 * t2 / 720.0
        c = 1.0 / 6.0 - t2 / 120.0 + t2 * t2 / 5040.0
    else:
        b = (1.0 - math.cos(t)) / (t * t)
        c = (t - math.sin(t)) / (t * t * t)
    k = hat3(w)
    k2 = mul(k, k)
    g = [[(1.0 if i == j else 0.0) + b * k[i][j] + c * k2[i][j] for j in range(3)] for i in range(3)]
    return make_T(so3_exp(w), matvec(g, v))


def se3_log(t):
    """Return the 6-vector xi = (w, v) with se3_exp(xi) = t and |w| in [0, pi].

    w = so3_log(R) and v = G^(-1) p with
    G^(-1) = I - [w] / 2 + D [w]^2, D = (1 - (theta / 2) cot(theta / 2)) / theta^2.
    """
    r, p = _rp(t)
    w = so3_log(r)
    th = norm(w)
    if th < SERIES_THETA:
        t2 = th * th
        d = 1.0 / 12.0 + t2 / 720.0 + t2 * t2 / 30240.0
    else:
        half = th / 2.0
        d = (1.0 - half * math.cos(half) / math.sin(half)) / (th * th)
    k = hat3(w)
    k2 = mul(k, k)
    gi = [[(1.0 if i == j else 0.0) - 0.5 * k[i][j] + d * k2[i][j] for j in range(3)] for i in range(3)]
    return w + matvec(gi, p)


def adjoint(t):
    """Return the 6x6 adjoint [[R, 0], [[p] R, R]] of a pose t."""
    r, p = _rp(t)
    pr = mul(hat3(p), r)
    out = zeros(6, 6)
    for i in range(3):
        for j in range(3):
            out[i][j] = r[i][j]
            out[i + 3][j + 3] = r[i][j]
            out[i + 3][j] = pr[i][j]
    return out


# ---------------------------------------------------------------- quaternions


def quat_mul(q, r):
    """Return the Hamilton product q r of quaternions (w, x, y, z)."""
    a1, b1, c1, d1 = q
    a2, b2, c2, d2 = r
    return [
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    ]


def quat_conj(q):
    """Return the conjugate (w, -x, -y, -z)."""
    return [q[0], -q[1], -q[2], -q[3]]


def quat_to_rot(q):
    """Return the rotation matrix of the quaternion q, so that (0, R v) = q (0, v) q*.

    q need not be of unit length; the result is the rotation of q / |q|.
    """
    w, x, y, z = q
    n = w * w + x * x + y * y + z * z
    s = 2.0 / n
    return [
        [1.0 - s * (y * y + z * z), s * (x * y - w * z), s * (x * z + w * y)],
        [s * (x * y + w * z), 1.0 - s * (x * x + z * z), s * (y * z - w * x)],
        [s * (x * z - w * y), s * (y * z + w * x), 1.0 - s * (x * x + y * y)],
    ]


def quat_from_axis_angle(axis, angle):
    """Return (cos(angle / 2), sin(angle / 2) axis / |axis|).

    A zero axis is allowed only with angle 0 (the identity); otherwise
    raise ValueError.
    """
    n = norm(axis)
    if n == 0.0:
        if angle == 0.0:
            return [1.0, 0.0, 0.0, 0.0]
        raise ValueError("zero axis with a nonzero angle")
    s = math.sin(angle / 2.0) / n
    return [math.cos(angle / 2.0), s * axis[0], s * axis[1], s * axis[2]]


# ---------------------------------------------------------------- derivatives


def num_jacobian(f, x, h=1e-6):
    """Return the Jacobian of f at x by central differences with step h.

    f maps a list of n numbers to a list of m numbers; the result is m by n.
    """
    cols = []
    for i in range(len(x)):
        xp = list(x)
        xm = list(x)
        xp[i] += h
        xm[i] -= h
        fp, fm = f(xp), f(xm)
        cols.append([(a - b) / (2.0 * h) for a, b in zip(fp, fm)])
    return transpose(cols)


# ---------------------------------------------------------------- self-test


def self_test():
    """Check the area check values; return True or raise AssertionError."""
    r = so3_exp([2.0 * math.pi / 3.0 / math.sqrt(3.0)] * 3)
    want = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    assert max(abs(r[i][j] - want[i][j]) for i in range(3) for j in range(3)) < 1e-12
    w = so3_log(want)
    assert abs(norm(w) - 2.0943951) < 1e-7
    assert max(abs(x - 2.0 * math.pi / 3.0 / math.sqrt(3.0)) for x in w) < 1e-12
    t = se3_exp([0.0, 0.0, math.pi / 2.0, math.pi / 2.0, 0.0, 0.0])
    want_t = make_T(rot_z(math.pi / 2.0), [1.0, 1.0, 0.0])
    assert max(abs(t[i][j] - want_t[i][j]) for i in range(4) for j in range(4)) < 1e-12
    return True
