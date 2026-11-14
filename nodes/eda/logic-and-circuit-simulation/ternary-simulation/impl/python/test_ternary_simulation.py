# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ternary-simulation/. The authors are listed in prov/9Z1Y7X.jsonl.

import itertools
import random

import pytest

from logicnet import OPS, X, Circuit, all_vectors, completions, eval2, eval3, random_circuit
from ternary_simulation import eichelberger, evaluate, leq, report, step

HAZARD = Circuit(
    ["a", "b", "c"],
    [("na", "NOT", ["a"]), ("p", "AND", ["a", "b"]), ("q", "AND", ["na", "c"]), ("y", "OR", ["p", "q"])],
    ["y"],
)
FIXED = Circuit(
    ["a", "b", "c"],
    [("na", "NOT", ["a"]), ("p", "AND", ["a", "b"]), ("q", "AND", ["na", "c"]), ("r", "AND", ["b", "c"]),
     ("y", "OR", ["p", "q", "r"])],
    ["y"],
)
NAND_LATCH = Circuit(["sn", "rn"], [("q", "NAND", ["sn", "qn"]), ("qn", "NAND", ["rn", "q"])], ["q"])


def gate_state(c, full):
    return {g[0]: full[g[0]] for g in c.gates}


def test_gate_tables_are_monotone_and_exact():
    for op in OPS:
        for k in ((1,) if op in ("NOT", "BUF") else (2, 3)):
            for u in itertools.product((0, 1, X), repeat=k):
                outs = {eval2(op, list(v)) for v in itertools.product(*[(0, 1) if x == X else (x,) for x in u])}
                assert eval3(op, list(u)) == (outs.pop() if len(outs) == 1 else X)
                for w in itertools.product((0, 1, X), repeat=k):
                    if all(wi == X or wi == ui for ui, wi in zip(u, w)):
                        r, rw = eval3(op, list(u)), eval3(op, list(w))
                        assert rw == X or rw == r


@pytest.mark.parametrize("seed", range(12))
def test_combinational_soundness_against_all_completions(seed):
    rng = random.Random(seed)
    c = random_circuit(rng, rng.randint(1, 8), rng.randint(1, 30))
    for _ in range(40):
        u = {n: rng.choice((0, 1, X)) for n in c.inputs}
        got = evaluate(c, u)
        assert got == gate_state(c, c.direct_eval(u, three=True))
        seen = {g[0]: set() for g in c.gates}
        for v in completions(u):
            full = c.direct_eval(v)
            for n in seen:
                seen[n].add(full[n])
        for n, vals in seen.items():
            if got[n] != X:
                assert vals == {got[n]}


def random_tree(rng, n_inputs):
    """A fanout-free circuit: every input and every gate output is read at most once."""
    free = [f"i{k}" for k in range(n_inputs)]
    gates = []
    while len(free) > 1:
        op = rng.choice(("AND", "OR", "NAND", "NOR", "XOR", "XNOR"))
        k = min(len(free), rng.randint(2, 3))
        ins = [free.pop(rng.randrange(len(free))) for _ in range(k)]
        out = f"g{len(gates)}"
        if rng.random() < 0.3:
            gates.append((out + "n", "NOT", [out]))
            gates.append((out, op, ins))
            out += "n"
        else:
            gates.append((out, op, ins))
        free.append(out)
    return Circuit([f"i{k}" for k in range(n_inputs)], gates, free)


@pytest.mark.parametrize("seed", range(8))
def test_exact_on_fanout_free_circuits(seed):
    rng = random.Random(30 + seed)
    c = random_tree(rng, rng.randint(2, 8))
    for _ in range(30):
        u = {n: rng.choice((0, 1, X)) for n in c.inputs}
        got = evaluate(c, u)[c.outputs[0]]
        vals = {c.direct_eval(v)[c.outputs[0]] for v in completions(u)}
        assert got == (vals.pop() if len(vals) == 1 else X)


def test_x_pessimism_on_reconvergent_fanout():
    mux = Circuit(["s", "a", "b"], [("ns", "NOT", ["s"]), ("p", "AND", ["s", "a"]), ("q", "AND", ["ns", "b"]),
                                    ("y", "OR", ["p", "q"])], ["y"])
    u = {"s": X, "a": 1, "b": 1}
    assert evaluate(mux, u)["y"] == X
    assert {mux.direct_eval(v)["y"] for v in completions(u)} == {1}


def test_page_example_hazard_and_consensus_fix():
    a, b = {"a": 1, "b": 1, "c": 1}, {"a": 0, "b": 1, "c": 1}
    s0 = gate_state(HAZARD, HAZARD.direct_eval(a))
    s_a, t_b, ka, kb = eichelberger(HAZARD, a, b, s0)
    assert s_a == {"na": X, "p": X, "q": X, "y": X} and (ka, kb) == (2, 3)
    assert t_b == {"na": 1, "p": 0, "q": 1, "y": 1}
    assert report(s0, s_a, t_b)["static_hazard"] == ["y"]
    s0 = gate_state(FIXED, FIXED.direct_eval(a))
    s_a, t_b, _, _ = eichelberger(FIXED, a, b, s0)
    assert s_a["y"] == 1 and report(s0, s_a, t_b)["static_hazard"] == []


