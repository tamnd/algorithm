# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-oracle-model/. The authors are listed in prov/6J2DGY.jsonl.

import random

from random_oracle_model import Q, LazyRandomOracle, keygen, sign, simulate_sign, verify


def test_lazy_sampling_is_consistent_and_uniform() -> None:
    h = LazyRandomOracle(16, random.Random(1993))
    assert h.query(b"a") == h.query(b"a")
    counts = [0] * 16
    for i in range(16000):
        counts[h.query(i.to_bytes(4, "big"))] += 1
    # chi-square with 15 degrees of freedom; the 0.999 quantile is about 37.7
    chi2 = sum((c - 1000) ** 2 / 1000 for c in counts)
    assert chi2 < 37.7
    assert len(h.log) == 16002


def test_programming_rules() -> None:
    h = LazyRandomOracle(100, random.Random(2))
    h.program(b"x", 42)
    assert h.query(b"x") == 42
    for bad in (b"x",):
        try:
            h.program(bad, 1)
        except ValueError:
            pass
        else:
            raise AssertionError("reprogramming must fail")
    try:
        h.program(b"y", 100)
    except ValueError:
        pass
    else:
        raise AssertionError("out of range must fail")


def test_real_signatures_verify() -> None:
    rng = random.Random(7)
    h = LazyRandomOracle(Q, rng)
    x, y = keygen(rng)
    for i in range(50):
        m = b"msg %d" % i
        assert verify(h, y, m, sign(h, x, m, rng))
    assert not verify(h, y, b"other", sign(h, x, b"msg 0", rng))


def test_simulator_signs_without_the_key() -> None:
    rng = random.Random(11)
    h = LazyRandomOracle(Q, rng)
    _, y = keygen(rng)  # the simulator throws the secret key away
    for i in range(200):
        m = b"chosen message %d" % i
        sig = simulate_sign(h, y, m, rng)
        assert verify(h, y, m, sig)


def test_extractability_sees_the_queries() -> None:
    rng = random.Random(3)
    h = LazyRandomOracle(Q, rng)
    x, y = keygen(rng)
    sig = sign(h, x, b"m", rng)
    h.log.clear()
    verify(h, y, b"m", sig)
    assert len(h.log) == 1 and h.log[0].endswith(b"m")
