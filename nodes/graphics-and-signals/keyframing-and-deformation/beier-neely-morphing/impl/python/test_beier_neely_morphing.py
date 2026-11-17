# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beier-neely-morphing/. The authors are listed in prov/QXNMEN.jsonl.
import math
import random

import pytest

from beier_neely_morphing import (
    interpolate_lines,
    morph,
    sample_bilinear,
    warp_image,
    warp_point,
)


def close(p, q, tol):
    return math.hypot(p[0] - q[0], p[1] - q[1]) < tol


def random_point(rng, lo=0.0, hi=20.0):
    return (rng.uniform(lo, hi), rng.uniform(lo, hi))


def random_image(rng, h, w):
    return [[rng.random() for _ in range(w)] for _ in range(h)]


def one_line_reference(x, p, q, p2, q2):
    # Reference: rotate by the angle between the lines, scale along the line by the ratio
    # of the lengths, keep the distance across the line, as a matrix product.
    d, e = (q[0] - p[0], q[1] - p[1]), (q2[0] - p2[0], q2[1] - p2[1])
    ld, le = math.hypot(*d), math.hypot(*e)
    dh = (d[0] / ld, d[1] / ld)
    nh = (-dh[1], dh[0])
    rel = (x[0] - p[0], x[1] - p[1])
    along = (rel[0] * dh[0] + rel[1] * dh[1]) * le / ld
    across = rel[0] * nh[0] + rel[1] * nh[1]
    ang = math.atan2(e[1], e[0]) - math.atan2(d[1], d[0])
    c, s = math.cos(ang), math.sin(ang)
    local = (along * dh[0] + across * nh[0], along * dh[1] + across * nh[1])
    return (p2[0] + c * local[0] - s * local[1], p2[1] + s * local[0] + c * local[1])


def test_one_line_is_rotation_translation_and_stretch_along_the_line(rng=random.Random(1)):
    for _ in range(50):
        p, q, p2, q2 = (random_point(rng) for _ in range(4))
        for _ in range(5):
            x = random_point(rng, -10, 30)
            assert close(warp_point(x, [(p, q)], [(p2, q2)]), one_line_reference(x, p, q, p2, q2), 1e-9)


def test_same_lines_give_the_identity(rng=random.Random(2)):
    lines = [(random_point(rng), random_point(rng)) for _ in range(4)]
    for _ in range(50):
        x = random_point(rng)
        assert close(warp_point(x, lines, lines), x, 1e-10)


def test_common_rigid_motion_is_reproduced(rng=random.Random(3)):
    ang, tx, ty = 0.8, 3.0, -2.0
    c, s = math.cos(ang), math.sin(ang)

    def m(z):
        return (c * z[0] - s * z[1] + tx, s * z[0] + c * z[1] + ty)

    dst = [(random_point(rng), random_point(rng)) for _ in range(5)]
    src = [(m(pp), m(qq)) for pp, qq in dst]
    for _ in range(50):
        x = random_point(rng)
        assert close(warp_point(x, dst, src, a=0.5, b=1.5, p=0.5), m(x), 1e-9)


def test_weights_against_a_direct_sum(rng=random.Random(4)):
    dst = [(random_point(rng), random_point(rng)) for _ in range(3)]
    src = [(random_point(rng), random_point(rng)) for _ in range(3)]
    a, b, p = 0.7, 1.3, 0.6
    for _ in range(30):
        x = random_point(rng)
        num, den = [0.0, 0.0], 0.0
        for (p0, q0), (p1, q1) in zip(dst, src):
            xi = warp_point(x, [(p0, q0)], [(p1, q1)])
            # Distance to the segment by dense sampling of the segment.
            dist = min(math.hypot(x[0] - (p0[0] + k / 4000 * (q0[0] - p0[0])), x[1] - (p0[1] + k / 4000 * (q0[1] - p0[1]))) for k in range(4001))
            w = (math.hypot(q0[0] - p0[0], q0[1] - p0[1]) ** p / (a + dist)) ** b
            num[0] += w * (xi[0] - x[0])
            num[1] += w * (xi[1] - x[1])
            den += w
        ref = (x[0] + num[0] / den, x[1] + num[1] / den)
        assert close(warp_point(x, dst, src, a, b, p), ref, 1e-3)