def test_nand_latch_race_and_clean_set():
    s0 = {"q": 1, "qn": 1}  # stable with sn = rn = 0
    s_a, t_b, _, _ = eichelberger(NAND_LATCH, {"sn": 0, "rn": 0}, {"sn": 1, "rn": 1}, s0)
    assert t_b == {"q": X, "qn": X}
    s0 = {"q": 0, "qn": 1}  # stable with sn = rn = 1
    s_a, t_b, _, _ = eichelberger(NAND_LATCH, {"sn": 1, "rn": 1}, {"sn": 0, "rn": 1}, s0)
    assert s_a == {"q": X, "qn": X} and t_b == {"q": 1, "qn": 0}


def test_cannot_tell_a_clean_change_from_a_dynamic_hazard():
    buf = Circuit(["a"], [("y", "BUF", ["a"])], ["y"])
    s_a, t_b, _, _ = eichelberger(buf, {"a": 0}, {"a": 1}, {"y": 0})
    assert s_a == {"y": X} and t_b == {"y": 1}


def stable_states(c, a):
    names = [g[0] for g in c.gates]
    for bits in itertools.product((0, 1), repeat=len(names)):
        s = dict(zip(names, bits))
        if step(c, a, s) == s:
            yield s


def gmw_reachable(c, b, s0):
    """Every state reachable when any nonempty set of unstable gates may change at each step."""
    seen = {tuple(sorted(s0.items()))}
    todo = [s0]
    while todo:
        s = todo.pop()
        f = step(c, b, s)
        unstable = [n for n in s if f[n] != s[n]]
        for r in range(1, len(unstable) + 1):
            for sub in itertools.combinations(unstable, r):
                t = dict(s)
                for n in sub:
                    t[n] = f[n]
                key = tuple(sorted(t.items()))
                if key not in seen:
                    seen.add(key)
                    todo.append(t)
    return [dict(k) for k in seen]


@pytest.mark.parametrize("seed", range(40))
def test_phases_bound_every_gmw_run(seed):
    rng = random.Random(500 + seed)
    c = random_circuit(rng, rng.randint(1, 3), rng.randint(2, 6), loops=True)
    a = {n: rng.randint(0, 1) for n in c.inputs}
    b = {n: rng.randint(0, 1) for n in c.inputs}
    for s0 in list(stable_states(c, a))[:3]:
        s_a, t_b, ka, kb = eichelberger(c, a, b, s0)
        n = len(c.gates)
        assert ka <= n and kb <= n
        assert leq(s0, s_a) and leq(t_b, s_a)
        for r in gmw_reachable(c, b, s0):
            assert leq(r, s_a)
            if step(c, b, r) == r:
                assert leq(r, t_b)


def transport_run(c, delay, a, b, s0, t_end):
    """Unit-time step simulation with integer transport delays: out(t) = f(values at t - d).

    The inputs are a before time 0 and b from time 0. Before time 0 the circuit rests in s0, which is stable under a.
    """
    hist = []
    for t in range(t_end + 1):
        cur = dict(b)
        for out, op, ins in c.gates:
            d = delay[out]
            cur[out] = s0[out] if t - d < 0 else eval2(op, [hist[t - d][n] for n in ins])
        hist.append(cur)
    return hist


@pytest.mark.parametrize("seed", range(10))
def test_binary_after_phase_a_means_no_glitch_for_any_delays(seed):
    rng = random.Random(900 + seed)
    c = random_circuit(rng, rng.randint(2, 5), rng.randint(3, 12))
    for _ in range(5):
        a = {n: rng.randint(0, 1) for n in c.inputs}
        b = {n: rng.randint(0, 1) for n in c.inputs}
        s0 = gate_state(c, c.direct_eval(a))
        s_a, _, _, _ = eichelberger(c, a, b, s0)
        for _ in range(20):
            delay = {g[0]: rng.randint(1, 4) for g in c.gates}
            hist = transport_run(c, delay, a, b, s0, 4 * len(c.gates) + 4)
            for n, v in s_a.items():
                if v != X:
                    assert all(h[n] == v for h in hist)


def test_unit_delays_show_the_hazard_found_by_phase_a():
    a, b = {"a": 1, "b": 1, "c": 1}, {"a": 0, "b": 1, "c": 1}
    s0 = gate_state(HAZARD, HAZARD.direct_eval(a))
    hist = transport_run(HAZARD, {g[0]: 1 for g in HAZARD.gates}, a, b, s0, 6)
    assert [h["y"] for h in hist] == [1, 1, 0, 1, 1, 1, 1]
