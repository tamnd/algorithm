# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-element-assembly/. The authors are listed in prov/AW3E0H.jsonl.

import math
import random
from fractions import Fraction as F

import scimat
from finite_element_assembly import (
    apply_dirichlet,
    assemble,
    boundary_points,
    element_1d,
    errors_1d,
    errors_2d,
    lagrange_basis_1d,
    mesh_1d,
    p1_triangle,
    solve_poisson_1d,
    solve_poisson_2d,
    square_mesh,
    to_dense,
)


# Tests of the shared helper scimat.py.


def test_scimat_solve_fraction_exact() -> None:
    a = [[F(2), F(1), F(1)], [F(4), F(-6), F(0)], [F(-2), F(7), F(2)]]
    b = [F(5), F(-2), F(9)]
    x = scimat.solve(a, b)
    assert x == [F(1), F(1), F(2)]
    assert scimat.matvec(a, x) == b
    assert all(isinstance(v, F) for v in x)


def test_scimat_inv_det() -> None:
    a = [[F(2), F(1), F(1)], [F(4), F(-6), F(0)], [F(-2), F(7), F(2)]]
    assert scimat.det(a) == F(-16)
    assert scimat.matmul(a, scimat.inv(a)) == scimat.eye(3)
    assert scimat.det([[1, 2], [2, 4]]) == 0
    assert scimat.det([[0, 1], [1, 0]]) == -1
    try:
        scimat.solve([[1, 2], [2, 4]], [1, 1])
    except ValueError:
        pass
    else:
        raise AssertionError("singular matrix not detected")


def test_scimat_solve_matrix_rhs_and_pivoting() -> None:
    a = [[0, 1], [1, 0]]
    assert scimat.solve(a, [3, 4]) == [4, 3]
    x = scimat.solve([[F(1), F(2)], [F(3), F(4)]], [[F(1), F(0)], [F(0), F(1)]])
    assert x == [[F(-2), F(1)], [F(3, 2), F(-1, 2)]]


def test_scimat_cholesky_known_factor() -> None:
    low = [[2.0, 0.0, 0.0], [6.0, 1.0, 0.0], [-8.0, 5.0, 3.0]]
    a = scimat.matmul(low, scimat.transpose(low))
    assert a == [[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]]
    got = scimat.cholesky(a)
    for i in range(3):
        for j in range(3):
            assert abs(got[i][j] - low[i][j]) < 1e-12
    x = scimat.cholesky_solve(got, [1.0, 2.0, 3.0])
    r = scimat.sub(scimat.matvec(a, x), [1.0, 2.0, 3.0])
    assert scimat.norm2(r) < 1e-10
    try:
        scimat.cholesky([[1.0, 2.0], [2.0, 1.0]])
    except ValueError:
        pass
    else:
        raise AssertionError("indefinite matrix not detected")


def test_scimat_random_float_solve() -> None:
    rng = random.Random(7)
    for n in range(1, 8):
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i] += n
        x = [rng.uniform(-1, 1) for _ in range(n)]
        b = scimat.matvec(a, x)
        y = scimat.solve(a, b)
        assert scimat.norm2(scimat.sub(x, y)) < 1e-12


def test_scimat_small_ops() -> None:
    assert scimat.zeros(2, 3) == [[0, 0, 0], [0, 0, 0]]
    assert scimat.zeros(2) == [[0, 0], [0, 0]]
    assert scimat.add([1, 2], [3, 4]) == [4, 6]
    assert scimat.sub([[1, 2]], [[3, 5]]) == [[-2, -3]]
    assert scimat.scale(F(1, 2), [[2, 4]]) == [[1, 2]]
    assert scimat.dot([1, 2, 3], [4, 5, 6]) == 32
    assert scimat.outer([1, 2], [3, 4, 5]) == [[3, 4, 5], [6, 8, 10]]
    assert scimat.transpose([[1, 2, 3]]) == [[1], [2], [3]]
    assert scimat.norm2([3, 4]) == 5.0


def test_scimat_error_norms_and_order() -> None:
    e = [F(1, 2), F(-1, 4), F(1, 4)]
    assert scimat.err_l1(e, F(1, 2)) == F(1, 2)
    assert abs(scimat.err_l2(e, F(1, 2)) - math.sqrt(0.1875)) < 1e-15
    assert scimat.err_linf(e) == F(1, 2)
    errors = [3 * (1 / 2**k) ** 2 for k in range(1, 6)]
    orders = scimat.observed_order(errors)
    assert len(orders) == 4
    assert all(abs(p - 2.0) < 1e-12 for p in orders)


# Tests of the assembly.

BOOLE_RULE = [(F(0), F(7, 90)), (F(1, 4), F(32, 90)), (F(1, 2), F(12, 90)), (F(3, 4), F(32, 90)), (F(1), F(7, 90))]


def _pmul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def _pint01(p):
    return sum(c / (n + 1) for n, c in enumerate(p))


def _pder(p):
    return [n * p[n] for n in range(1, len(p))] or [F(0)]


