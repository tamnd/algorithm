# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verification-condition-generation/. The authors are listed in prov/7VA8XP.jsonl.

import itertools
import random
import unittest

from verification_condition_generation import (
    compact_vc,
    dag_size,
    evaluate,
    run,
    size,
    valid_on_box,
    vcgen,
)


def V(x):
    return ("var", x)


def K(c):
    return ("int", c)


def seqs(*ss):
    out = ss[-1]
    for s in reversed(ss[:-1]):
        out = ("seq", s, out)
    return out


# The worked example of the page: division by repeated subtraction.
PRE = ("and", ("<=", K(0), V("x")), ("<", K(0), V("y")))
INV = ("and", ("==", V("x"), ("+", ("*", V("q"), V("y")), V("r"))), ("<=", K(0), V("r")))
BODY = ("seq", ("assign", "r", ("-", V("r"), V("y"))), ("assign", "q", ("+", V("q"), K(1))))
POST = ("and", ("==", V("x"), ("+", ("*", V("q"), V("y")), V("r"))),
        ("and", ("<=", K(0), V("r")), ("<", V("r"), V("y"))))


def division(inv):
    return seqs(("assign", "q", K(0)), ("assign", "r", V("x")), ("while", ("<=", V("y"), V("r")), inv, BODY))


DIV_NAMES = ["x", "y", "q", "r"]


def toward_zero(n):
    step = ("if", ("<", K(0), V("x")), ("assign", "x", ("-", V("x"), K(1))), ("assign", "x", ("+", V("x"), K(1))))
    return seqs(*([step] * n))


def outcome_ok(res, post):
    kind, final = res
    if kind == "ok":
        return evaluate(post, final)
    return kind == "blocked"


class TestPage(unittest.TestCase):
    def test_division_vcs(self):
        vcs = vcgen(PRE, division(INV), POST)
        self.assertEqual(len(vcs), 3)
        self.assertEqual([size(f) for f in vcs], [19, 33, 32])
        for f in vcs:
            self.assertIsNone(valid_on_box(f, DIV_NAMES, -6, 6))

    def test_division_run(self):
        heads = []
        res = run(division(INV), {"x": 7, "y": 2, "q": 0, "r": 0}, heads=heads)
        self.assertEqual(res, ("ok", {"x": 7, "y": 2, "q": 3, "r": 1}))
        self.assertEqual([(h["q"], h["r"]) for h in heads], [(0, 7), (1, 5), (2, 3), (3, 1)])
        for h in heads:
            self.assertTrue(evaluate(INV, h))

    def test_weak_invariant_gives_invalid_vc(self):
        weak = ("==", V("x"), ("+", ("*", V("q"), V("y")), V("r")))
        vcs = vcgen(PRE, division(weak), POST)
        self.assertIsNone(valid_on_box(vcs[0], DIV_NAMES, -6, 6))
        self.assertIsNone(valid_on_box(vcs[1], DIV_NAMES, -6, 6))
        self.assertIsNotNone(valid_on_box(vcs[2], DIV_NAMES, -6, 6))
        # The program is still correct on every start state of the box.
        for x, y in itertools.product(range(0, 7), range(1, 7)):
            res = run(division(weak), {"x": x, "y": y, "q": 0, "r": 0})
            self.assertTrue(outcome_ok(res, POST))

    def test_bounded_check_is_not_a_proof(self):
        f = vcgen(("bool", True), ("skip",), ("<", V("x"), K(100)))[0]
        self.assertIsNone(valid_on_box(f, ["x"], -8, 8))
        self.assertFalse(evaluate(f, {"x": 100}))

    def test_exponential_example(self):
        tree = []
        for n in range(1, 11):
            pre = ("and", ("<=", K(-n), V("x")), ("<=", V("x"), K(n)))
            post = ("and", ("<=", K(0), V("x")), ("<=", V("x"), K(1)))
            s = toward_zero(n)
            naive = vcgen(pre, s, post)[0]
            compact = compact_vc(pre, s, post)
            tree.append(size(naive))
            if n >= 2:
                self.assertEqual(dag_size(naive), 10 * 2 ** n + 2)
            self.assertEqual(size(compact), 15 + 26 * n)
            self.assertIsNone(valid_on_box(naive, ["x"], -12, 12))
            self.assertIsNone(valid_on_box(compact, ["x"], -12, 12))
        self.assertEqual(tree, [40, 106, 270, 662, 1574, 3654, 8326, 18694, 41478, 91142])

    def test_compact_needs_loop_free(self):
        with self.assertRaises(ValueError):
            compact_vc(PRE, division(INV), POST)


