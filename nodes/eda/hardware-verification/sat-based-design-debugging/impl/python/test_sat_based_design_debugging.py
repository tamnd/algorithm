# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-based-design-debugging/. The authors are listed in prov/1D5R8Y.jsonl.

import random
from itertools import combinations, product

from dpll import Solver
from sat_based_design_debugging import OPS, Circuit, at_most, correction_values, debug, simulate

BINARY = ("AND", "OR", "XOR", "NAND", "NOR", "XNOR")


# ------------------------------------------------------------------ references

def passes(c, tests, override_per_test=None):
    for j, (inputs, expected) in enumerate(tests):
        v = simulate(c, inputs, override_per_test[j] if override_per_test else None)
        if any(v[y] != expected[y] for y in c.outputs):
            return False
    return True


def brute_force_fixes(c, tests, size):
    """All gate sets of the given size where some values per test fix every test."""
    names = [g[0] for g in c.gates]
    out = []
    for fix in combinations(names, size):
        for bits in product((0, 1), repeat=size * len(tests)):
            over = [dict(zip(fix, bits[j * size:(j + 1) * size])) for j in range(len(tests))]
            if passes(c, tests, over):
                out.append(frozenset(fix))
                break
    return out


def random_circuit(rng, n_in, n_gates, n_out):
    inputs = [f"i{j}" for j in range(n_in)]
    gates = []
    for j in range(n_gates):
        pool = inputs + [g[0] for g in gates]
        if rng.random() < 0.15:
            gates.append((f"g{j}", "NOT", (rng.choice(pool),)))
        else:
            a, b = rng.sample(pool, 2)
            gates.append((f"g{j}", rng.choice(BINARY), (a, b)))
    return Circuit(inputs, gates, [g[0] for g in gates[-n_out:]])


def all_vectors(c):
    return [dict(zip(c.inputs, bits)) for bits in product((0, 1), repeat=len(c.inputs))]


def make_tests(golden, vectors):
    return [(v, {y: simulate(golden, v)[y] for y in golden.outputs}) for v in vectors]


def mutate(rng, c, count):
    """A copy of c with the type of count random two-input gates changed."""
    gates = list(c.gates)
    sites = rng.sample([j for j, g in enumerate(gates) if g[1] != "NOT"], count)
    for j in sites:
        name, op, fanins = gates[j]
        gates[j] = (name, rng.choice([o for o in BINARY if o != op]), fanins)
    return Circuit(c.inputs, gates, c.outputs), {gates[j][0] for j in sites}


# ----------------------------------------------------------------------- tests

EXAMPLE_GOLDEN = Circuit(["a", "b", "c"],
                         [("g1", "OR", ("a", "b")), ("g2", "AND", ("b", "c")),
                          ("g3", "XOR", ("g1", "c")), ("g4", "OR", ("g1", "g2"))],
                         ["g3", "g4"])
EXAMPLE_BUGGY = Circuit(["a", "b", "c"],
                        [("g1", "AND", ("a", "b")), ("g2", "AND", ("b", "c")),
                         ("g3", "XOR", ("g1", "c")), ("g4", "OR", ("g1", "g2"))],
                        ["g3", "g4"])


def test_example_of_the_page():
    failing = [v for v in all_vectors(EXAMPLE_BUGGY)
               if any(simulate(EXAMPLE_BUGGY, v)[y] != simulate(EXAMPLE_GOLDEN, v)[y] for y in ("g3", "g4"))]
    assert [(v["a"], v["b"], v["c"]) for v in failing] == [(0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1)]
    tests = make_tests(EXAMPLE_GOLDEN, failing[:2])
    k, fixes = debug(EXAMPLE_BUGGY, tests, 2)
    assert k == 1 and set(fixes) == {frozenset({"g1"})}
    assert correction_values(EXAMPLE_BUGGY, tests, frozenset({"g1"})) == [{"g1": 1}, {"g1": 1}]
    # With one test only, the two outputs can also be fixed at g3 and g4 together, but not by one other gate.
    k, fixes = debug(EXAMPLE_BUGGY, tests[:1], 2)
    assert k == 1 and set(fixes) == {frozenset({"g1"})}


