# SPDX-License-Identifier: MIT
# Shared helper of the mx1 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small tools for triangle meshes and dense linear algebra, used by the mx1 pages.

Points are tuples of three numbers. Faces are tuples of three vertex indices,
counterclockwise when seen from outside, so that the face normals point out.
Only the standard library is used. The geometric signs (an obtuse angle, the
side of a plane) are decided exactly, with Fraction, from the float input.
The linear solvers work on float input and on Fraction input.
"""

import math
from fractions import Fraction

# ---------------------------------------------------------------- vectors


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(s, a):
    return tuple(s * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    return math.sqrt(dot(a, a))


def unit(a):
    n = norm(a)
    return tuple(x / n for x in a)


def exact(p):
    """The exact rational value of a point with float or Fraction coordinates."""
    return tuple(Fraction(x) for x in p)


def sign(x):
    return (x > 0) - (x < 0)


def dot_sign(a, b, c):
    """The exact sign of (b - a) . (c - a): positive for an acute angle at a, negative for an obtuse one."""
    a, b, c = exact(a), exact(b), exact(c)
    return sign(dot(sub(b, a), sub(c, a)))


def orient3d(a, b, c, d):
    """The exact sign of det(b - a, c - a, d - a): positive when d lies on the side of the plane abc that its normal points to."""
    a, b, c, d = exact(a), exact(b), exact(c), exact(d)
    return sign(dot(cross(sub(b, a), sub(c, a)), sub(d, a)))


# ---------------------------------------------------------------- topology


def edges(faces):
    """The undirected edges as sorted pairs, in sorted order."""
    s = set()
    for f in faces:
        for k in range(3):
            i, j = f[k], f[(k + 1) % 3]
            s.add((min(i, j), max(i, j)))
    return sorted(s)


def neighbours(n, faces):
    nb = [set() for _ in range(n)]
    for f in faces:
        for k in range(3):
            i, j = f[k], f[(k + 1) % 3]
            nb[i].add(j)
            nb[j].add(i)
    return [sorted(s) for s in nb]


def edge_faces(faces):
    """Map each undirected edge to the list of the faces that hold it."""
    m = {}
    for t, f in enumerate(faces):
        for k in range(3):
            i, j = f[k], f[(k + 1) % 3]
            m.setdefault((min(i, j), max(i, j)), []).append(t)
    return m


def face_adjacency(faces):
    """For each face, the sorted list of the faces that share an edge with it."""
    adj = [set() for _ in faces]
    for fs in edge_faces(faces).values():
        for a in fs:
            for b in fs:
                if a != b:
                    adj[a].add(b)
    return [sorted(s) for s in adj]


def boundary_vertices(faces):
    b = set()
    for (i, j), fs in edge_faces(faces).items():
        if len(fs) == 1:
            b.update((i, j))
    return b


def vertex_faces(n, faces):
    vf = [[] for _ in range(n)]
    for t, f in enumerate(faces):
        for i in f:
            vf[i].append(t)
    return vf


# ---------------------------------------------------------------- face geometry


def face_cross(points, f):
    """cross(b - a, c - a): twice the area times the unit normal."""
    a, b, c = (points[i] for i in f)
    return cross(sub(b, a), sub(c, a))


def face_area(points, f):
    return norm(face_cross(points, f)) / 2


def face_normal(points, f):
    return unit(face_cross(points, f))


def centroid(points, f):
    a, b, c = (points[i] for i in f)
    return tuple((x + y + z) / 3 for x, y, z in zip(a, b, c))


def cot_at(a, b, c):
    """The cotangent of the angle at a in the triangle a, b, c."""
    u, v = sub(b, a), sub(c, a)
    return dot(u, v) / norm(cross(u, v))


def cotan_weights(points, faces):
    """w_ij = (cot alpha_ij + cot beta_ij) / 2, with alpha and beta the angles opposite the edge ij."""
    w = {}
    for f in faces:
        for k in range(3):
            i, j, o = f[k], f[(k + 1) % 3], f[(k + 2) % 3]
            e = (min(i, j), max(i, j))
            w[e] = w.get(e, 0.0) + cot_at(points[o], points[i], points[j]) / 2
    return w


def stiffness_rows(n, weights):
    """The cotangent stiffness matrix C = -L as a list of dict rows: C_ij = -w_ij, C_ii = sum of w_ij."""
    C = [dict() for _ in range(n)]
    for (i, j), w in weights.items():
        C[i][j] = C[i].get(j, 0) - w
        C[j][i] = C[j].get(i, 0) - w
        C[i][i] = C[i].get(i, 0) + w
        C[j][j] = C[j].get(j, 0) + w
    return C


def barycentric_area(points, faces):
    A = [0.0] * len(points)
    for f in faces:
        a = face_area(points, f) / 3
        for i in f:
            A[i] += a
    return A


def mixed_area(points, faces):
    """The mixed Voronoi area of Meyer, Desbrun, Schroeder and Barr (2003).

    A triangle with no obtuse angle gives each corner its Voronoi part,
    (|ij|^2 cot k + |ik|^2 cot j) / 8. An obtuse triangle gives half its area
    to the obtuse corner and a quarter to each other corner.
    """
    A = [0.0] * len(points)
    for f in faces:
        P = [points[i] for i in f]
        obtuse = [dot_sign(P[k], P[(k + 1) % 3], P[(k + 2) % 3]) < 0 for k in range(3)]
        area = face_area(points, f)
        for k in range(3):
            i, pj, pk, pi = f[k], P[(k + 1) % 3], P[(k + 2) % 3], P[k]
            if not any(obtuse):
                eij, eik = sub(pj, pi), sub(pk, pi)
                A[i] += (dot(eij, eij) * cot_at(pk, pi, pj) + dot(eik, eik) * cot_at(pj, pi, pk)) / 8
            else:
                A[i] += area / 2 if obtuse[k] else area / 4
    return A


def mean_curvature_normal(points, faces, area="mixed"):
    """K_i = (1 / (2 A_i)) sum_j (cot alpha_ij + cot beta_ij)(x_i - x_j), which is 2 H n_i with outward n_i."""
    A = mixed_area(points, faces) if area == "mixed" else barycentric_area(points, faces)
    w = cotan_weights(points, faces)
    K = [[0.0, 0.0, 0.0] for _ in points]
    for (i, j), wij in w.items():
        d = sub(points[i], points[j])
        for c in range(3):
            K[i][c] += wij * d[c]
            K[j][c] -= wij * d[c]
    return [tuple(x / A[i] for x in K[i]) for i in range(len(points))]


def area_gradient(points, faces):
    """The gradient of the total area with respect to each vertex, summed face by face.

    For a face with corner i and other corners j, k, the gradient at i is
    (cot k (x_i - x_j) + cot j (x_i - x_k)) / 2, where cot j is the cotangent of the angle at j.
    """
    g = [[0.0, 0.0, 0.0] for _ in points]
    for f in faces:
        for k in range(3):
            i, j, l = f[k], f[(k + 1) % 3], f[(k + 2) % 3]
            pi, pj, pl = points[i], points[j], points[l]
            cl, cj = cot_at(pl, pi, pj), cot_at(pj, pi, pl)
            for c in range(3):
                g[i][c] += (cl * (pi[c] - pj[c]) + cj * (pi[c] - pl[c])) / 2
    return [tuple(v) for v in g]


def total_area(points, faces):
    return sum(face_area(points, f) for f in faces)


# ---------------------------------------------------------------- dense linear algebra


def identity(n, one=1):
    return [[one if i == j else 0 * one for j in range(n)] for i in range(n)]


def transpose(A):
    return [list(r) for r in zip(*A)]


def mat_mul(A, B):
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]


def mat_vec(A, x):
    return [sum(a * b for a, b in zip(r, x)) for r in A]


def det3(A):
    return dot(A[0], cross(A[1], A[2]))


def solve_dense(A, b):
    """Solve A x = b by Gaussian elimination with partial pivoting. Exact on Fraction input."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0:
            raise ValueError("singular matrix")
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    x = [0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (M[r][n] - sum(M[r][k] * x[k] for k in range(r + 1, n))) / M[r][r]
    return x


def cholesky(A):
    """The lower triangular L with A = L L^T, for a symmetric positive definite A."""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = A[j][j] - sum(L[j][k] ** 2 for k in range(j))
        if d <= 0:
            raise ValueError("matrix is not positive definite")
        L[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            L[i][j] = (A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
    return L


def cholesky_solve(L, b):
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
    return x


def _rotation(theta):
    """c, s of the Jacobi rotation for the cotangent theta of twice its angle."""
    t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
    c = 1 / math.sqrt(1 + t * t)
    return c, t * c


def jacobi_eigen(A, tol=1e-15, sweeps=100):
    """Eigenvalues (ascending) and unit eigenvectors of a symmetric matrix, by cyclic Jacobi rotations."""
    n = len(A)
    a = [[float(x) for x in r] for r in A]
    v = identity(n, 1.0)
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off <= tol * tol * sum(a[i][i] ** 2 for i in range(n)) or off == 0:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if a[p][q] == 0:
                    continue
                c, s = _rotation((a[q][q] - a[p][p]) / (2 * a[p][q]))
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    order = sorted(range(n), key=lambda k: a[k][k])
    return [a[k][k] for k in order], [[v[i][k] for i in range(n)] for k in order]


def svd3(A, sweeps=60):
    """A = U diag(s) V^T for a 3 x 3 matrix, with s descending and U, V orthogonal (one-sided Jacobi)."""
    U = [[float(x) for x in r] for r in A]
    V = identity(3, 1.0)
    for _ in range(sweeps):
        done = True
        for p, q in ((0, 1), (0, 2), (1, 2)):
            al = sum(U[i][p] ** 2 for i in range(3))
            be = sum(U[i][q] ** 2 for i in range(3))
            ga = sum(U[i][p] * U[i][q] for i in range(3))
            if ga == 0 or abs(ga) <= 1e-15 * math.sqrt(al * be):
                continue
            done = False
            c, s = _rotation((be - al) / (2 * ga))
            for M in (U, V):
                for i in range(3):
                    mp, mq = M[i][p], M[i][q]
                    M[i][p], M[i][q] = c * mp - s * mq, s * mp + c * mq
        if done:
            break
    sig = [math.sqrt(sum(U[i][k] ** 2 for i in range(3))) for k in range(3)]
    order = sorted(range(3), key=lambda k: -sig[k])
    s = [sig[k] for k in order]
    cols = [[U[i][k] for i in range(3)] for k in order]
    vcols = [[V[i][k] for i in range(3)] for k in order]
    tiny = 1e-13 * max(s[0], 1e-300)
    u = [tuple(x / s[k] for x in cols[k]) for k in range(3) if s[k] > tiny]
    while len(u) < 3:  # complete U where A has a null direction
        if not u:
            u.append((1.0, 0.0, 0.0))
        elif len(u) == 1:
            e = min(((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)), key=lambda t: abs(dot(t, u[0])))
            u.append(unit(cross(u[0], e)))
        else:
            u.append(cross(u[0], u[1]))
    Um = [[u[k][i] for k in range(3)] for i in range(3)]
    Vm = [[vcols[k][i] for k in range(3)] for i in range(3)]
    return Um, s, Vm


def best_rotation(S):
    """The rotation R (det 1) that maximizes trace(R S): with S = U diag(s) V^T, R = V diag(1, 1, d) U^T, d = det(V U^T)."""
    U, _, V = svd3(S)
    d = 1.0 if det3(mat_mul(V, transpose(U))) > 0 else -1.0
    return mat_mul(mat_mul(V, [[1.0, 0, 0], [0, 1.0, 0], [0, 0, d]]), transpose(U))


def rotation_matrix(axis, angle):
    """The rotation by angle about the unit vector axis (Rodrigues)."""
    x, y, z = unit(axis)
    c, s = math.cos(angle), math.sin(angle)
    C = 1 - c
    return [[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C]]


# ---------------------------------------------------------------- test meshes


def orient_outward(points, faces):
    """Flip each face of a mesh around the origin so that its normal points away from the origin (exact test)."""
    out = []
    o = (0, 0, 0)
    for f in faces:
        a, b, c = (points[i] for i in f)
        out.append(tuple(f) if orient3d(a, b, c, o) < 0 else (f[0], f[2], f[1]))
    return out


def octahedron():
    p = [(1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]
    f = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
    return p, orient_outward(p, f)


def icosahedron():
    t = (1 + math.sqrt(5)) / 2
    raw = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
           (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    p = [unit(tuple(float(x) for x in q)) for q in raw]
    f = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6),
         (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10),
         (8, 6, 7), (9, 8, 1)]
    return p, orient_outward(p, f)


def icosphere(level, radius=1.0):
    """The icosahedron with each triangle cut into four `level` times, projected to the sphere."""
    p, f = icosahedron()
    p = list(p)
    for _ in range(level):
        mid = {}

        def m(i, j):
            e = (min(i, j), max(i, j))
            if e not in mid:
                mid[e] = len(p)
                p.append(unit(scale(0.5, add(p[i], p[j]))))
            return mid[e]

        nf = []
        for a, b, c in f:
            ab, bc, ca = m(a, b), m(b, c), m(c, a)
            nf += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
        f = nf
    return [scale(radius, q) for q in p], f


def cylinder(radius, height, m, k, twisted=False):
    """An open tube of m vertices around and k + 1 rings, axis z, centred at the origin, normals outward.

    Plain: each rectangle is cut by the same diagonal. Twisted: ring l is turned by l half steps,
    so that each vertex has six neighbours, as in a grid of near-equilateral triangles.
    """
    p = []
    for l in range(k + 1):
        z = height * l / k - height / 2
        for s in range(m):
            th = 2 * math.pi * (s + (l / 2 if twisted else 0)) / m
            p.append((radius * math.cos(th), radius * math.sin(th), z))
    f = []
    for l in range(k):
        for s in range(m):
            a, b = l * m + s, l * m + (s + 1) % m
            c, d = b + m, a + m
            if twisted:  # the ring above is turned half a step forward
                f += [(a, b, d), (b, c, d)]
            else:
                f += [(a, b, c), (a, c, d)]
    return p, f


def box_mesh(size, div):
    """The closed surface of the box [-a/2, a/2] x [-b/2, b/2] x [-c/2, c/2], each side a grid of div cells.

    size = (a, b, c) may hold Fractions, div = (na, nb, nc) are the numbers of cells along each axis.
    Each grid cell is cut into two triangles. The normals point out.
    """
    index, p, f = {}, [], []

    def vid(key):
        if key not in index:
            index[key] = len(p)
            p.append(tuple(size[a] * Fraction(key[a], div[a]) - Fraction(size[a]) / 2 for a in range(3)))
        return index[key]

    for ax in range(3):
        u, w = [a for a in range(3) if a != ax]
        for side in (0, div[ax]):
            out = 1 if side else -1
            eu = [0, 0, 0]
            ew = [0, 0, 0]
            eu[u], ew[w] = 1, 1
            flip = cross(eu, ew)[ax] != out
            for s in range(div[u]):
                for t in range(div[w]):
                    q = []
                    for ds, dt in ((0, 0), (1, 0), (1, 1), (0, 1)):
                        key = [0, 0, 0]
                        key[ax], key[u], key[w] = side, s + ds, t + dt
                        q.append(vid(tuple(key)))
                    tris = [(q[0], q[1], q[2]), (q[0], q[2], q[3])]
                    f += [(a, c, b) if flip else (a, b, c) for a, b, c in tris]
    return p, f


def to_float(points):
    return [tuple(float(x) for x in q) for q in points]
