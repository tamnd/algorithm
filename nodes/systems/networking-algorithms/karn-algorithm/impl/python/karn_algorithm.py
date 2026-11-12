# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karn-algorithm/. The authors are listed in prov/ZDWFE6.jsonl.

"""Karn's algorithm: RTT sampling and timer backoff for a reliable sender.

KarnTimer wraps the RFC 6298 estimator (SRTT, RTTVAR, RTO). Its two rules:
1. Take no RTT sample from a segment that was retransmitted, because the
   sender cannot tell which copy the ACK answers.
2. On a timeout, double the RTO, and keep the doubled value until a segment
   that was sent only once is acknowledged and gives a valid sample.
simulate() runs a one-segment-at-a-time sender over a path whose RTT the
caller chooses, and it can also run the naive rules for comparison.
"""

from fractions import Fraction
from numbers import Rational
from typing import NamedTuple


class Estimator:
    """SRTT, RTTVAR and RTO as in RFC 6298, Section 2 (K = 4, G = 0)."""

    def __init__(self, min_rto: Rational = Fraction(1), max_rto: Rational = Fraction(60)) -> None:
        self.min_rto, self.max_rto = min_rto, max_rto
        self.srtt: Rational | None = None
        self.rttvar: Rational = Fraction(0)
        self.rto: Rational = Fraction(1)

    def sample(self, r: Rational) -> None:
        if self.srtt is None:
            self.srtt, self.rttvar = r, r / 2
        else:
            self.rttvar = Fraction(3, 4) * self.rttvar + abs(self.srtt - r) / 4
            self.srtt = Fraction(7, 8) * self.srtt + r / 8
        self.rto = min(self.max_rto, max(self.min_rto, self.srtt + 4 * self.rttvar))

    def back_off(self) -> None:
        self.rto = min(self.max_rto, 2 * self.rto)


class KarnTimer:
    """Karn's algorithm on top of the estimator.

    mode "karn" is the algorithm. The modes "first" and "last" are the naive
    rules that it replaces: they sample every ACK, measured from the first or
    from the last transmission of the segment, and so they also recompute RTO
    (and undo the backoff) on every ACK.
    """

    def __init__(self, mode: str = "karn", estimator: Estimator | None = None) -> None:
        if mode not in ("karn", "first", "last"):
            raise ValueError("mode is karn, first or last")
        self.mode = mode
        self.est = estimator if estimator is not None else Estimator()
        self.first_sent: dict[int, Rational] = {}
        self.last_sent: dict[int, Rational] = {}
        self.retransmitted: set[int] = set()

    @property
    def rto(self) -> Rational:
        return self.est.rto

    def on_send(self, seg: int, now: Rational) -> None:
        if seg in self.first_sent:
            self.retransmitted.add(seg)  # @line L2
        else:
            self.first_sent[seg] = now  # @line L1
        self.last_sent[seg] = now

    def on_timeout(self, seg: int) -> None:
        self.est.back_off()  # @line L3

    def on_ack(self, seg: int, now: Rational) -> Rational | None:  # @line L4
        """Return the RTT sample taken, or None."""
        if self.mode == "karn":
            if seg in self.retransmitted:  # @line L5
                return None  # @line L7
            r = now - self.first_sent[seg]
        else:
            r = now - (self.first_sent[seg] if self.mode == "first" else self.last_sent[seg])
        self.est.sample(r)  # @line L6
        return r


class Segment(NamedTuple):
    sent: int  # number of transmissions
    sample: Rational | None
    rto_after: Rational


def simulate(
    rtts: list[Rational],
    mode: str = "karn",
    lost: frozenset[tuple[int, int]] = frozenset(),
    estimator: Estimator | None = None,
    max_copies: int = 30,
) -> list[Segment]:
    """Send segment i only after segment i - 1 is acknowledged.

    Copy c of segment i, sent at time s, is answered by an ACK at s + rtts[i],
    unless (i, c) is in lost. The sender acts on the first ACK that arrives,
    and it cannot tell which copy that ACK answers. A timer expiry at the
    same instant as an ACK loses to the ACK.
    """
    timer = KarnTimer(mode, estimator)
    now: Rational = Fraction(0)
    out = []
    for i, rtt in enumerate(rtts):
        sends = [now]
        timer.on_send(i, now)
        while True:
            arrivals = [s + rtt for c, s in enumerate(sends) if (i, c) not in lost]
            first_ack = min(arrivals) if arrivals else None
            expiry = sends[-1] + timer.rto
            if first_ack is not None and first_ack <= expiry:
                now = first_ack
                break
            if len(sends) >= max_copies:
                raise RuntimeError("too many retransmissions")
            timer.on_timeout(i)
            sends.append(expiry)
            timer.on_send(i, expiry)
        sample = timer.on_ack(i, now)
        out.append(Segment(len(sends), sample, timer.rto))
    return out
