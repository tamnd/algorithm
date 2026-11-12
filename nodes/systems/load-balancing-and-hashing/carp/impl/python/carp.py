# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carp/. The authors are listed in prov/VTZKC2.jsonl.

"""The Cache Array Routing Protocol (CARP), draft-vinod-carp-v1-03, Section 3.

All hash arithmetic is on 32-bit unsigned integers. A request goes to the
member with the highest score, the combined hash of the URL and the member
times the load factor multiplier of the member.
"""

from collections.abc import Sequence

MASK = 0xFFFFFFFF


def rotl(x: int, r: int) -> int:
    x &= MASK
    return ((x << r) | (x >> (32 - r))) & MASK


def url_hash(url: str) -> int:
    """Section 3.1: for each character, hash += ROTL(hash, 19) + character."""
    h = 0
    for ch in url.encode():
        h = (h + rotl(h, 19) + ch) & MASK
    return h


def member_hash(name: str) -> int:
    """Section 3.1: the same loop over the member name, then a multiply and a rotation."""
    h = url_hash(name)
    h = (h + h * 0x62531965) & MASK
    return rotl(h, 21)


def combined_hash(u: int, m: int) -> int:
    """Section 3.2: combine the URL hash and the member hash."""
    c = u ^ m
    c = (c + c * 0x62531965) & MASK
    return rotl(c, 21)


def multipliers(loads: Sequence[float]) -> list[float]:
    """Section 3.3: the load factor multipliers X_k for load factors that sum to 1.

    The factors are processed in ascending order, and the result is returned
    in the order of the input.
    """
    k_total = len(loads)
    if abs(sum(loads) - 1) > 1e-9 or min(loads) <= 0:
        raise ValueError("load factors must be positive and sum to 1")
    order = sorted(range(k_total), key=lambda i: loads[i])
    out = [0.0] * k_total
    product, x_last, p_last = 1.0, 0.0, 0.0
    for k, i in enumerate(order, start=1):
        e = k_total - k + 1
        x = (e * (loads[i] - p_last)) / product + x_last ** e
        x = x ** (1.0 / e)
        out[i] = x
        product *= x
        x_last, p_last = x, loads[i]
    return out


class Carp:
    def __init__(self, members: Sequence[str], loads: Sequence[float] | None = None) -> None:
        self.members = list(members)
        if loads is None:
            loads = [1 / len(self.members)] * len(self.members)
        self.loads = list(loads)
        self.hm = [member_hash(m) for m in self.members]
        self.x = multipliers(self.loads)

    def route(self, url: str) -> str:
        u = 0  # @line L1
        for ch in url.encode():  # @line L2
            u = (u + rotl(u, 19) + ch) & MASK  # @line L3
        best, best_score = None, -1.0  # @line L4
        for k in range(len(self.members)):  # @line L5
            c = u ^ self.hm[k]  # @line L6
            c = (c + c * 0x62531965) & MASK  # @line L7
            c = rotl(c, 21)  # @line L8
            s = c * self.x[k]  # @line L9
            if s > best_score:  # @line L10
                best, best_score = k, s
        return self.members[best]  # @line L11


def exact_shares(x: Sequence[float]) -> list[float]:
    """The share of each member when the combined hashes are independent and uniform on (0, 1).

    Member k wins with score X_k u when every other member i has U_i < X_k u / X_i,
    so its share is the integral over u in (0, 1) of the product of
    min(1, X_k u / X_i). The product is a monomial between the breakpoints
    u = X_i / X_k, so the integral is exact.
    """
    out = []
    for k, xk in enumerate(x):
        others = sorted(xi for i, xi in enumerate(x) if i != k)
        total = 0.0
        lo = 0.0
        coef = 1.0  # product of xk / xi over the members still below 1
        active = list(others)
        for xi in active:
            coef *= xk / xi
        deg = len(active)
        # Breakpoints in increasing u: the member with the smallest X_i saturates first.
        for xi in others:
            hi = min(1.0, xi / xk)
            if hi > lo:
                total += coef * (hi ** (deg + 1) - lo ** (deg + 1)) / (deg + 1)
                lo = hi
            coef /= xk / xi
            deg -= 1
        if lo < 1.0:
            total += coef * (1.0 - lo ** (deg + 1)) / (deg + 1)
        out.append(total)
    return out
