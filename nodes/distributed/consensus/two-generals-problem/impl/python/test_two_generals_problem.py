# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-generals-problem/. The authors are listed in prov/6MJM6Y.jsonl.

from two_generals_problem import (
    all_runs,
    alternating,
    full_info_views,
    last_message_chain,
    one_bit_protocols,
    one_bit_solvable,
    rule_exists,
    same_view_witness,
    simultaneous,
    solvable,
)


def test_no_full_information_protocol_works() -> None:
    # Every protocol decides by a function of its full information view, so
    # these cover all deterministic protocols with these message patterns.
    for k in range(0, 9):
        assert not solvable(alternating(k))
    for r in range(0, 5):
        assert not solvable(simultaneous(r))


def test_no_one_bit_protocol_works() -> None:
    counts = {}
    for k in range(1, 4):
        total = 0
        for tables in one_bit_protocols(k):
            total += 1
            assert not one_bit_solvable(tables)
        counts[k] = total
    assert counts == {1: 4, 2: 256, 3: 16384}


def test_the_last_message_chain() -> None:
    for schedule in (alternating(1), alternating(4), alternating(7), simultaneous(3)):
        chain = last_message_chain(schedule)
        assert len(chain) == len([s for r in schedule for s in r]) + 3
        assert chain[0] == ((1, 1), frozenset())
        assert chain[-1][0] == (0, 0)
        for a, b in zip(chain, chain[1:]):
            assert same_view_witness(schedule, a, b) is not None


def test_weak_validity_is_easy() -> None:
    # Without "decide 1 when both want 1 and nothing is lost", the protocol
    # that always decides 0 is correct.
    for k in range(0, 5):
        assert solvable(alternating(k), strong=False)
    pairs = [(*full_info_views(alternating(3), *run), None) for run in all_runs(alternating(3))]
    rule = rule_exists(pairs)
    assert rule is not None and set(rule.values()) == {0}


def test_agreement_alone_or_validity_alone_is_easy() -> None:
    # With no message lost, two messages are enough: A sends its input, B
    # replies with its input, and both decide the AND. Loss breaks it.
    schedule = alternating(2)
    pairs = []
    for run in all_runs(schedule):
        if run[1]:
            continue
        va, vb = full_info_views(schedule, *run)
        v = 0 if run[0] == (0, 0) else (1 if run[0] == (1, 1) else None)
        pairs.append((va, vb, v))
    assert rule_exists(pairs) is not None