# Lagrange bases on [0, 1] as coefficient lists in s (constant term first).
_P1 = [[F(1), F(-1)], [F(0), F(1)]]
_P2 = [[F(1), F(-3), F(2)], [F(0), F(4), F(-4)], [F(0), F(-1), F(2)]]


def test_element_1d_exact_integrals() -> None:
    for k, basis in ((1, _P1), (2, _P2)):
        for h in (F(1), F(1, 3), F(2, 7)):
            a, m, _ = element_1d(F(5, 11), F(5, 11) + h, k)
            n = k + 1
            for i in range(n):
                for j in range(n):
                    want_a = _pint01(_pmul(_pder(basis[i]), _pder(basis[j]))) / h
                    want_m = _pint01(_pmul(basis[i], basis[j])) * h
                    assert a[i][j] == want_a
                    assert m[i][j] == want_m
    a, m, _ = element_1d(F(0), F(1), 2)
    assert a == scimat.scale(F(1, 3), [[7, -8, 1], [-8, 16, -8], [1, -8, 7]])
    assert m == scimat.scale(F(1, 30), [[4, 2, -1], [2, 16, 2], [-1, 2, 4]])
    a, m, _ = element_1d(F(0), F(1, 4), 1)
    assert a == [[4, -4], [-4, 4]]
    assert m == [[F(1, 12), F(1, 24)], [F(1, 24), F(1, 12)]]


def test_basis_is_nodal() -> None:
    nodes = {1: [F(0), F(1)], 2: [F(0), F(1, 2), F(1)]}
    for k in (1, 2):
        phi, _ = lagrange_basis_1d(k)
        for i in range(k + 1):
            for j in range(k + 1):
                assert phi[i](nodes[k][j]) == (1 if i == j else 0)


def _p1_by_vandermonde(p):
    """Gradients of the P1 basis from the 3 by 3 system phi_i(p_j) = delta_ij."""
    v = [[F(1), F(q[0]), F(q[1])] for q in p]
    c = scimat.inv(v)  # column i holds the coefficients of phi_i
    return [(c[1][i], c[2][i]) for i in range(3)]


def test_reference_triangle_stiffness() -> None:
    a, m, _ = p1_triangle((F(0), F(0)), (F(1), F(0)), (F(0), F(1)))
    assert a == scimat.scale(F(1, 2), [[2, -1, -1], [-1, 1, 0], [-1, 0, 1]])
    # Mass matrix against exact monomial integrals on the reference triangle:
    # the integral of x^a y^b is a! b! / (a + b + 2)!.
    fact = [1, 1, 2, 6, 24]
    phis = [{(0, 0): 1, (1, 0): -1, (0, 1): -1}, {(1, 0): 1}, {(0, 1): 1}]
    for i in range(3):
        for j in range(3):
            total = F(0)
            for (a1, b1), c1 in phis[i].items():
                for (a2, b2), c2 in phis[j].items():
                    aa, bb = a1 + a2, b1 + b2
                    total += c1 * c2 * F(fact[aa] * fact[bb], fact[aa + bb + 2])
            assert m[i][j] == total


def test_triangle_stiffness_random() -> None:
    rng = random.Random(3)
    for _ in range(40):
        p = [(F(rng.randint(-9, 9), 4), F(rng.randint(-9, 9), 4)) for _ in range(3)]
        det = (p[1][0] - p[0][0]) * (p[2][1] - p[0][1]) - (p[2][0] - p[0][0]) * (p[1][1] - p[0][1])
        if det == 0:
            continue
        a, m, _ = p1_triangle(*p)
        grads = _p1_by_vandermonde(p)
        area = abs(det) / 2
        for i in range(3):
            assert sum(a[i]) == 0
            for j in range(3):
                assert a[i][j] == area * (grads[i][0] * grads[j][0] + grads[i][1] * grads[j][1])
        assert sum(sum(r) for r in m) == area


def test_two_triangles_by_hand() -> None:
    pts = [(F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1))]
    tris = [(0, 1, 2), (0, 2, 3)]
    a, _ = assemble(4, [(t, t) for t in tris], lambda t: (p1_triangle(*(pts[v] for v in t))[0], [0, 0, 0]))
    h = F(1, 2)
    assert to_dense(a) == [[1, -h, 0, -h], [-h, 1, -h, 0], [0, -h, 1, -h], [-h, 0, -h, 1]]


def _random_mesh_1d(rng, n):
    x = [F(0)]
    for _ in range(n):
        x.append(x[-1] + F(rng.randint(1, 9), 10))
    return x


def test_assembly_against_brute_force_1d() -> None:
    rng = random.Random(5)
    for _ in range(10):
        x = _random_mesh_1d(rng, rng.randint(1, 8))
        n = len(x)
        cells, _ = mesh_1d(x, 1)
        a, b = assemble(n, cells, lambda d: (element_1d(d[0], d[1], 1)[0], element_1d(d[0], d[1], 1)[1][0]))
        dense = to_dense(a)

        def dhat(i, e):
            # derivative of the global hat function i on element e = [x_e, x_(e+1)]
            h = x[e + 1] - x[e]
            if i == e:
                return -1 / h
            if i == e + 1:
                return 1 / h
            return 0

        for i in range(n):
            for j in range(n):
                want = sum(dhat(i, e) * dhat(j, e) * (x[e + 1] - x[e]) for e in range(n - 1))
                assert dense[i][j] == want
            assert sum(dense[i]) == 0


