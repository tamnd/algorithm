# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-state-sequence-estimation/. The authors are listed in prov/J2DFVA.jsonl.

import itertools
import math
import random

import pytest

from reduced_state_sequence_estimation import check_partitions, ddfse_partitions, number_of_states, rsse


def cn(rng, var):
    s = math.sqrt(var / 2)
    return complex(rng.gauss(0, s), rng.gauss(0, s))


def channel_out(f, x, pre):
    mem = len(f) - 1
    full = list(pre) + list(x)
    return [sum(f[l] * full[mem + k - l] for l in range(len(f))) for k in range(len(x))]


def metric(y, f, x, pre):
    return sum(abs(a - b) ** 2 for a, b in zip(y, channel_out(f, x, pre)))


def brute_force(y, f, alphabet, pre):
    return min((list(c) for c in itertools.product(alphabet, repeat=len(y))), key=lambda c: metric(y, f, c, pre))


def dfe(y, f, alphabet, pre):
    past, out = list(pre), []
    for v in y:
        isi = sum(f[l] * past[-l] for l in range(1, len(f)))
        a = min(alphabet, key=lambda p: abs(v - isi - f[0] * p))
        out.append(a)
        past.append(a)
    return out


def test_example_on_the_page() -> None:
    f, y = [1, 0.6, 0.3], [1.4, 0.8, 1.8, 1.4, 0.0]
    assert rsse(y, f, [1, -1], ddfse_partitions(2, 1), pre=[1, 1]) == [1, 1, 1, 1, -1]
    assert rsse(y, f, [1, -1], ddfse_partitions(2, 2), pre=[1, 1]) == [1, 1, 1, 1, -1]
    assert rsse(y, f, [1, -1], [], pre=[1, 1]) == [1, -1, 1, 1, -1]
    assert abs(metric(y, f, [1, 1, 1, 1, -1], [1, 1]) - 1.73) < 1e-12


def test_full_partitions_are_exact_ml() -> None:
    rng = random.Random(7701)
    for _ in range(12):
        f = [rng.gauss(0, 1) for _ in range(rng.randint(1, 4))]
        pre = [rng.choice((-1, 1)) for _ in range(len(f) - 1)]
        x = [rng.choice((-1, 1)) for _ in range(10)]
        y = [v + rng.gauss(0, 0.8) for v in channel_out(f, x, pre)]
        assert rsse(y, f, [1, -1], ddfse_partitions(2, len(f) - 1), pre=pre) == brute_force(y, f, [1, -1], pre)
    qpsk = [complex(a, b) for a in (-1, 1) for b in (-1, 1)]
    for _ in range(6):
        f = [cn(rng, 1.0) for _ in range(3)]
        pre = [rng.choice(qpsk) for _ in range(2)]
        x = [rng.choice(qpsk) for _ in range(5)]
        y = [v + cn(rng, 1.0) for v in channel_out(f, x, pre)]
        assert rsse(y, f, qpsk, ddfse_partitions(4, 2), pre=pre) == brute_force(y, f, qpsk, pre)


def test_no_partition_is_the_dfe() -> None:
    rng = random.Random(7702)
    pam = [3, 1, -1, -3]
    for _ in range(20):
        f = [1.0] + [rng.uniform(-0.6, 0.6) for _ in range(rng.randint(0, 3))]
        pre = [rng.choice(pam) for _ in range(len(f) - 1)]
        x = [rng.choice(pam) for _ in range(40)]
        y = [v + rng.gauss(0, 0.6) for v in channel_out(f, x, pre)]
        assert rsse(y, f, pam, [], pre=pre) == dfe(y, f, pam, pre)


def test_ddfse_agrees_with_ml_on_most_blocks_at_high_snr() -> None:
    # 200 blocks of 50 BPSK symbols on f = (1, 0.6, 0.3), sigma = 0.35, seed 7703:
    # DDFSE with 2 states agrees with 4-state ML on 198 blocks, the DFE on 184
    rng = random.Random(7703)
    f = [1, 0.6, 0.3]
    agree_ddfse = agree_dfe = 0
    for _ in range(200):
        x = [rng.choice((1, -1)) for _ in range(50)]
        y = [v + rng.gauss(0, 0.35) for v in channel_out(f, x, [1, 1])]
        ml = rsse(y, f, [1, -1], ddfse_partitions(2, 2), pre=[1, 1])
        agree_ddfse += rsse(y, f, [1, -1], ddfse_partitions(2, 1), pre=[1, 1]) == ml
        agree_dfe += rsse(y, f, [1, -1], [], pre=[1, 1]) == ml
    assert agree_ddfse == 198 and agree_dfe == 184


def test_set_partition_beats_a_bad_partition_on_4pam() -> None:
    # 2 states on 4-PAM, f = (1, 0.7), sigma = 0.35, seed 7704, 200 blocks of 40 symbols:
    # the partition {3, -1} {1, -3} agrees with ML on all 200, {3, 1} {-1, -3} on 182, the DFE on 177
    rng = random.Random(7704)
    pam, f = [3, 1, -1, -3], [1, 0.7]
    good, bad = [0, 1, 0, 1], [0, 0, 1, 1]
    counts = [0, 0, 0]
    for _ in range(200):
        x = [rng.choice(pam) for _ in range(40)]
        y = [v + rng.gauss(0, 0.35) for v in channel_out(f, x, [3])]
        ml = rsse(y, f, pam, [list(range(4))], pre=[3])
        for i, parts in enumerate(([good], [bad], [])):
            counts[i] += rsse(y, f, pam, parts, pre=[3]) == ml
    assert counts == [200, 182, 177]


def test_noiseless_recovery_with_any_partition() -> None:
    rng = random.Random(7705)
    pam = [3, 1, -1, -3]
    f = [1, 0.5, -0.3]
    x = [rng.choice(pam) for _ in range(100)]
    y = channel_out(f, x, [1, 1])
    for parts in ([], [[0, 1, 0, 1]], [[0, 1, 2, 3]], [[0, 1, 2, 3], [0, 1, 0, 1]], [[0, 1, 0, 1], [0, 0, 0, 0]]):
        assert rsse(y, f, pam, parts, pre=[1, 1]) == x


def test_state_count_and_partition_checks() -> None:
    assert number_of_states([[0, 1, 2, 3], [0, 1, 0, 1]]) == 8
    assert check_partitions([[0, 1, 2, 3], [0, 1, 0, 1]], 4) == [4, 2]
    with pytest.raises(ValueError):
        check_partitions([[0, 1, 0, 1], [0, 0, 1, 1]], 4)  # {3, -1} is split by the next partition
    with pytest.raises(ValueError):
        check_partitions([[0, 2, 0, 2]], 4)
    with pytest.raises(ValueError):
        rsse([1.0], [1, 0.5], [1, -1], [[0, 1], [0, 1]], pre=[1])
