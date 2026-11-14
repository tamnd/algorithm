# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symbolic-trajectory-evaluation/. The authors are listed in prov/NEAHJQ.jsonl.

import itertools
import random

from bdd import FALSE, TRUE, BDD
from symbolic_trajectory_evaluation import Circuit, counterexample, gate_value, is_, leq, ste

OPS = ("BUF", "NOT", "AND", "OR", "NAND", "NOR", "XOR", "XNOR")
X, ZERO, ONE, TOP = (FALSE, FALSE), (FALSE, TRUE), (TRUE, FALSE), (TRUE, TRUE)
LATTICE = (X, ZERO, ONE, TOP)


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


def below(a, b):
    return (not a[0] or b[0]) and (not a[1] or b[1])


def pipeline(second="XOR"):
    """The circuit of the page: r1 <- a AND b, r2 <- r1 op c, and an unrelated toggle q."""
    return Circuit(
        inputs=("a", "b", "c"),
        latches=(("r1", "g1"), ("r2", "g2"), ("q", "nq")),
        gates=(("g1", "AND", ("a", "b")), ("g2", second, ("r1", "c")), ("nq", "NOT", ("q",))),
    )


def page_assertion(m):
    x, y, z = m.var(0), m.var(1), m.var(2)
    a = [is_(0, "a", x), is_(0, "b", y), is_(1, "c", z)]
    c = [is_(2, "r2", m.xor(m.conj(x, y), z))]
    return a, c


def test_gate_tables_are_monotone_and_exact():
    m = BDD()
    for op in OPS:
        n = 1 if op in ("BUF", "NOT") else 2
        for args in itertools.product(LATTICE, repeat=n):
            out = gate_value(m, op, list(args))
            for bigger in itertools.product(LATTICE, repeat=n):
                if all(below(a, b) for a, b in zip(args, bigger)):
                    assert below(out, gate_value(m, op, list(bigger)))
            if TOP in args:
                continue
            # On 0, 1 and X the table is Kleene's: binary exactly when all completions agree.
            comps = [[0, 1] if a == X else [int(a == ONE)] for a in args]
            vals = {boolean(op, list(xs)) for xs in itertools.product(*comps)}
            want = X if len(vals) == 2 else (ONE if vals == {1} else ZERO)
            assert out == want


def test_page_example_passes():
    m = BDD()
    a, c = page_assertion(m)
    r = ste(pipeline(), m, a, c)
    assert r.passed and r.antecedent_failure == FALSE
    x, y, z = m.var(0), m.var(1), m.var(2)
    assert r.trajectory[1]["r1"] == (m.conj(x, y), m.neg(m.conj(x, y)))
    assert r.trajectory[2]["c"] == X and r.trajectory[2]["q"] == X
    want = m.xor(m.conj(x, y), z)
    assert r.trajectory[1]["g2"] == (want, m.neg(want))
    assert r.trajectory[2]["r2"] == (want, m.neg(want))
    assert r.trajectory[0]["r1"] == X and r.trajectory[1]["g1"] == X


def test_page_example_bug_is_found():
    m = BDD()
    a, c = page_assertion(m)
    r = ste(pipeline("OR"), m, a, c)
    assert not r.passed
    x, y, z = m.var(0), m.var(1), m.var(2)
    assert r.residual == m.conj(m.conj(x, y), z)
    assert counterexample(m, r) == {0: 1, 1: 1, 2: 1}


def test_x_is_too_weak_without_a_variable():
    # z = a OR NOT a is 1 in every run, but with a left at X the check fails.
    c = Circuit(("a",), (), (("na", "NOT", ("a",)), ("z", "OR", ("a", "na"))))
    m = BDD()
    assert not ste(c, m, [], [is_(0, "z", TRUE)]).passed
    assert ste(c, m, [is_(0, "a", m.var(0))], [is_(0, "z", TRUE)]).passed


def test_antecedent_failure_is_vacuous():
    c = Circuit(("a",), (), (("z", "BUF", ("a",)),))
    m = BDD()
    x, y = m.var(0), m.var(1)
    r = ste(c, m, [is_(0, "a", x), is_(0, "a", y)], [is_(0, "z", FALSE)])
    assert r.antecedent_failure == m.xor(x, y)
    assert r.residual == m.conj(x, y)


# ---------------------------------------------------------------- brute force

