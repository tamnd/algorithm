# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/protein-threading/. The authors are listed in prov/K6H9KW.jsonl.

import random
from fractions import Fraction

from protein_threading import all_threadings, brute_force, thread_singleton, threading_energy

ALPHABET = "HPC"


def random_case(rng: random.Random):
    m = rng.randint(1, 3)
    c = [rng.randint(1, 3) for _ in range(m)]
    gap_min = [rng.randint(0, 2) for _ in range(m - 1)]
    n = sum(c) + sum(gap_min) + rng.randint(0, 5)
    a = "".join(rng.choice(ALPHABET) for _ in range(n))
    table = {(u, x): Fraction(rng.randint(-6, 6), rng.randint(1, 3)) for u in range(sum(c)) for x in ALPHABET}
    return a, c, gap_min, (lambda u, x: table[(u, x)])


def is_valid(n, c, gap_min, t) -> bool:
    if len(t) != len(c) or t[0] < 0 or t[-1] + c[-1] > n:
        return False
    return all(t[k + 1] >= t[k] + c[k] + gap_min[k] for k in range(len(c) - 1))


def test_singleton_dp_matches_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(400):
        a, c, gap_min, single = random_case(rng)
        e, t = thread_singleton(a, c, gap_min, single)
        best, _ = brute_force(a, c, gap_min, single)
        assert e == best
        assert is_valid(len(a), c, gap_min, t)
        assert threading_energy(a, c, t, single) == e


def test_enumeration_count() -> None:
    # One segment of length c in a sequence of length n has n - c + 1 places.
    assert len(list(all_threadings(10, [3], []))) == 8
    # Two segments of length 1, no minimum gap, n = 4: the pairs s0 < s1, C(4, 2) = 6.
    assert len(list(all_threadings(4, [1, 1], [0]))) == 6
    # Every enumerated threading is valid, and no threading is listed twice.
    ts = list(all_threadings(9, [2, 1, 2], [1, 0]))
    assert len(set(ts)) == len(ts)
    assert all(is_valid(9, [2, 1, 2], [1, 0], t) for t in ts)


def test_too_short() -> None:
    single = lambda u, x: 0
    assert thread_singleton("HPH", [2, 2], [0], single) == (None, None)
    assert brute_force("HPH", [2, 2], [0], single) == (None, None)


def test_pair_terms_change_the_optimum() -> None:
    # The page example: core positions 0 and 3 are buried, positions 1 and 2 are in contact.
    a = "HHPPHPP"
    c, gap_min = [2, 2], [1]
    buried = {0, 3}
    single = lambda u, x: (-1 if x == "H" else 1) if u in buried else 0
    pair = lambda x, y: -3 if x == y == "H" else 0
    contacts = [(1, 2)]
    table = {t: (threading_energy(a, c, t, single), threading_energy(a, c, t, single, contacts, pair))
             for t in all_threadings(len(a), c, gap_min)}
    assert table == {(0, 3): (-2, -2), (0, 4): (0, -3), (0, 5): (0, 0),
                     (1, 4): (0, 0), (1, 5): (0, 0), (2, 5): (2, 2)}
    assert thread_singleton(a, c, gap_min, single) == (-2, (0, 3))
    assert brute_force(a, c, gap_min, single, contacts, pair) == (-3, (0, 4))


def test_pairwise_brute_force_is_a_lower_bound_of_dp_choice() -> None:
    # With pair terms, the singleton optimum is only a feasible threading.
    rng = random.Random(11)
    differs = 0
    for _ in range(200):
        a, c, gap_min, single = random_case(rng)
        C = sum(c)
        contacts = [(u, v) for u in range(C) for v in range(u + 1, C) if rng.random() < 0.4]
        ptab = {(x, y): Fraction(rng.randint(-6, 6), 2) for x in ALPHABET for y in ALPHABET}
        pair = lambda x, y: ptab[(x, y)]
        best, t = brute_force(a, c, gap_min, single, contacts, pair)
        _, t1 = thread_singleton(a, c, gap_min, single)
        assert threading_energy(a, c, t, single, contacts, pair) == best
        assert best <= threading_energy(a, c, t1, single, contacts, pair)
        differs += best < threading_energy(a, c, t1, single, contacts, pair)
    assert differs > 0
