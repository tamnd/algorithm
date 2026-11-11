# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linearizability/. The authors are listed in prov/68Z96K.jsonl.

import random

from lincheck import (
    Objects,
    Queue,
    Register,
    Stack,
    is_linearizable,
    is_sequentially_consistent,
    linearize,
    project,
)
from linearizability import (
    NOT_LOCAL,
    OVERLAP,
    PENDING_SEEN,
    PENDING_UNSEEN,
    SC_NOT_LIN,
    STALE_READ,
    TWO_QUEUES,
    random_history,
    single,
)


def test_overlapping_enqueues_are_linearizable() -> None:
    order = linearize(OVERLAP, Queue())
    assert order is not None
    assert [o.arg for o in order[:2]] == ["y", "x"]


def test_sc_counterexample_is_sc_but_not_linearizable() -> None:
    assert not is_linearizable(SC_NOT_LIN, Queue())
    assert is_sequentially_consistent(SC_NOT_LIN, Queue())


def test_stale_read_is_sc_but_not_linearizable() -> None:
    assert not is_linearizable(STALE_READ, Register(0))
    assert is_sequentially_consistent(STALE_READ, Register(0))


def test_sequential_consistency_is_not_local() -> None:
    for obj in ("p", "q"):
        assert is_sequentially_consistent(single(project(NOT_LOCAL, obj)), Queue())
    assert not is_sequentially_consistent(NOT_LOCAL, TWO_QUEUES)
    # Each queue alone is not linearizable either, and neither is the whole.
    assert not is_linearizable(NOT_LOCAL, TWO_QUEUES)


def test_pending_operations() -> None:
    assert is_linearizable(PENDING_SEEN, Queue())
    assert is_linearizable(PENDING_UNSEEN, Queue())
    bad = PENDING_SEEN[:2] + [("res", 1, "z")]
    assert not is_linearizable(bad, Queue())


def test_a_sequential_history_is_checked_exactly() -> None:
    h = [("inv", 0, "push", 1), ("res", 0, None), ("inv", 0, "push", 2), ("res", 0, None),
         ("inv", 0, "pop", None), ("res", 0, 2)]
    assert is_linearizable(h, Stack())
    h[-1] = ("res", 0, 1)
    assert not is_linearizable(h, Stack())


def test_locality_on_random_histories() -> None:
    rng = random.Random(7)
    seen = {True: 0, False: 0}
    for _ in range(400):
        h = random_history(rng)
        whole = is_linearizable(h, TWO_QUEUES)
        parts = all(is_linearizable(single(project(h, o)), Queue()) for o in ("p", "q"))
        assert whole == parts
        seen[whole] += 1
    assert seen[True] > 0 and seen[False] > 0


def test_linearizable_implies_sequentially_consistent() -> None:
    rng = random.Random(11)
    for _ in range(300):
        h = random_history(rng, objects=("p",))
        if is_linearizable(h, Objects({"p": Queue()})):
            assert is_sequentially_consistent(h, Objects({"p": Queue()}))
