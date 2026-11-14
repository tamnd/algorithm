# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/event-driven-logic-simulation/. The authors are listed in prov/V1JG2T.jsonl.

import random

import pytest

from event_driven_logic_simulation import Oscillation, TimeWheel, simulate, waveform
from logicnet import Circuit, all_vectors, eval2, random_circuit

# The page example: y = ab + a'c, with b = c = 1 and a falling at time 10.
HAZARD = Circuit(
    ["a", "b", "c"],
    [("na", "NOT", ["a"]), ("p", "AND", ["a", "b"]), ("q", "AND", ["na", "c"]), ("y", "OR", ["p", "q"])],
    ["y"],
)
HAZARD_INIT = {"a": 1, "b": 1, "c": 1, "na": 0, "p": 1, "q": 0, "y": 1}


def values_at(init, changes, t):
    val = dict(init)
    for tc, n, v in changes:
        if tc > t:
            break
        val[n] = v
    return val


def step_reference(c, delay, init, events, t_end, inertial=False):
    """Unit-time step simulation. Every delay must be at least 1.

    z(t) is the gate function of the values at time t. With transport delay,
    out(t) = z(t - d). With inertial delay, out(t) = z(t - d) when z kept that
    value on all of t - d, ..., t - 1, and out(t) = out(t - 1) otherwise.
    """
    evs = sorted(events, key=lambda e: e[0])
    hist, zhist = [], []
    for t in range(t_end + 1):
        cur = {n: init[n] for n in c.inputs}
        for te, n, v in evs:
            if te <= t:
                cur[n] = v
        for out, op, ins in c.gates:
            d = delay[out]
            if t < d:
                cur[out] = init[out]
            elif not inertial:
                cur[out] = zhist[t - d][out]
            elif all(zhist[s][out] == zhist[t - d][out] for s in range(t - d, t)):
                cur[out] = zhist[t - d][out]
            else:
                cur[out] = hist[t - 1][out]
        z = {out: eval2(op, [cur[n] for n in ins]) for out, op, ins in c.gates}
        hist.append(cur)
        zhist.append(z)
    return hist


def depth(c):
    memo = {n: 0 for n in c.inputs}

    def lev(n):
        if n not in memo:
            memo[n] = 1 + max(lev(m) for m in c.gates[c.driver[n]][2])
        return memo[n]

    return max([lev(n) for n in c.nets] + [0])


def test_time_wheel_order_and_overflow():
    w = TimeWheel(3)
    for t in (7, 0, 2, 2, 30):
        w.schedule(t, (str(t), 0, None))
    seen = []
    t = w.next_time()
    while t is not None:
        w.advance(t)
        seen += [(t, e[0]) for e in w.take(t)]
        t = w.next_time()
    assert seen == [(0, "0"), (2, "2"), (2, "2"), (7, "7"), (30, "30")]


@pytest.mark.parametrize("seed", range(6))
def test_zero_delay_equals_direct_evaluation(seed):
    rng = random.Random(seed)
    c = random_circuit(rng, rng.randint(2, 6), rng.randint(3, 25))
    zero = {g[0]: 0 for g in c.gates}
    vectors = list(all_vectors(c.inputs))
    init = {n: 0 for n in c.nets}
    events = [(10 * k, n, vec[n]) for k, vec in enumerate(vectors) for n in c.inputs]
    _, changes, _ = simulate(c, zero, init, events, 10 * len(vectors))
    for k, vec in enumerate(vectors):
        assert values_at(init, changes, 10 * k) == c.direct_eval(vec)


@pytest.mark.parametrize("seed", range(6))
def test_unit_delay_settles_to_direct_evaluation_within_depth(seed):
    rng = random.Random(100 + seed)
    c = random_circuit(rng, rng.randint(2, 6), rng.randint(3, 25))
    unit = {g[0]: 1 for g in c.gates}
    dep = depth(c)
    for vec in all_vectors(c.inputs):
        init = c.direct_eval({n: 1 - v for n, v in vec.items()})
        events = [(0, n, vec[n]) for n in c.inputs]
        val, changes, _ = simulate(c, unit, init, events, 1000)
        assert val == c.direct_eval(vec)
        assert all(t <= dep for t, _, _ in changes)


