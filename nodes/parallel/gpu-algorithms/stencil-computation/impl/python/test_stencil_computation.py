# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stencil-computation/. The authors are listed in prov/WF3821.jsonl.
import random
from fractions import Fraction

from stencil_computation import (
    halo_loads, jacobi_average, star_offsets, step_direct, step_tiled, steps_temporal,
)

P = 1_000_003


def mixed(vals):
    """An exact integer update with distinct weights, so a misplaced neighbour shows."""
    return sum((k + 2) * v for k, v in enumerate(vals)) % P


def grid(rng, h, w):
    return [[rng.randrange(P) for _ in range(w)] for _ in range(h)]


def test_tiled_matches_direct():
    for seed in range(40):
        rng = random.Random(seed)
        r = rng.choice([1, 2])
        h, w = rng.randrange(1, 30), rng.randrange(1, 30)
        u = grid(rng, h, w)
        ref, _ = step_direct(u, r, mixed)
        for halo in ("star", "box"):
            got, st = step_tiled(u, r, mixed, rng.randrange(1, 9), halo)
            assert got == ref
            assert st["global_stores"] == st["outputs"] == max(0, h - 2 * r) * max(0, w - 2 * r)


def test_halo_load_formula_on_full_tiles():
    for r in (1, 2, 3):
        for t in (1, 4, 8, 16):
            h = w = 2 * r + 3 * t
            u = [[0] * w for _ in range(h)]
            for halo in ("star", "box"):
                _, st = step_tiled(u, r, lambda v: 0, t, halo)
                assert st["blocks"] == 9
                assert st["global_loads"] == 9 * halo_loads(t, r, halo)


def test_load_ratios_of_the_worked_example():
    assert Fraction(halo_loads(16, 1, "box"), 16 * 16) == Fraction(81, 64)
    assert Fraction(halo_loads(16, 1, "star"), 16 * 16) == Fraction(5, 4)
    assert len(star_offsets(1)) == 5 and len(star_offsets(2)) == 9
    _, loads = step_direct([[0] * 18 for _ in range(18)], 1, lambda v: 0)
    assert loads == 5 * 256
    assert halo_loads(8, 1, "star", 3) == 512 + 384
    assert halo_loads(8, 1, "box", 3) == 1000


def test_jacobi_with_fractions():
    u = [[Fraction(0)] * 6 for _ in range(6)]
    u[0] = [Fraction(1)] * 6                       # hot top edge
    for _ in range(3):
        a, _ = step_direct(u, 1, jacobi_average)
        b, _ = step_tiled(u, 1, jacobi_average, 2)
        assert a == b
        u = a
    assert u[1][1] == Fraction(23, 64)            # 1/4, then 5/16, then 23/64


def test_temporal_blocking_matches_repeated_sweeps():
    for seed in range(25):
        rng = random.Random(100 + seed)
        r, s, t = rng.choice([1, 2]), rng.randrange(1, 4), rng.randrange(2, 8)
        h, w = rng.randrange(1, 26), rng.randrange(1, 26)
        u = grid(rng, h, w)
        ref = u
        for _ in range(s):
            ref, _ = step_direct(ref, r, mixed)
        got, loads = steps_temporal(u, r, mixed, t, s)
        assert got == ref
        blocks = (-(-max(0, h - 2 * r) // t)) * (-(-max(0, w - 2 * r) // t))
        assert loads <= blocks * (t + 2 * r * s) ** 2
