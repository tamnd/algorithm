# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verlet-neighbor-list/. The authors are listed in prov/NKWXRA.jsonl.

import itertools
import random

import pytest

from verlet_neighbor_list import VerletList, minimum_image_dist2


def brute_force_pairs(positions, box, rc):
    """Every pair i < j whose nearest periodic image is closer than rc.

    In a cubic box the 27 images split by coordinate, so the nearest image
    takes the smallest of the shifts -box, 0 and box on each axis.
    """
    out = []
    for i, j in itertools.combinations(range(len(positions)), 2):
        best = 0.0
        for a in range(3):
            d = positions[i][a] - positions[j][a]
            best += min(d * d, (d - box) ** 2, (d + box) ** 2)
        if best < rc * rc:
            out.append((i, j))
    return out


def page_atoms():
    return [[1.0, 0.0, 0.0], [3.95, 0.0, 0.0], [1.0, 3.05, 0.0]]


def test_page_example_build():
    v = VerletList(page_atoms(), 10.0, 2.5, 0.5)
    assert v.neighbors == [(0, 1)]
    assert v.pairs(page_atoms()) == []


def test_page_example_two_atoms_approach():
    v = VerletList(page_atoms(), 10.0, 2.5, 0.5)
    moved = [[1.0, 0.3, 0.0], [3.95, 0.0, 0.0], [1.0, 2.75, 0.0]]
    assert v.displacements(moved) == pytest.approx([0.3, 0.0, 0.3])
    # One atom alone moved less than the skin, but the pair (0, 2) is now at 2.45.
    assert max(v.displacements(moved)) < v.skin
    assert v.needs_rebuild(moved)
    assert v.pairs(moved) == [(0, 2)]
    assert v.builds == 2


def test_page_example_stale_list_would_miss_the_pair():
    v = VerletList(page_atoms(), 10.0, 2.5, 0.5)
    moved = [[1.0, 0.3, 0.0], [3.95, 0.0, 0.0], [1.0, 2.75, 0.0]]
    stale = [p for p in v.neighbors if minimum_image_dist2(moved[p[0]], moved[p[1]], 10.0) < 2.5 ** 2]
    assert stale == []
    assert brute_force_pairs(moved, 10.0, 2.5) == [(0, 2)]


def test_page_example_two_rule_saves_a_rebuild():
    moved = [[1.0, 0.0, 0.0], [3.65, 0.0, 0.0], [1.0, 2.95, 0.0]]
    two = VerletList(page_atoms(), 10.0, 2.5, 0.5, rule="two")
    half = VerletList(page_atoms(), 10.0, 2.5, 0.5, rule="half")
    assert not two.needs_rebuild(moved)
    assert half.needs_rebuild(moved)
    assert two.pairs(moved) == half.pairs(moved) == brute_force_pairs(moved, 10.0, 2.5)


@pytest.mark.parametrize("rule", ["two", "half"])
def test_random_walk_against_brute_force(rule):
    rng = random.Random(11)
    box, rc, skin, n = 7.0, 1.5, 0.4, 60
    pos = [[rng.uniform(0, box) for _ in range(3)] for _ in range(n)]
    v = VerletList(pos, box, rc, skin, rule=rule)
    for _ in range(60):
        for r in pos:
            for a in range(3):
                r[a] = (r[a] + rng.gauss(0.0, 0.02)) % box
        assert v.pairs(pos) == brute_force_pairs(pos, box, rc)
    assert 1 < v.builds < 60


def test_two_rule_rebuilds_no_more_than_half_rule():
    rng = random.Random(12)
    box, rc, skin, n = 7.0, 1.5, 0.4, 80
    start = [[rng.uniform(0, box) for _ in range(3)] for _ in range(n)]
    steps = [[[rng.gauss(0.0, 0.02) for _ in range(3)] for _ in range(n)] for _ in range(150)]
    counts = {}
    for rule in ("two", "half"):
        pos = [list(r) for r in start]
        v = VerletList(pos, box, rc, skin, rule=rule)
        for step in steps:
            for r, dr in zip(pos, step):
                for a in range(3):
                    r[a] = (r[a] + dr[a]) % box
            v.pairs(pos)
        counts[rule] = v.builds
    assert counts["two"] <= counts["half"]


def test_atom_crossing_the_boundary():
    pos = [[9.9, 5.0, 5.0], [2.3, 5.0, 5.0]]
    v = VerletList(pos, 10.0, 2.5, 0.5)
    assert v.neighbors == [(0, 1)]
    pos[0][0] = (9.9 + 0.2) % 10.0
    assert v.displacements(pos)[0] == pytest.approx(0.2)
    assert v.pairs(pos) == [(0, 1)]
    assert v.builds == 1


def test_list_radius_must_fit_the_box():
    with pytest.raises(ValueError):
        VerletList([[0.0, 0.0, 0.0]], 5.0, 2.3, 0.4)
