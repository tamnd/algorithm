# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/predicate-locking/. The authors are listed in prov/THBP05.jsonl.

import itertools
import random

from predicate_locking import PredicateLockManager, intersects, run, run_serial

# Employees with a department and a salary.
INITIAL = {1: {"dept": 1, "sal": 10}, 2: {"dept": 1, "sal": 20}, 3: {"dept": 2, "sal": 30}}
DEPT1 = {"dept": (1, 1)}


def random_box(rng: random.Random) -> dict:
    box = {}
    for a in ("a", "b"):
        if rng.random() < 0.7:
            lo = rng.randrange(0, 6)
            box[a] = (lo, lo + rng.randrange(-1, 4))  # may be empty
    return box


def test_intersects_matches_a_grid_search() -> None:
    rng = random.Random(5)
    for _ in range(3000):
        p, q = random_box(rng), random_box(rng)
        inside = lambda box, x, y: all(  # noqa: E731
            lo <= v <= hi for a, v in (("a", x), ("b", y)) for lo, hi in [box.get(a, (-99, 99))]
        )
        brute = any(inside(p, x, y) and inside(q, x, y) for x, y in itertools.product(range(-2, 12), repeat=2))
        assert intersects(p, q) == brute


def test_lock_manager_modes() -> None:
    lm = PredicateLockManager()
    lm.grant(1, "S", {"dept": (1, 1)})
    assert lm.blockers(2, "S", {"dept": (1, 2)}) == set()  # S and S never conflict
    assert lm.blockers(2, "X", {"dept": (1, 1), "sal": (5, 5), "id": (9, 9)}) == {1}
    assert lm.blockers(2, "X", {"dept": (2, 2), "sal": (5, 5), "id": (9, 9)}) == set()
    assert lm.blockers(1, "X", {"dept": (1, 1)}) == set()  # own locks never block
    lm.release(1)
    assert lm.locks == []


PHANTOM = {1: [("select", DEPT1), ("select", DEPT1)], 2: [("insert", 4, {"dept": 1, "sal": 40})]}


def test_row_locks_let_a_phantom_in() -> None:
    out = run(PHANTOM, INITIAL, "tuple", script=[1, 2, 2, 1, 1])
    first, second = out["results"][1]
    assert [r for r, _ in first] == [1, 2] and [r for r, _ in second] == [1, 2, 4]
    serials = [run_serial(PHANTOM, INITIAL, o)[0] for o in ([1, 2], [2, 1])]
    assert out["results"] not in serials


def test_predicate_lock_makes_the_insert_wait() -> None:
    out = run(PHANTOM, INITIAL, "predicate", script=[1, 2, 2, 1, 1])
    first, second = out["results"][1]
    assert first == second and [r for r, _ in first] == [1, 2]
    assert out["commit_order"] == [1, 2]


def test_insert_outside_the_predicate_runs() -> None:
    progs = {1: PHANTOM[1], 2: [("insert", 4, {"dept": 2, "sal": 40})]}
    out = run(progs, INITIAL, "predicate", script=[1, 2, 2, 1, 1])
    assert out["schedule"][1] == ("insert", 2, 4)
    assert out["commit_order"] == [2, 1]


def test_update_that_moves_a_row_into_the_predicate_waits() -> None:
    progs = {1: PHANTOM[1], 2: [("update", 3, {"dept": 1, "sal": 30})]}
    out = run(progs, INITIAL, "predicate", script=[1, 2, 2, 1, 1])
    assert out["commit_order"] == [1, 2]
    out = run(progs, INITIAL, "tuple", script=[1, 2, 2, 1, 1])
    assert [r for r, _ in out["results"][1][1]] == [1, 2, 3]  # a phantom


def random_case(rng: random.Random) -> dict:
    fresh = iter(range(10, 30))
    progs = {}
    for t in range(1, rng.randint(2, 4) + 1):
        acts = []
        for _ in range(rng.randint(1, 4)):
            x = rng.random()
            row = {"dept": rng.randint(1, 3), "sal": rng.randrange(0, 50, 10)}
            if x < 0.45:
                lo = rng.randint(1, 3)
                box = {"dept": (lo, lo + rng.randint(0, 1))}
                if rng.random() < 0.5:
                    box["sal"] = (rng.randrange(0, 50, 10), 50)
                acts.append(("select", box))
            elif x < 0.7:
                acts.append(("insert", next(fresh), row))
            elif x < 0.9:
                acts.append(("update", rng.randint(1, 3), row))
            else:
                acts.append(("delete", rng.randint(1, 3)))
        if rng.random() < 0.5 and acts[0][0] == "select":
            acts.append(acts[0])
        progs[t] = acts
    return progs


def test_random_runs_are_serializable() -> None:
    rng = random.Random(23)
    tuple_bad = 0
    for _ in range(1500):
        progs = random_case(rng)
        out = run(progs, INITIAL, "predicate", rng=rng)
        results, table = run_serial(progs, INITIAL, out["commit_order"])
        assert out["results"] == results and out["table"] == table
        out = run(progs, INITIAL, "tuple", rng=rng)
        results, table = run_serial(progs, INITIAL, out["commit_order"])
        tuple_bad += out["results"] != results or out["table"] != table
    assert tuple_bad > 0
