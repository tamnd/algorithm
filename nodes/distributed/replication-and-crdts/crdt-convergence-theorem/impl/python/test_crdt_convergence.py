# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crdt-convergence-theorem/. The authors are listed in prov/TXVMWX.jsonl.

import random

from crdt_convergence import (
    G_COUNTER,
    G_SET,
    LAST_ARRIVAL,
    REMOVE_SET,
    SUM_MERGE,
    CausalReplica,
    OpCounter,
    OpORSet,
    OpRegister,
    or_set_without_causal_delivery,
    run_op_based,
    run_state_based,
)


def test_state_based_counter_and_set_converge() -> None:
    rng = random.Random(386)
    for obj in (G_COUNTER, G_SET):
        for _ in range(300):
            n = rng.randint(1, 4)
            run = run_state_based(obj, rng, n, rng.randint(0, 40))
            assert run.converged_pairs_ok  # strong convergence at every step
            assert run.invariant_ok  # state = join of the post-update states
            assert len(set(run.states)) == 1  # eventual convergence


def test_state_based_values_match_a_model() -> None:
    # The model of a g-counter is the number of updates in the history.
    rng = random.Random(29)
    for _ in range(200):
        n = rng.randint(1, 4)
        run = run_state_based(G_COUNTER, rng, n, rng.randint(0, 40))
        assert all(G_COUNTER.query(s) == len(h) for s, h in zip(run.states, run.histories))


def test_any_order_and_any_duplication_give_the_same_join() -> None:
    rng = random.Random(400)
    for obj in (G_COUNTER, G_SET):
        for _ in range(200):
            n = 3
            states = []
            s = obj.bottom(n)
            for _ in range(rng.randint(1, 5)):
                s = obj.update(s, rng.randrange(n), obj.gen_arg(rng))
                states.append(s)
            seq = states + rng.choices(states, k=rng.randint(0, 4))
            rng.shuffle(seq)
            a = obj.bottom(n)
            for x in seq:
                a = obj.merge(a, x)
            b = obj.bottom(n)
            for x in states:
                b = obj.merge(b, x)
            assert a == b


def test_last_arrival_is_not_strongly_convergent() -> None:
    # Two replicas update and exchange states at the same time: they swap.
    s0 = LAST_ARRIVAL.update(LAST_ARRIVAL.bottom(2), 0, 5)
    s1 = LAST_ARRIVAL.update(LAST_ARRIVAL.bottom(2), 1, 7)
    s0, s1 = LAST_ARRIVAL.merge(s0, s1), LAST_ARRIVAL.merge(s1, s0)
    # Both have seen both updates, yet their states differ.
    assert (s0, s1) == (7, 5)
    # The random runs also find violations.
    rng = random.Random(1)
    bad = sum(not run_state_based(LAST_ARRIVAL, rng, 3, 30).converged_pairs_ok for _ in range(100))
    assert bad > 0


def test_non_idempotent_merge_fails() -> None:
    a = SUM_MERGE.update(SUM_MERGE.bottom(2), 0, None)  # replica 0 increments
    b = SUM_MERGE.bottom(2)
    b = SUM_MERGE.merge(b, a)
    b = SUM_MERGE.merge(b, a)  # the same message, duplicated
    # Both replicas have history {inc}, but the values are 1 and 2.
    assert (SUM_MERGE.query(a), SUM_MERGE.query(b)) == (1, 2)
    rng = random.Random(5)
    bad = sum(not run_state_based(SUM_MERGE, rng, 3, 30).converged_pairs_ok for _ in range(100))
    assert bad > 0


def test_non_inflationary_update_fails() -> None:
    s0 = REMOVE_SET.update(REMOVE_SET.bottom(2), 0, ("add", 1))  # update 1
    old = s0  # replica 0 sends this state to replica 1
    s0 = REMOVE_SET.update(s0, 0, ("rm", 1))  # update 2
    s1 = REMOVE_SET.merge(REMOVE_SET.bottom(2), old)  # history {1}
    s1 = REMOVE_SET.merge(s1, s0)  # history {1, 2}
    # Replica 0 also has history {1, 2}, but the remove is lost at replica 1.
    assert (s0, s1) == (frozenset(), frozenset({1}))
    rng = random.Random(8)
    bad = sum(not run_state_based(REMOVE_SET, rng, 3, 30).converged_pairs_ok for _ in range(100))
    assert bad > 0


def test_op_based_without_causal_delivery_diverges() -> None:
    v0, v2 = or_set_without_causal_delivery()
    assert v0 == frozenset() and v2 == frozenset({"x"})


def test_non_commuting_concurrent_ops_diverge() -> None:
    a, b = OpRegister(), OpRegister()
    for op in [("set", 1), ("set", 2)]:
        a.effect(op)
    for op in [("set", 2), ("set", 1)]:
        b.effect(op)
    assert a.value() != b.value()


def test_op_based_objects_converge_with_causal_delivery() -> None:
    rng = random.Random(2011)
    for _ in range(250):
        n = rng.randint(1, 4)
        objs = run_op_based(lambda i: OpCounter(), rng, n, rng.randint(0, 30))
        assert len({o.value() for o in objs}) == 1
        objs = run_op_based(lambda i: OpORSet(i), rng, n, rng.randint(0, 30))
        assert len({o.value() for o in objs}) == 1


def test_causal_broadcast_buffers_until_ready() -> None:
    seen: list[tuple] = []
    a = CausalReplica(3, 0, lambda op: None)
    b = CausalReplica(3, 1, lambda op: None)
    c = CausalReplica(3, 2, seen.append)
    m1 = a.broadcast(("x",))
    b.receive(m1)
    m2 = b.broadcast(("y",))  # m1 happened before m2
    c.receive(m2)
    assert seen == []  # buffered
    c.receive(m1)
    assert seen == [("x",), ("y",)]
    c.receive(m1)  # duplicate ignored
    assert seen == [("x",), ("y",)]
