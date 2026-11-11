# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cap-theorem/. The authors are listed in prov/CYTDK7.jsonl.

import random

import pytest

from cap_theorem import (
    PROTOCOLS,
    LocalAnswer,
    Primary,
    PrimaryWithTimeout,
    cap_executions,
    no_partition_read,
    run,
)


@pytest.mark.parametrize("protocol", PROTOCOLS)
def test_g2_cannot_tell_alpha_from_alpha2(protocol: type) -> None:
    v = cap_executions(protocol)
    assert v.same_view_for_g2


@pytest.mark.parametrize("protocol", PROTOCOLS)
def test_no_protocol_is_both_available_and_atomic(protocol: type) -> None:
    v = cap_executions(protocol)
    assert not (v.available and v.atomic)


def test_each_protocol_gives_up_one_property() -> None:
    assert cap_executions(LocalAnswer).available and not cap_executions(LocalAnswer).atomic
    assert not cap_executions(Primary).available and cap_executions(Primary).atomic
    v = cap_executions(PrimaryWithTimeout)
    assert v.available and not v.atomic and v.read_answer == 0


def test_without_loss_two_of_three() -> None:
    # The primary protocol is atomic and, with no lost messages, it answers.
    assert no_partition_read(Primary) == 1
    # The timeout protocol is atomic when no message is lost (Section 4.3).
    assert no_partition_read(PrimaryWithTimeout) == 1


def test_local_answer_is_stale_even_without_partition() -> None:
    r = run(LocalAnswer, [(0, 0, 1, "write", 1), (0, 1, 2, "read", None)], partition=False)
    assert r.responses[2][1] == 0  # the read overlaps the write here, so 0 is allowed
    r = run(LocalAnswer, [(0, 0, 1, "write", 1), (5, 1, 2, "read", None)], partition=False)
    assert r.responses[2][1] == 1  # the update arrived at tick 1


def test_primary_is_atomic_on_random_runs_without_loss() -> None:
    # Model: one register. With no loss and requests spaced out, each read
    # returns the last write that completed before it.
    rng = random.Random(2002)
    for _ in range(500):
        script = []
        expected = {}
        value, t = 0, 0
        for rid in range(1, rng.randint(2, 8)):
            node = rng.randrange(2)
            if rng.random() < 0.5:
                value = rid
                script.append((t, node, rid, "write", value))
            else:
                script.append((t, node, rid, "read", None))
                expected[rid] = value
            t += 3  # each request finishes within 2 ticks
        for proto in (Primary, PrimaryWithTimeout):
            r = run(proto, script, partition=False, ticks=t + 5)
            for rid, val in expected.items():
                assert r.responses[rid][1] == val
