# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/supersampling-antialiasing/. The authors are listed in prov/DED02A.jsonl.

import random
from fractions import Fraction as F

from supersampling_antialiasing import inside, supersampling_antialiasing, visible

TRI = ((F(3, 5), F(2, 5)), (F(7, 2), F(1)), (F(1), F(3)), (F(1),))
BLACK = (F(0),)


def clip(poly, keep):
    """Sutherland-Hodgman against one half-plane, given as a signed function."""
    out = []
    for idx in range(len(poly)):
        p, q = poly[idx], poly[(idx + 1) % len(poly)]
        fp, fq = keep(p), keep(q)
        if fp >= 0:
            out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def area(poly):
    s = F(0)
    for idx in range(len(poly)):
        p, q = poly[idx], poly[(idx + 1) % len(poly)]
        s += p[0] * q[1] - q[0] * p[1]
    return abs(s) / 2


def exact_coverage(tri, i, j):
    poly = [tri[0], tri[1], tri[2]]
    for keep in (lambda p: p[0] - i, lambda p: i + 1 - p[0], lambda p: p[1] - j, lambda p: j + 1 - p[1]):
        poly = clip(poly, keep)
        if not poly:
            return F(0)
    return area(poly)


def random_triangle(rng, w, h, den):
    pts = [(F(rng.randint(-den, w * den + den), den), F(rng.randint(-den, h * den + den), den)) for _ in range(3)]
    return (pts[0], pts[1], pts[2], (F(1),))


def test_example() -> None:
    img1 = supersampling_antialiasing([TRI], 4, 3, 1, BLACK)
    img4 = supersampling_antialiasing([TRI], 4, 3, 4, BLACK)
    assert [[c[0] for c in r] for r in img1] == [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0]]
    assert [[c[0] for c in r] for r in img4] == [
        [F(1, 8), F(7, 16), F(1, 4), F(0)],
        [F(1, 4), F(1), F(13, 16), F(1, 16)],
        [F(1, 16), F(5, 8), F(0), F(0)],
    ]
    exact = [[exact_coverage(TRI, i, j) for i in range(4)] for j in range(3)]
    assert exact == [
        [F(369, 1885), F(12, 29), F(6, 29), F(3, 116)],
        [F(3, 13), F(1), F(31, 40), F(1, 10)],
        [F(1, 13), F(3, 5), F(1, 40), F(0)],
    ]
    assert sum(sum(r) for r in exact) == area(TRI[:3]) == F(73, 20)


def test_edges() -> None:
    assert supersampling_antialiasing([], 2, 2, 3, BLACK) == [[BLACK, BLACK], [BLACK, BLACK]]
    big = ((F(-10), F(-10)), (F(10), F(-10)), (F(0), F(10)), (F(1, 2),))
    assert supersampling_antialiasing([big], 1, 1, 2, BLACK) == [[(F(1, 2),)]]
    flat = ((F(0), F(0)), (F(1), F(1)), (F(2), F(2)), (F(1),))
    assert supersampling_antialiasing([flat], 2, 2, 2, BLACK)[0][0] == BLACK
    assert supersampling_antialiasing([TRI], 0, 0, 2, BLACK) == []
    try:
        supersampling_antialiasing([TRI], 1, 1, 0, BLACK)
    except ValueError:
        pass
    else:
        raise AssertionError("k = 0 accepted")


def cell_coverage(tri, i, j, k, a, b):
    """Exact covered fraction of cell (a, b) of the k x k cells of pixel (i, j)."""
    x0, y0 = i + F(a, k), j + F(b, k)
    x1, y1 = x0 + F(1, k), y0 + F(1, k)
    poly = [tri[0], tri[1], tri[2]]
    for keep in (lambda p: p[0] - x0, lambda p: x1 - p[0], lambda p: p[1] - y0, lambda p: y1 - p[1]):
        poly = clip(poly, keep)
        if not poly:
            return F(0)
    return area(poly) * k * k


def test_error_bound_against_exact_area() -> None:
    rng = random.Random(1977)
    for _ in range(500):
        tri = random_triangle(rng, 2, 2, 4)
        k = rng.randint(1, 4)
        img = supersampling_antialiasing([tri], 2, 2, k, BLACK)
        for j in range(2):
            for i in range(2):
                mixed = 0
                for a in range(k):
                    for b in range(k):
                        c = cell_coverage(tri, i, j, k, a, b)
                        centre = (i + F(2 * a + 1, 2 * k), j + F(2 * b + 1, 2 * k))
                        if c == 0:
                            assert not inside(tri, centre)
                        elif c == 1:
                            assert inside(tri, centre)
                        else:
                            mixed += 1
                assert mixed <= 3 * (2 * k - 1)
                err = abs(img[j][i][0] - exact_coverage(tri, i, j))
                assert err <= F(mixed, k * k)


