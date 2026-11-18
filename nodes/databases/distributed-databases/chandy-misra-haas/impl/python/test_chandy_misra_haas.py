# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandy-misra-haas/. The authors are listed in prov/H4QN6P.jsonl.
import random
import unittest

from chandy_misra_haas import CMH

SITES = ["S1", "S2", "S3"]


def wait_graph(db):
    """The global wait-for graph of idle processes, built from the raw
    state of all controllers at once. The algorithm never sees this."""
    idle = set()
    for s, c in db.ctl.items():
        for t in c.waiting:
            idle.add((t, s))
        for t, held in c.held.items():
            tx = db.txns[t]
            if held and s != tx.home and t not in c.waiting and tx.outstanding != s:
                idle.add((t, s))                 # an agent waiting for its home
    for t in db.txns.values():
        if t.status == "active" and t.outstanding is not None:
            idle.add((t.tid, t.home))
    edges = {p: [] for p in idle}
    for t, s in idle:
        c, tx = db.ctl[s], db.txns[t]
        if t in c.waiting:
            nxt = (c.holder[c.waiting[t]], s)
        elif s == tx.home:
            nxt = (t, tx.outstanding)
        else:
            nxt = (t, tx.home)
        if nxt in idle:
            edges[(t, s)].append(nxt)
    return edges


def on_cycle(edges, p):
    if p not in edges:
        return False
    seen, stack = set(), list(edges[p])
    while stack:
        u = stack.pop()
        if u == p:
            return True
        if u not in seen:
            seen.add(u)
            stack.extend(edges[u])
    return False


def reaches(edges, p, q):
    seen, stack = set(), [p]
    while stack:
        u = stack.pop()
        if u == q:
            return True
        if u not in seen:
            seen.add(u)
            stack.extend(edges[u])
    return False


def remote_edge_count(db):
    """Wait edges between controllers that start at an idle process."""
    e = sum(1 for t in db.txns.values() if t.status == "active" and t.outstanding is not None)
    for s, c in db.ctl.items():
        e += sum(1 for t, held in c.held.items()
                 if held and t not in c.waiting and s != db.txns[t].home)
    return e


def random_txns(rng):
    where = {"r%d" % j: rng.choice(SITES) for j in range(5)}
    txns = {}
    for tid in range(1, rng.randint(3, 5) + 1):
        plan = [(r, where[r]) for r in rng.sample(sorted(where), rng.randint(2, 3))]
        txns[tid] = (rng.choice(SITES), plan)
    return txns


def cross_cycle():
    """T1 at S1 holds a, T2 at S2 holds b, T1 asks for b and T2 asks for a.
    The cycle is (1,S1) -> (1,S2) -> (2,S2) -> (2,S1) -> (1,S1), and the
    edge into (1,S1) is local."""
    return {1: ("S1", [("a", "S1"), ("b", "S2")]),
            2: ("S2", [("b", "S2"), ("a", "S1")])}


