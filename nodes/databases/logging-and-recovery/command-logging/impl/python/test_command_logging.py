# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/command-logging/. The authors are listed in prov/DQZNNJ.jsonl.

"""Command logging checked by crash injection.

A random workload of procedures, group commits and checkpoints is cut by a
crash after every prefix. Recovery must give the state of a serial run of
exactly the commands in the stable log, and every reported transaction must
be among them.
"""

import random

from command_logging import ACCOUNTS, PROCS, CmdDb


def random_action(db: CmdDb, rng: random.Random, reported: set, states: dict) -> None:
    r = rng.random()
    if r < 0.55:
        kind = rng.choice(sorted(PROCS))
        if kind == "deposit":
            db.submit("deposit", rng.choice(ACCOUNTS), rng.randint(1, 30))
        elif kind == "transfer":
            src, dst = rng.sample(ACCOUNTS, 2)
            db.submit("transfer", src, dst, rng.randint(1, 150))
        else:
            db.submit("bonus", rng.choice(ACCOUNTS))
        states[len(db.log) + len(db.tail)] = dict(db.state)
    elif r < 0.75:
        reported.update(db.group_commit())
    elif r < 0.85 and db.writing is None:
        db.begin_checkpoint()
    elif db.writing is not None:
        db.checkpoint_step()


def test_crash_at_every_prefix() -> None:
    for seed in range(5):
        steps = 80
        for k in range(steps + 1):
            rng = random.Random(seed)
            db = CmdDb()
            reported: set = set()
            states = {0: dict(db.state)}
            for _ in range(k):
                random_action(db, rng, reported, states)
            stable = len(db.log)
            db = db.crash()
            db.recover()
            # the state after the last stable command, as it was before the crash
            assert db.state == states[stable]
            assert reported <= {c.txn for c in db.log}


def test_recovery_equals_replay_from_the_start() -> None:
    rng = random.Random(3)
    db = CmdDb()
    reported: set = set()
    for _ in range(300):
        random_action(db, rng, reported, {})
    db.group_commit()
    db = db.crash()
    replayed = db.recover()
    full = CmdDb(db.log)
    full.snapshots = full.snapshots[:1]
    assert full.recover() == len(db.log)
    assert full.state == db.state
    # the snapshot bounds the replay to the commands after it
    assert replayed == len(db.log) - db.snapshots[-1].lsn


def test_crash_during_recovery() -> None:
    rng = random.Random(8)
    db = CmdDb()
    for _ in range(200):
        random_action(db, rng, set(), {})
    db.group_commit()
    expect = db.state
    # recovery changes only memory, so a crash during it loses nothing
    db = db.crash()
    db.recover()
    db = db.crash()
    db.recover()
    assert db.state == expect


def test_aborts_replay_as_aborts() -> None:
    db = CmdDb()
    db.submit("transfer", "a", "b", 500)  # aborts: a has 100
    db.submit("transfer", "a", "b", 60)
    db.submit("transfer", "a", "b", 60)  # aborts: a has 40
    db.group_commit()
    db = db.crash()
    db.recover()
    assert db.state == {"a": 40, "b": 160, "c": 100, "d": 100}


def test_a_procedure_that_is_not_deterministic_breaks_recovery() -> None:
    clock = [0]

    def stamp(state: dict, rnd: random.Random, acct: str) -> bool:
        clock[0] += 7  # reads a clock outside the database, not the seeded source
        state[acct] += clock[0]
        return True

    db = CmdDb(procs=dict(PROCS, stamp=stamp))
    db.submit("stamp", "a")
    db.submit("bonus", "b")
    db.group_commit()
    before = dict(db.state)
    db = db.crash()
    db.recover()
    assert db.state["b"] == before["b"]  # the seeded source gives the same bonus
    assert db.state["a"] != before["a"]  # the clock does not
