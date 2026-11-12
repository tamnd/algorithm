# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossy-image-compression/. The authors are listed in prov/DWVCRA.jsonl.

import math
import random

from lossy_image_compression import (
    clamp8,
    gaussian_window,
    mse,
    psnr,
    rgb_to_ycbcr,
    ssim,
    ssim_window,
    subsample_420,
    upsample_420,
    ycbcr_to_rgb,
)


def make_image() -> list:
    """A 32 x 32 test image: a gradient plus a checkerboard of 4 x 4 squares."""
    return [[min(255, 40 + 4 * i + 2 * j + (30 if (i // 4 + j // 4) % 2 else 0)) for j in range(32)] for i in range(32)]


def test_psnr_example() -> None:
    x, y = [[52, 55, 61, 66]], [[54, 55, 60, 70]]
    assert mse(x, y) == 5.25
    assert abs(psnr(x, y) - 40.9292) < 1e-4
    assert psnr(x, x) == math.inf


def test_ssim_example_one_window() -> None:
    x, y = [52, 55, 61, 66], [54, 55, 60, 70]
    s = ssim_window(x, y, [0.25] * 4)
    # means 58.5 and 59.75, variances 29.25 and 40.1875, covariance 32.875
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    lum = (2 * 58.5 * 59.75 + c1) / (58.5 ** 2 + 59.75 ** 2 + c1)
    cs = (2 * 32.875 + c2) / (29.25 + 40.1875 + c2)
    assert abs(s - lum * cs) < 1e-12
    assert abs(s - 0.97097) < 1e-5


def test_ssim_basic_properties() -> None:
    img = make_image()
    rng = random.Random(1)
    other = [[v + rng.randint(-20, 20) for v in row] for row in img]
    assert abs(ssim(img, img) - 1) < 1e-12
    assert abs(ssim(img, other) - ssim(other, img)) < 1e-12
    assert -1 <= ssim(img, other) < 1
    w = gaussian_window()
    assert abs(sum(map(sum, w)) - 1) < 1e-12 and w[5][5] == max(map(max, w))


def test_same_psnr_different_ssim() -> None:
    img = make_image()
    shift = [[v + 10 for v in row] for row in img]
    rng = random.Random(7)
    noise = [[v + rng.choice((-10, 10)) for v in row] for row in img]
    assert mse(img, shift) == mse(img, noise) == 100
    assert psnr(img, shift) == psnr(img, noise)
    s_shift, s_noise = ssim(img, shift), ssim(img, noise)
    assert abs(s_shift - 0.99761) < 1e-5 and abs(s_noise - 0.85297) < 1e-5
    # The same ranking with a uniform 8 x 8 window.
    assert ssim(img, shift, 8, 0) > 0.99 > 0.9 > ssim(img, noise, 8, 0)


def test_constant_shift_changes_only_luminance() -> None:
    img = make_image()
    shift = [[v + 10 for v in row] for row in img]
    c1 = (0.01 * 255) ** 2
    w = [v for row in gaussian_window() for v in row]
    total = 0.0
    for i in range(22):
        for j in range(22):
            mx = sum(wi * img[i + k // 11][j + k % 11] for k, wi in enumerate(w))
            my = mx + 10
            total += (2 * mx * my + c1) / (mx * mx + my * my + c1)
    assert abs(ssim(img, shift) - total / 484) < 1e-12


def test_jfif_colour_conversion() -> None:
    assert rgb_to_ycbcr(255, 255, 255) == (255.0, 128.0, 128.0)
    y, cb, cr = rgb_to_ycbcr(0, 0, 0)
    assert (round(y, 9), round(cb, 9), round(cr, 9)) == (0, 128, 128)
    for v in range(0, 256, 17):  # grey has no chroma
        y, cb, cr = rgb_to_ycbcr(v, v, v)
        assert abs(y - v) < 1e-9 and abs(cb - 128) < 1e-9 and abs(cr - 128) < 1e-9
    assert clamp8(rgb_to_ycbcr(255, 0, 0)[2]) == 255  # Cr of pure red is 255.5 before clamping
    worst_real = 0.0
    worst_int = 0
    for r in range(0, 256, 5):
        for g in range(0, 256, 5):
            for b in range(0, 256, 5):
                y, cb, cr = rgb_to_ycbcr(r, g, b)
                back = ycbcr_to_rgb(y, cb, cr)
                worst_real = max(worst_real, max(abs(u - v) for u, v in zip(back, (r, g, b))))
                back = ycbcr_to_rgb(*(clamp8(v) for v in (y, cb, cr)))
                worst_int = max(worst_int, max(abs(clamp8(u) - v) for u, v in zip(back, (r, g, b))))
    # The coefficients are rounded to four or five digits, so the real round trip is not exact.
    assert worst_real < 0.02
    assert worst_int <= 1


def test_chroma_420() -> None:
    plane = [[float(i * 10 + j) for j in range(5)] for i in range(3)]
    sub = subsample_420(plane)
    assert sub == [[5.5, 7.5, 9.0], [20.5, 22.5, 24.0]]  # the last row is repeated
    assert len(upsample_420(sub, 3, 5)) == 3 and len(upsample_420(sub, 3, 5)[0]) == 5
    # 4:2:0 keeps one luma sample per pixel and one Cb and one Cr per 2 x 2 block.
    h = w = 16
    assert h * w + 2 * len(subsample_420([[0] * w] * h)) * len(subsample_420([[0] * w] * h)[0]) == 1.5 * h * w
    # A constant chroma plane survives exactly; a 1-pixel checkerboard is lost.
    flat = [[100.0] * 8 for _ in range(8)]
    assert upsample_420(subsample_420(flat), 8, 8) == flat
    board = [[255.0 * ((i + j) % 2) for j in range(8)] for i in range(8)]
    assert all(v == 127.5 for row in upsample_420(subsample_420(board), 8, 8) for v in row)
