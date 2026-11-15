# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/answer-set-grounding/. The authors are listed in prov/JQHNQC.jsonl.

import random
import unittest
from itertools import product

import lp
from answer_set_grounding import ground, instantiate, is_var, subst

ARITY = {"p": 1, "q": 1, "r": 2, "s": 0}
CONSTANTS = ("a", "b")
VARS = ("X", "Y")


def constants_of(program):
    out = set()
    for h, pos, neg in program:
        for atom in (h,) + tuple(pos) + tuple(neg):
            out.update(t for t in atom[1:] if not is_var(t))
    return sorted(out) or ["a"]


def rule_vars(rule):
    h, pos, neg = rule
    return sorted({t for atom in (h,) + tuple(pos) + tuple(neg) for t in atom[1:] if is_var(t)})


def full_instantiation(program, consts=None):
    """Every rule under every substitution of its variables by constants of the program."""
    if consts is None:
        consts = constants_of(program)
    out = set()
    for rule in program:
        vs = rule_vars(rule)
        for values in product(consts, repeat=len(vs)):
            theta = dict(zip(vs, values))
            h, pos, neg = rule
            out.add((subst(h, theta), tuple(subst(b, theta) for b in pos), tuple(subst(c, theta) for c in neg)))
    return sorted(out)


def naive_instances(program):
    """The instances whose positive body lies in the least model of the positive parts, by plain iteration."""
    full = full_instantiation(program)
    domain = lp.least_model([(h, pos, ()) for h, pos, neg in full])
    return domain, {r for r in full if all(b in domain for b in r[1])}


def random_atom(rng, allow_vars):
    pred = rng.choice(sorted(ARITY))
    terms = [rng.choice(VARS + CONSTANTS) if allow_vars else rng.choice(CONSTANTS) for _ in range(ARITY[pred])]
    return (pred,) + tuple(terms)


def random_program(rng):
    program = []
    for _ in range(rng.randint(1, 4)):
        program.append((random_atom(rng, False), (), ()))
    for _ in range(rng.randint(1, 5)):
        pos = tuple(random_atom(rng, True) for _ in range(rng.randint(1, 2)))
        safe = {t for atom in pos for t in atom[1:] if is_var(t)}
        fix = lambda atom: (atom[0],) + tuple(t if not is_var(t) or t in safe else rng.choice(CONSTANTS) for t in atom[1:])
        head = fix(random_atom(rng, True))
        neg = tuple(fix(random_atom(rng, True)) for _ in range(rng.randint(0, 1)))
        program.append((head, pos, neg))
    return program


class TestGrounding(unittest.TestCase):
    def test_example(self):
        # Reachability with a choice between two colours of each reached node.
        program = [
            (("edge", "a", "b"), (), ()),
            (("edge", "b", "c"), (), ()),
            (("start", "a"), (), ()),
            (("reach", "X"), (("start", "X"),), ()),
            (("reach", "Y"), (("reach", "X"), ("edge", "X", "Y")), ()),
            (("red", "X"), (("reach", "X"),), (("green", "X"),)),
            (("green", "X"), (("reach", "X"),), (("red", "X"),)),
        ]
        g = ground(program)
        self.assertEqual(len(g), 12)
        self.assertIn((("red", "c"), (), (("green", "c"),)), g)
        self.assertEqual(len(lp.stable_models(g)), 8)

    def test_semi_naive_finds_each_instance_once(self):
        rng = random.Random(4483)
        for _ in range(300):
            program = random_program(rng)
            stats = {}
            domain, instances = instantiate(program, stats)
            n_domain, n_instances = naive_instances(program)
            self.assertEqual(domain, set(n_domain))
            self.assertEqual(set(instances), n_instances)
            # Each (rule, substitution) pair is produced in exactly one round and one position.
            consts = constants_of(program)
            pairs = sum(1 for r in program for i in full_instantiation([r], consts) if all(b in domain for b in i[1]))
            self.assertEqual(stats["emitted"], pairs)

    def test_same_stable_models_as_full_instantiation(self):
        rng = random.Random(266)
        for _ in range(200):
            program = random_program(rng)
            full = full_instantiation(program)
            self.assertLessEqual(len(lp.atoms(full)), 9)
            expected = lp.stable_models(full)
            got = lp.stable_models(ground(program))
            self.assertEqual(got, expected, program)

    def test_unsafe_rule_is_rejected(self):
        with self.assertRaises(ValueError):
            ground([(("p", "X"), (), (("q", "X"),))])

    def test_exponential_family(self):
        # p(X1, ..., Xk) <- d(X1), ..., d(Xk) with d(a), d(b) has 2^k ground instances,
        # and every one of them is a different fact in the output.
        for k in range(1, 9):
            vs = tuple(f"X{i}" for i in range(1, k + 1))
            program = [(("d", "a"), (), ()), (("d", "b"), (), ()), (("p",) + vs, tuple(("d", v) for v in vs), ())]
            g = ground(program)
            self.assertEqual(len(g), 2 + 2 ** k)
            self.assertEqual(len(lp.least_model(g)), 2 + 2 ** k)


if __name__ == "__main__":
    unittest.main()
