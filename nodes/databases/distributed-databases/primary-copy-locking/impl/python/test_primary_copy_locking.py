# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primary-copy-locking/. The authors are listed in prov/SBHSMT.jsonl.
import itertools
import random
import unittest

from primary_copy_locking import PrimaryCopyDB

PLACEMENT = {"x": ["A", "B", "C"], "y": ["B", "C"], "z": ["A", "C"]}
SITES = ["A", "B", "C", "D"]


def item(copy):
    return copy.split("@")[0]


def physical_view(db):
    """Reads-from on items and the final writer of each copy, from the
    copy-level history. Every write in the history is committed."""
    committed = {t for t, x in db.txns.items() if x.status == "committed"}
    last = {}
    rf = {}
    for kind, t, c in db.history:
        if kind == "w":
            last[c] = t
        elif kind == "r" and t in committed:
            rf[(t, item(c))] = last.get(c, 0)
    return committed, rf, last


def serial_view(db, order):
    last, rf = {}, {}
    for t in order:
        for kind, x in db.txns[t].ops:
            if kind == "r" and (t, x) not in rf:
                rf[(t, x)] = last.get(x, 0)
            elif kind == "w":
                last[x] = t
    return rf, last


def equivalent(db, order):
    """The definition of one-copy serializability (BHG Section 8.3)."""
    committed, rf, final_copy = physical_view(db)
    rf1, final1 = serial_view(db, order)
    if rf1 != rf:
        return False
    return all(any(item(c) == x and t == w for c, t in final_copy.items())
               for x, w in final1.items())


def one_copy_orders(db):
    committed = sorted(t for t, x in db.txns.items() if x.status == "committed")
    assert len(committed) <= 6
    return [o for o in itertools.permutations(committed) if equivalent(db, o)]


def random_txns(rng, n):
    txns, homes = {}, {}
    for tid in range(1, n + 1):
        ops = []
        for x in rng.sample(sorted(PLACEMENT), rng.randint(1, 2)):
            ops += [(k, x) for k in rng.choice([["r"], ["w"], ["r", "w"]])]
        txns[tid] = ops
        homes[tid] = rng.choice(SITES)
    return txns, homes


def live_copies_agree(db):
    for x, sites in PLACEMENT.items():
        if not db.sites[db.primary[x]].up:
            continue
        vals = {db.sites[s].value[x] for s in sites if db.sites[s].up}
        if len(vals) > 1:
            return False
    return True


class TestPrimaryCopy(unittest.TestCase):
    def test_one_copy_serializable_in_commit_order(self):
        for seed in range(200):
            rng = random.Random(seed)
            db = PrimaryCopyDB(PLACEMENT)
            txns, homes = random_txns(rng, rng.randint(2, 4))
            db.run(rng, txns, homes)
            committed = [t for t in db.commit_order if db.txns[t].status == "committed"]
            self.assertTrue(equivalent(db, committed), seed)
            self.assertTrue(live_copies_agree(db), seed)

    def test_with_site_failures(self):
        for seed in range(200):
            rng = random.Random(1000 + seed)
            db = PrimaryCopyDB(PLACEMENT)
            txns, homes = random_txns(rng, 3)
            events = [(rng.randrange(8), "fail", rng.choice(["A", "B", "C"]))]
            db.run(rng, txns, homes, events)
            committed = [t for t in db.commit_order if db.txns[t].status == "committed"]
            self.assertTrue(equivalent(db, committed), seed)
            self.assertTrue(live_copies_agree(db), seed)

    def test_early_release_is_wrong(self):
        bad = 0
        for seed in range(200):
            rng = random.Random(seed)
            db = PrimaryCopyDB(PLACEMENT, early_release=True)
            txns, homes = random_txns(rng, 3)
            db.run(rng, txns, homes)
            bad += not one_copy_orders(db)
        self.assertGreater(bad, 0)

    def test_locks_only_at_the_primary(self):
        # A write of x with three copies, from a home site that holds no copy:
        # lock request and grant at A, two installs and two acks, one release.
        db = PrimaryCopyDB(PLACEMENT)
        db.run(random.Random(0), {1: [("w", "x")]}, {1: "D"})
        self.assertEqual(db.messages, 2 + 2 * 2 + 1)
        self.assertEqual(sorted(c for k, t, c in db.history if k == "w"), ["x@A", "x@B", "x@C"])
        self.assertEqual({db.sites[s].value["x"] for s in "ABC"}, {100})

    def test_read_costs(self):
        # Reading the local copy at B needs a lock at the primary A: 2 messages.
        db = PrimaryCopyDB(PLACEMENT)
        db.run(random.Random(0), {1: [("r", "x")]}, {1: "B"})
        self.assertEqual(db.messages, 2 + 1)            # lock, grant, release
        self.assertEqual(db.history[0], ("r", 1, "x@B"))
        # With no local copy, the lock request reads the primary copy at once.
        db = PrimaryCopyDB(PLACEMENT)
        db.run(random.Random(0), {1: [("r", "y")]}, {1: "A"})
        self.assertEqual(db.messages, 2 + 1)
        self.assertEqual(db.history[0], ("r", 1, "y@B"))
        # At the primary site itself, a read sends no message.
        db = PrimaryCopyDB(PLACEMENT)
        db.run(random.Random(0), {1: [("r", "x")]}, {1: "A"})
        self.assertEqual(db.messages, 0)

    def test_failed_primary_makes_the_item_unavailable(self):
        db = PrimaryCopyDB(PLACEMENT)
        db.fail("A")
        db.run(random.Random(0), {1: [("r", "x")], 2: [("r", "y")]}, {1: "B", 2: "C"})
        self.assertEqual(db.txns[1].status, "aborted")
        self.assertEqual(db.txns[2].status, "committed")

    def test_deadlock_on_upgrade_is_broken(self):
        found = False
        for seed in range(80):
            db = PrimaryCopyDB(PLACEMENT)
            db.run(random.Random(seed), {1: [("r", "x"), ("w", "x")], 2: [("r", "x"), ("w", "x")]},
                   {1: "B", 2: "C"}, start_spread=1)
            self.assertTrue(one_copy_orders(db))
            for victim, cycle in db.victims:
                found = True
                self.assertEqual(victim, max(cycle))
        self.assertTrue(found)

    def test_oracle_rejects_a_stale_read(self):
        # T1 writes x at A only, then T2 reads the old copy at B and writes y,
        # and T1 read y: the BHG history H1 is serial but not 1SR.
        db = PrimaryCopyDB({"x": ["A", "B"], "y": ["C"]})
        db.txns = {}
        from primary_copy_locking import Txn
        db.txns[1] = Txn(1, [("r", "y"), ("w", "x")], "A")
        db.txns[2] = Txn(2, [("r", "x"), ("w", "y")], "A")
        db.txns[1].status = db.txns[2].status = "committed"
        db.history = [("r", 1, "y@C"), ("w", 1, "x@A"), ("r", 2, "x@B"), ("w", 2, "y@C")]
        self.assertEqual(one_copy_orders(db), [])


if __name__ == "__main__":
    unittest.main()