@pytest.mark.parametrize("seed", range(12))
@pytest.mark.parametrize("inertial", [False, True])
def test_integer_delays_match_step_reference(seed, inertial):
    rng = random.Random(200 + seed)
    c = random_circuit(rng, rng.randint(1, 4), rng.randint(2, 14), loops=seed % 2 == 1)
    delay = {g[0]: rng.randint(1, 3) for g in c.gates}
    init = {n: rng.randint(0, 1) for n in c.nets}
    events = [(rng.randint(0, 30), rng.choice(c.inputs), rng.randint(0, 1)) for _ in range(rng.randint(0, 12))]
    _, changes, _ = simulate(c, delay, init, events, 40, inertial=inertial)
    ref = step_reference(c, delay, init, events, 40, inertial=inertial)
    for t in range(41):
        assert values_at(init, changes, t) == ref[t]


def test_zero_delay_loop_oscillates():
    ring = Circuit(["a"], [("y", "NOT", ["y"])], ["y"])
    with pytest.raises(Oscillation):
        simulate(ring, {"y": 0}, {"a": 0, "y": 0}, [], 5, max_delta=50)
    _, changes, _ = simulate(ring, {"y": 1}, {"a": 0, "y": 0}, [], 6)
    assert waveform({"y": 0}, changes, "y") == [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1), (6, 0)]


def test_three_inverter_ring_has_period_six():
    ring = Circuit(["a"], [("x", "NOT", ["z"]), ("y", "NOT", ["x"]), ("z", "NOT", ["y"])], ["z"])
    init = {"a": 0, "x": 1, "y": 0, "z": 1}
    _, changes, _ = simulate(ring, {"x": 1, "y": 1, "z": 1}, init, [], 24)
    w = waveform(init, changes, "z")
    rises = [t for t, v in w[1:] if v == 1]
    assert [b - a for a, b in zip(rises, rises[1:])] == [6] * (len(rises) - 1)


def test_nor_latch_race():
    latch = Circuit(["s", "r"], [("q", "NOR", ["r", "qn"]), ("qn", "NOR", ["s", "q"])], ["q"])
    init = {"s": 1, "r": 1, "q": 0, "qn": 0}
    release = [(5, "s", 0), (5, "r", 0)]
    _, changes, _ = simulate(latch, {"q": 1, "qn": 1}, init, release, 40)
    assert len([1 for t, n, _ in changes if n == "q" and t > 30]) > 0  # equal delays: it keeps toggling
    _, changes, _ = simulate(latch, {"q": 1, "qn": 2}, init, release, 40)
    assert len([1 for t, n, _ in changes if n == "q" and t > 30]) > 0  # transport keeps the pulses alive
    val, changes, _ = simulate(latch, {"q": 1, "qn": 2}, init, release, 40, inertial=True)
    assert (val["q"], val["qn"]) == (1, 0) and max(t for t, _, _ in changes) == 6
    with pytest.raises(Oscillation):
        simulate(latch, {"q": 0, "qn": 0}, init, release, 40, max_delta=50)


def test_page_example_glitch():
    unit = {g[0]: 1 for g in HAZARD.gates}
    _, changes, _ = simulate(HAZARD, unit, HAZARD_INIT, [(10, "a", 0)], 30)
    assert waveform(HAZARD_INIT, changes, "y") == [(0, 1), (12, 0), (13, 1)]
    _, changes, _ = simulate(HAZARD, dict(unit, y=2), HAZARD_INIT, [(10, "a", 0)], 30, inertial=True)
    assert waveform(HAZARD_INIT, changes, "y") == [(0, 1)]
    _, changes, _ = simulate(HAZARD, dict(unit, y=2), HAZARD_INIT, [(10, "a", 0)], 30)
    assert waveform(HAZARD_INIT, changes, "y") == [(0, 1), (13, 0), (14, 1)]
    zero = {g[0]: 0 for g in HAZARD.gates}
    _, changes, _ = simulate(HAZARD, zero, HAZARD_INIT, [(10, "a", 0)], 30)
    assert waveform(HAZARD_INIT, changes, "y") == [(0, 1), (10, 0), (10, 1)]


def test_selective_trace_evaluates_only_the_fanout_cone():
    n = 40
    gates = [(f"x{k}", "NOT", [f"a{k}"]) for k in range(n)]
    c = Circuit([f"a{k}" for k in range(n)], gates, ["x0"])
    init = c.direct_eval({f"a{k}": 0 for k in range(n)})
    _, changes, evals = simulate(c, {f"x{k}": 1 for k in range(n)}, init, [(5, "a7", 1)], 20)
    assert evals == n + 1  # n at time 0, then one gate for the change of a7
    assert changes == [(5, "a7", 1), (6, "x7", 0)]
