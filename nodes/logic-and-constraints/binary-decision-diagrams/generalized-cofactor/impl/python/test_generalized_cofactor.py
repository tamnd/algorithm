# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-cofactor/. The authors are listed in prov/PVN188.jsonl.

import random

from generalized_cofactor import BDD, FALSE, TRUE, constrain, restrict


def distance(n: int, a: int, b: int) -> int:
    """sum of |a_i - b_i| 2^(n-1-i): x_0 is the top variable and weighs most."""
    d = a ^ b
    return sum(1 << (n - 1 - i) for i in range(n) if d >> i & 1)


def support(n: int, t: list[int]) -> set[int]:
    return {i for i in range(n) if any(t[a] != t[a | 1 << i] for a in range(1 << n) if not a >> i & 1)}


def random_table(rng: random.Random, n: int) -> list[int]:
    p = rng.random()
    return [int(rng.random() < p) for _ in range(1 << n)]


def test_tables_and_ite() -> None:
    rng = random.Random(3)
    for n in range(0, 7):
        b = BDD(n)
        for _ in range(20):
            t, s, r = (random_table(rng, n) for _ in range(3))
            f, g, h = b.from_table(t), b.from_table(s), b.from_table(r)
            assert b.table(f) == t
            assert b.table(b.ite(f, g, h)) == [s[a] if t[a] else r[a] for a in range(1 << n)]
            assert b.from_table(list(t)) == f  # canonical
        b.check_invariant()


def test_agree_on_care_set_and_closest_point() -> None:
    rng = random.Random(1989)
    checked = 0
    for _ in range(600):
        n = rng.randrange(1, 8)
        b = BDD(n)
        tf = random_table(rng, n)
        tc = random_table(rng, n)
        if not any(tc):
            tc[rng.randrange(1 << n)] = 1
        f, c = b.from_table(tf), b.from_table(tc)
        g = constrain(b, f, c)
        h = restrict(b, f, c)
        tg, th = b.table(g), b.table(h)
        care = [a for a in range(1 << n) if tc[a]]
        for a in care:
            assert tg[a] == tf[a] and th[a] == tf[a]
        for a in range(1 << n):  # constrain maps x to the nearest care point
            y = min(care, key=lambda z: distance(n, a, z))
            assert tg[a] == tf[y]
        assert support(n, th) <= support(n, tf)
        assert constrain(b, f, TRUE) == f and restrict(b, f, TRUE) == f
        checked += 1
        b.check_invariant()
    assert checked >= 500


def test_cube_gives_the_ordinary_cofactor() -> None:
    rng = random.Random(8)
    for _ in range(200):
        n = rng.randrange(1, 8)
        b = BDD(n)
        tf = random_table(rng, n)
        lits = {i: rng.randrange(2) for i in range(n) if rng.random() < 0.4}
        tc = [int(all((a >> i & 1) == v for i, v in lits.items())) for a in range(1 << n)]
        f, c = b.from_table(tf), b.from_table(tc)
        fixed = [a for a in range(1 << n)]
        for i, v in lits.items():
            fixed = [(a | 1 << i) if v else (a & ~(1 << i)) for a in fixed]
        cof = b.from_table([tf[a] for a in fixed])
        assert constrain(b, f, c) == cof
        assert restrict(b, f, c) == cof


def test_results_can_be_larger_than_f() -> None:
    rng = random.Random(1990)
    grew_c = grew_r = 0
    for _ in range(400):
        n = 5
        b = BDD(n)
        f = b.from_table(random_table(rng, n))
        tc = random_table(rng, n)
        if not any(tc):
            continue
        c = b.from_table(tc)
        grew_c += b.size(constrain(b, f, c)) > b.size(f)
        grew_r += b.size(restrict(b, f, c)) > b.size(f)
    assert grew_c > 0 and grew_r > 0


def test_small_examples() -> None:
    b = BDD(3)
    x0 = b.mk(0, FALSE, TRUE)
    x1 = b.mk(1, FALSE, TRUE)
    f = b.ite(x0, x1, FALSE)  # x0 AND x1
    assert constrain(b, f, x0) == x1
    assert constrain(b, f, f) == TRUE
    assert restrict(b, x1, x0) == x1
