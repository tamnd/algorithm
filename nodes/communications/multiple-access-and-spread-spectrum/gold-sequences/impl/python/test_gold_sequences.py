# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gold-sequences/. The authors are listed in prov/BGG18W.jsonl.

from collections import Counter

from gold_sequences import (
    correlation_values,
    decimate,
    gold_family,
    gold_t,
    is_preferred_pair,
    max_correlation,
    mseq,
    shift,
    xcorr,
)


def brute_xcorr(a: list[int], b: list[int], t: int) -> int:
    pa = [1 - 2 * x for x in a]
    pb = [1 - 2 * x for x in b]
    n = len(a)
    return sum(pa[k] * pb[(k + t) % n] for k in range(n))


def test_check_value_degree_five() -> None:
    u = mseq([5, 2, 0])
    v = mseq([5, 4, 3, 2, 0])
    counts = Counter(xcorr(u, v, t) for t in range(31))
    assert counts == {-9: 6, -1: 15, 7: 10}
    assert gold_t(5) == 9
    assert is_preferred_pair(u, v, 5)


def test_xcorr_matches_plus_minus_one_sum() -> None:
    u = mseq([5, 2, 0])
    v = mseq([5, 4, 3, 2, 0])
    for t in range(31):
        assert xcorr(u, v, t) == brute_xcorr(u, v, t)


def test_second_sequence_is_a_decimation() -> None:
    u = mseq([5, 2, 0])
    assert decimate(u, 3) == mseq([5, 4, 3, 2, 0])


def test_family_size_and_bound_degree_five() -> None:
    fam = gold_family(mseq([5, 2, 0]), mseq([5, 4, 3, 2, 0]))
    assert len(fam) == 33
    assert len({tuple(s) for s in fam}) == 33
    assert max_correlation(fam) == gold_t(5)
    # every value of every correlation is -1, -t or t - 2 (except the peaks)
    allowed = {-1, -9, 7}
    for i in (0, 1, 2, 17, 32):
        for j in (0, 1, 5, 20, 31):
            for t in range(31):
                if i == j and t == 0:
                    continue
                assert xcorr(fam[i], fam[j], t) in allowed


def test_family_degree_six() -> None:
    u = mseq([6, 1, 0])
    v = mseq([6, 5, 2, 1, 0])
    assert decimate(u, 5) == v
    assert correlation_values(u, v) == {-17, -1, 15}
    fam = gold_family(u, v)
    assert len(fam) == 65 and max_correlation(fam) == 17 == gold_t(6)


def test_no_preferred_pair_for_degree_four() -> None:
    # the two primitive polynomials of degree 4 give a four-valued cross-correlation
    u = mseq([4, 1, 0])
    v = mseq([4, 3, 0])
    vals = correlation_values(u, v)
    assert vals == {-5, -1, 3, 7}
    assert not is_preferred_pair(u, v, 4)
    for q in (7,):
        assert not is_preferred_pair(u, decimate(u, q), 4)


def test_members_have_full_period_and_three_valued_autocorrelation() -> None:
    u = mseq([5, 2, 0])
    v = mseq([5, 4, 3, 2, 0])
    fam = gold_family(u, v)
    for s in fam[2:]:
        assert all(s != shift(s, t) for t in range(1, 31))
        auto = {xcorr(s, s, t) for t in range(1, 31)}
        assert auto <= {-1, -9, 7}


def test_t_values() -> None:
    assert [gold_t(n) for n in range(3, 11)] == [5, 9, 9, 17, 17, 33, 33, 65]
