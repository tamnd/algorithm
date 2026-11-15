# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-chaining/. The authors are listed in prov/.

import random
import unittest
from itertools import combinations, product

from forward_chaining import forward_chain, is_var, match, substitute


def ground(rules, facts):
    """Every ground instance of every rule over the constants that occur in the input."""
    consts = set()
    for _, body, head in rules:
        for p in list(body) + [head]:
            consts.update(t for t in p[1:] if not is_var(t))
    for f in facts:
        consts.update(f[1:])
    consts = sorted(consts)
    out = [(tuple(f), ()) for f in facts]
    for _, body, head in rules:
        vs = sorted({t for p in body for t in p if is_var(t)} | {t for t in head if is_var(t)})
        for values in product(consts, repeat=len(vs)):
            b = dict(zip(vs, values))
            out.append((substitute(head, b), tuple(substitute(p, b) for p in body)))
    return out


def least_model_brute(ground_rules):
    """The least model of a ground definite program: the smallest subset of the Herbrand base closed under every rule."""
    base = sorted({h for h, _ in ground_rules} | {a for _, body in ground_rules for a in body})
    assert len(base) <= 12
    for k in range(len(base) + 1):
        for subset in combinations(base, k):
            s = set(subset)
            if all(h in s for h, body in ground_rules if all(a in s for a in body)):
                return s
    raise AssertionError("the full base is always a model")


def random_propositional(rng, n_atoms, n_rules):
    names = [("p" + str(i),) for i in range(n_atoms)]
    rules = []
    for r in range(n_rules):
        head = rng.choice(names)
        body = tuple(rng.sample(names, rng.randint(0, min(3, n_atoms))))
        rules.append(("r" + str(r), body, head))
    facts = [f for f in names if rng.random() < 0.15]
    return rules, facts


def random_first_order(rng):
    """Two constants and the predicates p/1, q/1, e/2, so the Herbrand base has 2 + 2 + 4 = 8 atoms."""
    consts = ["a", "b"]
    preds = [("p", 1), ("q", 1), ("e", 2)]
    vars_ = ["?x", "?y"]

    def pattern():
        name, arity = rng.choice(preds)
        return (name,) + tuple(rng.choice(vars_ + consts) for _ in range(arity))

    rules = []
    for r in range(rng.randint(1, 5)):
        body = tuple(pattern() for _ in range(rng.randint(1, 3)))
        body_vars = sorted({t for p in body for t in p if is_var(t)})
        name, arity = rng.choice(preds)
        head = (name,) + tuple(rng.choice(body_vars + consts) for _ in range(arity))
        rules.append(("r" + str(r), body, head))
    facts = []
    for name, arity in preds:
        for args in product(consts, repeat=arity):
            if rng.random() < 0.2:
                facts.append((name,) + args)
    return rules, facts


class TestForwardChaining(unittest.TestCase):
    def test_match(self):
        self.assertEqual(match(("e", "?x", "?x"), ("e", "a", "a"), {}), {"?x": "a"})
        self.assertIsNone(match(("e", "?x", "?x"), ("e", "a", "b"), {}))
        self.assertIsNone(match(("e", "?x"), ("e", "a", "b"), {}))

    def test_page_example(self):
        rules = [
            ("R1", (("parent", "?x", "?y"),), ("ancestor", "?x", "?y")),
            ("R2", (("parent", "?x", "?y"), ("ancestor", "?y", "?z")), ("ancestor", "?x", "?z")),
        ]
        facts = [("parent", "ann", "bob"), ("parent", "bob", "cat")]
        found, memory, fired = forward_chain(rules, facts)
        self.assertFalse(found)
        self.assertEqual(
            fired,
            [
                ("R1", ("ancestor", "ann", "bob")),
                ("R1", ("ancestor", "bob", "cat")),
                ("R2", ("ancestor", "ann", "cat")),
            ],
        )
        self.assertEqual(len(memory), 5)
        found, _, fired = forward_chain(rules, facts, goal=("ancestor", "bob", "cat"))
        self.assertTrue(found)
        self.assertEqual(len(fired), 2)

    def test_unsafe_rule(self):
        with self.assertRaises(ValueError):
            forward_chain([("bad", (("p", "?x"),), ("q", "?y"))], [])

    def test_random_propositional(self):
        rng = random.Random(20261115)
        for _ in range(400):
            rules, facts = random_propositional(rng, rng.randint(1, 10), rng.randint(0, 14))
            _, memory, fired = forward_chain(rules, facts)
            expected = least_model_brute(ground(rules, facts))
            self.assertEqual(memory, expected)
            self.assertEqual(len(fired), len({f for _, f in fired}))
            for atom in [("p" + str(i),) for i in range(10)]:
                found, _, _ = forward_chain(rules, facts, goal=atom)
                self.assertEqual(found, atom in expected)

    def test_random_first_order(self):
        rng = random.Random(7)
        for _ in range(300):
            rules, facts = random_first_order(rng)
            _, memory, _ = forward_chain(rules, facts)
            self.assertEqual(memory, least_model_brute(ground(rules, facts)))


if __name__ == "__main__":
    unittest.main()