def runs(c, depth):
    """Every binary run of length depth + 1: all initial latch values and all inputs."""
    nl, ni = len(c.latches), len(c.inputs)
    for bits in itertools.product((0, 1), repeat=nl + ni * (depth + 1)):
        state = dict(zip([s for s, _ in c.latches], bits[:nl]))
        out = []
        for t in range(depth + 1):
            val = dict(state)
            val.update(zip(c.inputs, bits[nl + t * ni: nl + (t + 1) * ni]))
            for g, op, fi in c.gates:
                val[g] = boolean(op, [val[f] for f in fi])
            out.append(val)
            state = {s: val[n] for s, n in c.latches}
        yield out


def satisfies(m, cs, run, phi):
    return all(not m.evaluate(g, phi) or run[t][u] == m.evaluate(e, phi) for t, u, e, g in cs)


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


def random_case(rng):
    ni, nl = rng.randint(1, 2), rng.randint(0, 2)
    inputs = tuple(f"i{j}" for j in range(ni))
    lat = [f"s{j}" for j in range(nl)]
    nodes = list(inputs) + lat
    gates = []
    for j in range(rng.randint(1, 5)):
        op = rng.choice(OPS)
        ar = 1 if op in ("BUF", "NOT") else 2
        gates.append((f"g{j}", op, tuple(rng.choice(nodes) for _ in range(ar))))
        nodes.append(f"g{j}")
    c = Circuit(inputs, tuple((s, rng.choice(nodes)) for s in lat), tuple(gates))
    depth = rng.randint(0, 2)
    while nl + ni * (depth + 1) > 8:
        depth -= 1
    return c, nodes, depth


def test_random_soundness_against_all_runs():
    rng = random.Random(5150)
    nv = 2
    checked = 0
    for _ in range(500):
        c, nodes, depth = random_case(rng)
        m = BDD()
        guard = lambda: TRUE if rng.random() < 0.6 else random_expr(m, rng, nv)  # noqa: E731
        ant = [is_(rng.randint(0, depth), rng.choice(nodes), random_expr(m, rng, nv), guard())
               for _ in range(rng.randint(0, 4))]
        con = [is_(rng.randint(0, depth), rng.choice(nodes), random_expr(m, rng, nv), guard())
               for _ in range(rng.randint(1, 2))]
        r = ste(c, m, ant, con)
        all_runs = list(runs(c, depth))
        for bits in itertools.product((0, 1), repeat=nv):
            phi = dict(enumerate(bits))
            good = [run for run in all_runs if satisfies(m, ant, run, phi)]
            if m.evaluate(r.antecedent_failure, phi):
                assert not good  # TOP means that no run meets the antecedent
            for run in good:
                # The key lemma: the defining trajectory lies below every run that meets A.
                for t, tau in enumerate(r.trajectory):
                    for u, (one, zero) in tau.items():
                        if m.evaluate(one, phi):
                            assert run[t][u] == 1
                        if m.evaluate(zero, phi):
                            assert run[t][u] == 0
                if not m.evaluate(r.residual, phi):
                    assert satisfies(m, con, run, phi)  # soundness
                checked += 1
    assert checked > 1000


def test_complete_when_antecedent_fixes_all_inputs_and_state():
    # With every input and initial latch value fixed, the trajectory is binary,
    # so a failure is a real counterexample.
    rng = random.Random(77)
    for _ in range(300):
        c, nodes, depth = random_case(rng)
        m = BDD()
        ant = [is_(0, s, random_expr(m, rng, 2)) for s, _ in c.latches]
        ant += [is_(t, i, random_expr(m, rng, 2)) for t in range(depth + 1) for i in c.inputs]
        con = [is_(rng.randint(0, depth), rng.choice(nodes), random_expr(m, rng, 2))]
        r = ste(c, m, ant, con)
        assert r.antecedent_failure == FALSE
        for bits in itertools.product((0, 1), repeat=2):
            phi = dict(enumerate(bits))
            good = [run for run in runs(c, depth) if satisfies(m, ant, run, phi)]
            assert len(good) == 1
            assert bool(m.evaluate(r.residual, phi)) == (not satisfies(m, con, good[0], phi))


def test_leq_on_constants():
    m = BDD()
    for a in LATTICE:
        for b in LATTICE:
            assert leq(m, a, b) == (TRUE if below(a, b) else FALSE)
