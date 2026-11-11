# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indifferentiability-framework/. The authors are listed in prov/C3GSSY.jsonl.

import random

from indifferentiability_framework import (
    LazyRandomFunction,
    advantage,
    chop_extension_attempt,
    length_extension_distinguisher,
    md,
    nmac,
)


def test_plain_md_is_distinguished() -> None:
    real, ideal = advantage(300)
    assert real == 1.0  # D always outputs 1 against (MD^f, f)
    assert ideal == 0.0  # and, here, never against (RO, S^RO)


def test_chop_md_resists_this_distinguisher() -> None:
    # With s = 16 bits dropped, D sees only half of the chaining value. Guessing the rest
    # succeeds with probability about 2^-16, so in 300 trials D almost surely never wins.
    rng = random.Random(5)
    hits = sum(chop_extension_attempt(LazyRandomFunction(t), 16, rng) for t in range(300))
    assert hits <= 2


def test_nmac_resists_this_distinguisher() -> None:
    rng = random.Random(9)
    hits = 0
    for t in range(300):
        f, g = LazyRandomFunction(t), LazyRandomFunction(10_000 + t)
        hits += length_extension_distinguisher(lambda b, f=f, g=g: nmac(f, g, b), f, rng)
    assert hits == 0


def test_md_extension_identity() -> None:
    # The identity that D uses: MD(m1, 1, s) = f(f(MD(m1), s), 3).
    f = LazyRandomFunction(42)
    for m1, s in ((1, 2), (0xDEADBEEF, 7)):
        assert md(f, [m1, 1, s]) == f(f(md(f, [m1]), s), 3)
