# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loop-modeling/. The authors are listed in prov/BQJJ13.jsonl.

import math
import random

from loop_modeling import (
    A_C_N_CA, A_CA_C_N, A_N_CA_C, B_C_N, B_CA_C, B_N_CA, angle, build_backbone, ccd_angle, ccd_close,
    dihedral, dot, end_deviation, norm, rotatable_bonds, rotate, sub, unit,
)


def random_torsions(rng: random.Random, n: int):
    return [rng.uniform(-180, 180) for _ in range(n)], [rng.uniform(-180, 180) for _ in range(n)]


def sum_sq(moving, targets) -> float:
    return sum(dot(sub(p, q), sub(p, q)) for p, q in zip(moving, targets))


def check_geometry(x) -> None:
    for k in range(len(x) // 3):
        n, ca, c = x[3 * k], x[3 * k + 1], x[3 * k + 2]
        assert abs(norm(sub(ca, n)) - B_N_CA) <= 1e-9
        assert abs(norm(sub(c, ca)) - B_CA_C) <= 1e-9
        assert abs(angle(n, ca, c) - A_N_CA_C) <= 1e-6
        if k + 1 < len(x) // 3:
            n2, ca2 = x[3 * k + 3], x[3 * k + 4]
            assert abs(norm(sub(n2, c)) - B_C_N) <= 1e-9
            assert abs(angle(ca, c, n2) - A_CA_C_N) <= 1e-6
            assert abs(angle(c, n2, ca2) - A_C_N_CA) <= 1e-6
            assert abs(abs(dihedral(ca, c, n2, ca2)) - 180.0) <= 1e-6  # trans peptide bond


def test_build_backbone_has_the_given_dihedrals() -> None:
    rng = random.Random(1)
    phis, psis = random_torsions(rng, 6)
    x = build_backbone(phis, psis)
    check_geometry(x)
    for k in range(1, 6):
        got = dihedral(x[3 * k - 1], x[3 * k], x[3 * k + 1], x[3 * k + 2])
        assert abs((got - phis[k] + 180) % 360 - 180) <= 1e-6
    for k in range(5):
        got = dihedral(x[3 * k], x[3 * k + 1], x[3 * k + 2], x[3 * k + 3])
        assert abs((got - psis[k] + 180) % 360 - 180) <= 1e-6


def test_ccd_angle_is_the_best_single_rotation() -> None:
    rng = random.Random(2)
    for _ in range(15):
        x = build_backbone(*random_torsions(rng, 7))
        targets = build_backbone(*random_torsions(rng, 7))[-3:]
        i, j = rng.choice(rotatable_bonds(7))
        axis = unit(sub(x[j], x[i]))
        theta = ccd_angle(x[j], axis, x[-3:], targets)
        best = sum_sq([rotate(p, x[j], axis, theta) for p in x[-3:]], targets)
        grid = min(sum_sq([rotate(p, x[j], axis, 2 * math.pi * s / 3600) for p in x[-3:]], targets)
                   for s in range(3600))
        assert best <= grid + 1e-9  # no angle of the dense grid does better
        assert best >= grid - 0.05  # and the grid, with steps of 0.1 degree, comes close


def test_each_rotation_never_moves_the_end_away() -> None:
    rng = random.Random(3)
    x = build_backbone(*random_torsions(rng, 7))
    targets = build_backbone(*random_torsions(rng, 7))[-3:]
    for i, j in rotatable_bonds(7):
        before = sum_sq(x[-3:], targets)
        axis = unit(sub(x[j], x[i]))
        theta = ccd_angle(x[j], axis, x[-3:], targets)
        x = x[:j + 1] + [rotate(p, x[j], axis, theta) for p in x[j + 1:]]
        assert sum_sq(x[-3:], targets) <= before + 1e-12


def reachable_case(seed: int, n_res: int):
    """A target taken from a real chain with the same anchor, and a random start."""
    rng = random.Random(seed)
    true_phi, true_psi = random_torsions(rng, n_res)
    targets = build_backbone(true_phi, true_psi)[-3:]
    phi, psi = random_torsions(rng, n_res)
    phi[-1] = true_phi[-1]  # the end residue is a rigid block, so its own phi must match the target
    return build_backbone(phi, psi), targets


def test_ccd_closes_reachable_loops() -> None:
    # CCD has no convergence guarantee; these fixed seeds close within 3000 sweeps.
    for seed in range(102, 108):
        x0, targets = reachable_case(seed, 8)  # anchor, six loop residues, moving end
        assert end_deviation(x0, targets) > 4.0
        x, sweeps, dev = ccd_close(x0, targets, tol=0.08, max_sweeps=3000)
        assert dev <= 0.08, (seed, sweeps, dev)
        assert x[:3] == x0[:3]  # the anchor does not move
        check_geometry(x)


def test_deviation_never_grows_even_when_ccd_stalls() -> None:
    x, targets = reachable_case(106, 6)  # a start where CCD stalls far from closure
    last = end_deviation(x, targets)
    for _ in range(100):
        x, _, dev = ccd_close(x, targets, tol=0.0, max_sweeps=1)
        assert dev <= last + 1e-12
        last = dev
    assert last > 0.08


def test_random_bond_order_also_closes() -> None:
    rng = random.Random(7)
    true_phi, true_psi = random_torsions(rng, 8)
    targets = build_backbone(true_phi, true_psi)[-3:]
    phi, psi = random_torsions(rng, 8)
    phi[-1] = true_phi[-1]
    x, _, dev = ccd_close(build_backbone(phi, psi), targets, tol=0.01, rng=random.Random(8))
    assert dev <= 0.01
    check_geometry(x)
