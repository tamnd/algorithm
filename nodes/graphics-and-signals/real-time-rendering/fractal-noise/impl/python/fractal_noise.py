# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fractal-noise/. The authors are listed in prov/KJNY6S.jsonl.

"""Fractal noise: a sum of octaves of a base noise.

fbm(x) = sum over i < K of g^i N(lambda^i x + o_i), where N is any base noise,
lambda is the lacunarity, g is the gain (the persistence) and o_i is an
optional offset per octave. Turbulence sums g^i |N| in place of g^i N.
Musgrave's form sets g = lambda^(-H) for a roughness exponent H.

The base noise here is a 2D gradient noise in the style of Perlin noise, so
that the module stands alone: a seeded permutation picks one of 8 gradients
at each integer point, and the quintic fade blends the 4 corners of the cell.
Any callable N(x, y) can take its place.
"""

import random
from math import floor, log

GRADS = ((1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))


def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


class GradientNoise2D:
    """A seeded 2D gradient noise. It is 0 at the integer points and |N| <= 2."""

    def __init__(self, seed=0):
        p = list(range(256))
        random.Random(seed).shuffle(p)
        self.perm = p + p

    def gradient(self, i, j):
        p = self.perm
        return GRADS[p[p[i & 255] + (j & 255)] & 7]

    def __call__(self, x, y):
        i, j = floor(x), floor(y)
        tx, ty = x - i, y - j
        u, v = fade(tx), fade(ty)
        total = 0.0
        for a in (0, 1):
            for b in (0, 1):
                gx, gy = self.gradient(i + a, j + b)
                w = (u if a else 1 - u) * (v if b else 1 - v)
                total += w * (gx * (tx - a) + gy * (ty - b))
        return total


def octave_offsets(count, seed=0):
    """Fixed pseudorandom offsets, one per octave, to break the alignment of the lattices."""
    rng = random.Random(seed)
    return [(rng.uniform(0, 256), rng.uniform(0, 256)) for _ in range(count)]


def fbm(noise, x, y, octaves=6, lacunarity=2.0, gain=0.5, offsets=None):
    """Fractal Brownian motion noise: sum of gain^i * noise(lacunarity^i * p + o_i)."""
    total, amp, freq = 0.0, 1.0, 1.0
    for i in range(octaves):
        ox, oy = offsets[i] if offsets else (0.0, 0.0)
        total += amp * noise(x * freq + ox, y * freq + oy)
        amp *= gain
        freq *= lacunarity
    return total


def turbulence(noise, x, y, octaves=6, lacunarity=2.0, gain=0.5, offsets=None):
    """Perlin's turbulence: the same sum with |noise| in place of noise."""
    total, amp, freq = 0.0, 1.0, 1.0
    for i in range(octaves):
        ox, oy = offsets[i] if offsets else (0.0, 0.0)
        total += amp * abs(noise(x * freq + ox, y * freq + oy))
        amp *= gain
        freq *= lacunarity
    return total


def musgrave_gain(H, lacunarity=2.0):
    """The gain g = lacunarity^(-H) that gives the amplitude a power law in the frequency."""
    return lacunarity ** (-H)


def amplitude_sum(octaves, gain):
    """The sum of gain^i for i < octaves, which bounds |fbm| / max|N|."""
    return sum(gain ** i for i in range(octaves))


def octave_limit(footprint, lacunarity=2.0, base_frequency=1.0):
    """The number of octaves whose period is at least two pixel footprints.

    Octave i has the frequency base_frequency * lacunarity^i. It is kept when
    base_frequency * lacunarity^i <= 1 / (2 * footprint).
    """
    top = 1.0 / (2.0 * footprint * base_frequency)
    if top < 1:
        return 0
    return floor(log(top) / log(lacunarity) + 1e-9) + 1
