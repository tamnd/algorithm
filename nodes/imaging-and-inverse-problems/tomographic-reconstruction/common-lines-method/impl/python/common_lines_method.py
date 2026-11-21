# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/common-lines-method/. The authors are listed in prov/41Z2MF.jsonl.
"""Orientations of projection images from their common lines (angular
reconstitution with a triangle of three images).

Model: image i is P_i(x, y) = int f(R_i (x, y, z)^T) dz for a 3D density f
and a rotation R_i. The columns of R_i are the image axes x, y and the beam
direction, written in the frame of the molecule.

Common lines: for images i and j with different beam directions, the unit
vector q along the cross product of the beam directions lies in both central
planes. In image i it is the direction c_ij = (R_i^T q)[0:2], in image j it is
c_ji = (R_j^T q)[0:2], and R_i [c_ij; 0] = R_j [c_ji; 0] = q. By the slice
theorem the 2D Fourier transforms of the images agree on these lines, and
equivalently the 1D projections of the images onto these directions agree
(both are the 3D Radon transform of f in the direction q). This code finds the
common lines in the sinograms of the images, then the rotations.

The answer is fixed only up to a global rotation and a reflection: the data
of (f, R_i) and of (f(J .), J R_i J) with J = diag(1, 1, -1) are equal. The
code gives the first image of its anchor triple the rotation I and picks the
mirror solution with a positive third coordinate of q_bc.

Images use the shared pixel convention: an n x n image covers [-1, 1]^2,
x_j = -1 + (2 j + 1) / n and y_i = 1 - (2 i + 1) / n.
"""

import math

import imgkit as ik

# ------------------------------------------------------------------ 3x3 algebra


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def transpose(a):
    return [list(r) for r in zip(*a)]


def matvec(a, v):
    return [sum(a[i][k] * v[k] for k in range(3)) for i in range(3)]


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def unit(u):
    r = math.sqrt(dot(u, u))
    if r == 0:
        raise ValueError("zero vector")
    return [a / r for a in u]


def rotation_angle(a, b):
    """The angle of the rotation a^T b, in radians, from ||a - b||_F = 2 sqrt(2) sin(angle / 2)."""
    d = math.sqrt(sum((a[i][k] - b[i][k]) ** 2 for i in range(3) for k in range(3)))
    return 2 * math.asin(min(1.0, d / (2 * math.sqrt(2))))


def rotation_from_axis(axis, angle):
    """Rodrigues' formula."""
    x, y, z = unit(axis)
    c, s = math.cos(angle), math.sin(angle)
    C = 1 - c
    return [[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C]]


def random_rotation(rng):
    """A rotation from a uniformly random unit quaternion."""
    q = [rng.gauss(0, 1) for _ in range(4)]
    w, x, y, z = unit(q)
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]


J = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]]

# ------------------------------------------------------------------ test data


def project_gaussians(blobs, R, n):
    """The n x n image of int f(R (x, y, z)) dz for f = sum of w exp(-|x - c|^2 / (2 s^2)).

    Each blob (w, c, s) projects to a 2D Gaussian with the center (R^T c)[0:2]
    and the weight w s sqrt(2 pi), sampled at the pixel centers.
    """
    xs, ys = ik.pixel_centers(n)
    img = ik.new_image(n, n)
    Rt = transpose(R)
    for w, c, s in blobs:
        m = matvec(Rt, c)
        a = w * s * math.sqrt(2 * math.pi)
        for i, y in enumerate(ys):
            for j, x in enumerate(xs):
                img[i][j] += a * math.exp(-((x - m[0]) ** 2 + (y - m[1]) ** 2) / (2 * s * s))
    return img


def true_common_line(Ri, Rj):
    """(c_ij, c_ji) for the rotations of images i and j."""
    q = unit(cross([r[2] for r in Ri], [r[2] for r in Rj]))
    a, b = matvec(transpose(Ri), q), matvec(transpose(Rj), q)
    return (a[0], a[1]), (b[0], b[1])


# ------------------------------------------------------------------ the method


def sinograms(images, L, nbins):
    """For each image, its line projections at the angles pi l / L, l = 0..L-1."""
    n = len(images[0])
    rows = ik.parallel_beam_matrix(n, [math.pi * l / L for l in range(L)], nbins)
    out = []
    for img in images:
        v = ik.sp_matvec(rows, ik.flatten(img))
        out.append([v[l * nbins:(l + 1) * nbins] for l in range(L)])
    return out


