# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/outer-loop-link-adaptation/. The authors are listed in prov/ZM1GV1.jsonl.

"""Outer loop link adaptation (OLLA).

The receiver reports an SINR estimate in dB. The inner loop maps the report to
the fastest modulation and coding scheme whose threshold it meets. The outer
loop keeps a backoff offset in dB that is subtracted from each report before
the lookup. On each NACK the offset grows by step_up; on each ACK it shrinks by
step_down = step_up * target / (1 - target). If the offset stays bounded, the
fraction of NACKs tends to the target.
"""

import bisect


def step_down_for(step_up, target):
    """The down step that makes the target the balance point of the loop."""
    if not step_up > 0:
        raise ValueError("step_up must be positive")
    if not 0 < target < 1:
        raise ValueError("target must be in (0, 1)")
    return step_up * target / (1 - target)


def select_scheme(thresholds, snr_db):
    """Index of the largest threshold <= snr_db, or 0 if none (thresholds increase)."""
    return max(bisect.bisect_right(thresholds, snr_db) - 1, 0)


class OuterLoop:
    """The OLLA state: one offset, two steps and optional bounds."""

    def __init__(self, step_up, target, offset=0.0, lower=None, upper=None):
        self.step_up = step_up
        self.step_down = step_down_for(step_up, target)  # @line L1
        self.offset = offset
        self.lower, self.upper = lower, upper

    def choose(self, thresholds, report_db):
        adjusted = report_db - self.offset  # @line L3
        return select_scheme(thresholds, adjusted)  # @line L4

    def update(self, ack):
        if not ack:  # @line L6
            self.offset += self.step_up
        else:  # @line L7
            self.offset -= self.step_down
        if self.lower is not None and self.offset < self.lower:  # @line L8
            self.offset = self.lower
        if self.upper is not None and self.offset > self.upper:
            self.offset = self.upper
        return self.offset


def olla(thresholds, reports, feedback, step_up, target, offset=0.0, lower=None, upper=None):
    """Run the loop over a sequence of reports.

    feedback(n, scheme) returns True for an ACK and False for a NACK of
    transmission n sent with the given scheme. Returns (schemes, offsets, nacks),
    where offsets[n] is the offset after transmission n.
    """
    loop = OuterLoop(step_up, target, offset, lower, upper)
    schemes, offsets, nacks = [], [], 0
    for n, report in enumerate(reports):  # @line L2
        j = loop.choose(thresholds, report)
        ack = feedback(n, j)  # @line L5
        nacks += not ack
        loop.update(ack)
        schemes.append(j)
        offsets.append(loop.offset)
    return schemes, offsets, nacks
