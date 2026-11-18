# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pax-page-layout/. The authors are listed in prov/2CYGS7.jsonl.

import math
import random
import struct
import unittest

from pax_page_layout import PaxFile, PaxPage, PageFull, capacity, counts_by_page


def random_tuple(rng, types):
    out = []
    for t in types:
        if t == "int":
            out.append(rng.randrange(-2 ** 63, 2 ** 63))
        else:
            out.append("".join(rng.choice("abcxyzé") for _ in range(rng.randrange(0, 12))))
    return tuple(out)


def lines_of(lo, hi, line):
    """The cache lines that meet the byte range [lo, hi)."""
    return set(range(lo // line, (hi - 1) // line + 1)) if hi > lo else set()


class TestPAX(unittest.TestCase):
    def test_worked_example(self):
        page = PaxPage(["int", "str", "int"], size=128, avg=[0, 4, 0])
        self.assertEqual(page.c, 5)
        self.assertEqual(page.start, [16, 56, 88])
        self.assertEqual(page.end, [56, 88, 128])
        self.assertEqual(page.insert((962, "Jane", 30)), 0)
        self.assertEqual(page.insert((7658, "John", 45)), 1)
        self.assertEqual(struct.unpack_from("<HHHHH", page.data, 0), (2, 5, 16, 56, 88))
        self.assertEqual(page.data[10], 0b11)
        self.assertEqual(struct.unpack_from("<qq", page.data, 16), (962, 7658))
        self.assertEqual(struct.unpack_from("<HH", page.data, 56), (4, 8))
        self.assertEqual(bytes(page.data[66:74]), b"JaneJohn")
        self.assertEqual(struct.unpack_from("<qq", page.data, 88), (30, 45))
        self.assertEqual(page.text_free(1), 14)
        page.log.clear()
        self.assertEqual([row for _, row in page.scan([2])], [(30,), (45,)])
        self.assertEqual(page.log, [(0, 11), (88, 8), (96, 8)])
        with self.assertRaises(PageFull):
            page.insert((1, "x" * 15, 2))
        self.assertEqual(page.insert((1, "x" * 14, 2)), 2)
        page.delete(0)
        self.assertEqual([row for _, row in page.scan([0, 1])], [(7658, "John"), (1, "x" * 14)])

    def test_round_trip_against_a_list(self):
        for seed in range(30):
            rng = random.Random(seed)
            types = [rng.choice(["int", "str"]) for _ in range(rng.randrange(1, 6))]
            avg = [rng.randrange(0, 12) for _ in types]
            f = PaxFile(types, page_size=rng.choice([128, 256, 4096]), avg=avg)
            model = {}
            for _ in range(300):
                if model and rng.random() < 0.2:
                    rid = rng.choice(sorted(model))
                    f.delete(rid)
                    del model[rid]
                else:
                    t = random_tuple(rng, types)
                    try:
                        rid = f.insert(t)
                    except PageFull:
                        self.assertTrue(any(len(str(v).encode()) > 0 for v in t))
                        continue
                    self.assertNotIn(rid, model)
                    model[rid] = t
                f.check()
            self.assertEqual(list(f.scan()), [model[r] for r in sorted(model)])
            for rid in rng.sample(sorted(model), min(10, len(model))):
                self.assertEqual(f.get(rid), model[rid])
            cols = sorted(rng.sample(range(len(types)), rng.randrange(1, len(types) + 1)))
            self.assertEqual(list(f.scan(cols)),
                             [tuple(model[r][j] for j in cols) for r in sorted(model)])

    def test_capacity_and_page_count(self):
        self.assertEqual(capacity(["int"] * 8, 4096), 63)
        for k in (1, 2, 8, 16):
            c = capacity(["int"] * k, 4096)
            header = 4 + 2 * k + math.ceil(c / 8)
            self.assertLessEqual(math.ceil(header / 8) * 8 + 8 * k * c, 4096)
            self.assertGreater(math.ceil((4 + 2 * k + math.ceil((c + 1) / 8)) / 8) * 8 + 8 * k * (c + 1), 4096)
            for n_records in (1, c, c + 1, 1000):
                f = PaxFile(["int"] * k, page_size=4096)
                for i in range(n_records):
                    f.insert(tuple(range(i, i + k)))
                self.assertEqual(len(f.pages), math.ceil(n_records / c))

    def test_cache_lines_of_a_scan(self):
        p, line, k = 4096, 32, 8
        c = capacity(["int"] * k, p)
        for n_records in (63, 150, 600):
            f = PaxFile(["int"] * k, page_size=p)
            for i in range(n_records):
                f.insert(tuple(range(i, i + k)))
            for cols in ([3], [0, 5], list(range(k))):
                f.clear_logs()
                self.assertEqual(sum(1 for _ in f.scan(cols)), n_records)
                expected = 0
                for q, n in counts_by_page(n_records, c).items():
                    page = f.pages[q]
                    touched = lines_of(0, page.header_size, line)
                    for j in cols:
                        touched |= lines_of(page.start[j], page.start[j] + 8 * n, line)
                    expected += len(touched)
                self.assertEqual(f.lines_touched(line), expected)
        # one attribute of a full page: one header line and 16 lines of values
        f = PaxFile(["int"] * k, page_size=p)
        for i in range(c):
            f.insert(tuple(range(k)))
        f.clear_logs()
        list(f.scan([0]))
        self.assertEqual(f.lines_touched(line), 17)

    def test_errors(self):
        with self.assertRaises(ValueError):
            PaxPage([])
        with self.assertRaises(ValueError):
            PaxPage(["int"] * 10, size=64)
        f = PaxFile(["str"], page_size=64, avg=[4])
        with self.assertRaises(PageFull):
            f.insert(("y" * 64,))
        self.assertEqual(f.pages, [])


if __name__ == "__main__":
    unittest.main()
