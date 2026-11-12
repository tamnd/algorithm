# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bbr-congestion-control/. The authors are listed in prov/BBWT9S.jsonl.

"""A model of BBR version 1 (Cardwell et al., 2016): the state machine,
the two estimates and the pacing rule. It is not the Linux code. A round
model of one bottleneck link drives it: rates are packets per second, times
are seconds, and each round lasts one round-trip time.
"""

import math
from collections import deque
from dataclasses import dataclass, field

HIGH_GAIN = 2 / math.log(2)  # about 2.885, the STARTUP gain
DRAIN_GAIN = math.log(2) / 2  # 1 / HIGH_GAIN
GAINS = [1.25, 0.75, 1, 1, 1, 1, 1, 1]  # the PROBE_BW gain cycle
BW_WINDOW = 10  # rounds kept by the BtlBw max filter
RTPROP_WINDOW = 10.0  # seconds kept by the RTprop min filter
PROBE_RTT_TIME = 0.2  # seconds spent in PROBE_RTT
MIN_CWND = 4  # packets in flight during PROBE_RTT


class BBR:
    """BBR state for one sender. on_round runs once per round trip."""

    def __init__(self, init_rate: float, init_rtt: float, phase: int = 2) -> None:
        self.state = "STARTUP"
        self.btl_bw = init_rate
        self.samples: deque[float] = deque(maxlen=BW_WINDOW)
        self.rt_prop = init_rtt
        self.rt_prop_stamp = 0.0
        self.full_bw = 0.0
        self.full_bw_count = 0
        self.filled_pipe = False
        self.start_phase = phase
        self.phase = phase
        self.probe_rtt_done = 0.0
        self.pacing_gain = HIGH_GAIN
        self.cwnd_gain = HIGH_GAIN
        self._set_controls()

    def bdp(self) -> float:
        return self.btl_bw * self.rt_prop

    def _set_controls(self) -> None:
        self.pacing_rate = self.pacing_gain * self.btl_bw  # @line L8
        if self.state == "PROBE_RTT":
            self.cwnd = float(MIN_CWND)
        else:
            self.cwnd = max(self.cwnd_gain * self.bdp(), float(MIN_CWND))  # @line L9

    def on_round(self, delivery_rate: float, rtt: float, now: float, inflight: float) -> None:
        """Update the model with the delivery rate and RTT of the last round."""
        self.samples.append(delivery_rate)
        self.btl_bw = max(self.samples)  # @line L1
        expired = now - self.rt_prop_stamp > RTPROP_WINDOW
        if rtt <= self.rt_prop or expired:  # @line L2
            self.rt_prop = rtt
            self.rt_prop_stamp = now
        if self.state == "STARTUP":  # @line L3
            if self.btl_bw >= 1.25 * self.full_bw:
                self.full_bw = self.btl_bw
                self.full_bw_count = 0
            else:
                self.full_bw_count += 1
                if self.full_bw_count >= 3:
                    self.filled_pipe = True
                    self.state = "DRAIN"
        if self.state == "DRAIN" and inflight <= self.bdp():  # @line L4
            self.state = "PROBE_BW"
            self.phase = self.start_phase
        elif self.state == "PROBE_BW":  # @line L5
            self.phase = (self.phase + 1) % len(GAINS)
        if expired and self.state != "PROBE_RTT":  # @line L6
            self.state = "PROBE_RTT"
            self.probe_rtt_done = now + PROBE_RTT_TIME
        elif self.state == "PROBE_RTT" and now >= self.probe_rtt_done:
            self.rt_prop_stamp = now
            self.state = "PROBE_BW" if self.filled_pipe else "STARTUP"
        if self.state == "STARTUP":  # @line L7
            self.pacing_gain, self.cwnd_gain = HIGH_GAIN, HIGH_GAIN
        elif self.state == "DRAIN":
            self.pacing_gain, self.cwnd_gain = DRAIN_GAIN, HIGH_GAIN
        elif self.state == "PROBE_BW":
            self.pacing_gain, self.cwnd_gain = GAINS[self.phase], 2.0
        else:
            self.pacing_gain, self.cwnd_gain = 1.0, 1.0
        self._set_controls()


@dataclass
class Round:
    time: float
    state: str
    rate: float
    queue: float
    rtt: float
    btl_bw: float
    rt_prop: float


@dataclass
class Link:
    """One bottleneck: capacity c packets/s, propagation RTT d seconds,
    and a buffer of buffer packets (excess arrivals are dropped)."""

    c: float
    d: float
    buffer: float = float("inf")
    queue: float = 0.0
    log: list[Round] = field(default_factory=list)


def simulate(bbr: BBR, link: Link, rounds: int) -> list[Round]:
    """Drive one BBR flow over the link for a number of rounds.

    A round lasts T = d + queue / c. The sender sends at the pacing rate,
    limited so that the data in flight stays within cwnd. The link serves at
    most c * T packets; the rest stays in the queue. Cost O(rounds).
    """
    now = 0.0
    for _ in range(rounds):
        t_round = link.d + link.queue / link.c
        rate = min(bbr.pacing_rate, max(bbr.cwnd - link.queue, 0.0) / link.d)
        arriving = rate * t_round
        served = min(link.queue + arriving, link.c * t_round)
        link.queue = min(link.queue + arriving - served, link.buffer)
        delivery_rate = served / t_round
        now += t_round
        inflight = link.queue + rate * link.d
        link.log.append(Round(now, bbr.state, delivery_rate, link.queue, t_round, bbr.btl_bw, bbr.rt_prop))
        bbr.on_round(delivery_rate, t_round, now, inflight)
    return link.log
