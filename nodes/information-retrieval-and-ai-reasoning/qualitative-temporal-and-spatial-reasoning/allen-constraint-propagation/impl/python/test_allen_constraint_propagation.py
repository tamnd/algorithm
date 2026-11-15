# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/allen-constraint-propagation/. The authors are listed in prov/7P7E2R.jsonl.

import random
from collections import Counter
from itertools import combinations, permutations

from allen_constraint_propagation import AllenNetwork
from qcn import ALLEN_NAMES, allen, consistent, consistent_scenarios, label, network

IA = allen()


def rel(*names: str) -> int:
    return IA.rel(*names)


def reference(n, cons):
    """Path consistency by passes over all triples, from scratch."""
    net = network(IA, n, cons)
    r = {(i, j): label(IA, net, i, j) for i, j in permutations(range(n), 2)}
    changed = True
    while changed:
        changed = False
        for i, j, k in permutations(range(n), 3):
            t = r[(i, j)] & IA.compose(r[(i, k)], r[(k, j)])
            if t != r[(i, j)]:
                r[(i, j)], r[(j, i)] = t, IA.converse(t)
                changed = True
    if any(v == 0 for v in r.values()):
        return None
    return r


def labels_of(net: AllenNetwork):
    return {(i, j): net.label(i, j) for i, j in permutations(range(net.n), 2)}


def closed_scenarios(net: AllenNetwork):
    """Every atomic refinement of the labels in which each triangle obeys the table."""
    n = net.n
    pairs = list(combinations(range(n), 2))
    atoms: dict[tuple[int, int], int] = {}

    def get(i, j):
        return atoms[(i, j)] if i < j else IA.conv[atoms[(j, i)]]

    def ok(i, j) -> bool:
        for k in range(n):
            if k in (i, j):
                continue
            if (min(i, k), max(i, k)) in atoms and (min(k, j), max(k, j)) in atoms:
                if not IA.table[get(i, k)][get(k, j)] >> atoms[(i, j)] & 1:
                    return False
        return True

    def search(t):
        if t == len(pairs):
            yield dict(atoms)
            return
        i, j = pairs[t]
        for b in range(13):
            if net.label(i, j) >> b & 1:
                atoms[(i, j)] = b
                if ok(i, j):
                    yield from search(t + 1)
                del atoms[(i, j)]

    yield from search(0)


def random_label(rng, keep):
    r = 0
    while r == 0:
        r = sum(1 << b for b in range(13) if rng.random() < keep)
    return r


def ord_horn_relations() -> list[int]:
    """The ORD-Horn relations, computed from the clauses. Each base relation is
    turned into its endpoint order; a clause is a set of literals p != q with at
    most one literal p <= q, over the 4 endpoints x-, x+, y-, y+."""
    cfg = []
    for b in range(13):
        (a0, a1), (b0, b1) = IA.realize(2, {(0, 1): b})
        cfg.append((a0, a1, b0, b1))
    pts = range(4)
    negs = list(combinations(pts, 2))
    masks = set()
    for chosen in range(1 << len(negs)):
        neg = [negs[t] for t in range(len(negs)) if chosen >> t & 1]
        for pos in [None] + [(p, q) for p in pts for q in pts if p != q]:
            m = 0
            for b, c in enumerate(cfg):
                if any(c[p] != c[q] for p, q in neg) or (pos is not None and c[pos[0]] <= c[pos[1]]):
                    m |= 1 << b
            masks.add(m)
    out = []
    for r in range(1, 1 << 13):
        hull = IA.universal
        for m in masks:
            if r & m == r:
                hull &= m
        if hull == r:
            out.append(r)
    return out


def test_base_relations_and_table() -> None:
    assert IA.names == ALLEN_NAMES and IA.size == 13
    assert IA.identity == rel("eq")
    assert IA.conv == [12 - b for b in range(13)]
    sizes = Counter(bin(IA.table[a][b]).count("1") for a in range(13) for b in range(13))
    assert sum(sizes.values()) == 169
    assert sum(k * v for k, v in sizes.items()) == 409
    assert sizes == {1: 97, 3: 42, 5: 24, 9: 3, 13: 3}
    assert IA.table[IA.names.index("m")][IA.names.index("m")] == rel("b")
    assert IA.table[IA.names.index("d")][IA.names.index("d")] == rel("d")
    assert IA.table[IA.names.index("o")][IA.names.index("o")] == rel("b", "m", "o")


