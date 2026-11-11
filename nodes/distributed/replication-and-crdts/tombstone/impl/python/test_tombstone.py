# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tombstone/. The authors are listed in prov/MG0079.jsonl.

from tombstone import TOMB, Replica, collect, erase_run, random_run, sync


def test_erase_resurrects_on_the_page_example() -> None:
    reps = erase_run()
    # replica 0 deleted x, but the session with replica 1 copied x back
    assert reps[0].get("x") == "v1"
    assert all(r.get("x") == "v1" for r in reps)


def test_tombstone_keeps_the_key_deleted_on_the_page_example() -> None:
    reps = [Replica(i, 3) for i in range(3)]
    reps[0].put("x", "v1", 1)
    sync(reps[0], reps[1], 2)
    sync(reps[1], reps[2], 3)
    reps[0].delete("x", 4, "tombstone")
    sync(reps[0], reps[1], 5)
    assert reps[0].get("x") is None and reps[1].get("x") is None
    assert reps[2].get("x") == "v1"  # not yet reached
    sync(reps[1], reps[2], 6)
    assert all(r.get("x") is None for r in reps)
    assert all(r.data["x"][1] is TOMB for r in reps)


def test_erase_resurrects_in_random_runs() -> None:
    back = sum(any(r.get("x") for r in random_run(seed, "erase")["reps"]) for seed in range(200))
    assert back == 200


def test_tombstones_never_resurrect() -> None:
    for seed in range(200):
        res = random_run(seed, "tombstone")
        assert all(r.get("x") is None for r in res["reps"]), seed
        assert all(r.get("y") == "keep" for r in res["reps"]), seed


def test_stable_gc_collects_and_never_resurrects() -> None:
    for seed in range(200):
        res = random_run(seed, "tombstone", gc="stable", down=(1, 5, 40), rounds=150)
        reps = res["reps"]
        assert all(r.get("x") is None for r in reps), seed
        # after the last sessions some replicas may hold the tombstone again; collect once more
        for r in reps:
            for k in [k for k in r.data if r.data[k][1] is TOMB]:
                r.seen_by[k] = set(range(res["n"]))
            collect(r, 10 ** 6, "stable")
        assert all("x" not in r.data for r in reps), seed


def test_grace_gc_resurrects_when_a_replica_is_down_too_long() -> None:
    back_short = back_long = 0
    for seed in range(200):
        # replica 1 holds x and is down from time 5 to 80; it misses the delete
        short = random_run(seed, "tombstone", gc="grace", grace=10, down=(1, 5, 80), rounds=150)
        long_ = random_run(seed, "tombstone", gc="grace", grace=200, down=(1, 5, 80), rounds=150)
        back_short += any(r.get("x") for r in short["reps"])
        back_long += any(r.get("x") for r in long_["reps"])
    assert back_long == 0
    assert back_short == 200
