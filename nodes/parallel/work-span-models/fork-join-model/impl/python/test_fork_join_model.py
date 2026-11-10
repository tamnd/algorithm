# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fork-join-model/. The authors are listed in prov/CRAW0D.jsonl.

import math
import random

from fork_join_model import (build_dag, dag_work_span, greedy_time, p_fib, parallel_for, random_program,
                             sp_term, work_span)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def test_composition_rules_match_the_dag():
    rng = random.Random(1)
    for _ in range(400):
        body = random_program(rng, rng.randint(0, 4))
        dag, _, _ = build_dag(body)
        assert work_span(sp_term(body)) == dag_work_span(dag)


def test_one_source_and_one_sink():
    rng = random.Random(2)
    for _ in range(100):
        dag, source, sink = build_dag(random_program(rng, 3))
        n = len(dag.weight)
        has_pred = [False] * n
        for v in range(n):
            for u in dag.succ[v]:
                has_pred[u] = True
        assert [v for v in range(n) if not has_pred[v]] == [source]
        assert [v for v in range(n) if not dag.succ[v]] == [sink]


def test_spawn_and_sync_example():
    # work 2; spawn (work 5); work 3; sync; work 1  gives W = 11 and S = 2 + max(5, 3) + 1 = 8
    body = [("work", 2), ("spawn", [("work", 5)]), ("work", 3), ("sync",), ("work", 1)]
    assert work_span(sp_term(body)) == (11, 8)
    # without the sync the last strand runs in parallel with the child: S = 2 + max(5, 3 + 1)
    body = [("work", 2), ("spawn", [("work", 5)]), ("work", 3), ("work", 1)]
    assert work_span(sp_term(body)) == (11, 7)
    # a call is serial
    body = [("work", 2), ("call", [("work", 5)]), ("work", 3), ("sync",), ("work", 1)]
    assert work_span(sp_term(body)) == (11, 11)


def test_p_fib_work_and_span():
    for n in range(1, 16):
        w, s = work_span(sp_term(p_fib(n)))
        assert w == 3 * fib(n + 1) - 2
        assert s == 2 * n - 1


def test_parallel_for():
    for n in list(range(1, 40)) + [64, 100, 128]:
        for b in (1, 3):
            w, s = work_span(sp_term(parallel_for(0, n, b)))
            assert w == n * b + (n - 1)
            assert s == math.ceil(math.log2(n)) + b if n > 1 else s == b


def test_greedy_bounds():
    rng = random.Random(3)
    for _ in range(150):
        dag, _, _ = build_dag(random_program(rng, 4, 5))
        w, s = dag_work_span(dag)
        for p in (1, 2, 3, 4, 8):
            t = greedy_time(dag, p)
            assert max(math.ceil(w / p), s) <= t <= w // p + s
        assert greedy_time(dag, 1) == w
        assert greedy_time(dag, max(w, 1)) == s
