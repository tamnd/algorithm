# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marsaglia-polar-method/. The authors are listed in prov/E555BW.jsonl.

"""Marsaglia's polar method for pairs of independent N(0, 1) variates.

A uniform point (V1, V2) in the unit disk is found by rejection from the
square [-1, 1)^2. Each try succeeds with probability pi / 4, so a pair
takes 4 / pi tries in expectation (8 / pi uniforms). No sine or cosine is
needed. Exact for exact uniform reals; in floating point the output lies on
a finite set.
"""

import math
import random
from typing import Tuple


def polar_method(rng: random.Random) -> Tuple[float, float]:
    """Return two independent standard normal variates."""
    pair, _ = polar_method_counted(rng)
    return pair


def polar_method_counted(rng: random.Random) -> Tuple[Tuple[float, float], int]:
    """Same as polar_method, and also return the number of tries used."""
    tries = 0
    while True:  # @line L1
        tries += 1
        v1 = 2.0 * rng.random() - 1.0  # @line L2
        v2 = 2.0 * rng.random() - 1.0  # @line L2
        s = v1 * v1 + v2 * v2  # @line L3
        if 0.0 < s < 1.0:  # @line L4
            break
    f = math.sqrt(-2.0 * math.log(s) / s)  # @line L5
    return (v1 * f, v2 * f), tries  # @line L6
