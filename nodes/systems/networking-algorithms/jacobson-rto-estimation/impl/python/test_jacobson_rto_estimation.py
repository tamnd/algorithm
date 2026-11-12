# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobson-rto-estimation/. The authors are listed in prov/CNHXD2.jsonl.

import random
from fractions import Fraction as F

from jacobson_rto_estimation import JacobsonRto


def test_initial_and_first_sample() -> None:
    e = JacobsonRto()
    assert e.rto == 1 and e.srtt is None
    e.sample(F(1, 2))
    assert (e.srtt, e.rttvar) == (F(1, 2), F(1, 4))
    assert e.rto == F(3, 2)  # 1/2 + 4 * 1/4


def test_worked_example_exact() -> None:
    e = JacobsonRto(min_rto=F(0))
    rows = []
    for r in (F(1, 2), F(3, 5), F(2, 5), F(6, 5), F(1, 2)):
        e.sample(r)
        rows.append((e.srtt, e.rttvar, e.rto))
    assert rows == [
        (F(1, 2), F(1, 4), F(3, 2)),
        (F(41, 80), F(17, 80), F(109, 80)),
        (F(319, 640), F(3, 16), F(799, 640)),
        (F(3001, 5120), F(809, 2560), F(9473, 5120)),
        (F(23567, 40960), F(1059, 4096), F(65927, 40960)),
    ]


def test_rttvar_uses_the_old_srtt() -> None:
    e = JacobsonRto()
    e.sample(F(1, 2))
    e.sample(F(3, 5))
    assert e.rttvar == F(17, 80)
    # The wrong order (SRTT first) would give 67/320.
    assert F(3, 4) * F(1, 4) + abs(F(7, 8) * F(1, 2) + F(3, 5) / 8 - F(3, 5)) / 4 == F(67, 320)


def test_lower_bound_and_granularity() -> None:
    e = JacobsonRto()
    for _ in range(50):
        e.sample(F(1, 100))
    assert e.rto == 1  # rule 2.4 rounds up to 1 second
    raw = JacobsonRto(granularity=F(1, 10), min_rto=F(0))
    for _ in range(200):
        raw.sample(F(1, 100))
    # RTTVAR decays to almost 0, so max(G, 4 RTTVAR) = G.
    assert raw.rto == raw.srtt + F(1, 10)


def test_back_off_doubles_and_caps() -> None:
    e = JacobsonRto()
    seen = [e.back_off() for _ in range(8)]
    assert seen == [2, 4, 8, 16, 32, 60, 60, 60]
    e.sample(F(1, 5))  # a new sample collapses the backed-off value
    assert e.rto == 1


def test_constant_samples_converge() -> None:
    e = JacobsonRto(min_rto=F(0))
    for _ in range(300):
        e.sample(F(2))
    assert abs(e.srtt - 2) < F(1, 10**9)
    assert e.rttvar < F(1, 10**9)


def test_fewer_spurious_timeouts_than_rfc793() -> None:
    # Four samples of 0.1 s, then a spike of 0.4 s, twenty times.
    pattern = ([F(1, 10)] * 4 + [F(2, 5)]) * 20
    srtt, late793 = None, 0
    for x in pattern:  # RFC 793: alpha = 0.9, beta = 2
        if srtt is not None and x > 2 * srtt:
            late793 += 1
        srtt = x if srtt is None else F(9, 10) * srtt + F(1, 10) * x
    e, late = JacobsonRto(min_rto=F(0)), []
    for j, x in enumerate(pattern):
        if j > 0 and x > e.rto:
            late.append(j)
        e.sample(x)
    assert late793 == 20
    assert late == [4, 9, 14]


def test_float_and_fraction_agree() -> None:
    rng = random.Random(3)
    a, b = JacobsonRto(), JacobsonRto(granularity=0.0, alpha=0.125, beta=0.25, initial_rto=1.0, min_rto=1.0, max_rto=60.0)
    for _ in range(100):
        x = F(rng.randint(1, 3000), 1000)
        a.sample(x)
        b.sample(float(x))
        assert abs(float(a.rto) - b.rto) < 1e-9
