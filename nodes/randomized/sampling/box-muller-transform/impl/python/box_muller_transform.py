# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/box-muller-transform/. The authors are listed in prov/D2WV7Z.jsonl.

"""The Box-Muller transform: two uniforms in, two independent N(0, 1) out.

In exact arithmetic with exact uniform reals the output pair is exactly a
pair of independent standard normal variates. In floating point the output
lies on a finite set; with 53-bit uniforms, |Z| never exceeds
sqrt(2 * 53 * ln 2), about 8.57. O(1) time per pair.
"""

import math
import random
from typing import Tuple


def box_muller(rng: random.Random) -> Tuple[float, float]:
    """Return two independent standard normal variates."""
    u1 = 1.0 - rng.random()  # @line L1
    u2 = rng.random()  # @line L2
    r = math.sqrt(-2.0 * math.log(u1))  # @line L3
    theta = 2.0 * math.pi * u2  # @line L4
    return r * math.cos(theta), r * math.sin(theta)  # @line L5


def box_muller_inverse(z1: float, z2: float) -> Tuple[float, float]:
    """The inverse map (z1, z2) -> (u1, u2), for tests and for the proof."""
    u1 = math.exp(-(z1 * z1 + z2 * z2) / 2.0)
    u2 = math.atan2(z2, z1) / (2.0 * math.pi)
    if u2 < 0.0:
        u2 += 1.0
    return u1, u2
