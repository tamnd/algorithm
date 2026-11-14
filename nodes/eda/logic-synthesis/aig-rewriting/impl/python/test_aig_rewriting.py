# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aig-rewriting/. The authors are listed in prov/CJJRNE.jsonl.

import random

from aig_rewriting import FULL3, LIBRARY, NPN, VAR3, Aig, npn_transform, rewrite


def structure_table(gates: list[tuple[int, int]], root: int) -> int:
    val = {0: 0, 1: FULL3}
    for j in range(3):
        val[2 * (j + 1)] = VAR3[j]
        val[2 * (j + 1) + 1] = VAR3[j] ^ FULL3
    for i, (a, b) in enumerate(gates):
        v = val[a] & val[b]
        val[2 * (4 + i)] = v
        val[2 * (4 + i) + 1] = v ^ FULL3
    return val[root]


def min_sizes_by_search(limit: int) -> dict[int, int]:
    """The least number of AND nodes for every 3-input function, by breadth-first search up to limit."""
    cost = {0: 0, FULL3: 0}
    for t in VAR3:
        cost[t] = 0
        cost[t ^ FULL3] = 0
    level = {()}
    for k in range(1, limit + 1):
        nxt = set()
        for st in level:
            sig = list(VAR3) + list(st)
            have = set(sig) | {s ^ FULL3 for s in sig} | {0, FULL3}
            for i in range(len(sig)):
                for j in range(i + 1, len(sig)):
                    for pa in (0, FULL3):
                        for pb in (0, FULL3):
                            x = (sig[i] ^ pa) & (sig[j] ^ pb)
                            if x not in have:
                                nxt.add(tuple(sorted(st + (x,))))
        level = nxt
        for st in level:
            for x in st:
                for y in (x, x ^ FULL3):
                    cost.setdefault(y, k)
    return cost


def test_npn_classes() -> None:
    assert len(set(c for c, _, _, _ in NPN.values())) == 14
    assert sorted(LIBRARY) == sorted(set(c for c, _, _, _ in NPN.values()))
    for t, (c, perm, neg, out) in NPN.items():
        assert npn_transform(t, perm, neg, out) == c


def test_library_is_right_and_smallest() -> None:
    cost = min_sizes_by_search(5)
    for c, (gates, root) in LIBRARY.items():
        assert structure_table(gates, root) == c
        if len(gates) <= 5:
            assert cost[c] == len(gates)
        else:
            assert c not in cost  # no AIG of 5 or fewer nodes exists
    assert max(len(g) for g, _ in LIBRARY.values()) == 6


def example() -> Aig:
    g = Aig(3)
    ab = g.and_(2, 4)
    ac = g.and_(2, 6)
    o = g.and_(ab ^ 1, ac ^ 1) ^ 1  # ab + ac
    g.outputs = [o]
    return g


def test_example_saves_one_node() -> None:
    g = example()
    table = g.simulate()
    assert g.num_ands() == 3
    log = rewrite(g)
    assert g.simulate() == table == [0b11100000]
    assert g.num_ands() == 2
    assert log == [(1, 3, 2)]


def test_example_with_shared_node_is_kept() -> None:
    g = example()
    g.outputs.append(g.and_(2, 4))  # a & b is also an output
    table = g.simulate()
    log = rewrite(g)
    assert log == []
    assert g.num_ands() == 3 and g.simulate() == table


def test_redundant_logic_is_removed() -> None:
    g = Aig(3)
    x = g.and_(2, 4)
    y = g.and_(x, g.and_(2, 6))  # a & b & c with a twice
    z = g.and_(y ^ 1, x ^ 1) ^ 1  # (abc) + (ab) = ab
    g.outputs = [z]
    table = g.simulate()
    rewrite(g)
    assert g.simulate() == table
    assert g.num_ands() == 1


def check_invariants(g: Aig) -> None:
    live = g.live_ands()
    pos = {v: i for i, v in enumerate(live)}
    keys = set()
    for v in live:
        a, b = g.fanin0[v], g.fanin1[v]
        assert g.alive[v] and 2 <= a < b and a != b ^ 1
        assert g.table[(a, b)] == v
        keys.add((a, b))
        for x in (a, b):
            if g.is_and(x >> 1):
                assert pos[x >> 1] < pos[v]
    assert len(keys) == len(live)


def random_aig(rng: random.Random) -> Aig:
    n = rng.randrange(3, 7)
    g = Aig(n)
    lits = [2 * i for i in range(1, n + 1)]
    for _ in range(rng.randrange(4, 35)):
        a = lits[-1] if rng.random() < 0.4 else rng.choice(lits)
        x = g.and_(a ^ rng.randrange(2), rng.choice(lits) ^ rng.randrange(2))
        if x > 1:
            lits.append(x)
    g.outputs = [rng.choice(lits[n:] or lits) ^ rng.randrange(2) for _ in range(rng.randrange(1, 4))]
    return g


def test_random_aigs_keep_function_and_shrink() -> None:
    rng = random.Random(31)
    changed = 0
    for _ in range(500):
        g = random_aig(rng)
        g.collect_garbage()
        table = g.simulate()
        size = g.num_ands()
        log = rewrite(g)
        assert g.simulate() == table
        assert g.num_ands() <= size
        for gain, before, after in log:
            assert gain > 0 and after <= before - gain
        check_invariants(g)
        changed += bool(log)
    assert changed > 100
