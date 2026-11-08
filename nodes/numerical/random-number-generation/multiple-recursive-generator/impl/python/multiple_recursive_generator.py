# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-recursive-generator/. The authors are listed in prov/S7DSDC.jsonl.


def mrg_next(x: list[int], a: list[int], m: int) -> int:
    """One step of x_n = (a_1 x_{n-1} + ... + a_k x_{n-k}) mod m.

    x holds the last k values, newest first: x[0] = x_{n-1}, ..., x[k-1] = x_{n-k}.
    It is updated in place and the new value is returned; the output is s / m.
    Cost: k multiplications and additions modulo m.
    """
    s = 0  # @line L1
    for j in range(len(a)):  # @line L2
        s = (s + a[j] * x[j]) % m
    for j in range(len(x) - 1, 0, -1):  # @line L3
        x[j] = x[j - 1]
    x[0] = s  # @line L4
    return s  # @line L5


def mrg_stream(seed: list[int], a: list[int], m: int, n: int) -> list[int]:
    """The next n values from a seed (newest first); the seed must not be all zero."""
    x = [v % m for v in seed]
    if len(x) != len(a):
        raise ValueError("the seed needs k values")
    if not any(x):
        raise ValueError("the all-zero seed is a fixed point")
    return [mrg_next(x, a, m) for _ in range(n)]


# Polynomials modulo a prime p are lists of coefficients, lowest degree first.

def _poly_mulmod(f: list[int], g: list[int], mod: list[int], p: int) -> list[int]:
    """f * g modulo the monic polynomial mod, coefficients modulo p."""
    k = len(mod) - 1
    prod = [0] * (len(f) + len(g) - 1)
    for i, fi in enumerate(f):
        if fi:
            for j, gj in enumerate(g):
                prod[i + j] = (prod[i + j] + fi * gj) % p
    for d in range(len(prod) - 1, k - 1, -1):
        c = prod[d]
        if c:
            for j in range(k + 1):
                prod[d - k + j] = (prod[d - k + j] - c * mod[j]) % p
    out = prod[:k] + [0] * (k - len(prod[:k]))
    return out


def poly_x_power(e: int, mod: list[int], p: int) -> list[int]:
    """z^e modulo (mod, p) by repeated squaring, as a list of k coefficients."""
    k = len(mod) - 1
    result = [1] + [0] * (k - 1)
    base = ([0, 1] + [0] * k)[:k] if k > 1 else _poly_mulmod([0, 1], [1], mod, p)
    while e:
        if e & 1:
            result = _poly_mulmod(result, base, mod, p)
        base = _poly_mulmod(base, base, mod, p)
        e >>= 1
    return result


def characteristic_polynomial(a: list[int], p: int) -> list[int]:
    """P(z) = z^k - a_1 z^(k-1) - ... - a_k, lowest coefficient first."""
    k = len(a)
    return [(-a[k - 1 - i]) % p for i in range(k)] + [1]


def is_primitive_knuth(a: list[int], p: int, r_prime_factors: list[int], p1_prime_factors: list[int]) -> bool:
    """Knuth's test (TAOCP 3.2.2) that z^k - a_1 z^(k-1) - ... - a_k is primitive modulo the prime p.

    r = (p^k - 1)/(p - 1). The caller supplies the distinct prime factors of r and of p - 1.
    (i) (-1)^(k-1) a_k is a primitive root modulo p;
    (ii) z^r mod P is the constant (-1)^(k-1) a_k;
    (iii) for every prime q dividing r, z^(r/q) mod P is not a constant.
    """
    k = len(a)
    mod = characteristic_polynomial(a, p)
    g = ((-1) ** (k - 1) * a[k - 1]) % p
    if g == 0 or any(pow(g, (p - 1) // q, p) == 1 for q in p1_prime_factors):
        return False
    r = (p**k - 1) // (p - 1)
    if poly_x_power(r, mod, p) != [g] + [0] * (k - 1):
        return False
    for q in r_prime_factors:
        t = poly_x_power(r // q, mod, p)
        if not any(t[1:]):
            return False
    return True


def mat_mul(A: list[list[int]], B: list[list[int]], m: int) -> list[list[int]]:
    n, l, c = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(l)) % m for j in range(c)] for i in range(n)]


def companion(a: list[int], m: int) -> list[list[int]]:
    """The matrix M with (x_n, ..., x_{n-k+1}) = M (x_{n-1}, ..., x_{n-k})."""
    k = len(a)
    M = [[0] * k for _ in range(k)]
    M[0] = [v % m for v in a]
    for i in range(1, k):
        M[i][i - 1] = 1
    return M


def mrg_jump(x: list[int], a: list[int], m: int, steps: int) -> list[int]:
    """The state after `steps` steps, by the matrix power M^steps mod m, in O(k^3 log steps)."""
    k = len(a)
    R = [[int(i == j) for j in range(k)] for i in range(k)]
    B = companion(a, m)
    e = steps
    while e:
        if e & 1:
            R = mat_mul(R, B, m)
        B = mat_mul(B, B, m)
        e >>= 1
    return [row[0] for row in mat_mul(R, [[v] for v in x], m)]
