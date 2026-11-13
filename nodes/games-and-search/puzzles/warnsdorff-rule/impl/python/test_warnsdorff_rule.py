# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warnsdorff-rule/. The authors are listed in prov/6DD0YJ.jsonl.

from warnsdorff_rule import MOVES, is_tour, open_tour_from, warnsdorff


def test_every_result_is_a_valid_path() -> None:
    for n in range(1, 13):
        for r in range(n):
            for c in range(n):
                path = warnsdorff(n, n, (r, c))
                assert len(set(path)) == len(path) and path[0] == (r, c)
                assert all({abs(a[0] - b[0]), abs(a[1] - b[1])} == {1, 2} for a, b in zip(path, path[1:]))
                assert is_tour(n, n, path) == (len(path) == n * n)


def test_corner_start_succeeds_for_5_to_30() -> None:
    for n in range(5, 31):
        assert is_tour(n, n, warnsdorff(n, n, (0, 0))), n


def test_corner_tours_are_not_closed() -> None:
    for n in range(5, 31):
        path = warnsdorff(n, n, (0, 0))
        a, b = path[0], path[-1]
        assert {abs(a[0] - b[0]), abs(a[1] - b[1])} != {1, 2}, n


def test_corner_start_first_failures() -> None:
    fails = [n for n in range(5, 67) if len(warnsdorff(n, n, (0, 0))) < n * n]
    assert fails == [64, 66]


def test_success_counts_over_all_starts() -> None:
    counts = {n: sum(is_tour(n, n, warnsdorff(n, n, (r, c))) for r in range(n) for c in range(n))
              for n in range(5, 13)}
    assert counts == {5: 12, 6: 35, 7: 18, 8: 63, 9: 41, 10: 98, 11: 61, 12: 138}


def test_failures_where_a_tour_exists() -> None:
    # Warnsdorff fails from these starts, but exhaustive search finds a tour.
    for n, start in [(5, (2, 0)), (6, (3, 3)), (8, (4, 2))]:
        assert not is_tour(n, n, warnsdorff(n, n, start))
        assert is_tour(n, n, open_tour_from(n, n, start))


def test_odd_board_white_start_cannot_succeed() -> None:
    # On an odd board an open tour starts and ends on the majority colour.
    for r in range(5):
        for c in range(5):
            if (r + c) % 2 == 1:
                assert not is_tour(5, 5, warnsdorff(5, 5, (r, c)))


def test_tie_rule_matters() -> None:
    rotated = MOVES[3:] + MOVES[:3]
    assert is_tour(7, 7, warnsdorff(7, 7, (0, 0)))
    assert not is_tour(7, 7, warnsdorff(7, 7, (0, 0), rotated))
