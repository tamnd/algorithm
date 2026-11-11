# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prefix-code/. The authors are listed in prov/M6D811.jsonl.

import random
from fractions import Fraction

import pytest

from prefix_code import DecodeError, PrefixCode

COMPLETE = {"a": "0", "b": "10", "c": "110", "d": "111"}
INCOMPLETE = {"a": "0", "b": "10", "c": "110"}


def outcome(f, bits):
    try:
        return f(bits)
    except DecodeError:
        return "error"


def test_complete_code() -> None:
    code = PrefixCode(COMPLETE)
    assert code.kraft_sum() == 1 and code.is_complete()
    assert code.encode("abacd") == "0100110111"
    assert code.decode_tree("0100110111") == list("abacd")
    assert code.decode_table("0100110111") == list("abacd")
    assert code.table[0b101] == ("b", 2) and code.table[0b011] == ("a", 1)


def test_complete_code_parses_every_string_up_to_a_tail() -> None:
    # In a complete code each bit string is a sequence of codewords and then a proper prefix of a codeword.
    code = PrefixCode(COMPLETE)
    rng = random.Random(1)
    for _ in range(300):
        bits = "".join(rng.choice("01") for _ in range(rng.randint(0, 30)))
        out = outcome(code.decode_tree, bits)
        if out == "error":
            with pytest.raises(DecodeError, match="end inside"):
                code.decode_tree(bits)
        else:
            assert code.encode(out) == bits


def test_incomplete_code() -> None:
    code = PrefixCode(INCOMPLETE)
    assert code.kraft_sum() == Fraction(7, 8)
    assert not code.is_complete()
    assert code.decode_tree("0110") == ["a", "c"]
    for f in (code.decode_tree, code.decode_table):
        with pytest.raises(DecodeError, match="do not start"):
            f("111")
        with pytest.raises(DecodeError, match="end inside"):
            f("011")
    assert code.table[0b111] is None


def test_not_prefix_free_is_rejected() -> None:
    with pytest.raises(ValueError):
        PrefixCode({"a": "0", "b": "01"})
    with pytest.raises(ValueError):
        PrefixCode({"a": "01", "b": "0"})
    with pytest.raises(ValueError):
        PrefixCode({"a": "1", "b": "1"})
    with pytest.raises(ValueError):
        PrefixCode({"a": ""})


def random_prefix_code(rng: random.Random) -> dict:
    """Leaves of a random binary tree, with some leaves dropped to make incomplete codes."""
    leaves = [""]
    for _ in range(rng.randint(0, 10)):
        i = rng.randrange(len(leaves))
        w = leaves.pop(i)
        leaves += [w + "0", w + "1"]
    if len(leaves) > 1 and rng.random() < 0.5:
        leaves.pop(rng.randrange(len(leaves)))
    if leaves == [""]:
        leaves = ["0", "1"]
    return {i: w for i, w in enumerate(leaves)}


def test_round_trip_random_codes() -> None:
    rng = random.Random(2)
    for _ in range(300):
        cw = random_prefix_code(rng)
        code = PrefixCode(cw)
        assert code.kraft_sum() <= 1
        msg = [rng.randrange(len(cw)) for _ in range(rng.randint(0, 50))]
        bits = code.encode(msg)
        assert code.decode_tree(bits) == msg
        assert code.decode_table(bits) == msg


def test_tree_and_table_agree_on_any_bits() -> None:
    rng = random.Random(3)
    for _ in range(300):
        code = PrefixCode(random_prefix_code(rng))
        for _ in range(5):
            bits = "".join(rng.choice("01") for _ in range(rng.randint(0, 25)))
            assert outcome(code.decode_tree, bits) == outcome(code.decode_table, bits)


def test_single_codeword() -> None:
    code = PrefixCode({"x": "0"})
    assert code.decode_table("000") == ["x"] * 3
    assert not code.is_complete()
