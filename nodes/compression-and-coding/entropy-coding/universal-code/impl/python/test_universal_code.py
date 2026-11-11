# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-code/. The authors are listed in prov/WKVPS7.jsonl.

import math
import random

from universal_code import (
    CODES,
    block_entropy,
    block_expected_length,
    block_is_decreasing,
    block_power_law,
    block_ratio,
    block_uniform,
    delta_length,
    entropy,
    exp_golomb_length,
    expected_length,
    fibonacci_length,
    gamma_length,
    geometric,
    is_decreasing,
    normalize,
    omega_length,
    power_law,
    ratio,
    uniform,
    vbyte_length,
    zipf,
)

PHI = (1 + math.sqrt(5)) / 2

# ---------------------------------------------------------------------------
# Codeword oracles, written from the definitions with strings.
# ---------------------------------------------------------------------------


def gamma_word(x: int) -> str:
    b = format(x, "b")
    return "0" * (len(b) - 1) + b


def delta_word(x: int) -> str:
    b = format(x, "b")
    return gamma_word(len(b)) + b[1:]


def omega_word(x: int) -> str:
    out = "0"
    while x > 1:
        b = format(x, "b")
        out = b + out
        x = len(b) - 1
    return out


def fibonacci_word(x: int) -> str:
    fib = [1, 2]
    while fib[-1] <= x:
        fib.append(fib[-1] + fib[-2])
    bits = []
    for f in reversed(fib):
        if f <= x:
            bits.append("1")
            x -= f
        else:
            bits.append("0")
    word = "".join(reversed(bits)).rstrip("0")
    return word + "1"


def test_lengths_match_codewords() -> None:
    assert omega_word(1000) == "11" + "1001" + "1111101000" + "0"
    assert fibonacci_word(100) == "00101000011"
    for x in range(1, 3000):
        assert gamma_length(x) == len(gamma_word(x))
        assert delta_length(x) == len(delta_word(x))
        assert omega_length(x) == len(omega_word(x))
        assert fibonacci_length(x) == len(fibonacci_word(x))
        y = x - 1 + 4
        assert exp_golomb_length(2)(x) == 2 * (y.bit_length() - 1) - 2 + 1
        assert vbyte_length(x) == 8 * len(range(0, x.bit_length(), 7))


def test_families_are_decreasing() -> None:
    n = 2000
    for p in (zipf(n), power_law(1.5, n), power_law(3.0, n), geometric(0.9, n), uniform(n)):
        assert is_decreasing(p)
        assert abs(math.fsum(p) - 1) < 1e-12
    assert block_is_decreasing(block_uniform(50))
    assert block_is_decreasing(block_power_law(1.2, 50))


# Concave, nondecreasing bounds l(x) <= f(log2 x). With E[log2 x] <= H(P) for a
# decreasing P, Jensen's inequality gives E[l] <= f(H(P)).
BOUNDS = {
    "gamma": lambda t: 2 * t + 1,
    "delta": lambda t: t + 2 * math.log2(t + 1) + 1,
    "omega": lambda t: t + 2 * math.log2(t + 1) + 4,
    "fibonacci": lambda t: t / math.log2(PHI) + 2,
    "expgolomb2": lambda t: 2 * t + 3,
    "vbyte": lambda t: 8 * t / 7 + 8,
}


def test_pointwise_bounds() -> None:
    for x in list(range(1, 5000)) + [2**j + d for j in range(13, 200) for d in (-1, 0, 1)]:
        t = math.log2(x)
        for name, f in BOUNDS.items():
            assert CODES[name](x) <= f(t) + 1e-9, (name, x)


def random_decreasing(rng: random.Random) -> list[float]:
    n = rng.randrange(1, 400)
    shape = rng.choice(["flat", "steep", "heavy"])
    if shape == "flat":
        w = [rng.random() for _ in range(n)]
    elif shape == "steep":
        w = [rng.random() ** rng.uniform(1, 30) for _ in range(n)]
    else:
        w = [rng.random() / rng.randrange(1, n + 1) ** rng.uniform(0.5, 3) for _ in range(n)]
    w = sorted((v + 1e-300 for v in w), reverse=True)
    return normalize(w)


def test_random_decreasing_laws() -> None:
    rng = random.Random(73)
    for _ in range(500):
        p = random_decreasing(rng)
        h = entropy(p)
        # The key lemma: P(x) <= 1/x for a decreasing P, so E[log2 x] <= H(P).
        assert math.fsum(q * math.log2(i + 1) for i, q in enumerate(p)) <= h + 1e-9
        for name, f in BOUNDS.items():
            assert expected_length(p, CODES[name]) <= f(h) + 1e-9, name
        # Universal with these constants K.
        assert ratio(p, CODES["gamma"]) <= 3 + 1e-9
        assert ratio(p, CODES["delta"]) <= 4 + 1e-9
        assert ratio(p, CODES["fibonacci"]) <= 1 / math.log2(PHI) + 2 + 1e-9


def test_block_evaluator_matches_exact() -> None:
    for w in (block_uniform(11), block_power_law(1.3, 11), block_power_law(2.5, 11)):
        p = []
        for j, m in enumerate(w):
            p.extend([m / 2**j] * 2**j)
        assert abs(entropy(p) - block_entropy(w)) < 1e-9
        # Exp-Golomb of order 2 on x - 1 does not depend only on floor(log2 x).
        for name in ("gamma", "delta", "omega", "vbyte"):
            assert abs(expected_length(p, CODES[name]) - block_expected_length(w, CODES[name])) < 1e-9


def test_asymptotic_optimality() -> None:
    gamma = [block_ratio(block_uniform(m), CODES["gamma"]) for m in (16, 256, 4096, 65536)]
    delta = [block_ratio(block_uniform(m), CODES["delta"]) for m in (16, 256, 4096, 65536)]
    omega = [block_ratio(block_uniform(m), CODES["omega"]) for m in (16, 256, 4096, 65536)]
    vbyte = [block_ratio(block_uniform(m), CODES["vbyte"]) for m in (16, 256, 4096, 65536)]
    # Delta and omega: the ratio tends to 1.
    assert delta == sorted(delta, reverse=True) and delta[-1] < 1.001
    assert omega == sorted(omega, reverse=True) and omega[-1] < 1.001
    # Gamma: universal, but the ratio tends to 2.
    assert gamma == sorted(gamma) and 1.999 < gamma[-1] <= 2
    # VByte: the ratio tends to 8/7.
    assert abs(vbyte[-1] - 8 / 7) < 1e-3


def test_unary_is_not_universal() -> None:
    # The ratio grows without bound as the support of the Zipf law grows.
    ratios = [ratio(zipf(n), CODES["unary"]) for n in (16, 256, 4096, 65536)]
    assert ratios == sorted(ratios) and ratios[-1] > 500
    # It is optimal for P(x) = 2^-x, where the ratio is 1.
    assert abs(ratio(geometric(0.5, 200), CODES["unary"]) - 1) < 1e-9


def test_known_ratios() -> None:
    n = 1 << 12
    z = zipf(n)
    assert ratio(z, CODES["delta"]) < ratio(z, CODES["gamma"])
    assert ratio(uniform(n), CODES["gamma"]) > 1.7
    assert ratio(power_law(2.0, n), CODES["gamma"]) < 1.1
