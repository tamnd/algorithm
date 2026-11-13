# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/endgame-tablebase/. The authors are listed in prov/Q9YYTV.jsonl.

import unittest
from collections import Counter

from endgame_tablebase import (CLASSES, SIZE, SYM, all_positions, build, canonical, decode, encode,
                               index, king_pair_classes, mated, mirror_only, moves, probe, symmetries,
                               unmoves)


def forward_solve(ps, frozen=False):
    """Reference on the full position set, with no symmetry: W_n and L_n
    computed forward from the moves until they stop growing. Positions in
    neither set are draws (a capture of the rook, a stalemate, or play that
    can go on for ever)."""
    kids = {p: moves(p, frozen) for p in ps}
    win, loss = {}, {p: 0 for p in ps if mated(p)}
    n = 0
    while True:
        n += 1
        nw = [p for p in ps if p not in win and any(c is not None and c in loss for c in kids[p])]
        nl = [p for p in ps if p not in loss and kids[p] and all(c is not None and c in win for c in kids[p])]
        if not nw and not nl:
            return {p: ((1, win[p]) if p in win else (-1, loss[p]) if p in loss else (0, None)) for p in ps}
        for p in nw:
            win[p] = n
        for p in nl:
            loss[p] = n


class TestEndgameTablebase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = build()
        cls.ps = all_positions()

    def test_king_placements(self):
        self.assertEqual(len(CLASSES), 21)  # 4 by 4, 8 symmetries
        self.assertEqual(len(king_pair_classes(4, mirror_only(4))), 78)
        self.assertEqual(len(king_pair_classes(8, symmetries(8))), 462)  # pawnless chess
        self.assertEqual(len(king_pair_classes(8, mirror_only(8))), 1806)  # with pawns

    def test_sizes(self):
        self.assertEqual(len(self.ps), 3496)
        self.assertEqual(SIZE, 672)  # versus 16 * 16 * 16 * 2 = 8192 with no index function
        self.assertEqual(len(self.table), 672)
        used = sum(1 for b in self.table if b)
        self.assertEqual(used, 443)
        self.assertEqual(len({index(p) for p in self.ps}), 443)
        self.assertEqual(Counter(decode(b)[0] for b in self.table if b), {1: 167, -1: 198, 0: 78})

    def test_probe_equals_forward_solve(self):
        want = forward_solve(self.ps)
        for p in self.ps:
            self.assertEqual(probe(self.table, p), want[p])

    def test_draws_by_endless_play(self):
        # The variant in which the white king may not move. A draw with White
        # to move has no move out of the set (White never captures), so neither
        # side can force a mate and the play can go on for ever.
        table = build(frozen=True)
        want = forward_solve(self.ps, frozen=True)
        for p in self.ps:
            self.assertEqual(probe(table, p), want[p])
        got = Counter((p[3], probe(table, p)[0]) for p in self.ps)
        self.assertEqual(got, {(0, 1): 368, (0, 0): 944, (1, -1): 404, (1, 0): 1780})
        for p in self.ps:
            if p[3] == 0 and probe(table, p)[0] == 0:
                self.assertTrue(moves(p, True) and None not in moves(p, True))

    def test_symmetric_positions_agree(self):
        for p in self.ps:
            wk, wr, bk, stm = p
            for g in SYM:
                q = (g(wk), g(wr), g(bk), stm)
                self.assertEqual(index(q), index(p))
                self.assertEqual(probe(self.table, q), probe(self.table, p))

    def test_unmoves_and_encoding(self):
        s = set(self.ps)
        for p in self.ps:
            for q in moves(p):
                if q is not None:
                    self.assertIn(q, s)
                    self.assertIn(p, unmoves(q))
            self.assertEqual(canonical(canonical(p)), canonical(p))
        for v, d in ((0, None), (1, 1), (1, 13), (-1, 0), (-1, 14)):
            self.assertEqual(decode(encode(v, d)), (v, d))

    def test_distances_are_exact(self):
        for p in self.ps:
            v, d = probe(self.table, p)
            kids = [probe(self.table, c) for c in moves(p) if c is not None]
            if v == 1:
                self.assertEqual(min(dc for vc, dc in kids if vc == -1), d - 1)
            elif v == -1 and d > 0:
                self.assertTrue(all(vc == 1 for vc, _ in kids) and len(kids) == len(moves(p)))
                self.assertEqual(max(dc for _, dc in kids), d - 1)


if __name__ == "__main__":
    unittest.main()
