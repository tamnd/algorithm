# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burst-errors/. The authors are listed in prov/0R3JDV.jsonl.

import random

from burst_errors import (
    all_binary_linear_codes, binary_image, burst_length, bursts, coset_leader_key,
    corrects_bursts, count_bursts_of_length, cyclic_burst_length, cyclic_code_rows, fire_code,
    gilbert_elliott, gilbert_elliott_error_rate, max_correctable_burst, poly_mod, poly_period,
    reduce_basis,
    rs_codewords, symbols_hit,
)


def bits(s: str) -> int:
    return sum(1 << i for i, ch in enumerate(s) if ch == "1")


def test_burst_length() -> None:
    assert burst_length(0) == 0
    assert burst_length(bits("0001000")) == 1
    assert burst_length(bits("0010110")) == 4  # first error at 2, last at 5
    assert burst_length(bits("1000001")) == 7
    assert cyclic_burst_length(bits("1000001"), 7) == 2  # wraps around the end
    for n in range(1, 11):
        for b in range(1, n + 1):
            exact = sum(1 for e in range(1, 1 << n) if burst_length(e) == b)
            assert exact == count_bursts_of_length(n, b)
            listed = list(bursts(n, b))
            assert len(listed) == len(set(listed)) == sum(1 for e in range(1, 1 << n) if burst_length(e) <= b)
            cyc = list(bursts(n, b, cyclic=True))
            assert sorted(cyc) == [e for e in range(1, 1 << n) if cyclic_burst_length(e, n) <= b]


def test_reiger_bound_exhaustive() -> None:
    # every binary linear [n, k] code with n <= 6 that corrects all bursts of length <= b has
    # n - k >= 2b, and one that detects all bursts of length <= b has n - k >= b
    tight = set()
    count = 0
    for n in range(2, 7):
        for rows in all_binary_linear_codes(n):
            count += 1
            k = len(rows)
            assert len(reduce_basis(rows)) == k
            b = max_correctable_burst(rows, n)
            assert n - k >= 2 * b
            if b and n - k == 2 * b:
                tight.add(b)
            basis = reduce_basis(rows)
            detect = 0
            while detect < n and all(coset_leader_key(basis, e) != 0 for e in bursts(n, detect + 1)):
                detect += 1
            assert n - k >= detect
    # the number of subspaces of dimension 1 .. n - 1 (Gaussian binomials), summed over n = 2 .. 6
    assert count == 3 + 14 + 65 + 372 + 2823
    assert tight == {1, 2}  # met by the repetition codes [3, 1] and [5, 1], for example
    assert max_correctable_burst([bits("111")], 3) == 1
    assert max_correctable_burst([bits("11111")], 5) == 2


def test_fire_code() -> None:
    p = 0b1011  # x^3 + x + 1
    assert poly_period(p) == 7
    g, n, k = fire_code(2, p)
    assert (n, k) == (21, 15)
    rows = cyclic_code_rows(g, n)
    # g divides x^n + 1, so the code is cyclic
    assert poly_mod(1 | (1 << n), g) == 0
    basis = reduce_basis(rows)
    assert len(basis) == k
    assert corrects_bursts(rows, n, 2)
    assert corrects_bursts(rows, n, 2, cyclic=True)
    assert not corrects_bursts(rows, n, 3)
    # n - k = 6 >= 2b = 4: the Reiger bound holds with room to spare
    # a cyclic code with n - k = 6 detects every burst of length <= 6
    assert all(coset_leader_key(basis, e) != 0 for e in bursts(n, 6, cyclic=True))


def test_reed_solomon_binary_image() -> None:
    m, prim, k = 3, 0b1011, 3
    words = rs_codewords(m, prim, k)
    n = len(words[0])
    assert (n, len(words)) == (7, 512)
    assert min(sum(1 for s in w if s) for w in words if any(w)) == n - k + 1  # d = 5, so t = 2
    images = [binary_image(w, m) for w in words]
    basis = reduce_basis(images)
    assert len(basis) == m * k
    nb = n * m
    # a bit burst of length <= m (t - 1) + 1 = 4 touches at most t = 2 symbols
    assert all(symbols_hit(e, m) <= 2 for e in bursts(nb, 4))
    assert any(symbols_hit(e, m) == 3 for e in bursts(nb, 5))
    assert corrects_bursts(basis, nb, 4)
    # the same code corrects 2 symbol errors anywhere, so any two error bits are fine as well
    singles = [1 << i for i in range(nb)]
    keys = {coset_leader_key(basis, a ^ b) for a in singles + [0] for b in singles}
    keys.add(0)
    assert len(keys) == 1 + nb + nb * (nb - 1) // 2


def test_gilbert_elliott() -> None:
    rng = random.Random(7)
    p_gb, p_bg, e_good, e_bad = 0.01, 0.1, 0.001, 0.3
    n = 200000
    errs = gilbert_elliott(n, p_gb, p_bg, e_good, e_bad, rng)
    rate = sum(errs) / n
    exact = gilbert_elliott_error_rate(p_gb, p_bg, e_good, e_bad)
    assert abs(exact - (10 / 11) * 0.001 - (1 / 11) * 0.3) < 1e-12
    assert abs(rate - exact) < 0.15 * exact
    # errors cluster: after an error, the next bit is in error far more often than on average
    pairs = sum(1 for i in range(n - 1) if errs[i] and errs[i + 1])
    assert pairs / sum(errs[:-1]) > 5 * rate
    # Gilbert's model: no errors at all in the good state
    gil = gilbert_elliott(n, p_gb, p_bg, 0.0, 0.5, random.Random(8))
    assert abs(sum(gil) / n - gilbert_elliott_error_rate(p_gb, p_bg, 0.0, 0.5)) < 0.15 * (0.5 / 11)
