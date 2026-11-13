# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superdense-coding/. The authors are listed in prov/4E2Q6C.jsonl.

import math
import random

from superdense_coding import decode_circuit, decode_probabilities, encode, send
from qsim import X, Z, apply_1q, eigvalsh, entropy_of, inner, kron_vec, max_abs_diff, outer, probabilities, random_state, random_unitary_1q, reduced_density

MESSAGES = [(0, 0), (0, 1), (1, 0), (1, 1)]
TOL = 1e-12


def test_every_message_is_decoded_with_probability_one() -> None:
    for x, y in MESSAGES:
        p = decode_probabilities(x, y)
        assert abs(p[(x, y)] - 1) < TOL
        assert all(abs(v) < TOL for k, v in p.items() if k != (x, y))


def test_the_four_encoded_states_are_orthonormal() -> None:
    for a in MESSAGES:
        for b in MESSAGES:
            assert abs(inner(encode(*a), encode(*b)) - (1 if a == b else 0)) < TOL


def test_one_qubit_alone_carries_no_information() -> None:
    for x, y in MESSAGES:
        s = encode(x, y)
        for keep in ([1], [0]):
            assert max_abs_diff(reduced_density(s, 2, keep), [[0.5, 0], [0, 0.5]]) < TOL


def test_sampled_messages() -> None:
    rng = random.Random(77)
    for _ in range(1000):
        x, y = rng.randrange(2), rng.randrange(2)
        assert send(x, y, rng) == (x, y)


def _holevo(states, priors):
    avg = [[sum(p * outer(s, s)[i][j] for s, p in zip(states, priors)) for j in range(len(states[0]))] for i in range(len(states[0]))]
    return entropy_of(eigvalsh(avg))  # pure states have entropy 0


def test_holevo_quantity_is_two_with_the_pair() -> None:
    assert abs(_holevo([encode(*m) for m in MESSAGES], [0.25] * 4) - 2) < 1e-9


def test_without_entanglement_success_is_at_most_one_half() -> None:
    rng = random.Random(8)
    for _ in range(200):
        start = kron_vec(random_state(1, rng), random_state(1, rng))
        encoders = [random_unitary_1q(rng) for _ in range(4)]
        success = 0.0
        for k, (x, y) in enumerate(MESSAGES):
            s = decode_circuit(apply_1q(start, encoders[k], 1))
            success += probabilities(s)[2 * x + y] / 4
        assert success <= 0.5 + 1e-9
    # The product state |00> with the protocol's own encoders reaches exactly 1/2.
    success = sum(probabilities(decode_circuit(_encode_from(x, y, [1, 0, 0, 0])))[2 * x + y] for x, y in MESSAGES) / 4
    assert abs(success - 0.5) < TOL


def _encode_from(x, y, s):
    if y:
        s = apply_1q(s, X, 1)
    if x:
        s = apply_1q(s, Z, 1)
    return s


def test_holevo_bound_one_qubit_ensembles() -> None:
    rng = random.Random(12)
    for _ in range(200):
        states = [random_state(1, rng) for _ in range(4)]
        w = [rng.random() for _ in range(4)]
        priors = [v / sum(w) for v in w]
        assert _holevo(states, priors) <= 1 + 1e-9
    assert math.isclose(_holevo([[1, 0], [0, 1]], [0.5, 0.5]), 1)