class TestCMH(unittest.TestCase):
    def check_sound(self, literal):
        # No victims: a deadlock stays, and the other transactions go on and
        # change the wait-for graph while probes are in flight. Every
        # declaration must be a process on a cycle at that moment, and every
        # cycle left at the end must have a declared process.
        found = 0
        for seed in range(150):
            rng = random.Random(seed)
            db = CMH(SITES, literal=literal, resolve=False)

            def hook(p, db=db):
                self.assertTrue(on_cycle(wait_graph(db), p), (seed, p))

            db.on_declare = hook
            db.run(rng, random_txns(rng))
            edges = wait_graph(db)
            for p in edges:
                if on_cycle(edges, p):
                    comp = {q for q in edges if on_cycle(edges, q) and reaches(edges, p, q)}
                    self.assertTrue(comp & set(db.declared), (seed, p))
            found += len(db.declared)
        self.assertGreater(found, 100)

    def test_no_false_deadlocks_and_every_cycle_found(self):
        self.check_sound(literal=False)

    def test_literal_rule_with_every_idle_process_initiating(self):
        self.check_sound(literal=True)

    def test_with_victims(self):
        # The process declared deadlocked loses its transaction. Then no
        # transaction is left waiting, but probes that were in flight when
        # a victim aborted can declare a process whose cycle is gone.
        phantom = 0
        for seed in range(150):
            rng = random.Random(seed)
            db = CMH(SITES)

            def hook(p, db=db):
                nonlocal phantom
                if not on_cycle(wait_graph(db), p):
                    self.assertGreater(len(db.declared), 1, seed)   # an abort came first
                    phantom += 1

            db.on_declare = hook
            self.assertEqual(db.run(rng, random_txns(rng)), [], seed)
        self.assertGreater(phantom, 0)

    def test_each_computation_against_the_global_graph(self):
        # Let the system come to rest with no detector, then start one
        # computation at a time: P is declared exactly when P is on a cycle.
        cycles = 0
        for seed in range(150):
            rng = random.Random(seed)
            db = CMH(SITES, resolve=False, timers=False)
            db.run(rng, random_txns(rng), auto=False)
            edges = wait_graph(db)
            e = remote_edge_count(db)
            for p in sorted(edges):
                before, sent = len(db.declared), db.probes
                db.initiate(p)
                db.drain(rng)
                self.assertEqual(p in db.declared[before:], on_cycle(edges, p), (seed, p))
                self.assertLessEqual(db.probes - sent, e * (e + 1))
                cycles += on_cycle(edges, p)
        self.assertGreater(cycles, 20)

    def test_literal_rule_misses_a_local_closing_edge(self):
        # With the literal rule the probe goes round once more and is
        # dropped at (1,S2), whose flag is already set.
        for literal, declared, probes in ((True, [], 3), (False, [(1, "S1")], 2)):
            db = CMH(["S1", "S2"], literal=literal, resolve=False, timers=False)
            db.run(random.Random(0), cross_cycle(), auto=False)
            self.assertTrue(on_cycle(wait_graph(db), (1, "S1")))
            db.initiate((1, "S1"))
            db.drain(random.Random(0))
            self.assertEqual(db.declared, declared)
            self.assertEqual(db.probes, probes)
        # The computation of (2,S1), the end of the remote edge, finds it.
        db = CMH(["S1", "S2"], literal=True, resolve=False, timers=False)
        db.run(random.Random(0), cross_cycle(), auto=False)
        db.initiate((2, "S1"))
        db.drain(random.Random(0))
        self.assertEqual(db.declared, [(2, "S1")])

    def test_numbered_computations(self):
        # The first computation of (1,S1) runs before T3 closes the cycle
        # and leaves flags at (1,S2) and (2,S3). Without numbers they stop
        # the second computation.
        txns = {1: ("S1", [("a", "S1"), ("b", "S2")]),
                2: ("S2", [("b", "S2"), ("c", "S3")]),
                3: ("S3", [("c", "S3"), ("a", "S1")])}
        for numbered in (True, False):
            rng = random.Random(0)
            db = CMH(SITES, numbered=numbered, resolve=False, timers=False)
            for tid in sorted(txns):
                db.start(tid, *txns[tid])
            db.drain(rng, hold=lambda m: m[2] == ("next", 3))
            db.initiate((1, "S1"))
            db.drain(rng, hold=lambda m: m[2] == ("next", 3))
            self.assertEqual(db.declared, [])
            self.assertFalse(on_cycle(wait_graph(db), (1, "S1")))
            db.drain(rng)
            self.assertTrue(on_cycle(wait_graph(db), (1, "S1")))
            db.initiate((1, "S1"))
            db.drain(rng)
            self.assertEqual(db.declared, [(1, "S1")] if numbered else [])

    def test_no_deadlock_no_declaration(self):
        # Two transactions that ask for a and b in the same order wait but
        # never deadlock, even with probes in flight while locks move.
        for seed in range(100):
            rng = random.Random(seed)
            db = CMH(SITES)
            txns = {t: (SITES[t % 3], [("a", "S1"), ("b", "S2"), ("c", "S3")]) for t in (1, 2, 3)}
            self.assertEqual(db.run(rng, txns), [])
            self.assertEqual(db.declared, [])
            self.assertTrue(all(t.status == "committed" for t in db.txns.values()))


if __name__ == "__main__":
    unittest.main()
