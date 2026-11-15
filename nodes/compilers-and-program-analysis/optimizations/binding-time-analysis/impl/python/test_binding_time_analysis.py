# SPDX-License-Identifier: MIT
import random
import unittest

import toylam
from binding_time_analysis import (
    Budget, NotTypable, annotate, congruent, infer, show_annotated, specialize,
)


def V(x):
    return ("var", x)


def I(k):
    return ("int", k)


POWER = ("app", ("app",
         ("fix", "p", "n", ("lam", "x",
          ("if", ("prim", "==", V("n"), I(0)), I(1),
           ("prim", "*", V("x"), ("app", ("app", V("p"), ("prim", "-", V("n"), I(1))), V("x")))))),
         V("s")), V("d"))

TWICE = ("let", "t", ("lam", "f", ("lam", "z", ("app", V("f"), ("app", V("f"), V("z"))))),
         ("app", ("app", V("t"), ("lam", "y", ("prim", "+", V("y"), V("s")))), V("d")))

LOOP = ("app", ("fix", "f", "n", ("if", ("prim", "<", V("d"), V("n")), V("n"),
                                  ("app", V("f"), ("prim", "+", V("n"), I(1))))), V("s"))


def value_of(rng, t):
    if t == ("bool",):
        return ("bool", rng.random() < 0.5)
    return ("int", rng.randint(-2, 4))


def run_original(e, values):
    for x, v in values.items():
        e = toylam.subst(e, x, v)
    return toylam.evaluate(e, 3000)


def random_cases(seed, count):
    """Typable random programs with inputs s (static) and d (dynamic),
    a result of base type and inputs of base type."""
    rng = random.Random(seed)
    out = []
    while len(out) < count:
        e = toylam.random_term(rng, rng.randint(2, 6), ("s", "d"))
        try:
            a = annotate(e, ["s"], ["d"])
        except NotTypable:
            continue
        if a.node[()][0] != "base":
            continue
        out.append((e, a))
    return rng, out


class AnalysisTest(unittest.TestCase):
    def test_power_annotation(self):
        a = annotate(POWER, ["s"], ["d"])
        self.assertEqual(show_annotated(a),
                         "(((fix p n -> (fun x -> (if (n == 0) then lift(1) else (x _* ((p (n - 1)) x))))) s) d)")
        a2 = annotate(POWER, ["d"], ["s"])
        self.assertEqual(show_annotated(a2),
                         "(((_fix p n -> (_fun x -> (_if (n _== lift(0)) then lift(1) else"
                         " (x _* ((p @ (n _- lift(1))) @ x))))) @ s) @ lift(d))")

    def test_random_annotations_are_congruent_and_least(self):
        _, cases = random_cases(1, 250)
        flips = 0
        for e, a in cases:
            self.assertEqual(congruent(a), [], toylam.show(e))
            # Least: making any single dynamic variable static breaks a rule.
            for v in sorted(a.dyn):
                self.assertNotEqual(congruent(a, a.dyn - {v}), [])
                flips += 1
        self.assertGreater(flips, 300)

    def test_all_static(self):
        # With no dynamic input and a base result, nothing is D, and the
        # residual program is the lifted value.
        e = ("prim", "+", V("s"), I(1))
        a = annotate(e, ["s", "d"], [])
        self.assertEqual(show_annotated(a), "(s + 1)")
        self.assertEqual(a.dyn, set())
        self.assertEqual(specialize(a, {"s": I(4), "d": I(0)}), I(5))

    def test_function_result_is_dynamic(self):
        e = ("lam", "x", ("prim", "+", V("x"), V("s")))
        a = annotate(e, ["s"], [])
        self.assertEqual(show_annotated(a), "(_fun x -> (x _+ lift(s)))")
        self.assertEqual(toylam.show(specialize(a, {"s": I(2)})), "(fun x1 -> (x1 + 2))")

    def test_a_bad_annotation_is_caught(self):
        a = annotate(POWER, ["s"], ["d"])
        self.assertNotEqual(congruent(a, set()), [])

    def test_untypable(self):
        with self.assertRaises(NotTypable):
            annotate(("app", I(1), I(2)), [], [])
        with self.assertRaises(NotTypable):
            annotate(("var", "q"), ["s"], ["d"])


class SpecializerTest(unittest.TestCase):
    def test_power(self):
        a = annotate(POWER, ["s"], ["d"])
        shown = [toylam.show(specialize(a, {"s": I(n)})) for n in range(4)]
        self.assertEqual(shown, ["1", "(d * 1)", "(d * (d * 1))", "(d * (d * (d * 1)))"])
        r = specialize(a, {"s": I(3)})
        self.assertEqual(toylam.evaluate(toylam.subst(r, "d", I(2))), ("value", I(8)))

    def test_twice(self):
        a = annotate(TWICE, ["s"], ["d"])
        r = specialize(a, {"s": I(5)})
        self.assertEqual(toylam.show(r), "(let y1 = (d + 5) in (y1 + 5))")
        self.assertEqual(toylam.evaluate(toylam.subst(r, "d", I(1))), ("value", I(11)))

    def test_static_loop_under_dynamic_test_does_not_stop(self):
        a = annotate(LOOP, ["s"], ["d"])
        self.assertEqual(show_annotated(a), "((fix f n -> (_if (d _< lift(n)) then lift(n) else (f (n + 1)))) s)")
        self.assertEqual(run_original(LOOP, {"s": I(0), "d": I(3)}), ("value", I(4)))
        with self.assertRaises(Budget):
            specialize(a, {"s": I(0)}, budget=50)

    def test_residual_agrees_with_original(self):
        rng, cases = random_cases(2, 400)
        agree = budget = 0
        for e, a in cases:
            types = infer(e, ["s", "d"])[1]
            for _ in range(3):
                s = value_of(rng, types[("in", "s")])
                d = value_of(rng, types[("in", "d")])
                want = run_original(e, {"s": s, "d": d})
                self.assertNotEqual(want[0], "stuck")
                if want[0] != "value":
                    continue
                try:
                    r = specialize(a, {"s": s})
                except Budget:
                    budget += 1
                    continue
                self.assertLessEqual(toylam.free_vars(r), {"d"})
                got = toylam.evaluate(toylam.subst(r, "d", d), 100000)
                self.assertEqual(got, want, toylam.show(e))
                agree += 1
        self.assertGreater(agree, 600)


if __name__ == "__main__":
    unittest.main()
