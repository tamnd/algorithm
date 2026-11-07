# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kogge-stone-adder/. The authors are listed in prov/PABN90.jsonl.

"""The Kogge-Stone parallel-prefix adder, simulated gate by gate.

Bit lists are least significant bit first. The simulation keeps, for every
signal, its value and its depth (the number of gates on the longest path from
an input), and counts the gates, so that the size and depth of the circuit can
be checked as well as its output.
"""


class Stats:
    def __init__(self) -> None:
        self.gates = 0
        self.cells = 0
        self.levels = 0


def _and(x: tuple[int, int], y: tuple[int, int], st: Stats) -> tuple[int, int]:
    st.gates += 1
    return x[0] & y[0], max(x[1], y[1]) + 1


def _or(x: tuple[int, int], y: tuple[int, int], st: Stats) -> tuple[int, int]:
    st.gates += 1
    return x[0] | y[0], max(x[1], y[1]) + 1


def _xor(x: tuple[int, int], y: tuple[int, int], st: Stats) -> tuple[int, int]:
    st.gates += 1
    return x[0] ^ y[0], max(x[1], y[1]) + 1


def kogge_stone_add(a: list[int], b: list[int], c_in: int = 0, st: Stats | None = None) -> tuple[list[int], int]:
    """Add two n-bit lists; return the n + 1 sum bits (carry out last) and the depth."""
    if st is None:
        st = Stats()
    n = len(a)
    if len(b) != n:
        raise ValueError("the operands must have the same width")
    cin = (c_in & 1, 0)
    if n == 0:
        return [cin[0]], 0
    A = [(x & 1, 0) for x in a]
    B = [(x & 1, 0) for x in b]
    g = [_and(A[i], B[i], st) for i in range(n)]  # @line L1: generate and propagate bits
    p = [_xor(A[i], B[i], st) for i in range(n)]
    g[0] = _or(g[0], _and(p[0], cin, st), st)  # @line L2: fold the carry in into g[0]
    G, P = list(g), list(p)  # @line L3
    d = 1
    while d < n:  # @line L4: about log2 n levels
        newG, newP = list(G), list(P)
        for i in range(d, n):  # @line L5: (G, P)[i] <- (G, P)[i] o (G, P)[i - d], all i at once
            newG[i] = _or(G[i], _and(P[i], G[i - d], st), st)
            if i >= 2 * d:  # P is needed only while the span has not reached position 0
                newP[i] = _and(P[i], P[i - d], st)
            st.cells += 1
        G, P = newG, newP
        st.levels += 1
        d *= 2  # @line L6
    c = [cin] + G  # @line L7: c[i + 1] = G[i], the carry out of position i
    s = [_xor(p[i], c[i], st) for i in range(n)]  # @line L8
    out = s + [c[n]]
    return [x[0] for x in out], max(x[1] for x in out)  # @line L9


def kogge_stone_word(a: int, b: int, n: int, c_in: int = 0) -> int:
    """The same prefix computation with machine-word operations on n-bit integers.

    Each round combines every position i with position i - d at once, as the
    circuit does, by shifting the whole words G and P by d.
    """
    mask = (1 << n) - 1
    a &= mask
    b &= mask
    g = a & b
    p = a ^ b
    G = g | (p & c_in & 1)
    P = p
    d = 1
    while d < n:
        G = G | (P & (G << d))
        P = P & (P << d)
        G &= mask
        P &= mask
        d *= 2
    carries = ((G << 1) | (c_in & 1)) & ((1 << (n + 1)) - 1)
    return (p ^ carries) & mask | (carries >> n) << n


def to_bits(x: int, n: int) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def from_bits(s: list[int]) -> int:
    return sum(bit << i for i, bit in enumerate(s))


def add_limbs(a: list[int], b: list[int], w: int = 8, c_in: int = 0) -> list[int]:
    """Add two limb arrays in radix 2**w with one Kogge-Stone adder of their full width.

    Returns len + 1 limbs; the last limb is the carry out (0 or 1).
    """
    n = max(len(a), len(b))
    a = list(a) + [0] * (n - len(a))
    b = list(b) + [0] * (n - len(b))
    abits = [(a[i // w] >> (i % w)) & 1 for i in range(n * w)]
    bbits = [(b[i // w] >> (i % w)) & 1 for i in range(n * w)]
    s, _ = kogge_stone_add(abits, bbits, c_in)
    out = [0] * (n + 1)
    for i, bit in enumerate(s):
        out[i // w] |= bit << (i % w)
    return out
