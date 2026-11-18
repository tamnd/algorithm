# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truthfinder/. The authors are listed in prov/HNKC9H.jsonl.
import math
import random
import unittest

from truthfinder import answers, exclusive_implication, truthfinder, voting


def synthetic(seed, objects=200, good=4, bad=20, good_acc=0.9, bad_acc=0.3):
    """Few accurate sources with large coverage, many poor sources that share a popular wrong value."""
    rng = random.Random(seed)
    truth, popular = {}, {}
    for o in range(objects):
        a, b = rng.sample(range(6), 2)
        truth[o] = "v%d_%d" % (o, a)
        popular[o] = "v%d_%d" % (o, b)
    specs = [("good%d" % i, good_acc, 0.5) for i in range(good)]
    specs += [("bad%d" % i, bad_acc, 0.15) for i in range(bad)]
    claims = []
    for name, acc, cover in specs:
        for o in range(objects):
            if rng.random() < cover:
                if rng.random() < acc:
                    v = truth[o]
                elif rng.random() < 0.7:
                    v = popular[o]
                else:
                    v = truth[o]
                    while v in (truth[o], popular[o]):
                        v = "v%d_%d" % (o, rng.randint(0, 5))
                claims.append((name, o, v))
    return truth, claims


def accuracy(ans, truth):
    return sum(ans[o] == truth[o] for o in ans) / len(ans)


class TestTruthFinder(unittest.TestCase):
    def test_one_iteration_by_hand(self):
        claims = [("w1", "o", "a"), ("w2", "o", "a"), ("w2", "o", "b")]
        s, t, it = truthfinder(claims, imp=exclusive_implication(), max_iter=1)
        self.assertEqual(it, 1)
        tau = -math.log(1 - 0.9)
        sa, sb = 2 * tau, tau
        star_a = sa + 0.5 * sb * (-0.5)
        star_b = sb + 0.5 * sa * (-0.5)
        conf_a = 1 / (1 + math.exp(-0.3 * star_a))
        conf_b = 1 / (1 + math.exp(-0.3 * star_b))
        self.assertAlmostEqual(s[("o", "a")], conf_a, places=12)
        self.assertAlmostEqual(s[("o", "b")], conf_b, places=12)
        self.assertAlmostEqual(t["w1"], conf_a, places=12)
        self.assertAlmostEqual(t["w2"], (conf_a + conf_b) / 2, places=12)
        self.assertEqual(answers(s), {"o": "a"})

    def test_cosine_stop_with_one_source(self):
        # One trust value: the cosine of two one-element vectors is 1, so the loop stops at once.
        s, t, it = truthfinder([("w", "o", "a")])
        self.assertEqual(it, 1)
        self.assertAlmostEqual(s[("o", "a")], 1 / (1 + 0.1 ** 0.3), places=12)

    def test_iteration_cap(self):
        truth, claims = synthetic(3)
        for cap in (1, 2, 5):
            _, _, it = truthfinder(claims, max_iter=cap, delta=0.0)
            self.assertEqual(it, cap)

    def test_ranges_and_renaming(self):
        rng = random.Random(8)
        truth, claims = synthetic(8, objects=60)
        s, t, it = truthfinder(claims, imp=exclusive_implication())
        self.assertTrue(all(0 < c < 1 for c in s.values()))
        self.assertTrue(all(0 < x < 1 for x in t.values()))
        names = sorted({w for w, _, _ in claims})
        shuffled = names[:]
        rng.shuffle(shuffled)
        rename = dict(zip(names, ["src%03d" % i for i in range(len(names))]))
        renamed = [(rename[w], o, v) for w, o, v in reversed(claims)]
        s2, t2, it2 = truthfinder(renamed, imp=exclusive_implication())
        self.assertEqual(it, it2)
        for f in s:
            self.assertAlmostEqual(s[f], s2[f], places=9)
        for w in t:
            self.assertAlmostEqual(t[w], t2[rename[w]], places=9)

    def test_similar_facts_support_each_other(self):
        claims = [("w1", "x", 100), ("w2", "x", 101), ("w3", "x", 50)]

        def imp(o, v1, v2):
            return math.exp(-abs(v1 - v2)) - 0.5

        s0, _, _ = truthfinder(claims)
        self.assertAlmostEqual(s0[("x", 100)], s0[("x", 50)], places=12)
        s, _, _ = truthfinder(claims, imp=imp)
        self.assertGreater(s[("x", 100)], s[("x", 50)])
        self.assertGreater(s[("x", 101)], s[("x", 50)])
        self.assertIn(answers(s)["x"], (100, 101))

    def test_against_voting_synthetic(self):
        truth, claims = synthetic(42)
        vote = accuracy(voting(claims), truth)
        s, t, it = truthfinder(claims)
        plain = accuracy(answers(s), truth)
        s2, t2, it2 = truthfinder(claims, imp=exclusive_implication())
        excl = accuracy(answers(s2), truth)
        # The numbers on the page (seed 42): 1025 claims on 200 objects.
        self.assertEqual(len(claims), 1025)
        self.assertEqual((round(vote, 3), round(plain, 3), round(excl, 3)), (0.63, 0.72, 0.73))
        self.assertEqual((it, it2), (3, 5))
        good = sum(t2["good%d" % i] for i in range(4)) / 4
        bad = sum(t2["bad%d" % i] for i in range(20)) / 20
        self.assertGreater(good, bad)

    def test_first_iteration_is_a_vote(self):
        truth, claims = synthetic(42)
        count = {}
        for w, o, v in claims:
            count[(o, v)] = count.get((o, v), 0) + 1
        for imp in (None, exclusive_implication()):
            if imp is None:
                s, _, _ = truthfinder(claims, max_iter=1)
            else:
                s, _, _ = truthfinder(claims, imp=imp, max_iter=1)
            for f in s:
                for g in s:
                    if f[0] == g[0] and count[f] > count[g]:
                        self.assertGreater(s[f], s[g])

    def test_page_example(self):
        claims = [
            ("A", "b1", "x"), ("A", "b2", "x"), ("A", "b3", "x"),
            ("B", "b1", "y"), ("B", "b2", "y"),
            ("C", "b2", "x"), ("C", "b3", "x"),
        ]
        imp = exclusive_implication()
        s, t, it = truthfinder(claims, imp=imp, max_iter=1)
        r = {f: round(c, 3) for f, c in s.items()}
        self.assertEqual(r, {("b1", "x"): 0.627, ("b1", "y"): 0.627, ("b2", "x"): 0.77, ("b2", "y"): 0.585, ("b3", "x"): 0.799})
        self.assertEqual({w: round(x, 3) for w, x in t.items()}, {"A": 0.732, "B": 0.606, "C": 0.785})
        s, t, it = truthfinder(claims, imp=imp, max_iter=2, delta=0.0)
        self.assertEqual((round(s[("b1", "x")], 3), round(s[("b1", "y")], 3)), (0.581, 0.545))
        s, t, it = truthfinder(claims, imp=imp)
        self.assertEqual(it, 5)
        self.assertEqual(answers(s), {"b1": "x", "b2": "x", "b3": "x"})
        self.assertEqual({w: round(x, 3) for w, x in t.items()}, {"A": 0.611, "B": 0.529, "C": 0.638})

    def test_several_seeds_beat_voting(self):
        for seed in (1, 2, 3, 4, 5):
            truth, claims = synthetic(seed)
            s, _, _ = truthfinder(claims, imp=exclusive_implication())
            self.assertGreater(accuracy(answers(s), truth), accuracy(voting(claims), truth))


if __name__ == "__main__":
    unittest.main()
