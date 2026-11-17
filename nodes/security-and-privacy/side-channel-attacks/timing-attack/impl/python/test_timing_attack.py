# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timing-attack/. The authors are listed in prov/M5SV5X.jsonl.

import math
import random
import statistics

import pytest
from timing_attack import (
    Montgomery,
    bits_of,
    blinded_cost,
    extra_reduction_cost,
    hamming_weight_from_total,
    modexp_montgomery_ladder,
    modexp_square_and_multiply,
    recover_exponent,
)

# A toy RSA key of 127 binary digits. Both primes are known small primes, so
# the key is reproducible; no real key is ever this small.
P = 18446744073709551557
Q = 9223372036854775783
N = P * Q
E = 65537
D = pow(E, -1, math.lcm(P - 1, Q - 1))


def test_both_exponentiations_agree_with_pow() -> None:
    rnd = random.Random(7)
    for _ in range(20):
        base = rnd.randrange(2, N)
        exponent = rnd.randrange(2, 1 << 48)
        expected = pow(base, exponent, N)
        assert modexp_square_and_multiply(base, exponent, N)[0] == expected
        assert modexp_montgomery_ladder(base, exponent, N)[0] == expected


def test_the_trace_of_square_and_multiply_gives_the_secret_exponent() -> None:
    """The attack: the per-bit work counts are the exponent in another alphabet."""
    rnd = random.Random(20251111)
    for _ in range(5):
        secret = rnd.randrange(1 << 63, 1 << 64)  # a toy private exponent
        _, trace = modexp_square_and_multiply(rnd.randrange(2, N), secret, N)
        assert recover_exponent(trace) == secret
    # The real private exponent of the toy key comes out the same way.
    _, trace = modexp_square_and_multiply(12345, D, N)
    assert recover_exponent(trace) == D
    assert len(trace.per_bit) == D.bit_length()


def test_the_total_alone_gives_only_the_hamming_weight() -> None:
    """One stopwatch reading is weaker: it counts the 1 bits, not their places."""
    _, trace = modexp_square_and_multiply(12345, D, N)
    weight = hamming_weight_from_total(trace, D.bit_length())
    assert weight == sum(bits_of(D))
    assert weight == bin(D).count("1")


def test_the_ladder_trace_is_constant_and_useless() -> None:
    """Both branches do one squaring and one multiplication, so nothing leaks."""
    rnd = random.Random(99)
    first = rnd.randrange(1 << 63, 1 << 64)
    second = (1 << 63) | ((1 << 63) - 1 - (first & ((1 << 63) - 1)))  # same length
    _, trace_one = modexp_montgomery_ladder(12345, first, N)
    _, trace_two = modexp_montgomery_ladder(12345, second, N)
    assert first != second
    assert trace_one.per_bit == trace_two.per_bit == [2] * 64
    assert trace_one.total == trace_two.total
    with pytest.raises(ValueError):
        recover_exponent(trace_one)


def test_montgomery_multiplication_is_correct() -> None:
    rnd = random.Random(11)
    engine = Montgomery(N)
    for _ in range(50):
        a, b = rnd.randrange(N), rnd.randrange(N)
        product = engine.leave(engine.mul(engine.enter(a), engine.enter(b)))
        assert product == a * b % N
    base = rnd.randrange(2, N)
    assert engine.exponentiate(base, D) == pow(base, D, N)
    assert engine.extra_reductions > 0


def test_the_extra_reduction_count_is_a_repeatable_function_of_the_ciphertext() -> None:
    """The leak Brumley and Boneh used: chosen input, stable signal."""
    first, second = 0x1234567890abcdef, 0x0fedcba098765432
    plain_one, cost_one = extra_reduction_cost(N, D, first)
    plain_two, cost_two = extra_reduction_cost(N, D, second)
    assert pow(plain_one, E, N) == first and pow(plain_two, E, N) == second
    assert cost_one != cost_two  # the work depends on the chosen input
    for _ in range(4):  # and it never changes, so an attacker can average
        assert extra_reduction_cost(N, D, first)[1] == cost_one


def test_blinding_makes_the_cost_independent_of_the_ciphertext() -> None:
    """With a fresh random blind, the same query costs a different amount."""
    rnd = random.Random(2024)
    first, second = 0x1234567890abcdef, 0x0fedcba098765432
    samples = {first: [], second: []}
    for ciphertext in samples:
        for _ in range(30):
            blind = rnd.randrange(2, N)
            plain, cost = blinded_cost(N, E, D, ciphertext, blind)
            assert pow(plain, E, N) == ciphertext  # the answer is still right
            samples[ciphertext].append(cost)
    # Repeating one query no longer repeats the measurement.
    assert len(set(samples[first])) > 1
    # And the two ciphertexts are no longer told apart by the mean cost.
    gap = abs(statistics.mean(samples[first]) - statistics.mean(samples[second]))
    spread = statistics.pstdev(samples[first] + samples[second])
    assert gap < spread


def test_nothing_in_this_module_reads_a_clock() -> None:
    """The cost model is exact counting. A wall clock would add only noise."""
    import inspect

    import timing_attack
    source = inspect.getsource(timing_attack)
    for banned in ("import time", "perf_counter", "monotonic", "timeit"):
        assert banned not in source
