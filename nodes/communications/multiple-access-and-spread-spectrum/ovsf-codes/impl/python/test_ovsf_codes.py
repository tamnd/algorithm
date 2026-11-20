# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ovsf-codes/. The authors are listed in prov/MV4CVC.jsonl.

import random

from ovsf_codes import allocate, bit_reverse, despread, is_ancestor, orthogonal, ovsf, spread, sylvester_row, valid_assignment

SFS = [1, 2, 4, 8, 16, 32]


def dot(a: list[int], b: list[int]) -> int:
    return sum(x * y for x, y in zip(a, b))


def test_check_values() -> None:
    assert ovsf(1, 0) == [1]
    assert ovsf(2, 0) == [1, 1] and ovsf(2, 1) == [1, -1]
    assert ovsf(4, 0) == [1, 1, 1, 1]
    assert ovsf(4, 1) == [1, 1, -1, -1]
    assert ovsf(4, 2) == [1, -1, 1, -1]
    assert ovsf(4, 3) == [1, -1, -1, 1]


def test_same_spreading_factor_is_orthogonal() -> None:
    for sf in SFS + [64]:
        rows = [ovsf(sf, k) for k in range(sf)]
        for i in range(sf):
            for j in range(sf):
                assert dot(rows[i], rows[j]) == (sf if i == j else 0)


def test_codes_are_bit_reversed_hadamard_rows() -> None:
    for bits in range(7):
        sf = 1 << bits
        for k in range(sf):
            assert ovsf(sf, k) == sylvester_row(sf, bit_reverse(k, bits))


def test_mixed_rates_orthogonal_iff_not_ancestor() -> None:
    rng = random.Random(1)
    for s1 in SFS:
        for s2 in SFS:
            if s1 > s2:
                continue
            for k1 in range(s1):
                short = ovsf(s1, k1)
                data = [rng.choice((-1, 1)) for _ in range(s2 // s1)]
                for k2 in range(s2):
                    out = despread(spread(data, short), ovsf(s2, k2))
                    blocks = [dot(short, ovsf(s2, k2)[i:i + s1]) for i in range(0, s2, s1)]
                    if orthogonal(s1, k1, s2, k2):
                        assert out == [0]
                        assert all(b == 0 for b in blocks)
                    else:
                        assert is_ancestor(s1, k1, s2, k2)
                        assert all(abs(b) == s1 for b in blocks)


def test_two_users_at_different_rates_separate_exactly() -> None:
    rng = random.Random(2)
    a_code, b_code = ovsf(4, 0), ovsf(8, 4)
    assert orthogonal(4, 0, 8, 4)
    a_data = [rng.choice((-1, 1)) for _ in range(40)]
    b_data = [rng.choice((-1, 1)) for _ in range(20)]
    chips = [x + 3 * y for x, y in zip(spread(a_data, a_code), spread(b_data, b_code))]
    assert despread(chips, a_code) == [4 * v for v in a_data]
    assert despread(chips, b_code) == [24 * v for v in b_data]


def test_greedy_allocation_in_order_never_blocks() -> None:
    rng = random.Random(3)
    for _ in range(300):
        reqs = []
        load = 0.0
        while True:
            sf = rng.choice([2, 4, 8, 16, 32, 64])
            if load + 1 / sf > 1:
                break
            reqs.append(sf)
            load += 1 / sf
        used: list[tuple[int, int]] = []
        for sf in sorted(reqs):
            code = allocate(used, sf)
            assert code is not None
            used.append(code)
        assert valid_assignment(used)


def test_shifted_codes_are_not_orthogonal() -> None:
    a, b = ovsf(4, 1), ovsf(4, 3)
    assert sum(a[i] * b[(i + 1) % 4] for i in range(4)) == -4
    assert despread(spread([1, -1], ovsf(2, 0)), ovsf(4, 1)) == [4]


def test_code_blocking_example() -> None:
    used = [(4, 1), (4, 2)]
    assert valid_assignment(used)
    assert allocate(used, 2) is None
    assert allocate([(4, 0), (4, 1)], 2) == (2, 1)
