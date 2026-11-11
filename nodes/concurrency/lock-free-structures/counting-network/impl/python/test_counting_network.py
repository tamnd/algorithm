# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counting-network/. The authors are listed in prov/BHV1FX.jsonl.

import itertools
import random

from counting_network import (CountingNetwork, Network, bitonic, block, has_step_property, periodic,
                              quiescent_check)
from explorer import Memory, Run, explore, program, random_run
from lincheck import CounterSpec, lin_check, linearize


def make(net, procs, objs=None, atomic=True):
    """procs[p] = (input wire, number of tokens)."""
    def setup():
        mem = Memory()
        cn = CountingNetwork(mem, net, atomic=atomic)
        if objs is not None:
            objs[:] = [cn]
        return mem, [program(cn.token(wire), [("inc",)] * n) for wire, n in procs]

    return setup


def values(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def test_shape() -> None:
    for k in range(1, 6):
        w = 2 ** k
        p, b = periodic(w), bitonic(w)
        assert p.depth == k * k and len(p.bals) == w // 2 * k * k
        assert b.depth == k * (k + 1) // 2 and len(b.bals) == w // 2 * b.depth


def test_step_property_in_quiescent_states() -> None:
    for make_net in (periodic, bitonic):
        for w, top in ((2, 6), (4, 4), (8, 3)):
            net = make_net(w)
            for x in itertools.product(range(top), repeat=w):
                assert has_step_property(net.quiescent_outputs(list(x))), (make_net.__name__, w, x)
        rng = random.Random(5)
        for w in (16, 32):
            net = make_net(w)
            for _ in range(300):
                x = [rng.randrange(7) for _ in range(w)]
                assert has_step_property(net.quiescent_outputs(x)), (make_net.__name__, w, x)


def test_one_block_is_not_enough() -> None:
    # A single Block[w] with w >= 4 does not count; the periodic network
    # needs log w blocks. One layer of balancers does not count either.
    for w in (4, 8):
        one = Network(w)
        block(one, list(range(w)))
        one.close()
        bad = [x for x in itertools.product(range(3), repeat=w)
               if not has_step_property(one.quiescent_outputs(list(x)))]
        assert bad
    layer = Network(4)
    layer.add(0, 1)
    layer.add(2, 3)
    layer.close()
    assert layer.quiescent_outputs([0, 0, 2, 0]) == [0, 0, 1, 1]


def test_exhaustive_quiescent_consistency() -> None:
    cases = [
        (periodic(2), [(0, 2), (1, 1)]),
        (periodic(4), [(0, 1), (1, 1), (3, 1)]),
        (bitonic(4), [(0, 2), (2, 1)]),
    ]
    for net, procs in cases:
        st = explore(make(net, procs), quiescent_check)
        assert st.failure is None, st.failure
        assert st.runs > 10


def test_not_linearizable() -> None:
    # Width 2: one balancer. A passes the balancer (to output 0) and stops.
    # B goes to output 1 and gets 1. C starts after B has returned, goes to
    # output 0 and gets 0. Then A gets 2. The history is quiescently
    # consistent but not linearizable: C follows B in real time and has the
    # smaller value.
    net = periodic(2)
    run = Run(make(net, [(0, 1), (1, 2)]))
    run.step(0)
    run.finish(1)
    run.finish(0)
    assert values(run, 1) == [1, 0] and values(run, 0) == [2]
    assert quiescent_check(run) is None
    assert linearize(run.history, CounterSpec()) is None
    st = explore(make(net, [(0, 1), (1, 2)]), lin_check(CounterSpec()))
    assert st.failure is not None


def test_the_toggle_must_be_atomic() -> None:
    # With a read and a write, two tokens read the same state, both leave on
    # output 0, and the values are 0 and 2.
    net = periodic(2)
    run = Run(make(net, [(0, 1), (1, 1)], atomic=False))
    run.step(0)
    run.step(1)
    run.finish(0)
    run.finish(1)
    assert sorted(values(run)) == [0, 2]
    assert quiescent_check(run) is not None
    st = explore(make(net, [(0, 1), (1, 1)], atomic=False), quiescent_check)
    assert st.failure is not None


def test_seeded_runs() -> None:
    for make_net in (periodic, bitonic):
        net = make_net(8)
        for seed in range(100):
            rng = random.Random(seed)
            procs = [(rng.randrange(8), 1 + rng.randrange(3)) for _ in range(4)]
            objs = []
            run = random_run(make(net, procs, objs=objs), seed)
            assert all(op is None for op in run.pending)
            assert quiescent_check(run) is None, (make_net.__name__, seed)
            n = sum(c for _, c in procs)
            assert sorted(values(run)) == list(range(n))
            assert has_step_property(objs[0].outputs())


def test_solo_steps_are_bounded() -> None:
    # A token takes depth + 1 steps (one toggle per layer and one
    # fetch-and-add), whatever the other tokens do and wherever they stop:
    # every operation is wait-free.
    rng = random.Random(7)
    checked = 0
    for make_net in (periodic, bitonic):
        for w in (2, 4, 8, 16):
            net = make_net(w)
            for _ in range(10):
                procs = [(rng.randrange(w), 2) for _ in range(4)]
                run = Run(make(net, procs))
                for _ in range(rng.randrange(4 * (net.depth + 1))):
                    en = run.enabled()
                    run.step(rng.choice(en[1:] or en))
                if run.count[0] > 0:
                    run.finish_op(0)
                if run.pending[0] is not None:
                    assert run.finish_op(0) == net.depth + 1
                    checked += 1
    assert checked >= 40
