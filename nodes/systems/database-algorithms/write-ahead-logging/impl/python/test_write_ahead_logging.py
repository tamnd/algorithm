# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-ahead-logging/. The authors are listed in prov/MBX83W.jsonl.

import random

from write_ahead_logging import WalSystem, recover

ITEMS = ["a", "b", "c", "d"]


def fresh_disk() -> dict[str, tuple[int, int]]:
    return {x: (100 * (i + 1), 0) for i, x in enumerate(ITEMS)}


def make_workload(rng: random.Random, steps: int, first_txn: int = 1) -> list[tuple]:
    """A random strict workload: an item written by a running transaction is
    not written by another one until the writer ends."""
    ops: list[tuple] = []
    active: dict[int, set[str]] = {}
    nxt, val = first_txn, 1000 * first_txn
    for _ in range(steps):
        c = rng.random()
        if c < 0.15 and len(active) < 3:
            active[nxt] = set()
            nxt += 1
            continue
        if not active:
            continue
        t = rng.choice(sorted(active))
        if c < 0.55:
            locked = set().union(*(s for u, s in active.items() if u != t))
            free = [x for x in ITEMS if x not in locked]
            if free:
                x = rng.choice(free)
                val += 1
                active[t].add(x)
                ops.append(("update", t, x, val))
        elif c < 0.68:
            ops.append(("commit", t))
            del active[t]
        elif c < 0.75:
            ops.append(("abort", t))
            del active[t]
        elif c < 0.9:
            ops.append(("flush_page",))
        else:
            ops.append(("flush_log",))
    return ops


def apply(sys_: WalSystem, op: tuple) -> None:
    if op[0] == "update":
        sys_.update(op[1], op[2], op[3])
    elif op[0] == "commit":
        sys_.commit(op[1])
    elif op[0] == "abort":
        sys_.abort(op[1])
    elif op[0] == "flush_page":
        if sys_.buffer:
            sys_.flush_page(sorted(sys_.buffer)[0])
    else:
        sys_.flush_log(sys_.next_lsn)


def expected(start: dict[str, int], ops: list[tuple], committed: set[int]) -> dict[str, int]:
    """Reference: the last write of each item by a committed transaction."""
    state = dict(start)
    for op in ops:
        if op[0] == "update" and op[1] in committed:
            state[op[2]] = op[3]
    return state


def run_prefix(disk, log, ops, k, **flags):
    s = WalSystem(disk, log, **flags)
    for op in ops[:k]:
        apply(s, op)
    d, lg = s.crash()
    return s, d, lg


def check_all_crash_points(seed: int, steps: int, **flags) -> list[str]:
    rng = random.Random(seed)
    ops = make_workload(rng, steps)
    start = {x: v for x, (v, _) in fresh_disk().items()}
    errors = []
    for k in range(len(ops) + 1):
        s, d, lg = run_prefix(fresh_disk(), [], ops, k, **flags)
        committed = {r.txn for r in lg if r.kind == "commit"}
        if not s.acked <= committed:
            errors.append(f"k={k}: acked {s.acked - committed} lost")
        want = expected(start, ops[:k], committed)
        d2, lg2 = recover(d, lg)
        if {x: v for x, (v, _) in d2.items()} != want:
            errors.append(f"k={k}: wrong state")
    return errors


def test_crash_at_every_step() -> None:
    for seed in range(60):
        assert check_all_crash_points(seed, 100) == []


def test_crash_during_recovery_and_second_epoch() -> None:
    rng = random.Random(7)
    for seed in range(40):
        ops = make_workload(random.Random(seed), 60)
        start = {x: v for x, (v, _) in fresh_disk().items()}
        for k in range(0, len(ops) + 1, 3):
            _, d, lg = run_prefix(fresh_disk(), [], ops, k)
            committed = {r.txn for r in lg if r.kind == "commit"}
            want = expected(start, ops[:k], committed)
            for stop in range(6):
                d1, lg1 = recover(d, lg, stop_after=stop)
                d2, lg2 = recover(d1, lg1)
                assert {x: v for x, (v, _) in d2.items()} == want
                d3, lg3 = recover(d2, lg2)
                assert d3 == d2
            # a second run of work after recovery, then another crash
            ops2 = make_workload(rng, 25, first_txn=100)
            for j in range(len(ops2) + 1):
                s, e, elog = run_prefix(d2, lg2, ops2, j)
                c2 = {r.txn for r in elog if r.kind == "commit"}
                want2 = expected(want, ops2[:j], c2)
                e2, _ = recover(e, elog)
                assert {x: v for x, (v, _) in e2.items()} == want2


def test_hand_example() -> None:
    s = WalSystem({"A": (100, 0), "B": (50, 0)})
    s.update(1, "A", 70)
    s.update(2, "B", 80)
    s.commit(2)
    s.flush_page("A")
    d, lg = s.crash()
    assert d == {"A": (70, 1), "B": (50, 0)}
    assert [(r.lsn, r.kind, r.txn) for r in lg] == [(1, "update", 1), (2, "update", 2), (3, "commit", 2)]
    d2, lg2 = recover(d, lg)
    assert d2 == {"A": (100, 1), "B": (80, 2)}
    assert lg2[-1].kind == "abort" and lg2[-1].txn == 1


def test_dropping_the_wal_rule_breaks_atomicity() -> None:
    bad = [seed for seed in range(60) if check_all_crash_points(seed, 40, wal_rule=False)]
    assert bad
    s = WalSystem({"A": (100, 0)}, wal_rule=False)
    s.update(1, "A", 70)
    s.flush_page("A")
    d, lg = s.crash()
    assert lg == [] and recover(d, lg)[0]["A"][0] == 70  # the uncommitted 70 survives


def test_dropping_the_commit_rule_loses_a_commit() -> None:
    s = WalSystem({"B": (50, 0)}, commit_rule=False)
    s.update(2, "B", 80)
    s.commit(2)
    d, lg = s.crash()
    assert 2 in s.acked and recover(d, lg)[0]["B"][0] == 50
    assert any("lost" in e for seed in range(30) for e in check_all_crash_points(seed, 40, commit_rule=False))


def test_redo_is_idempotent_with_page_lsn() -> None:
    s = WalSystem({"A": (100, 0)})
    s.update(1, "A", 70)
    s.commit(1)
    s.update(2, "A", 60)
    s.commit(2)
    s.flush_page("A")
    d, lg = s.crash()
    assert d["A"] == (60, 3)
    assert recover(d, lg)[0]["A"] == (60, 3)  # record 1 is not redone over the newer page
