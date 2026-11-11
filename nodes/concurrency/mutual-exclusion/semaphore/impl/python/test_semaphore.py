# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semaphore/. The authors are listed in prov/AHWX4C.jsonl.

from interleave import explore, no_progress, run, starvation
from semaphore import P, V, declare, guarded, lock_cv_P, lock_cv_V, lock_cv_init, morris, naive_mutex


def sem_ops(name):
    return (lambda: P(name)), (lambda: V(name))


def test_counting_semaphore_admits_k() -> None:
    for strong in (False, True):
        for k in (1, 2):
            init = declare({}, "s", k, strong)
            procs = [guarded(*sem_ops("s"))] * 3
            assert explore(procs, init, cs_limit=k).violation is None
            if k > 1:  # k processes can be inside at the same time
                assert explore(procs, init, cs_limit=k - 1).violation is not None
            g = explore(procs, init, cs_limit=k)
            assert not g.stuck


def test_value_comes_back_after_two_rounds() -> None:
    init = declare({}, "s", 2)
    g = explore([guarded(*sem_ops("s"), rounds=2)] * 3, init, cs_limit=2)
    assert g.violation is None and not g.stuck
    # each run ends with value 2 and nobody blocked: P and V calls balance
    m = run([guarded(*sem_ops("s"), rounds=2)] * 3, init, seed=5)
    assert m.mem[("val", "s")] == 2 and m.mem[("blocked", "s")] == frozenset() and len(m.entries) == 6


def test_weak_semaphore_mutex_starves_with_three() -> None:
    make, init = naive_mutex(False, None)
    g = explore([make] * 3, init)
    assert g.violation is None and no_progress(g) == []
    assert starvation(g, 0) != []


def test_weak_semaphore_mutex_is_fair_with_two() -> None:
    make, init = naive_mutex(False, None)
    g = explore([make] * 2, init)
    assert starvation(g, 0) == [] and starvation(g, 1) == []


def test_strong_semaphore_mutex_does_not_starve() -> None:
    make, init = naive_mutex(True, None)
    g = explore([make] * 3, init)
    assert all(starvation(g, p) == [] for p in range(3))


def test_morris_is_safe_and_starvation_free() -> None:
    make, init = morris(1)
    g = explore([make] * 3, init)
    assert g.violation is None and not g.stuck
    make, init = morris(None)
    g = explore([make] * 3, init)
    assert g.violation is None and no_progress(g) == []
    assert all(starvation(g, p) == [] for p in range(3))


def test_semaphore_is_not_reentrant() -> None:
    def twice(pid):
        yield from P("s")
        yield from P("s")  # the same process asks again: it waits for itself
    g = explore([twice], declare({}, "s", 1))
    assert g.stuck


def test_semaphore_from_mutex_and_condition_variable() -> None:
    for k in (1, 2):
        procs = [guarded(lock_cv_P, lock_cv_V)] * 3
        g = explore(procs, lock_cv_init(k), cs_limit=k)
        assert g.violation is None and not g.stuck
