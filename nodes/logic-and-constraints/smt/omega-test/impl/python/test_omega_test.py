# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/omega-test/. The authors are listed in prov/8M5CJY.jsonl.

import itertools
import random

from omega_test import bounds_on, dark_shadow, holds, mod_hat, real_shadow, solve, splinters


def box(names: list, r: int) -> list:
    out = []
    for v in names:
        out.append(({v: 1}, r))  # v + r >= 0
        out.append(({v: -1}, r))  # r - v >= 0
    return out


def sat_at(cons: list, point: dict) -> bool:
    return all(c + sum(a * point[v] for v, a in co.items()) >= 0 for co, c in cons)


def brute(names: list, eqs: list, ineqs: list, r: int) -> bool:
    for p in itertools.product(range(-r, r + 1), repeat=len(names)):
        if holds(dict(zip(names, p)), eqs, ineqs):
            return True
    return False


def random_con(rng: random.Random, names: list, cmax: int, kmax: int) -> tuple:
    while True:
        co = {v: rng.randint(-cmax, cmax) for v in names}
        co = {v: a for v, a in co.items() if a}
        if co:
            return co, rng.randint(-kmax, kmax)


def test_mod_hat() -> None:
    for m in range(2, 9):
        for a in range(-30, 31):
            r = mod_hat(a, m)
            assert (a - r) % m == 0 and -m / 2 <= r < m / 2
    for a in list(range(-9, -1)) + list(range(2, 10)):
        assert mod_hat(a, abs(a) + 1) == (-1 if a > 0 else 1)


def test_page_example() -> None:
    # 2 <= 3x - 2y <= 3 and 1 <= y <= 4 (see the page)
    ineqs = [({"x": 3, "y": -2}, -2), ({"x": -3, "y": 2}, 3), ({"y": 1}, -1), ({"y": -1}, 4)]
    proj = {y for y in range(-10, 11) if any(sat_at(ineqs, {"x": x, "y": y}) for x in range(-10, 11))}
    assert proj == {2, 3}
    rs = real_shadow(ineqs, "x")
    ds = dark_shadow(ineqs, "x")
    assert {y for y in range(-10, 11) if sat_at(rs, {"y": y})} == {1, 2, 3, 4}
    assert {y for y in range(-10, 11) if sat_at(ds, {"y": y})} == set()
    sp = splinters(ineqs, "x")
    assert len(sp) == 2  # 3x = 2 + 2y + i for i = 0, 1
    m = solve([], ineqs)
    assert m is not None and holds(m, [], ineqs)
    assert solve([], ineqs + [({"y": -1}, 1)]) is None  # y <= 1 leaves no integer point


def test_pugh_style_examples() -> None:
    # A parallelogram with real points but no integer points.
    ineqs = [({"x": 11, "y": 13}, -27), ({"x": -11, "y": -13}, 45), ({"x": 7, "y": -9}, 10), ({"x": -7, "y": 9}, 4)]
    assert solve([], ineqs) is None
    assert not brute(["x", "y"], [], ineqs, 20)
    assert real_shadow(ineqs, "x") and all(not co or c >= 0 for co, c in real_shadow(real_shadow(ineqs, "x"), "y"))
    # Parity: 2x = 2y + 1 has no integer solution.
    assert solve([({"x": 2, "y": -2}, -1)], []) is None
    # Equalities with large coefficients and a planted solution.
    eqs = [({"x": 7, "y": 12, "z": 31}, -17 - 0), ({"x": 3, "y": 5, "z": 14}, -7)]
    m = solve(eqs, [({"x": 1}, -1), ({"x": -1}, 40), ({"y": 1}, 50), ({"y": -1}, 50)])
    if m is not None:
        assert holds(m, eqs, [])


def test_shadows_against_brute_force() -> None:
    rng = random.Random(1991)
    r = 3
    kinds = {"exact": 0, "inexact": 0, "splintered": 0}
    for _ in range(400):
        ineqs = box(["x", "y", "z"], r) + [random_con(rng, ["x", "y", "z"], 4, 8) for _ in range(rng.randint(1, 3))]
        lows, ups, _ = bounds_on(ineqs, "z")
        exact = all(a == 1 for a, _ in ups) or all(b == 1 for b, _ in lows)
        kinds["exact" if exact else "inexact"] += 1
        rs, ds, sp = real_shadow(ineqs, "z"), dark_shadow(ineqs, "z"), splinters(ineqs, "z")
        for x, y in itertools.product(range(-r, r + 1), repeat=2):
            zs = [z for z in range(-r, r + 1) if sat_at(ineqs, {"x": x, "y": y, "z": z})]
            in_real = sat_at(rs, {"x": x, "y": y})
            in_dark = sat_at(ds, {"x": x, "y": y})
            assert not in_dark or zs  # dark shadow is inside the integer projection
            assert not zs or in_real  # integer projection is inside the real shadow
            if exact:
                assert bool(zs) == in_real
            if zs and not in_dark:  # a splinter must catch this point
                kinds["splintered"] += 1
                p = {"x": x, "y": y}
                assert any(
                    c + sum(a * p.get(v, z) for v, a in co.items()) == 0 for co, c in sp for z in zs
                )
    assert min(kinds.values()) > 20


def test_solve_against_brute_force() -> None:
    rng = random.Random(4)
    r = 3
    for trial in range(300):
        names = ["x", "y"] if trial < 150 else ["x", "y", "z"]
        eqs = [random_con(rng, names, 5, 6) for _ in range(rng.randint(0, 1))]
        ineqs = box(names, r) + [random_con(rng, names, 5, 8) for _ in range(rng.randint(1, 3))]
        m = solve(eqs, ineqs)
        assert (m is not None) == brute(names, eqs, ineqs, r)
        if m is not None:
            assert holds(m, eqs, ineqs)


def test_planted_unbounded() -> None:
    rng = random.Random(12)
    names = ["a", "b", "c", "d"]
    for _ in range(150):
        point = {v: rng.randint(-20, 20) for v in names}
        cons = [random_con(rng, names, 9, 0) for _ in range(rng.randint(1, 4))]
        eqs = [(co, -sum(a * point[v] for v, a in co.items())) for co in [c for c, _ in cons[:2]]]
        ineqs = [(co, -sum(a * point[v] for v, a in co.items()) + rng.randint(0, 3)) for co, _ in cons[2:]]
        m = solve(eqs, ineqs)
        assert m is not None and holds(m, eqs, ineqs)
        # Doubling an equation and adding 1 to its constant leaves an odd
        # constant with even coefficients: no integer solution.
        co, c = eqs[0]
        assert solve([({v: 2 * a for v, a in co.items()}, 2 * c + 1)] + eqs[1:], ineqs) is None
