# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qm-mm-method/. The authors are listed in prov/CDM80T.jsonl.
import math
import random

import pytest

from qm_mm_method import Params, additive, jacobi_eigen, model_sites, oniom, qm_chain, velocity_verlet


def chain(n, seed, jitter=0.1):
    rng = random.Random(seed)
    return [2.0 * i + rng.uniform(-jitter, jitter) for i in range(n)]


def test_jacobi_matches_the_eigenvalues_of_a_uniform_chain():
    n = 6
    h = [[-1.0 if abs(i - j) == 1 else 0.0 for j in range(n)] for i in range(n)]
    vals, vecs = jacobi_eigen(h)
    exact = sorted(-2.0 * math.cos(k * math.pi / (n + 1)) for k in range(1, n + 1))
    assert vals == pytest.approx(exact, abs=1e-12)
    for lam, c in zip(vals, vecs):
        hc = [sum(h[i][j] * c[j] for j in range(n)) for i in range(n)]
        assert hc == pytest.approx([lam * ci for ci in c], abs=1e-12)


def test_dimer_by_hand():
    # Two sites at the distance r0: t = 1, E = -2 t + A = -1 and no force.
    e, f = qm_chain([0.0, 1.0], Params())
    assert e == pytest.approx(-1.0, abs=1e-14)
    assert f == pytest.approx([0.0, 0.0], abs=1e-14)


def test_three_atom_example_by_hand():
    # Atom 0 is QM; the link atom sits at 0 + 0.5 * 2.2 = 1.1.
    y = [0.0, 2.2, 4.2]
    t, phi = 2.0 ** -0.1, 2.0 ** -0.2
    e_qm = -2.0 * t + phi
    de_dr = 2.0 * math.log(2.0) * (t - phi)
    e, f = additive(y, 0, 1)
    assert e == pytest.approx(e_qm + 0.5 * 10.0 * 0.2 ** 2, abs=1e-12)
    assert f == pytest.approx([2.0 + de_dr / 2, -2.0 - de_dr / 2, 0.0], abs=1e-12)
    e2, f2 = oniom(y, 0, 1)
    assert e2 == pytest.approx(e_qm, abs=1e-12)
    assert f2 == pytest.approx([de_dr / 2, -de_dr / 2, 0.0], abs=1e-12)


@pytest.mark.parametrize("scheme", [additive, oniom])
@pytest.mark.parametrize("region", [(0, 3), (2, 6), (5, 8), (0, 8)])
def test_forces_are_minus_the_gradient(scheme, region):
    y = chain(8, 1)
    _, f = scheme(y, *region)
    eps = 1e-6
    for i in range(len(y)):
        up, down = list(y), list(y)
        up[i] += eps
        down[i] -= eps
        fd = -(scheme(up, *region)[0] - scheme(down, *region)[0]) / (2 * eps)
        assert fd == pytest.approx(f[i], abs=1e-7)
    assert abs(sum(f)) < 1e-12


def test_whole_system_in_the_qm_region_gives_the_qm_energy():
    y = chain(6, 3)
    e_qm, _ = qm_chain(y, Params())
    assert additive(y, 0, 6)[0] == pytest.approx(e_qm, abs=1e-12)
    assert oniom(y, 0, 6)[0] == pytest.approx(e_qm, abs=1e-12)


def test_additive_minus_subtractive_is_the_mm_energy_of_the_cut_bonds():
    p = Params()
    y = chain(8, 4, jitter=0.3)
    cut = [(1, 2), (5, 6)]
    e_cut = sum(0.5 * p.k * (y[j] - y[i] - p.d0) ** 2 for i, j in cut)
    assert additive(y, 2, 6)[0] - oniom(y, 2, 6)[0] == pytest.approx(e_cut, abs=1e-12)


def test_link_atoms_and_odd_model_systems():
    assert model_sites(5, 1, 3, 0.5) == [[(1, 0.5), (0, 0.5)], [(1, 1.0)], [(2, 1.0)], [(2, 0.5), (3, 0.5)]]
    with pytest.raises(ValueError):
        additive(chain(5, 0), 1, 2)  # one QM atom and two link atoms: three electrons
    with pytest.raises(ValueError):
        additive(chain(5, 0), 3, 3)


@pytest.mark.parametrize("scheme", [additive, oniom])
def test_energy_is_conserved_to_second_order(scheme):
    def drift(h):
        rng = random.Random(2)
        y = chain(8, 2)
        v = [rng.gauss(0.0, 0.3) for _ in y]
        mean = sum(v) / len(v)
        v = [x - mean for x in v]
        energies = velocity_verlet(y, v, h, round(5.0 / h), 2, 6, scheme)
        return max(abs(e - energies[0]) for e in energies)

    coarse, fine = drift(0.02), drift(0.01)
    assert coarse < 1e-3
    assert 3.0 < coarse / fine < 5.0
