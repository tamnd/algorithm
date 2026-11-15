# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/justification-based-truth-maintenance/. The authors are listed in prov/.

import random
import unittest
from itertools import combinations

from justification_based_truth_maintenance import IN, OUT, UNDEC, JTMS


def subsets(universe):
    for k in range(len(universe) + 1):
        yield from combinations(universe, k)


def unfounded(rules, u, true, false):
    """Each rule for an atom of u has an in-node that is false or in u, or an out-node that is true."""
    for h, ins, outs in rules:
        if h in u and not (any(b in false or b in u for b in ins) or any(c in true for c in outs)):
            return False
    return True


def wfs_brute(rules, universe):
    """The well-founded model as the least fixpoint of W(T, F) = (T_P(T, F), greatest unfounded set), all by brute force."""
    true, false = frozenset(), frozenset()
    while True:
        new_true = frozenset(h for h, ins, outs in rules if all(b in true for b in ins) and all(c in false for c in outs))
        gus = set()
        for s in subsets(universe):
            if unfounded(rules, set(s), true, false):
                gus.update(s)
        new_false = frozenset(gus)
        if (new_true, new_false) == (true, false):
            return true, false
        true, false = new_true, new_false


def least_model(definite):
    m = set()
    while True:
        nxt = {h for h, ins in definite if all(b in m for b in ins)}
        if nxt <= m:
            return m
        m |= nxt


def stable_models_brute(rules, universe):
    out = []
    for s in subsets(universe):
        s = set(s)
        reduct = [(h, ins) for h, ins, outs in rules if not any(c in s for c in outs)]
        if least_model(reduct) == s:
            out.append(frozenset(s))
    return out


def labels_from(universe, true, false):
    return {x: IN if x in true else OUT if x in false else UNDEC for x in universe}


class TestJTMS(unittest.TestCase):
    def test_page_example(self):
        t = JTMS()
        t.justify("flies", ins=["bird"], outs=["abnormal"])
        t.justify("abnormal", ins=["penguin"])
        a_bird = t.assume("bird")
        self.assertEqual((t.label["bird"], t.label["flies"], t.label["abnormal"]), (IN, IN, OUT))
        a_penguin = t.assume("penguin")
        self.assertEqual((t.label["penguin"], t.label["abnormal"], t.label["flies"]), (IN, IN, OUT))
        t.retract(a_penguin)
        self.assertEqual((t.label["abnormal"], t.label["flies"]), (OUT, IN))
        t.retract(a_bird)
        self.assertEqual(t.label["flies"], OUT)

    def test_loops(self):
        t = JTMS()
        t.justify("p", outs=["q"])
        t.justify("q", outs=["p"])  # an even loop: two stable models, so the well-founded labels are UNDEC
        self.assertEqual((t.label["p"], t.label["q"]), (UNDEC, UNDEC))
        t.justify("r", outs=["r"])  # an odd loop: no stable model
        self.assertEqual(t.label["r"], UNDEC)
        t.justify("s", ins=["s"])  # a positive loop has no support
        self.assertEqual(t.label["s"], OUT)
        t.assume("q")
        self.assertEqual((t.label["p"], t.label["q"]), (OUT, IN))

    def test_random_against_brute_force(self):
        rng = random.Random(20261115)
        undecided = 0
        for _ in range(250):
            n = rng.randint(1, 8)
            universe = list(range(n))
            t = JTMS()
            for x in universe:
                t.add_node(x)
            live = {}
            for _ in range(14):
                if live and rng.random() < 0.35:
                    jid = rng.choice(sorted(live))
                    t.retract(jid)
                    del live[jid]
                else:
                    x = rng.randrange(n)
                    ins = tuple(rng.sample(universe, rng.randint(0, min(2, n))))
                    outs = tuple(rng.sample(universe, rng.randint(0, min(2, n))))
                    live[t.justify(x, ins, outs)] = (x, ins, outs)
                rules = list(live.values())
                true, false = wfs_brute(rules, universe)
                self.assertEqual(t.label, labels_from(universe, true, false))
                undecided += len(true) + len(false) < n
            if len(true) + len(false) == n:
                self.assertEqual(stable_models_brute(rules, universe), [true])
        self.assertGreater(undecided, 100)  # the random networks do reach the UNDEC case


if __name__ == "__main__":
    unittest.main()
