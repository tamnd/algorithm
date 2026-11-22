# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isw-private-circuits/. The authors are listed in prov/F6CSK5.jsonl.
"""The ISW private circuit construction over GF(2) (Ishai, Sahai, Wagner, CRYPTO 2003).

Each bit x of a circuit is carried as n shares x_1 .. x_n with
x_1 xor .. xor x_n = x. XOR and NOT gates work on each share. The AND gate
is the randomized ISW gadget. The module also lists every intermediate
wire of the gadget, so that a test can check the probing model by
exhaustive enumeration. This is a model of a circuit, not of a device:
the randomness comes from a seeded ``random.Random``.
"""

import random

Wire = tuple[str, int]


def share(rng: random.Random, x: int, n: int) -> list[int]:
    """Return n uniform bits whose XOR is the bit x. Cost: Theta(n)."""
    s = [rng.randrange(2) for _ in range(n - 1)]
    last = x
    for v in s:
        last ^= v
    return s + [last]


def unshare(s: list[int]) -> int:
    """Return the XOR of the shares. Cost: Theta(n)."""
    x = 0
    for v in s:
        x ^= v
    return x


def isw_and_wires(
    a: list[int], b: list[int], r: dict[tuple[int, int], int]
) -> tuple[list[int], list[Wire]]:
    """The ISW AND gadget with given random bits, and the list of its wires.

    Precondition: len(a) == len(b) == n >= 1, and r[(i, j)] is a bit for
    each 0 <= i < j < n. Returns the n output shares and every value the
    gadget computes, in order, with a name. The input shares are wires too.
    Cost: n^2 ANDs, n(n-1)/2 random bits and 2n(n-1) XORs.
    """
    n = len(a)
    wires: list[Wire] = [(f"a{i}", a[i]) for i in range(n)] + [(f"b{i}", b[i]) for i in range(n)]
    rr: dict[tuple[int, int], int] = {}
    for i in range(n):  # @line L1
        for j in range(i + 1, n):  # @line L2
            rr[(i, j)] = r[(i, j)]  # @line L3
            wires.append((f"r{i}{j}", rr[(i, j)]))
            t1 = a[i] & b[j]
            t2 = rr[(i, j)] ^ t1
            t3 = a[j] & b[i]
            rr[(j, i)] = t2 ^ t3  # @line L4
            wires += [(f"a{i}b{j}", t1), (f"r{i}{j}+a{i}b{j}", t2), (f"a{j}b{i}", t3), (f"r{j}{i}", rr[(j, i)])]
    c = []
    for i in range(n):  # @line L5
        acc = a[i] & b[i]  # @line L6
        wires.append((f"a{i}b{i}", acc))
        for j in range(n):  # @line L7
            if j != i:
                acc ^= rr[(i, j)]
                wires.append((f"c{i} after r{i}{j}", acc))
        c.append(acc)
    return c, wires  # @line L8


def isw_and(rng: random.Random, a: list[int], b: list[int]) -> list[int]:
    """Return n shares of AND(unshare(a), unshare(b)), with fresh random bits.

    Precondition: len(a) == len(b) == n >= 1. Cost: Theta(n^2).
    """
    n = len(a)
    if len(b) != n or n < 1:
        raise ValueError("the two sharings must have the same number n >= 1 of shares")
    r = {(i, j): rng.randrange(2) for i in range(n) for j in range(i + 1, n)}
    return isw_and_wires(a, b, r)[0]


def naive_and_wires(a: list[int], b: list[int]) -> tuple[list[int], list[Wire]]:
    """A wrong gadget with no randomness: c_i = XOR over j of a_i b_j.

    The output is a correct sharing of a AND b, but c_i = a_i AND b, which
    a single probe can read.
    """
    n = len(a)
    wires: list[Wire] = [(f"a{i}", a[i]) for i in range(n)] + [(f"b{i}", b[i]) for i in range(n)]
    c = []
    for i in range(n):
        acc = 0
        for j in range(n):
            acc ^= a[i] & b[j]
            wires.append((f"c{i} after a{i}b{j}", acc))
        c.append(acc)
    return c, wires


def wrong_order_wires(
    a: list[int], b: list[int], r: dict[tuple[int, int], int]
) -> tuple[list[int], list[Wire]]:
    """ISW with line L4 bracketed as r_ij xor (a_i b_j xor a_j b_i).

    The output is still correct, but the wire a_i b_j xor a_j b_i is not
    masked by r_ij.
    """
    n = len(a)
    wires: list[Wire] = [(f"a{i}", a[i]) for i in range(n)] + [(f"b{i}", b[i]) for i in range(n)]
    rr: dict[tuple[int, int], int] = {}
    for i in range(n):
        for j in range(i + 1, n):
            rr[(i, j)] = r[(i, j)]
            t = (a[i] & b[j]) ^ (a[j] & b[i])
            rr[(j, i)] = rr[(i, j)] ^ t
            wires += [(f"r{i}{j}", rr[(i, j)]), (f"a{i}b{j}+a{j}b{i}", t), (f"r{j}{i}", rr[(j, i)])]
    c = []
    for i in range(n):
        acc = a[i] & b[i]
        for j in range(n):
            if j != i:
                acc ^= rr[(i, j)]
                wires.append((f"c{i} after r{i}{j}", acc))
        c.append(acc)
    return c, wires


Gate = tuple[str, int, int]


def eval_plain(gates: list[Gate], inputs: list[int]) -> int:
    """Evaluate a circuit of ("xor"|"and", i, j) and ("not", i, 0) gates on bits.

    Wire k < len(inputs) is input k; gate g writes wire len(inputs) + g.
    The result is the last wire. Cost: Theta(len(inputs) + len(gates)).
    """
    w = list(inputs)
    for op, i, j in gates:
        if op == "xor":
            w.append(w[i] ^ w[j])
        elif op == "and":
            w.append(w[i] & w[j])
        else:
            w.append(w[i] ^ 1)
    return w[-1]


def eval_masked(rng: random.Random, gates: list[Gate], inputs: list[list[int]]) -> list[int]:
    """Evaluate the same circuit on sharings with n shares each.

    XOR works share by share, NOT flips the first share, and AND is the ISW
    gadget. Returns the n shares of the result.
    Cost: Theta(n) for each XOR or NOT gate and Theta(n^2) for each AND gate.
    """
    w = [list(s) for s in inputs]
    for op, i, j in gates:
        if op == "xor":
            w.append([x ^ y for x, y in zip(w[i], w[j])])
        elif op == "and":
            w.append(isw_and(rng, w[i], w[j]))
        else:
            w.append([w[i][0] ^ 1] + w[i][1:])
    return w[-1]
