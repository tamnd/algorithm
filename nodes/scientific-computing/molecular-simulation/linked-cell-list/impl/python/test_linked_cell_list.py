# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linked-cell-list/. The authors are listed in prov/4RS32Z.jsonl.

import itertools
import random

import pytest

from linked_cell_list import CellList, cell_list_pairs, half_shell, minimum_image_dist2


def brute_force_pairs(positions, box, rc):
    """Every pair i < j whose nearest periodic image is closer than rc, found by trying all 3^d images."""
    dim = len(positions[0])
    out = []
    for i, j in itertools.combinations(range(len(positions)), 2):
        best = None
        for k in itertools.product((-1, 0, 1), repeat=dim):
            d2 = sum((positions[i][a] - positions[j][a] - box * k[a]) ** 2 for a in range(dim))
            best = d2 if best is None else min(best, d2)
        if best < rc * rc:
            out.append((i, j))
    return out


def random_box(rng, n, box, dim):
    return [[rng.uniform(0, box) for _ in range(dim)] for _ in range(n)]


def test_half_shell_sizes():
    assert len(half_shell(2)) == 4
    assert len(half_shell(3)) == 13
    for dim in (2, 3):
        shell = set(half_shell(dim))
        for o in shell:
            assert tuple(-v for v in o) not in shell


def test_page_example():
    p = [[0.5, 0.5], [1.6, 1.2], [2.4, 0.6], [7.6, 1.0], [4.5, 4.5], [1.0, 7.2], [5.9, 3.1]]
    cl = CellList(p, 8.0, 2.0)
    assert cl.s == 4
    assert cl.cell_of == [0, 0, 1, 3, 10, 12, 6]
    assert cl.chain(0) == [1, 0]
    found, tests = cl.pairs()
    assert sorted(found) == [(0, 1), (0, 2), (0, 3), (0, 5), (1, 2), (2, 5), (4, 6)]
    assert tests == 12
    assert sorted(found) == brute_force_pairs(p, 8.0, 2.0)


@pytest.mark.parametrize("seed,dim,n,box,rc", [
    (1, 2, 120, 10.0, 1.3),
    (2, 2, 80, 6.0, 2.0),
    (3, 3, 150, 6.0, 1.5),
    (4, 3, 100, 5.0, 1.0),
    (5, 3, 60, 4.5, 1.5),
])
def test_against_brute_force(seed, dim, n, box, rc):
    rng = random.Random(seed)
    p = random_box(rng, n, box, dim)
    found, _ = CellList(p, box, rc).pairs()
    assert len(found) == len(set(found))
    assert sorted(found) == brute_force_pairs(p, box, rc)


def test_positions_outside_the_box_are_wrapped():
    rng = random.Random(6)
    p = random_box(rng, 80, 6.0, 3)
    shifted = [[x + 6.0 * rng.randint(-2, 2) for x in r] for r in p]
    assert cell_list_pairs(shifted, 6.0, 1.5) == cell_list_pairs(p, 6.0, 1.5)


def test_cell_side_not_smaller_than_cutoff():
    for box, rc in [(10.0, 3.0), (10.0, 2.5), (9.99, 3.33)]:
        cl = CellList([[0.0, 0.0, 0.0]], box, rc)
        assert cl.side >= rc


def test_too_few_cells_is_rejected():
    with pytest.raises(ValueError):
        CellList([[0.0, 0.0, 0.0]], 5.0, 2.0)


def test_each_atom_in_exactly_one_chain():
    rng = random.Random(7)
    p = random_box(rng, 200, 8.0, 3)
    cl = CellList(p, 8.0, 2.0)
    seen = []
    for c in range(len(cl.head)):
        for i in cl.chain(c):
            assert cl.cell_of[i] == c
            seen.append(i)
    assert sorted(seen) == list(range(200))


def test_work_per_atom_is_bounded_at_fixed_density():
    # rho = 1 in 3D, rc = 1. Each atom meets 13.5 cells of atoms on average,
    # so the number of distance tests per atom is about 13.5 rho l^3 = 13.5.
    rng = random.Random(8)
    ratios = []
    for box in (4.0, 6.0, 8.0):
        n = int(box ** 3)
        p = random_box(rng, n, box, 3)
        _, tests = CellList(p, box, 1.0).pairs()
        ratios.append(tests / n)
    for r in ratios:
        assert 10.0 < r < 17.0
    assert max(ratios) / min(ratios) < 1.3


def test_distance_helper():
    assert minimum_image_dist2([0.5, 0.5], [7.6, 1.0], 8.0) == pytest.approx(0.9 ** 2 + 0.5 ** 2)
