# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hard-core-predicate/. The authors are listed in prov/1M8WNB.jsonl.

import random

from hard_core_predicate import (
    BASE,
    PRIME,
    TOY_DIGITS,
    ParityPredictor,
    blum_micali_digits,
    inner_product,
    recover_from_half_plus_predictor,
    recover_from_three_quarter_predictor,
    toy_one_way_function,
    true_accuracy,
)


def slow_inner_product(x: int, r: int, digits: int) -> int:
    """An independent oracle: add the products of the digits, modulo 2."""
    total = 0
    for index in range(digits):
        total += (x >> index & 1) * (r >> index & 1)
    return total % 2


def test_the_predicate_matches_an_independent_oracle() -> None:
    rnd = random.Random(1989)
    for _ in range(600):
        digits = rnd.randrange(1, 17)
        x = rnd.randrange(1 << digits)
        r = rnd.randrange(1 << digits)
        assert inner_product(x, r) == slow_inner_product(x, r, digits)


def test_the_predicate_is_linear_and_reads_one_digit() -> None:
    rnd = random.Random(3)
    for _ in range(100):
        x = rnd.randrange(1 << 12)
        r = rnd.randrange(1 << 12)
        s = rnd.randrange(1 << 12)
        # <x, r xor s> = <x, r> xor <x, s>, the identity the attack uses
        assert inner_product(x, r ^ s) == inner_product(x, r) ^ inner_product(x, s)
    for index in range(12):
        x = rnd.randrange(1 << 12)
        assert inner_product(x, 1 << index) == (x >> index & 1)


def test_the_toy_function_is_injective_on_its_domain() -> None:
    assert pow(BASE, PRIME - 1, PRIME) == 1
    images = {toy_one_way_function(x) for x in range(1 << TOY_DIGITS)}
    assert len(images) == 1 << TOY_DIGITS  # so a verifier can check a candidate


def test_the_predictor_is_deterministic_and_has_the_stated_density() -> None:
    predictor = ParityPredictor(secret=339, accuracy=0.80)
    first = [predictor(r) for r in range(50)]
    second = [predictor(r) for r in range(50)]
    assert first == second  # a fixed error pattern, not a fresh coin per call
    assert 0.76 < true_accuracy(predictor, TOY_DIGITS) < 0.86


def test_the_three_quarter_decoder_finds_every_digit() -> None:
    """The easy half of the Goldreich-Levin theorem, as a program."""
    rnd = random.Random(1989)
    secret = rnd.randrange(1 << TOY_DIGITS)
    assert secret == 339
    predictor = ParityPredictor(secret=secret, accuracy=0.80)
    assert round(true_accuracy(predictor, TOY_DIGITS), 6) == round(842 / 1024, 6)
    recovered = recover_from_three_quarter_predictor(
        predictor, TOY_DIGITS, rnd, trials=200
    )
    assert recovered == secret
    assert predictor.queries == 2 * TOY_DIGITS * 200 == 4000


def test_the_three_quarter_decoder_works_for_many_secrets() -> None:
    rnd = random.Random(11)
    for trial in range(40):
        secret = rnd.randrange(1 << TOY_DIGITS)
        predictor = ParityPredictor(
            secret=secret, accuracy=0.85, seed=b"many-%d" % trial
        )
        recovered = recover_from_three_quarter_predictor(
            predictor, TOY_DIGITS, rnd, trials=80
        )
        assert recovered == secret
        assert toy_one_way_function(recovered) == toy_one_way_function(secret)


def test_a_predictor_at_one_half_gives_nothing() -> None:
    """A coin flip is not a predictor, and the decoder must fail on it."""
    rnd = random.Random(7)
    secret = rnd.randrange(1 << TOY_DIGITS)
    predictor = ParityPredictor(secret=secret, accuracy=0.5, seed=b"coin")
    recovered = recover_from_three_quarter_predictor(
        predictor, TOY_DIGITS, rnd, trials=200
    )
    assert recovered != secret


def test_the_full_decoder_at_sixty_percent() -> None:
    """The real theorem: 1/2 + epsilon is enough, with pairwise independence."""
    rnd = random.Random(2024)
    secret = rnd.randrange(1 << TOY_DIGITS)
    image = toy_one_way_function(secret)
    predictor = ParityPredictor(secret=secret, accuracy=0.60, seed=b"v60")
    assert 0.55 < true_accuracy(predictor, TOY_DIGITS) < 0.68
    candidates = recover_from_half_plus_predictor(
        predictor,
        TOY_DIGITS,
        rnd,
        seeds=8,
        verifier=lambda guess: toy_one_way_function(guess) == image,
    )
    assert secret in candidates
    # The predictor is asked only about the 2^8 - 1 combined strings.
    assert predictor.queries == (2**8 - 1) * TOY_DIGITS == 2550


def test_the_full_decoder_at_fifty_eight_percent() -> None:
    rnd = random.Random(7)
    secret = rnd.randrange(1 << TOY_DIGITS)
    image = toy_one_way_function(secret)
    predictor = ParityPredictor(secret=secret, accuracy=0.58, seed=b"s9")
    candidates = recover_from_half_plus_predictor(
        predictor,
        TOY_DIGITS,
        rnd,
        seeds=9,
        verifier=lambda guess: toy_one_way_function(guess) == image,
    )
    assert secret in candidates
    assert predictor.queries == (2**9 - 1) * TOY_DIGITS == 5110


def test_the_full_decoder_returns_a_short_list_without_a_verifier() -> None:
    rnd = random.Random(5)
    predictor = ParityPredictor(secret=123, accuracy=0.65, seed=b"list")
    candidates = recover_from_half_plus_predictor(predictor, TOY_DIGITS, rnd, seeds=6)
    assert len(candidates) == 2**6  # one candidate per guess of the seed digits
    assert 123 in candidates


def test_the_blum_micali_chain_is_reproducible() -> None:
    digits = blum_micali_digits(3, 16)
    assert digits == [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
    assert all(digit in (0, 1) for digit in digits)
