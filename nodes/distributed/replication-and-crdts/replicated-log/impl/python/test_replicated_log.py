# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/replicated-log/. The authors are listed in prov/BQWX41.jsonl.

import random

from replicated_log import NOOP, Log


def add(state: int, cmd: tuple) -> int:
    return state * 2 if cmd[0] == "dbl" else state + cmd[1]


def test_paxos_gap_and_noop() -> None:
    log = Log(0, add)
    for s, c in [(1, ("add", 1)), (2, ("add", 2)), (3, ("dbl",)), (4, ("add", 4)), (6, ("add", 6))]:
        log.choose(s, 1, c)
    assert log.commit_index == 4
    assert log.apply_committed() == [1, 2, 3, 4]
    assert log.state == 10  # ((0 + 1 + 2) * 2) + 4
    assert log.gaps() == [5]
    # slot 6 waits: it is chosen but not in the committed prefix
    assert log.apply_committed() == []
    assert log.fill_gaps(term=2) == [5]
    assert log.entries[5] == (2, NOOP)
    assert log.commit_index == 6
    assert log.apply_committed() == [5, 6]
    assert log.state == 16


def follower_with(terms: list[int]) -> Log:
    log = Log(0, add)
    log.append_entries(0, 0, [(t, ("add", i + 1)) for i, t in enumerate(terms)], 0)
    return log


def repair(leader: list[tuple], f: Log, leader_commit: int) -> int:
    """The leader decrements nextIndex until AppendEntries succeeds. Returns the tries."""
    nxt = len(leader) + 1
    tries = 0
    while True:
        tries += 1
        prev = nxt - 1
        prev_term = leader[prev - 1][0] if prev > 0 else 0
        if f.append_entries(prev, prev_term, leader[prev:], leader_commit):
            return tries
        nxt -= 1


def test_raft_page_example() -> None:
    leader = [(1, ("add", 1)), (1, ("add", 2)), (2, ("add", 3)), (3, ("add", 40)), (3, ("add", 50))]
    f = follower_with([1, 1, 2, 2, 2, 2])
    f.commit_index = 3
    assert not f.append_entries(4, 3, leader[4:], 5)
    assert f.append_entries(3, 2, leader[3:], 5)
    assert [f.entries[i][0] for i in sorted(f.entries)] == [1, 1, 2, 3, 3]
    f.apply_committed()
    assert f.state == 1 + 2 + 3 + 40 + 50


def test_log_matching_repair_random() -> None:
    for seed in range(300):
        rng = random.Random(seed)
        common = rng.randint(0, 6)
        terms = sorted(rng.randint(1, 3) for _ in range(common))
        top = terms[-1] if terms else 1
        leader = [(t, ("add", i)) for i, t in enumerate(terms)]
        # the leader of term top + 2 has at least one entry of its own term
        leader += [(top + 2, ("add", 100 + i)) for i in range(rng.randint(1, 4))]
        stale = [(top + 1, ("add", 200 + i)) for i in range(rng.randint(0, 5))]
        f = Log(0, add)
        f.append_entries(0, 0, leader[:common] + stale, 0)
        f.commit_index = rng.randint(0, common)  # committed entries are in the common prefix
        before = {i: f.entries[i] for i in range(1, f.commit_index + 1)}
        tries = repair(leader, f, len(leader))
        assert tries <= len(leader) + 1
        assert [f.entries[i] for i in sorted(f.entries)] == leader
        assert all(f.entries[i] == e for i, e in before.items())


def test_snapshot_then_suffix_gives_same_state() -> None:
    for seed in range(300):
        rng = random.Random(seed)
        cmds = [("dbl",) if rng.random() < 0.3 else ("add", rng.randint(1, 9)) for _ in range(rng.randint(1, 15))]
        entries = [(1, c) for c in cmds]
        full = Log(0, add)
        full.append_entries(0, 0, entries, len(entries))
        full.apply_committed()
        # a replica that compacts at a random point and goes on
        a = Log(0, add)
        cut = rng.randint(0, len(entries))
        a.append_entries(0, 0, entries[:cut], cut)
        a.apply_committed()
        idx, term, st = a.snapshot()
        assert idx == cut and all(i > cut for i in a.entries)
        a.append_entries(cut, term, entries[cut:], len(entries))
        a.apply_committed()
        assert a.state == full.state
        # a new replica that installs the snapshot, then gets the suffix
        b = Log(0, add)
        b.install_snapshot(idx, term, st)
        assert b.append_entries(cut, term, entries[cut:], len(entries))
        b.apply_committed()
        assert b.state == full.state and b.last_applied == len(entries)
