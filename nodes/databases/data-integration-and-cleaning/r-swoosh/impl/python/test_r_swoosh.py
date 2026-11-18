# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-swoosh/. The authors are listed in prov/92B1R4.jsonl.
import random
import unittest

from r_swoosh import (
    comparison_bound,
    make_record,
    maximal_records,
    r_swoosh,
    rule_match,
    union_merge,
)

EMAILS = ["e1", "e2", "e3", "e4"]
NAMES = ["ann", "bob", "cal"]
PHONES = ["p1", "p2", "p3"]


def random_records(rng, n):
    out = []
    for i in range(n):
        while True:
            email = rng.choice(EMAILS + [None, None])
            name = rng.choice(NAMES + [None])
            phone = rng.choice(PHONES + [None])
            # Every record matches itself, so the match rule is idempotent.
            if email is not None or (name is not None and phone is not None):
                break
        out.append(make_record(i, email=email, name=name, phone=phone))
    return out


class TestRSwoosh(unittest.TestCase):
    def test_page_example(self):
        r1 = make_record(1, name="ann", phone="p1")
        r2 = make_record(2, name="ann", email="e1")
        r3 = make_record(3, phone="p1", email="e1")
        r4 = make_record(4, name="bob", phone="p1")
        out, calls = r_swoosh([r1, r2, r3, r4], rule_match, union_merge)
        self.assertEqual(sorted(sorted(r[1]) for r in out), [[1, 2, 3], [4]])
        self.assertEqual(calls, 6)
        # The pairs alone match only r2 and r3.
        recs = [r1, r2, r3, r4]
        pairs = [(a + 1, b + 1) for a in range(4) for b in range(a + 1, 4) if rule_match(recs[a], recs[b])]
        self.assertEqual(pairs, [(2, 3)])

    def test_against_merge_closure(self):
        rng = random.Random(20261118)
        for _ in range(300):
            n = rng.randint(0, 7)
            recs = random_records(rng, n)
            out, calls = r_swoosh(recs, rule_match, union_merge)
            self.assertEqual(len(out), len(set(out)))
            self.assertEqual(set(out), maximal_records(recs, rule_match, union_merge))
            for a in range(len(out)):
                for b in range(a + 1, len(out)):
                    self.assertFalse(rule_match(out[a], out[b]))
            self.assertLessEqual(calls, comparison_bound(n, len(out)))

    def test_order_does_not_change_result(self):
        rng = random.Random(9)
        for _ in range(100):
            recs = random_records(rng, rng.randint(1, 8))
            first, _ = r_swoosh(recs, rule_match, union_merge)
            shuffled = recs[:]
            rng.shuffle(shuffled)
            second, _ = r_swoosh(shuffled, rule_match, union_merge)
            self.assertEqual(set(first), set(second))

    def test_bound_is_reached(self):
        # A match rule (not ICAR) that makes every match the last record of R'.
        for n in range(1, 10):
            def match(r, s, n=n):
                u = r | s
                return not (r & s) and (n - 1) in u and max(u) - min(u) + 1 == len(u)

            recs = [frozenset([i]) for i in range(n)]
            out, calls = r_swoosh(recs, match, lambda r, s: r | s)
            self.assertEqual(out, [frozenset(range(n))])
            self.assertEqual(calls, comparison_bound(n, 1))
            self.assertEqual(calls, (n - 1) ** 2)
        # The ICAR rule of the page reaches the bound 4 for n = 3.
        r1 = make_record(1, name="ann", phone="p1")
        r2 = make_record(2, name="ann", email="e1")
        r3 = make_record(3, phone="p1", email="e1")
        out, calls = r_swoosh([r1, r2, r3], rule_match, union_merge)
        self.assertEqual(len(out), 1)
        self.assertEqual(calls, 4)

    def test_no_matches(self):
        for n in range(0, 12):
            recs = [make_record(i, email="x%d" % i) for i in range(n)]
            out, calls = r_swoosh(recs, rule_match, union_merge)
            self.assertEqual(len(out), n)
            self.assertEqual(calls, n * (n - 1) // 2)
            self.assertLessEqual(calls, comparison_bound(n, n))

    def test_precision_recall_synthetic(self):
        rng = random.Random(42)
        recs, truth = [], []
        for e in range(40):
            email = "mail%d" % e
            name = rng.choice(["ann", "bob", "cal", "dan", "eve", "fay", "gus", "hal"])
            phone = "ph%d" % rng.randint(0, 59)
            for _ in range(rng.randint(1, 4)):
                fields = {"email": email, "name": name, "phone": phone}
                drop = rng.random()
                if drop < 0.4:
                    fields["email"] = None
                elif drop < 0.6:
                    fields["phone"] = None
                if fields["email"] is None and fields["phone"] is None:
                    fields["phone"] = phone
                if fields["email"] is None and fields["name"] is None:
                    fields["name"] = name
                recs.append(make_record(len(recs), **fields))
                truth.append(e)
        out, calls = r_swoosh(recs, rule_match, union_merge)
        found = set()
        for r in out:
            ids = sorted(r[1])
            found |= {(a, b) for i, a in enumerate(ids) for b in ids[i + 1:]}
        n = len(recs)
        true = {(a, b) for a in range(n) for b in range(a + 1, n) if truth[a] == truth[b]}
        hit = len(found & true)
        precision = hit / len(found)
        recall = hit / len(true)
        self.assertEqual(sum(len(r[1]) for r in out), n)
        # The numbers on the page: 108 records, 119 true pairs, 46 clusters.
        self.assertEqual((n, len(true), len(out), calls), (108, 119, 46, 3488))
        self.assertEqual(round(precision, 3), 0.926)
        self.assertEqual(round(recall, 3), 0.840)
        self.assertLessEqual(calls, comparison_bound(n, len(out)))


if __name__ == "__main__":
    unittest.main()