def _line(S, a):
    """Line a of a sinogram for any integer a: the line at angle theta + pi is
    the line at theta read in reverse, because the bins are symmetric."""
    L = len(S)
    v = S[a % L]
    return v if (a // L) % 2 == 0 else v[::-1]


def _dist(u, v):
    return sum((x - y) ** 2 for x, y in zip(u, v))


def _vertex(dm, d0, dp):
    """The offset in [-0.5, 0.5] of the vertex of the parabola through (-1, dm), (0, d0), (1, dp)."""
    curv = dm - 2 * d0 + dp
    if curv <= 0:
        return 0.0
    return max(-0.5, min(0.5, (dm - dp) / (2 * curv)))


def find_common_line(Si, Sj):
    """The best match of a line of Si with a line of Sj, read forward or reversed.

    Returns (c_ij, c_ji, distance): c_ij = omega(alpha), and c_ji = omega(beta)
    or -omega(beta) when the reversed line of Sj matches. The grid angles are
    refined by a parabola through the distances at the two neighbors.
    """
    L = len(Si)
    both = list(Sj) + [v[::-1] for v in Sj]  # line b + L is line b read in reverse
    best = None
    for a, u in enumerate(Si):
        for b, v in enumerate(both):
            d = _dist(u, v)
            if best is None or d < best[0]:
                best = (d, a, b)
    d, a, b = best
    u, v = Si[a], _line(Sj, b)
    da = _vertex(_dist(_line(Si, a - 1), v), d, _dist(_line(Si, a + 1), v))
    db = _vertex(_dist(u, _line(Sj, b - 1)), d, _dist(u, _line(Sj, b + 1)))
    alpha, beta = math.pi * (a + da) / L, math.pi * (b + db) / L
    return (math.cos(alpha), math.sin(alpha)), (math.cos(beta), math.sin(beta)), d


def frame(u, v):
    """The rotation with columns e1 = u/|u|, e2 = the part of v orthogonal to e1, e3 = e1 x e2."""
    e1 = unit(u)
    e2 = unit([b - dot(v, e1) * a for a, b in zip(e1, v)])
    e3 = cross(e1, e2)
    return [[e1[i], e2[i], e3[i]] for i in range(3)]


def _lift(c):
    return [c[0], c[1], 0.0]


def _sin(c, d):
    """|sin| of the angle between two directions of an image."""
    return abs(c[0] * d[1] - c[1] * d[0]) / (math.hypot(*c) * math.hypot(*d))


def _cos(c, d):
    return (c[0] * d[0] + c[1] * d[1]) / (math.hypot(*c) * math.hypot(*d))


def triangle(cab, cac, cba, cbc, cca, ccb):
    """Rotations (I, R_b, R_c) of three images from their six common lines.

    cab is the common line of images a and b seen in image a, and so on.
    Of the two mirror solutions, the one with q_bc[2] > 0 is returned.
    """
    q_ab, q_ac = _lift(cab), _lift(cac)  # @line L5
    cos_b, cos_c = _cos(cba, cbc), _cos(cca, ccb)  # q_bc . q_ab and q_bc . q_ac
    det = q_ab[0] * q_ac[1] - q_ab[1] * q_ac[0]
    if abs(det) < 1e-12:
        raise ValueError("the common lines of image a with images b and c coincide")
    x = (cos_b * q_ac[1] - cos_c * q_ab[1]) / det
    y = (q_ab[0] * cos_c - q_ac[0] * cos_b) / det
    q_bc = [x, y, math.sqrt(max(0.0, 1 - x * x - y * y))]  # @line L6
    Rb = matmul(frame(q_ab, q_bc), transpose(frame(_lift(cba), _lift(cbc))))  # @line L7
    Rc = matmul(frame(q_ac, q_bc), transpose(frame(_lift(cca), _lift(ccb))))
    eye = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    return eye, Rb, Rc


def rotations_from_common_lines(c, N):
    """Rotations R_0..R_{N-1} from the common lines c[(i, j)] = c_ij of all pairs.

    The anchor triple is the one whose worst in-image angle between its two
    common lines is largest; it gets R = I for its first image. Then each
    other image is placed from the two placed images whose common lines with
    it are closest to perpendicular in it.
    """
    best = None
    for a in range(N):  # @line L4
        for b in range(N):
            for d in range(b + 1, N):
                if a in (b, d):
                    continue
                s = min(_sin(c[(a, b)], c[(a, d)]), _sin(c[(b, a)], c[(b, d)]), _sin(c[(d, a)], c[(d, b)]))
                if best is None or s > best[0]:
                    best = (s, a, b, d)
    if best[0] < 1e-9:
        raise ValueError("the beams of every three images lie in one plane")
    _, a, b, d = best
    R = [None] * N
    R[a], R[b], R[d] = triangle(c[(a, b)], c[(a, d)], c[(b, a)], c[(b, d)], c[(d, a)], c[(d, b)])
    while any(r is None for r in R):  # @line L8
        best = None
        placed = [i for i in range(N) if R[i] is not None]
        for k in range(N):
            if R[k] is not None:
                continue
            for u in placed:
                for v in placed:
                    if u < v:
                        s = _sin(c[(k, u)], c[(k, v)])
                        if best is None or s > best[0]:
                            best = (s, k, u, v)
        if best[0] < 1e-9:
            raise ValueError("no two placed images fix the next image")
        _, k, u, v = best
        qu, qv = matvec(R[u], _lift(c[(u, k)])), matvec(R[v], _lift(c[(v, k)]))
        R[k] = matmul(frame(qu, qv), transpose(frame(_lift(c[(k, u)]), _lift(c[(k, v)]))))  # @line L9
    return R


def common_lines_method(images, L=60, nbins=23):
    """Estimate the rotations of N >= 3 projection images, up to a global
    rotation and the reflection J."""
    N = len(images)
    if N < 3:
        raise ValueError("need at least 3 images")
    S = sinograms(images, L, nbins)  # @line L1
    c = {}
    for i in range(N):
        for j in range(i + 1, N):
            cij, cji, _ = find_common_line(S[i], S[j])  # @line L2
            c[(i, j)], c[(j, i)] = cij, cji  # @line L3
    return rotations_from_common_lines(c, N)  # @line L10


def align_error(est, true):
    """The largest angle between est_0^T est_i and true_0^T true_i, for the
    better of the two mirror solutions (as is, or conjugated by J)."""
    e0, t0 = transpose(est[0]), transpose(true[0])
    rel_e = [matmul(e0, R) for R in est]
    rel_t = [matmul(t0, R) for R in true]
    plain = max(rotation_angle(a, b) for a, b in zip(rel_e, rel_t))
    mirrored = max(rotation_angle(a, matmul(J, matmul(b, J))) for a, b in zip(rel_e, rel_t))
    return min(plain, mirrored)
