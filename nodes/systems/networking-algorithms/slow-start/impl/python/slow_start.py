# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slow-start/. The authors are listed in prov/VM5NDN.jsonl.

"""Slow start and congestion avoidance, with the window in bytes, as in
RFC 5681, Section 3.1. The initial window follows RFC 5681, RFC 3390 or
RFC 6928. A round model counts the window at the start of each round trip.
"""

LARGE = 2**30  # "arbitrarily high" initial ssthresh (RFC 5681)


def iw_rfc5681(smss: int) -> int:
    """The upper bound on the initial window in RFC 5681, Section 3.1."""
    if smss > 2190:
        return 2 * smss
    if smss > 1095:
        return 3 * smss
    return 4 * smss


def iw_rfc3390(mss: int) -> int:
    """The upper bound on the initial window in RFC 3390."""
    return min(4 * mss, max(2 * mss, 4380))


def iw_rfc6928(mss: int) -> int:
    """The experimental initial window of RFC 6928 (about ten segments)."""
    return min(10 * mss, max(2 * mss, 14600))


class SlowStart:
    """The congestion window of one TCP sender, in bytes.

    on_ack takes the number of newly acknowledged bytes; on_timeout takes
    FlightSize, the bytes sent and not yet acknowledged. Each call is O(1).
    """

    def __init__(self, smss: int, iw: int | None = None, ssthresh: int = LARGE) -> None:
        if smss <= 0:
            raise ValueError("smss must be positive")
        self.smss = smss
        self.cwnd = iw_rfc5681(smss) if iw is None else iw  # @line L1
        self.ssthresh = ssthresh

    def in_slow_start(self) -> bool:
        return self.cwnd < self.ssthresh

    def on_ack(self, n: int) -> None:
        """An ACK acknowledged n > 0 previously unacknowledged bytes."""
        if n <= 0:
            return
        if self.cwnd < self.ssthresh:  # @line L2
            self.cwnd += min(n, self.smss)  # @line L3
        else:  # @line L4
            self.cwnd += max(1, self.smss * self.smss // self.cwnd)  # @line L5

    def on_timeout(self, flight_size: int) -> None:
        """The retransmission timer expired with flight_size bytes outstanding."""
        self.ssthresh = max(flight_size // 2, 2 * self.smss)  # @line L6
        self.cwnd = self.smss  # @line L7


def rounds(cc: SlowStart, count: int, ack_every: int = 1) -> list[int]:
    """Window at the start of each of count round trips, with no loss.

    In each round the sender sends cwnd // smss full segments, and the
    receiver sends one ACK for every ack_every segments (ack_every = 2 is
    the delayed ACK of RFC 1122), plus one ACK for a last odd segment.
    """
    out = []
    for _ in range(count):
        out.append(cc.cwnd)
        segs = cc.cwnd // cc.smss
        while segs > 0:
            k = min(ack_every, segs)
            cc.on_ack(k * cc.smss)
            segs -= k
    return out
