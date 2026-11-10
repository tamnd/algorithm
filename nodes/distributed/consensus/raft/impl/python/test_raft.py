# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raft/. The authors are listed in prov/MSG4TW.jsonl.

from raft import LEADER, Cluster

ALL = {0, 1, 2, 3, 4}


def elect(c: Cluster, i: int, group: set[int]) -> None:
    c.timeout(i, force=True)
    c.run_group(group)


def test_basic_replication() -> None:
    c = Cluster(5)
    elect(c, 0, ALL)
    assert c.servers[0].role == LEADER and c.servers[0].current_term == 1
    for k in range(3):
        c.client(0, f"x{k}")
    c.run_group(ALL)
    c.heartbeat(0)
    c.run_group(ALL)
    for s in c.servers:
        assert s.state == ["x0", "x1", "x2"]
    assert c.violations == []


def test_one_server() -> None:
    c = Cluster(1)
    elect(c, 0, {0})
    c.client(0, "x")
    assert c.servers[0].state == ["x"]


def test_vote_once_per_term_and_up_to_date() -> None:
    c = Cluster(3)
    elect(c, 0, {0, 1, 2})
    c.client(0, "a")
    c.run_group({0, 1})  # only server 1 stores "a"
    c.crash(0)
    # server 2 has an empty log, so server 1 refuses it: 2 cannot win
    for _ in range(3):
        elect(c, 2, {1, 2})
        assert c.servers[2].role != LEADER
    elect(c, 1, {1, 2})
    assert c.servers[1].role == LEADER


def test_conflicting_suffix_is_replaced() -> None:
    c = Cluster(3)
    elect(c, 0, {0, 1, 2})
    c.client(0, "a")
    c.client(0, "b")  # never leaves server 0
    c.inflight.clear()
    c.crash(0)
    elect(c, 1, {1, 2})
    c.client(1, "c")
    c.restart(0)
    c.heartbeat(1)
    c.run_group({0, 1, 2})
    assert [e[1] for e in c.servers[0].log[1:]] == ["c"]
    assert c.violations == []


def figure8(commit_rule: str, fix: bool = False) -> Cluster:
    """The run of Figure 8 of the Raft paper, with servers S1..S5 as 0..4."""
    c = Cluster(5, commit_rule=commit_rule)
    s1, s2, s3, s4, s5 = range(5)
    # (a) S1 leads term 1 and stores "a" at index 1 on S1 and S2 only.
    elect(c, s1, ALL)
    c.client(s1, "a")
    c.run_group({s1, s2})
    # (b) S1 crashes. S5 wins term 2 with S3 and S4, stores "b" at index 1 only locally, and crashes.
    c.crash(s1)
    elect(c, s5, {s3, s4, s5})
    assert c.servers[s5].role == LEADER and c.servers[s5].current_term == 2
    c.client(s5, "b")
    c.inflight.clear()
    c.crash(s5)
    # (c) S1 restarts and wins term 3 (term 2 fails: S3 and S4 voted for S5).
    c.restart(s1)
    elect(c, s1, {s1, s2, s3})
    elect(c, s1, {s1, s2, s3})
    assert c.servers[s1].role == LEADER and c.servers[s1].current_term == 3
    if fix:
        c.client(s1, "c")  # an entry of term 3 that reaches a majority
    c.run_group({s1, s2, s3})  # "a" of term 1 is now on S1, S2 and S3
    # (d) S1 crashes. S5 restarts and tries to win.
    c.crash(s1)
    c.restart(s5)
    for _ in range(3):
        elect(c, s5, {s2, s3, s4, s5})
        if c.servers[s5].role == LEADER:
            c.client(s5, "d")
            c.run_group({s2, s3, s4, s5})
            c.heartbeat(s5)
            c.run_group({s2, s3, s4, s5})
            break
    return c


def test_figure8_count_rule_is_unsafe() -> None:
    c = figure8("count")
    assert c.servers[0].state == ["a"]  # S1 applied "a" at index 1 by counting replicas
    assert c.servers[4].role == LEADER and c.servers[4].state[0] == "b"  # S5 then overwrote it
    assert any(v.startswith("state machine safety") for v in c.violations)


def test_figure8_raft_rule_is_safe() -> None:
    c = figure8("raft")
    assert c.servers[0].state == []  # S1 did not commit "a": it is not of term 3
    assert c.servers[4].role == LEADER and c.servers[4].state == ["b", "d"]
    assert c.violations == []


def test_figure8_with_entry_of_current_term() -> None:
    c = figure8("raft", fix=True)
    assert c.servers[0].state == ["a", "c"]  # "c" of term 3 commits, and "a" with it
    assert c.servers[4].role != LEADER  # S2 and S3 refuse S5: their logs are more up to date
    assert c.violations == []


def run_seeds(seeds: range, **kw: object) -> float:
    commits = runs = 0
    for seed in seeds:
        c = Cluster(5 if seed % 3 else 3, seed=seed, **kw)
        c.run(1200)
        assert c.violations == [], (seed, kw, c.violations[:3])
        for ls in c.leaders.values():
            assert len(ls) == 1
        commits += len(c.applied)
        runs += 1
    return commits / runs


def test_random_runs_with_crashes_and_partitions() -> None:
    assert run_seeds(range(300)) > 10  # the runs commit entries, so the checks are not empty


def test_random_runs_with_loss_and_duplicates() -> None:
    assert run_seeds(range(1000, 1200), drop=0.1, dup=0.05) > 10


def test_random_runs_last_in_first_out() -> None:
    assert run_seeds(range(2000, 2200), lifo=True) > 10
