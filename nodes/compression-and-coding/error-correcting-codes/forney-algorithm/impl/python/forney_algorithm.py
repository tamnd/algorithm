# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forney-algorithm/. The authors are listed in prov/6QZVB2.jsonl.
"""The Forney algorithm: error values from the error locator and the syndromes.

Conventions. The code has the consecutive zeros beta^b, ..., beta^(b+2t-1), with
beta = alpha^step a primitive element (step = 1 for most codes, 11 for CCSDS).
S_j = r(beta^j). An error of value Y at position i has the locator X = beta^i.
Lambda(x) = prod_k (1 - X_k x). Then, for each error,

    Y_k = - X_k^(1-b) * Omega(X_k^-1) / Lambda'(X_k^-1),
    Omega(x) = S(x) Lambda(x) mod x^(2t),  S(x) = sum_{i<2t} S_(b+i) x^i.

Polynomials are lists, lowest degree first. Works over GF(2^m) and GF(p).
"""

from gf import GF2m, GFp

Field = GF2m | GFp


def poly_mul_mod(f: Field, a: list[int], b: list[int], deg_bound: int) -> list[int]:
    """a * b mod x^deg_bound."""
    out = [0] * deg_bound
    for i, x in enumerate(a[:deg_bound]):
        if x:
            for j, y in enumerate(b[: deg_bound - i]):
                if y:
                    out[i + j] = f.add(out[i + j], f.mul(x, y))
    return out


def poly_eval(f: Field, a: list[int], x: int) -> int:
    y = 0
    for c in reversed(a):
        y = f.add(f.mul(y, x), c)
    return y


def formal_derivative(f: Field, a: list[int]) -> list[int]:
    """sum i a_i x^(i-1); over GF(2^m) only the odd terms stay."""
    return [f.times(i, a[i]) for i in range(1, len(a))]


def locator(f: Field, positions: list[int], step: int = 1) -> list[int]:
    """prod_k (1 - X_k x) with X_k = beta^(i_k)."""
    lam = [1]
    for i in positions:
        x = f.alpha(step * i)
        nxt = lam + [0]
        for d in range(len(lam)):
            nxt[d + 1] = f.sub(nxt[d + 1], f.mul(x, lam[d]))
        lam = nxt
    return lam


def forney(f: Field, syn: list[int], lam: list[int], positions: list[int], b: int = 1,
           step: int = 1) -> list[int]:
    """Error values Y_k for the given positions.

    Precondition: syn = [S_b, ..., S_(b+2t-1)], lam = Lambda with Lambda(0) = 1 whose
    roots are the beta^(-i_k) for the given distinct positions, and len(positions) <= 2t.
    With erasures, lam is the full locator (errors times erasures).
    Cost: O(t^2) field operations for Omega and O(t) per error value.
    """
    two_t = len(syn)
    s_poly = list(syn)  # @line L1: S(x) = sum S_(b+i) x^i
    omega = poly_mul_mod(f, s_poly, lam, two_t)  # @line L2: Omega = S Lambda mod x^(2t)
    dlam = formal_derivative(f, lam)  # @line L3
    values = []
    for i in positions:  # @line L4
        x = f.alpha(step * i)  # @line L5: X_k
        x_inv = f.inv(x)
        num = f.mul(f.pow(x, 1 - b), poly_eval(f, omega, x_inv))  # @line L6
        den = poly_eval(f, dlam, x_inv)
        values.append(f.sub(0, f.mul(num, f.inv(den))))
    return values  # @line L7


def syndromes(f: Field, word: list[int], two_t: int, b: int = 1, step: int = 1) -> list[int]:
    """S_j = word(beta^j) for j = b .. b + 2t - 1."""
    return [poly_eval(f, word, f.alpha(step * j)) for j in range(b, b + two_t)]
