# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tagged-pointers/. The authors are listed in prov/6NM0K3.jsonl.
"""Tests for tagged pointers on the Treiber stack and the Michael and Scott queue.

The memory is a type-stable pool that reuses the last freed address first.
A stale read of a freed node is allowed, as in a free list, so the only
failure that can show is the ABA problem: a CAS that succeeds on a word
that changed and changed back. The check at the end of each run looks for
lost, duplicated or freed values in the structure.
"""

from tagged_pointers import setup
from smr_sim import explore, run_random

ABA1 = [[("pop",)], [("pop",), ("push", "x")]]
ABA2 = [[("pop",)], [("pop",), ("push", "x"), ("pop",), ("push", "y")]]
PP = [[("push", "a"), ("pop",)], [("pop",), ("push", "b")]]
QA1 = [[("deq",)], [("deq",), ("enq", "x"), ("deq",)]]
QA2 = [[("deq",)], [("deq",), ("enq", "x"), ("deq",), ("enq", "y"), ("deq",)]]
EQ = [[("enq", "a"), ("deq",)], [("deq",), ("enq", "b")]]

WIDE = 16


def test_exhaustive_safe_with_wide_tags():
    for progs, kind, initial in [(ABA1, "stack", 2), (ABA2, "stack", 3), (PP, "stack", 2),
                                 (QA1, "queue", 1), (QA2, "queue", 2), (EQ, "queue", 1)]:
        r = explore(setup(progs, WIDE, kind, initial))
        assert r.violation is None, (progs, kind, r.violation, r.schedule)
        assert r.finals > 0


def test_random_safe_with_wide_tags():
    for progs, kind, initial in [(ABA2, "stack", 3), (QA2, "queue", 2)]:
        r = run_random(setup(progs, WIDE, kind, initial), range(300))
        assert r.violation is None, (kind, r.violation, r.schedule)


def test_no_tag_gives_aba():
    for progs, kind, initial in [(ABA1, "stack", 2), (PP, "stack", 2), (QA1, "queue", 1), (QA2, "queue", 2)]:
        r = explore(setup(progs, None, kind, initial))
        assert r.kind == "corrupt", (progs, kind, r.kind)


def test_wraparound_stack():
    # One reuse of the top node between the read and the CAS: one tag bit wraps, two do not.
    assert explore(setup(ABA1, 1, "stack", 2)).kind == "corrupt"
    assert explore(setup(ABA1, 2, "stack", 2)).violation is None
    # Two reuses: the root tag moves four times, so two bits wrap and three do not.
    assert explore(setup(ABA2, 2, "stack", 3)).kind == "corrupt"
    assert explore(setup(ABA2, 3, "stack", 3)).violation is None


def test_wraparound_queue():
    # The head moves twice between the read and the CAS of the stalled dequeue.
    assert explore(setup(QA1, 1, "queue", 1)).kind == "corrupt"
    assert explore(setup(QA1, 2, "queue", 1)).violation is None
