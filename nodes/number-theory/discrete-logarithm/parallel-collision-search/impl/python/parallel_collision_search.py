# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-collision-search/. The authors are listed in prov/M0GDZC.jsonl.

import random
from math import gcd, isqrt


def _solve(a: int, b: int, a2: int, b2: int, g: int, h: int, n: int, p: int) -> int | None:
    """Given g^a h^b = g^a2 h^b2, return a solution x of g^x = h, or None.

    None means the collision is useless: b = b2 (mod n), or gcd(b - b2, n) is
    too large to try all candidates.
    """
    s = (b - b2) % n  # @line L12
    d = gcd(s, n)
    if s == 0 or d > isqrt(n) + 1:
        return None
    m = n // d
    y = (a2 - a) // d * pow(s // d, -1, m) % m  # @line L13
    for t in range(d):  # @line L14
        if pow(g, y + t * m, p) == h:  # @line L15
            return y + t * m
    return None


def parallel_collision_search(
    g: int, h: int, n: int, p: int, clients: int = 4, seed: int = 0
) -> int | None:
    """Van Oorschot and Wiener's parallel collision search for log_g h modulo p.

    The clients are simulated in round robin: in each round every client makes
    one step of an r-adding walk on elements x = g^a h^b. A client that stands
    on a distinguished point sends (x, a, b) to the server table and restarts
    at a random point; two reports of the same x with different b give the
    logarithm. Return the x in [0, n) with g^x = h (mod p), or None if h is not
    a power of g.
    Precondition: p is prime, gcd(g, p) = 1 and n = ord(g) exactly.
    Raises ValueError if p < 2, n < 1 or clients < 1.
    Cost: heuristically (pi n / 2)^(1/2) / clients + 1/theta walk steps per
    client, one multiplication modulo p each, plus two exponentiations per
    restart; the server stores about theta (pi n / 2)^(1/2) + clients triples,
    where theta = 1/spacing is the density of distinguished points.
    """
    if p < 2 or n < 1 or clients < 1:
        raise ValueError("need p >= 2, n >= 1 and clients >= 1")
    g %= p
    h %= p
    if pow(h, n, p) != 1:  # @line L1
        return None
    if h == 1:  # @line L2
        return 0
    rng = random.Random(seed)
    spacing = max(1, isqrt(n) // (8 * clients))
    max_len = 20 * spacing
    rounds = 8 * (isqrt(n) // clients + spacing) + 16
    r_add = 16
    while True:  # @line L3
        # @line L4
        steps = [(rng.randrange(n), rng.randrange(n)) for _ in range(r_add)]
        mult = [pow(g, u, p) * pow(h, v, p) % p for u, v in steps]
        key = rng.randrange(1, p)
        table: dict[int, tuple[int, int]] = {}  # @line L5
        walkers = []
        for _ in range(clients):  # @line L6
            a, b = rng.randrange(n), rng.randrange(n)
            walkers.append([pow(g, a, p) * pow(h, b, p) % p, a, b, 0])
        for _ in range(rounds):  # @line L7
            for w in walkers:  # @line L8
                x, a, b, length = w
                v = x * key % p
                distinguished = v % spacing == 0
                if distinguished:  # @line L9
                    if x in table:  # @line L10
                        a2, b2 = table[x]
                        z = _solve(a, b, a2, b2, g, h, n, p)  # @line L11
                        if z is not None:
                            return z
                    else:
                        table[x] = (a, b)  # @line L16
                if distinguished or length >= max_len:  # @line L17
                    a, b = rng.randrange(n), rng.randrange(n)
                    w[:] = [pow(g, a, p) * pow(h, b, p) % p, a, b, 0]
                    continue
                j = v // spacing % r_add  # @line L18
                u, t = steps[j]
                w[:] = [x * mult[j] % p, (a + u) % n, (b + t) % n, length + 1]
