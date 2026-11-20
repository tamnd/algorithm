# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-transferable-vote/. The authors are listed in prov/CH8C0N.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import combinations

from agtprefs import all_rankings, check_anonymity, random_profile
from single_transferable_vote import droop_quota, hare_quota, single_transferable_vote, stv_count

A, B, C, D, E = range(5)
EXAMPLE = [(A, B)] * 9 + [(B, A)] * 2 + [(C, D)] * 4 + [(D, C)] * 3 + [(E, D)] * 2


def recount_stv(profile, m, k, quota="droop"):
    """A second count: it recomputes every tally from the ballots in each round.

    It also checks that the total weight is conserved in every round. It returns the winners.
    """
    ballots = [list(r) for r in profile if len(r) > 0]
    v = len(ballots)
    q = droop_quota(v, k) if quota == "droop" else hare_quota(v, k)
    weight = [Fraction(1)] * v
    cont = set(range(m))
    winners = []
    kept = Fraction(0)

    def top(r):
        for a in r:
            if a in cont:
                return a
        return None

    while len(winners) < k and cont:
        t = {a: Fraction(0) for a in cont}
        exhausted = Fraction(0)
        for r, w in zip(ballots, weight):
            a = top(r)
            if a is None:
                exhausted += w
            else:
                t[a] += w
        assert sum(t.values()) + kept + exhausted == v
        if len(cont) <= k - len(winners):
            winners.extend(sorted(cont, key=lambda a: (-t[a], a)))
            return winners
        best = max(t.values())
        e = min(a for a in cont if t[a] == best)
        if t[e] >= q and t[e] > 0:
            f = (t[e] - q) / t[e]
            for i, r in enumerate(ballots):
                if top(r) == e:
                    weight[i] *= f
            kept += q
            cont.discard(e)
            winners.append(e)
        else:
            worst = min(t.values())
            cont.discard(max(a for a in cont if t[a] == worst))
    return winners


def irv_to_the_end(profile, m):
    """Instant runoff run until one candidate is left; elimination ties to the largest index."""
    cont = set(range(m))
    while len(cont) > 1:
        t = {a: 0 for a in cont}
        for r in profile:
            for a in r:
                if a in cont:
                    t[a] += 1
                    break
        worst = min(t.values())
        cont.discard(max(a for a in cont if t[a] == worst))
    return cont.pop()


def random_ballots(rng, m, n, truncate):
    out = []
    for r in random_profile(rng, m, n):
        if truncate:
            r = r[: rng.randint(0, m)]
        out.append(r)
    return out


def solid_coalitions(profile, m, q):
    """Yield (S, j): the ballots that rank all of S above every other candidate number at least j q."""
    for size in range(1, m + 1):
        for S in combinations(range(m), size):
            s = set(S)
            count = sum(1 for r in profile if len(r) >= size and set(r[:size]) == s)
            j = int(Fraction(count) / q)
            if j >= 1:
                yield s, j


class TestQuotas(unittest.TestCase):
    def test_droop_and_hare(self):
        self.assertEqual(droop_quota(20, 3), 6)
        self.assertEqual(droop_quota(100, 1), 51)
        self.assertEqual(droop_quota(99, 2), 34)
        self.assertEqual(hare_quota(20, 3), Fraction(20, 3))
        for v in range(1, 60):
            for k in range(1, 6):
                q = droop_quota(v, k)
                self.assertGreater((k + 1) * q, v)
                self.assertLessEqual(k * q, v + k)


class TestWorkedExample(unittest.TestCase):
    def test_rounds(self):
        winners, log = stv_count(EXAMPLE, 5, 3)
        self.assertEqual(winners, [A, D, B])
        self.assertEqual([(act, c) for act, c, _ in log], [("elect", A), ("eliminate", E), ("eliminate", C), ("fill", D), ("fill", B)])
        self.assertEqual(log[0][2], [9, 2, 4, 3, 2])
        self.assertEqual(log[1][2], [None, 5, 4, 3, 2])
        self.assertEqual(log[2][2], [None, 5, 4, 5, None])
        self.assertEqual(log[3][2], [None, 5, None, 9, None])

    def test_hare_gives_the_same_set(self):
        self.assertEqual(set(single_transferable_vote(EXAMPLE, 5, 3, "hare")), {A, B, D})

    def test_first_preferences_alone_pick_another_set(self):
        firsts = [sum(1 for r in EXAMPLE if r[0] == a) for a in range(5)]
        top3 = sorted(range(5), key=lambda a: (-firsts[a], a))[:3]
        self.assertEqual(set(top3), {A, C, D})


