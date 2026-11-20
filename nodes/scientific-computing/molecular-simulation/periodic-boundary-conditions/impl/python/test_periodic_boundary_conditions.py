# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/periodic-boundary-conditions/. The authors are listed in prov/VY641R.jsonl.

import itertools
import math
import random

import pytest

from periodic_boundary_conditions import distance, fcc_lattice, minimum_image, pair_energy, wrap


def lj(r):
    return 4 * (r ** -12 - r ** -6)


def nearest_image_brute(ri, rj, box):
    """The shortest of the 27 vectors ri - (rj + box m) with m in {-1, 0, 1}^3, for positions in the box."""
    best = None
    for m in itertools.product((-1, 0, 1), repeat=3):
        d = [ri[a] - rj[a] - box * m[a] for a in range(3)]
        if best is None or sum(x * x for x in d) < sum(x * x for x in best):
            best = d
    return best


def test_page_example_one_dimension():
    assert minimum_image([1.0], [9.0], 10.0) == [2.0]
    assert minimum_image([9.0], [1.0], 10.0) == [-2.0]
    assert wrap([10.3], 10.0) == pytest.approx([0.3])
    assert wrap([-0.4], 10.0) == pytest.approx([9.6])


def test_wrap_stays_in_box():
    rng = random.Random(1)
    for _ in range(2000):
        r = [rng.uniform(-30.0, 30.0) for _ in range(3)]
        w = wrap(r, 7.0)
        for x, y in zip(r, w):
            assert 0.0 <= y < 7.0
            assert (x - y) / 7.0 == pytest.approx(round((x - y) / 7.0), abs=1e-9)
    assert wrap([-1e-18], 7.0) == [0.0]


def test_minimum_image_against_27_images():
    rng = random.Random(2)
    box = 5.0
    for _ in range(3000):
        ri = [rng.uniform(0, box) for _ in range(3)]
        rj = [rng.uniform(0, box) for _ in range(3)]
        mi = minimum_image(ri, rj, box)
        bf = nearest_image_brute(ri, rj, box)
        assert sum(x * x for x in mi) == pytest.approx(sum(x * x for x in bf), rel=1e-12)
        assert all(abs(x) <= box / 2 + 1e-12 for x in mi)


def test_distance_does_not_depend_on_which_image_is_stored():
    rng = random.Random(3)
    box = 6.0
    for _ in range(500):
        ri = [rng.uniform(0, box) for _ in range(3)]
        rj = [rng.uniform(0, box) for _ in range(3)]
        shifted = [x + box * rng.randint(-3, 3) for x in rj]
        assert distance(ri, shifted, box) == pytest.approx(distance(ri, rj, box), abs=1e-12)


def test_at_most_one_image_within_half_the_box():
    rng = random.Random(4)
    box = 4.0
    for _ in range(500):
        ri = [rng.uniform(0, box) for _ in range(3)]
        rj = [rng.uniform(0, box) for _ in range(3)]
        close = 0
        for m in itertools.product((-2, -1, 0, 1, 2), repeat=3):
            d = math.sqrt(sum((ri[a] - rj[a] - box * m[a]) ** 2 for a in range(3)))
            if d < box / 2:
                close += 1
        assert close <= 1


def test_fcc_box_has_twelve_nearest_neighbors_each():
    a = 1.7
    pos = fcc_lattice(3, a)
    box = 3 * a
    assert len(pos) == 108
    rnn = a / math.sqrt(2)
    for i in range(0, 108, 7):
        near = sum(1 for j in range(108) if j != i and abs(distance(pos[i], pos[j], box) - rnn) < 1e-9)
        assert near == 12


def test_fcc_energy_matches_the_infinite_lattice():
    # rho* = 0.8442 with 108 atoms gives L = 5.0388, just above 2 rc = 5.
    n, rho, rc = 108, 0.8442, 2.5
    box = (n / rho) ** (1 / 3)
    a = box / 3
    pos = fcc_lattice(3, a)
    u_box = pair_energy(pos, box, rc, lj) / n
    # Per atom energy of the infinite lattice with the same truncation, summed directly.
    u_lat = 0.0
    for i, j, k in itertools.product(range(-3, 4), repeat=3):
        for b in [(0, 0, 0), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5)]:
            v = [(i + b[0]) * a, (j + b[1]) * a, (k + b[2]) * a]
            r = math.sqrt(sum(x * x for x in v))
            if 0 < r < rc:
                u_lat += 0.5 * lj(r)
    assert u_box == pytest.approx(u_lat, rel=1e-12)


def test_cutoff_above_half_box_is_rejected():
    with pytest.raises(ValueError):
        pair_energy([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], 4.0, 2.5, lj)
