# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimistic-concurrency-control/. The authors are listed in prov/8MJ6N3.jsonl.

import random
from itertools import permutations

from optimistic_concurrency_control import Occ

ITEMS = ["x", "y", "z", "u"]


def programs(rng: random.Random, n: int) -> dict[int, list[tuple]]:
    out = {}
    for t in range(1, n + 1):
        ops = [(rng.choice("rw"), rng.choice(ITEMS)) for _ in range(rng.randrange(1, 5))]
        out[t] = ops
    return out


def run(seed: int, parallel: bool, n: int = 5) -> Occ:
    """Interleave the read phases (and, for parallel validation, the steps of
    validation and of the write phases) at random. A transaction that fails
    validation is restarted once with a new number; then it gives up."""
    rng = random.Random(seed)
    occ = Occ({x: 0 for x in ITEMS})
    progs = programs(rng, n)
    todo = {t: list(p) for t, p in progs.items()}
    stage, tries, nxt = {}, {}, 100
    for t in todo:
        occ.begin(t)
        stage[t] = "read"
    while todo:
        t = rng.choice(sorted(todo))
        s = stage[t]
        if s == "read" and todo[t]:
            k, x = todo[t].pop(0)
            if k == "r":
                occ.read(t, x)
            else:
                occ.write(t, x, (t, x))
            continue
        if s == "read" and not parallel:
            ok = occ.serial_commit(t)
            stage[t] = "done" if ok else "failed"
        elif s == "read":
            occ.enter_validation(t)
            stage[t] = "validate"
        elif s == "validate":
            ok = occ.validate(t)
            stage[t] = "writing" if ok else "failed"
            todo[t] = sorted(occ.ws[t]) if ok else []
        elif s == "writing" and todo[t]:
            occ.write_one(t, todo[t].pop(0))
        elif s == "writing":
            occ.finish_commit(t)
            stage[t] = "done"
        if stage[t] == "failed":
            del todo[t]
            if tries.get(t, 0) < 1:  # restart as a new transaction
                nxt += 1
                tries[nxt] = tries.get(t, 0) + 1
                todo[nxt] = list(progs[t])
                occ.begin(nxt)
                stage[nxt] = "read"
        elif stage[t] == "done":
            del todo[t]
    return occ


def conflict_pairs(occ: Occ) -> list[tuple[int, int]]:
    com = set(occ.tn)
    ops = [o for o in occ.ops if o[1] in com]
    return [(a[1], b[1]) for i, a in enumerate(ops) for b in ops[i + 1:]
            if a[1] != b[1] and a[2] == b[2] and "w" in (a[0], b[0])]


def equivalent(order, pairs) -> bool:
    pos = {t: i for i, t in enumerate(order)}
    return all(pos[a] < pos[b] for a, b in pairs)


def serial_orders(occ: Occ) -> list[tuple]:
    pairs = conflict_pairs(occ)
    return [p for p in permutations(sorted(occ.tn)) if equivalent(p, pairs)]


def test_serial_validation_is_serializable_in_tn_order() -> None:
    commits = aborts = 0
    for seed in range(400):
        occ = run(seed, parallel=False)
        by_tn = tuple(sorted(occ.tn, key=occ.tn.get))
        assert by_tn in serial_orders(occ), seed  # brute force over all orders
        commits += len(occ.tn)
        aborts += len(occ.start) - len(occ.tn)
    assert commits > 1000 and aborts > 50


def test_parallel_validation_is_serializable() -> None:
    differ = 0
    for seed in range(400):
        occ = run(seed, parallel=True)
        orders = serial_orders(occ)
        assert orders, seed
        by_entry = tuple(sorted(occ.tn, key=occ.entered.get))
        assert by_entry in orders, seed
        by_tn = tuple(sorted(occ.tn, key=occ.tn.get))
        differ += by_tn not in orders
    assert differ > 0  # the order of the numbers is not always a serial order


def test_backward_validation_conditions() -> None:
    # T1 reads x; T2 writes x and commits during the read phase of T1: T1 fails.
    occ = Occ({"x": 0, "y": 0})
    occ.begin(1)
    occ.begin(2)
    occ.read(1, "x")
    occ.write(2, "x", 5)
    assert occ.serial_commit(2) and occ.tn[2] == 1
    assert not occ.serial_commit(1)
    # T3 starts after T2 has its number: condition (1), no check needed.
    occ.begin(3)
    occ.read(3, "x")
    assert occ.serial_commit(3)
    # Disjoint sets: condition (2) holds, T4 commits although T5 committed first.
    occ.begin(4)
    occ.begin(5)
    occ.read(4, "y")
    occ.write(5, "x", 7)
    assert occ.serial_commit(5) and occ.serial_commit(4)


def test_parallel_numbers_differ_from_serial_order() -> None:
    # U reads x and enters validation; T writes x, validates against U (no
    # overlap with U's write set) and finishes first, so tn(T) < tn(U) though
    # U read x before T wrote it. The equivalent order is U, T.
    occ = Occ({"x": 0, "y": 0})
    occ.begin(1)  # U
    occ.begin(2)  # T
    occ.read(1, "x")
    occ.write(1, "y", 1)
    occ.enter_validation(1)
    occ.write(2, "x", 2)
    occ.enter_validation(2)
    assert occ.validate(2)
    occ.write_one(2, "x")
    occ.finish_commit(2)
    assert occ.validate(1)
    occ.write_one(1, "y")
    occ.finish_commit(1)
    assert occ.tn == {2: 1, 1: 2}
    assert serial_orders(occ) == [(1, 2)]
