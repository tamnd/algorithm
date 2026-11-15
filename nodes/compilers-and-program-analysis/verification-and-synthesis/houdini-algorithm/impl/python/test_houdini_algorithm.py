# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/houdini-algorithm/. The authors are listed in prov/8FP30Z.jsonl.

import itertools
import random
import unittest

from houdini_algorithm import Loop, box_prover, evaluate, houdini, inductive_on_box


def V(x):
    return ("var", x)


def K(c):
    return ("int", c)


# The worked example of the page.
PAGE_LOOP = Loop(
    ["i", "j", "n"],
    ("and", ("==", V("i"), K(0)), ("and", ("==", V("j"), K(0)), ("<=", K(0), V("n")))),
    ("<", V("i"), V("n")),
    [("i", ("+", V("i"), K(1))), ("j", ("+", V("j"), K(2)))],
)
PAGE_CANDS = [
    ("<=", K(0), V("i")),
    ("<=", V("i"), V("n")),
    ("==", V("j"), ("*", K(2), V("i"))),
    ("<=", V("j"), V("n")),
    ("==", V("i"), V("j")),
    ("<=", K(0), V("n")),
    ("<=", V("j"), ("*", K(2), V("n"))),
    ("<=", V("n"), K(3)),
]


def largest_inductive(loop, cands, lo, hi):
    """The brute-force oracle: the union of all subsets that are inductive
    on the box."""
    best = set()
    for r in range(len(cands) + 1):
        for sub in itertools.combinations(range(len(cands)), r):
            if inductive_on_box(loop, cands, sub, lo, hi):
                best |= set(sub)
    return tuple(sorted(best))


class TestPage(unittest.TestCase):
    def test_page_example(self):
        prove = box_prover(PAGE_LOOP, PAGE_CANDS, -4, 4)
        h, calls = houdini(PAGE_CANDS, prove)
        self.assertEqual(h, (0, 1, 2, 5, 6))
        self.assertEqual(calls, 3)
        self.assertEqual(prove.calls, 3)
        self.assertEqual(h, largest_inductive(PAGE_LOOP, PAGE_CANDS, -4, 4))

    def test_page_trace(self):
        prove = box_prover(PAGE_LOOP, PAGE_CANDS, -4, 4)
        first = prove(tuple(range(8)))
        self.assertEqual(first, ("init", {"i": 0, "j": 0, "n": 4}))
        second = prove((0, 1, 2, 3, 4, 5, 6))
        self.assertEqual(second, ("step", {"i": 0, "j": 0, "n": 1}, {"i": 1, "j": 2, "n": 1}))

    def test_result_proves_postcondition(self):
        # The result, with the exit i >= n, gives j = 2n on the box.
        h, _ = houdini(PAGE_CANDS, box_prover(PAGE_LOOP, PAGE_CANDS, -4, 4))
        for vals in itertools.product(range(-4, 5), repeat=3):
            s = dict(zip(["i", "j", "n"], vals))
            if all(evaluate(PAGE_CANDS[k], s) for k in h) and s["i"] >= s["n"]:
                self.assertEqual(s["j"], 2 * s["n"])

    def test_empty_candidates(self):
        h, calls = houdini([], box_prover(PAGE_LOOP, [], -1, 1))
        self.assertEqual((h, calls), ((), 1))

    def test_c_plus_one_calls_reached(self):
        # From x = 0 the loop counts up for ever. Each call removes exactly
        # one bound x <= k, so the c = 3 candidates need c + 1 = 4 calls.
        loop = Loop(["x"], ("==", V("x"), K(0)), ("==", K(0), K(0)), [("x", ("+", V("x"), K(1)))])
        cands = [("<=", V("x"), K(k)) for k in range(3)]
        h, calls = houdini(cands, box_prover(loop, cands, -3, 3))
        self.assertEqual((h, calls), ((), 4))

    def test_only_conjunctions(self):
        # x flips between 1 and -1. Both bounds are inductive, but their
        # conjunction allows x = 0, so it cannot prove x != 0. The candidate
        # x != 0 itself is found when it is offered.
        loop = Loop(["x"], ("==", V("x"), K(1)), ("==", K(0), K(0)), [("x", ("-", K(0), V("x")))])
        cands = [("<=", K(-1), V("x")), ("<=", V("x"), K(1))]
        h, _ = houdini(cands, box_prover(loop, cands, -3, 3))
        self.assertEqual(h, (0, 1))
        self.assertTrue(all(evaluate(cands[k], {"x": 0}) for k in h))
        cands2 = cands + [("!=", V("x"), K(0))]
        h2, _ = houdini(cands2, box_prover(loop, cands2, -3, 3))
        self.assertEqual(h2, (0, 1, 2))


NAMES = ["x", "y"]
LO, HI = -3, 3


def rand_term(rng):
    a = rng.choice([V("x"), V("y"), K(rng.randint(-2, 2))])
    if rng.random() < 0.5:
        return a
    b = rng.choice([V("x"), V("y"), K(rng.randint(-2, 2))])
    return (rng.choice(["+", "-", "*"]), a, b)


def rand_atom(rng):
    return (rng.choice(["<", "<=", "==", "!="]), rand_term(rng), rand_term(rng))


class TestRandom(unittest.TestCase):
    def test_random_loops(self):
        rng = random.Random(2024)
        nonempty = 0
        for _ in range(500):
            init = rand_atom(rng) if rng.random() < 0.3 else ("and", rand_atom(rng), rand_atom(rng))
            guard = rand_atom(rng) if rng.random() < 0.8 else ("==", K(0), K(0))
            body = [(rng.choice(NAMES), rand_term(rng)) for _ in range(rng.randint(1, 2))]
            loop = Loop(NAMES, init, guard, body)
            c = rng.randint(0, 6)
            cands = [rand_atom(rng) for _ in range(c)]
            prove = box_prover(loop, cands, LO, HI)
            h, calls = houdini(cands, prove)
            self.assertLessEqual(calls, c + 1)
            self.assertEqual(calls, prove.calls)
            self.assertTrue(inductive_on_box(loop, cands, h, LO, HI))
            self.assertEqual(h, largest_inductive(loop, cands, LO, HI))
            nonempty += bool(h)
        self.assertGreater(nonempty, 100)


if __name__ == "__main__":
    unittest.main()
