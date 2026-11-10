# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-fibonacci/. The authors are listed in prov/SX5BQA.jsonl.

from parallel_fibonacci import cost, dag_work_span, fib, p_fib, pfib_dag


def closed_work(n):
    return 4 * fib(n + 1) - 3


def closed_span(n):
    return 1 if n <= 1 else 2 * n


def test_values():
    for n in range(0, 22):
        assert p_fib(n)[0] == fib(n)


def test_work_and_span_closed_forms():
    for n in range(0, 22):
        _, w, s = p_fib(n)
        assert w == closed_work(n)
        assert s == closed_span(n)
    for n in range(0, 300):
        assert cost(n) == (closed_work(n), closed_span(n))


def test_dag_matches_composition_rules():
    for n in range(0, 16):
        assert dag_work_span(pfib_dag(n)) == p_fib(n)[1:]


def test_clrs_figure_example():
    # P-FIB(4): work 17, span 8 (CLRS 3e, Figure 27.2)
    assert p_fib(4) == (3, 17, 8)


def test_parallelism_grows():
    prev = 0
    for n in range(3, 60):
        w, s = cost(n)
        assert w / s > prev
        prev = w / s
