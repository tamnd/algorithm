# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/work-stealing/. The authors are listed in prov/D9FWRC.jsonl.

import random

from work_stealing import build_dag, fib_program, random_program, sum_program, work_stealing

C_TIME = 2  # the stated constant c in mean T_p <= T_1/p + c * T_inf
C_STEAL = 2  # mean attempts <= c * p * T_inf


def check_run(dag, p, seed):
    r = work_stealing(dag, p, random.Random(seed))
    n = len(dag)
    # every node runs exactly once, on a real processor
    assert all(1 <= t <= r["time"] for t in r["ran_at"])
    assert all(0 <= q < p for q in r["ran_by"])
    # in dependency order: each node runs in a later step than each predecessor
    for u in range(n):
        for v in dag.succ[u]:
            assert r["ran_at"][u] < r["ran_at"][v]
    # no step runs more than p nodes
    per_step = [0] * (r["time"] + 1)
    for t in r["ran_at"]:
        per_step[t] += 1
    assert max(per_step) <= p
    # each processor step is one node or one steal attempt
    assert p * r["time"] == n + r["attempts"]
    # the lower bounds of every schedule
    assert r["time"] >= max(-(-n // p), dag.span())
    return r


def dags():
    yield build_dag(fib_program(10), ("fib", 10))
    yield build_dag(fib_program(1), ("fib", 1))
    for n in (1, 2, 7, 64, 100):
        prog, root = sum_program(n)
        yield build_dag(prog, root)
    rng = random.Random(2024)
    for _ in range(25):
        prog, root = random_program(rng, 5)
        yield build_dag(prog, root)


def test_small_dag_shape():
    d = build_dag(fib_program(2), ("fib", 2))
    # fib(2): entry, spawn, [fib(1): entry, work, exit], [fib(0): entry, work, exit], sync, work, exit
    assert len(d) == 11
    assert d.span() == 8  # entry, spawn, fib(1) entry, work, exit, sync, work, exit
    assert all(len(s) <= 2 for s in d.succ)


def test_one_processor_is_serial():
    for d in dags():
        r = check_run(d, 1, 0)
        assert r["time"] == len(d) and r["attempts"] == 0


def test_every_strand_once_in_order():
    for d in dags():
        for p in (2, 3, 8):
            for seed in range(3):
                check_run(d, p, seed)


def test_mean_time_and_steals():
    for d in dags():
        t1, tinf = len(d), d.span()
        for p in (2, 4, 16):
            runs = [check_run(d, p, seed) for seed in range(20)]
            mean_t = sum(r["time"] for r in runs) / len(runs)
            mean_a = sum(r["attempts"] for r in runs) / len(runs)
            assert mean_t <= t1 / p + C_TIME * tinf
            assert mean_a <= C_STEAL * p * tinf


def test_fib_speedup():
    d = build_dag(fib_program(12), ("fib", 12))
    runs = [check_run(d, 8, seed) for seed in range(10)]
    mean_t = sum(r["time"] for r in runs) / len(runs)
    assert len(d) / mean_t > 6.5  # near linear speedup: parallelism is about 32
