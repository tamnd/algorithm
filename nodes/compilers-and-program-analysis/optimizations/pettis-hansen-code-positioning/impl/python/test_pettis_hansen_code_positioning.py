# SPDX-License-Identifier: MIT
import random
import unittest
from itertools import permutations

import toyir
from pettis_hansen_code_positioning import (
    apply_layout, best_layout, chain_blocks, closest_is_best,
    fallthrough_weight, layout,
)


def random_graph(rng, n, p):
    blocks = ["B%d" % i for i in range(n)]
    weight = {}
    for a in blocks:
        for b in blocks:
            if a != b and rng.random() < p:
                weight[(a, b)] = rng.randint(1, 9)
    return blocks, weight


def has_hamiltonian_path(nodes, arcs, start):
    """Brute force: a directed path from start through every node once."""
    rest = [v for v in nodes if v != start]
    for p in permutations(rest):
        order = [start] + list(p)
        if all((a, b) in arcs for a, b in zip(order, order[1:])):
            return True
    return False


class BlockTest(unittest.TestCase):
    def test_layout_is_a_permutation_with_entry_first(self):
        rng = random.Random(1)
        for _ in range(500):
            blocks, weight = random_graph(rng, rng.randint(1, 9), rng.random() * 0.6)
            order = layout(blocks, weight)
            self.assertEqual(order[0], blocks[0])
            self.assertEqual(sorted(order), sorted(blocks))
            for chain in chain_blocks(blocks, weight):
                for a, b in zip(chain, chain[1:]):
                    self.assertIn((a, b), weight)
                    self.assertNotEqual(b, blocks[0])

    def test_never_better_than_brute_force(self):
        rng = random.Random(2)
        trials = worse = 0
        for _ in range(600):
            blocks, weight = random_graph(rng, rng.randint(2, 7), rng.random() * 0.6)
            got = fallthrough_weight(layout(blocks, weight), weight)
            best, best_w = best_layout(blocks, weight)
            self.assertEqual(best[0], blocks[0])
            self.assertEqual(fallthrough_weight(best, weight), best_w)
            self.assertLessEqual(got, best_w)
            trials += 1
            worse += got < best_w
        # The greedy is often optimal, and sometimes not.
        self.assertGreater(worse, 0)
        self.assertGreater(trials - worse, worse)

    def test_greedy_is_not_optimal(self):
        blocks = ["E", "A", "B", "X", "D", "C"]
        weight = {("E", "A"): 19, ("A", "B"): 10, ("A", "D"): 9,
                  ("D", "C"): 9, ("C", "B"): 9, ("B", "X"): 19}
        self.assertEqual(chain_blocks(blocks, weight), [["E", "A", "B", "X"], ["D", "C"]])
        order = layout(blocks, weight)
        self.assertEqual(order, ["E", "A", "B", "X", "D", "C"])
        self.assertEqual(fallthrough_weight(order, weight), 57)
        self.assertEqual(best_layout(blocks, weight), (["E", "A", "D", "C", "B", "X"], 65))

    def test_loop_example(self):
        blocks = ["B0", "B1", "B2", "B3", "B4"]
        weight = {("B0", "B1"): 1, ("B1", "B2"): 100, ("B1", "B4"): 1,
                  ("B2", "B3"): 10, ("B2", "B1"): 90, ("B3", "B1"): 10}
        order = layout(blocks, weight)
        self.assertEqual(order, ["B0", "B1", "B2", "B3", "B4"])
        self.assertEqual(fallthrough_weight(order, weight), 111)
        self.assertEqual(best_layout(blocks, weight)[1], 111)

    def test_hamiltonian_path_reduction(self):
        # With weight 1 on every arc, the best fall-through weight is n - 1
        # exactly when a Hamiltonian path starts at the entry.
        rng = random.Random(3)
        yes = no = 0
        for _ in range(300):
            blocks, weight = random_graph(rng, rng.randint(2, 6), rng.random() * 0.7)
            unit = {e: 1 for e in weight}
            _, best_w = best_layout(blocks, unit)
            ham = has_hamiltonian_path(blocks, set(unit), blocks[0])
            self.assertEqual(best_w == len(blocks) - 1, ham)
            yes += ham
            no += not ham
        self.assertGreater(yes, 20)
        self.assertGreater(no, 20)


