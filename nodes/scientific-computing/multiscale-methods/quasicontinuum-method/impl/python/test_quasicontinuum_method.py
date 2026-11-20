# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quasicontinuum-method/. The authors are listed in prov/7F8PW8.jsonl.
import random

import pytest

from quasicontinuum_method import (Chain, full_atomistic, interpolation, lennard_jones, positions,
                                   qce_energy, qce_gradient_hessian, qcf_residual_jacobian,
                                   quasicontinuum)

A0 = 1.1196108663112254  # equilibrium spacing of the LJ chain with first and second neighbors


def full_energy(chain, y):
    return sum(s * chain.pair(y[j] - y[i])[0] for i, j, s in chain.bonds())


def atom_energy_sum(chain, rep, nonlocal_set, z):
    """Oracle for E_QCE: add the energy of each atom, one atom at a time."""
    t_rows = interpolation(chain.n, rep)
    y = positions(t_rows, z)
    total = 0.0
    for i in range(chain.n):
        if i in nonlocal_set:
            total += 0.5 * sum(s * chain.pair(y[q] - y[p])[0]
                               for p, q, s in chain.bonds() if i in (p, q))
            continue
        k = max(k for k, p in enumerate(rep) if p <= i)
        if rep[k] == i:
            ws = []
            for e in (k - 1, k):
                h = (rep[e + 1] - rep[e]) * chain.a
                ws.append(chain.cauchy_born((z[e + 1] - z[e]) / h)[0])
            total += 0.5 * (ws[0] + ws[1])
        else:
            h = (rep[k + 1] - rep[k]) * chain.a
            total += chain.cauchy_born((z[k + 1] - z[k]) / h)[0]
    return total


def random_mesh(rng, n):
    nonlocal_set = set(range(0, 3)) | set(range(n - 3, n))
    mid = rng.randrange(8, n - 12)
    nonlocal_set |= set(range(mid, mid + rng.randrange(1, 5)))
    rep = set(nonlocal_set)
    for i in range(n):
        if rng.random() < 0.3:
            rep.add(i)
    return sorted(rep), nonlocal_set


def test_all_atoms_nonlocal_is_full_atomistics():
    rng = random.Random(1)
    chain = Chain(25, A0, lennard_jones, True, {(12, 13): 0.5})
    rep = list(range(25))
    y = [A0 * i + rng.uniform(-0.02, 0.02) for i in range(25)]
    assert qce_energy(chain, rep, set(rep), y) == pytest.approx(full_energy(chain, y), rel=1e-13)


@pytest.mark.parametrize("seed", range(6))
def test_energy_equals_sum_of_atom_energies(seed):
    rng = random.Random(seed)
    n = 40
    chain = Chain(n, A0, lennard_jones, nnn=rng.random() < 0.7)
    rep, nonlocal_set = random_mesh(rng, n)
    z = [A0 * 1.01 * p + rng.uniform(-0.01, 0.01) for p in rep]
    assert qce_energy(chain, rep, nonlocal_set, z) == pytest.approx(
        atom_energy_sum(chain, rep, nonlocal_set, z), rel=1e-12)


def test_gradient_and_hessian_match_finite_differences():
    rng = random.Random(7)
    n = 30
    chain = Chain(n, A0, lennard_jones, True)
    rep, nonlocal_set = random_mesh(rng, n)
    z = [A0 * 1.01 * p + rng.uniform(-0.01, 0.01) for p in rep]
    g, kmat = qce_gradient_hessian(chain, rep, nonlocal_set, z)
    e = 1e-6
    for k in range(len(rep)):
        zp, zm = list(z), list(z)
        zp[k] += e
        zm[k] -= e
        fd = (qce_energy(chain, rep, nonlocal_set, zp) - qce_energy(chain, rep, nonlocal_set, zm)) / (2 * e)
        assert g[k] == pytest.approx(fd, abs=1e-6)
        gp, _ = qce_gradient_hessian(chain, rep, nonlocal_set, zp, False)
        gm, _ = qce_gradient_hessian(chain, rep, nonlocal_set, zm, False)
        for m in range(len(rep)):
            assert kmat[m][k] == pytest.approx((gp[m] - gm[m]) / (2 * e), abs=1e-5)


