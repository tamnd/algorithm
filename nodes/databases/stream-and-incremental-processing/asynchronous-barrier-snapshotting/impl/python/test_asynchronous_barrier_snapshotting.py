# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asynchronous-barrier-snapshotting/. The authors are listed in prov/8TJ3Y4.jsonl.

import random
from collections import Counter

from asynchronous_barrier_snapshotting import acyclic_job, cyclic_job, drain

PAGE_STEPS = [("emit", "s1"), ("trigger",), ("barrier", "s1"), ("emit", "s1"),
              ("emit", "s2"), ("barrier", "s2"),
              ("take", "m1", ("s1", "m1")), ("take", "m1", ("s1", "m1")), ("take", "m1", ("s1", "m1")),
              ("take", "m2", ("s2", "m2")), ("take", "m2", ("s2", "m2")),
              ("take", "cnt", ("m1", "cnt")), ("take", "cnt", ("m1", "cnt")),
              ("take", "cnt", ("m2", "cnt")), ("take", "cnt", ("m2", "cnt"))]


def page_run(aligned):
    job = acyclic_job([1, 4], [5], aligned)
    for act in PAGE_STEPS:
        job.do(act)
    job.run(random.Random(0))
    return job


def test_page_example() -> None:
    truth = drain(acyclic_job([1, 4], [5]), random.Random(1))
    assert truth["cnt"] == Counter({1: 2, 2: 1})

    job = page_run(True)
    snap = job.last_snapshot()
    assert snap["s1"]["offset"] == 1 and snap["s2"]["offset"] == 1
    assert snap["cnt"]["state"] == Counter({1: 1, 2: 1})
    assert drain(job.restored(snap), random.Random(2)) == truth

    bad = page_run(False)
    snap = bad.last_snapshot()
    assert snap["cnt"]["state"] == Counter({1: 1})
    assert drain(bad.restored(snap), random.Random(2))["cnt"] == Counter({1: 2})


def random_inputs(rng):
    return ([rng.randrange(6) for _ in range(rng.randrange(0, 8))],
            [rng.randrange(6) for _ in range(rng.randrange(0, 8))])


def check(make, seed, aligned=True):
    """Fail the job at a random step; return (recovery is exact, snapshot is a consistent cut, log size)."""
    rng = random.Random(seed)
    a, b = random_inputs(rng)
    truth = drain(make(a, b, aligned) if aligned is not None else make(a, b), random.Random(seed + 1))
    job = make(a, b, aligned) if aligned is not None else make(a, b)
    job.run(rng, steps=rng.randrange(0, 80), snapshots=rng.randrange(1, 4), p_trigger=0.2)
    snap = job.last_snapshot()
    recovered = drain(job.restored(snap), random.Random(seed + 2))
    # The cut: the job run on the prefixes of the inputs up to the stored offsets.
    pa, pb = a[:snap["s1"]["offset"]], b[:snap["s2"]["offset"]]
    prefix = make(pa, pb, aligned) if aligned is not None else make(pa, pb)
    cut = drain(prefix, random.Random(seed + 3))
    from_snap = drain(job.restored(snap, {"s1": pa, "s2": pb}), random.Random(seed + 4))
    logged = sum(len(p.get("log", [])) for p in snap.values())
    return recovered == truth, from_snap == cut, logged, snap, cut


def test_acyclic_recovery_and_cut() -> None:
    for seed in range(300):
        exact, consistent, logged, snap, cut = check(acyclic_job, seed)
        assert exact and consistent
        assert logged == 0
        # No channel state: the copied states are the states of the prefix run.
        for t in ("m1", "m2", "cnt", "sink"):
            assert +snap[t]["state"] == cut[t]


def test_cyclic_recovery_and_cut() -> None:
    with_log = 0
    for seed in range(300):
        exact, consistent, logged, _, _ = check(cyclic_job, seed, aligned=None)
        assert exact and consistent
        with_log += logged > 0
    assert with_log > 0  # back-edge logging was used


def test_back_edges() -> None:
    assert cyclic_job([], []).back == {("fb", "dec")}
    assert acyclic_job([], []).back == set()


def test_no_alignment_is_not_consistent() -> None:
    wrong = 0
    for seed in range(300):
        exact, consistent, _, _, _ = check(acyclic_job, seed, aligned=False)
        wrong += not (exact and consistent)
        assert check(acyclic_job, seed, aligned=True)[:2] == (True, True)
    assert wrong > 0
