# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-ordered-bdd/. The authors are listed in prov/4A6P2D.jsonl.

import random

from reduced_ordered_bdd import AND, FALSE, OR, TRUE, XOR, BDD


def bits(a: int, n: int) -> list[int]:
    return [(a >> j) & 1 for j in range(n)]


def random_table(rng: random.Random, n: int) -> list[int]:
    return [rng.randrange(2) for _ in range(1 << n)]


def test_example() -> None:
    # f = (x0 AND x1) OR x2, the example of the page.
    b = BDD(3)
    t = [((a & 1) & (a >> 1 & 1)) | (a >> 2 & 1) for a in range(8)]
    f = b.build(t)
    assert b.size(f) == 5
    assert b.satcount(f) == 5
    assert b.truth_table(f) == t
    b.check_invariants()


def test_operator_tables() -> None:
    names = {"AND": lambda a, c: a & c, "OR": lambda a, c: a | c, "XOR": lambda a, c: a ^ c, "NAND": lambda a, c: 1 - (a & c), "NOR": lambda a, c: 1 - (a | c), "XNOR": lambda a, c: 1 - (a ^ c), "IMPLIES": lambda a, c: (1 - a) | c}
    import reduced_ordered_bdd as m

    b = BDD(0)
    for name, fn in names.items():
        for a in (0, 1):
            for c in (0, 1):
                assert b.apply(getattr(m, name), a, c) == fn(a, c), name


def test_edges() -> None:
    b = BDD(0)
    assert b.build([0]) == FALSE and b.build([1]) == TRUE
    b = BDD(4)
    assert b.build([0] * 16) == FALSE
    assert b.build([1] * 16) == TRUE
    x2 = b.ithvar(2)
    assert b.build([a >> 2 & 1 for a in range(16)]) == x2
    assert b.size(x2) == 3


def test_build_round_trip_and_invariants() -> None:
    rng = random.Random(4)
    for n in range(1, 11):
        b = BDD(n)
        for _ in range(4):
            t = random_table(rng, n)
            assert b.truth_table(b.build(t)) == t
        b.check_invariants()


def test_canonicity_two_construction_orders() -> None:
    rng = random.Random(1986)
    for n in range(1, 9):
        b = BDD(n)
        for _ in range(5):
            t = random_table(rng, n)
            f = b.build(t)
            ones = [a for a in range(1 << n) if t[a]]
            # Construction 2: OR of minterms, in a random order.
            rng.shuffle(ones)
            g = FALSE
            for a in ones:
                m = TRUE
                for j in reversed(range(n)):
                    lit = b.ithvar(j) if a >> j & 1 else b.neg(b.ithvar(j))
                    m = b.apply(AND, m, lit)
                g = b.apply(OR, g, m)
            assert g == f
            # Construction 3: Shannon expansion on x_0 with ITE.
            t0 = [t[a] for a in range(1 << n) if not a & 1]
            t1 = [t[a] for a in range(1 << n) if a & 1]
            c = BDD(n - 1)
            f0, f1 = c.build(t0), c.build(t1)
            assert c.truth_table(f0) == t0 and c.truth_table(f1) == t1
            h = b.ite(b.ithvar(0), b.restrict(f, 0, 1), b.restrict(f, 0, 0))
            assert h == f
        b.check_invariants()


def test_equal_functions_iff_equal_nodes() -> None:
    rng = random.Random(7)
    n = 4
    b = BDD(n)
    seen: dict[tuple[int, ...], int] = {}
    for _ in range(400):
        t = tuple(random_table(rng, n))
        f = b.build(list(t))
        if t in seen:
            assert seen[t] == f
        else:
            assert f not in seen.values()
            seen[t] = f


def test_operations_against_truth_tables() -> None:
    rng = random.Random(10)
    for n in range(1, 11):
        b = BDD(n)
        for _ in range(3):
            tf, tg, th = (random_table(rng, n) for _ in range(3))
            f, g, h = b.build(tf), b.build(tg), b.build(th)
            for op in range(16):
                want = [(op >> (2 * x + y)) & 1 for x, y in zip(tf, tg)]
                assert b.truth_table(b.apply(op, f, g)) == want
            want = [y if x else z for x, y, z in zip(tf, tg, th)]
            assert b.truth_table(b.ite(f, g, h)) == want
            i = rng.randrange(n)
            for v in (0, 1):
                want = [tf[(a & ~(1 << i)) | (v << i)] for a in range(1 << n)]
                assert b.truth_table(b.restrict(f, i, v)) == want
            xs = set(rng.sample(range(n), rng.randint(1, n)))
            ex, fa = list(tf), list(tf)
            for j in xs:
                ex = [ex[a] | ex[a ^ (1 << j)] for a in range(1 << n)]
                fa = [fa[a] & fa[a ^ (1 << j)] for a in range(1 << n)]
            assert b.truth_table(b.exists(f, xs)) == ex
            assert b.truth_table(b.forall(f, xs)) == fa
            want = [tf[(a & ~(1 << i)) | (tg[a] << i)] for a in range(1 << n)]
            assert b.truth_table(b.compose(f, i, g)) == want
            assert b.satcount(f) == sum(tf)
            assert b.truth_table(b.apply(XOR, f, b.neg(f))) == [1] * (1 << n)
        b.check_invariants()


def test_satcount_skipped_levels() -> None:
    b = BDD(10)
    assert b.satcount(TRUE) == 1024 and b.satcount(FALSE) == 0
    assert b.satcount(b.ithvar(9)) == 512
    assert b.satcount(b.apply(AND, b.ithvar(0), b.ithvar(9))) == 256
    assert b.satcount(b.apply(OR, b.ithvar(3), b.ithvar(6))) == 768
