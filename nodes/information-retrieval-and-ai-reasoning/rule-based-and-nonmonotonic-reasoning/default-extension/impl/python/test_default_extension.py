# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/default-extension/. The authors are listed in prov/DNSBMF.jsonl.

import random
import unittest
from itertools import combinations

from default_extension import evaluate, extensions, in_extension, worlds

TRUE = ("true",)
FALSE = ("false",)


def v(x):
    return ("var", x)


def neg(f):
    return ("not", f)


def disj(*fs):
    return ("or",) + fs


def conj(*fs):
    return ("and",) + fs


def normal(alpha, gamma):
    return (alpha, [gamma], gamma)


def reiter_fixed_points(names, w_part, d_part):
    """Every theory E over the atoms (a set of worlds) with E = union of Reiter's E_i (Theorem 2.1), by trying all of them."""
    ws = worlds(names)
    idx = range(len(ws))

    def mods(fs):
        return frozenset(i for i in idx if all(evaluate(f, ws[i]) for f in fs))

    out = set()
    for k in range(len(ws) + 1):
        for e in combinations(idx, k):
            e = frozenset(e)
            cur = mods(w_part)  # E_0 = Th(W)
            while True:
                add = [g for (a, bs, g) in d_part
                       if all(evaluate(a, ws[i]) for i in cur)
                       and all(any(evaluate(b, ws[i]) for i in e) for b in bs)]
                nxt = cur & mods(add)
                if nxt == cur:
                    break
                cur = nxt
            if cur == e:
                out.add(e)
    return out


def random_formula(rng, names, depth):
    if depth == 0 or rng.random() < 0.35:
        x = v(rng.choice(names))
        return neg(x) if rng.random() < 0.4 else x
    if rng.random() < 0.25:
        return neg(random_formula(rng, names, depth - 1))
    kids = [random_formula(rng, names, depth - 1) for _ in range(2)]
    return conj(*kids) if rng.random() < 0.5 else disj(*kids)


def random_theory(rng, names, normal_only=False):
    w_part = [random_formula(rng, names, 1) for _ in range(rng.randint(0, 2))]
    d_part = []
    for _ in range(rng.randint(0, 4)):
        alpha = TRUE if rng.random() < 0.4 else random_formula(rng, names, 1)
        gamma = random_formula(rng, names, 1)
        if normal_only:
            d_part.append(normal(alpha, gamma))
        else:
            betas = [random_formula(rng, names, 1) for _ in range(rng.randint(0, 2))]
            d_part.append((alpha, betas, gamma))
    return w_part, d_part


class TestExamples(unittest.TestCase):
    def test_nixon_diamond(self):
        names = ["q", "r", "p"]
        q, r, p = v("q"), v("r"), v("p")
        exts = extensions(names, [q, r], [normal(q, p), normal(r, neg(p))])
        self.assertEqual(len(exts), 2)
        (e1, g1), (e2, g2) = exts
        self.assertEqual((g1, g2), (frozenset({0}), frozenset({1})))
        self.assertTrue(in_extension(e1, p, names))
        self.assertTrue(in_extension(e2, neg(p), names))
        for e, _ in exts:
            self.assertTrue(in_extension(e, conj(q, r), names))

    def test_no_extension(self):
        a = v("a")
        self.assertEqual(extensions(["a"], [], [(TRUE, [neg(a)], a)]), [])
        # The same default next to a normal one still blocks every candidate.
        b = v("b")
        self.assertEqual(extensions(["a", "b"], [], [(TRUE, [neg(a)], a), normal(TRUE, b)]), [])

    def test_tweety(self):
        names = ["b", "f"]
        b, f = v("b"), v("f")
        exts = extensions(names, [b], [normal(b, f)])
        self.assertEqual(len(exts), 1)
        self.assertTrue(in_extension(exts[0][0], f, names))
        exts = extensions(names, [b, neg(f)], [normal(b, f)])
        self.assertEqual(exts[0][1], frozenset())
        self.assertFalse(in_extension(exts[0][0], f, names))

    def test_makinson_cumulativity(self):
        names = ["a", "b"]
        a, b = v("a"), v("b")
        d_part = [normal(TRUE, a), normal(disj(a, b), neg(a))]
        exts = extensions(names, [], d_part)
        self.assertEqual(len(exts), 1)
        self.assertTrue(in_extension(exts[0][0], a, names))
        self.assertTrue(in_extension(exts[0][0], disj(a, b), names))
        exts = extensions(names, [disj(a, b)], d_part)
        self.assertEqual(len(exts), 2)
        self.assertEqual([in_extension(e, a, names) for e, _ in exts], [True, False])
        self.assertTrue(in_extension(exts[1][0], conj(neg(a), b), names))

    def test_inconsistent_facts(self):
        a = v("a")
        exts = extensions(["a"], [a, neg(a)], [normal(TRUE, a)])
        self.assertEqual(exts, [(frozenset(), frozenset())])

    def test_no_defaults(self):
        a = v("a")
        exts = extensions(["a"], [a], [])
        self.assertEqual(len(exts), 1)
        self.assertTrue(in_extension(exts[0][0], a, ["a"]))


class TestAgainstFixedPoints(unittest.TestCase):
    def test_random_theories(self):
        rng = random.Random(1980)
        for t in range(500):
            names = ["a", "b"] if t % 10 else ["a", "b", "c"]
            w_part, d_part = random_theory(rng, names)
            got = {e for e, _ in extensions(names, w_part, d_part)}
            self.assertEqual(got, reiter_fixed_points(names, w_part, d_part), (w_part, d_part))


class TestNormalTheories(unittest.TestCase):
    def test_existence_orthogonality_and_semi_monotonicity(self):
        rng = random.Random(1987)
        names = ["a", "b", "c"]
        ws = worlds(names)
        for _ in range(300):
            w_part, d_part = random_theory(rng, names, normal_only=True)
            if not any(all(evaluate(f, w) for f in w_part) for w in ws):
                continue
            exts = [e for e, _ in extensions(names, w_part, d_part)]
            self.assertGreaterEqual(len(exts), 1)
            for e1, e2 in combinations(exts, 2):
                self.assertFalse(e1 & e2)  # distinct extensions contradict each other
            extra = normal(TRUE if rng.random() < 0.5 else random_formula(rng, names, 1), random_formula(rng, names, 1))
            bigger = [e for e, _ in extensions(names, w_part, d_part + [extra])]
            for e in exts:
                self.assertTrue(any(f <= e for f in bigger))  # some new extension contains e


if __name__ == "__main__":
    unittest.main()
