# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/n-ary-storage-model/. The authors are listed in prov/HJWXRS.jsonl.

import math
import random
import unittest

from n_ary_storage_model import NSMFile, Page, PageFull, Schema, records_per_page


def random_tuple(rng, types):
    out = []
    for t in types:
        if t == "int":
            out.append(rng.randrange(-2 ** 63, 2 ** 63))
        else:
            out.append("".join(rng.choice("abcxyzé") for _ in range(rng.randrange(0, 12))))
    return tuple(out)


class TestNSM(unittest.TestCase):
    def test_worked_example(self):
        schema = Schema(["int", "str", "int"])
        page = Page(64)
        self.assertEqual(page.insert(schema, (962, "Jane", 30)), 0)
        self.assertEqual(page.insert(schema, (7658, "John", 45)), 1)
        page.log.clear()
        self.assertEqual(page.header(), (2, 20))
        self.assertEqual(page.slot(0), (42, 22))
        self.assertEqual(page.slot(1), (20, 22))
        self.assertEqual(page.free(), 8)
        self.assertEqual(bytes(page.data[60:64]), b"Jane")
        page.log.clear()
        self.assertEqual(page.attr(schema, 1, 2), 45)
        self.assertEqual(page.log, [(8, 4), (30, 8)])
        self.assertEqual(page.attr(schema, 0, 1), "Jane")
        with self.assertRaises(PageFull):
            page.insert(schema, (1, "Ann", 2))

    def test_round_trip_against_a_list(self):
        for seed in range(30):
            rng = random.Random(seed)
            types = [rng.choice(["int", "str"]) for _ in range(rng.randrange(1, 6))]
            f = NSMFile(types, page_size=rng.choice([128, 256, 4096]))
            model = {}
            for _ in range(300):
                if model and rng.random() < 0.2:
                    rid = rng.choice(sorted(model))
                    f.delete(rid)
                    del model[rid]
                else:
                    t = random_tuple(rng, types)
                    rid = f.insert(t)
                    self.assertNotIn(rid, model)
                    model[rid] = t
                f.check()
            self.assertEqual(list(f.scan()), [model[r] for r in sorted(model)])
            for rid in rng.sample(sorted(model), min(10, len(model))):
                self.assertEqual(f.get(rid), model[rid])
            cols = sorted(rng.sample(range(len(types)), rng.randrange(1, len(types) + 1)))
            self.assertEqual(list(f.scan(cols)),
                             [tuple(model[r][j] for j in cols) for r in sorted(model)])

    def test_page_count(self):
        for k in (1, 2, 8, 16):
            s = 8 * k
            for n_records in (0, 1, 59, 60, 61, 1000):
                f = NSMFile(["int"] * k, page_size=4096)
                for i in range(n_records):
                    f.insert(tuple(range(i, i + k)))
                m = records_per_page(4096, s)
                self.assertEqual(m, (4096 - 4) // (s + 4))
                self.assertEqual(len(f.pages), math.ceil(n_records / m))

    def test_cache_lines_of_a_scan(self):
        p, line, k = 4096, 32, 8
        s = 8 * k
        m = (p - 4) // (s + 4)
        self.assertEqual(m, 60)
        for n_records in (60, 150, 600):
            f = NSMFile(["int"] * k, page_size=p)
            for i in range(n_records):
                f.insert(tuple(range(i, i + k)))
            sizes = [min(m, n_records - m * i) for i in range(len(f.pages))]
            slot_lines = sum(math.ceil((4 + 4 * c) / line) for c in sizes)
            f.clear_logs()
            self.assertEqual(sum(1 for _ in f.scan([3])), n_records)
            self.assertEqual(f.lines_touched(line), n_records + slot_lines)
            f.clear_logs()
            list(f.scan())
            self.assertEqual(f.lines_touched(line), n_records * s // line + slot_lines)

    def test_records_do_not_overlap_after_many_pages(self):
        f = NSMFile(["str", "int"], page_size=64)
        rids = [f.insert(("x" * (i % 30), i)) for i in range(200)]
        f.check()
        self.assertEqual([f.get(r)[1] for r in rids], list(range(200)))
        with self.assertRaises(PageFull):
            f.insert(("y" * 60, 0))

    def test_bad_schema(self):
        with self.assertRaises(ValueError):
            Schema([])
        with self.assertRaises(ValueError):
            Schema(["float"])


if __name__ == "__main__":
    unittest.main()
