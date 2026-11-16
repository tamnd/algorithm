# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-of-gaussians-detector/. The authors are listed in prov/832KGB.jsonl.

import math
import random

from difference_of_gaussians_detector import (
    blur,
    dog_keypoints,
    find_extrema,
    gaussian_kernel,
    octave_stack,
    passes_edge_test,
    refine,
)


def blob(n, cx, cy, sb, amp=1.0):
    return [[amp * math.exp(-((u - cx) ** 2 + (v - cy) ** 2) / (2 * sb * sb)) for u in range(n)] for v in range(n)]


def direct_blur(img, sigma):
    """2D convolution with the outer product of the kernel, clamp border."""
    k = gaussian_kernel(sigma)
    r = len(k) // 2
    h, w = len(img), len(img[0])
    out = []
    for v in range(h):
        row = []
        for u in range(w):
            acc = 0.0
            for j in range(-r, r + 1):
                for i in range(-r, r + 1):
                    acc += k[i + r] * k[j + r] * img[min(max(v + j, 0), h - 1)][min(max(u + i, 0), w - 1)]
            row.append(acc)
        out.append(row)
    return out


def oracle_extrema(dog):
    out = []
    levels, h, w = len(dog), len(dog[0]), len(dog[0][0])
    for i in range(1, levels - 1):
        for v in range(1, h - 1):
            for u in range(1, w - 1):
                x = dog[i][v][u]
                nb = [dog[i + a][v + b][u + c] for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)
                      if (a, b, c) != (0, 0, 0)]
                if all(y < x for y in nb) or all(y > x for y in nb):
                    out.append((i, u, v))
    return out


def test_kernel_is_normalized_and_symmetric():
    for sigma in (0.5, 1.0, 1.6, 2.7):
        k = gaussian_kernel(sigma)
        assert abs(sum(k) - 1) < 1e-12
        assert k == k[::-1]
        assert len(k) == 2 * math.ceil(3 * sigma) + 1


def test_separable_blur_matches_direct_convolution():
    rng = random.Random(4)
    for _ in range(15):
        w, h = rng.randint(3, 8), rng.randint(3, 8)
        img = [[rng.random() for _ in range(w)] for _ in range(h)]
        for sigma in (0.7, 1.3):
            a, b = blur(img, sigma), direct_blur(img, sigma)
            assert all(abs(x - y) < 1e-12 for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_extrema_against_oracle():
    rng = random.Random(2004)
    for _ in range(600):
        levels, h, w = rng.randint(3, 5), rng.randint(3, 6), rng.randint(3, 6)
        dog = [[[rng.randint(-3, 3) for _ in range(w)] for _ in range(h)] for _ in range(levels)]
        assert sorted(find_extrema(dog)) == sorted(oracle_extrema(dog))


def test_refine_recovers_the_vertex_of_a_quadratic():
    rng = random.Random(9)
    for _ in range(50):
        u0, v0, i0 = rng.uniform(3.6, 5.4), rng.uniform(3.6, 5.4), rng.uniform(1.6, 2.4)
        c = rng.uniform(0.1, 1)

        def q(u, v, i):
            du, dv, di = u - u0, v - v0, i - i0
            return c - (2 * du * du + 3 * dv * dv + di * di + du * dv + 0.5 * du * di)

        dog = [[[q(u, v, i) for u in range(9)] for v in range(9)] for i in range(5)]
        # The vertex can be more than 0.5 away from (4, 4, 2), so the fit may have to move.
        fit = refine(dog, 2, 4, 4, 5)
        assert fit is not None
        x, y, s, value, _ = fit
        assert abs(x - u0) < 1e-9 and abs(y - v0) < 1e-9 and abs(s - i0) < 1e-9
        assert abs(value - c) < 1e-9
        fit2 = refine(dog, 1 if i0 > 2 else 3, 3, 6, 5)
        assert fit2 is not None and abs(fit2[0] - u0) < 1e-9 and abs(fit2[2] - i0) < 1e-9


def test_edge_test():
    assert passes_edge_test(-1.0, -1.0, 0.0)
    assert passes_edge_test(-1.0, -9.0, 0.0)  # ratio 9 < 10
    assert not passes_edge_test(-1.0, -11.0, 0.0)  # ratio 11 > 10
    assert not passes_edge_test(-1.0, 1.0, 0.0)  # saddle
    assert not passes_edge_test(-1.0, -1.0, 1.0)  # det = 0


def test_worked_example_blob():
    img = blob(32, 16, 16, 3.0)
    base = blur(img, math.sqrt(1.6 ** 2 - 0.5 ** 2))
    _, dog = octave_stack(base, 3, 1.6)
    centre = [dog[i][16][16] for i in range(5)]
    assert [round(x, 4) for x in centre] == [-0.0933, -0.1096, -0.1186, -0.1141, -0.0993]
    keys = dog_keypoints(img)
    assert len(keys) == 1
    x, y, sigma, value = keys[0]
    assert abs(x - 16) < 1e-6 and abs(y - 16) < 1e-6
    assert abs(sigma - 2.639) < 1e-3 and abs(value + 0.1188) < 1e-4
    # The DoG between sigma and k sigma peaks at sigma^2 = t0 / k, with t0 the blob variance less 0.5^2.
    assert abs(sigma - math.sqrt((9 - 0.25) / 2 ** (1 / 3))) < 0.01


def test_blob_scale_follows_blob_size_and_polarity():
    for sb in (3.0, 4.0):
        (x, y, sigma, value), = dog_keypoints(blob(32, 16, 16, sb))
        assert abs(sigma - math.sqrt((sb * sb - 0.25) / 2 ** (1 / 3))) < 0.03 * sigma
        assert value < 0
    dark = [[1 - p for p in r] for r in blob(32, 16, 16, 3.0)]
    (x, y, sigma, value), = dog_keypoints(dark)
    assert value > 0 and abs(sigma - 2.639) < 1e-3


def test_small_blob_needs_a_finer_first_level():
    # sigma 1.73 is below the first searched level sigma0 k = 2.02.
    assert dog_keypoints(blob(32, 16, 16, 2.0)) == []


def test_edge_and_flat_and_low_contrast_give_nothing():
    edge = [[1.0 if u >= 16 else 0.0 for u in range(32)] for v in range(32)]
    assert dog_keypoints(edge) == []
    assert dog_keypoints([[0.5] * 20 for _ in range(20)]) == []
    assert dog_keypoints(blob(32, 16, 16, 3.0, 0.2)) == []


def test_offset_does_not_move_keypoints():
    img = blob(32, 15, 17, 3.5, 0.6)
    a = dog_keypoints(img)
    b = dog_keypoints([[p + 0.3 for p in r] for r in img])
    assert len(a) == len(b) == 1
    assert all(abs(p - q) < 1e-9 for p, q in zip(a[0], b[0]))
