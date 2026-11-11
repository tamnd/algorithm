# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consensus-number/. The authors are listed in prov/FQYCHK.jsonl.

import pytest

from consensus_number import PROTOCOLS, cas_n, tas3_attempt, verify
from explorer import Found


@pytest.mark.parametrize("name", ["tas", "faa", "swap", "queue", "stack"])
def test_two_process_protocols(name) -> None:
    states, finals, worst = verify(PROTOCOLS[name], ["a", "b"])
    assert finals == 2            # the winner is p0 or p1
    assert worst == 3             # write, one step on the object, at most one read


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_cas_for_up_to_four_processes(n) -> None:
    values = [f"v{i}" for i in range(n)]
    states, finals, worst = verify(cas_n, values)
    assert finals == n            # one final state for each possible winner
    assert worst == 1             # one step each


def test_cas_with_equal_inputs() -> None:
    verify(cas_n, ["a", "a", "b"])


def test_tas_fails_for_three() -> None:
    with pytest.raises(Found, match="disagreement"):
        verify(tas3_attempt, ["a", "b", "c"])
