# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cutpoint-equivalence-checking/. The authors are listed in prov/MX8Z1M.jsonl.

import random

from bdd import BDD
from cutpoint_equivalence_checking import cutpoint_equivalence
from netlist import Netlist, mutate, random_netlist, rewrite, simulate

# The circuits of the page. A: o1 = a AND b, o2 = a.
# B: z = NOT(NOT a OR NOT b), w = z OR a, outputs (z, w).
A = Netlist(("a", "b"), (("g", "AND", ("a", "b")),), ("g", "a"))
B = Netlist(
    ("a", "b"),
    (
        ("p", "NOT", ("a",)),
        ("q", "NOT", ("b",)),
        ("r", "OR", ("p", "q")),
        ("z", "NOT", ("r",)),
        ("w", "OR", ("z", "a")),
    ),
    ("z", "w"),
)


def truth_tables(net: Netlist) -> list[int]:
    """Oracle: the truth table of every output, by simulation of all 2^n input vectors at once."""
    n = len(net.inputs)
    rows = 1 << n
    mask = (1 << rows) - 1
    words = {}
    for i, x in enumerate(net.inputs):
        w = 0
        for r in range(rows):
            if (r >> i) & 1:
                w |= 1 << r
        words[x] = w
    val = simulate(net, words, mask)
    return [val[o] for o in net.outputs]


def outputs_at(net: Netlist, point: dict[str, int]) -> list[int]:
    val = simulate(net, dict(point), 1)
    return [val[o] for o in net.outputs]


def test_page_example_is_equivalent_after_one_false_negative():
    res = cutpoint_equivalence(A, B)
    assert res.equivalent and res.counterexample is None
    assert res.merges == 2
    assert res.false_negatives == 1
    assert truth_tables(A) == truth_tables(B)


def test_the_cut_miter_of_the_page_has_a_false_counterexample():
    bdd = BDD()
    a, v = bdd.var(0), bdd.var(2)
    cut_miter = bdd.xor(bdd.disj(v, a), a)
    assert cut_miter == bdd.conj(v, bdd.neg(a))
    assert bdd.sat_one(cut_miter) == {0: 0, 2: 1}
    # No real input vector gives z = 1 and a = 0, and no input vector separates the circuits.
    for av in (0, 1):
        for bv in (0, 1):
            assert outputs_at(A, {"a": av, "b": bv}) == outputs_at(B, {"a": av, "b": bv})
    # Moving the cut back to the inputs: v := a AND b gives the exact miter, which is 0.
    assert bdd.compose(cut_miter, 2, bdd.conj(a, bdd.var(1))) == 0


def test_real_difference_gives_a_true_counterexample():
    b2 = Netlist(B.inputs, B.gates[:-1] + (("w", "OR", ("z", "b")),), B.outputs)
    res = cutpoint_equivalence(A, b2)
    assert not res.equivalent
    assert outputs_at(A, res.counterexample) != outputs_at(b2, res.counterexample)


def test_identical_and_constant_circuits():
    c = Netlist(("x",), (("k", "CONST1", ()), ("y", "AND", ("x", "k"))), ("y",))
    d = Netlist(("x",), (), ("x",))
    assert cutpoint_equivalence(c, c).equivalent
    assert cutpoint_equivalence(c, d).equivalent
    e = Netlist(("x",), (("k", "CONST0", ()),), ("k",))
    res = cutpoint_equivalence(c, e)
    assert not res.equivalent and res.counterexample == {"x": 1}


def test_random_against_exhaustive_simulation():
    rng = random.Random(20260)
    seen_false_negative = 0
    seen_different = 0
    for case in range(600):
        n = rng.randint(1, 5)
        a = random_netlist(rng, n, 0, rng.randint(1, 9), rng.randint(1, 3))
        b = rewrite(a, rng)
        if case % 2:
            b = mutate(b, rng)
        res = cutpoint_equivalence(a, b, width=rng.choice([1, 4, 64]), seed=case)
        same = truth_tables(a) == truth_tables(b)
        assert res.equivalent == same
        if not same:
            seen_different += 1
            assert outputs_at(a, res.counterexample) != outputs_at(b, res.counterexample)
        seen_false_negative += res.false_negatives
    assert seen_different > 50
    assert seen_false_negative > 0
