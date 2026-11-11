# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kraft-inequality/. The authors are listed in prov/AMFER4.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from kraft_inequality import is_prefix_free, kraft_sum, prefix_code_from_lengths, satisfies_kraft


def test_examples() -> None:
    assert prefix_code_from_lengths([1, 2, 3, 3]) == ["0", "10", "110", "111"]
    assert prefix_code_from_lengths([3, 1, 3, 2]) == ["110", "0", "111", "10"]
    assert prefix_code_from_lengths([2, 2, 2, 3, 3]) == ["00", "01", "10", "110", "111"]
    assert prefix_code_from_lengths([1, 2, 2], D=3) == ["0", "10", "11"]
    assert kraft_sum([1, 2, 3, 3]) == 1
    assert kraft_sum([1, 2, 3]) == Fraction(7, 8)
    assert kraft_sum([1, 1, 2]) == Fraction(5, 4)
    with pytest.raises(ValueError):
        prefix_code_from_lengths([1, 1, 2])


def test_edge_cases() -> None:
    assert prefix_code_from_lengths([]) == []
    assert prefix_code_from_lengths([0]) == [""]
    with pytest.raises(ValueError):
        prefix_code_from_lengths([0, 1])
    assert prefix_code_from_lengths([1, 1]) == ["0", "1"]


def check_code(lengths, D) -> None:
    code = prefix_code_from_lengths(lengths, D)
    assert [len(w) for w in code] == list(lengths)
    assert is_prefix_free(code)
    assert all(ch in "0123456789"[:D] for w in code for ch in w)


def test_random_feasible_vectors() -> None:
    rng = random.Random(1)
    built = 0
    for _ in range(3000):
        D = rng.choice([2, 2, 3, 4])
        lengths = [rng.randint(1, 8) for _ in range(rng.randint(1, 12))]
        if satisfies_kraft(lengths, D):
            check_code(lengths, D)
            built += 1
        else:
            with pytest.raises(ValueError):
                prefix_code_from_lengths(lengths, D)
    assert built > 500


def random_complete_lengths(rng: random.Random, D: int, splits: int) -> list[int]:
    """The leaf depths of a random full D-ary tree: the Kraft sum is exactly 1."""
    leaves = [0]
    for _ in range(splits):
        i = rng.randrange(len(leaves))
        d = leaves.pop(i)
        leaves.extend([d + 1] * D)
    return leaves


def test_boundary_sum_equal_to_one() -> None:
    rng = random.Random(2)
    for _ in range(500):
        D = rng.choice([2, 3, 5])
        lengths = random_complete_lengths(rng, D, rng.randint(0, 20))
        assert kraft_sum(lengths, D) == 1
        check_code(lengths, D)
        # One more codeword of any length breaks the inequality.
        assert not satisfies_kraft(lengths + [rng.randint(1, 30)], D)
        # Removing a codeword leaves room: the sum drops below 1.
        if len(lengths) > 1:
            assert kraft_sum(lengths[1:], D) < 1


def test_converse_against_exhaustive_search() -> None:
    # For short binary codes, a prefix code with the lengths exists exactly when the Kraft sum is at most 1.
    words = {l: ["".join(t) for t in itertools.product("01", repeat=l)] for l in range(1, 4)}
    for m in range(1, 5):
        for lengths in itertools.combinations_with_replacement(range(1, 4), m):
            exists = any(
                len(set(choice)) == m and is_prefix_free(choice)
                for choice in itertools.product(*(words[l] for l in lengths))
            )
            assert exists == satisfies_kraft(lengths)


def test_is_prefix_free() -> None:
    assert is_prefix_free(["0", "10", "11"])
    assert not is_prefix_free(["0", "01"])
    assert not is_prefix_free(["1", "1"])
    assert is_prefix_free(["10", "00", "11", "01"])
