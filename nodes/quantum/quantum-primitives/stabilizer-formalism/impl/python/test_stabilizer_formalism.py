# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stabilizer-formalism/. The authors are listed in prov/YFZYCG.jsonl.

import itertools
import math

from qsim import apply_pauli, close
from stabilizer_formalism import (anticommute, code_dimension, enumerate_stabilizer_states, is_valid_stabilizer,
                                  multiply, stabilizer_state, stabilizer_state_count, syndrome)

R = 1 / math.sqrt(2)


def test_bell_and_ghz_states() -> None:
    bell = stabilizer_state([(1, "XX"), (1, "ZZ")])
    phase = bell[0] / abs(bell[0])
    assert close([a / phase for a in bell], [R, 0, 0, R])
    singlet = stabilizer_state([(-1, "XX"), (-1, "ZZ")])
    phase = singlet[1] / abs(singlet[1])
    assert close([a / phase for a in singlet], [0, R, -R, 0])
    ghz = stabilizer_state([(1, "XXX"), (1, "ZZI"), (1, "IZZ")])
    phase = ghz[0] / abs(ghz[0])
    assert close([a / phase for a in ghz], [R, 0, 0, 0, 0, 0, 0, R])


def test_generators_fix_the_state() -> None:
    gens = [(1, "XXX"), (-1, "ZZI"), (1, "IZZ")]
    v = stabilizer_state(gens)
    for sign, word in gens:
        assert close([sign * a for a in apply_pauli(v, word)], v)
    # the product of two generators is in the group and fixes the state too
    ph, w = multiply(gens[1], gens[2])
    assert (ph, w) == (-1, "ZIZ")
    assert close([ph * a for a in apply_pauli(v, w)], v)


def test_invalid_groups() -> None:
    assert not is_valid_stabilizer([(1, "X"), (1, "Z")])  # anticommute
    assert not is_valid_stabilizer([(1, "XX"), (1, "ZZ"), (-1, "YY")])  # XX ZZ = -YY: not independent
    assert not is_valid_stabilizer([(1, "XX"), (1, "ZZ"), (1, "YY")])  # XX ZZ YY = -I
    assert multiply(multiply((1, "XX"), (1, "ZZ")), (1, "YY")) == (-1, "II")
    assert is_valid_stabilizer([(1, "XX"), (1, "ZZ")])


def test_code_dimension_is_two_to_the_n_minus_m() -> None:
    bit_flip = [(1, "IZZ"), (1, "ZZI")]
    assert code_dimension(bit_flip) == 2
    assert code_dimension([(1, "ZZI")]) == 4
    five = [(1, "XZZXI"), (1, "IXZZX"), (1, "XIXZZ"), (1, "ZXIXZ")]  # the [[5, 1, 3]] code
    assert is_valid_stabilizer(five)
    assert code_dimension(five) == 2


def test_five_qubit_code_syndromes_are_distinct() -> None:
    five = [(1, "XZZXI"), (1, "IXZZX"), (1, "XIXZZ"), (1, "ZXIXZ")]
    seen = {syndrome(five, "IIIII")}
    for q in range(5):
        for p in "XYZ":
            e = "I" * (4 - q) + p + "I" * q
            s = syndrome(five, e)
            assert s not in seen
            seen.add(s)
    assert len(seen) == 16  # 1 + 15 errors fill all 2^4 syndromes: a perfect code


def test_anticommute_counts_positions() -> None:
    for a, b in itertools.product(["X", "Y", "Z", "I"], repeat=2):
        assert anticommute(a, b) == (a != "I" and b != "I" and a != b)
    assert not anticommute("XX", "ZZ")
    assert anticommute("XI", "ZZ")


def test_number_of_stabilizer_states() -> None:
    assert [stabilizer_state_count(n) for n in (1, 2, 3)] == [6, 60, 1080]
    assert enumerate_stabilizer_states(1) == 6
    assert enumerate_stabilizer_states(2) == 60
    assert enumerate_stabilizer_states(3) == 1080
