# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-file/. The authors are listed in prov/FWEZG7.jsonl.

import math
import random
import unittest

from heap_file import SLOT, DirectoryHeapFile, ListHeapFile


def rand_rec(rng, hi):
    return bytes(rng.randrange(256) for _ in range(rng.randrange(1, hi)))


class TestDirectoryHeapFile(unittest.TestCase):
    def test_worked_example(self):
        # The example on the page: pages of 100 bytes, D = 2 entries per directory page.
        h = DirectoryHeapFile(capacity=100, entries_per_dir_page=2)
        sizes = [56, 46, 36, 26, 26]
        ios = []
        rids = []
        for n in sizes:
            rids.append(h.insert(b"x" * n))
            ios.append(h.last_io)
        self.assertEqual(rids, [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0)])
        self.assertEqual(ios, [(1, 2), (1, 2), (2, 2), (2, 2), (1, 3)])
        self.assertEqual([e for d in h.directory for e in d], [[0, 0], [1, 20], [2, 70]])
        self.assertEqual(h.n_dir_pages(), 2)
        h.delete((1, 0))
        self.assertEqual(h.last_io, (2, 2))
        self.assertEqual(h.directory[0][1], [1, 70])
        self.assertEqual(h.insert(b"y" * 30), (1, 0))
        self.assertEqual(h.last_io, (2, 2))
        self.assertEqual(h.directory[0][1], [1, 36])
        before = h.reads
        self.assertEqual(len(list(h.scan())), 5)
        self.assertEqual(h.reads - before, 2 + 3)

    def test_get_costs_one_read(self):
        h = DirectoryHeapFile(capacity=64, entries_per_dir_page=4)
        rid = h.insert(b"abc")
        self.assertEqual(h.get(rid), b"abc")
        self.assertEqual(h.last_io, (1, 0))
        with self.assertRaises(KeyError):
            h.get((0, 5))

    def test_record_too_big(self):
        h = DirectoryHeapFile(capacity=32)
        with self.assertRaises(ValueError):
            h.insert(b"z" * 29)
        h.insert(b"z" * 28)

    def test_random_against_oracle(self):
        for seed in range(12):
            rng = random.Random(seed)
            cap = rng.choice([64, 128, 256])
            d = rng.choice([1, 2, 3, 8])
            h = DirectoryHeapFile(capacity=cap, entries_per_dir_page=d)
            oracle = {}
            free = []  # the oracle's own record of free bytes per page
            for _ in range(300):
                if rng.random() < 0.65 or not oracle:
                    rec = rand_rec(rng, cap // 3)
                    need = len(rec) + SLOT
                    fit = next((p for p, f in enumerate(free) if f >= need), None)
                    last_full = len(h.directory[-1]) == d
                    rid = h.insert(rec)
                    if fit is None:
                        self.assertEqual(rid[0], len(free))
                        free.append(cap)
                        self.assertEqual(h.last_io, (h.n_dir_pages() - (1 if last_full else 0), 3 if last_full else 2))
                    else:
                        self.assertEqual(rid[0], fit)
                        self.assertEqual(h.last_io, (fit // d + 2, 2))
                    free[rid[0]] -= need
                    oracle[rid] = rec
                else:
                    rid = rng.choice(sorted(oracle))
                    h.delete(rid)
                    self.assertEqual(h.last_io, (2, 2))
                    free[rid[0]] += len(oracle.pop(rid)) + SLOT
                h.check()
            self.assertEqual(h.records(), oracle)
            n = h.n_pages()
            self.assertEqual(h.n_dir_pages(), max(1, math.ceil(n / d)))
            before = h.reads
            self.assertEqual(dict(h.scan()), oracle)
            self.assertEqual(h.reads - before, n + h.n_dir_pages())
            for rid, rec in oracle.items():
                self.assertEqual(h.get(rid), rec)


class TestListHeapFile(unittest.TestCase):
    def test_worked_example(self):
        h = ListHeapFile(capacity=100, min_free=20)
        sizes = [56, 46, 36, 26, 26]
        rids = [h.insert(b"x" * n) for n in sizes]
        self.assertEqual(rids, [(0, 0), (1, 0), (1, 1), (0, 1), (2, 0)])
        self.assertEqual(h.full_list(), [0, 1])
        self.assertEqual(h.free_list(), [2])
        h.delete((1, 0))
        self.assertEqual(h.full_list(), [0])
        self.assertEqual(h.free_list(), [1, 2])
        before = h.reads
        self.assertEqual(len(list(h.scan())), 4)
        self.assertEqual(h.reads - before, 1 + 3)

    def test_random_against_oracle(self):
        for seed in range(12):
            rng = random.Random(100 + seed)
            cap = rng.choice([64, 128, 256])
            h = ListHeapFile(capacity=cap, min_free=rng.choice([8, 16, 24]))
            oracle = {}
            for _ in range(300):
                if rng.random() < 0.65 or not oracle:
                    rec = rand_rec(rng, cap // 3)
                    fl = h.free_list()
                    fit = next((i for i, p in enumerate(fl) if h.pages[p].fits(rec)), None)
                    rid = h.insert(rec)
                    r, w = h.last_io
                    if fit is None:
                        self.assertEqual(rid[0], h.n_pages() - 1)
                        self.assertLessEqual(r, 1 + len(fl) + 1)
                    else:
                        self.assertEqual(rid[0], fl[fit])
                        self.assertLessEqual(r, 1 + (fit + 1) + 2)
                        if rid[0] in h.free_list():
                            self.assertEqual((r, w), (fit + 2, 1))
                    self.assertLessEqual(w, 5)
                    oracle[rid] = rec
                else:
                    rid = rng.choice(sorted(oracle))
                    h.delete(rid)
                    del oracle[rid]
                    r, w = h.last_io
                    self.assertLessEqual(r, 5)
                    self.assertLessEqual(w, 5)
                h.check()
            self.assertEqual(h.records(), oracle)
            before = h.reads
            self.assertEqual(dict(h.scan()), oracle)
            self.assertEqual(h.reads - before, 1 + h.n_pages())


if __name__ == "__main__":
    unittest.main()