def test_ghost_forces_at_the_reference_lattice():
    n = 31
    nonlocal_set = set(range(0, 11)) | set(range(21, 31))
    rep = list(range(n))
    z = [A0 * i for i in range(n)]
    chain = Chain(n, A0, lennard_jones, True)
    g, _ = qce_gradient_hessian(chain, rep, nonlocal_set, z, False)
    half = 0.5 * lennard_jones(2 * A0)[1]
    expected = {9: -half, 10: half, 11: half, 12: -half, 19: half, 20: -half, 21: -half, 22: half}
    for i in range(2, n - 2):
        assert -g[i] == pytest.approx(expected.get(i, 0.0), abs=1e-12)
    # With nearest neighbors only, or with the force-based coupling, there are no ghost forces.
    g_nn, _ = qce_gradient_hessian(Chain(n, A0, lennard_jones, False), rep, nonlocal_set, z, False)
    r_qcf, _ = qcf_residual_jacobian(chain, rep, nonlocal_set, z)
    for i in range(2, n - 2):
        assert abs(g_nn[i]) < 1e-12
        assert abs(r_qcf[i]) < 1e-12


def defect_problem():
    n = 81
    chain = Chain(n, A0, lennard_jones, True, {(40, 41): 0.5})
    y0 = [1.02 * A0 * i for i in range(n)]
    fixed_atoms = [0, 1, n - 2, n - 1]
    nonlocal_set = set(range(0, 4)) | set(range(32, 50)) | set(range(77, 81))
    rep = sorted(nonlocal_set | set(range(4, 32, 4)) | set(range(50, 77, 4)))
    z0 = [y0[p] for p in rep]
    fixed = [rep.index(p) for p in fixed_atoms]
    exact = full_atomistic(chain, y0, fixed_atoms)
    return chain, rep, nonlocal_set, z0, fixed, exact


def test_weak_bond_qcf_matches_full_atomistics_with_half_the_unknowns():
    chain, rep, nonlocal_set, z0, fixed, exact = defect_problem()
    assert len(rep) == 40
    _, y_qcf = quasicontinuum(chain, rep, nonlocal_set, z0, fixed, "qcf")
    _, y_qce = quasicontinuum(chain, rep, nonlocal_set, z0, fixed, "qce")
    err_qcf = max(abs(p - q) for p, q in zip(y_qcf, exact))
    err_qce = max(abs(p - q) for p, q in zip(y_qce, exact))
    assert err_qcf < 1e-8
    assert 1e-4 < err_qce < 1e-2
    # The weak bond opens more than the mean spacing.
    assert exact[41] - exact[40] > 1.02 * A0 + 0.03


def test_qce_minimizer_has_zero_gradient_and_qcf_keeps_uniform_strain():
    n = 41
    chain = Chain(n, A0, lennard_jones, True)
    nonlocal_set = set(range(0, 4)) | set(range(18, 23)) | set(range(37, 41))
    rep = sorted(nonlocal_set | {6, 9, 12, 15, 26, 30, 34})
    z0 = [1.03 * A0 * p for p in rep]
    fixed = [rep.index(p) for p in (0, 1, n - 2, n - 1)]
    z_qcf, _ = quasicontinuum(chain, rep, nonlocal_set, z0, fixed, "qcf")
    assert max(abs(p - q) for p, q in zip(z_qcf, z0)) < 1e-12
    z_qce, _ = quasicontinuum(chain, rep, nonlocal_set, z0, fixed, "qce")
    g, _ = qce_gradient_hessian(chain, rep, nonlocal_set, z_qce, False)
    free = [k for k in range(len(rep)) if k not in fixed]
    assert max(abs(g[k]) for k in free) < 1e-10
    assert max(abs(p - q) for p, q in zip(z_qce, z0)) > 1e-4


def test_bad_meshes_are_rejected():
    with pytest.raises(ValueError):  # the last atom is not a repatom
        quasicontinuum(Chain(10, A0, lennard_jones), [0, 3, 8], {0, 8}, [0.0, 3.0, 8.0], [0, 2])
    chain = Chain(10, A0, lennard_jones, True, {(4, 5): 0.5})
    with pytest.raises(ValueError):  # the weak bond is in the local region
        quasicontinuum(chain, [0, 4, 5, 9], {0, 9}, [0.0, 4.0, 5.0, 9.0], [0, 3])
