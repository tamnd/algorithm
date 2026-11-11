# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forking-lemma/. The authors are listed in prov/WQ62KQ.jsonl.

import random

from forking_lemma import G, P, Q, extract_key, fork_bound, general_fork


def first_hit_algorithm(s: int):
    """A(x, h_1..h_q): J is the first index i with h_i < s, or 0. It ignores x and its coins."""

    def algo(x, answers, coins):
        for i, a in enumerate(answers, 1):
            if a < s:
                return i, a
        return 0, None

    return algo


def test_fork_meets_the_bound() -> None:
    q, h, s, trials = 8, 64, 8, 6000
    rng = random.Random(2006)
    algo = first_hit_algorithm(s)
    acc_runs = sum(algo(None, [rng.randrange(h) for _ in range(q)], 0)[0] >= 1 for _ in range(trials))
    frk_runs = sum(general_fork(algo, None, q, h, rng) is not None for _ in range(trials))
    acc_exact = 1 - (1 - s / h) ** q
    frk_exact = acc_exact * (s - 1) / h  # the fork succeeds iff the new h_J is a different value < s
    assert abs(acc_runs / trials - acc_exact) < 0.03
    assert abs(frk_runs / trials - frk_exact) < 0.015
    assert frk_exact >= fork_bound(acc_exact, q, h)
    # The bound is within a factor 1 / acc of the truth here: the 1/q loss is real.
    assert frk_exact <= fork_bound(acc_exact, q, h) / acc_exact * 1.7


def test_fork_fails_when_answers_do_not_matter() -> None:
    # If A never succeeds, neither does the fork.
    rng = random.Random(1)
    never = lambda x, answers, coins: (0, None)  # noqa: E731
    assert all(general_fork(never, None, 4, 16, rng) is None for _ in range(100))


def test_schnorr_key_extraction() -> None:
    rng = random.Random(1996)
    for x in (5, 123, 1000):
        y = pow(G, x, P)
        assert extract_key(y, q=4, rng=rng) == x


def test_fork_gives_same_commitment_and_new_challenge() -> None:
    from forking_lemma import schnorr_as_algorithm

    rng = random.Random(2000)
    y = pow(G, 77, P)
    algo = schnorr_as_algorithm(4)
    found = 0
    for _ in range(40):
        res = general_fork(algo, y, 4, Q, rng)
        if res is None:
            continue
        _, e1, (r1, m1, s1), e2, (r2, m2, s2) = res
        assert (r1, m1) == (r2, m2) and e1 != e2
        assert (s1 - s2) % Q == (e1 - e2) * 77 % Q
        found += 1
    assert found >= 5
