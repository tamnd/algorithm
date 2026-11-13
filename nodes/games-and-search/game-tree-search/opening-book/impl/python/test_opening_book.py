# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/opening-book/. The authors are listed in prov/398VMX.jsonl.

import random
import unittest
from fractions import Fraction

from opening_book import (EMPTY, OpeningBook, build_book, legal_moves, noisy_game, play, solve,
                          zobrist_key, zobrist_table)


def reachable():
    seen, stack = {EMPTY}, [EMPTY]
    while stack:
        b = stack.pop()
        for m in legal_moves(b):
            c = play(b, m)
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def full_book(table, max_ply):
    book = OpeningBook(table, max_ply)
    stack = [(EMPTY, [])]
    while stack:
        b, moves = stack.pop()
        ms = legal_moves(b)
        if not ms or len(moves) == max_ply:
            book.add_line(moves, 0)
            continue
        for m in ms:
            stack.append((play(b, m), moves + [m]))
    return book


def tree_value(book, board, leaf):
    """Reference: negamax over the book moves as a tree, with no sharing."""
    es = book.probe(board) if sum(1 for p in board if p) < book.max_ply else []
    if not es:
        return leaf(board)
    return max(-tree_value(book, play(board, e.move), leaf) for e in es)


class TestOpeningBook(unittest.TestCase):
    def setUp(self):
        self.table = zobrist_table(random.Random(1970))
        self.memo = {}

    def test_keys_and_transpositions(self):
        t = self.table
        a, b = EMPTY, EMPTY
        for m in (0, 4, 8):
            a = play(a, m)
        for m in (8, 4, 0):
            b = play(b, m)
        self.assertEqual(a, b)
        self.assertEqual(zobrist_key(a, t), zobrist_key(b, t))
        positions = reachable()
        self.assertEqual(len(positions), 5478)
        self.assertEqual(len({zobrist_key(p, t) for p in positions}), 5478)  # no collision
        for p in positions:
            for m in legal_moves(p):
                side = 1 if p.count(1) == p.count(2) else 2
                self.assertEqual(zobrist_key(play(p, m), t), zobrist_key(p, t) ^ t[m][side])

    def test_full_book_is_a_dag(self):
        book = full_book(self.table, 4)
        self.assertEqual(len(book.entries), 334)  # positions with 0 to 3 pieces
        self.assertEqual(len(book.edges()), 2097)
        # As a tree, the same book would have 1 + 9 + 72 + 504 = 586 inner nodes.
        indeg = {}
        for k, mv, c in book.edges():
            indeg[c] = indeg.get(c, 0) + 1
            child = play(book.board_of[k], mv)
            self.assertEqual(zobrist_key(child, self.table), c)
            # Each arc adds one piece, so the graph has no cycle.
            self.assertEqual(sum(1 for p in child if p), sum(1 for p in book.board_of[k] if p) + 1)
        # A position whose last mover has two pieces on the board has two parents.
        self.assertEqual(max(indeg.values()), 2)
        self.assertEqual(sum(1 for v in indeg.values() if v == 2), 252 + 756)
        self.assertEqual(book.backup(lambda b: solve(b, self.memo))[0], 0)

    def test_page_example(self):
        rng = random.Random(7)
        lines = [noisy_game(rng, self.memo, 0.2) for _ in range(500)]
        res = [r for _, r in lines]
        self.assertEqual((res.count(1), res.count(2), res.count(0)), (169, 75, 256))
        book = build_book(lines, self.table, 4)
        self.assertEqual(len(book.entries), 211)
        self.assertEqual(len(book.edges()), 527)
        indeg = {}
        for _, _, c in book.edges():
            indeg[c] = indeg.get(c, 0) + 1
        self.assertEqual(sum(1 for v in indeg.values() if v >= 2), 76)
        root = {e.move: (e.games, e.points) for e in book.probe(EMPTY)}
        self.assertEqual(root[4], (52, 33))
        self.assertEqual(root[1], (66, 35))
        self.assertEqual(root[7], (59, 40))
        self.assertEqual(book.backup(lambda b: solve(b, self.memo))[0], 0)

    def test_backup_equals_tree_negamax(self):
        for seed in range(40):
            rng = random.Random(seed)
            noise = rng.choice([0.0, 0.3, 1.0])
            lines = [noisy_game(rng, self.memo, noise) for _ in range(rng.randint(1, 60))]
            book = build_book(lines, self.table, rng.randint(1, 5))
            leaf = lambda b: solve(b, self.memo)
            self.assertEqual(book.backup(leaf)[0], tree_value(book, EMPTY, leaf))

    def test_choose_follows_the_weights(self):
        rng = random.Random(7)
        book = build_book([noisy_game(rng, self.memo, 0.2) for _ in range(500)], self.table, 4)
        es = book.probe(EMPTY)
        total = sum(e.weight for e in es)
        draws = random.Random(99)
        count = {}
        for _ in range(10000):
            m = book.choose(EMPTY, draws)
            count[m] = count.get(m, 0) + 1
        for e in es:
            self.assertLess(abs(count[e.move] / 10000 - float(e.weight / total)), 0.02)
        self.assertIsNone(book.choose(play(play(play(play(EMPTY, 0), 1), 2), 3), draws))

    def test_learning(self):
        book = OpeningBook(self.table, 4)
        book.add_line([4, 0, 8, 2], 2)  # X plays 4 and 8, O wins
        book.add_line([0, 4, 8, 2], 0)
        x4 = next(e for e in book.probe(EMPTY) if e.move == 4)
        o0 = next(e for e in book.probe(play(EMPTY, 4)) if e.move == 0)
        self.assertEqual((x4.weight, o0.weight), (1, 1))
        book.learn([4, 0, 8, 2], side=1, result=2)  # X lost: its moves lose weight
        self.assertEqual((x4.weight, o0.weight), (Fraction(1, 2), 1))
        book.learn([4, 0, 8, 2], side=1, result=2)
        self.assertEqual(x4.weight, Fraction(1, 4))
        book.learn([4, 0, 8, 2], side=1, result=2)
        self.assertEqual(x4.weight, 0)  # below the floor: out of the book
        rng = random.Random(3)
        self.assertTrue(all(book.choose(EMPTY, rng) == 0 for _ in range(200)))
        book.learn([0, 4, 8, 2], side=1, result=1)
        self.assertEqual(next(e for e in book.probe(EMPTY) if e.move == 0).weight, Fraction(3, 2))
        book.learn([0, 4, 8, 2], side=1, result=0)  # a draw changes nothing
        self.assertEqual(next(e for e in book.probe(EMPTY) if e.move == 0).weight, Fraction(3, 2))


if __name__ == "__main__":
    unittest.main()
