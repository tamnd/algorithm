# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primary-backup-replication/. The authors are listed in prov/04PKB8.jsonl.

import random

from primary_backup_replication import linearizable, run, split_brain_run


def h(op: str, arg: object, inv: int, res: int | None, out: object = None) -> dict:
    return {"op": op, "arg": arg, "inv": inv, "res": res, "out": out}


def test_checker_on_small_histories() -> None:
    # write 1 then read 1: fine
    assert linearizable([h("write", 1, 1, 2), h("read", None, 3, 4, 1)])
    # write 1 completes, then a read returns the initial value: not linearizable
    assert not linearizable([h("write", 1, 1, 2), h("read", None, 3, 4, None)])
    # overlapping write and read may see either value
    assert linearizable([h("write", 1, 1, 4), h("read", None, 2, 3, None)])
    assert linearizable([h("write", 1, 1, 4), h("read", None, 2, 3, 1)])
    # a pending write may take effect
    assert linearizable([h("write", 1, 1, None), h("read", None, 5, 6, 1)])
    # two reads that see the new value and then the old one: not linearizable
    assert not linearizable([h("write", 1, 1, 10), h("read", None, 2, 3, 1), h("read", None, 4, 5, None)])


def test_page_example() -> None:
    # S0 sends UPDATE for write 2 to S1 only, then crashes (its third UPDATE send)
    r = run(1, 3, [[("write", 1), ("write", 2), ("read", None)]], crash_after={0: 3})
    hist = r["history"]
    assert [(x["op"], x["out"]) for x in hist] == [("write", None), ("write", None), ("read", 2)]
    assert r["vs"].view == (2, 1, (2,))
    s1, s2 = r["servers"][1], r["servers"][2]
    assert s1.value == s2.value == 2
    assert s1.cache[(0, 2)] == "ok"  # the retry of write 2 is answered from the cache
    assert linearizable(hist)


def random_ops(rng: random.Random, clients: int, k: int) -> list[list[tuple]]:
    out = []
    for c in range(clients):
        out.append([("write", 10 * c + i) if rng.random() < 0.5 else ("read", None) for i in range(k)])
    return out


def test_no_crash_runs_are_linearizable() -> None:
    for seed in range(100):
        rng = random.Random(seed)
        r = run(seed, 3, random_ops(rng, 3, 4))
        assert all(x["res"] is not None for x in r["history"])
        assert linearizable(r["history"])
        values = {s.value for s in r["servers"]}
        assert len(values) == 1


def test_primary_crash_at_random_times() -> None:
    for seed in range(200):
        rng = random.Random(1000 + seed)
        r = run(seed, 3, random_ops(rng, 2, 4), crash={0: rng.randint(1, 60)})
        hist = r["history"]
        assert all(x["res"] is not None for x in hist), seed
        assert linearizable(hist), seed
        num, p, bs = r["vs"].view
        assert p != 0
        live = [s for s in r["servers"] if s.sid in (p,) + bs]
        assert len({s.value for s in live}) == 1


def test_primary_crash_in_the_middle_of_an_update() -> None:
    # the primary sends UPDATE to the first backup only, then crashes
    for seed in range(200):
        rng = random.Random(2000 + seed)
        r = run(seed, 3, random_ops(rng, 2, 4), crash_after={0: rng.randint(1, 5)})
        assert all(x["res"] is not None for x in r["history"]), seed
        assert linearizable(r["history"]), seed


def test_tolerates_f_crashes_with_f_plus_1_servers() -> None:
    # n = 3 servers, f = 2 crashes: the last server serves alone
    for seed in range(100):
        rng = random.Random(3000 + seed)
        t1 = rng.randint(1, 40)
        r = run(seed, 3, random_ops(rng, 2, 4), crash={0: t1, 1: t1 + rng.randint(0, 40)})
        assert all(x["res"] is not None for x in r["history"]), seed
        assert linearizable(r["history"]), seed
        assert r["vs"].view[1] == 2 and r["vs"].view[2] == ()


def test_backup_crash_keeps_the_primary() -> None:
    for seed in range(100):
        rng = random.Random(4000 + seed)
        r = run(seed, 3, random_ops(rng, 2, 4), crash={1: rng.randint(1, 60)})
        assert r["vs"].view[1] == 0
        assert linearizable(r["history"])


def test_split_brain_is_not_linearizable() -> None:
    r = split_brain_run()
    hist = r["history"]
    assert [(x["op"], x["arg"], x["out"]) for x in hist] == [("write", 1, None), ("write", 2, None), ("read", None, 1)]
    assert hist[1]["res"] < hist[2]["inv"]  # write 2 completed before the read began
    assert not linearizable(hist)
    assert r["servers"][0].value == 1 and r["servers"][1].value == 2
