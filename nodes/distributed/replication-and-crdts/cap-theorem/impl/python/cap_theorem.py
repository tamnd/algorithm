# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cap-theorem/. The authors are listed in prov/CYTDK7.jsonl.

"""The two executions in the proof of the CAP theorem (Gilbert and Lynch 2002).

A small deterministic simulator runs a replicated read/write register on two
nodes. Node 0 is the group G1 and node 1 is the group G2. Time moves in ticks;
a message sent at tick t arrives at tick t + 1 unless the network loses it. A
partition loses every message between G1 and G2.

The proof builds three runs for any protocol:

  alpha1  a write of v1 at G1, with every message between the groups lost;
  alpha2  a read at G2 after that time, with no write, every message lost;
  alpha   alpha1 followed by alpha2.

G2 receives no message in alpha or in alpha2, so its view is the same in both
and the read returns the same answer. In alpha2 the only correct answer is the
initial value v0, so in alpha the read returns v0 after the write of v1 has
completed, which is not atomic. If instead the read never answers, the
protocol is not available. The functions below build these runs and report
which of the two properties a given protocol gives up.
"""

from dataclasses import dataclass, field
from typing import Optional

V0 = 0
Msg = tuple  # (source, destination, payload)


@dataclass
class Result:
    responses: dict[int, tuple[int, object]] = field(default_factory=dict)  # request id -> (tick, value)
    views: dict[int, list[tuple]] = field(default_factory=dict)  # node -> what it saw and did


class Node:
    """A protocol is a class with these three handlers. Each returns
    (responses, messages): responses are (request id, value) pairs."""

    def __init__(self, nid: int) -> None:
        self.nid = nid

    def on_request(self, rid: int, op: str, arg: Optional[int], now: int) -> tuple[list, list]:
        raise NotImplementedError

    def on_message(self, src: int, payload: tuple, now: int) -> tuple[list, list]:
        return [], []

    def on_tick(self, now: int) -> tuple[list, list]:
        return [], []


class LocalAnswer(Node):
    """Answer from the local copy and send writes to the other node. Available, not atomic."""

    def __init__(self, nid: int) -> None:
        super().__init__(nid)
        self.value = V0

    def on_request(self, rid, op, arg, now):
        if op == "write":
            self.value = arg
            return [(rid, "ack")], [(self.nid, 1 - self.nid, ("update", arg))]
        return [(rid, self.value)], []

    def on_message(self, src, payload, now):
        self.value = payload[1]
        return [], []


class Primary(Node):
    """Node 0 holds the register; node 1 forwards and waits. Atomic, not available."""

    def __init__(self, nid: int) -> None:
        super().__init__(nid)
        self.value = V0

    def on_request(self, rid, op, arg, now):
        if self.nid == 0:
            if op == "write":
                self.value = arg
                return [(rid, "ack")], []
            return [(rid, self.value)], []
        return [], [(1, 0, ("req", rid, op, arg))]

    def on_message(self, src, payload, now):
        if payload[0] == "req":
            _, rid, op, arg = payload
            [(r, v)], _ = self.on_request(rid, op, arg, now)
            return [], [(0, src, ("resp", r, v))]
        _, rid, v = payload
        return [(rid, v)], []


class PrimaryWithTimeout(Primary):
    """Gilbert and Lynch, Section 4.3: as Primary, but node 1 answers a read
    from its last known value when the primary is silent for 2 t_msg + t_local
    ticks. Available always, atomic when no message is lost."""

    TIMEOUT = 3  # 2 * t_msg + t_local with t_msg = 1 and t_local = 1

    def __init__(self, nid: int) -> None:
        super().__init__(nid)
        self.pending: dict[int, tuple[int, str]] = {}

    def on_request(self, rid, op, arg, now):
        if self.nid == 1:
            self.pending[rid] = (now, op)
        return super().on_request(rid, op, arg, now)

    def on_message(self, src, payload, now):
        out, msgs = super().on_message(src, payload, now)
        if self.nid == 1 and payload[0] == "resp":
            if payload[1] not in self.pending:
                return [], msgs  # answered already by the timeout
            del self.pending[payload[1]]
            if isinstance(payload[2], int):
                self.value = payload[2]
        return out, msgs

    def on_tick(self, now):
        out = []
        for rid, (start, op) in list(self.pending.items()):
            if now - start >= self.TIMEOUT:
                out.append((rid, self.value if op == "read" else "ack"))
                del self.pending[rid]
        return out, []


PROTOCOLS = [LocalAnswer, Primary, PrimaryWithTimeout]


def run(protocol: type, script: list[tuple[int, int, int, str, Optional[int]]], partition: bool, ticks: int = 30) -> Result:
    """script: (tick, node, request id, op, arg). Returns responses and views."""
    nodes = [protocol(0), protocol(1)]
    res = Result(views={0: [], 1: []})
    inflight: list[tuple[int, Msg]] = []

    def emit(nid: int, out: list, msgs: list, now: int) -> None:
        for rid, v in out:
            res.responses[rid] = (now, v)
            res.views[nid].append(("respond", rid, v))
        for m in msgs:
            src, dst, _ = m
            if partition and src != dst:
                continue  # lost: the groups are cut off from each other
            inflight.append((now + 1, m))

    for now in range(ticks):
        due = [m for (t, m) in inflight if t == now]
        inflight[:] = [(t, m) for (t, m) in inflight if t != now]
        for src, dst, payload in due:
            res.views[dst].append(("message", src, payload))
            emit(dst, *nodes[dst].on_message(src, payload, now), now)
        for t, nid, rid, op, arg in script:
            if t == now:
                res.views[nid].append(("request", rid, op, arg))
                emit(nid, *nodes[nid].on_request(rid, op, arg, now), now)
        for nid in (0, 1):
            emit(nid, *nodes[nid].on_tick(now), now)
    return res


@dataclass
class Verdict:
    write_done: bool
    read_answer: Optional[object]  # None if the read never answered
    same_view_for_g2: bool

    @property
    def available(self) -> bool:
        return self.write_done and self.read_answer is not None

    @property
    def atomic(self) -> bool:
        # The write completed before the read started, so an atomic read returns v1.
        return self.read_answer is None or self.read_answer == 1


def cap_executions(protocol: type, ticks: int = 30) -> Verdict:
    """Build alpha1, alpha2 and alpha for the protocol and compare them."""
    a1 = run(protocol, [(0, 0, 1, "write", 1)], partition=True, ticks=ticks)
    write_done = 1 in a1.responses
    end1 = a1.responses[1][0] if write_done else ticks
    read_at = end1 + 1
    a2 = run(protocol, [(read_at, 1, 2, "read", None)], partition=True, ticks=ticks + read_at)
    alpha = run(protocol, [(0, 0, 1, "write", 1), (read_at, 1, 2, "read", None)], partition=True, ticks=ticks + read_at)
    read2 = a2.responses.get(2)
    readA = alpha.responses.get(2)
    assert (read2 is None) == (readA is None)
    if read2 is not None:
        assert read2[1] == V0  # in alpha2 no write happened
    return Verdict(write_done, None if readA is None else readA[1], a2.views[1] == alpha.views[1])


def no_partition_read(protocol: type) -> Optional[object]:
    """Write v1 at node 0, then read at node 1 after the write ends, with no loss."""
    r = run(protocol, [(0, 0, 1, "write", 1), (5, 1, 2, "read", None)], partition=False)
    return r.responses.get(2, (None, None))[1]
