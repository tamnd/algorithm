# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/health-checking/. The authors are listed in prov/K5FA12.jsonl.

"""Health checking for a load balancer: active probes with rise and fall
thresholds, passive outlier ejection, and a panic threshold.

Model: time is an integer clock. An active prober sends one probe to each
backend every `interval` ticks, at times 0, interval, 2 * interval, and so on.
A probe sent at time s sees the state of the backend at time s. A passing probe
reports at s; a failing probe reports at s + timeout (the prober waits for the
answer that never comes). Passive checks see the status code of each real
response. Nothing here opens a socket or reads a clock.
"""

from dataclasses import dataclass


class RiseFallChecker:
    """The state of one backend under active checks with hysteresis.

    A healthy backend becomes unhealthy after `fall` consecutive failed
    probes. An unhealthy backend becomes healthy after `rise` consecutive
    passed probes. A result that agrees with the current state resets the
    counter of opposite results.
    """

    def __init__(self, rise: int, fall: int, healthy: bool = False) -> None:
        if rise < 1 or fall < 1:
            raise ValueError("rise and fall must be at least 1")
        self.rise = rise
        self.fall = fall
        self.healthy = healthy
        self.streak = 0  # consecutive results that disagree with the state
        self.transitions = 0

    def observe(self, ok: bool) -> bool:
        """Record one probe result and return the new state."""
        if ok == self.healthy:  # @line L1
            self.streak = 0
            return self.healthy
        self.streak += 1  # @line L2
        if self.streak >= (self.fall if self.healthy else self.rise):  # @line L3
            self.healthy = ok  # @line L4
            self.streak = 0
            self.transitions += 1
        return self.healthy


def state_by_runs(results: list[bool], rise: int, fall: int, healthy: bool = False) -> bool:
    """Reference: the state after `results`, computed from maximal runs.

    Inside one run of equal results the counter only grows, so the state
    flips exactly when a run opposes the state and is at least as long as the
    threshold of the current state.
    """
    i = 0
    while i < len(results):
        j = i
        while j < len(results) and results[j] == results[i]:
            j += 1
        if results[i] != healthy and j - i >= (fall if healthy else rise):
            healthy = results[i]
        i = j
    return healthy


def detection_delay(fail_time: int, interval: int, timeout: int, fall: int) -> int:
    """Simulate probes and return the time from the failure of a healthy
    backend at `fail_time` until the prober marks it unhealthy.

    The backend is up before fail_time and down from fail_time on.
    """
    checker = RiseFallChecker(rise=1, fall=fall, healthy=True)
    s = 0
    while True:
        ok = s < fail_time
        if not checker.observe(ok):
            return s + timeout - fail_time
        s += interval


def detection_delay_formula(fail_time: int, interval: int, timeout: int, fall: int) -> int:
    """Closed form: the first probe at or after the failure, plus fall - 1
    more intervals, plus the timeout of the last probe."""
    first = -(-fail_time // interval) * interval
    return first + (fall - 1) * interval + timeout - fail_time


@dataclass
class _Host:
    consecutive_5xx: int = 0
    ejected_at: int = -1  # -1 when the host is not ejected
    ejection_time: int = 0
    multiplier: int = 0  # number of ejections not yet forgiven


class OutlierDetector:
    """Passive health checking by consecutive server errors.

    A host is ejected after `consecutive_5xx` server errors in a row, if the
    share of ejected hosts after the ejection stays at most
    `max_ejection_percent`. The k-th ejection in a row lasts
    min(k * base_ejection_time, max_ejection_time). A sweep every `interval`
    ticks returns hosts whose time is over, and lowers the multiplier of each
    host that is in service by one.
    """

    def __init__(self, n_hosts: int, consecutive_5xx: int = 5, base_ejection_time: int = 30,
                 max_ejection_time: int = 300, max_ejection_percent: int = 10) -> None:
        self.hosts = [_Host() for _ in range(n_hosts)]
        self.threshold = consecutive_5xx
        self.base = base_ejection_time
        self.max_time = max(max_ejection_time, base_ejection_time)
        self.max_percent = max_ejection_percent
        self.log: list[tuple[int, int, int]] = []  # (time, host, ejection time)

    def ejected(self, h: int) -> bool:
        return self.hosts[h].ejected_at >= 0

    def ejected_count(self) -> int:
        return sum(1 for h in self.hosts if h.ejected_at >= 0)

    def on_response(self, h: int, status: int, now: int) -> None:
        host = self.hosts[h]
        if status < 500:  # @line L5
            host.consecutive_5xx = 0
            return
        host.consecutive_5xx += 1  # @line L6
        if host.consecutive_5xx >= self.threshold and host.ejected_at < 0:  # @line L7
            if (self.ejected_count() + 1) * 100 <= self.max_percent * len(self.hosts):
                host.multiplier += 1  # @line L8
                host.ejection_time = min(host.multiplier * self.base, self.max_time)
                host.ejected_at = now
                self.log.append((now, h, host.ejection_time))

    def sweep(self, now: int) -> None:
        for host in self.hosts:  # @line L9
            if host.ejected_at >= 0:
                if now >= host.ejected_at + host.ejection_time:  # @line L10
                    host.ejected_at = -1
                    host.consecutive_5xx = 0
            elif host.multiplier > 0:  # @line L11
                host.multiplier -= 1


def routable(healthy: list[bool], panic_percent: int = 50) -> list[int]:
    """The hosts a balancer may pick. If the healthy share is below the panic
    threshold, use every host, as a deep check that fails everywhere would
    otherwise leave nothing."""
    good = [i for i, ok in enumerate(healthy) if ok]  # @line L12
    if len(good) * 100 < panic_percent * len(healthy):  # @line L13
        return list(range(len(healthy)))
    return good  # @line L14