def test_full_and_empty_pixels_are_exact() -> None:
    rng = random.Random(5)
    for _ in range(300):
        tri = random_triangle(rng, 3, 3, 2)
        k = rng.randint(1, 4)
        img = supersampling_antialiasing([tri], 3, 3, k, BLACK)
        for j in range(3):
            for i in range(3):
                ex = exact_coverage(tri, i, j)
                if ex == 1:
                    assert img[j][i][0] == 1
                if ex == 0:
                    # an empty pixel can only get samples that lie on the triangle's boundary
                    assert img[j][i][0] <= F(3 * (2 * k - 1), k * k)


def test_convergence_in_k() -> None:
    tri = ((F(1, 3), F(1, 7)), (F(13, 7), F(2, 5)), (F(3, 5), F(17, 9)), (F(1),))
    for k in (8, 16, 32):
        img = supersampling_antialiasing([tri], 2, 2, k, BLACK)
        for j in range(2):
            for i in range(2):
                assert abs(img[j][i][0] - exact_coverage(tri, i, j)) <= F(3 * (2 * k - 1), k * k)


def brute_sample_count(scene, i, j, k):
    """Count, per triangle index, the ordered-grid samples it wins, by a direct scan."""
    wins = {}
    for a in range(k):
        for b in range(k):
            p = (i + F(2 * a + 1, 2 * k), j + F(2 * b + 1, 2 * k))
            best = None
            for t, tri in enumerate(scene):
                x = [tri[0], tri[1], tri[2]]
                d = (x[1][0] - x[0][0]) * (x[2][1] - x[0][1]) - (x[1][1] - x[0][1]) * (x[2][0] - x[0][0])
                if d == 0:
                    continue
                # barycentric coordinates, all >= 0 means inside
                l1 = ((p[0] - x[0][0]) * (x[2][1] - x[0][1]) - (p[1] - x[0][1]) * (x[2][0] - x[0][0])) / d
                l2 = ((x[1][0] - x[0][0]) * (p[1] - x[0][1]) - (x[1][1] - x[0][1]) * (p[0] - x[0][0])) / d
                if l1 >= 0 and l2 >= 0 and l1 + l2 <= 1:
                    best = t
            wins[best] = wins.get(best, 0) + 1
    return wins


def test_scenes_against_brute_force() -> None:
    rng = random.Random(42)
    for _ in range(200):
        n = rng.randint(1, 3)
        scene = []
        for _ in range(n):
            tri = random_triangle(rng, 2, 2, 3)
            scene.append((tri[0], tri[1], tri[2], (F(rng.randint(0, 4), 4), F(rng.randint(0, 4), 4))))
        k = rng.randint(1, 3)
        bg = (F(0), F(1))
        img = supersampling_antialiasing(scene, 2, 2, k, bg)
        for j in range(2):
            for i in range(2):
                wins = brute_sample_count(scene, i, j, k)
                want = [F(0), F(0)]
                for t, cnt in wins.items():
                    col = bg if t is None else scene[t][3]
                    want = [w + cnt * c for w, c in zip(want, col)]
                assert img[j][i] == tuple(w / (k * k) for w in want)


def test_shading_per_sample() -> None:
    big = ((F(-10), F(-10)), (F(10), F(-10)), (F(0), F(10)), (F(1),))
    img = supersampling_antialiasing([big], 2, 1, 2, BLACK, shade=lambda t, x, y: (x,))
    # the mean of x over the 4 samples of a pixel is its center
    assert img == [[(F(1, 2),), (F(3, 2),)]]


def test_jittered_is_unbiased() -> None:
    tri = ((F(1, 5), F(1, 9)), (F(9, 10), F(3, 10)), (F(1, 3), F(4, 5)), (F(1),))
    ex = exact_coverage(tri, 0, 0)
    k, runs = 3, 400
    rng = random.Random(1996)
    vals = [supersampling_antialiasing([tri], 1, 1, k, BLACK, rng=rng)[0][0][0] for _ in range(runs)]
    mean = sum(vals) / runs
    var_bound = F(3 * (2 * k - 1), 4 * k ** 4)  # three edges, each meets at most 2k - 1 cells
    # the standard error of the mean is at most sqrt(var_bound / runs); allow 5 of them
    assert (mean - ex) ** 2 <= 25 * var_bound / runs
    sample_var = sum((v - mean) ** 2 for v in vals) / (runs - 1)
    assert sample_var <= 2 * var_bound


def test_inside_and_visible() -> None:
    assert inside(TRI, (F(1), F(1)))
    assert inside(TRI, TRI[0])
    assert not inside(TRI, (F(3), F(3)))
    cw = (TRI[0], TRI[2], TRI[1], TRI[3])
    assert inside(cw, (F(1), F(1)))
    other = ((F(0), F(0)), (F(4), F(0)), (F(0), F(4)), (F(0),))
    assert visible([TRI, other], (F(1), F(1))) == 1
    assert visible([other, TRI], (F(1), F(1))) == 1
    assert visible([], (F(1), F(1))) is None
