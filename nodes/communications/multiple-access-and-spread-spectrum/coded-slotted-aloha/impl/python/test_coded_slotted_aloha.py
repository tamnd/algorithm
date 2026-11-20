# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coded-slotted-aloha/. The authors are listed in prov/KAWTQF.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from cbb import wilson
from coded_slotted_aloha import (
    de_converges,
    decode,
    load_bound,
    rate,
    threshold,
    transmit,
    unresolved_brute_force,
)

CRDSA = {2: 1.0}
REG3 = {3: 1.0}
LIVA_LAMBDA3 = {2: 0.5, 3: 0.28, 8: 0.22}  # Liva 2011, Section IV-B
PAOLINI_R13 = {2: 0.554016, 3: 0.261312, 6: 0.184672}  # Paolini, Liva and Chiani 2015, Table I


def random_dist(rng, m):
    degrees = sorted(rng.sample(range(1, min(m, 4) + 1), rng.randint(1, min(m, 4))))
    w = [rng.random() + 0.05 for _ in degrees]
    s = sum(w)
    return {d: x / s for d, x in zip(degrees, w)}


def test_decode_matches_largest_stopping_set():
    rng = random.Random(11)
    for _ in range(150):
        m = rng.randint(1, 8)
        k = rng.randint(0, 9)
        frame = transmit(rng, k, m, random_dist(rng, m))
        got = decode(frame, m)
        assert len(got) == len(set(got))
        assert set(got) == set(range(k)) - unresolved_brute_force(frame, m)


def test_resolved_set_does_not_depend_on_order():
    rng = random.Random(12)
    for _ in range(60):
        m = rng.randint(2, 30)
        k = rng.randint(1, 40)
        frame = transmit(rng, k, m, random_dist(rng, m))
        ref = set(decode(frame, m))
        for seed in range(4):
            assert set(decode(frame, m, random.Random(seed))) == ref


def test_decoding_order_is_valid():
    # Each resolved user must have a slot that is clean once the earlier users are cancelled.
    rng = random.Random(13)
    for _ in range(60):
        m = rng.randint(2, 20)
        k = rng.randint(1, 25)
        frame = transmit(rng, k, m, random_dist(rng, m))
        done = set()
        for u in decode(frame, m):
            assert any(
                all(v == u or v in done for v in range(k) if s in frame[v]) for s in frame[u]
            )
            done.add(u)


def test_hand_example():
    # Four users, four slots: users 0 and 1 collide in both their slots (a stopping set).
    frame = [[0, 1], [0, 1], [1, 2], [2, 3]]
    assert decode(frame, 4) == [3, 2]
    assert unresolved_brute_force(frame, 4) == {0, 1}
    # Peeling chain: slot 0 holds only user 0; cancelling it cleans slot 1 for user 1, and so on.
    frame = [[0, 1], [1, 2], [2, 3], [3]]
    assert decode(frame, 4) == [0, 1, 2, 3]


def test_page_example():
    # The example of the page: M = 6, K = 6; users 4 and 5 form a stopping set.
    frame = [[0, 1], [1, 2], [2, 3], [3], [4, 5], [4, 5]]
    assert decode(frame, 6) == [0, 1, 2, 3]
    assert unresolved_brute_force(frame, 6) == {4, 5}
    # Without cancellation only slot 0 is clean.
    clean = [s for s in range(6) if sum(s in f for f in frame) == 1]
    assert clean == [0]


def test_slotted_aloha_degree_one_closed_form():
    # Degree 1 is slotted ALOHA: a user succeeds iff no other user picks its slot,
    # with probability (1 - 1/M)^(K - 1). n = 30000 user trials, about 11000 failures expected.
    rng = random.Random(14)
    k, m, frames = 10, 20, 3000
    ok = sum(len(decode(transmit(rng, k, m, {1: 1.0}), m)) for _ in range(frames))
    lo, hi = wilson(ok, k * frames)
    assert lo <= (1 - 1 / m) ** (k - 1) <= hi


def test_loss_rate_matches_exact_enumeration():
    # K = 3 users of degree 2 in M = 4 slots: enumerate all 6^3 frames with the brute-force
    # stopping set, then simulate n = 3 * 20000 user trials and check the Wilson interval.
    k, m = 3, 4
    pairs = list(itertools.combinations(range(m), 2))
    lost = sum(len(unresolved_brute_force([list(p) for p in f], m)) for f in itertools.product(pairs, repeat=k))
    exact = Fraction(lost, k * len(pairs) ** k)
    rng = random.Random(15)
    frames = 20000
    sim = sum(k - len(decode(transmit(rng, k, m, CRDSA), m)) for _ in range(frames))
    lo, hi = wilson(sim, k * frames)
    assert sim >= 100
    assert lo <= float(exact) <= hi


@pytest.mark.parametrize(
    "dist, expected, tol",
    [
        (CRDSA, 0.5, 1e-3),  # Liva 2011: CRDSA threshold 0.5
        (LIVA_LAMBDA3, 0.938, 1e-3),  # Liva 2011, Section IV-B
        (PAOLINI_R13, 0.8792, 1e-3),  # Paolini et al. 2015, Table I, R = 1/3
        ({4: 1.0}, 0.772, 1e-3),  # Liva 2011, 4-regular
    ],
)
def test_density_evolution_thresholds(dist, expected, tol):
    g = threshold(dist, tol=1e-4)
    assert abs(g - expected) < tol
    assert g <= load_bound(rate(dist)) + 1e-9
    if 2 in dist:
        assert g <= 1 / (2 * dist[2]) + 1e-3  # stability bound


def test_regular_three_threshold_and_bound():
    g = threshold(REG3, tol=1e-4)
    assert 0.817 < g < 0.820
    assert de_converges(REG3, 0.80)
    assert not de_converges(REG3, 0.83)


@pytest.mark.parametrize(
    "r, expected",
    [(1 / 3, 0.9405), (2 / 5, 0.8926), (1 / 2, 0.7968), (3 / 5, 0.6758)],
)
def test_load_bound_values(r, expected):
    # Paolini et al. 2015, Theorem 4.1 and Table I
    assert abs(load_bound(r) - expected) < 1e-4


def test_finite_frame_below_threshold():
    # Liva's distribution at G = 0.5 with M = 200 slots: almost every packet is resolved.
    rng = random.Random(16)
    m, k, frames = 200, 100, 30
    lost = sum(k - len(decode(transmit(rng, k, m, LIVA_LAMBDA3), m)) for _ in range(frames))
    assert lost / (k * frames) < 0.02


def test_input_checks():
    with pytest.raises(ValueError):
        decode([[1, 1]], 3)
    with pytest.raises(ValueError):
        transmit(random.Random(0), 2, 3, {4: 1.0})
    with pytest.raises(ValueError):
        load_bound(1.0)
