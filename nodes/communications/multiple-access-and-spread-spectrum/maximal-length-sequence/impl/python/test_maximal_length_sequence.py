# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-length-sequence/. The authors are listed in prov/09SJJW.jsonl.

import random

from maximal_length_sequence import autocorrelation, is_primitive, lfsr_bits, mseq, period, periodic_xcorr, runs, to_pm

# One primitive polynomial per degree, as exponent lists.
PRIMITIVE = {
    2: [2, 1, 0],
    3: [3, 1, 0],
    4: [4, 1, 0],
    5: [5, 2, 0],
    6: [6, 1, 0],
    7: [7, 1, 0],
    8: [8, 4, 3, 2, 0],
    9: [9, 4, 0],
    10: [10, 3, 0],
}


def test_check_value_degree_three() -> None:
    s = mseq([3, 1, 0], [1, 0, 0])
    assert s == [1, 0, 0, 1, 0, 1, 1]
    assert autocorrelation(to_pm(s)) == [7, -1, -1, -1, -1, -1, -1]


def test_degree_four_sequence() -> None:
    assert "".join(map(str, mseq([4, 1, 0]))) == "100010011010111"


def test_period_balance_and_two_level_autocorrelation() -> None:
    for n, f in PRIMITIVE.items():
        s = mseq(f)
        big = (1 << n) - 1
        assert len(s) == big
        assert period(f) == big
        assert sum(s) == 1 << (n - 1)  # one more 1 than 0
        assert autocorrelation(to_pm(s)) == [big] + [-1] * (big - 1)


def test_run_property() -> None:
    for n in range(3, 11):
        r = runs(mseq(PRIMITIVE[n]))
        assert sum(r.values()) == 1 << (n - 1)
        for length in range(1, n - 1):
            # 2^(n-length-2) runs of each bit value for 1 <= length <= n-2
            assert r.get((0, length), 0) == 1 << (n - length - 2)
            assert r.get((1, length), 0) == 1 << (n - length - 2)
        assert r.get((0, n - 1), 0) == 1 and r.get((1, n), 0) == 1
        assert r.get((1, n - 1), 0) == 0 and r.get((0, n), 0) == 0


def test_every_nonzero_state_is_a_shift() -> None:
    f = PRIMITIVE[5]
    s = mseq(f)
    seen = set()
    for code in range(1, 32):
        state = [(code >> i) & 1 for i in range(5)]
        t = mseq(f, state)
        shifts = [d for d in range(31) if all(t[k] == s[(k + d) % 31] for k in range(31))]
        assert len(shifts) == 1
        seen.add(shifts[0])
    assert seen == set(range(31))


def test_shift_and_add() -> None:
    for n in (3, 4, 6):
        s = mseq(PRIMITIVE[n])
        big = len(s)
        for t in range(1, big):
            w = [s[k] ^ s[(k + t) % big] for k in range(big)]
            assert sum(1 for d in range(big) if all(w[k] == s[(k + d) % big] for k in range(big))) == 1


def test_primitive_count_by_brute_force() -> None:
    # phi(2^n - 1) / n primitive polynomials of degree n
    expected = {2: 1, 3: 2, 4: 2, 5: 6, 6: 6, 7: 18, 8: 16}
    for n, want in expected.items():
        count = 0
        for mid in range(1 << (n - 1)):
            exps = [n] + [i for i in range(1, n) if (mid >> (i - 1)) & 1] + [0]
            count += is_primitive(exps)
        assert count == want


def test_non_primitive_polynomials() -> None:
    assert period([4, 2, 0]) == 6  # (x^2 + x + 1)^2
    assert period([4, 3, 2, 1, 0]) == 5  # irreducible but not primitive
    assert not is_primitive([4, 3, 2, 1, 0])


def test_xcorr_against_direct_sum() -> None:
    rng = random.Random(7)
    a = [rng.choice((1, -1)) for _ in range(20)]
    b = [rng.choice((1, -1)) for _ in range(20)]
    for t in range(20):
        assert periodic_xcorr(a, b, t) == sum(a[k] * b[(k + t) % 20] for k in range(20))


def test_lfsr_continues_periodically() -> None:
    s = lfsr_bits([5, 2, 0], [1, 0, 0, 0, 0], 93)
    assert s[31:62] == s[:31] and s[62:93] == s[:31]
