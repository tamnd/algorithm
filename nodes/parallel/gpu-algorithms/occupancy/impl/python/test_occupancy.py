# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occupancy/.

from fractions import Fraction

from occupancy import CC, brute_force_blocks, limits, occupancy, regs_per_warp, resident_blocks


def test_formula_matches_brute_force():
    for name in ("8.0", "8.6", "9.0"):
        dev = CC[name]
        for threads in (32, 64, 96, 128, 192, 256, 384, 512, 768, 1024):
            for regs in (0, 16, 24, 32, 37, 40, 48, 64, 96, 128, 255):
                for smem in (0, 4096, 16384, 40960, 65536):
                    assert resident_blocks(dev, threads, regs, smem) == \
                        brute_force_blocks(dev, threads, regs, smem)


def test_guide_examples_for_compute_capability_10():
    dev = CC["10.0"]
    assert occupancy(dev, 768, 32, 0) == Fraction(3, 4)
    assert occupancy(dev, 32, 32, 0) == Fraction(1, 2)
    assert limits(dev, 32, 32, 0)["blocks"] == 32
    assert resident_blocks(dev, 256, 32, 100 * 1024) == 2


def test_best_practices_examples_for_compute_capability_7():
    dev = CC["7.0"]
    assert regs_per_warp(37) == 1280
    assert resident_blocks(dev, 128, 37, 0) == 12
    assert occupancy(dev, 128, 37, 0) == Fraction(3, 4)
    assert resident_blocks(dev, 320, 37, 0) == 4
    assert occupancy(dev, 320, 37, 0) == Fraction(5, 8)


def test_page_example_for_compute_capability_8():
    dev = CC["8.0"]
    lim = limits(dev, 256, 40, 40 * 1024)
    assert lim == {"blocks": 32, "threads": 8, "warps": 8, "registers": 6, "shared": 4}
    assert occupancy(dev, 256, 40, 40 * 1024) == Fraction(1, 2)
    assert occupancy(dev, 256, 40, 16 * 1024) == Fraction(3, 4)
    assert occupancy(dev, 256, 32, 16 * 1024) == 1
