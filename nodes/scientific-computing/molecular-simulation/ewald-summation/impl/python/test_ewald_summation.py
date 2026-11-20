# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ewald-summation/. The authors are listed in prov/674E3C.jsonl.

import math
import random

import pytest

from ewald_summation import ewald, madelung_nacl, nacl_cell


def random_system(seed: int, n: int, box: float) -> tuple[list[float], list[list[float]]]:
    rng = random.Random(seed)
    pos = [[rng.uniform(0, box) for _ in range(3)] for _ in range(n)]
    q = [rng.uniform(-1, 1) for _ in range(n - 1)]
    q.append(-sum(q))
    return q, pos


def test_madelung_constant_of_nacl() -> None:
    # 1.747565 is the Madelung constant of rock salt for the nearest-neighbour distance
    assert abs(madelung_nacl() - 1.747565) < 1e-6
    assert abs(madelung_nacl(2.0, 3.0, 8) - madelung_nacl(3.0, 2.2, 11)) < 1e-9


def test_energy_does_not_depend_on_alpha() -> None:
    q, pos = random_system(1, 6, 4.0)
    energies = [ewald(q, pos, 4.0, a, 9.0, 12)[0] for a in (0.8, 1.0, 1.3)]
    assert max(energies) - min(energies) < 1e-8
    parts = [ewald(q, pos, 4.0, a, 9.0, 12)[2] for a in (0.8, 1.3)]
    assert abs(parts[0]["real"] - parts[1]["real"]) > 1e-2  # the split moves, the sum does not


def test_vacuum_energy_is_the_limit_of_spherical_direct_sums() -> None:
    q, pos, box = [1.0, -1.0, 0.5, -0.5], None, 3.0
    rng = random.Random(5)
    pos = [[rng.uniform(0, box) for _ in range(3)] for _ in range(4)]
    e_vac = ewald(q, pos, box, 1.2, 7.0, 10, "vacuum")[0]

    def direct(radius: int) -> float:
        e = 0.0
        for nx in range(-radius, radius + 1):
            for ny in range(-radius, radius + 1):
                for nz in range(-radius, radius + 1):
                    if nx * nx + ny * ny + nz * nz > radius * radius:
                        continue
                    for i in range(4):
                        for j in range(4):
                            if i == j and nx == ny == nz == 0:
                                continue
                            d = [pos[i][0] - pos[j][0] + nx * box, pos[i][1] - pos[j][1] + ny * box, pos[i][2] - pos[j][2] + nz * box]
                            e += 0.5 * q[i] * q[j] / math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)
        return e

    e4, e8 = direct(4), direct(8)
    assert abs(e8 - e_vac) < 2e-5
    assert abs(e8 - e_vac) < abs(e4 - e_vac)


@pytest.mark.parametrize("surface", ["tinfoil", "vacuum"])
def test_forces_are_minus_the_gradient(surface: str) -> None:
    box = 4.0
    q, pos = random_system(2, 5, box)
    _, f, _ = ewald(q, pos, box, 1.0, 6.5, 9, surface)
    h = 1e-6
    for i in range(len(q)):
        for a in range(3):
            pp = [list(p) for p in pos]
            pm = [list(p) for p in pos]
            pp[i][a] += h
            pm[i][a] -= h
            num = -(ewald(q, pp, box, 1.0, 6.5, 9, surface)[0] - ewald(q, pm, box, 1.0, 6.5, 9, surface)[0]) / (2 * h)
            assert abs(num - f[i][a]) < 1e-6 * max(1.0, abs(f[i][a]))


def test_newton_third_law_and_lattice_symmetry() -> None:
    box = 4.0
    q, pos = random_system(3, 6, box)
    _, f, _ = ewald(q, pos, box, 1.0, 9.0, 12)
    for a in range(3):
        assert abs(sum(fi[a] for fi in f)) < 1e-10
    # each ion of the perfect crystal is at a centre of symmetry, so its force is zero
    q, pos, box = nacl_cell()
    _, f, _ = ewald(q, pos, box, 2.5, 2.5, 9)
    assert max(abs(x) for fi in f for x in fi) < 1e-12


def test_tinfoil_energy_is_periodic_in_each_position() -> None:
    box = 4.0
    q, pos = random_system(4, 4, box)
    e0 = ewald(q, pos, box, 1.0, 9.0, 12)[0]
    moved = [list(p) for p in pos]
    moved[2][1] += box
    assert abs(ewald(q, moved, box, 1.0, 9.0, 12)[0] - e0) < 1e-10


def test_charged_system_is_rejected() -> None:
    with pytest.raises(ValueError):
        ewald([1.0, 1.0], [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]], 3.0, 1.0, 5.0, 5)