def test_example() -> None:
    net = AllenNetwork(4, IA)
    assert net.add(0, 1, rel("d"))
    assert net.add(1, 2, rel("b"))
    assert net.label(0, 2) == rel("b")
    assert net.add(2, 3, rel("o", "s"))
    assert net.label(0, 3) == rel("b") and net.label(1, 3) == rel("b")
    assert not net.add(0, 3, rel("bi"))
    assert not net.ok


def test_closed_but_inconsistent() -> None:
    cons = [(0, 1, rel("o", "si")), (0, 2, rel("fi", "si")), (0, 3, rel("o", "fi")),
            (1, 2, rel("m", "mi")), (1, 3, rel("b", "f")), (2, 3, rel("b", "s"))]
    net = AllenNetwork(4, IA)
    assert all(net.add(i, j, r) for i, j, r in cons)
    assert labels_of(net) == reference(4, cons)
    assert consistent(IA, 4, network(IA, 4, cons)) is None
    assert list(closed_scenarios(net)) == []


def test_edges() -> None:
    net = AllenNetwork(1, IA)
    assert net.label(0, 0) == rel("eq")
    net = AllenNetwork(3, IA)
    stats: dict = {}
    assert net.add(0, 1, IA.universal, stats) and stats == {}
    assert net.add(0, 1, rel("b", "m"), stats) and stats["pops"] == 1
    assert net.add(1, 0, rel("bi"))
    assert net.label(0, 1) == rel("b") and net.label(1, 0) == rel("bi")
    assert not net.add(0, 1, rel("eq"))
    assert not net.add(1, 2, IA.universal)


def test_against_naive_fixpoint() -> None:
    rng = random.Random(31)
    for _ in range(150):
        n = rng.randint(2, 6)
        net = AllenNetwork(n, IA)
        cons = []
        stats: dict = {}
        for _ in range(rng.randint(1, 12)):
            i, j = rng.sample(range(n), 2)
            cons.append((i, j, random_label(rng, 0.4)))
            ok = net.add(*cons[-1], stats)
            ref = reference(n, cons)
            assert ok == (ref is not None)
            if not ok:
                break
            assert labels_of(net) == ref
        assert stats.get("pops", 0) <= len(cons) + 12 * n * (n - 1) // 2


def test_scenarios_inside_and_realized() -> None:
    rng = random.Random(32)
    outcomes = Counter()
    for _ in range(120):
        n = rng.randint(3, 4)
        cons = [(i, j, random_label(rng, 0.2)) for i, j in combinations(range(n), 2)]
        net = AllenNetwork(n, IA)
        ok = all(net.add(i, j, r) for i, j, r in cons)
        real = {tuple(sorted(a.items())) for a, _ in consistent_scenarios(IA, n, network(IA, n, cons))}
        if not ok:
            assert real == set()
            outcomes["contradiction"] += 1
            continue
        kept = set()
        for atoms in closed_scenarios(net):
            vals = IA.realize(n, atoms)
            assert vals is not None  # integer endpoints
            assert all(vals[i][0] < vals[i][1] for i in range(n))
            assert all(IA.base_of(vals[i], vals[j]) == b for (i, j), b in atoms.items())
            kept.add(tuple(sorted(atoms.items())))
        assert kept == real
        outcomes["consistent" if real else "closed but inconsistent"] += 1
    assert outcomes["contradiction"] > 10 and outcomes["consistent"] > 10


def test_ord_horn_networks_are_decided() -> None:
    horn = ord_horn_relations()
    assert len(horn) == 867
    # The closed but inconsistent network uses 5 labels that are not ORD-Horn.
    assert [rel(*s.split()) in horn for s in ("o si", "fi si", "o fi", "m mi", "b f", "b s")] == [
        False, False, True, False, False, False]
    small = [r for r in horn if bin(r).count("1") <= 4]
    rng = random.Random(33)
    seen = Counter()
    for _ in range(300):
        n = rng.randint(3, 4)
        net = AllenNetwork(n, IA)
        cons = [(i, j, rng.choice(small)) for i, j in combinations(range(n), 2) if rng.random() < 0.9]
        ok = all(net.add(i, j, r) for i, j, r in cons)
        assert ok == (consistent(IA, n, network(IA, n, cons)) is not None)
        seen[ok] += 1
    assert min(seen.values()) > 60
