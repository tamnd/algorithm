# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chain-replication/. The authors are listed in prov/BZKFM5.jsonl.

import random

from chain_replication import Chain, linearizable, random_run


def complete(ch: Chain) -> bool:
    return all(h["res"] is not None for h in ch.history)


def same_history(ch: Chain) -> bool:
    hs = [[e.seq for e in ch.servers[s].hist] for s in ch.chain]
    return all(h == hs[0] for h in hs)


def test_checker_rejects_a_stale_read() -> None:
    h = [{"op": "write", "arg": 1, "inv": 0, "res": 5, "out": None},
         {"op": "read", "arg": None, "inv": 6, "res": 9, "out": None}]
    assert not linearizable(h)
    h[1]["out"] = 1
    assert linearizable(h)


def test_message_counts() -> None:
    ch = Chain(4, seed=0)
    ch.add_client(0, [("write", "a"), ("read", None)])
    ch.run()
    # write: request, 3 forwards, reply, 3 acks; read: request, reply
    assert ch.messages == 8 + 2
    assert ch.history[1]["out"] == "a"


def test_no_crash_runs_are_linearizable() -> None:
    for seed in range(60):
        ch = random_run(seed)
        assert complete(ch) and same_history(ch), seed
        assert linearizable(ch.history), seed
        assert all(not ch.servers[s].sent for s in ch.chain), seed


def run_with_crash(position: str, seeds: range) -> None:
    for seed in seeds:
        rng = random.Random(1000 + seed)
        n = 4
        s = {"head": 0, "tail": n - 1, "middle": rng.choice([1, 2])}[position]
        ch = random_run(seed, n=n, crashes=[(rng.randint(5, 120), s)])
        assert s not in ch.chain and len(ch.chain) == n - 1, seed
        assert complete(ch) and same_history(ch), (position, seed)
        assert linearizable(ch.history), (position, seed)


def test_head_crash() -> None:
    run_with_crash("head", range(80))


def test_middle_crash() -> None:
    run_with_crash("middle", range(80))


def test_tail_crash() -> None:
    run_with_crash("tail", range(80))


def test_n_minus_one_crashes() -> None:
    for seed in range(60):
        rng = random.Random(2000 + seed)
        n = 4
        victims = rng.sample(range(n), n - 1)
        crashes = [(rng.randint(5, 250), v) for v in victims]
        ch = random_run(seed, n=n, ops=6, crashes=crashes)
        assert len(ch.chain) == 1, seed
        assert complete(ch), seed
        assert linearizable(ch.history), seed


def test_reads_at_any_server_are_not_linearizable() -> None:
    # The reason queries go to the tail: a server before the tail can return a
    # value that a later read at the tail does not show yet.
    bad = sum(not linearizable(random_run(seed, clients=4, read_at="any").history)
              for seed in range(200))
    assert bad > 0


def test_tail_crash_does_not_lose_forwarded_updates() -> None:
    # The tail crashes at once: the write reaches the middle server but never
    # the tail. The new tail answers the client from its Sent list.
    ch = Chain(3, seed=0, delay=(5, 5))
    ch.at(0, ch.crash, 2)
    ch.add_client(0, [("write", "x"), ("read", None)], start=1)
    ch.run()
    assert ch.chain == [0, 1]
    w, r = ch.history
    assert w["res"] is not None and r["out"] == "x"
    assert [e.value for e in ch.servers[1].hist] == ["x"]
