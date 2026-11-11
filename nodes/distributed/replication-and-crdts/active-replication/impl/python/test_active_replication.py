# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-replication/. The authors are listed in prov/9FZTP1.jsonl.

import random

from active_replication import kv_apply, run, sequential

DMAX = 10  # the largest link delay of the simulator


def workload(rng: random.Random, m: int) -> list[tuple]:
    cmds = []
    for _ in range(m):
        k = rng.choice("xy")
        op = rng.choice(["put", "add", "cas", "get"])
        if op == "put":
            cmds.append(("put", k, rng.randint(0, 3)))
        elif op == "add":
            cmds.append(("add", k, rng.randint(1, 3)))
        elif op == "cas":
            cmds.append(("cas", k, rng.randint(0, 3), rng.randint(0, 3)))
        else:
            cmds.append(("get", k))
    return cmds


def test_page_example() -> None:
    cmds = [("put", "x", 1), ("add", "x", 1), ("cas", "x", 2, 5), ("get", "x")]
    states, outs = sequential(cmds)
    assert outs == ["ok", 2, True, 5]
    assert states[-1] == (("x", 5),)
    res = run(seed=1, n=3, cmds=cmds, crash={1: 4})
    assert [r.state for r in res["replicas"] if r.rid != 1] == [(("x", 5),)] * 2


def test_same_log_same_state_many_seeds() -> None:
    for seed in range(300):
        rng = random.Random(seed)
        n = rng.randint(1, 5)
        cmds = workload(rng, rng.randint(1, 12))
        crash = {r: rng.randint(0, 40) for r in range(n) if rng.random() < 0.3}
        res = run(seed, n, cmds, crash=crash)
        states, outs = sequential(res["order"])
        assert sorted(res["order"]) == sorted(cmds)  # every command is ordered once
        for r in res["replicas"]:
            # a replica that applied i commands is in state s_i, and passed through s_0 .. s_i
            assert r.history == states[: len(r.history)]
            if ("R", r.rid) not in res["sim"].crashed:
                assert r.state == states[-1]
        # with at least one correct replica, the first reply is the right output
        if len(crash) < n:
            cl = res["client"]
            assert len(cl.result) == len(cmds)
            for k, o in cl.result.items():
                assert o == outs[k - 1]


def test_no_failover_delay() -> None:
    # crashes of f = n - 1 replicas do not slow the client: three link delays at most
    for seed in range(200):
        rng = random.Random(seed)
        cmds = workload(rng, 8)
        crash = {0: rng.randint(0, 20), 1: rng.randint(0, 20)}
        res = run(seed, 3, cmds, crash=crash)
        cl = res["client"]
        assert len(cl.result) == len(cmds)
        for k, t in cl.latency.items():
            assert t - res["sent_at"][k - 1] <= 3 * DMAX


def test_byzantine_vote_2f_plus_1() -> None:
    for seed in range(100):
        rng = random.Random(seed)
        f = rng.randint(1, 2)
        n = 2 * f + 1
        bad = set(rng.sample(range(n), f))
        cmds = workload(rng, 6)
        res = run(seed, n, cmds, byzantine=bad, need=f + 1)
        _, outs = sequential(res["order"])
        assert res["client"].result == {k + 1: o for k, o in enumerate(outs)}


def test_byzantine_vote_2f_is_not_enough() -> None:
    # n = 2, f = 1: the lying replica is as loud as the correct one, so no output gets f + 1 = 2 votes
    res = run(3, 2, [("put", "x", 1)], byzantine={1}, need=2)
    assert res["client"].result == {}
    # with need = 1 the client accepts the lie in some runs
    lies = 0
    for seed in range(50):
        res = run(seed, 2, [("put", "x", 1)], byzantine={1}, need=1)
        lies += res["client"].result[1] != "ok"
    assert 0 < lies < 50


def test_nondeterminism_breaks_replicas() -> None:
    # a command that reads a local random number is not deterministic: replicas diverge
    noise = random.Random(7)

    def noisy(state: tuple, cmd: tuple) -> tuple:
        if cmd[0] == "rand":
            return kv_apply(state, ("put", cmd[1], noise.randint(0, 10 ** 6)))
        return kv_apply(state, cmd)

    res = run(0, 3, [("rand", "x")], apply=noisy)
    assert len({r.state for r in res["replicas"]}) > 1
