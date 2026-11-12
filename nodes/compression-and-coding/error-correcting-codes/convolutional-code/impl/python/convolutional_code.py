# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convolutional-code/. The authors are listed in prov/F34YG7.jsonl.

"""Binary rate 1/n feedforward and recursive systematic convolutional encoders.

Conventions. K is the constraint length, K = m + 1 where m is the encoder
memory, so the encoder has 2^(K-1) states. A generator is written in octal,
and its K-bit binary form lists the taps from D^0 (the leftmost bit) to
D^(K-1) (the rightmost bit). So 7 = 111 is 1 + D + D^2 and 5 = 101 is 1 + D^2.
The state holds the last K - 1 inputs; bit K-2 is the newest one.
"""

import heapq
from typing import Dict, List, Sequence, Tuple


def octal_taps(g: str) -> int:
    """The generator in octal as an integer mask, bit K-1 for D^0."""
    return int(g, 8)


def step(state: int, u: int, gens: Sequence[int], k: int) -> Tuple[int, Tuple[int, ...]]:
    """One clock of the feedforward encoder: return (next state, output bits)."""
    window = (u << (k - 1)) | state
    out = tuple(bin(g & window).count("1") & 1 for g in gens)
    return window >> 1, out


def encode(bits: Sequence[int], gens: Sequence[int], k: int, terminate: bool = True) -> List[int]:
    """Encode the bits with a rate 1/n feedforward encoder.

    With terminate, K - 1 zeros flush the register back to state 0.
    Cost: O((L + K) n) for L input bits and n generators.
    """
    state = 0
    out: List[int] = []
    tail = [0] * (k - 1) if terminate else []
    for u in list(bits) + tail:
        state, o = step(state, u, gens, k)
        out.extend(o)
    return out


def free_distance(gens: Sequence[int], k: int) -> int:
    """The free distance: the least output weight of a path that leaves state 0
    and later returns to it. Dijkstra on the state diagram, O(2^K log 2^K)."""
    s1, o = step(0, 1, gens, k)
    if s1 == 0:
        return sum(o)
    dist: Dict[int, int] = {s1: sum(o)}
    heap = [(sum(o), s1)]
    while heap:
        d, s = heapq.heappop(heap)
        if s == 0:
            return d
        if d > dist.get(s, 1 << 60):
            continue
        for u in (0, 1):
            t, o = step(s, u, gens, k)
            nd = d + sum(o)
            if nd < dist.get(t, 1 << 60):
                dist[t] = nd
                heapq.heappush(heap, (nd, t))
    raise ValueError("no path returns to state 0")


def weight_spectrum(gens: Sequence[int], k: int, dmax: int, max_steps: int = 10000) -> Dict[int, Tuple[int, int]]:
    """For each output weight d <= dmax: (A_d, B_d), the number of first-event
    paths of weight d and the total input weight of those paths. The encoder
    must be non-catastrophic, so that every long path has a large weight."""
    spec: Dict[int, List[int]] = {}
    s1, o = step(0, 1, gens, k)
    live: Dict[Tuple[int, int, int], int] = {}
    if sum(o) <= dmax:
        live[(s1, sum(o), 1)] = 1
    for _ in range(max_steps):
        if not live:
            return {d: (a, b) for d, (a, b) in sorted(spec.items())}
        nxt: Dict[Tuple[int, int, int], int] = {}
        for (s, w, iw), cnt in live.items():
            if s == 0:
                e = spec.setdefault(w, [0, 0])
                e[0] += cnt
                e[1] += cnt * iw
                continue
            for u in (0, 1):
                t, o = step(s, u, gens, k)
                nw = w + sum(o)
                if nw <= dmax:
                    key = (t, nw, iw + u)
                    nxt[key] = nxt.get(key, 0) + cnt
        live = nxt
    raise ValueError("the encoder looks catastrophic: paths of bounded weight never end")


def _poly_from_taps(g: int, k: int) -> int:
    """Convert a tap mask (bit K-1 = D^0) to a polynomial (bit j = D^j)."""
    return sum(1 << j for j in range(k) if (g >> (k - 1 - j)) & 1)


def _gf2_mod(a: int, b: int) -> int:
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def gf2_gcd(a: int, b: int) -> int:
    """The gcd of two polynomials over GF(2), as bit masks with bit j = D^j."""
    while b:
        a, b = b, _gf2_mod(a, b)
    return a


def is_catastrophic(gens: Sequence[int], k: int) -> bool:
    """Massey and Sain (1968) for rate 1/n: the encoder is catastrophic exactly
    when the gcd of its generator polynomials is not a power of D."""
    g = 0
    for x in gens:
        g = gf2_gcd(g, _poly_from_taps(x, k))
    return g & (g - 1) != 0


def puncture(coded: Sequence[int], pattern: Sequence[Sequence[int]]) -> List[int]:
    """Delete coded bits by a puncturing matrix with n rows and P columns.
    pattern[j][t % P] == 1 keeps output j of time t."""
    n, p = len(pattern), len(pattern[0])
    return [c for i, c in enumerate(coded) if pattern[i % n][(i // n) % p]]


def depuncture(received: Sequence[float], pattern: Sequence[Sequence[int]], length: int, fill: float = 0.0) -> List[float]:
    """Put the received values back at their places; fill the deleted places
    with a neutral value (an LLR of 0 means no information)."""
    n, p = len(pattern), len(pattern[0])
    it = iter(received)
    return [next(it) if pattern[i % n][(i // n) % p] else fill for i in range(length)]


def rsc_encode(bits: Sequence[int], fb: int, ff: int, k: int) -> List[Tuple[int, int]]:
    """Recursive systematic encoder with transfer function (1, ff(D)/fb(D)).

    fb and ff are tap masks in the same octal convention; fb must have its D^0
    tap. Returns (systematic bit, parity bit) for each input bit, no tail.
    """
    state = 0
    out: List[Tuple[int, int]] = []
    for u in bits:
        a = (u + bin(fb & state).count("1")) & 1
        window = (a << (k - 1)) | state
        out.append((u, bin(ff & window).count("1") & 1))
        state = window >> 1
    return out
