# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-based-simulation/. The authors are listed in prov/BBKYW7.jsonl.

import itertools
import random

import pytest

from cycle_based_simulation import CombinationalLoop, SyncDesign, simulate
from logicnet import eval2, random_circuit

# The page example: a serial adder with one carry register.
ADDER = SyncDesign(
    ["a", "b"],
    [("c", "cn", 0)],
    [("x1", "XOR", ["a", "b"]), ("s", "XOR", ["x1", "c"]), ("g1", "AND", ["a", "b"]),
     ("g2", "AND", ["x1", "c"]), ("cn", "OR", ["g1", "g2"])],
    ["s"],
)


def random_design(rng):
    n_in, n_reg = rng.randint(1, 3), rng.randint(1, 4)
    c = random_circuit(rng, n_in + n_reg, rng.randint(2, 20), n_outputs=2)
    qs = c.inputs[n_in:]
    regs = [(q, rng.choice([g[0] for g in c.gates] + qs), rng.randint(0, 1)) for q in qs]
    return SyncDesign(c.inputs[:n_in], regs, c.gates, c.outputs)


def fsm_table(design):
    """The explicit next-state and output table, from direct evaluation of every (state, input) pair."""
    qs = [q for q, _, _ in design.regs]
    table = {}
    for s in itertools.product((0, 1), repeat=len(qs)):
        for x in itertools.product((0, 1), repeat=len(design.inputs)):
            full = design.logic.direct_eval(dict(zip(qs + design.inputs, s + x)))
            table[s, x] = (tuple(full[d] for _, d, _ in design.regs), {o: full[o] for o in design.outputs})
    return table


def depth(c):
    memo = {n: 0 for n in c.inputs}

    def lev(n):
        if n not in memo:
            memo[n] = 1 + max(lev(m) for m in c.gates[c.driver[n]][2])
        return memo[n]

    return max([lev(n) for n in c.nets] + [0])


def clocked_step_reference(design, stimulus, period):
    """Unit delay per gate. Inputs change at the clock edge; registers sample the D nets just before the next edge."""
    c = design.logic
    state = {q: v for q, _, v in design.regs}
    prev = {n: 0 for n in c.nets}
    prev.update(state)
    trace = []
    for x in stimulus:
        for _ in range(period):
            cur = dict(x)
            cur.update(state)
            for out, op, ins in c.gates:
                cur[out] = eval2(op, [prev[n] for n in ins])
            prev = cur
        trace.append({o: prev[o] for o in design.outputs})
        state = {q: prev[d] for q, d, _ in design.regs}
    return trace, state


def test_serial_adder():
    a, b = [0, 1, 1, 0, 0], [1, 1, 1, 0, 0]  # 6 and 7, least significant bit first
    trace, state = simulate(ADDER, [{"a": p, "b": q} for p, q in zip(a, b)])
    assert [t["s"] for t in trace] == [1, 0, 1, 1, 0]  # 13
    assert state == {"c": 0}


@pytest.mark.parametrize("seed", range(15))
def test_matches_explicit_fsm_table(seed):
    rng = random.Random(seed)
    d = random_design(rng)
    table = fsm_table(d)
    stim = [{n: rng.randint(0, 1) for n in d.inputs} for _ in range(60)]
    trace, state = simulate(d, stim)
    s = tuple(v for _, _, v in d.regs)
    for x, out in zip(stim, trace):
        s, want = table[s, tuple(x[n] for n in d.inputs)]
        assert out == want
    assert tuple(state[q] for q, _, _ in d.regs) == s


@pytest.mark.parametrize("seed", range(15))
def test_matches_unit_delay_reference_when_the_period_exceeds_the_depth(seed):
    rng = random.Random(100 + seed)
    d = random_design(rng)
    stim = [{n: rng.randint(0, 1) for n in d.inputs} for _ in range(30)]
    period = depth(d.logic) + 1
    assert clocked_step_reference(d, stim, period) == simulate(d, stim)


def test_short_period_breaks_the_match():
    # q' = NOT(NOT(NOT(q))) has depth 3, so a period of 2 samples a value that has not settled.
    d = SyncDesign([], [("q", "n3", 0)], [("n1", "NOT", ["q"]), ("n2", "NOT", ["n1"]), ("n3", "NOT", ["n2"])], ["q"])
    stim = [{}] * 8
    assert clocked_step_reference(d, stim, 4) == simulate(d, stim)
    assert clocked_step_reference(d, stim, 2) != simulate(d, stim)


def test_loop_not_cut_by_a_register_is_rejected():
    d = SyncDesign(["s", "r"], [], [("q", "NOR", ["r", "qn"]), ("qn", "NOR", ["s", "q"])], ["q"])
    with pytest.raises(CombinationalLoop):
        simulate(d, [{"s": 0, "r": 0}])
