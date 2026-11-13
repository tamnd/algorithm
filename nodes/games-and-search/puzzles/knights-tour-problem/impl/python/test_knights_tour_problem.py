# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knights-tour-problem/. The authors are listed in prov/C2A3S2.jsonl.

from knights_tour_problem import (count_open_tours, find_tour, is_tour, open_tour_exists_rule,
                                  schwenk_closed)

BOARDS = [(m, n) for m in range(1, 6) for n in range(m, 11) if m * n <= 30 and (m, n) != (4, 7)] + [(4, 7), (6, 6)]


def test_closed_tours_match_schwenk() -> None:
    for m, n in BOARDS:
        if m * n == 1:
            continue
        tour = find_tour(m, n, closed=True)
        assert (tour is not None) == schwenk_closed(m, n), (m, n)
        if tour is not None:
            assert is_tour(m, n, tour, closed=True)


def test_open_tours_match_rule() -> None:
    for m, n in BOARDS:
        tour = find_tour(m, n)
        assert (tour is not None) == open_tour_exists_rule(m, n), (m, n)
        if tour is not None:
            assert is_tour(m, n, tour)


def test_five_by_five() -> None:
    assert find_tour(5, 5) is not None and find_tour(5, 5, closed=True) is None
    assert count_open_tours(5, 5) == 1728


def test_odd_boards_have_no_closed_tour() -> None:
    for m, n in [(3, 3), (3, 5), (3, 7), (3, 9), (5, 5)]:
        assert find_tour(m, n, closed=True) is None


def test_validator_rejects() -> None:
    tour = find_tour(5, 6, closed=True)
    assert is_tour(5, 6, tour, closed=True)
    assert not is_tour(5, 6, tour[:-1])
    assert not is_tour(5, 6, tour[:-1] + [tour[0]])
    swapped = tour[:]
    swapped[3], swapped[4] = swapped[4], swapped[3]
    assert not is_tour(5, 6, swapped)
