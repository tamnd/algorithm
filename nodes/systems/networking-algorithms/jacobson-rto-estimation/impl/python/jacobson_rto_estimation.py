# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobson-rto-estimation/. The authors are listed in prov/CNHXD2.jsonl.

"""Jacobson's retransmission timeout, as specified in RFC 6298.

SRTT is an exponentially weighted moving average of the round-trip time
samples, RTTVAR is the same kind of average of the absolute deviation
|SRTT - R|, and RTO = SRTT + max(G, K * RTTVAR). All times are in seconds.
Pass Fraction values to get exact results.
"""

from fractions import Fraction
from numbers import Rational


class JacobsonRto:
    """The RTO estimator of RFC 6298, Section 2, with the backoff of Section 5.

    granularity is the clock granularity G. min_rto is the lower bound of
    rule 2.4 (1 second); set it to 0 to see the raw formula. max_rto is the
    upper bound of rule 2.5 (at least 60 seconds), or None for no bound.
    """

    def __init__(
        self,
        granularity: Rational = Fraction(0),
        k: int = 4,
        alpha: Rational = Fraction(1, 8),
        beta: Rational = Fraction(1, 4),
        initial_rto: Rational = Fraction(1),
        min_rto: Rational = Fraction(1),
        max_rto: Rational | None = Fraction(60),
    ) -> None:
        self.g, self.k, self.alpha, self.beta = granularity, k, alpha, beta
        self.min_rto, self.max_rto = min_rto, max_rto
        self.srtt: Rational | None = None
        self.rttvar: Rational | None = None
        self.rto: Rational = self._clamp(initial_rto)  # @line L1

    def _clamp(self, rto: Rational) -> Rational:
        rto = max(rto, self.min_rto)  # @line L8
        if self.max_rto is not None:
            rto = min(rto, self.max_rto)
        return rto

    def sample(self, r: Rational) -> Rational:
        """Take one RTT sample r (from a segment that was not retransmitted)."""
        if r < 0:
            raise ValueError("an RTT sample cannot be negative")
        if self.srtt is None or self.rttvar is None:  # @line L2
            self.srtt = r  # @line L3
            self.rttvar = r / 2  # @line L4
        else:
            # RTTVAR first: it uses the SRTT from before this sample.
            self.rttvar = (1 - self.beta) * self.rttvar + self.beta * abs(self.srtt - r)  # @line L5
            self.srtt = (1 - self.alpha) * self.srtt + self.alpha * r  # @line L6
        self.rto = self._clamp(self.srtt + max(self.g, self.k * self.rttvar))  # @line L7
        return self.rto

    def back_off(self) -> Rational:
        """The retransmission timer expired: double the RTO (rule 5.5)."""
        self.rto = self._clamp(2 * self.rto)  # @line L9
        return self.rto
