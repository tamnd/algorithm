# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symbolic-simulation/. The authors are listed in prov/HYGZ61.jsonl.

import itertools
import random

from bdd import FALSE, TRUE, BDD
from symbolic_simulation import OPS, Circuit, instance, symbolic_simulation

# The circuit of the page: latch r (reset to 0), n = r XOR a, z = r AND a.
PAGE = Circuit(
    inputs=("a",),
    latches=(("r", "n", 0),),
    gates=(("n", "XOR", ("r", "a")), ("z", "AND", ("r", "a"))),
    outputs=("z",),
)


def concrete(c: Circuit, init: dict[str, int], seq: list[dict[str, int]]) -> list[dict[str, int]]:
    """Plain two-valued simulation of one run: the oracle."""
    state = {s: (init[s] if v is None else v) for s, _, v in c.latches}
    out = []
    for vec in seq:
        val = dict(vec)
        val.update(state)
        for name, op, fi in c.gates:
            xs = [val[f] for f in fi]
            if op == "BUF":
                r = xs[0]
            elif op == "NOT":
                r = 1 - xs[0]
            elif op in ("AND", "NAND"):
                r = int(all(xs)) ^ (op == "NAND")
            elif op in ("OR", "NOR"):
                r = int(any(xs)) ^ (op == "NOR")
            else:
                r = (sum(xs) % 2) ^ (op == "XNOR")
            val[name] = r
        out.append({o: val[o] for o in c.outputs})
        state = {s: val[n] for s, n, _ in c.latches}
    return out


def all_runs(c: Circuit, k: int):
    unknown = [s for s, _, v in c.latches if v is None]
    for bits in itertools.product((0, 1), repeat=len(unknown) + k * len(c.inputs)):
        init = dict(zip(unknown, bits))
        rest = bits[len(unknown):]
        seq = [dict(zip(c.inputs, rest[t * len(c.inputs):(t + 1) * len(c.inputs)])) for t in range(k)]
        yield init, seq


def check_against_concrete(c: Circuit, k: int) -> int:
    tr = symbolic_simulation(c, k)
    runs = 0
    for init, seq in all_runs(c, k):
        a = instance(tr, init, seq)
        want = concrete(c, init, seq)
        for t in range(k):
            for o in c.outputs:
                assert tr.mgr.evaluate(tr.outputs[t][o], a) == want[t][o]
        runs += 1
    return runs


def test_page_example():
    tr = symbolic_simulation(PAGE, 3)
    m = tr.mgr
    a0, a1, a2 = (m.var(tr.variables[("in", "a", t)]) for t in range(3))
    assert tr.outputs[0]["z"] == FALSE
    assert tr.outputs[1]["z"] == m.conj(a0, a1)
    assert tr.outputs[2]["z"] == m.conj(m.xor(a0, a1), a2)
    assert tr.states[2]["r"] == m.xor(a0, a1)
    # BDD sizes, terminals included, as in the table of the page.
    assert [m.size(tr.outputs[t]["z"]) for t in range(3)] == [1, 4, 6]
    assert check_against_concrete(PAGE, 3) == 8
    # The property of the page: z is never 1 in two cycles in a row.
    assert m.conj(tr.outputs[1]["z"], tr.outputs[2]["z"]) == FALSE


def test_unknown_initial_state():
    c = Circuit(PAGE.inputs, (("r", "n", None),), PAGE.gates, PAGE.outputs)
    tr = symbolic_simulation(c, 3)
    m = tr.mgr
    s = m.var(tr.variables[("init", "r")])
    a = [m.var(tr.variables[("in", "a", t)]) for t in range(3)]
    assert tr.outputs[0]["z"] == m.conj(s, a[0])
    assert tr.states[2]["r"] == m.xor(m.xor(s, a[0]), a[1])
    assert check_against_concrete(c, 3) == 16


def test_one_bdd_per_function():
    # Two different circuits for the same function give the same node: the check
    # of equivalence is one comparison of integers.
    c1 = Circuit(("x", "y"), (), (("o", "XOR", ("x", "y")),), ("o",))
    c2 = Circuit(
        ("x", "y"),
        (),
        (("p", "NAND", ("x", "y")), ("q", "OR", ("x", "y")), ("o", "AND", ("p", "q"))),
        ("o",),
    )
    m = BDD()
    t1 = symbolic_simulation(c1, 1, m)
    t2 = symbolic_simulation(c2, 1, m)
    assert t1.outputs[0]["o"] == t2.outputs[0]["o"]


def test_constant_and_zero_cycles():
    c = Circuit(("x",), (), (("nx", "NOT", ("x",)), ("o", "AND", ("x", "nx"))), ("o",))
    tr = symbolic_simulation(c, 2)
    assert tr.outputs[0]["o"] == FALSE and tr.outputs[1]["o"] == FALSE
    assert symbolic_simulation(c, 0).outputs == []
    c1 = Circuit(("x",), (), (("o", "XNOR", ("x", "x")),), ("o",))
    assert symbolic_simulation(c1, 1).outputs[0]["o"] == TRUE


def random_circuit(rng: random.Random) -> tuple[Circuit, int]:
    n_in = rng.randint(1, 2)
    n_latch = rng.randint(0, 2)
    k = rng.randint(1, 3)
    inputs = tuple(f"x{i}" for i in range(n_in))
    lat_names = [f"s{i}" for i in range(n_latch)]
    inits = [rng.choice((0, 1, None)) for _ in lat_names]
    while sum(v is None for v in inits) + k * n_in > 8:
        k -= 1
    nodes = list(inputs) + lat_names
    gates = []
    for g in range(rng.randint(1, 7)):
        op = rng.choice(OPS)
        ar = 1 if op in ("BUF", "NOT") else rng.randint(2, 3)
        gates.append((f"g{g}", op, tuple(rng.choice(nodes) for _ in range(ar))))
        nodes.append(f"g{g}")
    latches = tuple((s, rng.choice(nodes), v) for s, v in zip(lat_names, inits))
    outputs = tuple(sorted(set(rng.choice(nodes) for _ in range(2))))
    return Circuit(inputs, latches, tuple(gates), outputs), k


def test_random_circuits_against_every_run():
    rng = random.Random(20261114)
    runs = 0
    for _ in range(600):
        c, k = random_circuit(rng)
        runs += check_against_concrete(c, k)
    assert runs > 5000
