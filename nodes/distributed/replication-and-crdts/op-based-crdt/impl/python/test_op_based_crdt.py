# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/op-based-crdt/. The authors are listed in prov/G9QCWP.jsonl.

import random

from op_based_crdt import (
    Endpoint,
    Msg,
    OpCounter,
    OpORSet,
    or_set_model,
    or_set_remove_before_add,
    run,
    same_run_with_causal_delivery,
)


def test_counter_converges_in_any_order_with_exactly_once_delivery() -> None:
    # Counter effects commute, so causal order is not needed: only exactly-once.
    rng = random.Random(101)
    for _ in range(500):
        n = rng.randint(1, 4)
        r = run(OpCounter, "exactly-once", rng, n, rng.randint(0, 30))
        model = sum(op[1] for op in r.ops)
        assert all(o.value() == model for o in r.objects)


def test_counter_with_causal_delivery_matches_the_model() -> None:
    rng = random.Random(102)
    for _ in range(500):
        n = rng.randint(1, 4)
        r = run(OpCounter, "causal", rng, n, rng.randint(0, 30))
        assert all(o.value() == sum(op[1] for op in r.ops) for o in r.objects)


def test_counter_diverges_when_duplicates_are_applied() -> None:
    a, b = Endpoint(2, 0, OpCounter(0), "raw"), Endpoint(2, 1, OpCounter(1), "raw")
    m = Msg(0, (1, 0), ("add", 1))
    a.obj.effect(m.op)
    b.receive(m)
    b.receive(m)  # the network delivered the message twice
    assert (a.obj.value(), b.obj.value()) == (1, 2)
    rng = random.Random(103)
    diverged = 0
    for _ in range(200):
        r = run(OpCounter, "raw", rng, 3, 20)
        diverged += len({o.value() for o in r.objects}) > 1
    assert diverged > 0


def test_or_set_constructed_run_without_causal_delivery_diverges() -> None:
    v0, v1, v2 = or_set_remove_before_add()
    # All three replicas applied the same add and the same remove.
    assert v0 == v1 == frozenset()
    assert v2 == frozenset({"x"})  # the remove found nothing to remove


def test_or_set_same_arrivals_with_causal_delivery_converge() -> None:
    v0, v1, v2 = same_run_with_causal_delivery()
    assert v0 == v1 == v2 == frozenset()


def test_or_set_converges_under_causal_delivery_and_matches_the_model() -> None:
    rng = random.Random(104)
    for _ in range(500):
        n = rng.randint(1, 4)
        r = run(OpORSet, "causal", rng, n, rng.randint(0, 40))
        model = or_set_model(r.ops)
        assert all(o.value() == model for o in r.objects)


def test_or_set_random_runs_without_causal_delivery_can_diverge() -> None:
    rng = random.Random(105)
    diverged = 0
    for _ in range(300):
        r = run(OpORSet, "exactly-once", rng, 3, 40)
        diverged += len({o.value() for o in r.objects}) > 1
    assert diverged > 0


def test_causal_layer_applies_each_effect_once() -> None:
    a = Endpoint(3, 0, OpCounter(0), "causal")
    m1 = Msg(1, (0, 1, 0), ("add", 1))
    m2 = Msg(2, (0, 1, 1), ("add", 5))  # m1 happened before m2
    for m in [m2, m2, m1, m1, m2]:
        a.receive(m)
    assert a.applied == 2 and a.obj.value() == 6
