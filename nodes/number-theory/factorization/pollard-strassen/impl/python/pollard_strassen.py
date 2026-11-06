# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-strassen/. The authors are listed in prov/CC5JPW.jsonl.

from math import gcd, isqrt

# Below this length, polynomials are multiplied and divided by the schoolbook
# method; above it, by Kronecker substitution and Newton iteration.
SMALL = 24


def poly_mul(a: list[int], b: list[int], n: int) -> list[int]:
    """Product of two polynomials with coefficients in [0, n), lowest degree first.

    Precondition: n >= 2. Large inputs use Kronecker substitution: each
    polynomial is packed into one integer, with a slot wide enough for a
    coefficient of the product, so one integer multiplication does the work.
    Cost: one multiplication of integers of O((len a + len b) log(n len)) bits."""
    if not a or not b:
        return []
    la, lb = len(a), len(b)
    if min(la, lb) <= SMALL:
        out = [0] * (la + lb - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    out[i + j] += x * y
        return [c % n for c in out]
    w = (2 * n.bit_length() + min(la, lb).bit_length()) // 8 + 1
    x = int.from_bytes(b"".join(c.to_bytes(w, "little") for c in a), "little")
    y = int.from_bytes(b"".join(c.to_bytes(w, "little") for c in b), "little")
    k = la + lb - 1
    z = (x * y).to_bytes(w * k, "little")
    return [int.from_bytes(z[i * w:(i + 1) * w], "little") % n for i in range(k)]


def series_inverse(g: list[int], k: int, n: int) -> list[int]:
    """h with g h = 1 mod x^k, for g[0] = 1. Newton iteration h <- h (2 - g h).

    Precondition: g[0] == 1, k >= 1. Cost: O(M(k)) ring operations, where M(k)
    is the cost of a product of length k."""
    h = [1]
    m = 1
    while m < k:
        m = min(2 * m, k)
        e = poly_mul(g[:m], h, n)[:m]
        e += [0] * (m - len(e))
        e[0] = (e[0] - 1) % n
        c = poly_mul(h, e, n)[:m]
        c += [0] * (m - len(c))
        h = [((h[i] if i < len(h) else 0) - c[i]) % n for i in range(m)]
    return h


def poly_rem(a: list[int], g: list[int], n: int) -> list[int]:
    """a mod g for a monic g of degree d >= 1, as a list of length d.

    Precondition: g[-1] == 1. Monic divisors need no inverses, so this works
    modulo a composite n. Cost: O(M(len a)) ring operations."""
    d = len(g) - 1
    if len(a) <= d:
        return a + [0] * (d - len(a))
    q_len = len(a) - d
    if d <= SMALL or q_len <= SMALL:
        r = a[:]
        for i in range(len(r) - 1, d - 1, -1):
            c = r[i]
            if c:
                for j in range(d):
                    r[i - d + j] = (r[i - d + j] - c * g[j]) % n
        return r[:d]
    inv = series_inverse(g[::-1], q_len, n)
    q = poly_mul(a[::-1][:q_len], inv, n)[:q_len]
    q = (q + [0] * (q_len - len(q)))[::-1]
    qg = poly_mul(q, g, n)
    return [(a[i] - qg[i]) % n for i in range(d)]


def product_tree(leaves: list[list[int]], n: int) -> list[list[list[int]]]:
    """Levels of the subproduct tree; level 0 is the leaves, the last level is
    the root. Node i of level k + 1 is the product of nodes 2i and 2i + 1 of
    level k, or a copy of node 2i if that one has no partner."""
    levels = [leaves]
    while len(levels[-1]) > 1:
        cur = levels[-1]
        levels.append([poly_mul(cur[i], cur[i + 1], n) if i + 1 < len(cur) else cur[i]
                       for i in range(0, len(cur), 2)])
    return levels


def rising_product(b: int, n: int) -> list[int]:
    """Coefficients of f(x) = (x + 1)(x + 2)...(x + b) modulo n.

    Precondition: b >= 1. Small b multiply one linear factor at a time, in
    O(b^2) operations; larger b use the root of the subproduct tree, in
    O(M(b) log b) operations."""
    if b > SMALL:
        return product_tree([[i % n, 1] for i in range(1, b + 1)], n)[-1][0]
    f = [1]
    for i in range(1, b + 1):
        g = [0] + f
        for k, c in enumerate(f):
            g[k] = (g[k] + i * c) % n
        f = g
    return f


def multipoint_eval(f: list[int], points: list[int], n: int) -> list[int]:
    """[f(a) mod n for a in points], by the remainder tree.

    Precondition: points is not empty. Cost: O(M(k) log k) ring operations
    for k points and deg f < 2k or so. For at most SMALL points, Horner's rule
    on each point is faster, at O(k deg f) operations."""
    if len(points) <= SMALL:
        out = []
        for a in points:
            v = 0
            for c in reversed(f):
                v = (v * a + c) % n
            out.append(v)
        return out
    levels = product_tree([[(-a) % n, 1] for a in points], n)
    rems = [poly_rem(f, levels[-1][0], n)]
    for k in range(len(levels) - 2, -1, -1):
        rems = [poly_rem(rems[i // 2], node, n) for i, node in enumerate(levels[k])]
    return [r[0] for r in rems]


def least_prime_factor(n: int) -> int:
    """The least prime factor of n >= 2, by the Pollard-Strassen method.

    Precondition: n >= 2. With b = ceil(n^(1/4)), f(x) = (x + 1)(x + 2)...(x + b)
    gives f(jb) = the product of the b integers in (jb, (j + 1) b]. The first
    j with gcd(f(jb), n) > 1 holds the least prime factor, found by a scan of
    that block. If no block of the b blocks up to b^2 >= sqrt(n) shares a
    factor with n, then n is prime. Cost: O(n^(1/4) log^2 n) ring operations
    modulo n with fast multiplication, and O(n^(1/4) log n) stored residues."""
    if n < 2:
        raise ValueError("n must be at least 2")
    b = isqrt(isqrt(n))  # @line L1
    while b ** 4 < n:
        b += 1
    f = rising_product(b, n)  # @line L2
    values = multipoint_eval(f, [j * b for j in range(b)], n)  # @line L3
    for j, v in enumerate(values):  # @line L4
        if gcd(v, n) > 1:  # @line L5
            for d in range(max(2, j * b + 1), j * b + b + 1):  # @line L6
                if n % d == 0:
                    return d
    return n  # @line L7


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Each pass finds the least prime factor p of what is left and divides it
    out. A cofactor m < p^2 has all its prime factors >= p, so it is 1 or a
    prime, and the loop stops. Cost: at most log2 n calls of
    least_prime_factor."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    while n > 1:
        p = least_prime_factor(n)
        while n % p == 0:
            out.append(p)
            n //= p
        if 1 < n < p * p:
            out.append(n)
            break
    return out
