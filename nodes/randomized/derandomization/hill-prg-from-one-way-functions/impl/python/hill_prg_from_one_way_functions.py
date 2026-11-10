# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hill-prg-from-one-way-functions/. The authors are listed in prov/4E8GV3.jsonl.

"""The easy case of HILL: a generator from a permutation and the Goldreich-Levin bit.

A permutation f of {0,1}^n is a list of length 2^n. A string x in {0,1}^n is an int
whose bit j is x_j. The code shows the structure of the Blum-Micali-Yao generator
with the Goldreich-Levin bit. It is not secure: no small permutation is one-way.
"""

from fractions import Fraction
from typing import Callable, List, Sequence, Tuple

Bits = Tuple[int, ...]


def inner(x: int, r: int) -> int:
    """The Goldreich-Levin bit <x, r> = sum_j x_j r_j mod 2."""
    return bin(x & r).count("1") & 1


def to_bits(v: int, n: int) -> Bits:
    """Bits v_0, ..., v_(n-1) of v."""
    return tuple((v >> j) & 1 for j in range(n))


def from_bits(b: Sequence[int]) -> int:
    return sum(bit << j for j, bit in enumerate(b))


def is_permutation(f: Sequence[int]) -> bool:
    return sorted(f) == list(range(len(f)))


def one_step(f: Sequence[int], n: int, x: int, r: int) -> Bits:
    """The stretch-one generator G(x, r) = (f(x), r, <x, r>) from 2n to 2n + 1 bits."""
    return to_bits(f[x], n) + to_bits(r, n) + (inner(x, r),)


def bmy(f: Sequence[int], n: int, x: int, r: int, ell: int) -> Bits:
    """The Blum-Micali-Yao generator with the Goldreich-Levin bit.

    Output: (f^ell(x), r, b_1, ..., b_ell) with b_i = <f^(i-1)(x), r>.
    The seed has 2n bits and the output has 2n + ell bits."""
    bits = []
    for _ in range(ell):
        bits.append(inner(x, r))
        x = f[x]
    return to_bits(x, n) + to_bits(r, n) + tuple(bits)


def stretch_extension(g: Callable[[Bits], Bits], seed: Bits, ell: int) -> Bits:
    """Iterate a stretch-one generator g: N -> N + 1 bits ell times.

    Each step outputs the last bit of g and keeps the first N bits as the new state.
    Output: (final state, b_1, ..., b_ell)."""
    state = tuple(seed)
    out = []
    for _ in range(ell):
        y = g(state)
        out.append(y[-1])
        state = y[:-1]
    return state + tuple(out)


def linear_permutation(rows: Sequence[int], n: int) -> List[int]:
    """The table of x -> Ax over GF(2), where bit j of Ax is <rows[j], x>."""
    return [from_bits([inner(row, x) for row in rows]) for x in range(2**n)]


def rank_gf2(vectors: Sequence[int]) -> int:
    basis: List[int] = []
    for v in vectors:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
    return len(basis)


def dependency(vectors: Sequence[int]) -> int:
    """A nonempty set S (as a bit mask of indices) with XOR of vectors[i], i in S, equal to 0.

    Returns 0 if the vectors are independent."""
    basis: List[Tuple[int, int]] = []
    for i, v in enumerate(vectors):
        mask = 1 << i
        for b, bm in basis:
            if v ^ b < v:
                v, mask = v ^ b, mask ^ bm
        if v == 0:
            return mask
        basis.append((v, mask))
        basis.sort(reverse=True)
    return 0


def linear_attack_test(rows: Sequence[int], n: int, ell: int) -> Callable[[Bits], int]:
    """A test that breaks bmy when f is the linear map given by rows and ell > n.

    b_i = <A^(i-1) x, r> = <x, v_i> with v_i = (A^T)^(i-1) r, so n + 1 of the
    bits satisfy a linear relation that the test can find from r."""

    def transpose_apply(r: int) -> int:
        out = 0
        for j in range(n):
            if (r >> j) & 1:
                out ^= rows[j]
        return out

    def test(z: Bits) -> int:
        r = from_bits(z[n : 2 * n])
        b = z[2 * n :]
        vs = []
        v = r
        for _ in range(ell):
            vs.append(v)
            v = transpose_apply(v)
        s = dependency(vs)
        parity = 0
        for i in range(ell):
            if (s >> i) & 1:
                parity ^= b[i]
        return 1 if parity == 0 else 0

    return test


def advantage_on_bmy(f: Sequence[int], n: int, ell: int, test: Callable[[Bits], int]) -> Fraction:
    """Exact Pr[test(bmy(U_2n)) = 1] - Pr[test(U_(2n+ell)) = 1]."""
    hits_gen = sum(test(bmy(f, n, x, r, ell)) for x in range(2**n) for r in range(2**n))
    hits_uni = sum(test(to_bits(z, 2 * n + ell)) for z in range(2 ** (2 * n + ell)))
    return Fraction(hits_gen, 4**n) - Fraction(hits_uni, 2 ** (2 * n + ell))
