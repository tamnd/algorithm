# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quorum-replication/. The authors are listed in prov/TKDEFR.jsonl.

import random

from quorum_replication import (disjoint_writes_run, inversion_run, linearizable, make,
                                add_client, run, stale_read_run)


def h(op: str, arg: object, inv: int, res: int | None, out: object = None) -> dict:
    return {"op": op, "arg": arg, "inv": inv, "res": res, "out": out}


def test_checker() -> None:
    assert linearizable([h("write", 1, 1, 2), h("read", None, 3, 4, 1)])
    assert not linearizable([h("write", 1, 1, 2), h("read", None, 3, 4, None)])
    assert linearizable([h("write", 1, 1, 9), h("read", None, 2, 3, 1), h("read", None, 4, 5, 1)])
    assert not linearizable([h("write", 1, 1, 9), h("read", None, 2, 3, 1), h("read", None, 4, 5, None)])


def ops(rng: random.Random, cid: int, k: int, writer: bool = True) -> list[dict]:
    out = []
    for i in range(k):
        if writer and rng.random() < 0.5:
            out.append({"op": "write", "arg": 100 * cid + i})
        else:
            out.append({"op": "read"})
    return out


def minority_crashes(rng: random.Random, n: int) -> dict[int, int]:
    f = (n - 1) // 2
    victims = rng.sample(range(n), rng.randint(0, f))
    return {s: rng.randint(0, 60) for s in victims}


def test_abd_multi_writer_linearizable_under_minority_crashes() -> None:
    for seed in range(300):
        rng = random.Random(seed)
        n = rng.choice([3, 5])
        sys = run(seed, n, [ops(rng, c, 3) for c in range(3)], crash=minority_crashes(rng, n))
        hist = sys["history"]
        assert all(x["res"] is not None for x in hist), seed
        assert linearizable(hist), seed


def test_abd_single_writer_linearizable_under_minority_crashes() -> None:
    for seed in range(300):
        rng = random.Random(10_000 + seed)
        n = rng.choice([3, 5])
        cl = [ops(rng, 0, 4)] + [ops(rng, c, 3, writer=False) for c in (1, 2)]
        sys = run(seed, n, cl, mode="swmr", crash=minority_crashes(rng, n))
        assert all(x["res"] is not None for x in sys["history"]), seed
        assert linearizable(sys["history"]), seed


def test_read_without_write_back_is_not_linearizable() -> None:
    bad = inversion_run(writeback=False)["history"]
    assert [x["out"] for x in bad if x["op"] == "read"] == [1, None]
    assert bad[0]["res"] is None  # the write is still running
    assert not linearizable(bad)
    good = inversion_run(writeback=True)["history"]
    assert [x["out"] for x in good if x["op"] == "read"] == [1, 1]
    assert linearizable(good)


def test_r_plus_w_greater_than_n_reads_last_completed_write() -> None:
    # one client, operations one after another: every read sees the last write
    for seed in range(300):
        rng = random.Random(20_000 + seed)
        n = rng.randint(1, 6)
        w = rng.randint(n // 2 + 1, n)  # 2W > N
        r = rng.randint(n - w + 1, n)  # R + W > N
        sys = make(seed, n, "gifford", r, w)
        seq = ops(rng, 0, 8)
        add_client(sys, 0, seq, start=0)
        sys["sim"].run()
        last = None
        for x in sys["history"]:
            if x["op"] == "write":
                last = x["arg"]
            else:
                assert x["out"] == last, (seed, n, r, w)


def test_r_plus_w_at_most_n_gives_a_stale_read() -> None:
    for n, r, w in [(3, 1, 2), (3, 2, 1), (4, 2, 2), (5, 2, 3)]:
        hist = stale_read_run(n, r, w)["history"]
        assert hist[0]["res"] < hist[1]["inv"]
        assert hist[1]["out"] is None  # the initial value, not 1
        assert not linearizable(hist)
    # with random quorums, stale reads also happen without a constructed schedule
    stale = 0
    for seed in range(300):
        sys = make(seed, 5, "gifford", 1, 1)
        sys["sim"].delay = (1, 50)
        add_client(sys, 0, [{"op": "write", "arg": 1}, {"op": "read"}], start=0)
        sys["sim"].run()
        stale += sys["history"][1]["out"] is None
    assert stale == 66  # of 300 seeded runs with N = 5, R = W = 1


def test_version_numbers_need_2w_greater_than_n() -> None:
    hist = disjoint_writes_run("gifford")["history"]
    assert [x["out"] for x in hist if x["op"] == "read"] == ["a", "b", "a"]
    assert not linearizable(hist)
    # tags (ts, writer id) order the two writes, so ABD needs only R + W > N
    hist = disjoint_writes_run("abd")["history"]
    assert [x["out"] for x in hist if x["op"] == "read"] == ["b", "b", "b"]
    assert linearizable(hist)


def test_abd_message_count() -> None:
    # a read and a write each cost 4n messages when all n servers are up
    sys = run(1, 5, [[{"op": "write", "arg": 1}, {"op": "read"}]])
    assert sys["sim"].messages == 2 * 4 * 5
