# SPDX-License-Identifier: MIT
import random
import unittest

import toyir
from ball_larus_path_profiling import (
    ENTRY, EXIT, all_paths, cfg_to_dag, decode_history, instrument,
    number_paths, path_blocks, place_increments, regenerate,
)


def random_dag(rng, n, p):
    """A random DAG on v0 .. v(n-1): v0 reaches every node, every node
    reaches v(n-1), and parallel edges are allowed."""
    nodes = ["v%d" % i for i in range(n)]
    edges = []
    for i in range(n - 1):
        edges.append((nodes[i], nodes[rng.randrange(i + 1, n)]))
        for j in range(i + 1, n):
            if rng.random() < p:
                edges.append((nodes[i], nodes[j]))
    for j in range(1, n):
        if not any(e[1] == nodes[j] for e in edges):
            edges.append((nodes[rng.randrange(0, j)], nodes[j]))
    return nodes, edges


def path_freq(edges, paths, rng):
    """Edge frequencies from random path counts."""
    freq = [0] * len(edges)
    for p in paths:
        c = rng.choice((0, 1, 1, 2, 5, 50))
        for i in p:
            freq[i] += c
    return freq


class NumberingTest(unittest.TestCase):
    def test_bijection_and_regeneration(self):
        rng = random.Random(7)
        for _ in range(400):
            nodes, edges = random_dag(rng, rng.randint(2, 9), rng.random() * 0.6)
            s, t = nodes[0], nodes[-1]
            num, val = number_paths(nodes, edges, s, t)
            paths = all_paths(nodes, edges, s, t)
            self.assertEqual(len(paths), num[s])
            sums = sorted(sum(val[i] for i in p) for p in paths)
            self.assertEqual(sums, list(range(num[s])))
            for p in paths:
                r = sum(val[i] for i in p)
                self.assertEqual(regenerate(nodes, edges, num, val, s, t, r), p)

    def test_textbook_graph(self):
        nodes = list("ABCDEF")
        edges = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"),
                 ("C", "D"), ("D", "E"), ("D", "F"), ("E", "F")]
        num, val = number_paths(nodes, edges, "A", "F")
        self.assertEqual(num, {"A": 6, "B": 4, "C": 2, "D": 2, "E": 1, "F": 1})
        self.assertEqual(val, [0, 4, 0, 2, 0, 0, 1, 0])
        names = []
        for r in range(6):
            p = regenerate(nodes, edges, num, val, "A", "F", r)
            names.append("A" + "".join(edges[i][1] for i in p))
        self.assertEqual(names, ["ABCDEF", "ABCDF", "ABDEF", "ABDF", "ACDEF", "ACDF"])

    def test_cycle_is_rejected(self):
        with self.assertRaises(ValueError):
            number_paths(["a", "b"], [("a", "b"), ("b", "a")], "a", "b")