def test_row_sums_zero_and_symmetry_2d() -> None:
    rng = random.Random(11)

    def shift(i, j):
        return (F(rng.randint(-2, 2), 40), F(rng.randint(-2, 2), 40))

    pts, tris = square_mesh(4, shift)
    a, _ = assemble(len(pts), [(t, t) for t in tris], lambda t: (p1_triangle(*(pts[v] for v in t))[0], [0, 0, 0]))
    dense = to_dense(a)
    assert all(sum(row) == 0 for row in dense)
    assert dense == scimat.transpose(dense)


def test_patch_test_2d_exact() -> None:
    rng = random.Random(13)

    def shift(i, j):
        return (F(rng.randint(-3, 3), 50), F(rng.randint(-3, 3), 50))

    pts, tris = square_mesh(4, shift)
    g = lambda x, y: 1 + 2 * x - 3 * y  # noqa: E731
    u = solve_poisson_2d(pts, tris, boundary_points(4), None, g)
    assert u == [g(*p) for p in pts]


def test_patch_test_1d_p2_exact() -> None:
    rng = random.Random(17)
    x = _random_mesh_1d(rng, 5)
    coords, u = solve_poisson_1d(x, 2, lambda s: -2, x[0] ** 2, x[-1] ** 2, load_rule=BOOLE_RULE)
    assert u == [c * c for c in coords]


def test_hand_example_1d() -> None:
    x = [F(0), F(1, 3), F(2, 3), F(1)]
    # Boundary values are Fractions: an int divided by an int in the solve would give a float.
    _, u = solve_poisson_1d(x, 1, lambda s: 1, F(0), F(0), load_rule=BOOLE_RULE)
    assert u == [0, F(1, 9), F(1, 9), 0]
    assert all(isinstance(v, F) for v in u)
    pts, tris = square_mesh(2)
    u = solve_poisson_2d(pts, tris, boundary_points(2), lambda x, y: 1, lambda x, y: F(0))
    assert u[4] == F(1, 16) and isinstance(u[4], F)


def test_dirichlet_keeps_symmetry_and_solution() -> None:
    rng = random.Random(19)
    x = _random_mesh_1d(rng, 6)
    cells, coords = mesh_1d(x, 2)
    n = len(coords)
    f = lambda s: 1 + s  # noqa: E731

    def element(d):
        a_k, _, b_k = element_1d(d[0], d[1], 2, f, 1, BOOLE_RULE, BOOLE_RULE)
        return a_k, b_k

    a, b = assemble(n, cells, element)
    full = to_dense(a)
    rhs = list(b)
    apply_dirichlet(a, b, {0: F(1), n - 1: F(-2)})
    dense = to_dense(a)
    assert dense == scimat.transpose(dense)
    u = scimat.solve(dense, b)
    assert u[0] == 1 and u[-1] == -2
    # the interior equations of the original system hold
    for i in range(1, n - 1):
        assert sum(full[i][j] * u[j] for j in range(n)) == rhs[i]


def test_rates_1d_p1_p2() -> None:
    pi = math.pi
    u = lambda s: math.sin(pi * s) + s  # noqa: E731
    du = lambda s: pi * math.cos(pi * s) + 1  # noqa: E731
    f = lambda s: pi * pi * math.sin(pi * s)  # noqa: E731
    for k, p0, p1 in ((1, 2, 1), (2, 3, 2)):
        e0, e1 = [], []
        for n in (4, 8, 16, 32):
            x = [i / n for i in range(n + 1)]
            _, uh = solve_poisson_1d(x, k, f, 0.0, 1.0)
            a, b = errors_1d(x, k, uh, u, du)
            e0.append(a)
            e1.append(b)
        assert all(abs(q - p0) < 0.2 for q in scimat.observed_order(e0))
        assert all(abs(q - p1) < 0.2 for q in scimat.observed_order(e1))


def test_rates_2d_p1() -> None:
    pi = math.pi
    u = lambda x, y: math.sin(pi * x) * math.sin(pi * y)  # noqa: E731
    gu = lambda x, y: (pi * math.cos(pi * x) * math.sin(pi * y), pi * math.sin(pi * x) * math.cos(pi * y))  # noqa: E731
    f = lambda x, y: 2 * pi * pi * u(x, y)  # noqa: E731
    e0, e1 = [], []
    for m in (4, 8, 16):
        pts, tris = square_mesh(m)
        pts = [(float(p[0]), float(p[1])) for p in pts]
        uh = solve_poisson_2d(pts, tris, boundary_points(m), f, lambda x, y: 0.0)
        a, b = errors_2d(pts, tris, uh, u, gu)
        e0.append(a)
        e1.append(b)
    assert all(abs(q - 2) < 0.2 for q in scimat.observed_order(e0))
    assert all(abs(q - 1) < 0.2 for q in scimat.observed_order(e1))