class TestAgainstRecount(unittest.TestCase):
    def test_random_profiles(self):
        rng = random.Random(11)
        for _ in range(600):
            m = rng.randint(1, 5)
            n = rng.randint(1, 12)
            k = rng.randint(1, m)
            prof = random_ballots(rng, m, n, rng.random() < 0.5)
            for quota in ("droop", "hare"):
                self.assertEqual(single_transferable_vote(prof, m, k, quota), recount_stv(prof, m, k, quota))

    def test_elect_entries_reach_the_quota(self):
        rng = random.Random(12)
        for _ in range(300):
            m = rng.randint(2, 5)
            n = rng.randint(2, 15)
            k = rng.randint(1, m)
            prof = random_ballots(rng, m, n, True)
            v = sum(1 for r in prof if r)
            if v == 0:
                continue
            q = droop_quota(v, k)
            winners, log = stv_count(prof, m, k)
            self.assertEqual(len(winners), k)
            self.assertEqual(len(set(winners)), k)
            for act, c, t in log:
                if act == "elect":
                    self.assertGreaterEqual(t[c], q)
                    self.assertEqual(t[c], max(x for x in t if x is not None))


class TestOneSeat(unittest.TestCase):
    def test_k1_is_instant_runoff(self):
        rng = random.Random(13)
        for _ in range(500):
            m = rng.randint(1, 5)
            n = rng.randint(1, 11)
            prof = random_ballots(rng, m, n, rng.random() < 0.5)
            if not any(prof):
                continue
            self.assertEqual(single_transferable_vote(prof, m, 1), [irv_to_the_end(prof, m)])

    def test_not_monotone(self):
        before = [(A, B, C)] * 6 + [(B, A, C)] * 2 + [(B, C, A)] * 4 + [(C, A, B)] * 5
        after = [(A, B, C)] * 8 + [(B, C, A)] * 4 + [(C, A, B)] * 5
        self.assertEqual(single_transferable_vote(before, 3, 1), [A])
        self.assertEqual(single_transferable_vote(after, 3, 1), [C])


class TestProportionality(unittest.TestCase):
    def check(self, prof, m, k, quota):
        v = sum(1 for r in prof if r)
        q = droop_quota(v, k) if quota == "droop" else hare_quota(v, k)
        W = set(single_transferable_vote(prof, m, k, quota))
        for S, j in solid_coalitions(prof, m, q):
            self.assertGreaterEqual(len(W & S), min(j, k, len(S)))

    def test_planted_coalitions(self):
        rng = random.Random(14)
        for _ in range(300):
            m = rng.randint(2, 5)
            k = rng.randint(1, m)
            size = rng.randint(1, m)
            S = rng.sample(range(m), size)
            prof = random_ballots(rng, m, rng.randint(0, 8), True)
            for _ in range(rng.randint(1, 10)):
                head = S[:]
                rng.shuffle(head)
                tail = [a for a in range(m) if a not in S]
                rng.shuffle(tail)
                prof.append(tuple(head + tail[: rng.randint(0, len(tail))]))
            rng.shuffle(prof)
            for quota in ("droop", "hare"):
                self.check(prof, m, k, quota)

    def test_all_profiles_of_four_voters(self):
        rankings = all_rankings(3)
        for p in combinations(rankings * 4, 4):
            for k in (1, 2):
                self.check(list(p), 3, k, "droop")


class TestQuotaChoice(unittest.TestCase):
    def test_droop_and_hare_differ(self):
        prof = [(0, 1, 3, 2), (0, 3, 1, 2), (1, 0, 3, 2), (2, 0, 3, 1)] + [(2, 1, 0, 3)] * 2 + [(2, 1, 3, 0)] * 2
        self.assertEqual(single_transferable_vote(prof, 4, 2), [2, 1])
        self.assertEqual(single_transferable_vote(prof, 4, 2, "hare"), [2, 0])
        self.assertEqual(single_transferable_vote(prof, 4, 1), [2])


class TestEdgeCases(unittest.TestCase):
    def test_more_seats_than_candidates(self):
        self.assertEqual(single_transferable_vote([(1, 0), (1,)], 2, 3), [1, 0])

    def test_empty_ballots_are_ignored(self):
        prof = [(), (0,), (1, 0), (1,), ()]
        self.assertEqual(single_transferable_vote(prof, 2, 1), [1])

    def test_anonymity(self):
        rng = random.Random(15)
        sample = [random_profile(rng, 4, rng.randint(2, 9)) for _ in range(200)]
        rule = lambda P, m: frozenset(single_transferable_vote(P, m, 2))
        self.assertIsNone(check_anonymity(rule, 4, None, profiles=sample))


if __name__ == "__main__":
    unittest.main()
