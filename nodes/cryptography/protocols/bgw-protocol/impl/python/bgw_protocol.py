# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bgw-protocol/. The authors are listed in prov/DSEB3X.jsonl.
"""Semi-honest BGW over a prime field, with n parties and threshold t < n/2.

Party P_i holds the value f(i) of a random polynomial f of degree t on each
wire (Shamir sharing, a small local copy here). Addition and multiplication
by a constant are local. A product of two sharings has degree 2t, so each
multiplication ends with a degree reduction, in one of two ways:

  "bgw": the original method of Ben-Or, Goldwasser and Wigderson (1988):
         randomize the degree-2t polynomial with sharings of zero, then
         truncate it to degree t with the linear map A = V P V^-1, computed
         on shares and reconstructed toward each party;
  "grr": the simplification of Gennaro, Rabin and Rabin (1998): each party
         reshares its product h_i with degree t, and each party combines the
         shares it received with the Lagrange coefficients at 0.

A brute-force Reed-Solomon decoder shows the malicious case: with n >= 3t + 1
any t wrong shares can be corrected (the efficient way is Berlekamp-Welch).

For study only. The code is not constant time, uses Python's random module,
and runs all parties in one process with no real channels. Use a maintained
framework such as MP-SPDZ for real data.
"""

import itertools
import random
from dataclasses import dataclass
from typing import Optional, Sequence

P61 = (1 << 61) - 1

Gate = tuple[str, int, int, int]   # (op, a, b, c); for CMUL, b is the constant


@dataclass
class Circuit:
    n_wires: int
    inputs: dict[int, int]          # input wire -> owner party (1..n)
    outputs: list[int]
    gates: list[Gate]


@dataclass
class Stats:
    messages: int = 0               # field elements sent between parties
    multiplications: int = 0
    max_degree_after_mul: int = 0   # largest degree of a product sharing after reduction


# ---------------------------------------------------------------- polynomials


def poly_eval(coeffs: Sequence[int], x: int, p: int) -> int:
    acc = 0
    for c in reversed(coeffs):
        acc = (acc * x + c) % p
    return acc


def share(secret: int, t: int, n: int, p: int, rng: random.Random) -> list[int]:
    """Shamir shares f(1), ..., f(n) of a random f of degree t with f(0) = secret."""
    coeffs = [secret % p] + [rng.randrange(p) for _ in range(t)]
    return [poly_eval(coeffs, i, p) for i in range(1, n + 1)]


def lagrange_at_zero(points: Sequence[int], p: int) -> list[int]:
    """Coefficients l_i with g(0) = sum l_i g(x_i) for every g of degree < len(points)."""
    lam = []
    for i, xi in enumerate(points):
        num = den = 1
        for j, xj in enumerate(points):
            if j != i:
                num = num * xj % p
                den = den * (xj - xi) % p
        lam.append(num * pow(den, p - 2, p) % p)
    return lam


def reconstruct(shares: Sequence[int], p: int, points: Optional[Sequence[int]] = None) -> int:
    """Interpolate at 0 from the given shares (by default at the points 1..len)."""
    pts = list(points) if points is not None else list(range(1, len(shares) + 1))
    return sum(l * s for l, s in zip(lagrange_at_zero(pts, p), shares)) % p


def interpolate(xs: Sequence[int], ys: Sequence[int], p: int) -> list[int]:
    """Coefficients of the polynomial of degree < len(xs) through the points."""
    k = len(xs)
    coeffs = [0] * k
    for i in range(k):
        basis = [1]
        den = 1
        for j in range(k):
            if j != i:
                basis = [(a - xs[j] * b) % p for a, b in zip([0] + basis, basis + [0])]
                den = den * (xs[i] - xs[j]) % p
        f = ys[i] * pow(den, p - 2, p) % p
        coeffs = [(c + f * b) % p for c, b in zip(coeffs, basis)]
    return coeffs


def degree(shares: Sequence[int], p: int) -> int:
    """Degree of the polynomial through (i, shares[i-1]), i = 1..n (-1 for zero)."""
    c = interpolate(list(range(1, len(shares) + 1)), shares, p)
    d = len(c) - 1
    while d >= 0 and c[d] == 0:
        d -= 1
    return d


# ---------------------------------------------------------------- degree reduction


def truncation_matrix(n: int, t: int, p: int) -> list[list[int]]:
    """A = V P V^-1: maps the values at 1..n of a polynomial of degree < n to
    the values of the same polynomial cut to its coefficients 0..t."""
    # Column m of V^-1 maps values to coefficient m; we build A row by row.
    xs = list(range(1, n + 1))
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        unit = [1 if k == i else 0 for k in range(n)]
        coeffs = interpolate(xs, unit, p)[: t + 1]       # P V^-1 e_i
        for j in range(n):
            a[j][i] = poly_eval(coeffs, xs[j], p)        # V (...)
    return a


