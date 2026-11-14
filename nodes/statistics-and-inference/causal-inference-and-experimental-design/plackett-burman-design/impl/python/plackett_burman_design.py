# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plackett-burman-design/. The authors are listed in prov/9V49FC.jsonl.
"""Plackett-Burman designs: N runs for up to N - 1 two-level factors, N a multiple of 4.

The design is a normalized Hadamard matrix H (H H^T = N I, first column all +1) without
its first column. Each remaining column has N/2 entries +1 and N/2 entries -1, and any two
columns are orthogonal, so the main effects are estimated independently, each with
variance 4 sigma^2 / N.
"""

from collections.abc import Sequence

# Plackett and Burman's first row for N = 12; the other rows are its cyclic shifts,
# and a last row of all minus signs completes the design.
PB12_GENERATOR = "++-+++---+-"


def cyclic_design(generator: str) -> list[list[int]]:
    """N - 1 cyclic shifts of the generator (row i is the generator shifted left by i),
    then a row of -1: the cyclic Plackett-Burman construction."""
    g = [1 if c == "+" else -1 for c in generator]
    m = len(g)
    return [[g[(j + i) % m] for j in range(m)] for i in range(m)] + [[-1] * m]


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def paley_design(q: int) -> list[list[int]]:
    """The Plackett-Burman design with N = q + 1 runs for a prime q = 3 (mod 4): the first
    row has +1 at the quadratic residues of q and at 0, and -1 at the non-residues."""
    if not is_prime(q) or q % 4 != 3:
        raise ValueError("q must be a prime with q = 3 (mod 4)")
    residues = {(x * x) % q for x in range(1, q)}
    gen = "".join("+" if j == 0 or j in residues else "-" for j in range(q))
    return cyclic_design(gen)


def sylvester_design(m: int) -> list[list[int]]:
    """The design with N = 2^m runs from the Sylvester-Hadamard matrix (a 2^(k-p) fraction)."""
    n = 2 ** m
    return [[-1 if bin(r & c).count("1") % 2 else 1 for c in range(1, n)] for r in range(n)]


def is_hadamard(h: Sequence[Sequence[int]]) -> bool:
    n = len(h)
    return all(len(r) == n and all(v in (1, -1) for v in r) for r in h) and all(
        sum(a * b for a, b in zip(h[i], h[j])) == (n if i == j else 0) for i in range(n) for j in range(n))


def with_mean_column(design: Sequence[Sequence[int]]) -> list[list[int]]:
    """The model matrix [1 | D]; for a Plackett-Burman design it is a Hadamard matrix."""
    return [[1] + list(r) for r in design]


def main_effects(design: Sequence[Sequence[int]], y: Sequence[float]) -> list[float]:
    """Main effect estimates: mean of y at +1 minus mean of y at -1, column by column."""
    n = len(design)
    return [2.0 * sum(r[j] * v for r, v in zip(design, y)) / n for j in range(len(design[0]))]
