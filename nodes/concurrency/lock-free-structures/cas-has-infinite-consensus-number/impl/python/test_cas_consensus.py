# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cas-has-infinite-consensus-number/. The authors are listed in prov/MGMTMQ.jsonl.

import itertools

import pytest

from cas_consensus import bool_cas_decide, cas_decide, random_with_crashes, verify


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_cmpxchg_all_interleavings(n) -> None:
    states, finals, worst = verify(cas_decide, [f"v{i}" for i in range(n)])
    assert finals == n        # one end state for each possible winner
    assert worst == 1         # one step per process


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_boolean_cas_all_interleavings(n) -> None:
    states, finals, worst = verify(bool_cas_decide, [f"v{i}" for i in range(n)])
    assert finals == n
    assert worst == (1 if n == 1 else 2)   # the CAS and, for a loser, one read


def test_all_binary_inputs_for_three() -> None:
    for inputs in itertools.product((0, 1), repeat=3):
        verify(cas_decide, list(inputs))
        verify(bool_cas_decide, list(inputs))


def test_random_runs_with_crashes() -> None:
    for seed in range(50):
        for proto in (cas_decide, bool_cas_decide):
            decided, live_decided = random_with_crashes(proto, 8, seed)
            assert len(decided) == 1               # agreement
            assert live_decided                    # every process that did not crash decides