def test_a_zero_gives_exact_control_on_the_lines(rng=random.Random(5)):
    dst = [(random_point(rng), random_point(rng)) for _ in range(3)]
    src = [(random_point(rng), random_point(rng)) for _ in range(3)]
    for (p0, q0), (p1, q1) in zip(dst, src):
        for f in (0.0, 0.25, 0.6, 1.0):
            x = (p0[0] + f * (q0[0] - p0[0]), p0[1] + f * (q0[1] - p0[1]))
            target = (p1[0] + f * (q1[0] - p1[0]), p1[1] + f * (q1[1] - p1[1]))
            got = warp_point(x, dst, src, a=0.0, b=1.0, p=0.0)
            # x is on the line up to roundoff, so the weight of its line is huge.
            assert close(got, target, 1e-6)


def test_bilinear_sampler(rng=random.Random(6)):
    img = random_image(rng, 5, 7)
    for yy in range(5):
        for xx in range(7):
            assert sample_bilinear(img, xx, yy) == pytest.approx(img[yy][xx], abs=1e-15)
    x, y = 2.25, 3.5
    ref = 0.5 * (0.75 * img[3][2] + 0.25 * img[3][3]) + 0.5 * (0.75 * img[4][2] + 0.25 * img[4][3])
    assert sample_bilinear(img, x, y) == pytest.approx(ref)
    assert sample_bilinear(img, -3.0, 10.0) == pytest.approx(img[4][0])


def test_integer_translation_shifts_the_image(rng=random.Random(7)):
    img = random_image(rng, 10, 12)
    src = [((2.0, 3.0), (8.0, 4.0)), ((1.0, 7.0), (5.0, 9.0))]
    dst = [((pp[0] + 2, pp[1] + 1), (qq[0] + 2, qq[1] + 1)) for pp, qq in src]
    out = warp_image(img, src, dst)
    for yy in range(1, 10):
        for xx in range(2, 12):
            assert out[yy][xx] == pytest.approx(img[yy - 1][xx - 2], abs=1e-9)


def test_morph_ends_are_the_input_images(rng=random.Random(8)):
    img0, img1 = random_image(rng, 9, 11), random_image(rng, 9, 11)
    lines0 = [((2.0, 2.0), (8.0, 3.0)), ((3.0, 7.0), (6.0, 5.0))]
    lines1 = [((1.0, 3.0), (9.0, 2.0)), ((4.0, 8.0), (7.0, 4.0))]
    for t, img in ((0.0, img0), (1.0, img1)):
        out = morph(img0, img1, lines0, lines1, t)
        for r_out, r_img in zip(out, img):
            for u, v in zip(r_out, r_img):
                assert abs(u - v) < 1e-9


def test_morph_of_an_image_with_itself_is_constant(rng=random.Random(9)):
    img = random_image(rng, 8, 8)
    lines = [((1.0, 1.0), (6.0, 2.0)), ((2.0, 6.0), (6.0, 6.0))]
    out = morph(img, img, lines, lines, 0.37)
    for r_out, r_img in zip(out, img):
        for u, v in zip(r_out, r_img):
            assert abs(u - v) < 1e-9


def test_midway_feature_is_between_the_two_positions():
    # A bright column at x = 2 in img0 and at x = 8 in img1, marked by a vertical line in each.
    h, w = 9, 11
    img0 = [[1.0 if xx == 2 else 0.0 for xx in range(w)] for _ in range(h)]
    img1 = [[1.0 if xx == 8 else 0.0 for xx in range(w)] for _ in range(h)]
    lines0 = [((2.0, 0.0), (2.0, 8.0))]
    lines1 = [((8.0, 0.0), (8.0, 8.0))]
    mid = morph(img0, img1, lines0, lines1, 0.5)
    for row in mid:
        assert row[5] == pytest.approx(1.0, abs=1e-9)
        assert max(abs(v) for i, v in enumerate(row) if i != 5) < 1e-9
    # A plain cross-dissolve shows two half-bright ghosts instead.
    dissolve = [[0.5 * u + 0.5 * v for u, v in zip(r0, r1)] for r0, r1 in zip(img0, img1)]
    assert dissolve[0][2] == 0.5 and dissolve[0][8] == 0.5 and dissolve[0][5] == 0.0


def test_interpolate_lines():
    lines = interpolate_lines([((0.0, 0.0), (2.0, 0.0))], [((4.0, 2.0), (4.0, 6.0))], 0.25)
    assert lines[0][0] == pytest.approx((1.0, 0.5))
    assert lines[0][1] == pytest.approx((2.5, 1.5))


def test_bad_input():
    with pytest.raises(ValueError):
        warp_point((0.0, 0.0), [((0.0, 0.0), (0.0, 0.0))], [((0.0, 0.0), (1.0, 0.0))])
    with pytest.raises(ValueError):
        warp_point((0.0, 0.0), [], [])
