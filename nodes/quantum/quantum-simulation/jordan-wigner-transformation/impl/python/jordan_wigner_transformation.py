# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jordan-wigner-transformation/. The authors are listed in prov/HV0RT2.jsonl.
"""The Jordan-Wigner transformation: fermionic operators on n modes to Pauli sums on n qubits.

Mode j is qubit j, and qubit j holds the occupation number n_j. The image of a_j is
Z_0 Z_1 ... Z_{j-1} (X_j + i Y_j) / 2, and the image of a_j^dagger is
Z_0 Z_1 ... Z_{j-1} (X_j - i Y_j) / 2. A fermionic operator is a list of
(coefficient, word) pairs, where a word is a tuple of (mode, dagger) pairs.
"""

from qsim import pauli_on, qop_add, qop_clean, qop_mul, qop_scale


def jw_ladder(n: int, j: int, is_dagger: bool) -> dict:
    """The image of a_j (is_dagger False) or a_j^dagger (is_dagger True)."""
    if not 0 <= j < n:
        raise ValueError("mode out of range")
    # the parity string on the modes below j, then (X -/+ iY)/2 on qubit j
    z = {q: "Z" for q in range(j)}  # @line L2
    x = pauli_on(n, {**z, j: "X"})
    y = pauli_on(n, {**z, j: "Y"})
    return {x: 0.5 + 0j, y: (-0.5j if is_dagger else 0.5j)}  # @line L3


def jw_word(n: int, word) -> dict:
    """The image of a product of ladder operators, by multiplying the images."""
    out = {"I" * n: 1 + 0j}
    for j, is_dagger in word:
        out = qop_mul(out, jw_ladder(n, j, is_dagger))  # @line L4
    return out


def jordan_wigner(n: int, terms: list) -> dict:
    """The image of a fermionic operator: the sum of the images of its words."""
    out: dict = {}
    for coef, word in terms:  # @line L1
        out = qop_add(out, qop_scale(jw_word(n, word), coef))  # @line L5
    out = qop_clean(out)  # @line L6
    return out  # @line L7


def no_string_ladder(n: int, j: int, is_dagger: bool) -> dict:
    """The wrong map that drops the Z string: a_j -> (X_j + i Y_j) / 2 only. Used to show the pitfall."""
    x = pauli_on(n, {j: "X"})
    y = pauli_on(n, {j: "Y"})
    return {x: 0.5 + 0j, y: (-0.5j if is_dagger else 0.5j)}


def no_string_map(n: int, terms: list) -> dict:
    out: dict = {}
    for coef, word in terms:
        w = {"I" * n: 1 + 0j}
        for j, is_dagger in word:
            w = qop_mul(w, no_string_ladder(n, j, is_dagger))
        out = qop_add(out, qop_scale(w, coef))
    return qop_clean(out)
