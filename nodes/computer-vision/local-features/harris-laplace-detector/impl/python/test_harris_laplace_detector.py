# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harris-laplace-detector/. The authors are listed in prov/B4GHVB.jsonl.

import math
import random

from harris_laplace_detector import (
    gaussian_kernel,
    harris_laplace,
    harris_measure,
    normalized_laplacian,
    select_points,
)


def rect(n, u0, u1, v0, v1):
    return [[1.0 if u0 <= u <= u1 and v0 <= v <= v1 else 0.0 for u in range(n)] for v in range(n)]


def blob(n, cx, cy, sb):
    return [[math.exp(-((u - cx) ** 2 + (v - cy) ** 2) / (2 * sb * sb)) for u in range(n)] for v in range(n)]


def at(img, u, v):
    h, w = len(img), len(img[0])
    return img[min(max(v, 0), h - 1)][min(max(u, 0), w - 1)]


def direct_blur(img, sigma):
    k = gaussian_kernel(sigma)
    r = len(k) // 2
    h, w = len(img), len(img[0])
    return [[sum(k[i + r] * k[j + r] * at(img, u + i, v + j) for i in range(-r, r + 1) for j in range(-r, r + 1))
             for u in range(w)] for v in range(h)]


def direct_harris(img, si, sd, alpha):
    L = direct_blur(img, sd)
    h, w = len(img), len(img[0])
    lx = [[(at(L, u + 1, v) - at(L, u - 1, v)) / 2 for u in range(w)] for v in range(h)]
    ly = [[(at(L, u, v + 1) - at(L, u, v - 1)) / 2 for u in range(w)] for v in range(h)]
    a = direct_blur([[sd * sd * lx[v][u] ** 2 for u in range(w)] for v in range(h)], si)
    b = direct_blur([[sd * sd * ly[v][u] ** 2 for u in range(w)] for v in range(h)], si)
    c = direct_blur([[sd * sd * lx[v][u] * ly[v][u] for u in range(w)] for v in range(h)], si)
    out = []
    for v in range(h):
        row = []
        for u in range(w):
            # det and trace of [[a, c], [c, b]] written out from the eigenvalues
            tr = a[v][u] + b[v][u]
            disc = math.sqrt(max((a[v][u] - b[v][u]) ** 2 + 4 * c[v][u] ** 2, 0.0))
            l1, l2 = (tr + disc) / 2, (tr - disc) / 2
            row.append(l1 * l2 - alpha * (l1 + l2) ** 2)
        out.append(row)
    return out


def oracle_select(R, F, th, tl):
    out = []
    for n in range(1, len(R) - 1):
        for v in range(1, len(R[0]) - 1):
            for u in range(1, len(R[0][0]) - 1):
                nb = [R[n][v + b][u + a] for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
                if (R[n][v][u] > th and max(nb) < R[n][v][u] and F[n][v][u] > tl
                        and F[n][v][u] > max(F[n - 1][v][u], F[n + 1][v][u])):
                    out.append((n, u, v))
    return out


def test_measures_match_direct_computation():
    rng = random.Random(21)
    for _ in range(4):
        img = [[rng.random() for _ in range(6)] for _ in range(5)]
        for si in (1.0, 1.4):
            a, b = harris_measure(img, si, 0.7 * si, 0.06), direct_harris(img, si, 0.7 * si, 0.06)
            assert all(abs(x - y) < 1e-12 for ra, rb in zip(a, b) for x, y in zip(ra, rb))
            L = direct_blur(img, si)
            f = normalized_laplacian(img, si)
            for v in range(1, 4):
                for u in range(1, 5):
                    lap = L[v][u + 1] + L[v][u - 1] + L[v + 1][u] + L[v - 1][u] - 4 * L[v][u]
                    assert abs(f[v][u] - si * si * abs(lap)) < 1e-12


def test_selection_against_oracle():
    rng = random.Random(2004)
    for _ in range(600):
        k, h, w = rng.randint(3, 5), rng.randint(3, 6), rng.randint(3, 6)
        R = [[[rng.randint(-2, 3) for _ in range(w)] for _ in range(h)] for _ in range(k)]
        F = [[[rng.randint(0, 3) for _ in range(w)] for _ in range(h)] for _ in range(k)]
        th, tl = rng.choice([-5, 0, 1]), rng.choice([-1, 0, 1])
        assert sorted(select_points(R, F, th, tl)) == sorted(oracle_select(R, F, th, tl))


def test_worked_example_square():
    img = rect(28, 10, 18, 10, 18)
    pts = harris_laplace(img)
    assert [(u, v) for u, v, _ in pts] == [(11, 11), (17, 11), (14, 14), (11, 17), (17, 17)]
    assert all(abs(s - 1.4) < 1e-12 for u, v, s in pts if (u, v) != (14, 14))
    assert abs(pts[2][2] - 1.4 ** 4) < 1e-12
    F = [normalized_laplacian(img, 1.4 ** n)[11][11] for n in range(6)]
    assert [round(x, 4) for x in F] == [0.3541, 0.3996, 0.3468, 0.2991, 0.3259, 0.3356]


def test_blob_scale_is_the_level_of_the_blob():
    for n in (1, 2, 3, 4):
        sn = 1.4 ** n
        assert harris_laplace(blob(28, 14, 14, sn)) == [(14, 14, sn)]


def test_sharp_corner_scale_comes_from_the_pixel_grid():
    # A quarter plane has no size of its own; the only scale left is the pixel,
    # so its corner gets the same point and scale as the corner of the square.
    img = [[1.0 if u >= 14 and v >= 14 else 0.0 for u in range(28)] for v in range(28)]
    assert harris_laplace(img) == [(15, 15, 1.4)]
    F = [normalized_laplacian(img, 1.4 ** n)[14][14] for n in range(6)]
    assert all(F[n] > F[n + 1] for n in range(5))


def test_flat_and_offset():
    assert harris_laplace([[0.4] * 12 for _ in range(12)]) == []
    img = rect(28, 10, 18, 10, 18)
    assert harris_laplace([[p + 0.5 for p in r] for r in img]) == harris_laplace(img)


def test_rotation_by_90_degrees_of_the_measures():
    rng = random.Random(5)
    h, w = 7, 8
    img = [[rng.random() for _ in range(w)] for _ in range(h)]
    rot = [[img[h - 1 - j][i] for j in range(h)] for i in range(w)]
    a, b = harris_measure(img, 1.2, 0.84, 0.06), harris_measure(rot, 1.2, 0.84, 0.06)
    fa, fb = normalized_laplacian(img, 1.2), normalized_laplacian(rot, 1.2)
    for v in range(h):
        for u in range(w):
            assert abs(a[v][u] - b[u][h - 1 - v]) < 1e-12
            assert abs(fa[v][u] - fb[u][h - 1 - v]) < 1e-12
