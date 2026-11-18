# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bw-tree/. The authors are listed in prov/R4MGVH.jsonl.

import random
import unittest

from bw_tree import BwTree, Delta, base_of, bounds, chain_length, run, run_one


def apply(state, name, k, v):
    """The sequential reference: a Python dict. Returns (result, new state)."""
    old = state.get(k)
    if name == "lookup":
        return old, state
    s = dict(state)
    if name == "upsert":
        s[k] = v
    else:
        s.pop(k, None)
    return old, s


def linearizable(log, init):
    """Brute force: is there an order of the operations that respects real
    time (an operation that ended before another started comes first) and in
    which every result matches the dict reference?"""
    ops = list(log)
    n = len(ops)

    def dfs(done, state):
        if len(done) == n:
            return True
        pending = [i for i in range(n) if i not in done]
        for i in pending:
            t, name, k, v, res, s, e = ops[i]
            # i may go next only if no pending operation ended before i started
            if any(ops[j][6] < s for j in pending if j != i):
                continue
            r, s2 = apply(state, name, k, v)
            if r == res and dfs(done | {i}, s2):
                return True
        return False

    return dfs(frozenset(), dict(init))


def preload(tree, keys):
    for k in keys:
        run_one(tree, tree.upsert(k, "v%d" % k))


class TestSequential(unittest.TestCase):
    def test_against_a_dict(self):
        rng = random.Random(1)
        for seed in range(4):
            t = BwTree(max_leaf=4, max_inner=4, max_chain=3)
            ref = {}
            for i in range(400):
                k = rng.randrange(150)
                r = rng.random()
                if r < 0.6:
                    self.assertEqual(run_one(t, t.upsert(k, i)), ref.get(k))
                    ref[k] = i
                elif r < 0.8:
                    self.assertEqual(run_one(t, t.delete(k)), ref.pop(k, None))
                else:
                    self.assertEqual(run_one(t, t.lookup(k)), ref.get(k))
            self.assertEqual(t.items(), sorted(ref.items()))
            self.assertGreaterEqual(t.height(), 3)
            self.assertGreater(t.stats["split"], 0)
            self.assertGreater(t.stats["consolidate"], 0)

    def test_delta_chain_and_consolidation(self):
        t = BwTree(max_leaf=8, max_inner=4, max_chain=3)
        for k in (5, 1, 9):
            run_one(t, t.upsert(k, k))
        h = t.M[0]
        self.assertEqual(chain_length(h), 3)
        self.assertEqual([h.kind, h.key, h.nxt.key, h.nxt.nxt.key], ["ins", 9, 1, 5])
        run_one(t, t.delete(1))      # the fourth delta makes the chain too long
        h = t.M[0]
        self.assertEqual(chain_length(h), 0)
        self.assertEqual(h.keys, [5, 9])


class TestConcurrent(unittest.TestCase):
    def test_disjoint_writers_and_static_readers(self):
        """Each writer owns its keys; readers look up keys that never change."""
        for seed in range(6):
            rng = random.Random(seed)
            t = BwTree(max_leaf=4, max_inner=4, max_chain=2)
            static = list(range(0, 400, 10))
            preload(t, static)
            ops, final = [], {k: "v%d" % k for k in static}
            for w in range(4):
                for i in range(60):
                    k = 10 * rng.randrange(40) + 1 + w     # writer w owns the keys that end in w + 1
                    if rng.random() < 0.75:
                        ops.append((w, "upsert", k, (w, i)))
                        final[k] = (w, i)
                    else:
                        ops.append((w, "delete", k, None))
                        final.pop(k, None)
            for r in range(4, 6):
                for i in range(40):
                    ops.append((r, "lookup", rng.choice(static), None))
            owners = {}
            for w, name, k, v in ops:
                if name != "lookup":
                    self.assertEqual(owners.setdefault(k, w), w)
            res = run(t, ops, seed)
            for th, name, k, v, out in res:
                if name == "lookup":
                    self.assertEqual(out, "v%d" % k)
            self.assertEqual(t.items(), sorted(final.items()))
            self.assertGreater(t.stats["cas_fail"], 0)
            self.assertGreater(t.stats["split"] + t.stats["root_split"], 3)

    def test_linearizable_on_shared_keys(self):
        fails = 0
        for seed in range(60):
            rng = random.Random(100 + seed)
            t = BwTree(max_leaf=2, max_inner=2, max_chain=1)
            init = {k: "init" for k in range(0, 12, 2)}
            for k in init:
                run_one(t, t.upsert(k, "init"))
            t.stats["cas_fail"] = 0
            ops = []
            for th in range(3):
                for i in range(4):
                    name = rng.choice(["upsert", "upsert", "delete", "lookup"])
                    ops.append((th, name, rng.randrange(12), (th, i) if name == "upsert" else None))
            log = []
            run(t, ops, seed, log)
            self.assertTrue(linearizable(log, init), log)
            fails += t.stats["cas_fail"]
            t.items()                                       # the leaf level is still contiguous
        self.assertGreater(fails, 0)                        # the runs did have races

    def test_checker_rejects_a_bad_history(self):
        # Thread 0 writes 5 and ends; then thread 1 starts and reads nothing.
        bad = [(0, "upsert", 5, "a", None, 1, 2), (1, "lookup", 5, None, None, 3, 4)]
        self.assertFalse(linearizable(bad, {}))
        good = [(0, "upsert", 5, "a", None, 1, 4), (1, "lookup", 5, None, None, 2, 3)]
        self.assertTrue(linearizable(good, {}))

    def test_half_done_split_is_helped(self):
        """Stop a split after its split delta; a later reader posts the index term."""
        t = BwTree(max_leaf=4, max_inner=8, max_chain=10)
        ref = {k: "v%d" % k for k in range(0, 50, 5)}
        preload(t, ref)                               # several leaves under one root
        self.assertEqual(base_of(t.M[0]).level, 1)
        root_before = t.M[0]
        g = t.upsert(41, "x")
        ref[41] = "x"
        # Run the upsert until its split delta is installed, then stop it.
        old_heads = {id(h) for h in t.M.values()}
        split = None
        while split is None:
            next(g)
            split = next((h for h in t.M.values() if id(h) not in old_heads
                          and isinstance(h, Delta) and h.kind == "split"), None)
        sep = split.key
        self.assertIs(t.M[0], root_before)            # the parent has no index term yet
        helps = t.stats["help"]
        # A lookup that needs the new page still finds it by the side link.
        self.assertEqual(run_one(t, t.lookup(sep)), ref[sep])
        root = t.M[0]                                 # and it posted the index term
        self.assertIsInstance(root, Delta)
        self.assertEqual((root.kind, root.key, root.val[0]), ("term", sep, split.val))
        self.assertEqual(t.stats["help"], helps + 1)
        for k in range(50):
            self.assertEqual(run_one(t, t.lookup(k)), ref.get(k))
        self.assertEqual(t.items(), sorted(ref.items()))


if __name__ == "__main__":
    unittest.main()
