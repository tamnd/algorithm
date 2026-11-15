# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smodels-algorithm/. The authors are listed in prov/NCW1XZ.jsonl.

import random
import unittest
from itertools import combinations

import lp
from smodels_algorithm import Conflict, Program, expand, has_stable_model, stable_models


def key(models):
    return sorted(models, key=lambda m: (len(m), sorted(m)))


def brute_force(normal, choice=(), constraints=()):
    """Stable models by the reduct, over every subset of the atoms.

    A choice rule {H} <- pos, not neg survives the reduct by M when neg and M are
    disjoint, and then gives h <- pos for each h in H that is in M. M must also
    make no constraint body true.
    """
    universe = set()
    for h, pos, neg in normal:
        universe.update((h,) + tuple(pos) + tuple(neg))
    for hs, pos, neg in choice:
        universe.update(tuple(hs) + tuple(pos) + tuple(neg))
    for pos, neg in constraints:
        universe.update(tuple(pos) + tuple(neg))
    universe = sorted(universe)
    found = []
    for k in range(len(universe) + 1):
        for subset in combinations(universe, k):
            m = frozenset(subset)
            if any(all(b in m for b in pos) and not any(c in m for c in neg) for pos, neg in constraints):
                continue
            red = lp.reduct(normal, m)
            for hs, pos, neg in choice:
                if not any(c in m for c in neg):
                    red += [(h, tuple(pos), ()) for h in hs if h in m]
            if lp.least_model(red) == m:
                found.append(m)
    return key(found)


def translate_choice(normal, choice, offset=100):
    """The normal translation: h <- pos, not neg, not h'; h' <- not h, with h' = h + offset."""
    out = list(normal)
    for hs, pos, neg in choice:
        for h in hs:
            out.append((h, tuple(pos), tuple(neg) + (h + offset,)))
            out.append((h + offset, (), (h,)))
    return out


def random_choice_program(rng, n_atoms):
    normal = lp.random_program(rng, n_atoms, rng.randint(1, 6))
    choice = []
    for _ in range(rng.randint(1, 2)):
        hs = tuple(rng.sample(range(n_atoms), rng.randint(1, min(2, n_atoms))))
        pos = tuple(rng.sample(range(n_atoms), rng.randint(0, 1)))
        neg = tuple(rng.sample(range(n_atoms), rng.randint(0, 1)))
        choice.append((hs, pos, neg))
    constraints = []
    for _ in range(rng.randint(0, 2)):
        pos = tuple(rng.sample(range(n_atoms), rng.randint(1, min(2, n_atoms))))
        neg = tuple(rng.sample(range(n_atoms), rng.randint(0, 1)))
        constraints.append((pos, neg))
    return normal, choice, constraints


class TestSmodels(unittest.TestCase):
    def test_examples(self):
        # p <- not q. q <- not p. r <- p, not s.
        prog = [("p", (), ("q",)), ("q", (), ("p",)), ("r", ("p",), ("s",))]
        self.assertEqual(stable_models(prog), [frozenset({"q"}), frozenset({"p", "r"})])
        self.assertEqual(stable_models([("p", (), ("p",))]), [])
        self.assertEqual(stable_models([("p", ("p",), ())]), [frozenset()])
        # {a, b}. <- a, b. gives the three subsets of size at most 1.
        models = stable_models(choice=[(("a", "b"), (), ())], constraints=[(("a", "b"), ())])
        self.assertEqual(models, [frozenset(), frozenset({"a"}), frozenset({"b"})])

    def test_atmost_rejects_self_support(self):
        # p <- q. q <- p. The upper closure is empty, so EXPAND makes both false with no search.
        prog = Program([("p", ("q",), ()), ("q", ("p",), ())])
        a = expand(prog, {})
        self.assertEqual(a, {"p": False, "q": False})

    def test_conflict_from_constraint(self):
        prog = Program([("p", (), ())], constraints=[(("p",), ())])
        with self.assertRaises(Conflict):
            expand(prog, {})

    def test_random_normal_against_brute_force(self):
        rng = random.Random(20021)
        for _ in range(300):
            n = rng.randint(1, 6)
            prog = lp.random_program(rng, n, rng.randint(1, 9))
            expected = lp.stable_models(prog)
            self.assertEqual(stable_models(prog), expected, prog)
            self.assertEqual(stable_models(prog, use_lookahead=False), expected, prog)
            self.assertEqual(has_stable_model(prog), bool(expected), prog)

    def test_random_choice_against_brute_force(self):
        rng = random.Random(1382)
        for _ in range(250):
            n = rng.randint(1, 6)
            normal, choice, constraints = random_choice_program(rng, n)
            expected = brute_force(normal, choice, constraints)
            self.assertEqual(stable_models(normal, choice, constraints), expected, (normal, choice, constraints))
            self.assertEqual(stable_models(normal, choice, constraints, use_lookahead=False), expected)

    def test_choice_translation_has_same_models(self):
        rng = random.Random(77)
        for _ in range(80):
            n = rng.randint(1, 4)
            normal, choice, constraints = random_choice_program(rng, n)
            direct = stable_models(normal, choice, constraints)
            translated = stable_models(translate_choice(normal, choice), constraints=constraints)
            projected = key({frozenset(x for x in m if x < 100) for m in translated})
            self.assertEqual(direct, projected)
            # Each direct model comes from exactly one translated model.
            self.assertEqual(len(direct), len(translated))


if __name__ == "__main__":
    unittest.main()
