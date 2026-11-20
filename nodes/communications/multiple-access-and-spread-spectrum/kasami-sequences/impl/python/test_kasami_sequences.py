# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasami-sequences/. The authors are listed in prov/H5NT6J.jsonl.

import math

from kasami_sequences import decimate, kasami_small, least_period, max_correlation, mseq, welch_sequence_bound, xcorr

PRIMITIVE = {4: [4, 1, 0], 6: [6, 1, 0], 8: [8, 4, 3, 2, 0]}


def brute_xcorr(a: list[int], b: list[int], t: int) -> int:
    n = len(a)
    return sum((1 - 2 * a[k]) * (1 - 2 * b[(k + t) % n]) for k in range(n))


def all_values(fam: list[list[int]]) -> set[int]:
    out = set()
    for i, a in enumerate(fam):
        for j, b in enumerate(fam):
            for t in range(len(a)):
                if i != j or t != 0:
                    out.add(xcorr(a, b, t))
    return out


def test_xcorr_against_plus_minus_one_sum() -> None:
    fam = kasami_small(mseq(PRIMITIVE[4]))
    for a in fam:
        for b in fam:
            for t in range(15):
                assert xcorr(a, b, t) == brute_xcorr(a, b, t)


def test_decimated_sequence_has_short_period() -> None:
    for n, f in PRIMITIVE.items():
        w = decimate(mseq(f), (1 << (n // 2)) + 1)
        assert least_period(w) == (1 << (n // 2)) - 1


def test_three_values_and_bound() -> None:
    for n in (4, 6):
        fam = kasami_small(mseq(PRIMITIVE[n]))
        half = 1 << (n // 2)
        assert len(fam) == half
        assert len({tuple(s) for s in fam}) == half
        assert all_values(fam) == {-1, -1 - half, -1 + half}
        assert max_correlation(fam) == 1 + half


def test_degree_eight_bound() -> None:
    fam = kasami_small(mseq(PRIMITIVE[8]))
    assert len(fam) == 16 and max_correlation(fam) == 17


def test_optimal_against_welch_for_binary_sequences() -> None:
    # Correlations of binary sequences of odd length are odd integers, so
    # theta_max >= the least odd integer at or above the Welch bound.
    for n in (4, 6, 8, 10, 12):
        big = (1 << n) - 1
        m = 1 << (n // 2)
        w = welch_sequence_bound(m, big)
        least_odd = math.ceil(w)
        if least_odd % 2 == 0:
            least_odd += 1
        assert least_odd == 1 + m
        assert w < 1 + m  # the bound itself is not met with equality


def test_check_values_degree_six() -> None:
    assert abs(welch_sequence_bound(8, 63) - 7.431998) < 1e-6
