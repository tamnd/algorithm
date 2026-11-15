# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reiter-hs-tree/. The authors are listed in prov/PCV2A8.jsonl.

import random
import unittest
from itertools import combinations

from reiter_hs_tree import (
    collection_labels,
    diagnoses,
    hs_dag,
    minimal_hitting_sets,
    reiter_pruned_tree,
)


def brute_force(collection):
    """The minimal hitting sets, by trying every subset of the union."""
    sets = [frozenset(s) for s in collection]
    universe = sorted(set().union(*sets)) if sets else []
    hitting = [
        frozenset(c)
        for k in range(len(universe) + 1)
        for c in combinations(universe, k)
        if all(set(c) & s for s in sets)
    ]
    minimal = [h for h in hitting if not any(o < h for o in hitting)]
    return sorted(minimal, key=lambda s: (len(s), sorted(s)))


def random_collection(rng):
    n = rng.randint(1, 7)
    count = rng.randint(0, 7)
    out = []
    for _ in range(count):
        size = rng.choice([1, 1, 2, 2, 3, 3, 4]) if rng.random() > 0.03 else 0
        out.append(set(rng.sample(range(n), min(size, n))))
    return out


def superset_labels(collection, universe, rng):
    """Returns a member disjoint from h with extra elements added, so that the labels are often not minimal."""
    sets = [frozenset(s) for s in collection]

    def next_label(h):
        free = [s for s in sets if not (s & h)]
        if not free:
            return None
        base = rng.choice(free)
        extra = [x for x in universe if x not in h and rng.random() < 0.4]
        return base | set(extra)

    return next_label


FIG1 = [{"a", "b"}, {"b", "c"}, {"a", "c"}, {"b", "d"}, {"b"}]
FIG2 = [{"a", "b"}, {"a"}, {"b"}]


class TestHSDAG(unittest.TestCase):
    def test_random_collections(self):
        rng = random.Random(1987)
        for _ in range(600):
            coll = random_collection(rng)
            self.assertEqual(minimal_hitting_sets(coll), brute_force(coll), coll)

    def test_order_does_not_matter(self):
        rng = random.Random(41)
        for _ in range(200):
            coll = random_collection(rng)
            shuffled = coll[:]
            rng.shuffle(shuffled)
            self.assertEqual(minimal_hitting_sets(shuffled), brute_force(coll))

    def test_labels_that_are_not_minimal(self):
        rng = random.Random(1989)
        for _ in range(600):
            coll = random_collection(rng)
            universe = sorted(set().union(*coll)) if coll else []
            universe += [99, 100]  # elements outside every conflict
            got = hs_dag(superset_labels(coll, universe, rng))
            self.assertEqual(got, brute_force(coll), coll)

    def test_edge_cases(self):
        self.assertEqual(minimal_hitting_sets([]), [frozenset()])
        self.assertEqual(minimal_hitting_sets([set()]), [])
        self.assertEqual(minimal_hitting_sets([{1}, set(), {2}]), [])
        self.assertEqual(minimal_hitting_sets([{1}, {1}]), [frozenset({1})])
        self.assertEqual(minimal_hitting_sets([{1, 2, 3}]), [frozenset({1}), frozenset({2}), frozenset({3})])

    def test_bad_label_is_rejected(self):
        with self.assertRaises(ValueError):
            hs_dag(lambda h: {1})


class TestReiterError(unittest.TestCase):
    def test_figure_1(self):
        expected = [frozenset("ab"), frozenset("bc")]
        self.assertEqual(brute_force(FIG1), expected)
        self.assertEqual(minimal_hitting_sets(FIG1), expected)
        self.assertEqual(reiter_pruned_tree(FIG1), [frozenset("bc")])

    def test_figure_2(self):
        self.assertEqual(minimal_hitting_sets(FIG2), [frozenset("ab")])
        self.assertEqual(reiter_pruned_tree(FIG2), [])

    def test_uncorrected_tree_on_minimal_conflicts(self):
        # With an antichain of conflicts no pruning step applies, and the uncorrected tree is right.
        rng = random.Random(7)
        for _ in range(300):
            coll = [frozenset(s) for s in random_collection(rng)]
            anti = [s for s in set(coll) if not any(o < s for o in coll)]
            self.assertEqual(reiter_pruned_tree(anti), brute_force(anti), anti)

    def test_collection_labels(self):
        nl = collection_labels(FIG1)
        self.assertEqual(nl(frozenset()), frozenset("ab"))
        self.assertEqual(nl(frozenset("acd")), frozenset("b"))
        self.assertIsNone(nl(frozenset("ab")))


class TestDiagnosis(unittest.TestCase):
    def polybox_consistent(self, ok):
        # Inputs A=3, B=2, C=2, D=3, E=3 and outputs F=10, G=12. A correct
        # multiplier fixes its output, a correct adder ties its inputs to the
        # observed output, and a faulty component imposes nothing.
        for y in range(-50, 60):
            if "M2" in ok and y != 6:
                continue
            xs = ({6} if "M1" in ok else set()) | ({10 - y} if "A1" in ok else set())
            zs = ({6} if "M3" in ok else set()) | ({12 - y} if "A2" in ok else set())
            if len(xs) <= 1 and len(zs) <= 1:
                return True
        return False

    def test_polybox(self):
        got = diagnoses(["M1", "M2", "M3", "A1", "A2"], self.polybox_consistent)
        expected = [frozenset({"A1"}), frozenset({"M1"}), frozenset({"A2", "M2"}), frozenset({"M2", "M3"})]
        self.assertEqual(got, expected)

    def test_inconsistent_observations(self):
        self.assertEqual(diagnoses(["x", "y"], lambda ok: False), [])

    def test_no_fault(self):
        self.assertEqual(diagnoses(["x", "y"], lambda ok: True), [frozenset()])

    def test_random_conflict_systems(self):
        rng = random.Random(32)
        for _ in range(200):
            coll = [frozenset(s) for s in random_collection(rng)]
            comps = sorted(set().union(*coll)) if coll else []
            comps += [99]  # a component in no conflict

            def consistent(ok, coll=coll):
                return not any(s <= ok for s in coll)

            self.assertEqual(diagnoses(comps, consistent), brute_force(coll), coll)


if __name__ == "__main__":
    unittest.main()
