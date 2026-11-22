# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pcfg-password-model/. The authors are listed in prov/RSR0DF.jsonl.

import itertools
import math
import random
import re
from fractions import Fraction

import pytest

from pcfg_password_model import (
    count_above,
    guess_number,
    probability,
    segment,
    strength_bits,
    train,
)

# The training lists are made up in the test, by hand or from a seeded
# generator. No real password list is used.

RUN = re.compile(r"[A-Za-z]+|[0-9]+|[^A-Za-z0-9]+")


def oracle_probability(passwords: list, w: str) -> Fraction:
    """Split with a regular expression and count again from the list."""
    def tag(x: str) -> str:
        return "L" if x[0].isalpha() else "D" if x[0].isdigit() else "S"

    def shape(x: str) -> tuple:
        return tuple((tag(r), len(r)) for r in RUN.findall(x))

    train_list = [x for x in passwords if x]
    s = shape(w)
    p = Fraction(sum(1 for x in train_list if shape(x) == s), len(train_list))
    all_runs = [r for x in train_list for r in RUN.findall(x)]
    for r in RUN.findall(w):
        same_slot = [y for y in all_runs if tag(y) == tag(r) and len(y) == len(r)]
        if not same_slot:
            return Fraction(0)
        p *= Fraction(same_slot.count(r), len(same_slot))
    return p


def made_up_list(rng: random.Random, alphabet: str, size: int, max_len: int) -> list:
    return ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, max_len))) for _ in range(size)]


PAGE_LIST = ["love12", "love12", "star12", "love!", "star99", "moon1", "love99", "sun!!"]


def test_segment() -> None:
    assert segment("love12") == [("L", "love"), ("D", "12")]
    assert segment("ab 12!x") == [("L", "ab"), ("S", " "), ("D", "12"), ("S", "!"), ("L", "x")]
    assert segment("éa") == [("S", "é"), ("L", "a")]
    assert segment("") == []


def test_page_example() -> None:
    m = train(PAGE_LIST)
    L4D2 = (("L", 4), ("D", 2))
    assert m.structures[L4D2] == Fraction(5, 8)
    assert m.runs[("L", 4)] == {"love": Fraction(4, 7), "star": Fraction(2, 7), "moon": Fraction(1, 7)}
    assert m.runs[("D", 2)] == {"12": Fraction(3, 5), "99": Fraction(2, 5)}
    assert probability(m, "love12") == Fraction(3, 14)
    assert probability(m, "moon99") == Fraction(1, 28)
    assert probability(m, "sun!!") == Fraction(1, 8)
    assert probability(m, "lovestar") == 0
    assert probability(m, "love13") == 0
    assert round(strength_bits(m, "love12"), 2) == 2.22
    assert round(strength_bits(m, "moon99"), 2) == 4.81
    got = [guess_number(m, w) for w in ["love12", "sun!!", "star99", "love!", "love1", "moon99", "moon1"]]
    assert got == [1, 3, 5, 5, 5, 9, 12]
    assert count_above(m, Fraction(1, 10**6)) == 13


def test_against_recount() -> None:
    rng = random.Random(2009)
    checked = 0
    for _ in range(150):
        alphabet = rng.choice(["ab1", "a12!", "ab1!.", "a1"])
        passwords = made_up_list(rng, alphabet, rng.randint(1, 10), 6)
        m = train(passwords)
        for _ in range(4):
            if rng.random() < 0.5:
                w = rng.choice(passwords)
            else:
                w = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 6)))
            assert probability(m, w) == oracle_probability(passwords, w)
            checked += 1
    assert checked == 600


def all_strings(alphabet: str, max_len: int) -> list:
    return ["".join(t) for n in range(1, max_len + 1) for t in itertools.product(alphabet, repeat=n)]


def test_sum_is_one_and_guess_numbers() -> None:
    """Each string with a positive probability has the length of a training
    password, so a brute force over all short strings sees all of them."""
    rng = random.Random(12)
    checked = 0
    for _ in range(40):
        alphabet = rng.choice(["a1!", "ab1", "a1"])
        passwords = made_up_list(rng, alphabet, rng.randint(1, 8), 4)
        m = train(passwords)
        universe = all_strings(alphabet, 4)
        probs = {s: probability(m, s) for s in universe}
        assert sum(probs.values(), Fraction(0)) == 1
        positive = [s for s in universe if probs[s] > 0]
        for w in rng.sample(positive, min(4, len(positive))):
            expected = 1 + sum(1 for s in positive if probs[s] > probs[w])
            assert guess_number(m, w) == expected
            checked += 1
        for t in [Fraction(1, 2), Fraction(1, 7), Fraction(1, 100)]:
            assert count_above(m, t) == sum(1 for s in positive if probs[s] > t)
    assert checked >= 100


def test_count_above_on_a_larger_model() -> None:
    """Compare the pruned count with a full product over the run lists."""
    rng = random.Random(31)
    passwords = made_up_list(rng, "abc12!", 60, 7)
    m = train(passwords)
    every = []
    for s, ps in m.structures.items():
        for combo in itertools.product(*[list(m.runs[key].values()) for key in s]):
            p = ps
            for q in combo:
                p *= q
            every.append(p)
    assert sum(every, Fraction(0)) == 1
    for t in sorted(set(every))[:: max(1, len(set(every)) // 25)]:
        assert count_above(m, t) == sum(1 for p in every if p > t)


def test_bad_input() -> None:
    m = train(["ab1", "", "cd2"])
    assert probability(m, "ab") == 0
    assert strength_bits(m, "ab") == math.inf
    with pytest.raises(ValueError):
        guess_number(m, "ab")
    with pytest.raises(ValueError):
        count_above(m, Fraction(0))
    with pytest.raises(ValueError):
        train(["", ""])
