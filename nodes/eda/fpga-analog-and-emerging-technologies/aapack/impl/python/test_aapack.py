# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aapack/. The authors are listed in prov/11GQMP.jsonl.

import itertools
import random
from fractions import Fraction

from aapack import Ble, Block, aapack, check_config, external_inputs, fits_by_count, route_cluster


def pins(*ps):
    return [("pin", p) for p in ps]


def fbs(*ts):
    return [("fb", t) for t in ts]


def sparse_block() -> Block:
    """The block of the page: N = 2, K = 2, I = 3, a flip-flop in slot 0 only, two sources per LUT input."""
    return Block(
        [True, False],
        3,
        2,
        [
            [frozenset(pins(0) + fbs(1)), frozenset(pins(1) + fbs(0))],
            [frozenset(pins(2) + fbs(0)), frozenset(pins(1) + fbs(1))],
        ],
    )


def full_block(n: int, k: int, i: int) -> Block:
    every = frozenset(pins(*range(i)) + fbs(*range(n)))
    return Block([True] * n, i, k, [[every] * k for _ in range(n)])


def random_block(rng: random.Random) -> Block:
    n, k = rng.randint(1, 3), rng.randint(1, 2)
    i = rng.randint(k, k + 2)
    sources = pins(*range(i)) + fbs(*range(n))
    conn = [[frozenset(rng.sample(sources, rng.randint(1, len(sources)))) for _ in range(k)] for _ in range(n)]
    return Block([rng.random() < 0.7 for _ in range(n)], i, k, conn)


def random_netlist(rng: random.Random, n: int, k: int) -> list[Ble]:
    bles = []
    for v in range(n):
        pool = ["x", "y", "z", "w"][: rng.randint(1, 4)] + [f"o{j}" for j in range(v)]
        size = rng.randint(1, min(k, len(pool)))
        bles.append(Ble(tuple(sorted(rng.sample(pool, size))), f"o{v}", rng.random() < 0.25))
    return bles


def brute_routable(bles: list[Ble], block: Block, slot_of: dict[int, int]) -> bool:
    """Try every pin assignment and every order of LUT inputs: no matching, no pruning."""
    members = list(slot_of)
    if len(set(slot_of.values())) != len(members):
        return False
    if any(bles[i].registered and not block.has_ff[s] for i, s in slot_of.items()):
        return False
    driver = {bles[i].output: slot_of[i] for i in members}
    ext = external_inputs(bles, members)
    for perm in itertools.permutations(range(block.i_pins), len(ext)):
        pin_of = dict(zip(ext, perm))
        ok = True
        for i in members:
            nets = sorted(set(bles[i].inputs))
            src = [("fb", driver[x]) if x in driver else ("pin", pin_of[x]) for x in nets]
            if not any(
                all(src[t] in block.conn[slot_of[i]][js[t]] for t in range(len(nets)))
                for js in itertools.permutations(range(block.k), len(nets))
            ):
                ok = False
                break
        if ok:
            return True
    return False


def brute_legal(bles: list[Ble], block: Block, members: list[int]) -> bool:
    return any(
        brute_routable(bles, block, dict(zip(members, perm)))
        for perm in itertools.permutations(range(block.n_slots), len(members))
    )


def brute_min_blocks(bles: list[Ble], block: Block) -> int:
    n = len(bles)
    legal = [False] * (1 << n)
    for mask in range(1, 1 << n):
        members = [i for i in range(n) if mask >> i & 1]
        legal[mask] = len(members) <= block.n_slots and brute_legal(bles, block, members)
    best = [0] + [n + 1] * ((1 << n) - 1)
    for mask in range(1, 1 << n):
        low = mask & -mask
        sub = mask
        while sub:
            if sub & low and legal[sub]:
                best[mask] = min(best[mask], best[mask ^ sub] + 1)
            sub = (sub - 1) & mask
    return best[-1]


def assert_partition(bles, result):
    seen = sorted(i for cfg in result for i in cfg.slot_of)
    assert seen == list(range(len(bles)))


