# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/precision-time-protocol/. The authors are listed in prov/QV4H8D.jsonl.

"""The delay request-response mechanism of IEEE 1588 (PTP), with transparent
clocks and the data set comparison of the best master clock algorithm.

Timestamps (two-step clock: the precise t1 comes in a Follow_Up message):
  t1  master clock when Sync leaves the master
  t2  slave clock when Sync reaches the slave
  t3  slave clock when Delay_Req leaves the slave
  t4  master clock when Delay_Req reaches the master (sent back in Delay_Resp)

With slave clock = master clock + o, delay a master to slave and b slave to master:
  t2 = t1 + a + o,  t4 = t3 + b - o
  meanPathDelay    = ((t2 - t1) + (t4 - t3)) / 2 = (a + b) / 2
  offsetFromMaster = ((t2 - t1) - (t4 - t3)) / 2 = o + (a - b) / 2

A transparent clock on the path adds the residence time of each event message
to its correctionField, and the slave takes the corrections away first.
"""

import random
from dataclasses import dataclass


def ptp_compute(t1: float, t2: float, t3: float, t4: float, c_sync: float = 0.0, c_req: float = 0.0) -> tuple[float, float]:
    """Return (offsetFromMaster, meanPathDelay). c_sync and c_req are the
    correctionField values of the Sync and Delay_Req messages."""
    ms = t2 - t1 - c_sync  # @line L1
    sm = t4 - t3 - c_req  # @line L2
    return (ms - sm) / 2, (ms + sm) / 2  # @line L3


@dataclass
class Path:
    """A path of links and transparent clocks between master and slave.
    links_ms and links_sm are the link delays of each direction; the residence
    time in each bridge is drawn per message."""

    links_ms: list[float]
    links_sm: list[float]
    res_lo: float = 0.0
    res_hi: float = 0.0

    def traverse(self, links: list[float], rng: random.Random) -> tuple[float, float]:
        """Return (total delay, sum of residence times) for one message."""
        res = sum(rng.uniform(self.res_lo, self.res_hi) for _ in range(len(links) - 1))
        return sum(links) + res, res


def exchange(o: float, path: Path, rng: random.Random, use_tc: bool, start: float = 0.0, gap: float = 0.01) -> dict:
    """One Sync / Follow_Up / Delay_Req / Delay_Resp exchange. The slave clock
    is the master clock plus o."""
    t1 = start  # the master's precise send time, carried in Follow_Up
    a, res_a = path.traverse(path.links_ms, rng)
    t2 = t1 + a + o
    t3 = t2 + gap
    b, res_b = path.traverse(path.links_sm, rng)
    t4 = t3 - o + b
    c_sync, c_req = (res_a, res_b) if use_tc else (0.0, 0.0)
    off, mpd = ptp_compute(t1, t2, t3, t4, c_sync, c_req)
    return {"t": (t1, t2, t3, t4), "offset": off, "mpd": mpd, "a": a, "b": b, "res": (res_a, res_b)}


def boundary_chain(offsets: list[float], paths: list[Path], rng: random.Random) -> list[float]:
    """Clocks 0, 1, ..., k in a chain of boundary clocks: clock i + 1 is a slave
    of clock i on one port and a master on the next. offsets[i] is the error of
    clock i against the grandmaster (offsets[0] = 0). Each clock corrects itself
    by the measured offset. Returns the errors after one pass, in order."""
    err = list(offsets)
    for i, p in enumerate(paths):
        rel = err[i + 1] - err[i]
        meas = exchange(rel, p, rng, use_tc=False)["offset"]
        err[i + 1] -= meas
    return err


# --- the data set comparison of the best master clock algorithm (simplified) ---


@dataclass(frozen=True)
class AnnounceData:
    priority1: int
    clock_class: int
    clock_accuracy: int
    offset_scaled_log_variance: int
    priority2: int
    clock_identity: str

    def key(self) -> tuple:
        # Smaller is better at each field, in this order.
        return (
            self.priority1,
            self.clock_class,
            self.clock_accuracy,
            self.offset_scaled_log_variance,
            self.priority2,
            self.clock_identity,
        )


def best_master(cands: list[AnnounceData]) -> AnnounceData:
    """The grandmaster that the comparison picks (the part of the BMCA that
    compares two different grandmasters; the topology tie breaks are left out)."""
    return min(cands, key=AnnounceData.key)