NAMES = ["x", "y", "z"]
LO, HI = -2, 2


def rand_term(rng):
    a = rng.choice([V(n) for n in NAMES] + [K(rng.randint(-2, 2))])
    r = rng.random()
    if r < 0.4:
        return a
    b = rng.choice([V(n) for n in NAMES] + [K(rng.randint(-2, 2))])
    return (rng.choice(["+", "-", "+", "*"]), a, b)


def rand_atom(rng):
    return (rng.choice(["<", "<=", "=="]), rand_term(rng), rand_term(rng))


def rand_cond(rng):
    r = rng.random()
    if r < 0.6:
        return rand_atom(rng)
    if r < 0.8:
        return ("not", rand_atom(rng))
    return (rng.choice(["and", "or"]), rand_atom(rng), rand_atom(rng))


def rand_loop_free(rng, depth):
    r = rng.random()
    if depth == 0 or r < 0.35:
        k = rng.random()
        if k < 0.7:
            return ("assign", rng.choice(NAMES), rand_term(rng))
        if k < 0.85:
            return ("assert", rand_cond(rng))
        return ("assume", rand_cond(rng))
    if r < 0.7:
        return ("seq", rand_loop_free(rng, depth - 1), rand_loop_free(rng, depth - 1))
    return ("if", rand_cond(rng), rand_loop_free(rng, depth - 1), rand_loop_free(rng, depth - 1))


def box_states():
    for vals in itertools.product(range(LO, HI + 1), repeat=len(NAMES)):
        yield dict(zip(NAMES, vals))


class TestRandom(unittest.TestCase):
    def test_loop_free_vc_is_exact(self):
        # For a loop-free program the VC holds in a state exactly when the
        # run from that state is correct, so validity on the box equals
        # correctness of every run from the box. The compact VC agrees.
        rng = random.Random(7)
        valid_count = 0
        for _ in range(500):
            s = rand_loop_free(rng, 3)
            pre = rand_cond(rng) if rng.random() < 0.5 else ("bool", True)
            post = rand_cond(rng)
            vcs = vcgen(pre, s, post)
            self.assertEqual(len(vcs), 1)
            naive = vcs[0]
            compact = compact_vc(pre, s, post)
            all_ok = True
            for env in box_states():
                truth = (not evaluate(pre, env)) or outcome_ok(run(s, env), post)
                self.assertEqual(evaluate(naive, env), truth)
                self.assertEqual(evaluate(compact, env), truth)
                all_ok = all_ok and truth
            self.assertEqual(valid_on_box(naive, NAMES, LO, HI) is None, all_ok)
            valid_count += all_ok
        self.assertGreater(valid_count, 50)

    def test_loops_sound_on_box(self):
        # If every VC holds on the box, every run from a pre state whose
        # loop-head states stay in the box passes its asserts and ends in
        # the postcondition.
        rng = random.Random(11)
        checked = 0
        for _ in range(500):
            body = rand_loop_free(rng, 2)
            inv = rand_cond(rng) if rng.random() < 0.7 else ("bool", True)
            b = rand_atom(rng)
            post = rng.choice([("not", b), rand_cond(rng), ("and", inv, ("not", b))])
            pre = rand_cond(rng) if rng.random() < 0.5 else inv
            s = seqs(rand_loop_free(rng, 1), ("while", b, inv, body))
            vcs = vcgen(pre, s, post)
            if any(valid_on_box(f, NAMES, LO, HI) is not None for f in vcs):
                continue
            checked += 1
            for env in box_states():
                if not evaluate(pre, env):
                    continue
                heads = []
                res = run(s, env, fuel=60, heads=heads)
                if res[0] == "out":
                    continue
                if all(LO <= h[n] <= HI for h in heads for n in NAMES):
                    self.assertTrue(outcome_ok(res, post))
        self.assertGreater(checked, 50)


if __name__ == "__main__":
    unittest.main()
