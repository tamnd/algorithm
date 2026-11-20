# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radial-distribution-function/. The authors are listed in prov/WE4PJK.jsonl.

import itertools
import math
import random

import pytest

from radial_distribution_function import coordination_number, minimum_image_distance, rdf_histogram, simple_cubic


def uniform_gas(rng, n, box):
    return [[rng.uniform(0, box) for _ in range(3)] for _ in range(n)]


def random_hard_spheres(rng, n, box, d):
    """Random sequential addition: insert uniform points, rejecting any closer than d to one already placed."""
    out = []
    while len(out) < n:
        p = [rng.uniform(0, box) for _ in range(3)]
        if all(minimum_image_distance(p, q, box) >= d for q in out):
            out.append(p)
    return out


def test_minimum_image_distance_against_images():
    rng = random.Random(1)
    box = 4.0
    for _ in range(50):
        a = [rng.uniform(0, box) for _ in range(3)]
        b = [rng.uniform(0, box) for _ in range(3)]
        best = min(
            math.dist(a, [b[q] + box * m[q] for q in range(3)])
            for m in itertools.product((-1, 0, 1), repeat=3)
        )
        assert minimum_image_distance(a, b, box) == pytest.approx(best, abs=1e-12)


def test_page_example_simple_cubic():
    # 27 atoms on a simple cubic lattice with a = 1 in a box of side 3, so rho = 1.
    pos = simple_cubic(3, 1.0)
    r, g, h = rdf_histogram([pos], 3.0, 0.125, 12)
    assert h[8] == 27 * 6
    assert h[11] == 27 * 12
    assert sum(h) == 27 * 18
    assert g[8] == pytest.approx(3.3797, abs=1e-4)
    assert g[11] == pytest.approx(3.6946, abs=1e-4)
    assert all(g[k] == 0 for k in range(12) if k not in (8, 11))
    assert r[8] == pytest.approx(1.0625)


def test_coordination_numbers_simple_cubic():
    pos = simple_cubic(4, 1.0)
    dr = 0.05
    nb = 38  # up to 1.9, below the shell at 2 = box / 2
    _, g, _ = rdf_histogram([pos], 4.0, dr, nb)
    assert coordination_number(g, dr, 1.0, 21) == pytest.approx(6)  # up to 1.05
    assert coordination_number(g, dr, 1.0, 30) == pytest.approx(18)  # up to 1.5
    assert coordination_number(g, dr, 1.0, 36) == pytest.approx(26)  # up to 1.8


def test_ideal_gas_is_one_at_large_n():
    rng = random.Random(2)
    box, n = 5.0, 100
    confs = [uniform_gas(rng, n, box) for _ in range(20)]
    r, g, _ = rdf_histogram(confs, box, 0.1, 25)
    tail = [g[k] for k in range(10, 25)]
    for x in tail:
        assert abs(x - 1) < 0.1
    assert abs(sum(tail) / len(tail) - (n - 1) / n) < 0.02


def test_ideal_gas_finite_n_gives_n_minus_one_over_n():
    rng = random.Random(3)
    box, n = 5.0, 5
    confs = [uniform_gas(rng, n, box) for _ in range(4000)]
    _, g, _ = rdf_histogram(confs, box, 0.25, 10)
    mean = sum(g[2:]) / len(g[2:])
    assert abs(mean - 0.8) < 0.03
    assert abs(mean - 1.0) > 0.1


def test_two_atoms_give_one_half():
    rng = random.Random(4)
    box = 2.0
    confs = [uniform_gas(rng, 2, box) for _ in range(20000)]
    _, g, _ = rdf_histogram(confs, box, 0.25, 4)
    mean = sum(g[1:]) / 3
    assert abs(mean - 0.5) < 0.03


def test_hard_spheres_zero_inside_and_one_far_away():
    rng = random.Random(5)
    box, n, d = 6.0, 150, 0.8
    confs = [random_hard_spheres(rng, n, box, d) for _ in range(6)]
    dr = 0.1
    _, g, _ = rdf_histogram(confs, box, dr, 30)
    assert all(g[k] == 0 for k in range(8))  # r < 0.8
    assert max(g[8:12]) > 1.1  # contact peak
    for k in range(22, 30):  # 2.2 <= r < 3.0
        assert abs(g[k] - 1) < 0.1


def test_translation_does_not_change_the_estimate():
    rng = random.Random(6)
    box = 4.0
    pos = uniform_gas(rng, 30, box)
    moved = [[(x + 1.7) % box for x in p] for p in pos]
    _, g1, h1 = rdf_histogram([pos], box, 0.1, 20)
    _, g2, h2 = rdf_histogram([moved], box, 0.1, 20)
    assert h1 == h2


def test_rejects_range_beyond_half_box():
    with pytest.raises(ValueError):
        rdf_histogram([simple_cubic(2, 1.0)], 2.0, 0.25, 5)
