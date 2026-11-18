# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-in-time-recovery/. The authors are listed in prov/9VV51Q.jsonl.

"""Point-in-time recovery checked by failure injection.

A random workload with fuzzy copies runs and is cut by a media failure after
every prefix. For every target time, the recovered database must hold the
effects of exactly the transactions that committed at or before the target.
"""

import random

import pytest

from point_in_time_recovery import INIT, PAGE_OF, Copy, Db, recover_to, target_lsn

KEYS = sorted(PAGE_OF)
PAGES = sorted(set(PAGE_OF.values()))


def workload(rng: random.Random, steps: int) -> tuple[Db, list]:
    """Run steps random actions. Return the database and the committed
    transactions as (commit time, writes) in commit order."""
    db = Db()
    db.begin_copy()
    while db.copying:
        db.copy_step()
    active: dict[int, dict] = {}
    done: list = []
    nxt = 1
    for _ in range(steps):
        r = rng.random()
        if r < 0.15 and len(active) < 3:
            db.begin(nxt)
            active[nxt] = {}
            nxt += 1
        elif r < 0.5 and active:
            t = rng.choice(sorted(active))
            k = rng.choice(KEYS)
            v = rng.randint(100, 999)
            if db.write(t, k, v):
                active[t][k] = v
        elif r < 0.62 and active:
            t = rng.choice(sorted(active))
            done.append((db.commit(t), active.pop(t)))
        elif r < 0.67 and active:
            t = rng.choice(sorted(active))
            db.abort(t)
            del active[t]
        elif r < 0.75:
            if db.copying:
                db.copy_step()
            else:
                db.begin_copy()
        else:
            db.flush_page(rng.choice(PAGES))
    return db, done


def state_at(done: list, t: int) -> dict:
    s = dict(INIT)
    for time, writes in done:
        if time <= t:
            s.update(writes)
    return s


def values(disk: dict) -> dict:
    return {k: disk[PAGE_OF[k]][0][k] for k in KEYS}


def test_every_failure_point_and_every_target() -> None:
    for seed in range(4):
        steps = 70
        for k in range(0, steps + 1, 2):
            db, done = workload(random.Random(seed), k)
            log = list(db.log)  # the media failure: only the archive and the log are left
            for t in range(db.clock + 1):
                try:
                    disk, branch = recover_to(db.archive, log, t)
                except ValueError:
                    assert all(c.end > target_lsn(log, t) for c in db.archive)
                    continue
                assert values(disk) == state_at(done, t)
                # the new branch is the log up to the target plus the undo of the losers
                stop = target_lsn(log, t)
                assert branch[:stop] == log[:stop]
                assert all(r.kind in ("clr", "end") for r in branch[stop:])


def test_recovery_is_repeatable_after_a_crash() -> None:
    # recovery writes only to the new device; after a crash it starts again
    # from the archive copy and gives the same result
    db, done = workload(random.Random(9), 120)
    log = list(db.log)
    for t in range(db.clock + 1):
        try:
            a = recover_to(db.archive, log, t)
        except ValueError:
            continue
        b = recover_to(db.archive, log, t)
        assert a == b and values(a[0]) == state_at(done, t)


def test_transaction_open_at_the_target_is_rolled_back() -> None:
    db = Db()
    db.begin_copy()
    while db.copying:
        db.copy_step()
    db.begin(1)
    db.write(1, "a", 11)
    t1 = db.commit(1)  # time 1
    db.begin(2)
    db.write(2, "c", 31)  # T2 is open at time 1
    db.flush_page("P2")  # and its change reaches the disk
    db.begin_copy()
    while db.copying:
        db.copy_step()
    t2 = db.commit(2)  # time 2
    db.begin(3)
    db.write(3, "a", 99)  # a user error
    db.commit(3)  # time 3
    disk, branch = recover_to(db.archive, list(db.log), t1)
    assert values(disk) == dict(INIT, a=11)  # c = 31 of T2 is undone, a = 99 is not applied
    assert [r.kind for r in branch[-2:]] == ["clr", "end"] and branch[-1].txn == 2
    disk, _ = recover_to(db.archive, list(db.log), t2)
    assert values(disk) == dict(INIT, a=11, c=31)


def test_a_copy_that_ended_after_the_target_is_not_used() -> None:
    db = Db()
    db.begin_copy()
    while db.copying:
        db.copy_step()
    db.begin(1)
    db.write(1, "e", 55)
    db.commit(1)
    db.flush_page("P3")
    db.begin_copy()
    while db.copying:
        db.copy_step()
    first, second = db.archive
    # with only the second copy, a target before T1 cannot be reached: its
    # pages hold the committed change of T1, and recovery never undoes it
    with pytest.raises(ValueError):
        recover_to([second], list(db.log), 0)
    disk, _ = recover_to([first, second], list(db.log), 0)
    assert values(disk) == INIT


def test_start_lsn_of_a_fuzzy_copy_covers_dirty_pages() -> None:
    db = Db()
    db.begin_copy()
    while db.copying:
        db.copy_step()
    db.begin(1)
    db.write(1, "b", 22)  # LSN 4, P1 stays dirty in the buffer
    db.commit(1)
    db.begin_copy()  # the copy reads P1 without b = 22
    while db.copying:
        db.copy_step()
    copy = db.archive[-1]
    assert copy.start == 4 and copy.pages["P1"][0]["b"] == 20
    disk, _ = recover_to([copy], list(db.log), 1)
    assert values(disk)["b"] == 22
    # a start LSN at the begin_copy record would lose the committed change
    late = Copy(start=copy.end - 1, end=copy.end, pages=copy.pages)
    disk, _ = recover_to([late], list(db.log), 1)
    assert values(disk)["b"] == 20
