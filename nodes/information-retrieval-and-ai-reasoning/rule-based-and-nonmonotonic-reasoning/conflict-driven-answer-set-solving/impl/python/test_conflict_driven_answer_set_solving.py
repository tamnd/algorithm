# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-driven-answer-set-solving/. The authors are listed in prov/THR1ZW.jsonl.

import random
import unittest
from itertools import combinations

import lp
from conflict_driven_answer_set_solving import Solver, answer_sets, has_answer_set


def brute_force(program, constraints=()):
    """Stable models by the reduct, minus those that make a constraint body true."""
    extra = [a for pos, neg in constraints for a in pos + neg]
    universe = sorted(set(lp.atoms(program)) | set(extra))
    found = []
    for k in range(len(universe) + 1):
        for subset in combinations(universe, k):
            m = frozenset(subset)
            if any(all(b in m for b in pos) and not any(c in m for c in neg) for pos, neg in constraints):
                continue
            if lp.is_stable(program, m):
                found.append(m)
    return found


def induced(solver, m):
    """The total assignment of atoms and bodies that the set of atoms m gives, as a set of literals."""
    lits = set()
    for name, v in solver.atom_var.items():
        lits.add(v if name in m else -v)
    true_vars = {solver.atom_var[a] for a in m}
    for b, (pos, neg) in solver.body_of.items():
        holds = all(p in true_vars for p in pos) and not any(c in true_vars for c in neg)
        lits.add(b if holds else -b)
    return lits


def completion_and_loop_solutions(program, constraints, solver):
    """The sets of atoms whose induced assignment satisfies every completion nogood and every loop nogood.

    Every loop nogood lambda(p, U) is built here for every nonempty set U of atoms,
    from the definition, without the solver's code.
    """
    atoms = sorted(solver.atom_var.values())
    eb = {}
    for k in range(1, len(atoms) + 1):
        for u in combinations(atoms, k):
            us = set(u)
            eb[u] = [b for b in solver.body_of if any(h in us for h in solver.heads_of_body[b]) and not us.intersection(solver.body_of[b][0])]
    sols = []
    for m in brute_force_subsets(solver):
        lits = induced(solver, m)
        if any(ng <= lits for ng in solver.static):
            continue
        ok = True
        for u, bodies in eb.items():
            for p in u:
                if p in lits and all(-b in lits for b in bodies):
                    ok = False
        if ok:
            sols.append(m)
    return sols


def brute_force_subsets(solver):
    names = solver.atom_names
    for k in range(len(names) + 1):
        for subset in combinations(names, k):
            yield frozenset(subset)


def random_constraints(rng, n_atoms):
    out = []
    for _ in range(rng.randint(0, 2)):
        pos = tuple(rng.sample(range(n_atoms), rng.randint(1, min(2, n_atoms))))
        neg = tuple(rng.sample(range(n_atoms), rng.randint(0, 1)))
        out.append((pos, neg))
    return out


class TestCDNL(unittest.TestCase):
    def test_examples(self):
        prog = [("p", (), ("q",)), ("q", (), ("p",)), ("r", ("p",), ("s",))]
        self.assertEqual(answer_sets(prog), [frozenset({"q"}), frozenset({"p", "r"})])
        self.assertEqual(answer_sets([("p", (), ("p",))]), [])
        # A positive loop: p <- q. q <- p. p <- not r. r <- not p.
        loop = [("p", ("q",), ()), ("q", ("p",), ()), ("p", (), ("r",)), ("r", (), ("p",))]
        self.assertEqual(answer_sets(loop), [frozenset({"r"}), frozenset({"p", "q"})])
        # The completion of a <- b. b <- a. has the model {a, b}; the loop nogoods reject it.
        self.assertEqual(answer_sets([("a", ("b",), ()), ("b", ("a",), ())]), [frozenset()])

    def test_random_against_brute_force(self):
        rng = random.Random(2012)
        for _ in range(300):
            n = rng.randint(1, 6)
            prog = lp.random_program(rng, n, rng.randint(1, 9))
            expected = lp.stable_models(prog)
            self.assertEqual(answer_sets(prog), expected, prog)
            self.assertEqual(has_answer_set(prog), bool(expected), prog)

    def test_random_with_constraints(self):
        rng = random.Random(188)
        for _ in range(150):
            n = rng.randint(1, 6)
            prog = lp.random_program(rng, n, rng.randint(1, 9))
            cons = random_constraints(rng, n)
            self.assertEqual(answer_sets(prog, cons), brute_force(prog, cons), (prog, cons))

    def test_solutions_of_nogoods_are_the_stable_models(self):
        # Gebser, Kaufmann and Schaub: X is an answer set iff X is the true atoms of a solution of Delta_P and Lambda_P.
        rng = random.Random(55)
        for _ in range(60):
            n = rng.randint(1, 5)
            prog = lp.random_program(rng, n, rng.randint(1, 8))
            cons = random_constraints(rng, n)
            s = Solver(prog, cons)
            sols = completion_and_loop_solutions(prog, cons, s)
            self.assertEqual(sorted(sols, key=lambda m: (len(m), sorted(m))), brute_force(prog, cons))

    def test_learned_nogoods_are_implied(self):
        # Each learned nogood and each loop nogood must be avoided by every solution of the
        # completion and loop nogoods that the blocking nogoods of the run do not exclude.
        # The first run of each program has no blocking nogood, so there the learned nogoods
        # follow from Delta_P and Lambda_P alone.
        rng = random.Random(9)
        learned = 0
        for _ in range(300):
            n = rng.randint(3, 6)
            prog = lp.random_program(rng, n, rng.randint(6, 14))
            cons = random_constraints(rng, n)
            solvers = []
            answer_sets(prog, cons, solvers)
            stable = brute_force(prog, cons)
            for s in solvers:
                learned += len(s.learned)
                for m in stable:
                    if m in s.blocked_models:
                        continue
                    lits = induced(s, m)
                    for ng in s.learned + s.loop:
                        self.assertFalse(ng <= lits, (prog, cons, m, ng))
        self.assertGreater(learned, 100)

    def test_loop_nogoods_have_the_right_form(self):
        rng = random.Random(4)
        for _ in range(100):
            n = rng.randint(2, 6)
            prog = lp.random_program(rng, n, rng.randint(3, 10))
            s = Solver(prog)
            s.solve()
            for ng in s.loop:
                (p,) = [l for l in ng if l > 0]
                self.assertLessEqual(p, s.n_atoms)
                self.assertTrue(all(l < 0 and -l > s.n_atoms for l in ng if l != p))


if __name__ == "__main__":
    unittest.main()
