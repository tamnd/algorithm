# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/middle-square-method/. The authors are listed in prov/0TYC2R.jsonl.

import pytest

from middle_square_method import MiddleSquare, cycles, middle_square_step, tail_and_period


def test_knuth_example() -> None:
    # Knuth, TAOCP Vol. 2, Section 3.1: 5772156649 squared is 33317792380594909201.
    assert middle_square_step(5772156649, 10) == 7923805949


def test_four_digit_trace() -> None:
    g = MiddleSquare(5772, 4)
    assert [g.next() for _ in range(8)] == [3159, 9792, 8832, 42, 17, 2, 0, 0]
    assert tail_and_period(lambda x: middle_square_step(x, 4), 5772) == (7, 1)
    assert tail_and_period(lambda x: middle_square_step(x, 4), 2916) == (0, 4)


def test_four_digit_cycle_structure() -> None:
    f = lambda x: middle_square_step(x, 4)  # noqa: E731
    assert cycles(f, 10**4) == [
        (1, 0), (1, 100), (1, 2500), (1, 3792), (1, 7600),
        (4, 540), (4, 1600), (4, 2100)]
    longest = max(sum(tail_and_period(f, s)) for s in range(10**4))
    assert longest == 111 == sum(tail_and_period(f, 6239))


def test_metropolis_twenty_bits() -> None:
    # 13 cycles, the longest of period 142 (Metropolis, as reported by Knuth).
    f = lambda x: middle_square_step(x, 20, 2)  # noqa: E731
    cyc = cycles(f, 1 << 20)
    assert len(cyc) == 13 and max(cyc)[0] == 142


def test_small_values_decay_to_zero() -> None:
    n, b = 4, 10
    for x in range(1, b ** (n // 2)):
        y = middle_square_step(x, n, b)
        assert y < x
    # largest value and padding
    assert middle_square_step(9999, 4) == (9999 * 9999 // 100) % 10**4 == 9800


def test_bad_arguments() -> None:
    with pytest.raises(ValueError):
        middle_square_step(5, 3)
    with pytest.raises(ValueError):
        middle_square_step(10**4, 4)
    assert MiddleSquare(0, 4).next() == 0
    u = MiddleSquare(9999, 4).uniform()
    assert 0.0 <= u < 1.0
