# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/undo-log/. The authors are listed in prov/X5CC3X.jsonl.

import random

from undo_log import UndoLog


def test_worked_example():
    mem = {"x": 0, "y": 0, "z": 0}
    log = UndoLog()
    log.write(mem, "x", 1)
    log.write(mem, "y", 2)
    log.write(mem, "x", 3)
    assert log.entries == [("x", 0), ("y", 0)]
    assert mem == {"x": 3, "y": 2, "z": 0}  # the writes are in memory at once
    assert log.rollback(mem) == 2
    assert mem == {"x": 0, "y": 0, "z": 0} and len(log) == 0


def test_commit_keeps_the_new_values():
    mem = {"x": 0}
    log = UndoLog()
    log.write(mem, "x", 4)
    log.commit()
    assert mem == {"x": 4} and len(log) == 0
    assert log.rollback(mem) == 0 and mem == {"x": 4}  # nothing left to undo


def test_random_transactions_roll_back_exactly():
    rng = random.Random(3)
    for first_write_only in (True, False):
        for trial in range(300):
            words = [f"w{i}" for i in range(5)]
            mem = {a: rng.randrange(100) for a in words}
            before = dict(mem)
            log = UndoLog(first_write_only)
            writes = [(rng.choice(words), rng.randrange(100)) for _ in range(rng.randrange(1, 25))]
            for a, v in writes:
                log.write(mem, a, v)
            distinct = len({a for a, _ in writes})
            assert len(log) == (distinct if first_write_only else len(writes))
            log.rollback(mem)
            assert mem == before


def test_with_an_entry_per_write_only_the_reverse_order_works():
    mem = {"x": 0}
    log = UndoLog(first_write_only=False)
    log.write(mem, "x", 1)
    log.write(mem, "x", 2)
    assert log.entries == [("x", 0), ("x", 1)]
    log.rollback(mem, reverse=False)  # forward order leaves the value of the middle write
    assert mem == {"x": 1}
    mem = {"x": 0}
    log = UndoLog(first_write_only=False)
    log.write(mem, "x", 1)
    log.write(mem, "x", 2)
    log.rollback(mem)
    assert mem == {"x": 0}


def test_without_a_write_lock_another_reader_sees_a_value_that_is_undone():
    # T1 writes x in place; T2 reads x before T1 aborts and sees 1, a value that never commits.
    mem = {"x": 0, "y": 0}
    t1 = UndoLog()
    t1.write(mem, "x", 1)
    seen_by_t2 = mem["x"]
    t1.rollback(mem)
    assert seen_by_t2 == 1 and mem["x"] == 0


def test_without_a_write_lock_a_rollback_wipes_out_another_write():
    # T1 writes x = 1 in place (saving 0); T2 then writes x = 7 and commits; T1 aborts and restores 0.
    mem = {"x": 0}
    t1, t2 = UndoLog(), UndoLog()
    t1.write(mem, "x", 1)
    t2.write(mem, "x", 7)
    t2.commit()
    t1.rollback(mem)
    assert mem["x"] == 0  # the committed write of T2 is lost
