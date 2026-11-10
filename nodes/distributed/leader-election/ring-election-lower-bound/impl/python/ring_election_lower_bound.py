# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ring-election-lower-bound/. The authors are listed in prov/6S7ZTH.jsonl.

"""Checks for the Omega(n log n) lower bounds on ring election.

bit_reversal_ring and min_equivalent_count check the counting lemma of the
synchronous proof. burns_bound is the recurrence of the asynchronous proof.
lcr_sync runs a comparison-based algorithm on a synchronous ring, so the
tests can compare its message count with the bound. time_slice is the
non-comparison algorithm that uses only n messages.
"""

from collections import Counter


def bit_reversal_ring(n: int) -> list[int]:
    """Identifiers of the bit-reversal ring: p_i gets i with its bits reversed."""
    m = n.bit_length() - 1
    assert n == 1 << m, "n must be a power of 2"
    return [int(format(i, "0%db" % m)[::-1], 2) if m else 0 for i in range(n)]


def order_pattern(ids: list[int], a: int, length: int) -> tuple:
    """The order type of the segment of the given length that starts at p_a."""
    n = len(ids)
    seg = [ids[(a + t) % n] for t in range(length)]
    return tuple(sorted(range(length), key=lambda t: seg[t]))


def min_equivalent_count(ids: list[int], length: int) -> int:
    """The least number of segments order-equivalent to one segment."""
    counts = Counter(order_pattern(ids, a, length) for a in range(len(ids)))
    return min(counts.values())


def lemma_count(n: int, length: int) -> int:
    """n / 2^j for the least j with 2^j >= length: the count the lemma proves."""
    j = (length - 1).bit_length()
    return n >> j


def sync_bound(n: int) -> int:
    """Messages forced by the synchronous proof: the sum over active rounds."""
    total = 0
    for k in range(1, n // 4 + 1):
        total += lemma_count(n, 2 * k - 1)
    return total


def burns_bound(n: int) -> int:
    """T(2) = 1 and T(n) = 2 T(n/2) + n/4: the open-run recurrence."""
    if n == 2:
        return 1
    return 2 * burns_bound(n // 2) + n // 4


def lcr_sync(ids: list[int]) -> tuple[int, int]:
    """LCR in lock-step rounds on a unidirectional ring; return (messages, rounds)."""
    n = len(ids)
    inbox = list(ids)  # the id each process sends in round 1
    messages = 0
    rounds = 0
    leader = None
    while any(x is not None for x in inbox):
        rounds += 1
        sent = inbox
        messages += sum(1 for x in sent if x is not None)
        inbox = [None] * n
        for i in range(n):
            x = sent[(i - 1) % n]
            if x is None:
                continue
            if x > ids[i]:
                inbox[i] = x
            elif x == ids[i]:
                leader = i
    assert leader is not None and ids[leader] == max(ids)
    return messages, rounds


def time_slice(ids: list[int]) -> tuple[int, int, int]:
    """TimeSlice on a synchronous unidirectional ring of known size n.

    Identifiers are positive integers. Phase v has rounds (v-1)n+1 .. vn. If
    no message has been seen, the process with identifier v sends it at the
    start of phase v. Return (leader index, messages, rounds).
    """
    n = len(ids)
    u = min(ids)
    return ids.index(u), n, u * n


def time_slice_run(ids: list[int]) -> tuple[int, int, int]:
    """The same algorithm, run round by round, to check time_slice."""
    n = len(ids)
    seen = [False] * n
    inbox = [None] * n
    messages = 0
    r = 0
    while True:
        r += 1
        out = [None] * n
        for i in range(n):
            if inbox[i] is not None:
                if inbox[i] == ids[i]:
                    return i, messages, r - 1
                out[i] = inbox[i]
            elif not seen[i] and r == (ids[i] - 1) * n + 1:
                out[i] = ids[i]
        inbox = [None] * n
        for i in range(n):
            if out[i] is not None:
                messages += 1
                inbox[(i + 1) % n] = out[i]
                seen[(i + 1) % n] = True
