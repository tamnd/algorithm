# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fetch-and-add/. The authors are listed in prov/FAZZ48.jsonl.

import itertools

import pytest

from explorer import Found, explore
from fetch_and_add import agreement_check, consensus2, consensus3_attempt, consensus_setup, ticket


@pytest.mark.parametrize("values", list(itertools.product("ab", repeat=2)))
def test_two_process_consensus_in_every_interleaving(values) -> None:
    check = agreement_check(values)

    def bounded(w):
        # Wait-free: each process takes at most 3 of its own steps.
        if max(w.steps) > 3:
            return "a process took more than 3 steps"
        return check(w)

    states, finals = explore(consensus_setup(consensus2, values), check=bounded)
    assert finals >= 1
    # Every prefix of every run is a state, so a crash at any point is covered:
    # the processes that did decide agree.
    assert states > 10


def test_three_process_attempt_disagrees() -> None:
    values = ("a", "b", "c")
    with pytest.raises(Found) as e:
        explore(consensus_setup(consensus3_attempt, values), check=agreement_check(values))
    assert "disagreement" in e.value.msg


def test_tickets_are_distinct_in_every_interleaving() -> None:
    def setup():
        return {"next": 0}, [ticket(p) for p in range(4)]

    def final(w):
        return None if sorted(w.ret) == [0, 1, 2, 3] else f"tickets {w.ret}"

    states, finals = explore(setup, final=final)
    assert finals == 24
