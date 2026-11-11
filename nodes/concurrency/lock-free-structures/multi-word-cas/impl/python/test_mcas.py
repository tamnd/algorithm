# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-word-cas/. The authors are listed in prov/DFK374.jsonl.

import pytest

from explorer import Found, explore, final_histories
from lincheck import is_linearizable
from mcas import Words, setup_for, solo_cost, starve_reader

INIT = {"x": 0, "y": 0, "z": 0}

WORKLOADS = {
    # two CASNs on the same two words: exactly one can succeed
    "same": [[("casn", (("x", 0, 1), ("y", 0, 1)))], [("casn", (("x", 0, 2), ("y", 0, 2)))]],
    # two CASNs that share the word y
    "overlap": [[("casn", (("x", 0, 1), ("y", 0, 1)))], [("casn", (("y", 0, 5), ("z", 0, 5)))]],
    # a CASN and a reader of both words
    "reader": [[("casn", (("x", 0, 1), ("y", 0, 1)))], [("read", "x"), ("read", "y")]],
    # the second CASN names the words in the other order
    "opposite": [[("casn", (("x", 0, 1), ("y", 0, 1)))], [("casn", (("y", 0, 2), ("x", 0, 2)))]],
}


@pytest.mark.parametrize("k", [1, 2, 3, 4])
def test_solo_cost_is_3k_plus_1_cas(k) -> None:
    cas, reads, ok, words = solo_cost(k)
    assert ok is True
    assert cas == 3 * k + 1
    assert reads == k + 2
    assert set(words.values()) == {1}


@pytest.mark.parametrize("name", sorted(WORKLOADS))
def test_every_history_is_linearizable(name) -> None:
    hs = final_histories(setup_for(WORKLOADS[name], INIT), max_depth=300)
    assert hs
    for h in hs:
        assert is_linearizable(list(h), Words(INIT)), h


@pytest.mark.parametrize("name", sorted(WORKLOADS))
def test_every_run_ends(name) -> None:
    # No cycle and no run longer than the bound: on this finite workload,
    # some operation always completes, so the operations are lock-free here.
    states, finals = explore(setup_for(WORKLOADS[name], INIT), max_depth=300)
    assert states > 0 and finals > 0


def test_same_words_exactly_one_succeeds() -> None:
    for h in final_histories(setup_for(WORKLOADS["same"], INIT), max_depth=300):
        assert sorted(e[2] for e in h if e[0] == "res") == [False, True]


def test_without_address_order_helping_can_recurse_for_ever() -> None:
    with pytest.raises(Found, match="depth bound"):
        explore(setup_for(WORKLOADS["opposite"], INIT, sort=False), max_depth=200)


def test_not_wait_free_a_reader_can_starve() -> None:
    steps, done, others = starve_reader(1000)
    assert not done
    assert steps > 500 and others > 50
