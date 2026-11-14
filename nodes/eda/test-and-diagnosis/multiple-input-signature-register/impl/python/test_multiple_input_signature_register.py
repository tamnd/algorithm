# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-input-signature-register/. The authors are listed in prov/CM81DK.jsonl.

import random
from itertools import product

import pytest

from multiple_input_signature_register import MISR, signature_of

Q3 = 0b1011  # x^3 + x + 1, primitive
Q4 = 0b10011  # x^4 + x + 1, primitive
Q8 = 0x11D  # x^8 + x^4 + x^3 + x^2 + 1, primitive


def polymod(a: int, q: int) -> int:
    """Reference: remainder of a(x) by q(x) over GF(2), by long division from the top bit."""
    dq = q.bit_length() - 1
    while a and a.bit_length() - 1 >= dq:
        a ^= q << (a.bit_length() - 1 - dq)
    return a


def folded(words, seed: int) -> int:
    """The polynomial x^m s(x) + sum_t x^(m-1-t) w_t(x) of a stream of m words."""
    m = len(words)
    d = seed << m
    for t, w in enumerate(words):
        d ^= w << (m - 1 - t)
    return d


def test_page_example():
    # The example of the page: k = 3, q = x^3 + x + 1, five words, seed 0.
    words = [0b101, 0b011, 0b110, 0b001, 0b100]
    m = MISR(3, Q3)
    states = []
    for w in words:
        m.clock(w)
        states.append(m.signature())
        assert m.check_invariant()
    assert states == [0b101, 0b010, 0b010, 0b101, 0b101]
    assert m.signature() == polymod(folded(words, 0), Q3)


def test_one_stage_is_parity():
    # k = 1, q = x + 1: the register is the parity of all input bits.
    rng = random.Random(1)
    for _ in range(200):
        words = [rng.randint(0, 1) for _ in range(rng.randint(0, 20))]
        assert signature_of(1, 0b11, words) == sum(words) % 2


def test_empty_stream_keeps_seed():
    assert signature_of(4, Q4, [], seed=0b1010) == 0b1010


def test_bad_arguments():
    with pytest.raises(ValueError):
        MISR(3, 0b111)  # degree 2, not 3
    with pytest.raises(ValueError):
        MISR(3, Q3).clock(8)
    with pytest.raises(ValueError):
        MISR(3, Q3, seed=9)


@pytest.mark.parametrize("k", [1, 2, 3, 4, 5, 8, 16])
def test_signature_is_remainder(k):
    rng = random.Random(100 + k)
    for _ in range(300):
        q = (1 << k) | rng.randrange(1 << k)  # any polynomial of degree k, primitive or not
        seed = rng.randrange(1 << k)
        words = [rng.randrange(1 << k) for _ in range(rng.randint(0, 40))]
        assert signature_of(k, q, words, seed) == polymod(folded(words, seed), q)


def test_linearity():
    rng = random.Random(7)
    for _ in range(500):
        k = rng.randint(1, 8)
        q = (1 << k) | rng.randrange(1 << k)
        n = rng.randint(1, 20)
        good = [rng.randrange(1 << k) for _ in range(n)]
        err = [rng.randrange(1 << k) for _ in range(n)]
        seed = rng.randrange(1 << k)
        bad = [g ^ e for g, e in zip(good, err)]
        assert signature_of(k, q, bad, seed) == signature_of(k, q, good, seed) ^ signature_of(k, q, err)


@pytest.mark.parametrize("k,q,m", [(2, 0b111, 3), (3, Q3, 3), (3, 0b1001, 3), (2, 0b100, 4), (4, Q4, 2)])
def test_exhaustive_alias_count(k, q, m):
    # Every nonzero error stream of m words: exactly 2^(mk - k) - 1 of them alias, for every q of degree k.
    count = 0
    for err in product(range(1 << k), repeat=m):
        if any(err) and signature_of(k, q, list(err)) == 0:
            count += 1
    assert count == 2 ** (m * k - k) - 1


def test_single_bit_errors_never_alias():
    rng = random.Random(3)
    for _ in range(200):
        k = rng.randint(1, 8)
        q = (1 << k) | rng.randrange(1 << k)
        if q == 1 << k:
            continue
        m = rng.randint(1, 12)
        for t in range(m):
            for i in range(k):
                err = [0] * m
                err[t] = 1 << i
                assert signature_of(k, q, err) != 0


def test_monomial_feedback_aliases_single_bits():
    # q = x^k is a plain shift register: a bit that leaves the top stage is lost.
    err = [0b100, 0, 0]
    assert signature_of(3, 0b1000, err) == 0


def test_cancelling_pair_always_aliases():
    # An error in stage i at clock t and in stage i + 1 at clock t + 1 cancels, for every q.
    rng = random.Random(11)
    for _ in range(300):
        k = rng.randint(2, 10)
        q = (1 << k) | rng.randrange(1 << k)
        m = rng.randint(2, 15)
        t = rng.randrange(m - 1)
        i = rng.randrange(k - 1)
        err = [0] * m
        err[t] ^= 1 << i
        err[t + 1] ^= 1 << (i + 1)
        assert signature_of(k, q, err) == 0


def test_alias_rate_random_streams():
    # Equally likely nonzero error streams: the measured rate is close to (2^(mk-k) - 1)/(2^(mk) - 1), about 2^-k.
    rng = random.Random(2024)
    k, m, n = 8, 16, 40000
    hits = 0
    for _ in range(n):
        err = [rng.randrange(1 << k) for _ in range(m)]
        if not any(err):
            continue
        if signature_of(k, Q8, err) == 0:
            hits += 1
    p = 2.0 ** -k
    sigma = (p * (1 - p) / n) ** 0.5
    assert abs(hits / n - p) < 5 * sigma


def test_against_model_random_operations():
    # Long random sequences of reset and clock, against a model that keeps the folded polynomial.
    rng = random.Random(99)
    for _ in range(100):
        k = rng.randint(1, 12)
        q = (1 << k) | rng.randrange(1 << k)
        m = MISR(k, q)
        words, seed = [], 0
        for _ in range(60):
            if rng.random() < 0.1:
                seed = rng.randrange(1 << k)
                m.reset(seed)
                words = []
            else:
                w = rng.randrange(1 << k)
                m.clock(w)
                words.append(w)
            assert m.check_invariant()
            assert m.signature() == polymod(folded(words, seed), q)
