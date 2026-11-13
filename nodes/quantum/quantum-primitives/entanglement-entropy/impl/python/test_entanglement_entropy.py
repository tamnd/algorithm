# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/entanglement-entropy/. The authors are listed in prov/VEC71F.jsonl.

import math
import random

from entanglement_entropy import entanglement_entropy, renyi2_entropy, schmidt_coefficients, schmidt_rank
from qsim import apply_1q, kron_vec, random_state, random_unitary_1q

TOL = 1e-9


def h2(p):
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def test_bell_product_ghz_and_w() -> None:
    bell = [2 ** -0.5, 0, 0, 2 ** -0.5]
    assert abs(entanglement_entropy(bell, 2, [1]) - 1) < TOL
    assert abs(entanglement_entropy(kron_vec([0.6, 0.8], [1, 0]), 2, [1])) < TOL
    ghz = [0] * 8
    ghz[0] = ghz[7] = 2 ** -0.5
    for part in ([0], [1], [2], [0, 1], [1, 2]):
        assert abs(entanglement_entropy(ghz, 3, part) - 1) < TOL
    w = [0] * 8
    w[1] = w[2] = w[4] = 3 ** -0.5
    assert abs(entanglement_entropy(w, 3, [0]) - (math.log2(3) - 2 / 3)) < TOL
    assert abs(entanglement_entropy(w, 3, [0]) - h2(1 / 3)) < TOL


def test_two_qubit_family() -> None:
    for t in (0.1, math.pi / 8, 0.5, math.pi / 4):
        s = [math.cos(t), 0, 0, math.sin(t)]
        assert abs(entanglement_entropy(s, 2, [0]) - h2(math.cos(t) ** 2)) < TOL
    assert schmidt_rank([1, 0, 0, 0], 2, [0]) == 1


def test_both_sides_agree_and_the_bound_holds() -> None:
    rng = random.Random(21)
    for _ in range(8):
        psi = random_state(4, rng)
        for a in ([0], [3], [0, 1], [1, 3], [0, 2, 3]):
            b = [q for q in range(4) if q not in a]
            sa, sb = entanglement_entropy(psi, 4, a), entanglement_entropy(psi, 4, b)
            assert abs(sa - sb) < TOL
            assert -TOL <= sa <= min(len(a), len(b)) + TOL
            assert renyi2_entropy(psi, 4, a) <= sa + TOL
            c = schmidt_coefficients(psi, 4, a)
            assert abs(sum(x * x for x in c) - 1) < TOL


def test_local_unitaries_do_not_change_it_and_pairs_add() -> None:
    rng = random.Random(22)
    psi = random_state(3, rng)
    before = entanglement_entropy(psi, 3, [2])
    for q in range(3):
        psi = apply_1q(psi, random_unitary_1q(rng), q)
    assert abs(entanglement_entropy(psi, 3, [2]) - before) < TOL
    bell = [2 ** -0.5, 0, 0, 2 ** -0.5]
    two_pairs = kron_vec(bell, bell)  # pairs (3, 2) and (1, 0)
    assert abs(entanglement_entropy(two_pairs, 4, [3, 1]) - 2) < TOL
    assert abs(entanglement_entropy(two_pairs, 4, [3, 2])) < TOL


def test_random_states_are_close_to_maximal() -> None:
    # Page's formula for a 3 | 3 qubit cut: sum_(k=9)^(64) 1/k - 7/16 nats, about 2.292 bits.
    page = (sum(1 / k for k in range(9, 65)) - 7 / 16) / math.log(2)
    rng = random.Random(4)
    values = [entanglement_entropy(random_state(6, rng), 6, [3, 4, 5]) for _ in range(40)]
    mean = sum(values) / len(values)
    # The standard error of the mean is about 0.015 bits for 40 samples; allow four of them.
    assert abs(mean - page) < 0.06
    assert max(values) < 3