def reduce_bgw(h: list[int], t: int, p: int, rng: random.Random, st: Stats) -> list[int]:
    """Original BGW: randomize with sharings of zero, then truncate on shares."""
    n = len(h)
    # Randomize: each P_i shares a random q_i of degree 2t with q_i(0) = 0.
    ht = list(h)
    for _ in range(n):
        zero = share(0, 2 * t, n, p, rng)  # @line L7
        ht = [(x + z) % p for x, z in zip(ht, zero)]
        st.messages += n - 1
    # Each P_i shares its point ht_i with degree t.
    sub = [share(x, t, n, p, rng) for x in ht]  # @line L8
    st.messages += n * (n - 1)
    # Each P_j computes its share of (A ht)_k for every k, and sends it to P_k.
    a = truncation_matrix(n, t, p)
    new = []
    for k in range(n):
        shares_of_k = [sum(a[k][i] * sub[i][j] for i in range(n)) % p for j in range(n)]  # @line L9
        new.append(reconstruct(shares_of_k, p))  # @line L10
    st.messages += n * (n - 1)
    return new


def reduce_grr(h: list[int], t: int, p: int, rng: random.Random, st: Stats) -> list[int]:
    """GRR: reshare each h_i with degree t, combine with Lagrange coefficients at 0."""
    n = len(h)
    lam = lagrange_at_zero(list(range(1, n + 1)), p)
    sub = [share(x, t, n, p, rng) for x in h]               # sub[i][j]: P_j's share of h_i
    st.messages += n * (n - 1)
    return [sum(lam[i] * sub[i][j] for i in range(n)) % p for j in range(n)]


# ---------------------------------------------------------------- the protocol


def bgw(circ: Circuit, inputs: dict[int, int], n: int, t: int, p: int, rng: random.Random,
        mode: str = "grr") -> tuple[list[int], Stats]:
    """Evaluate circ on the inputs (wire -> value); return outputs and counters."""
    if not 2 * t < n:
        raise ValueError("semi-honest BGW needs t < n/2")
    st = Stats()
    sh: dict[int, list[int]] = {}
    for w, owner in circ.inputs.items():  # @line L1
        sh[w] = share(inputs[w], t, n, p, rng)
        st.messages += n - 1
    for op, a, b, c in circ.gates:  # @line L2
        if op == "ADD":  # @line L3
            sh[c] = [(x + y) % p for x, y in zip(sh[a], sh[b])]
        elif op == "CMUL":  # @line L4
            sh[c] = [b * x % p for x in sh[a]]
        elif op == "MUL":  # @line L5
            h = [x * y % p for x, y in zip(sh[a], sh[b])]  # @line L6
            if mode == "bgw":
                sh[c] = reduce_bgw(h, t, p, rng, st)
            else:
                sh[c] = reduce_grr(h, t, p, rng, st)
            st.multiplications += 1
            st.max_degree_after_mul = max(st.max_degree_after_mul, degree(sh[c], p))
        else:
            raise ValueError(op)
    out = [reconstruct(sh[w], p) for w in circ.outputs]  # @line L11
    st.messages += n * (n - 1) * len(circ.outputs)
    return out, st


def plain_eval(circ: Circuit, inputs: dict[int, int], p: int) -> list[int]:
    v = dict(inputs)
    for op, a, b, c in circ.gates:
        v[c] = (v[a] + v[b]) % p if op == "ADD" else v[a] * v[b] % p if op == "MUL" else b * v[a] % p
    return [v[w] for w in circ.outputs]


def random_circuit(n_parties: int, n_inputs: int, n_gates: int, n_out: int, p: int,
                   rng: random.Random) -> Circuit:
    wires = list(range(n_inputs))
    gates: list[Gate] = []
    for k in range(n_gates):
        c = n_inputs + k
        op = rng.choice(["ADD", "MUL", "MUL", "CMUL"])
        a = rng.choice(wires)
        b = rng.randrange(p) if op == "CMUL" else rng.choice(wires)
        gates.append((op, a, b, c))
        wires.append(c)
    owners = {w: 1 + w % n_parties for w in range(n_inputs)}
    return Circuit(n_inputs + n_gates, owners, wires[-n_out:], gates)


# ---------------------------------------------------------------- errors


def candidates(shares: Sequence[int], t: int, e: int, p: int) -> set[tuple[int, ...]]:
    """All polynomials of degree <= t that agree with at least n - e shares."""
    n = len(shares)
    xs = list(range(1, n + 1))
    found = set()
    for subset in itertools.combinations(range(n), t + 1):
        coeffs = interpolate([xs[i] for i in subset], [shares[i] for i in subset], p)
        agree = sum(poly_eval(coeffs, xs[i], p) == shares[i] for i in range(n))
        if agree >= n - e:
            found.add(tuple(coeffs))
    return found


def decode_with_errors(shares: Sequence[int], t: int, p: int, e: Optional[int] = None) -> Optional[int]:
    """Brute-force Reed-Solomon decoding with up to e wrong shares (default t).

    Returns the secret if exactly one polynomial of degree <= t agrees with at
    least n - e shares, and None otherwise. The answer is unique and right
    when n >= t + 1 + 2e, so for e = t when n >= 3t + 1. Berlekamp-Welch does
    the same in polynomial time; this loop over C(n, t+1) subsets is only for
    small n."""
    found = candidates(shares, t, t if e is None else e, p)
    return next(iter(found))[0] if len(found) == 1 else None
