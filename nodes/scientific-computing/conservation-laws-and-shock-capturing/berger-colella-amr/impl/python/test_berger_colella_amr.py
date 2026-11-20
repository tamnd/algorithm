# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berger-colella-amr/. The authors are listed in prov/64KT6D.jsonl.

import math
from fractions import Fraction

import pytest

from berger_colella_amr import Hierarchy, cell_runs, upwind_uniform


def box(x):
    return Fraction(1) if Fraction(3, 10) <= x < Fraction(1, 2) else Fraction(0)


def bump(x):
    return math.exp(-200 * (x - 0.3) ** 2)


def test_cell_runs_on_a_circle():
    assert cell_runs(set(), 8) == []
    assert cell_runs({2, 3, 4}, 8) == [(2, 5)]
    assert sorted(cell_runs({0, 1, 7, 4}, 8)) == [(4, 5), (7, 10)]
    assert cell_runs(set(range(8)), 8) == [(0, 8)]


def test_one_level_is_the_single_grid_upwind_scheme():
    n0 = 20
    h = Hierarchy(box, n0, 1, Fraction(1, 40), max_level=0)
    h.run(12)
    u0 = [box((j + Fraction(1, 2)) / n0) for j in range(n0)]
    assert [v for _, _, v in h.composite()] == upwind_uniform(u0, 1, Fraction(1, 2), 12)


@pytest.mark.parametrize("a", [1, -1])
def test_full_refinement_is_the_fine_grid_scheme_with_subcycling(a):
    # tol < 0 tags every cell, so level 1 covers the whole circle.
    n0, r = 10, 2
    h = Hierarchy(box, n0, a, Fraction(1, 20), ratio=r, max_level=1, tol=-1)
    h.run(5)
    assert h.levels[1][0].hi - h.levels[1][0].lo == n0 * r
    uf = [box((j + Fraction(1, 2)) / (n0 * r)) for j in range(n0 * r)]
    assert [v for _, _, v in h.composite()] == upwind_uniform(uf, a, a * Fraction(1, 2), 5 * r)


@pytest.mark.parametrize("a,levels", [(1, 1), (1, 2), (-1, 2)])
def test_refluxing_conserves_mass_exactly(a, levels):
    h = Hierarchy(box, 16, a, Fraction(1, 40), ratio=2, max_level=levels,
                  tol=Fraction(1, 10), regrid_every=2)
    m0 = h.mass()
    for _ in range(14):
        h.step()
        assert h.mass() == m0
    assert len(h.levels) == levels + 1


def test_without_refluxing_mass_is_not_conserved():
    h = Hierarchy(box, 16, 1, Fraction(1, 40), ratio=2, max_level=1,
                  tol=Fraction(1, 10), reflux=False)
    m0 = h.mass()
    h.run(6)
    assert h.mass() != m0


@pytest.mark.parametrize("reflux,u5", [(True, Fraction(1, 8)), (False, Fraction(1, 4))])
def test_flux_register_by_hand(reflux, u5):
    # Eight coarse cells, Courant number 1/2, u = 1 on [0, 9/16).
    def f(x):
        return Fraction(1) if x < Fraction(9, 16) else Fraction(0)
    h = Hierarchy(f, 8, 1, Fraction(1, 16), ratio=2, max_level=1,
                  tol=Fraction(1, 2), buffer=0, regrid_every=0, reflux=reflux)
    assert [(p.lo, p.hi) for p in h.levels[1]] == [(6, 10), (14, 18)]
    assert h.levels[1][0].u == [1, 1, 1, 0] and h.levels[0][0].u[4] == Fraction(1, 2)
    h.step()
    # Face 5: the coarse flux is 1/16 * 1/2, the two fine fluxes are 1/32 * (0 + 1/2).
    p, k = h.find(0, 5)
    assert p.u[k] == u5
    assert (h.mass() == Fraction(9, 16)) == reflux


def test_proper_nesting_after_regrids():
    h = Hierarchy(lambda x: bump(x), 32, 1.0, 1 / 64, ratio=2, max_level=2,
                  tol=0.02, buffer=1, regrid_every=2)
    for _ in range(20):
        h.step()
        for l in (1, 2):
            if l + 1 > len(h.levels) - 1:
                continue
            for q in h.levels[l + 1]:
                for c in range(q.lo // 2, q.hi // 2):
                    for d in (-1, 0, 1):
                        assert h.find(l, c + d) is not None


def test_amr_is_more_accurate_than_the_coarse_grid_with_fewer_cells_than_the_fine_grid():
    n0, T = 32, 0.25

    def err(cells):
        return sum(w * abs(v - bump(x + w / 2 - T)) for x, w, v in cells)

    steps = 16                                  # dt0 = T / steps, Courant number 1/2
    coarse = Hierarchy(bump, n0, 1.0, T / steps, max_level=0).run(steps)
    amr = Hierarchy(bump, n0, 1.0, T / steps, ratio=2, max_level=2, tol=0.02,
                    buffer=2, regrid_every=1).run(steps)
    e_c, e_a = err(coarse.composite()), err(amr.composite())
    uf = [bump((j + 0.5) / (4 * n0)) for j in range(4 * n0)]
    fine = upwind_uniform(uf, 1, 0.5, 4 * steps)
    e_f = sum(abs(v - bump((j + 0.5) / (4 * n0) - T)) / (4 * n0) for j, v in enumerate(fine))
    assert e_a < 0.5 * e_c
    assert e_a < 1.3 * e_f
    assert amr.cells() < 0.6 * 4 * n0


def test_rejects_bad_parameters():
    with pytest.raises(ValueError):
        Hierarchy(box, 2, 1, Fraction(1, 10))
