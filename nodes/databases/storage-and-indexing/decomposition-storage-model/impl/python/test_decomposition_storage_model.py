# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decomposition-storage-model/. The authors are listed in prov/Y6XVQQ.jsonl.

import math
import random
import struct
import unittest

from decomposition_storage_model import DSMTable, values_per_page


def random_tuple(rng, types):
    out = []
    for t in types:
        if t == "int":
            out.append(rng.randrange(-2 ** 63, 2 ** 63))
        else:
            out.append("".join(rng.choice("abcxyzé") for _ in range(rng.randrange(0, 12))))
    return tuple(out)


class TestDSM(unittest.TestCase):
    def test_worked_example(self):
        r = DSMTable(["int", "str", "int"], page_size=64)
        self.assertEqual(r.append((962, "Jane", 30)), 0)
        self.assertEqual(r.append((7658, "John", 45)), 1)
        ids, names, ages = (c.pages[0] for c in r.columns)
        self.assertEqual(struct.unpack_from("<HHqq", ids.data, 0), (2, 64, 962, 7658))
        self.assertEqual(struct.unpack_from("<HHHHHH", names.data, 0), (2, 56, 60, 4, 56, 4))
        self.assertEqual(bytes(names.data[56:64]), b"JohnJane")
        self.assertEqual(struct.unpack_from("<HHqq", ages.data, 0), (2, 64, 30, 45))
        r.clear_logs()
        self.assertEqual(r.fetch(1), (7658, "John", 45))
        self.assertEqual(r.pages_touched(), 3)
        r.clear_logs()
        self.assertEqual(list(r.scan([2])), [(30,), (45,)])
        self.assertEqual(r.pages_touched(), 1)
        self.assertEqual(ages.log, [(0, 4), (4, 8), (12, 8)])

    def test_round_trip_against_a_list(self):
        for seed in range(30):
            rng = random.Random(seed)
            types = [rng.choice(["int", "str"]) for _ in range(rng.randrange(1, 6))]
            r = DSMTable(types, page_size=rng.choice([64, 256, 4096]), ids=rng.random() < 0.5)
            rows = []
            for _ in range(rng.randrange(0, 400)):
                t = random_tuple(rng, types)
                self.assertEqual(r.append(t), len(rows))
                rows.append(t)
            r.check()
            self.assertEqual(list(r.scan()), rows)
            cols = sorted(rng.sample(range(len(types)), rng.randrange(1, len(types) + 1)))
            self.assertEqual(list(r.scan(cols)), [tuple(t[j] for j in cols) for t in rows])
            for i in rng.sample(range(len(rows)), min(20, len(rows))):
                self.assertEqual(r.fetch(i), rows[i])
                self.assertEqual(r.fetch(i, cols), tuple(rows[i][j] for j in cols))

    def test_page_counts_and_cache_lines(self):
        p, line, k = 4096, 32, 8
        for ids in (False, True):
            m = values_per_page(p, ids)
            self.assertEqual(m, (p - 4) // (16 if ids else 8))
            for n_records in (1, 511, 512, 513, 3000):
                r = DSMTable(["int"] * k, page_size=p, ids=ids)
                for i in range(n_records):
                    r.append(tuple(range(i, i + k)))
                pages = math.ceil(n_records / m)
                self.assertTrue(all(len(c.pages) == pages for c in r.columns))
                sizes = [min(m, n_records - m * q) for q in range(pages)]
                width = 16 if ids else 8
                for cols in ([3], [0, 5], list(range(k))):
                    r.clear_logs()
                    self.assertEqual(sum(1 for _ in r.scan(cols)), n_records)
                    self.assertEqual(r.pages_touched(), len(cols) * pages)
                    self.assertEqual(r.lines_touched(line),
                                     len(cols) * sum(math.ceil((4 + width * c) / line) for c in sizes))

    def test_reconstruction_touches_one_page_per_column(self):
        r = DSMTable(["int", "str", "int", "str"], page_size=128)
        for i in range(500):
            r.append((i, "v" * (i % 9), -i, str(i)))
        for i in (0, 77, 499):
            r.clear_logs()
            self.assertEqual(r.fetch(i), (i, "v" * (i % 9), -i, str(i)))
            self.assertEqual(r.pages_touched(), 4)
            r.clear_logs()
            r.fetch(i, [1, 2])
            self.assertEqual(r.pages_touched(), 2)

    def test_errors(self):
        with self.assertRaises(ValueError):
            DSMTable([])
        r = DSMTable(["str"], page_size=64)
        with self.assertRaises(ValueError):
            r.append(("x" * 60,))
        self.assertEqual(r.N, 0)
        with self.assertRaises(IndexError):
            r.fetch(0)


if __name__ == "__main__":
    unittest.main()
