# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/silo-concurrency-control/. The authors are listed in prov/023YX3.jsonl.

import random

import dbsched
from silo_concurrency_control import Silo, Txn, simulate

ITEMS = ["x", "y", "z"]


def workload(rng, n_programs, n_workers):
    workers = [[] for _ in range(n_workers)]
    for pid in range(n_programs):
        prog = [(rng.choice("rw"), rng.choice(ITEMS)) for _ in range(rng.randint(1, 3))]
        workers[rng.randrange(n_workers)].append((pid, prog))
    return workers


def replay(order, txns):
    """Run the committed transactions one by one in the given order and
    return the values each one reads and the final state."""
    db = {x: 0 for x in ITEMS}
    seen = {}
    for name in order:
        t = txns[name]
        mine, vals = {}, []
        for kind, x in t.program:
            if kind == "r":
                vals.append(mine.get(x, db[x]))
            else:
                mine[x] = (t.program_id, x, tuple(vals))
        db.update(mine)
        seen[name] = vals
    return seen, db


def check_run(silo):
    log = tuple(silo.log)
    dbsched.validate(log)
    cp = dbsched.committed_projection(log)
    order = [n for n in silo.sp if n in silo.committed]
    # The serialization points give a conflict-equivalent serial order.
    assert dbsched.conflict_equivalent(cp, dbsched.serial_schedule(cp, order))
    assert dbsched.is_conflict_serializable(log)
    # The same reads and the same final state as the serial run in that order.
    seen, final = replay(order, silo.committed)
    for name, t in silo.committed.items():
        assert t.seen == seen[name]
    assert {x: r.value for x, r in silo.db.items()} == final
    # Epochs never go back along the serial order.
    epochs = [silo.committed[n].epoch for n in order]
    assert epochs == sorted(epochs)
    # TIDs grow along write-read and write-write dependencies, per record
    # and per worker.
    tid = {n: t.tid for n, t in silo.committed.items()}
    for i, p in enumerate(cp):
        for q in cp[i + 1:]:
            if p[0] == "w" and dbsched.conflicts(p, q):
                assert tid[p[1]] < tid[q[1]]
    by_worker = {}
    for n in order:
        by_worker.setdefault(silo.committed[n].worker, []).append(n)
    for names in by_worker.values():
        names.sort()
        assert [tid[n] for n in names] == sorted(tid[n] for n in names)
    for t in silo.committed.values():
        assert t.tid[0] == t.epoch


def drive(silo, t, steps):
    for _ in range(steps):
        assert silo.step(t)


def test_read_write_conflict_of_figure_3():
    # T1 reads x and writes y; T2 reads y and writes x. Both read 0. T1
    # commits first, so T2 sees a new TID on y in Phase 2 and aborts.
    silo = Silo(ITEMS)
    t1 = Txn(1, 0, [("r", "x"), ("w", "y")], "A")
    t2 = Txn(2, 1, [("r", "y"), ("w", "x")], "B")
    silo.step(t1)
    silo.step(t2)
    silo.step(t1)                  # w(y) buffered
    silo.step(t2)                  # w(x) buffered
    silo.step(t1)                  # lock y
    silo.step(t1)                  # e = 1, the serialization point of T1
    silo.step(t2)                  # lock x
    silo.step(t2)                  # e = 1, the serialization point of T2
    silo.step(t1)                  # validate x: T2 holds its lock, so T1 aborts
    assert t1.phase == "aborted"
    silo.step(t2)                  # validate y: same TID, and T1 released the lock
    drive(silo, t2, 2)             # TID, install x
    assert t2.phase == "done" and t2.tid == (1, 0)
    assert dbsched.format(silo.log) == "r1(x) r2(y) a1 w2(x) c2"


def test_one_commits_when_the_other_runs_later():
    silo = Silo(ITEMS)
    t1 = Txn(1, 0, [("r", "x"), ("w", "y")], "A")
    t2 = Txn(2, 1, [("r", "y"), ("w", "x")], "B")
    silo.step(t1)
    silo.step(t2)                  # T2 reads y = 0 with TID (0, 0)
    drive(silo, t1, 6)             # w, lock y, epoch, validate x, TID, install y
    assert t1.phase == "done" and t1.tid == (1, 0)
    silo.advance_epoch()
    drive(silo, t2, 4)             # w, lock x, epoch 2, validate y
    assert t2.phase == "aborted"   # y now has TID (1, 0)
    t3 = Txn(3, 1, [("r", "y"), ("w", "x")], "B")
    drive(silo, t3, 7)
    assert t3.phase == "done" and t3.tid == (2, 0)
    assert silo.db["x"].value == ("B", "x", (("A", "y", (0,)),))


def test_tid_rule():
    # Same epoch: one more than the largest TID seen; new epoch: (e, 0).
    silo = Silo(ITEMS)
    silo.db["x"].tid = (1, 5)
    t = Txn(1, 0, [("r", "x"), ("w", "y")], "A")
    drive(silo, t, 7)
    assert t.tid == (1, 6)
    silo.advance_epoch()
    u = Txn(2, 0, [("w", "z")], "B")
    drive(silo, u, 6)              # write, lock, epoch, validate, TID, install
    assert u.tid == (2, 0)
    v = Txn(3, 0, [("w", "z")], "C")
    drive(silo, v, 6)              # the worker's last TID is (2, 0)
    assert v.tid == (2, 1)


def test_random_runs_are_serializable():
    rng = random.Random(2013)
    commits = aborts = 0
    for _ in range(400):
        workers = workload(rng, rng.randint(2, 5), rng.randint(2, 4))
        silo = simulate(rng, workers, ITEMS, epoch_rate=0.1)
        check_run(silo)
        commits += len(silo.committed)
        aborts += sum(1 for a in silo.log if a[0] == "a")
    assert commits > 1000 and aborts > 20


def test_lock_waits_keep_the_order():
    silo = Silo(ITEMS)
    t1 = Txn(1, 0, [("w", "x"), ("w", "y")], "A")
    t2 = Txn(2, 1, [("w", "y")], "B")
    drive(silo, t1, 3)             # both writes, lock x
    drive(silo, t2, 2)             # write, lock y
    assert not silo.step(t1)       # y is locked: T1 waits
    drive(silo, t2, 4)             # epoch, validate, TID, install y
    drive(silo, t1, 6)             # lock y, epoch, validate, TID, install x and y
    assert t2.tid < t1.tid and silo.db["y"].value[0] == "A"


def test_without_validation_some_run_is_not_serializable():
    rng = random.Random(7)
    found = False
    for _ in range(300):
        workers = workload(rng, rng.randint(2, 5), rng.randint(2, 4))
        silo = simulate(rng, workers, ITEMS, epoch_rate=0.1, validate=False)
        if not dbsched.is_conflict_serializable(tuple(silo.log)):
            found = True
            break
    assert found
