# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniquely-decodable-code/. The authors are listed in prov/JYNM78.jsonl.

import random
from fractions import Fraction

from uniquely_decodable_code import (
    brute_force_ambiguous, is_nonsingular, is_prefix, is_uniquely_decodable, parses, sardinas_patterson,
)

# Cover and Thomas, Elements of Information Theory, 2nd ed., Section 5.1, Table 5.1 (classes of codes),
# copied by hand. The symbols are 1, 2, 3, 4.
SINGULAR = ["0", "0", "0", "0"]
NONSINGULAR_NOT_UD = ["0", "010", "01", "10"]
UD_NOT_INSTANTANEOUS = ["10", "00", "11", "110"]
INSTANTANEOUS = ["0", "10", "110", "111"]


def kraft(code) -> Fraction:
    return sum((Fraction(1, 2 ** len(w)) for w in code), Fraction(0))


def test_cover_thomas_table_classes() -> None:
    assert not is_nonsingular(SINGULAR)
    assert not is_uniquely_decodable(SINGULAR)

    assert is_nonsingular(NONSINGULAR_NOT_UD)
    ud, witness = sardinas_patterson(NONSINGULAR_NOT_UD)
    assert not ud and len(parses(witness, NONSINGULAR_NOT_UD)) == 2
    assert len(parses("010", NONSINGULAR_NOT_UD, limit=5)) == 3  # 2, then 1 4, then 3 1

    assert is_uniquely_decodable(UD_NOT_INSTANTANEOUS)
    assert not is_prefix(UD_NOT_INSTANTANEOUS)

    assert is_uniquely_decodable(INSTANTANEOUS)
    assert is_prefix(INSTANTANEOUS)


def test_other_examples() -> None:
    assert is_uniquely_decodable(["0", "01", "11"])  # a suffix code, decodable from the right
    assert not is_prefix(["0", "01", "11"])
    ud, w = sardinas_patterson(["a", "ab", "b"])
    assert not ud and len(parses(w, ["a", "ab", "b"])) == 2
    assert is_uniquely_decodable(["0", "01"])
    assert not is_uniquely_decodable(["0", "1", "01"])
    assert not is_uniquely_decodable(["", "1"])
    assert is_uniquely_decodable([])
    assert is_uniquely_decodable(["1"])


def test_dangling_suffixes_can_need_many_rounds() -> None:
    # The shortest ambiguous string of this code has 10 bits, more than twice the longest codeword.
    code = ["0", "0010", "1001"]
    ud, w = sardinas_patterson(code)
    assert not ud and w == "0010010010"
    assert brute_force_ambiguous(code, 9) is None
    assert brute_force_ambiguous(code, 10) == "0010010010"
    assert sorted(parses(w, code)) == [[0, 0, 2, 1], [1, 0, 2, 0]]


def test_random_codes_against_brute_force() -> None:
    rng = random.Random(1)
    ud_count = not_ud = 0
    for _ in range(1500):
        m = rng.randint(2, 4)
        code = ["".join(rng.choice("01") for _ in range(rng.randint(1, 4))) for _ in range(m)]
        ud, witness = sardinas_patterson(code)
        if ud:
            assert brute_force_ambiguous(code, 14) is None
            assert kraft(code) <= 1  # McMillan
            ud_count += 1
        else:
            assert witness is not None
            if is_nonsingular(code):
                assert len(parses(witness, code)) == 2
            found = brute_force_ambiguous(code, len(witness))
            assert found is not None and len(found) <= len(witness)
            not_ud += 1
    assert ud_count > 200 and not_ud > 200


def test_prefix_codes_are_ud() -> None:
    rng = random.Random(2)
    for _ in range(500):
        code = list({"".join(rng.choice("01") for _ in range(rng.randint(1, 6))) for _ in range(rng.randint(1, 6))})
        if is_prefix(code):
            assert is_uniquely_decodable(code)


def test_reversed_prefix_code_is_ud() -> None:
    rng = random.Random(3)
    for _ in range(300):
        code = list({"".join(rng.choice("01") for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(1, 6))})
        if is_prefix(code):
            assert is_uniquely_decodable([w[::-1] for w in code])
