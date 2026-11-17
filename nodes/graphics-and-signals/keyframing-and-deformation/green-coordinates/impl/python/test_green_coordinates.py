# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/green-coordinates/. The authors are listed in prov/2QKV5N.jsonl.
import math
import random

from green_coordinates import deform, edge_integrals, green_coordinates, outward_normal

L_SHAPE = [(0.0, 0.0), (2.0, 0.0), (2.0, 1.0), (1.0, 1.0), (1.0, 2.0), (0.0, 2.0)]
SQUARE = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]


def gauss_legendre(m):
    """Nodes and weights on [0, 1], by Newton's method on the Legendre polynomial."""
    xs, ws = [], []
    for k in range(1, m + 1):
        x = math.cos(math.pi * (k - 0.25) / (m + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for j in range(2, m + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            dp = m * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append((1 - x) / 2)
        ws.append(1 / ((1 - x * x) * dp * dp))
    return xs, ws


GX, GW = gauss_legendre(24)


def quad(f, pieces=16):
    total = 0.0
    for p in range(pieces):
        for x, w in zip(GX, GW):
            total += f((p + x) / pieces) * w / pieces
    return total


def inside_points(rng, cage, count):
    from math import isclose

    out = []
    while len(out) < count:
        p = (rng.uniform(0.05, 1.95), rng.uniform(0.05, 1.95))
        if cage is L_SHAPE and p[0] > 0.95 and p[1] > 0.95:
            continue
        if cage is SQUARE and not (0.05 < p[0] < 0.95 and 0.05 < p[1] < 0.95):
            continue
        if not isclose(p[0], 1.0, abs_tol=0.05) or cage is SQUARE:
            out.append(p)
    return out


def test_closed_form_matches_quadrature():
    rng = random.Random(51)
    for eta in inside_points(rng, L_SHAPE, 8):
        for j in range(len(L_SHAPE)):
            a, b = L_SHAPE[j], L_SHAPE[(j + 1) % len(L_SHAPE)]

            def q(t):
                x, y = a[0] + t * (b[0] - a[0]) - eta[0], a[1] + t * (b[1] - a[1]) - eta[1]
                return x * x + y * y

            i0, i1, big_l = edge_integrals(a, b, eta)
            assert abs(i0 - quad(lambda t: 1 / q(t))) < 1e-10
            assert abs(i1 - quad(lambda t: t / q(t))) < 1e-10
            assert abs(big_l - quad(lambda t: math.log(q(t)))) < 1e-10


def test_point_on_line_of_edge():
    # The point (1, 0.5) lies on the line x = 1 of the edge (1, 1) -> (1, 2), below the edge.
    a, b, eta = (1.0, 1.0), (1.0, 2.0), (1.0, 0.5)
    i0, i1, big_l = edge_integrals(a, b, eta)
    want = quad(lambda t: math.log((0.5 + t) ** 2))
    assert abs(big_l - want) < 1e-10


def test_partition_of_unity_and_reproduction():
    rng = random.Random(52)
    for cage in (L_SHAPE, SQUARE):
        for eta in inside_points(rng, cage, 15):
            phi, psi = green_coordinates(eta, cage)
            assert abs(sum(phi) - 1) < 1e-12
            x = sum(p * v[0] for p, v in zip(phi, cage))
            y = sum(p * v[1] for p, v in zip(phi, cage))
            for j in range(len(cage)):
                nx, ny = outward_normal(cage[j], cage[(j + 1) % len(cage)])
                x += psi[j] * nx
                y += psi[j] * ny
            assert abs(x - eta[0]) < 1e-12 and abs(y - eta[1]) < 1e-12


def similarity(p, ang=0.7, sc=1.6, t=(0.3, -1.2)):
    c, s = math.cos(ang), math.sin(ang)
    return (sc * (c * p[0] - s * p[1]) + t[0], sc * (s * p[0] + c * p[1]) + t[1])


def test_similarity_is_reproduced_and_shear_is_not():
    rng = random.Random(53)
    moved = [similarity(v) for v in L_SHAPE]
    for eta in inside_points(rng, L_SHAPE, 10):
        assert math.dist(deform(eta, L_SHAPE, moved), similarity(eta)) < 1e-11
    sheared = [(x + 0.5 * y, y) for x, y in SQUARE]
    eta = (0.5, 0.5)
    f = deform(eta, SQUARE, sheared)
    assert math.dist(f, (0.75, 0.5)) < 1e-12
    eta = (0.25, 0.3)
    f = deform(eta, SQUARE, sheared)
    assert math.dist(f, (eta[0] + 0.5 * eta[1], eta[1])) > 1e-3


def cauchy(eta, cage, new_cage):
    """Return (1 / 2 pi i) times the integral over the old cage of g(xi) / (xi - eta).

    Here g is the piecewise linear boundary image: g(a + t (b - a)) = a' + t (b' - a').
    """
    z = complex(*eta)
    total = 0j
    n = len(cage)
    for j in range(n):
        a, b = complex(*cage[j]), complex(*cage[(j + 1) % n])
        a2, b2 = complex(*new_cage[j]), complex(*new_cage[(j + 1) % n])
        total += quad(lambda t: ((a2 + t * (b2 - a2)) / (a + t * (b - a) - z)).real) * (b - a)
        total += 1j * quad(lambda t: ((a2 + t * (b2 - a2)) / (a + t * (b - a) - z)).imag) * (b - a)
    return total / (2j * math.pi)


def test_equals_cauchy_integral_of_boundary_image():
    rng = random.Random(54)
    moved = [(x + rng.uniform(-0.3, 0.3), y + rng.uniform(-0.3, 0.3)) for x, y in L_SHAPE]
    for eta in inside_points(rng, L_SHAPE, 6):
        f = deform(eta, L_SHAPE, moved)
        g = cauchy(eta, L_SHAPE, moved)
        assert abs(complex(*f) - g) < 1e-9


def test_cauchy_riemann_so_the_map_is_conformal():
    rng = random.Random(55)
    moved = [(x + rng.uniform(-0.3, 0.3), y + rng.uniform(-0.3, 0.3)) for x, y in L_SHAPE]
    h = 1e-5
    for eta in inside_points(rng, L_SHAPE, 6):
        fx1 = deform((eta[0] + h, eta[1]), L_SHAPE, moved)
        fx0 = deform((eta[0] - h, eta[1]), L_SHAPE, moved)
        fy1 = deform((eta[0], eta[1] + h), L_SHAPE, moved)
        fy0 = deform((eta[0], eta[1] - h), L_SHAPE, moved)
        ux, vx = (fx1[0] - fx0[0]) / (2 * h), (fx1[1] - fx0[1]) / (2 * h)
        uy, vy = (fy1[0] - fy0[0]) / (2 * h), (fy1[1] - fy0[1]) / (2 * h)
        assert abs(ux - vy) < 1e-7
        assert abs(uy + vx) < 1e-7


def test_worked_example():
    # The center of the unit square. By symmetry each phi_i is 1/4.
    phi, psi = green_coordinates((0.5, 0.5), SQUARE)
    assert all(abs(p - 0.25) < 1e-12 for p in phi)
    want = -(1 / (4 * math.pi)) * quad(lambda t: math.log((t - 0.5) ** 2 + 0.25))
    assert all(abs(p - want) < 1e-12 for p in psi)
    assert abs(psi[0] - 0.0893138431) < 1e-9
    # A shear of the cage is not reproduced inside.
    sheared = [(x + 0.5 * y, y) for x, y in SQUARE]
    f = deform((0.25, 0.3), SQUARE, sheared)
    assert abs(f[0] - 0.4468487) < 1e-6 and abs(f[1] - 0.3609747) < 1e-6
