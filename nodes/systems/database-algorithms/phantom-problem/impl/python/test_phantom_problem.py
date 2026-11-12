# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phantom-problem/. The authors are listed in prov/J2PGNY.jsonl.

import random

from phantom_problem import has_phantom, run_index, run_serial

INITIAL = [5, 10, 20, 30]
EXAMPLE = {1: [("scan", 10, 20), ("scan", 10, 20)], 2: [("ins", 15)]}


def test_phantom_under_tuple_locks() -> None:
    out = run_index(EXAMPLE, INITIAL, "tuple", script=[1, 2, 2, 1, 1])
    assert out["results"][1] == [[10, 20], [10, 15, 20]]
    assert has_phantom(out["results"], EXAMPLE)
    # The result matches no serial order.
    assert out["results"] not in (run_serial(EXAMPLE, INITIAL, [1, 2]), run_serial(EXAMPLE, INITIAL, [2, 1]))


def test_next_key_locks_make_the_insert_wait() -> None:
    out = run_index(EXAMPLE, INITIAL, "next-key", script=[1, 2, 2, 1, 1])
    assert out["results"][1] == [[10, 20], [10, 20]]
    assert out["commit_order"] == [1, 2]
    assert out["schedule"][:3] == [("scan", 1, 10, 20, (10, 20)), ("scan", 1, 10, 20, (10, 20)), ("c", 1)]


def test_insert_after_the_range_is_not_blocked() -> None:
    progs = {1: [("scan", 10, 20), ("scan", 10, 20)], 2: [("ins", 35)]}
    out = run_index(progs, INITIAL, "next-key", script=[1, 2, 2, 1, 1])
    # 35 falls in the gap ended by the end of the index, which T1 did not lock.
    assert out["schedule"][1] == ("ins", 2, 35)
    assert out["commit_order"] == [2, 1]


def random_case(rng: random.Random):
    fresh = rng.sample([k for k in range(40) if k not in INITIAL], 8)
    progs = {}
    for t in range(1, rng.randint(2, 4) + 1):
        acts = []
        for _ in range(rng.randint(1, 4)):
            if rng.random() < 0.5 or not fresh:
                lo = rng.randrange(0, 40)
                acts.append(("scan", lo, lo + rng.randrange(0, 15)))
            else:
                acts.append(("ins", fresh.pop()))
        if rng.random() < 0.5 and acts[0][0] == "scan":
            acts.append(acts[0])  # repeat the first scan
        progs[t] = acts
    return progs


def test_random_runs() -> None:
    rng = random.Random(17)
    tuple_phantoms = 0
    for _ in range(1500):
        progs = random_case(rng)
        out = run_index(progs, INITIAL, "next-key", rng=rng)
        assert not has_phantom(out["results"], progs)
        assert out["results"] == run_serial(progs, INITIAL, out["commit_order"])
        out = run_index(progs, INITIAL, "tuple", rng=rng)
        tuple_phantoms += has_phantom(out["results"], progs)
    assert tuple_phantoms > 0