def test_tseitin_gates_and_counter():
    for op in OPS:
        arity = 1 if op in ("NOT", "BUF") else 3
        for bits in product((0, 1), repeat=arity):
            s = Solver()
            ins = [s.new_var() for _ in bits]
            out = s.new_var()
            from sat_based_design_debugging import gate_clauses
            gate_clauses(s, op, out, ins)
            want = OPS[op](list(bits))
            units = [x if b else -x for x, b in zip(ins, bits)]
            assert s.solve(units + [out if want else -out]) is not None
            assert s.solve(units + [-out if want else out]) is None
    for n, k in product(range(1, 6), range(0, 6)):
        for bits in product((0, 1), repeat=n):
            s = Solver()
            xs = [s.new_var() for _ in range(n)]
            at_most(s, xs, k)
            ok = s.solve([x if b else -x for x, b in zip(xs, bits)]) is not None
            assert ok == (sum(bits) <= k)


def test_single_gate_debug_matches_brute_force():
    rng = random.Random(1606)
    checked = 0
    while checked < 120:
        golden = random_circuit(rng, 4, 10, 3)
        buggy, sites = mutate(rng, golden, 1)
        failing = [v for v in all_vectors(golden) if simulate(golden, v) != simulate(buggy, v)
                   and any(simulate(golden, v)[y] != simulate(buggy, v)[y] for y in golden.outputs)]
        if not failing:
            continue
        rng.shuffle(failing)
        tests = make_tests(golden, failing[:3])
        k, fixes = debug(buggy, tests, 1)
        assert k == 1
        assert set(fixes) == set(brute_force_fixes(buggy, tests, 1))
        assert sites <= set().union(*fixes)          # the real error site is found
        for fix in fixes:                            # each reported set really fixes the tests
            over = correction_values(buggy, tests, fix)
            assert passes(buggy, tests, over)
        checked += 1


def test_two_errors_against_brute_force():
    rng = random.Random(2005)
    checked = 0
    while checked < 40:
        golden = random_circuit(rng, 3, 8, 2)
        buggy, sites = mutate(rng, golden, 2)
        failing = [v for v in all_vectors(golden)
                   if any(simulate(golden, v)[y] != simulate(buggy, v)[y] for y in golden.outputs)]
        if not failing:
            continue
        tests = make_tests(golden, failing[:3])
        k, fixes = debug(buggy, tests, 2)
        assert k in (1, 2)
        assert brute_force_fixes(buggy, tests, k - 1) == []
        assert set(fixes) == set(brute_force_fixes(buggy, tests, k))
        if k == 2:
            assert all(len(f) == 2 for f in fixes)
        checked += 1


def test_passing_circuit_needs_no_fix_and_impossible_tests_have_none():
    rng = random.Random(3)
    golden = random_circuit(rng, 4, 10, 2)
    tests = make_tests(golden, all_vectors(golden))
    assert debug(golden, tests, 2) == (0, [frozenset()])
    # Two tests with the same inputs and different expected outputs: no circuit
    # can pass both, but the instance gives each test its own correction values,
    # so it is satisfiable. The theorem needs distinct input vectors.
    v, e = tests[0]
    flipped = {y: 1 - b for y, b in e.items()}
    k, fixes = debug(golden, [(v, e), (v, flipped)], 3)
    assert k >= 1 and set(fixes) == set(brute_force_fixes(golden, [(v, e), (v, flipped)], k))
    # With a bound below the number of outputs that must change, there is no answer.
    assert debug(golden, [(v, e), (v, flipped)], k - 1) == (-1, [])


def test_suspect_list_restricts_the_answer():
    tests = make_tests(EXAMPLE_GOLDEN, [{"a": 0, "b": 1, "c": 0}, {"a": 1, "b": 0, "c": 1}])
    k, fixes = debug(EXAMPLE_BUGGY, tests, 2, suspects=["g2", "g3", "g4"])
    assert k == 2 and frozenset({"g3", "g4"}) in fixes
    assert set(fixes) == set(f for f in brute_force_fixes(EXAMPLE_BUGGY, tests, 2) if "g1" not in f)
