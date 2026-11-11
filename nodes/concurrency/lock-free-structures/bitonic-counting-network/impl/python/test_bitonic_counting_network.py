# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitonic-counting-network/. The authors are listed in prov/0S8S0R.jsonl.

import itertools
import random

from bitonic_counting_network import (BitonicCounter, bitonic, has_step_property, merger_network,
                                      quiescent_check, step_sequence)
from explorer import Memory, Run, explore, program, random_run
from lincheck import CounterSpec, lin_check, linearize


def make(net, procs, objs=None):
    """procs[p] = (input wire, number of tokens)."""
    def setup():
        mem = Memory()
        cn = BitonicCounter(mem, net)
        if objs is not None:
            objs[:] = [cn]
        return mem, [program(cn.token(wire), [("inc",)] * n) for wire, n in procs]

    return setup


def values(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def test_step_sequence() -> None:
    for k in (1, 2, 4, 8):
        for s in range(5 * k):
            y = step_sequence(s, k)
            assert sum(y) == s and has_step_property(y)


def test_depth_and_size() -> None:
    # Merger[2k] has depth log2(2k); Bitonic[2^m] has depth m(m+1)/2 and
    # (w/2) m(m+1)/2 balancers, and every layer is a perfect matching.
    for m in range(1, 7):
        w = 2 ** m
        net = bitonic(w)
        assert net.depth == m * (m + 1) // 2
        assert len(net.bals) == w // 2 * net.depth
        for layer in range(1, net.depth + 1):
            wires = [x for lv, a, b in net.bals if lv == layer for x in (a, b)]
            assert sorted(wires) == list(range(w))
        assert sorted(net.out) == list(range(w))
        assert merger_network(w // 2)[0].depth == m


def test_merger_keeps_the_step_property() -> None:
    # The lemma of the proof: if x and x' have the step property, so do the
    # outputs of Merger[2k]. A step sequence is fixed by its sum, so all
    # pairs of sums cover all cases up to that size.
    for k in (1, 2, 4, 8):
        net, _, _ = merger_network(k)
        for s in range(4 * k):
            for t in range(4 * k):
                y = net.quiescent_outputs(step_sequence(s, k) + step_sequence(t, k))
                assert has_step_property(y) and sum(y) == s + t, (k, s, t)


def test_merger_needs_step_inputs() -> None:
    # Without the step property on its inputs, a merger need not count:
    # x' = (0, 2) is not a step sequence.
    net, _, _ = merger_network(2)
    assert net.quiescent_outputs([0, 0, 0, 2]) == [1, 0, 1, 0]
    assert net.quiescent_outputs([0, 0, 1, 1]) == [1, 1, 0, 0]


def test_step_property_for_widths_2_4_8() -> None:
    for w, top in ((2, 8), (4, 5), (8, 3)):
        net = bitonic(w)
        for x in itertools.product(range(top), repeat=w):
            assert has_step_property(net.quiescent_outputs(list(x))), (w, x)
    rng = random.Random(11)
    for w in (16, 32, 64):
        net = bitonic(w)
        for _ in range(200):
            x = [rng.randrange(9) for _ in range(w)]
            assert has_step_property(net.quiescent_outputs(x)), (w, x)


def test_token_simulator_for_widths_2_4_8() -> None:
    # Tokens run concurrently, one balancer step at a time, in random
    # orders. At the end the outputs have the step property and match the
    # count computed from the inputs alone.
    for w in (2, 4, 8):
        net = bitonic(w)
        for seed in range(60):
            rng = random.Random(seed)
            procs = [(rng.randrange(w), 1 + rng.randrange(3)) for _ in range(1 + rng.randrange(5))]
            objs = []
            run = random_run(make(net, procs, objs=objs), seed)
            assert all(op is None for op in run.pending)
            x = [0] * w
            for wire, n in procs:
                x[wire] += n
            assert objs[0].outputs() == net.quiescent_outputs(x)
            assert has_step_property(objs[0].outputs())
            assert quiescent_check(run) is None, (w, seed)


def test_comparators_sort() -> None:
    # With comparators in place of balancers, Bitonic[w] sorts every 0-1
    # input, so by the 0-1 principle it is a sorting network.
    for w in (2, 4, 8):
        net = bitonic(w)
        for x in itertools.product((0, 1), repeat=w):
            y = net.comparator_outputs(list(x))
            assert y == sorted(x, reverse=True), (w, x)


def test_wrong_merger_wiring_does_not_count() -> None:
    # The bad network: each half merger gets the even (or the odd) outputs
    # of both inputs. For w = 4 and inputs (0, 1, 0, 1) the outputs are
    # (1, 0, 1, 0).
    bad = bitonic(4, wiring="even-even")
    assert bad.quiescent_outputs([0, 1, 0, 1]) == [1, 0, 1, 0]
    assert bitonic(4).quiescent_outputs([0, 1, 0, 1]) == [1, 1, 0, 0]
    st = explore(make(bad, [(1, 1), (3, 1)]), quiescent_check)
    assert st.failure is not None


def test_exhaustive_quiescent_consistency() -> None:
    for w, procs in ((2, [(0, 2), (1, 1)]), (4, [(0, 2), (3, 1)]), (4, [(1, 1), (2, 1), (3, 1)])):
        st = explore(make(bitonic(w), procs), quiescent_check)
        assert st.failure is None, st.failure
        assert st.runs > 10


def test_not_linearizable() -> None:
    # Bitonic[4]. A enters on wire 0, passes its three balancers, and stops
    # before it reads the counter of output 0. Then process 1 runs four
    # tokens one after another on wire 1: they get 1, 2, 3 and then 0, since
    # the fourth one leaves on output 0 before A takes its value. A gets 4.
    # The fourth token starts after the first one returned 1 and gets 0:
    # not linearizable, but quiescently consistent.
    net = bitonic(4)
    run = Run(make(net, [(0, 1), (1, 4)]))
    run.until(0, lambda op: op[1][0] == "out")
    run.finish(1)
    run.finish(0)
    assert values(run, 1) == [1, 2, 3, 0]
    assert values(run, 0) == [4]
    assert quiescent_check(run) is None
    assert linearize(run.history, CounterSpec()) is None
    st = explore(make(net, [(0, 1), (1, 3)]), lin_check(CounterSpec()))
    assert st.failure is not None


def test_solo_steps_are_bounded() -> None:
    rng = random.Random(3)
    checked = 0
    for w in (2, 4, 8, 16, 32):
        net = bitonic(w)
        for _ in range(10):
            run = Run(make(net, [(rng.randrange(w), 2) for _ in range(4)]))
            for _ in range(rng.randrange(4 * (net.depth + 1))):
                en = run.enabled()
                run.step(rng.choice(en[1:] or en))
            if run.count[0] > 0:
                run.finish_op(0)
            if run.pending[0] is not None:
                assert run.finish_op(0) == net.depth + 1
                checked += 1
    assert checked >= 30