class ProcedureTest(unittest.TestCase):
    def test_example(self):
        procs = ["main", "parse", "lex", "eval", "print", "gc"]
        calls = {("main", "parse"): 1, ("parse", "lex"): 500, ("main", "eval"): 1,
                 ("eval", "gc"): 40, ("eval", "print"): 30, ("main", "print"): 2,
                 ("parse", "gc"): 60}
        self.assertEqual(closest_is_best(procs, calls),
                         ["main", "print", "eval", "gc", "parse", "lex"])

    def test_random_call_graphs(self):
        rng = random.Random(4)
        for _ in range(300):
            n = rng.randint(1, 8)
            procs = ["f%d" % i for i in range(n)]
            calls = {}
            for f in procs:
                for g in procs:
                    if rng.random() < 0.3:
                        calls[(f, g)] = rng.randint(1, 50)
            order = closest_is_best(procs, calls)
            self.assertEqual(sorted(order), sorted(procs))
            pair = {}
            for (f, g), c in calls.items():
                if f != g:
                    k = frozenset((f, g))
                    pair[k] = pair.get(k, 0) + c
            if pair:
                top = max(pair.values())
                heavy = [k for k, c in pair.items() if c == top]
                # The heaviest edge is merged first, from two single
                # procedures, and they stay next to each other.
                if len(heavy) == 1:
                    f, g = tuple(heavy[0])
                    self.assertEqual(abs(order.index(f) - order.index(g)), 1)


def block_trace(prog, args):
    """The blocks a run executes, by a tracing copy of the program."""
    labels = list(prog.blocks)
    k = len(labels) + 1
    blocks = {"tr.entry": toyir.Block([("const", "tr", 0)], ("jump", prog.entry))}
    for i, (lab, b) in enumerate(prog.blocks.items()):
        code = [("op", "tr", "*", "tr", k), ("op", "tr", "+", "tr", i + 1)]
        term = ("ret", "tr") if b.term[0] == "ret" else b.term
        blocks[lab] = toyir.Block(code + list(b.instrs), term)
    out = toyir.run(toyir.Program(list(prog.params), blocks), args, 100000)
    if out[0] != "ret":
        return None
    h, seq = out[1], []
    while h:
        h, d = divmod(h, k)
        seq.append(labels[d - 1])
    return seq[::-1]


class ProgramTest(unittest.TestCase):
    def test_layout_keeps_the_meaning(self):
        rng = random.Random(5)
        for _ in range(150):
            prog = toyir.random_program(rng, 4, rng.randint(1, 9), rng.random() < 0.5)
            weight = {e: 0 for e in toyir.edges(prog)}
            inputs = [[rng.randint(-3, 6), rng.randint(-3, 6)] for _ in range(6)]
            for args in inputs:
                seq = block_trace(prog, args)
                for a, b in zip(seq or [], (seq or [])[1:]):
                    weight[(a, b)] += 1
            order = layout(list(prog.blocks), weight)
            moved = apply_layout(prog, order)
            self.assertEqual(list(moved.blocks), order)
            for args in inputs:
                self.assertEqual(toyir.run(moved, args, 5000), toyir.run(prog, args, 5000))

    def test_entry_must_stay_first(self):
        prog = toyir.parse("B0:\n  jump B1\nB1:\n  ret 0\n")
        with self.assertRaises(ValueError):
            apply_layout(prog, ["B1", "B0"])


if __name__ == "__main__":
    unittest.main()