class PlacementTest(unittest.TestCase):
    def test_same_sums_and_code_only_on_chords(self):
        rng = random.Random(11)
        for _ in range(400):
            nodes, edges = random_dag(rng, rng.randint(2, 9), rng.random() * 0.6)
            s, t = nodes[0], nodes[-1]
            num, val = number_paths(nodes, edges, s, t)
            paths = all_paths(nodes, edges, s, t)
            freq = path_freq(edges, paths, rng)
            inc, tree = place_increments(nodes, edges, val, s, t, freq)
            # A spanning tree of V nodes has V - 1 edges, one of them t -> s.
            self.assertEqual(len(tree), len(nodes) - 2)
            for i in tree:
                self.assertEqual(inc[i], 0)
            chords = len(edges) - len(tree)
            self.assertEqual(chords, len(edges) - len(nodes) + 2)
            for p in paths:
                self.assertEqual(sum(inc[i] for i in p), sum(val[i] for i in p))

    def test_maximum_tree_has_the_lightest_chords(self):
        rng = random.Random(13)
        for _ in range(200):
            nodes, edges = random_dag(rng, rng.randint(3, 8), rng.random() * 0.6)
            s, t = nodes[0], nodes[-1]
            num, val = number_paths(nodes, edges, s, t)
            paths = all_paths(nodes, edges, s, t)
            freq = path_freq(edges, paths, rng)
            _, tree = place_increments(nodes, edges, val, s, t, freq)
            best = sum(freq[i] for i in range(len(edges)) if i not in tree)
            for _ in range(10):
                other_w = [rng.random() for _ in edges]
                inc2, tree2 = place_increments(nodes, edges, val, s, t, other_w)
                other = sum(freq[i] for i in range(len(edges)) if i not in tree2)
                self.assertLessEqual(best, other)
                for p in paths:
                    self.assertEqual(sum(inc2[i] for i in p), sum(val[i] for i in p))

    def test_textbook_graph_hot_path(self):
        nodes = list("ABCDEF")
        edges = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"),
                 ("C", "D"), ("D", "E"), ("D", "F"), ("E", "F")]
        num, val = number_paths(nodes, edges, "A", "F")
        freq = [20, 80, 10, 10, 90, 15, 85, 15]
        inc, tree = place_increments(nodes, edges, val, "A", "F", freq)
        self.assertEqual(inc, [0, 5, 1, 3, 0, 0, 0, -1])
        self.assertEqual(sorted(tree), [0, 4, 5, 6])
        cost_val = sum(f for f, v in zip(freq, val) if v)
        cost_inc = sum(f for f, k in zip(freq, inc) if k)
        self.assertEqual((cost_val, cost_inc), (175, 115))


def tracer(prog, k):
    """prog changed to return the sequence of blocks it ran, in base k."""
    index = {lab: i for i, lab in enumerate(prog.blocks)}
    blocks = {"tr.entry": toyir.Block([("const", "tr", 0)], ("jump", prog.entry))}
    for lab, b in prog.blocks.items():
        code = [("op", "tr", "*", "tr", k), ("op", "tr", "+", "tr", index[lab] + 1)]
        term = ("ret", "tr") if b.term[0] == "ret" else b.term
        blocks[lab] = toyir.Block(code + list(b.instrs), term)
    return toyir.Program(list(prog.params), blocks)


def decode_trace(h, k, labels):
    out = []
    while h:
        h, d = divmod(h, k)
        out.append(labels[d - 1])
    return out[::-1]


class ProgramTest(unittest.TestCase):
    def check(self, prog, rng):
        nodes, edges, kind, back = cfg_to_dag(prog)
        num, val = number_paths(nodes, edges, ENTRY, EXIT)
        weight = [rng.randint(1, 9) for _ in edges]
        inc, _ = place_increments(nodes, edges, val, ENTRY, EXIT, weight)
        radix = num[ENTRY] + 1
        prof = instrument(prog, nodes, edges, kind, back, inc, radix)
        k = len(prog.blocks) + 1
        trace = tracer(prog, k)
        labels = list(prog.blocks)
        checked = 0
        for _ in range(6):
            args = [rng.randint(-3, 6), rng.randint(-3, 6)]
            out = toyir.run(prog, args, 4000)
            if out == ("fuel",):
                continue
            got = toyir.run(prof, args, 100000)
            self.assertEqual(got[0], out[0])
            if out[0] != "ret":
                continue
            seen = decode_trace(toyir.run(trace, args, 100000)[1], k, labels)
            regen = []
            for r in decode_history(got[1], radix):
                p = regenerate(nodes, edges, num, val, ENTRY, EXIT, r)
                regen += path_blocks(edges, kind, p)
            self.assertEqual(regen, seen)
            checked += 1
        return checked

    def test_acyclic_programs(self):
        rng = random.Random(3)
        total = 0
        for _ in range(150):
            prog = toyir.random_program(rng, 4, rng.randint(1, 8), True)
            total += self.check(prog, rng)
        self.assertGreater(total, 300)

    def test_programs_with_loops(self):
        rng = random.Random(5)
        total = 0
        loops = 0
        for _ in range(150):
            prog = toyir.random_program(rng, 4, rng.randint(2, 8), False)
            loops += bool(cfg_to_dag(prog)[3])
            total += self.check(prog, rng)
        self.assertGreater(total, 300)
        self.assertGreater(loops, 50)


if __name__ == "__main__":
    unittest.main()
