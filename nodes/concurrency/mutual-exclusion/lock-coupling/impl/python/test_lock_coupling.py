# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-coupling/. The authors are listed in prov/R9GFHC.jsonl.

from interleave import explore, linearizable
from lock_coupling import client, set_spec, setup

SCENARIOS = [
    ([], [[("add", 1)], [("add", 2), ("contains", 1)]]),
    ([], [[("add", 1)], [("add", 1)]]),
    ([1, 2], [[("remove", 1), ("contains", 2)], [("remove", 2)]]),
    ([1], [[("remove", 1), ("add", 1)], [("add", 2), ("contains", 1)]]),
    ([1, 3], [[("add", 2)], [("remove", 1)], [("remove", 3)]]),
    ([2], [[("add", 1)], [("remove", 2)], [("contains", 1)]]),
]


def check(initial, programs, couple):
    mem, keys = setup(initial, programs)
    procs = [client(programs, keys, couple)] * len(programs)
    g = explore(procs, mem)
    finals = {h for h in g.histories if h is not None}
    bad = [h for h in finals if not linearizable(h, set_spec, frozenset(initial))]
    return g, finals, bad


def test_lock_coupling_is_linearizable_and_deadlock_free() -> None:
    for initial, programs in SCENARIOS:
        g, finals, bad = check(initial, programs, True)
        assert finals and bad == []
        assert g.stuck == []  # locks are taken in list order, so no state waits forever


def test_one_lock_at_a_time_loses_an_update() -> None:
    # two adds at the same place: one of them overwrites the link of the other
    g, finals, bad = check(*SCENARIOS[0], couple=False)
    assert bad
    # two removes of neighbours: the second one puts the first node back
    g, finals, bad = check(*SCENARIOS[2], couple=False)
    assert bad
