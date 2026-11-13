# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-steinberg-dithering/. The authors are listed in prov/DDE4HS.jsonl.

import random
from fractions import Fraction as F

from floyd_steinberg_dithering import WEIGHTS, floyd_steinberg


def random_image(rng, w, h):
    return [[F(rng.randrange(0, 256), 255) for _ in range(w)] for _ in range(h)]


def test_weights_sum_to_one() -> None:
    assert sum(wt for _, _, wt in WEIGHTS) == 1
    assert [wt * 16 for _, _, wt in WEIGHTS] == [7, 3, 5, 1]


def test_error_is_conserved_exactly() -> None:
    rng = random.Random(8)
    for _ in range(60):
        w, h = rng.randrange(1, 12), rng.randrange(1, 12)
        image = random_image(rng, w, h)
        for serpentine in (False, True):
            for levels in ((0, 1), (0, F(1, 3), F(2, 3), 1)):
                out, err, lost = floyd_steinberg(image, levels, serpentine)
                # the input minus the output is exactly the error pushed off the image
                assert sum(map(sum, image)) - sum(map(sum, out)) == lost
                # the lost error is the sum of the shares that leave through the border
                dropped = 0
                for y in range(h):
                    step = -1 if serpentine and y % 2 else 1
                    for x in range(w):
                        for dx, dy, wt in WEIGHTS:
                            nx, ny = x + step * dx, y + dy
                            if not (0 <= nx < w and ny < h):
                                dropped += wt * err[y][x]
                assert dropped == lost


def test_error_per_pixel_is_at_most_half_a_step() -> None:
    rng = random.Random(8)
    for _ in range(60):
        image = random_image(rng, rng.randrange(1, 16), rng.randrange(1, 16))
        for serpentine in (False, True):
            _, err, _ = floyd_steinberg(image, (0, 1), serpentine)
            assert all(-F(1, 2) <= e <= F(1, 2) for row in err for e in row)
            _, err, _ = floyd_steinberg(image, (0, F(1, 3), F(2, 3), 1), serpentine)
            assert all(-F(1, 6) <= e <= F(1, 6) for row in err for e in row)


def test_constant_gray_gives_the_right_count_up_to_the_border() -> None:
    for g in (F(1, 2), F(1, 3), F(1, 4), F(5, 7)):
        for w, h in ((8, 8), (20, 13), (64, 64)):
            for serpentine in (False, True):
                out, _, lost = floyd_steinberg([[g] * w for _ in range(h)], (0, 1), serpentine)
                ones = sum(map(sum, out))
                assert ones == g * w * h - lost
                # only the pixels of the last row and of the two side columns push error off
                assert abs(ones - g * w * h) <= F(w + 2 * h, 2)


def test_example_from_the_page() -> None:
    out, err, lost = floyd_steinberg([[F(1, 2)] * 3 for _ in range(2)])
    assert out == [[1, 0, 1], [0, 1, 0]]
    assert err[0] == [F(-1, 2), F(9, 32), F(-193, 512)]
    assert err[1][0] == F(203, 512)
    assert lost == 0
    out, _, _ = floyd_steinberg([[F(1, 2)] * 8 for _ in range(8)])
    assert out == [[(x + y + 1) % 2 for x in range(8)] for y in range(8)]
    out, _, lost = floyd_steinberg([[F(1, 3)] * 64 for _ in range(64)])
    assert sum(map(sum, out)) == 1359 and lost == F(19, 3)
