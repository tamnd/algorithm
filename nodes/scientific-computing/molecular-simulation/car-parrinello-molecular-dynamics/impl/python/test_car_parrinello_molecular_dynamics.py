# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/car-parrinello-molecular-dynamics/. The authors are listed in prov/PQJARX.jsonl.
import math

import pytest

from car_parrinello_molecular_dynamics import ToyModel, cpmd

X0 = [0.0, 1.1, 2.0, 3.2]
V0 = [0.3, -0.2, 0.1, -0.2]
MASSES = [1.0] * 4


def bo_reference(model, h, steps):
    """Born-Oppenheimer positions with a tight SCF at every step, same integrator for the nuclei."""
    x, v = list(X0), list(V0)
    c = model.ground_state(x)
    f = model.nuclear_force(x, c)
    traj = [list(x)]
    for _ in range(steps):
        v = [vi + 0.5 * h * fi for vi, fi in zip(v, f)]
        x = [xi + h * vi for xi, vi in zip(x, v)]
        c = model.ground_state(x, [q * q for q in c])
        f = model.nuclear_force(x, c)
        v = [vi + 0.5 * h * fi for vi, fi in zip(v, f)]
        traj.append(list(x))
    return traj


def run(mu, h, steps):
    model = ToyModel(u=1.0)
    c = model.ground_state(X0)
    return model, cpmd(model, list(X0), list(V0), MASSES, c, [0.0] * 4, mu, h, steps)


def test_constraint_is_kept_to_rounding():
    _, out = run(0.01, 0.004, 500)
    assert max(abs(sum(q * q for q in o[1]) - 1.0) for o in out) < 1e-12


def test_ground_state_with_fixed_nuclei_does_not_move():
    model = ToyModel(u=1.0)
    c = model.ground_state(X0)
    out = cpmd(model, list(X0), [0.0] * 4, MASSES, list(c), [0.0] * 4, 0.01, 0.004, 200, fixed_nuclei=True)
    assert max(abs(p - q) for p, q in zip(out[-1][1], c)) < 1e-9
    assert out[-1][3] < 1e-15


def test_orbital_frequency_of_two_level_dimer():
    # U = 0 dimer at r = 1: gap 2, so omega_e = 2 sqrt(gap / mu).
    model = ToyModel(u=0.0)
    s = 1 / math.sqrt(2)
    th = 0.05
    c = [s * (math.cos(th) + math.sin(th)), s * (math.cos(th) - math.sin(th))]
    mu, h = 0.01, 0.002
    out = cpmd(model, [0.0, 1.0], [0.0, 0.0], [1.0, 1.0], c, [0.0, 0.0], mu, h, 3000, fixed_nuclei=True)
    proj = [s * (o[1][0] - o[1][1]) for o in out]
    down = [i for i in range(1, len(proj)) if proj[i - 1] > 0 >= proj[i]]
    period = (down[-1] - down[0]) * h / (len(down) - 1)
    assert 2 * math.pi / period == pytest.approx(2 * math.sqrt(2 / mu), rel=0.01)


def test_extended_energy_is_conserved():
    _, out = run(0.01, 0.004, 1250)
    e = [o[4] for o in out]
    assert max(e) - min(e) < 1e-5


def test_small_mass_tracks_born_oppenheimer_and_large_mass_does_not():
    h, steps = 0.004, 1250  # time 5
    model, small = run(0.01, h, steps)
    _, large = run(0.2, h, steps)
    ref = bo_reference(model, h, steps)
    dev_small = max(max(abs(a - b) for a, b in zip(r, o[0])) for r, o in zip(ref, small))
    dev_large = max(max(abs(a - b) for a, b in zip(r, o[0])) for r, o in zip(ref, large))
    assert dev_small < 0.01
    assert dev_large > 5 * dev_small
    # The fictitious kinetic energy stays a small part of the nuclear kinetic energy.
    k_fict = max(o[3] for o in small)
    k_nuc = sum(o[2] for o in small) / len(small)
    assert k_fict < 0.01 * k_nuc
