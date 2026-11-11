# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/helping/. The authors are listed in prov/4QNG5W.jsonl.

import pytest

from explorer import Found, explore, final_histories
from helping import setup_for, stop_after_link
from lincheck import Queue, is_linearizable

WORKLOADS = [
    [[("enq", "a")], [("enq", "b")]],
    [[("enq", "a")], [("deq", None)]],
    [[("enq", "a"), ("deq", None)], [("enq", "b"), ("deq", None)]],
    [[("enq", "a")], [("enq", "b")], [("deq", None)]],
]


def test_with_help_the_queue_goes_on_after_a_stop() -> None:
    assert stop_after_link(help=True) == "done"


def test_without_help_one_stop_blocks_all_enqueues() -> None:
    assert stop_after_link(help=False) == "loop"


def test_with_help_every_history_is_linearizable() -> None:
    for progs in WORKLOADS:
        hs = final_histories(setup_for(progs, help=True))
        assert hs
        for h in hs:
            assert is_linearizable(list(h), Queue()), h


def test_with_help_every_run_of_a_finite_workload_ends() -> None:
    for progs in WORKLOADS:
        explore(setup_for(progs, help=True), max_depth=200)


def test_without_help_some_run_never_ends() -> None:
    # A cycle of states: a process spins while the enqueuer waits to move Tail.
    for progs in WORKLOADS:
        with pytest.raises(Found, match="cycle"):
            explore(setup_for(progs, help=False), max_depth=200)
