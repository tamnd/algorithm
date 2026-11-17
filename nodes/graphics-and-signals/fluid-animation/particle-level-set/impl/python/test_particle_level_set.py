# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-level-set/. The authors are listed in prov/S6VHF6.jsonl.

"""Tests of the particle level set: seeding, the correction, and Zalesak's slotted disk."""

import math
import random

import pytest

import particle_level_set as P

N = 32
DX = 1.0 / N
SLOT = P.zalesak(0.5, 0.75, 0.15, 0.05, 0.25)
TURN = P.rotation(0.5, 0.5, 2.0 * math.pi)  # one turn in the time 1
M = 200  # sample points per side for the areas; the slot is then 10 samples wide


def run(use, steps, seed=3):
    st = P.ParticleLevelSet(N, DX, SLOT, random.Random(seed), use_particles=use)
    for k in range(steps):
        st.step(TURN, k / steps, 1.0 / steps)
    return st


def test_rotation_trace_is_exact():
    x, y = 0.3, 0.8
    for _ in range(8):
        x, y = TURN(x, y, 0.0, 0.125)
    assert abs(x - 0.3) < 1e-12 and abs(y - 0.8) < 1e-12
    assert TURN(*TURN(0.3, 0.8, 0.0, 0.1), 0.1, -0.1) == pytest.approx((0.3, 0.8), abs=1e-12)


def test_reinitialize_gives_a_distance_and_keeps_the_sign():
    def d(x, y):
        return math.hypot(x - 0.5, y - 0.5) - 0.3

    st = P.ParticleLevelSet(N, DX, lambda x, y: 1.5 * d(x, y), use_particles=False)
    cells = [(i, j) for i in range(N) for j in range(N) if 1.2 * DX < abs(d((i + 0.5) * DX, (j + 0.5) * DX)) < 3 * DX]
    assert len(cells) > 100
    assert max(abs(st.phi[i][j] - d((i + 0.5) * DX, (j + 0.5) * DX)) for (i, j) in cells) < 0.1 * DX
    assert all((st.phi[i][j] < 0.0) == (d((i + 0.5) * DX, (j + 0.5) * DX) < 0.0) for i in range(N) for j in range(N))


def test_seeded_particles_are_on_their_side_and_none_has_escaped():
    st = P.ParticleLevelSet(N, DX, SLOT, random.Random(3))
    assert len(st.particles) == 400
    pos = sum(1 for p in st.particles if p[2] > 0.0)
    assert 150 < pos < 250
    for (x, y, s, r) in st.particles:
        ph = st.value(x, y)
        assert st.b_min - 1e-12 <= s * ph <= st.b_max + 1e-12
        assert st.r_min <= r <= st.r_max and r <= s * ph + 1e-12
    before = [list(c) for c in st.phi]
    assert st.correct() == 0
    assert st.phi == before


def test_one_escaped_particle_moves_the_interface():
    st = P.ParticleLevelSet(N, DX, lambda x, y: y - 0.5, per_cell=0)
    assert st.particles == []
    x, y, r = 0.5 + 0.5 * DX, 0.5 + 0.4 * DX, 0.3 * DX  # an inside particle above the surface y = 0.5
    st.particles = [[x, y, -1.0, r]]
    old = [list(c) for c in st.phi]
    assert len(st.escaped()) == 1
    assert st.correct() == 1
    assert st.phi[16][16] == pytest.approx(-0.2 * DX, abs=1e-12)  # min(0.5 dx, -(0.3 - 0.1) dx)
    for (i, j) in ((16, 15), (15, 16), (17, 16), (15, 15), (17, 15)):
        assert st.phi[i][j] == old[i][j]
    changed = [(i, j) for i in range(N) for j in range(N) if st.phi[i][j] != old[i][j]]
    assert changed == [(16, 16)]


def test_a_particle_that_is_not_out_by_its_radius_has_not_escaped():
    st = P.ParticleLevelSet(N, DX, lambda x, y: y - 0.5, per_cell=0)
    st.particles = [[0.5, 0.5 + 0.2 * DX, -1.0, 0.3 * DX], [0.5, 0.5 + 0.2 * DX, 1.0, 0.3 * DX]]
    assert st.escaped() == []
    st.adjust_radii()
    assert st.particles[0][3] == st.r_min  # on the wrong side: the smallest radius
    assert st.particles[1][3] == pytest.approx(0.2 * DX)


def test_the_exact_slotted_disk_has_the_area_of_the_paper():
    assert abs(P.inside_area(SLOT, 1.0, M) - 0.05822) < 2e-4  # 582.2 on the 100 by 100 domain of the paper


def test_particles_keep_the_slotted_disk_through_a_turn():
    a0 = P.inside_area(SLOT, 1.0, M)
    plain = run(False, 64)
    pls = run(True, 64)
    a_plain = P.inside_area(plain.value, 1.0, M)
    a_pls = P.inside_area(pls.value, 1.0, M)
    assert a_plain < 0.5 * a0  # the plain level set loses more than half of the area
    assert a_pls > 0.9 * a0
    assert abs(a_plain - 0.02728) < 1e-4 and abs(a_pls - 0.05355) < 1e-4
    e_plain = P.area_of_difference(plain.value, SLOT, 1.0, M)
    e_pls = P.area_of_difference(pls.value, SLOT, 1.0, M)
    assert e_pls < 0.55 * e_plain


def test_more_steps_lose_more_area_without_particles():
    a32 = P.inside_area(run(False, 32).value, 1.0, M)
    a64 = P.inside_area(run(False, 64).value, 1.0, M)
    assert a64 < 0.7 * a32
    b32 = P.inside_area(run(True, 32).value, 1.0, M)
    assert abs(b32 - 0.05493) < 1e-4


def test_bad_input():
    with pytest.raises(ValueError):
        P.ParticleLevelSet(1, DX, SLOT)
    with pytest.raises(ValueError):
        P.ParticleLevelSet(N, 0.0, SLOT)
