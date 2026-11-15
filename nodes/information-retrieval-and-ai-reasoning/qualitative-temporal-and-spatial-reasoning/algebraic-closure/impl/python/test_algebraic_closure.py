# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-closure/. The authors are listed in prov/DTG755.jsonl.

import random
from collections import Counter
from itertools import combinations, permutations

from algebraic_closure import algebraic_closure
from qcn import allen, consistent, label, minimal_network, network, point_algebra

PA = point_algebra()
IA = allen()


def closed(calc, n, net) -> bool:
    for i, j, k in permutations(range(n), 3):
        rij = label(calc, net, i, j)
        if rij & ~calc.compose(label(calc, net, i, k), label(calc, net, k, j)):
            return False
    return True


def reference(calc, n, net):
    """Revise every triple in passes until a pass changes nothing."""
    r = {(i, j): label(calc, net, i, j) for i, j in permutations(range(n), 2)}
    changed = True
    while changed:
        changed = False
        for i, j, k in permutations(range(n), 3):
            t = r[(i, j)] & calc.compose(r[(i, k)], r[(k, j)])
            if t != r[(i, j)]:
                r[(i, j)], r[(j, i)] = t, calc.converse(t)
                changed = True
    if any(v == 0 for v in r.values()):
        return None
    return {(i, j): r[(i, j)] for i, j in combinations(range(n), 2)}


def random_network(rng, calc, n, keep, density=0.7):
    cons = []
    for i, j in combinations(range(n), 2):
        if rng.random() < density:
            r = 0
            while r == 0:
                r = sum(1 << b for b in range(calc.size) if rng.random() < keep)
            cons.append((i, j, r))
    return network(calc, n, cons)


def test_point_algebra_table() -> None:
    lt, eq, gt = PA.rel("<"), PA.rel("="), PA.rel(">")
    assert PA.size == 3 and PA.identity == eq
    assert [[PA.table[a][b] for b in range(3)] for a in range(3)] == [
        [lt, lt, PA.universal], [lt, eq, gt], [PA.universal, gt, gt]]


def test_allen_table() -> None:
    assert IA.size == 13 and IA.identity == IA.rel("eq")
    assert sum(len(row) for row in IA.table) == 169
    assert IA.conv == [12 - b for b in range(13)]
    sizes = Counter(bin(IA.table[a][b]).count("1") for a in range(13) for b in range(13))
    assert sizes == {1: 97, 3: 42, 5: 24, 9: 3, 13: 3}
    assert sum(k * v for k, v in sizes.items()) == 409

    def comp(x, y):
        return set(IA.names_of(IA.table[IA.names.index(x)][IA.names.index(y)]))

    assert comp("m", "m") == {"b"} and comp("d", "d") == {"d"} and comp("s", "f") == {"d"}
    assert comp("o", "o") == {"b", "m", "o"} and comp("o", "d") == {"o", "s", "d"}
    assert comp("m", "mi") == {"f", "eq", "fi"} and comp("b", "d") == {"b", "m", "o", "s", "d"}
    full = {(x, y) for x in IA.names for y in IA.names if len(comp(x, y)) == 13}
    assert full == {("b", "bi"), ("bi", "b"), ("d", "di")}
    for a in range(13):  # the converse rule and associativity on base relations
        for b in range(13):
            assert IA.converse(IA.table[a][b]) == IA.table[IA.conv[b]][IA.conv[a]]
            for c in range(13):
                assert IA.compose(IA.table[a][b], 1 << c) == IA.compose(1 << a, IA.table[b][c])


def test_example_chain() -> None:
    net = network(IA, 4, [(0, 1, IA.rel("b", "m")), (1, 2, IA.rel("b", "m")),
                          (2, 3, IA.rel("d")), (0, 3, IA.rel("o", "di", "bi"))])
    out = algebraic_closure(IA, 4, net)
    assert out[(0, 2)] == IA.rel("b")
    assert out[(0, 3)] == IA.rel("o")
    assert out == reference(IA, 4, net)


def test_closed_but_inconsistent() -> None:
    net = network(IA, 4, [(0, 1, IA.rel("o", "si")), (0, 2, IA.rel("fi", "si")),
                          (0, 3, IA.rel("o", "fi")), (1, 2, IA.rel("m", "mi")),
                          (1, 3, IA.rel("b", "f")), (2, 3, IA.rel("b", "s"))])
    assert algebraic_closure(IA, 4, net) == net
    assert consistent(IA, 4, net) is None


def test_edges() -> None:
    assert algebraic_closure(IA, 0, {}) == {}
    assert algebraic_closure(IA, 1, {}) == {}
    assert algebraic_closure(IA, 2, {(0, 1): 0}) is None
    assert algebraic_closure(PA, 2, {}) == {(0, 1): PA.universal}
    lt = PA.rel("<")
    assert algebraic_closure(PA, 3, network(PA, 3, [(0, 1, lt), (1, 2, lt), (2, 0, lt)])) is None
    net = {(0, 1): PA.rel("<", "=")}
    algebraic_closure(PA, 3, net)
    assert net == {(0, 1): PA.rel("<", "=")}  # the input is not changed


def check_against_brute_force(calc, n, net) -> bool:
    stats: dict[str, int] = {}
    out = algebraic_closure(calc, n, net, stats)
    assert stats["pops"] <= n * (n - 1) // 2 * (1 + calc.size)
    assert out == reference(calc, n, net)
    minimal = minimal_network(calc, n, net)
    if out is None:
        assert all(v == 0 for v in minimal.values()) and n >= 2
        return False
    assert closed(calc, n, out)
    for p, r in out.items():  # sound: no base relation of a solution is removed
        assert r & net[p] == r
        assert minimal[p] & ~r == 0
    return consistent(calc, n, out) is not None


def test_point_algebra_against_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(400):
        n = rng.randint(2, 5)
        net = random_network(rng, PA, n, 0.5)
        ok = check_against_brute_force(PA, n, net)
        # composition in the point algebra is strong, and closure decides consistency
        assert ok == (algebraic_closure(PA, n, net) is not None)


def test_allen_against_brute_force() -> None:
    rng = random.Random(12)
    for _ in range(250):
        n = rng.randint(2, 4)
        check_against_brute_force(IA, n, random_network(rng, IA, n, 0.3, 1.0))


def test_allen_atomic_networks_are_decided() -> None:
    rng = random.Random(13)
    for _ in range(300):
        n = rng.randint(3, 5)
        net = {p: 1 << rng.randrange(13) for p in combinations(range(n), 2)}
        out = algebraic_closure(IA, n, net)
        assert (out is not None) == (consistent(IA, n, net) is not None)
        assert out is None or out == net
