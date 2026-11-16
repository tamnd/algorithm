# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/state-lattice-planning/. The authors are listed in prov/C6YCHP.jsonl.

import math
import random

from state_lattice_planning import (
    QUARTER,
    R_UNIT,
    Lattice,
    build_control_set,
    drive,
    lattice_search,
    primitive_between,
    wrap,
)


def random_lattice(rng, n=24, density=0.04):
    # A lattice point touches four cells and the turning radius is 2.4 cells, so even a
    # low density of blocked cells removes many states.
    blocked = {(a, b) for a in range(n) for b in range(n) if rng.random() < density}
    return Lattice(n, n, blocked)


def random_state(rng, lat):
    return rng.randint(3, lat.nx - 3), rng.randint(3, lat.ny - 3), rng.randrange(8)


def test_primitives_end_on_lattice_states():
    control = build_control_set()
    for k in range(8):
        assert len(control[k]) == 3
        for di, dj, ke, length, segs in control[k]:
            x, y, th = drive((0.0, 0.0, k * QUARTER), segs)
            assert abs(x - di) < 1e-12 and abs(y - dj) < 1e-12
            assert abs(wrap(th - ke * QUARTER)) < 1e-12
            assert abs(length - sum(s for _, s in segs)) < 1e-15
            assert all(abs(kappa) <= 1.0 / R_UNIT + 1e-15 and s > 0 for kappa, s in segs)


def test_heading_is_continuous_inside_a_primitive():
    # Each primitive is a C1 curve: an arc and a line that meet with the same heading.
    control = build_control_set()
    for k in range(8):
        for _, _, _, _, segs in control[k]:
            q = (0.0, 0.0, k * QUARTER)
            for kappa, s in segs:
                a = drive(q, [(kappa, s - 1e-7)])
                b = drive(q, [(kappa, s)])
                assert math.hypot(b[0] - a[0], b[1] - a[1]) < 1.01e-7
                q = b


def test_a_star_matches_dijkstra():
    rng = random.Random(1)
    solved = 0
    for _ in range(40):
        lat = random_lattice(rng)
        s, t = random_state(rng, lat), random_state(rng, lat)
        a = lattice_search(lat, s, t)
        d = lattice_search(lat, s, t, use_heuristic=False)
        assert (a is None) == (d is None)
        if a is None:
            continue
        solved += 1
        assert abs(a[0] - d[0]) < 1e-9
        assert a[2] <= d[2]
        assert a[0] >= math.hypot(t[0] - s[0], t[1] - s[1]) - 1e-12
    assert solved >= 15


def test_path_is_continuous_and_collision_free():
    rng = random.Random(2)
    for _ in range(30):
        lat = random_lattice(rng)
        s, t = random_state(rng, lat), random_state(rng, lat)
        res = lattice_search(lat, s, t)
        if res is None:
            continue
        cost, states, _ = res
        q = (float(s[0]), float(s[1]), s[2] * QUARTER)
        total = 0.0
        for a, b in zip(states, states[1:]):
            segs = primitive_between(lat, a, b)
            # Dense samples, four times denser than the swath, lie in free cells.
            length = sum(x for _, x in segs)
            n = int(math.ceil(length * 32))
            for m in range(1, n):
                part, acc, target = [], 0.0, length * m / n
                for kappa, x in segs:
                    if acc + x >= target:
                        part.append((kappa, target - acc))
                        break
                    part.append((kappa, x))
                    acc += x
                px, py, _ = drive(q, part)
                cell = (int(math.floor(px)), int(math.floor(py)))
                assert cell not in lat.blocked and 0 <= cell[0] < lat.nx and 0 <= cell[1] < lat.ny
            q = drive(q, segs)
            total += length
            assert abs(q[0] - b[0]) < 1e-9 and abs(q[1] - b[1]) < 1e-9
            assert abs(wrap(q[2] - b[2] * QUARTER)) < 1e-9
        assert abs(total - cost) < 1e-9


def test_rotation_invariance():
    # On an empty lattice, rotating the problem by pi / 2 does not change the cost.
    rng = random.Random(3)
    lat = Lattice(30, 30)
    for _ in range(25):
        di, dj, k1 = rng.randint(-6, 6), rng.randint(-6, 6), rng.randrange(8)
        k0 = rng.randrange(8)
        costs = []
        for turns in range(4):
            a, b = di, dj
            for _ in range(turns):
                a, b = -b, a
            s = (15, 15, (k0 + 2 * turns) % 8)
            t = (15 + a, 15 + b, (k1 + 2 * turns) % 8)
            costs.append(lattice_search(lat, s, t)[0])
        assert max(costs) - min(costs) < 1e-9


def test_unreachable_goal():
    blocked = {(5, b) for b in range(10)}
    lat = Lattice(10, 10, blocked)
    assert lattice_search(lat, (1, 5, 0), (9, 5, 0)) is None
