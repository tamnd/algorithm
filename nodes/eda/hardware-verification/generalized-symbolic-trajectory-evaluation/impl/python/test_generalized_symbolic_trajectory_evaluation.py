# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-symbolic-trajectory-evaluation/. The authors are listed in prov/KNN3V9.jsonl.

import itertools
import random

from bdd import FALSE, TRUE, BDD
from generalized_symbolic_trajectory_evaluation import XV, Circuit, Edge, counterexample, gste, is_

OPS = ("BUF", "NOT", "AND", "OR", "NAND", "NOR", "XOR", "XNOR")


def boolean(op, xs):
    if op == "BUF":
        return xs[0]
    if op == "NOT":
        return 1 - xs[0]
    if op in ("AND", "NAND"):
        return int(all(xs)) ^ (op == "NAND")
    if op in ("OR", "NOR"):
        return int(any(xs)) ^ (op == "NOR")
    return (sum(xs) % 2) ^ (op == "XNOR")


def hold_register(buggy=False):
    """r loads d when en is 1 and keeps its value when en is 0 (the buggy one never clears)."""
    if buggy:
        gates = (("nen", "NOT", ("en",)), ("t1", "AND", ("en", "d")), ("m", "OR", ("t1", "r")))
    else:
        gates = (("nen", "NOT", ("en",)), ("t1", "AND", ("en", "d")),
                 ("t2", "AND", ("nen", "r")), ("m", "OR", ("t1", "t2")))
    return Circuit(("en", "d"), (("r", "m"),), gates)


def hold_graph(m):
    x = m.var(0)
    return [
        Edge(0, 0),                                                   # wait any number of cycles
        Edge(0, 1, ant=(is_("en", TRUE), is_("d", x))),               # load x
        Edge(1, 1, ant=(is_("en", FALSE),), cons=(is_("r", x),)),     # hold: r is x, for ever
    ]


def test_page_example_passes():
    m = BDD()
    r = gste(hold_register(), m, hold_graph(m))
    x = m.var(0)
    assert r.passed
    assert r.rounds == 3
    assert all(v == XV for v in r.sim[0].values())
    assert r.sim[1]["m"] == (x, m.neg(x)) and r.sim[1]["r"] == XV
    assert r.sim[2]["r"] == (x, m.neg(x)) and r.sim[2]["m"] == (x, m.neg(x))


def test_page_example_bug_is_found():
    m = BDD()
    r = gste(hold_register(buggy=True), m, hold_graph(m))
    x = m.var(0)
    assert not r.passed
    assert r.residual == m.neg(x)
    assert r.sim[2]["r"] == (x, FALSE)           # 1 when x is 1, X when x is 0
    assert counterexample(m, r) == {0: 0}
    # The failure is real: r = 1, then load 0, then hold, and r is still 1.
    assert violations(hold_register(buggy=True), m, hold_graph(m), {0: 0}, 3)


# ---------------------------------------------------------------- brute force

def runs(c, length):
    nl, ni = len(c.latches), len(c.inputs)
    for bits in itertools.product((0, 1), repeat=nl + ni * length):
        state = dict(zip([s for s, _ in c.latches], bits[:nl]))
        out = []
        for t in range(length):
            val = dict(state)
            val.update(zip(c.inputs, bits[nl + t * ni: nl + (t + 1) * ni]))
            for g, op, fi in c.gates:
                val[g] = boolean(op, [val[f] for f in fi])
            out.append(val)
            state = {s: val[n] for s, n in c.latches}
        yield out


def meets(m, cs, state, phi):
    return all(not m.evaluate(g, phi) or state[u] == m.evaluate(e, phi) for u, e, g in cs)


def active_edges(m, edges, run, phi, v0=0):
    """For each time k, the edges that end a path from v0 whose antecedents the run meets."""
    out = []
    reach = {v0}
    for state in run:
        act = {i for i, e in enumerate(edges) if e.src in reach and meets(m, e.ant, state, phi)}
        out.append(act)
        reach = {edges[i].dst for i in act}
    return out


def violations(c, m, edges, phi, length):
    found = []
    for run in runs(c, length):
        for k, act in enumerate(active_edges(m, edges, run, phi)):
            for i in act:
                if not meets(m, edges[i].cons, run[k], phi):
                    found.append((run, k, i))
    return found


def random_expr(m, rng, nv):
    k = rng.randrange(5)
    if k == 0:
        return rng.choice((FALSE, TRUE))
    v = m.var(rng.randrange(nv))
    if k == 1:
        return v
    if k == 2:
        return m.neg(v)
    w = m.var(rng.randrange(nv))
    return m.xor(v, w) if k == 3 else m.conj(v, w)


