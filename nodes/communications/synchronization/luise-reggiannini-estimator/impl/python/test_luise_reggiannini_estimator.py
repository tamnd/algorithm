# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luise-reggiannini-estimator/. The authors are listed in prov/6HGD52.jsonl.

import cmath
import math
import random

from luise_reggiannini_estimator import autocorrelation, crb_nu, lr_estimate


def tone(rng, n, nu, snr=None, phi=0.0):
    sd = math.sqrt(0.5 / snr) if snr else 0.0
    return [cmath.exp(1j * (2 * math.pi * nu * k + phi)) + (complex(rng.gauss(0, sd), rng.gauss(0, sd)) if sd else 0j) for k in range(n)]


def test_closed_form_of_the_sum() -> None:
    # sum_{m=1}^{L} e^(j 2 pi nu m) = e^(j pi nu (L+1)) sin(pi nu L) / sin(pi nu).
    for big_l in (1, 4, 16):
        for nu in (0.013, -0.04, 0.05):
            s = sum(cmath.exp(2j * math.pi * nu * m) for m in range(1, big_l + 1))
            c = cmath.exp(1j * math.pi * nu * (big_l + 1)) * math.sin(math.pi * nu * big_l) / math.sin(math.pi * nu)
            assert abs(s - c) < 1e-12


def test_exact_without_noise_inside_the_range() -> None:
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randrange(4, 40)
        big_l = rng.randrange(1, n)
        nu = rng.uniform(-1, 1) * 0.999 / (big_l + 1)
        z = tone(rng, n, nu, phi=rng.uniform(-3, 3))
        assert abs(lr_estimate(z, big_l) - nu) < 1e-12


def test_aliasing_outside_the_range() -> None:
    # For 1/(L+1) < nu < 1/L the angle wraps: the estimate is nu - 2/(L+1).
    big_l = 7
    nu = 0.135
    z = tone(random.Random(2), 32, nu)
    assert abs(lr_estimate(z, big_l) - (nu - 2 / (big_l + 1))) < 1e-12
    # For 1/L < nu the Dirichlet factor sin(pi nu L)/sin(pi nu) is negative as well.
    nu = 1.2 / (big_l + 1)
    z = tone(random.Random(2), 32, nu)
    assert abs(lr_estimate(z, big_l) - (nu - 1 / (big_l + 1))) < 1e-12


def test_autocorrelation_is_unbiased_for_a_tone() -> None:
    z = tone(random.Random(3), 20, 0.03, phi=1.0)
    for m in (1, 5, 19):
        assert abs(autocorrelation(z, m) - cmath.exp(2j * math.pi * 0.03 * m)) < 1e-12


def test_mse_against_the_crb() -> None:
    # N = 32, 300 trials per point, nu uniform in [-0.02, 0.02]. L = N/2 is close
    # to the bound down to about 0 dB; L = 8 is clearly worse at 0 dB.
    n, trials = 32, 300
    ratio = {}
    for big_l in (8, 16):
        for snr_db in (0, 10):
            snr = 10 ** (snr_db / 10)
            rng = random.Random(3)
            se = 0.0
            for _ in range(trials):
                nu = rng.uniform(-0.02, 0.02)
                e = lr_estimate(tone(rng, n, nu, snr, rng.uniform(-3, 3)), big_l) - nu
                se += e * e
            ratio[big_l, snr_db] = se / trials / crb_nu(n, snr)
    assert 0.8 < ratio[16, 10] < 1.3
    assert 0.9 < ratio[16, 0] < 1.8
    assert ratio[8, 0] > 1.2 * ratio[16, 0]
