# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strict-two-phase-locking/. The authors are listed in prov/4829PV.jsonl.

import random

from strict_two_phase_locking import is_strict, run_serial, run_strict_2pl

INITIAL = {"x": "x0", "y": "y0", "z": "z0"}


def random_case(rng: random.Random):
    progs = {
        t: [(rng.choice("rw"), rng.choice("xyz")) for _ in range(rng.randint(1, 4))]
        for t in range(1, rng.randint(2, 5) + 1)
    }
    aborts = {t: rng.randint(0, len(p)) for t, p in progs.items() if rng.random() < 0.3}
    return progs, aborts


def test_reader_waits_for_commit() -> None:
    progs = {1: [("r", "x"), ("w", "x"), ("w", "y")], 2: [("r", "x"), ("w", "z")]}
    out = run_strict_2pl(progs, INITIAL, script=[1, 1, 1, 2, 2, 1, 2])
    assert out["schedule"] == [
        ("r", 1, "x"), ("w", 1, "x"), ("w", 1, "y"), ("c", 1, None),
        ("r", 2, "x"), ("w", 2, "z"), ("c", 2, None),
    ]
    assert is_strict(out["schedule"])


def test_abort_restores_before_image_and_reader_sees_it() -> None:
    progs = {1: [("w", "x"), ("w", "y")], 2: [("r", "x")]}
    out = run_strict_2pl(progs, INITIAL, script=[1, 2, 1], user_aborts={1: 1})
    # T2 waits for the X lock of T1; T1 aborts, x gets its old value, T2 reads it.
    assert out["schedule"][:3] == [("w", 1, "x"), ("a", 1, None), ("r", 2, "x")]
    assert out["reads"][2] == ["x0"]
    assert is_strict(out["schedule"])


def test_is_strict_checker() -> None:
    assert not is_strict([("w", 1, "x"), ("r", 2, "x"), ("c", 1, None), ("c", 2, None)])
    assert not is_strict([("w", 1, "x"), ("w", 2, "x"), ("c", 1, None), ("c", 2, None)])
    assert is_strict([("w", 1, "x"), ("a", 1, None), ("w", 2, "x"), ("c", 2, None)])
    assert is_strict([("r", 1, "x"), ("w", 2, "x"), ("c", 1, None), ("c", 2, None)])


def test_random_runs_strict_and_equal_to_serial() -> None:
    rng = random.Random(2024)
    aborted_runs = 0
    for case in range(600):
        progs, aborts = random_case(rng)
        rigorous = case % 2 == 1
        out = run_strict_2pl(progs, INITIAL, rng=rng, rigorous=rigorous, user_aborts=aborts)
        assert is_strict(out["schedule"])
        if rigorous:
            order = out["commit_order"]
        else:
            order = sorted(progs, key=out["lock_point"].__getitem__)
        final, reads = run_serial(progs, order, INITIAL)
        assert out["final"] == final
        assert out["reads"] == reads
        aborted_runs += any(p[0] == "a" for p in out["schedule"])
    assert aborted_runs > 100


def test_commit_order_can_fail_for_strict_but_not_rigorous() -> None:
    # T1 reads x and releases S early; T2 writes x and commits before T1.
    progs = {1: [("r", "x"), ("w", "y"), ("r", "z")], 2: [("w", "x")]}
    out = run_strict_2pl(progs, INITIAL, script=[1, 1, 2, 2, 1, 1])
    assert out["commit_order"] == [2, 1]
    final, reads = run_serial(progs, [2, 1], INITIAL)
    assert out["reads"] != reads
    final, reads = run_serial(progs, [1, 2], INITIAL)
    assert (out["final"], out["reads"]) == (final, reads)
    out = run_strict_2pl(progs, INITIAL, script=[1, 1, 2, 2, 1, 1], rigorous=True)
    assert out["commit_order"] == [1, 2]
