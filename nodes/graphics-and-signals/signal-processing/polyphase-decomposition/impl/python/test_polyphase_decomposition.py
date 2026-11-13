# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyphase-decomposition/. The authors are listed in prov/AYGB1S.jsonl.

import random
from fractions import Fraction

from polyphase_decomposition import (
    convolve,
    downsample,
    polyphase_components,
    polyphase_decimate,
    polyphase_interpolate,
    upsample,
)


def rand_fracs(rng, n):
    return [Fraction(rng.randint(-20, 20), rng.randint(1, 9)) for _ in range(n)]


def test_components_rebuild_filter() -> None:
    """H(z) = sum_j z^(-j) E_j(z^M): interleaving the components gives h back."""
    rng = random.Random(11101)
    for _ in range(100):
        h = rand_fracs(rng, rng.randint(1, 20))
        m = rng.randint(1, 6)
        e = polyphase_components(h, m)
        rebuilt = [0] * len(h)
        for j, comp in enumerate(e):
            for i, c in enumerate(comp):
                rebuilt[i * m + j] = c
        assert rebuilt == h
        # the same identity as polynomials: sum_j z^(-j) E_j(z^M) = sum_j delay_j(upsample(e_j))
        total = [0] * len(h)
        for j, comp in enumerate(e):
            up = upsample(comp, m)
            for i, v in enumerate(up):
                if i + j < len(h):
                    total[i + j] += v
        assert total == h


def test_decimator_equals_filter_then_downsample() -> None:
    rng = random.Random(11102)
    for _ in range(200):
        k = rng.randint(1, 16)
        m = rng.randint(1, 6)
        h = rand_fracs(rng, k)
        x = rand_fracs(rng, rng.randint(1, 30))
        assert polyphase_decimate(h, x, m) == downsample(convolve(h, x), m)


def test_interpolator_equals_upsample_then_filter() -> None:
    rng = random.Random(11103)
    for _ in range(200):
        k = rng.randint(1, 16)
        l = rng.randint(1, 6)
        h = rand_fracs(rng, k)
        x = rand_fracs(rng, rng.randint(1, 30))
        assert polyphase_interpolate(h, x, l) == convolve(h, upsample(x, l))


def test_noble_identities() -> None:
    """G(z^M) then down by M equals down by M then G(z); up by L then G(z^L) equals G(z) then up by L."""
    rng = random.Random(11104)
    for _ in range(200):
        g = rand_fracs(rng, rng.randint(1, 8))
        f = rng.randint(1, 5)
        x = rand_fracs(rng, rng.randint(1, 25))
        left = downsample(convolve(upsample(g, f), x), f)
        right = convolve(g, downsample(x, f))
        n = min(len(left), len(right))
        assert left[:n] == right[:n]
        assert all(v == 0 for v in left[n:]) and all(v == 0 for v in right[n:])
        left = convolve(upsample(g, f), upsample(x, f))
        right = upsample(convolve(g, x), f)
        n = min(len(left), len(right))
        assert left[:n] == right[:n]
        assert all(v == 0 for v in left[n:]) and all(v == 0 for v in right[n:])


def test_multiply_counts() -> None:
    """Count the products the polyphase forms really compute, against K per kept output."""
    h = list(range(1, 25))  # K = 24
    x = list(range(1, 101))
    m = 4
    count = 0
    for j, comp in enumerate(polyphase_components(h, m)):
        for n in range((len(h) + len(x) - 2) // m + 1):
            for i in range(len(comp)):
                if 0 <= (n - i) * m - j < len(x):
                    count += 1
    # every product h[k] x[nM - k] with a valid index is used exactly once
    direct = sum(1 for n in range((len(h) + len(x) - 2) // m + 1) for k in range(len(h)) if 0 <= n * m - k < len(x))
    assert count == direct
    assert direct <= len(h) * ((len(h) + len(x) - 2) // m + 1)
