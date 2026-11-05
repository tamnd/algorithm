# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gale-shapley/. The authors are listed in prov/9YR7J5.jsonl.

import random
import unittest

from gale_shapley import gale_shapley


def rank_tables(pp, rp):
    rp_rank = [{p: k for k, p in enumerate(lst)} for lst in rp]
    pp_rank = [{r: k for k, r in enumerate(lst)} for lst in pp]
    return pp_rank, rp_rank


def is_stable(pp, rp, partner_p):
    pp_rank, rp_rank = rank_tables(pp, rp)
    partner_r = [-1] * len(rp)
    for p, r in enumerate(partner_p):
        if r >= 0:
            if r not in pp_rank[p] or p not in rp_rank[r] or partner_r[r] >= 0:
                return False
            partner_r[r] = p
    for p in range(len(pp)):
        for r in pp[p]:
            if p not in rp_rank[r]:
                continue
            cur = partner_p[p]
            p_wants = cur < 0 or pp_rank[p][r] < pp_rank[p][cur]
            q = partner_r[r]
            r_wants = q < 0 or rp_rank[r][p] < rp_rank[r][q]
            if p_wants and r_wants:
                return False
    return True


def all_stable(pp, rp):
    """Every stable matching, by brute force over the matchings of acceptable pairs."""
    n_p, n_r = len(pp), len(rp)
    _, rp_rank = rank_tables(pp, rp)
    out = []

    def go(p, used, cur):
        if p == n_p:
            if is_stable(pp, rp, cur):
                out.append(list(cur))
            return
        cur.append(-1)
        go(p + 1, used, cur)
        cur.pop()
        for r in pp[p]:
            if not used >> r & 1 and p in rp_rank[r]:
                cur.append(r)
                go(p + 1, used | 1 << r, cur)
                cur.pop()

    go(0, 0, [])
    return out


class TestGaleShapley(unittest.TestCase):
    # Proposers A, B, C = 0, 1, 2; receivers x, y, z = 0, 1, 2.
    def test_worked_example(self):
        pp = [[0, 1, 2], [1, 0, 2], [0, 1, 2]]
        rp = [[2, 1, 0], [0, 1, 2], [0, 1, 2]]
        log = []
        res = gale_shapley(pp, rp, lambda p, r, o: log.append((p, r, o)))
        self.assertEqual(
            log,
            [
                (0, 0, "accepted"),
                (1, 1, "accepted"),
                (2, 0, "replaces 0"),
                (0, 1, "replaces 1"),
                (1, 0, "rejected"),
                (1, 2, "accepted"),
            ],
        )
        self.assertEqual(res.partner_of_proposer, [1, 2, 0])
        self.assertEqual(res.proposals, 6)
        self.assertEqual(all_stable(pp, rp), [[1, 2, 0]])

    def test_two_stable_matchings(self):
        pp = [[0, 1, 2], [1, 0, 2], [0, 1, 2]]
        rp = [[1, 0, 2], [0, 1, 2], [0, 1, 2]]
        a = gale_shapley(pp, rp)
        b = gale_shapley(rp, pp)
        self.assertEqual(a.partner_of_proposer, [0, 1, 2])
        self.assertEqual(b.partner_of_receiver, [1, 0, 2])
        self.assertEqual(sorted(all_stable(pp, rp)), [[0, 1, 2], [1, 0, 2]])

    def test_empty(self):
        res = gale_shapley([], [])
        self.assertEqual((res.partner_of_proposer, res.partner_of_receiver, res.proposals), ([], [], 0))
        res = gale_shapley([[], []], [[0]])
        self.assertEqual(res.partner_of_proposer, [-1, -1])
        self.assertEqual(res.partner_of_receiver, [-1])

    def test_no_perfect_matching(self):
        # Both proposers find only receiver 0 acceptable.
        res = gale_shapley([[0], [0]], [[1, 0], [0, 1]])
        self.assertEqual(res.partner_of_proposer, [-1, 0])
        self.assertEqual(res.partner_of_receiver, [1, -1])

    def test_unacceptable_one_way(self):
        res = gale_shapley([[0, 1]], [[], [0]])
        self.assertEqual(res.partner_of_proposer, [1])

    def test_worst_case_proposals(self):
        # Every proposer has the same list, so proposer i is rejected i times:
        # n(n + 1)/2 proposals, within the bound n^2 - n + 1.
        n = 8
        pp = [list(range(n)) for _ in range(n)]
        rp = [list(range(n)) for _ in range(n)]
        res = gale_shapley(pp, rp)
        self.assertEqual(res.partner_of_proposer, list(range(n)))
        self.assertTrue(is_stable(pp, rp, res.partner_of_proposer))
        self.assertEqual(res.proposals, n * (n + 1) // 2)
        self.assertLessEqual(res.proposals, n * n - n + 1)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            gale_shapley([[0, 0]], [[0]])
        with self.assertRaises(ValueError):
            gale_shapley([[1]], [[0]])

    def test_random_against_brute_force(self):
        rng = random.Random(1962)
        for _ in range(600):
            n_p, n_r = rng.randint(0, 5), rng.randint(0, 5)
            complete = rng.random() < 0.4
            pp = []
            for _ in range(n_p):
                lst = list(range(n_r))
                rng.shuffle(lst)
                pp.append(lst if complete else lst[: rng.randint(0, n_r)])
            rp = []
            for _ in range(n_r):
                lst = list(range(n_p))
                rng.shuffle(lst)
                rp.append(lst if complete else lst[: rng.randint(0, n_p)])
            res = gale_shapley(pp, rp)
            mp = res.partner_of_proposer
            self.assertTrue(is_stable(pp, rp, mp))
            for r, p in enumerate(res.partner_of_receiver):
                if p >= 0:
                    self.assertEqual(mp[p], r)
            stables = all_stable(pp, rp)
            self.assertIn(mp, stables)
            pp_rank, rp_rank = rank_tables(pp, rp)
            big = 10**9
            for s in stables:
                # Same set of matched agents in every stable matching.
                self.assertEqual([r >= 0 for r in s], [r >= 0 for r in mp])
                for p in range(n_p):
                    # Proposer-optimal: no stable partner is better for p.
                    a = pp_rank[p][mp[p]] if mp[p] >= 0 else big
                    b = pp_rank[p][s[p]] if s[p] >= 0 else big
                    self.assertLessEqual(a, b)
            # Receiver-pessimal.
            for s in stables:
                inv = [-1] * n_r
                for p, r in enumerate(s):
                    if r >= 0:
                        inv[r] = p
                for r in range(n_r):
                    a = rp_rank[r][res.partner_of_receiver[r]] if res.partner_of_receiver[r] >= 0 else big
                    b = rp_rank[r][inv[r]] if inv[r] >= 0 else big
                    self.assertGreaterEqual(a, b)
            self.assertLessEqual(res.proposals, sum(len(lst) for lst in pp))


if __name__ == "__main__":
    unittest.main()
