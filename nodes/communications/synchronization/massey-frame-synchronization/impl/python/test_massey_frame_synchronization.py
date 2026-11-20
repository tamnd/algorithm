# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/massey-frame-synchronization/. The authors are listed in prov/JTBTTM.jsonl.

import math
import random

from cbb import wilson
from massey_frame_synchronization import (
    correlation_sync,
    hard_sync,
    high_snr_sync,
    ln_cosh,
    massey_metric,
    massey_sync,
)

BARKER7 = [1, 1, 1, -1, -1, 1, -1]
BARKER13 = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]


def window(rng, s, n, es, n0):
    """A cyclic window of n symbols: random +-1 data with s at a random start mu."""
    mu = rng.randrange(n)
    d = [rng.choice((1, -1)) for _ in range(n)]
    for i, si in enumerate(s):
        d[(mu + i) % n] = si
    sd = math.sqrt(n0 / 2)
    return mu, [math.sqrt(es) * x + rng.gauss(0, sd) for x in d]


def log_likelihood(y, s, mu, es, n0):
    """ln p(y | mu) from the model, term by term: Gaussian densities at the sync
    positions, and the average of the two Gaussian densities at the data positions."""
    n, a = len(y), math.sqrt(es)
    sync = {(mu + i) % n: si for i, si in enumerate(s)}
    total = 0.0
    for i, v in enumerate(y):
        if i in sync:
            total += -((v - a * sync[i]) ** 2) / n0
        else:
            total += math.log(0.5 * math.exp(-((v - a) ** 2) / n0) + 0.5 * math.exp(-((v + a) ** 2) / n0))
    return total - n * 0.5 * math.log(math.pi * n0)


def test_ln_cosh():
    for x in (-30.0, -2.5, -0.1, 0.0, 0.3, 4.0, 700.0):
        if abs(x) < 300:
            assert abs(ln_cosh(x) - math.log(math.cosh(x))) < 1e-12
    assert abs(ln_cosh(1000.0) - (1000.0 - math.log(2.0))) < 1e-9


def test_metric_is_scaled_log_likelihood():
    rng = random.Random(1)
    for _ in range(20):
        es, n0 = 1.0, rng.uniform(0.3, 3.0)
        s = BARKER7 if rng.random() < 0.5 else BARKER13
        _, y = window(rng, s, 24, es, n0)
        scale = 2 * math.sqrt(es) / n0
        ll = [log_likelihood(y, s, mu, es, n0) for mu in range(len(y))]
        m = [massey_metric(y, s, mu, es, n0) for mu in range(len(y))]
        for mu in range(1, len(y)):
            assert abs((ll[mu] - ll[0]) - scale * (m[mu] - m[0])) < 1e-9
        best = max(range(len(y)), key=lambda k: ll[k])
        assert massey_sync(y, s, es, n0) == best


def test_high_snr_limit():
    rng = random.Random(2)
    for _ in range(50):
        _, y = window(rng, BARKER13, 40, 1.0, 1.0)
        assert massey_sync(y, BARKER13, 1.0, 1e-4) == high_snr_sync(y, BARKER13)


def test_hard_rule_counts_disagreements():
    y = [0.9, -1.2, 0.1, 1.1, -0.3, -0.8, 0.7, 1.0]
    s = [1, -1, 1]
    # Start 0 gives signs (+, -, +): no disagreement.
    assert hard_sync(y, s) == 0
    # Without noise every rule finds a start whose window matches s.
    clean = [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0]
    w = [1, 1, -1, -1, 1]
    for rule in (hard_sync, high_snr_sync, correlation_sync):
        mu = rule(clean, w)
        assert [clean[(mu + i) % len(clean)] for i in range(len(w))] == [float(v) for v in w]


def test_massey_beats_correlation_at_zero_db():
    # Barker 7 in a window of 32 at Es/N0 = 0 dB. With 600 trials both rules make
    # more than 100 errors, so the 99.9 percent Wilson intervals are narrow.
    rng = random.Random(3)
    es, n0 = 1.0, 1.0
    trials = 600
    err_m = err_c = 0
    for _ in range(trials):
        mu, y = window(rng, BARKER7, 32, es, n0)
        err_m += massey_sync(y, BARKER7, es, n0) != mu
        err_c += correlation_sync(y, BARKER7) != mu
    assert err_m >= 100 and err_c >= 100
    lo_c, _ = wilson(err_c, trials)
    _, hi_m = wilson(err_m, trials)
    assert hi_m < lo_c