def test_counts_fit_but_route_fails():
    block = sparse_block()
    bles = [Ble(("x", "y"), "o0"), Ble(("x", "y"), "o1")]
    assert len(external_inputs(bles, [0, 1])) == 2
    assert fits_by_count(bles, block, {0: 0, 1: 1})
    assert route_cluster(bles, block, {0: 0, 1: 1}) is None
    assert route_cluster(bles, block, {0: 1, 1: 0}) is None
    assert not brute_legal(bles, block, [0, 1])
    result = aapack(bles, block)
    assert len(result) == 2
    # Speculative packing puts both in one block, the final route fails, and the block is redone.
    assert len(aapack(bles, block, speculative=True)) == 2


def test_slot_choice_example():
    block = sparse_block()
    bles = [Ble(("x", "y"), "o0"), Ble(("w", "x"), "o1", True)]
    result = aapack(bles, block)
    assert [cfg.slot_of for cfg in result] == [{0: 0}, {1: 0}]
    assert brute_min_blocks(bles, block) == 1
    cfg = route_cluster(bles, block, {0: 1, 1: 0})
    assert cfg is not None and check_config(bles, block, cfg)


def test_route_cluster_matches_brute_force():
    rng = random.Random(5)
    agree = [0, 0]
    for _ in range(400):
        block = random_block(rng)
        bles = random_netlist(rng, rng.randint(1, 3), block.k)
        m = rng.randint(1, min(len(bles), block.n_slots))
        members = rng.sample(range(len(bles)), m)
        slots = rng.sample(range(block.n_slots), m)
        slot_of = dict(zip(members, slots))
        cfg = route_cluster(bles, block, slot_of) if fits_by_count(bles, block, slot_of) else None
        want = brute_routable(bles, block, slot_of) and all(len(set(bles[i].inputs)) <= block.k for i in members)
        assert (cfg is not None) == want
        if cfg is not None:
            assert check_config(bles, block, cfg)
        agree[want] += 1
    assert min(agree) > 20  # both outcomes occur


def test_full_crossbar_route_iff_counts():
    rng = random.Random(8)
    for _ in range(300):
        n, k = rng.randint(1, 3), rng.randint(1, 3)
        i = rng.randint(k, k + 2)
        block = full_block(n, k, i)
        bles = [b for b in random_netlist(rng, rng.randint(1, n), k)]
        slot_of = {v: v for v in range(len(bles))}
        routed = route_cluster(bles, block, slot_of) is not None
        assert routed == (len(external_inputs(bles, slot_of)) <= i)


def test_legal_and_never_below_optimum():
    rng = random.Random(1)
    worse = 0
    for t in range(500):
        block = sparse_block() if t % 2 == 0 else random_block(rng)
        bles = random_netlist(rng, rng.randint(1, 5), block.k)
        if not all(brute_legal(bles, block, [v]) for v in range(len(bles))):
            continue  # some BLE fits in no slot of an empty block
        best = brute_min_blocks(bles, block)
        for speculative in (False, True):
            result = aapack(bles, block, speculative=speculative)
            assert_partition(bles, result)
            assert all(check_config(bles, block, cfg) for cfg in result)
            assert len(result) >= best
            worse += len(result) > best
    assert worse > 0


def test_closed_blocks_are_maximal():
    rng = random.Random(3)
    for _ in range(150):
        block = random_block(rng)
        bles = random_netlist(rng, rng.randint(1, 5), block.k)
        try:
            result = aapack(bles, block)
        except ValueError:
            continue
        later = set(range(len(bles)))
        for cfg in result:
            later -= set(cfg.slot_of)
            free = [s for s in range(block.n_slots) if s not in cfg.slot_of.values()]
            for b in later:
                for s in free:
                    assert not brute_routable(bles, block, {**cfg.slot_of, b: s})


def test_timing_weight_and_full_crossbar_speculation():
    rng = random.Random(12)
    for _ in range(100):
        block = full_block(3, 2, 4)
        bles = random_netlist(rng, rng.randint(1, 6), 2)
        crit = {(u, v): Fraction(rng.randint(1, 4), 4) for v, b in enumerate(bles) for u in range(v) if f"o{u}" in b.inputs}
        a = aapack(bles, block, lam=Fraction(3, 4), crit=crit)
        b = aapack(bles, block, lam=Fraction(3, 4), crit=crit, speculative=True)
        assert [c.slot_of for c in a] == [c.slot_of for c in b]
        assert all(check_config(bles, block, cfg) for cfg in a)