def random_circuit(rng):
    ni, nl = rng.randint(1, 2), rng.randint(1, 2)
    inputs = tuple(f"i{j}" for j in range(ni))
    lat = [f"s{j}" for j in range(nl)]
    nodes = list(inputs) + lat
    gates = []
    for j in range(rng.randint(1, 4)):
        op = rng.choice(OPS)
        ar = 1 if op in ("BUF", "NOT") else 2
        gates.append((f"g{j}", op, tuple(rng.choice(nodes) for _ in range(ar))))
        nodes.append(f"g{j}")
    return Circuit(inputs, tuple((s, rng.choice(nodes)) for s in lat), tuple(gates)), nodes


def random_graph(m, rng, nodes, nv):
    nvert = rng.randint(1, 3)
    edges = []
    for _ in range(rng.randint(1, 5)):
        guard = lambda: TRUE if rng.random() < 0.6 else random_expr(m, rng, nv)  # noqa: E731
        ant = tuple(is_(rng.choice(nodes), random_expr(m, rng, nv), guard()) for _ in range(rng.randint(0, 2)))
        cons = tuple(is_(rng.choice(nodes), random_expr(m, rng, nv), guard()) for _ in range(rng.randint(0, 1)))
        edges.append(Edge(rng.randrange(nvert), rng.randrange(nvert), ant, cons))
    return edges


def below_run(m, val, bit, phi):
    one, zero = m.evaluate(val[0], phi), m.evaluate(val[1], phi)
    return (not one or bit == 1) and (not zero or bit == 0)


def test_random_soundness_against_all_runs():
    rng = random.Random(4242)
    nv = 2
    checked = 0
    passed = 0
    for _ in range(500):
        c, nodes = random_circuit(rng)
        m = BDD()
        edges = random_graph(m, rng, nodes, nv)
        r = gste(c, m, edges)
        n_nodes, n_edges = len(nodes), len(edges)
        assert r.rounds <= 2 * n_nodes * n_edges + 1
        length = max(1, min(5, 9 // len(c.inputs) - len(c.latches)))
        all_runs = list(runs(c, length))
        for bits in itertools.product((0, 1), repeat=nv):
            phi = dict(enumerate(bits))
            bad = m.evaluate(r.residual, phi)
            passed += not bad
            for run in all_runs:
                for k, act in enumerate(active_edges(m, edges, run, phi)):
                    for i in act:
                        # The key lemma: sim(e) lies below every state where a run takes e.
                        for u, val in r.sim[i].items():
                            assert below_run(m, val, run[k][u], phi)
                        if not m.evaluate(r.failing[i], phi):
                            assert meets(m, edges[i].cons, run[k], phi)  # soundness
                        checked += 1
    assert checked > 5000 and passed > 500


def test_chain_with_everything_fixed_is_exact():
    # A chain of edges that sets all inputs at every step and all latches at the
    # first step has one run per assignment, and then the check is exact.
    rng = random.Random(99)
    for _ in range(300):
        c, nodes = random_circuit(rng)
        m = BDD()
        length = rng.randint(1, 3)
        edges = []
        for k in range(length):
            ant = tuple(is_(i, random_expr(m, rng, 2)) for i in c.inputs)
            if k == 0:
                ant += tuple(is_(s, random_expr(m, rng, 2)) for s, _ in c.latches)
            cons = (is_(rng.choice(nodes), random_expr(m, rng, 2)),)
            edges.append(Edge(k, k + 1, ant, cons))
        r = gste(c, m, edges)
        for bits in itertools.product((0, 1), repeat=2):
            phi = dict(enumerate(bits))
            assert bool(m.evaluate(r.residual, phi)) == bool(violations(c, m, edges, phi, length))


def test_unreachable_edge_is_never_checked():
    m = BDD()
    c = Circuit(("a",), (), (("z", "BUF", ("a",)),))
    edges = [Edge(1, 1, cons=(is_("z", TRUE),))]          # no path from v0 reaches vertex 1
    r = gste(c, m, edges)
    assert r.passed and r.sim[0]["z"] == (TRUE, TRUE)


def test_contradicting_antecedent_empties_the_edge():
    m = BDD()
    x = m.var(0)
    c = Circuit(("a",), (("r", "a"),), ())
    edges = [Edge(0, 1, ant=(is_("a", x), is_("a", m.neg(x)))), Edge(1, 1, cons=(is_("r", FALSE),))]
    r = gste(c, m, edges)
    assert r.passed                       # no run can take the first edge, so none reaches vertex 1
    assert r.sim[1]["r"] == (TRUE, TRUE)
