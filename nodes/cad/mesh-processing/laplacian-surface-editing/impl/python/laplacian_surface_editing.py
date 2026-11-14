# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-surface-editing/. The authors are listed in prov/44KQTR.jsonl.

"""Laplacian surface editing (Sorkine, Cohen-Or, Lipman, Alexa, Roessl and Seidel, SGP 2004).

The Laplacian coordinates of the rest mesh are delta_i = p_i - (1/d_i) sum_j p_j,
with the uniform Laplacian and d_i the degree of vertex i. The edited positions q
minimize

    E(q) = sum_i |L(q)_i - T_i(q) delta_i|^2 + lam^2 sum_{k in H} |q_k - h_k|^2,

where H is the set of handles with targets h_k. Without rotations T_i = I, and
the three coordinates are solved apart with one matrix. With rotations,
T_i(q) = s_i I + [h_i]_x is the linearized similarity that best maps the rest
ring of vertex i (i and its neighbours) to the new ring. Its coefficients are
linear in q, so E stays a quadratic and one linear solve gives q.

The solve uses the normal equations. On Fraction input it is exact
(Gaussian elimination); on float input it uses a Cholesky factorization.
"""

from fractions import Fraction

from mx1mesh import cholesky, cholesky_solve, neighbours, solve_dense


def is_exact(points):
    return all(isinstance(x, (int, Fraction)) for p in points for x in p)


def laplacian_rows(nb):
    """Row i of the uniform Laplacian as a dict {column: value}: L(q)_i = q_i - (1/d_i) sum_j q_j."""
    rows = []
    for i, ring in enumerate(nb):
        r = {i: Fraction(1)}
        for j in ring:
            r[j] = -Fraction(1, len(ring))
        rows.append(r)
    return rows


def apply_rows(rows, points):
    return [tuple(sum(w * points[j][c] for j, w in r.items()) for c in range(3)) for r in rows]


def cross_rows(v):
    """The 3 x 4 matrix K(v) with K(v) (s, h1, h2, h3) = s v + h x v."""
    x, y, z = v
    return [[x, 0, z, -y], [y, -z, 0, x], [z, y, -x, 0]]


def similarity_rows(points, i, ring):
    """The 4 rows that give (s, h1, h2, h3) of the best map x -> s x + h cross x + t of the rest ring to a new ring.

    Each row is a dict {(vertex, coordinate): coefficient}, so (s, h) is linear in the new positions.
    The fit is the least squares solution of A (s, h, t) = b, where A has 3 rows for each vertex of the ring.
    """
    A, keys = [], []
    for j in [i] + list(ring):
        K = cross_rows(points[j])
        for c in range(3):
            A.append(K[c] + [int(c == 0), int(c == 1), int(c == 2)])
            keys.append((j, c))
    G = [[sum(a[r] * a[s] for a in A) for s in range(7)] for r in range(7)]
    rows = []
    for r in range(4):
        g = solve_dense(G, [int(k == r) for k in range(7)])  # row r of G^-1, as G is symmetric
        rows.append({keys[m]: sum(g[k] * A[m][k] for k in range(7)) for m in range(len(A))})
    return rows


def least_squares_rows(points, faces, handles, weight=1, rotations=False):
    """The rows (dict {column: value}, right sides) of E. Columns are vertices without rotations, 3 i + c with them."""
    nb = neighbours(len(points), faces)
    Lrows = laplacian_rows(nb)
    delta = apply_rows(Lrows, points)  # @line L1
    if not rotations:
        rows = [(r, list(delta[i])) for i, r in enumerate(Lrows)]  # @line L3
        rows += [({k: weight}, [weight * x for x in h]) for k, h in handles.items()]  # @line L4
        return rows
    rows = []
    for i, r in enumerate(Lrows):
        S = similarity_rows(points, i, nb[i])  # @line L2
        K = cross_rows(delta[i])
        for c in range(3):
            row = {3 * j + c: w for j, w in r.items()}
            for t in range(4):
                if K[c][t]:
                    for (j, cc), g in S[t].items():
                        row[3 * j + cc] = row.get(3 * j + cc, 0) - K[c][t] * g
            rows.append((row, [0]))
    for k, h in handles.items():
        for c in range(3):
            rows.append(({3 * k + c: weight}, [weight * h[c]]))
    return rows


def columns(q, rotations):
    """The unknowns as columns: one list for each coordinate without rotations, one flat list with them."""
    if rotations:
        return [[x for p in q for x in p]]
    return [[p[c] for p in q] for c in range(3)]


def energy(points, faces, q, handles, weight=1, rotations=False):
    total = 0
    cols = columns(q, rotations)
    for row, rhs in least_squares_rows(points, faces, handles, weight, rotations):
        for x, r in zip(cols, rhs):
            total += (sum(v * x[j] for j, v in row.items()) - r) ** 2
    return total


def laplacian_edit(points, faces, handles, weight=1, rotations=False):
    """The positions q that keep the Laplacian coordinates of points while the handles go to their targets."""
    n = len(points)
    exact = is_exact(points) and is_exact(handles.values())
    rows = least_squares_rows(points, faces, handles, weight, rotations)
    size = 3 * n if rotations else n
    N = [[0] * size for _ in range(size)]
    b = [[0] * size for _ in rows[0][1]]
    for row, rhs in rows:
        items = list(row.items())
        for a, x in items:
            for c, y in items:
                N[a][c] += x * y
            for k, r in enumerate(rhs):
                b[k][a] += x * r  # @line L5
    if exact:
        x = [solve_dense(N, bk) for bk in b]  # @line L6
    else:
        L = cholesky(N)  # raises ValueError when N is not positive definite
        x = [cholesky_solve(L, bk) for bk in b]
    if rotations:
        return [(x[0][3 * i], x[0][3 * i + 1], x[0][3 * i + 2]) for i in range(n)]
    return [(x[0][i], x[1][i], x[2][i]) for i in range(n)]  # @line L7
