# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitstate-hashing/. The authors are listed in prov/0JT58E.jsonl.

"""Bitstate hashing (Holzmann's supertrace): a depth-first search whose visited set is a bit array.

A state is marked by setting k bits, chosen by k hash functions into an array
of m bits. A state counts as visited when all of its k bits are set. Two
different states can share all k bits; then the second one is wrongly taken as
visited and its successors may be lost. So the search can miss states, but it
never reports a state that is not reachable. Memory is m bits, whatever the
size of a state.

The k hash values come from one BLAKE2b digest of repr(state), cut into k
pieces of 8 bytes; the salt picks a different family of hash functions.
"""

import hashlib
from collections.abc import Callable, Hashable, Iterable


def hashes(state: Hashable, m: int, k: int, salt: bytes = b"") -> list[int]:
    """k positions in range(m) for state."""
    d = hashlib.blake2b(repr(state).encode(), digest_size=8 * k, salt=salt.ljust(16, b"\0")[:16]).digest()
    return [int.from_bytes(d[8 * j : 8 * j + 8], "little") % m for j in range(k)]


def bitstate_hashing(
    init: Hashable,
    succ: Callable[[Hashable], Iterable[Hashable]],
    m: int,
    k: int = 1,
    salt: bytes = b"",
) -> list:
    """The states that the bitstate search explores, in the order it finds them."""
    bits = bytearray((m + 7) // 8)

    def test_and_set(s) -> bool:
        """Set the bits of s; return True when they were all set already."""
        seen = True
        for h in hashes(s, m, k, salt):  # @line L6
            byte, bit = h >> 3, 1 << (h & 7)
            if not bits[byte] & bit:
                seen = False
                bits[byte] |= bit  # @line L7
        return seen

    test_and_set(init)  # @line L1
    order = [init]
    stack = [iter(succ(init))]  # @line L2
    while stack:  # @line L3
        t = next(stack[-1], None)
        if t is None:
            stack.pop()
            continue
        if test_and_set(t):  # @line L4
            continue
        order.append(t)
        stack.append(iter(succ(t)))  # @line L5
    return order


def exact_search(init, succ) -> set:
    """Plain search with an exact visited set: the oracle."""
    seen, todo = {init}, [init]
    while todo:
        s = todo.pop()
        for t in succ(s):
            if t not in seen:
                seen.add(t)
                todo.append(t)
    return seen


def no_collision_bound(n: int, m: int, k: int) -> float:
    """Lower bound on P(n states all get a fresh bit) under uniform independent hashing.

    The j-th state is wrongly taken as visited only if all k of its bits are
    among the at most k (j - 1) bits set before; that has probability at most
    (k (j - 1) / m) ** k. A union bound over j gives the result.
    """
    return 1.0 - sum((k * (j - 1) / m) ** k for j in range(1, n + 1))
