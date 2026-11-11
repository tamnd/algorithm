# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/session-guarantees/. The authors are listed in prov/HVCFWA.jsonl.

"""Session guarantees over a weakly consistent store (Terry et al. 1994).

The store has m servers. A client writes or reads at any server. A server
gives each new write a Lamport stamp larger than every stamp it knows, so the
write order extends what the server has seen, and a read returns the write
with the largest stamp for the key (last writer wins). Servers exchange their
whole logs by anti-entropy, so a log that holds a write also holds every write
that its origin server had when it accepted it. Each server summarizes its log
by a version vector: entry j is the number of writes from server j it holds.

A Session keeps a read vector and a write vector. With checks turned on, a
server may serve an operation only if its version vector dominates the vector
that the guarantee names:

  guarantee            checked on   needed vector   vector updated on
  read your writes     read         write vector    write
  monotonic reads      read         read vector     read
  writes follow reads  write        read vector     read
  monotonic writes     write        write vector    write

The Monitor checks the four guarantees on the run itself, with the
definitions of the paper, and records each violation.
"""

from dataclasses import dataclass, field
from typing import Optional

RYW, MR, WFR, MW = "read your writes", "monotonic reads", "writes follow reads", "monotonic writes"
ALL = frozenset({RYW, MR, WFR, MW})

WriteId = tuple[int, int]  # (origin server, sequence number at that server)


@dataclass(frozen=True)
class Write:
    wid: WriteId
    stamp: tuple[int, int]  # (Lamport counter, origin server)
    key: str
    value: int


class Unavailable(Exception):
    """The chosen server cannot serve the operation without breaking a guarantee."""


class Server:
    def __init__(self, sid: int, m: int) -> None:
        self.sid = sid
        self.m = m
        self.log: dict[WriteId, Write] = {}
        self.own = 0

    def vv(self) -> list[int]:
        v = [0] * self.m
        for origin, seq in self.log:
            v[origin] = max(v[origin], seq)
        return v

    def accept(self, key: str, value: int) -> Write:
        counter = 1 + max((w.stamp[0] for w in self.log.values()), default=0)
        self.own += 1
        w = Write((self.sid, self.own), (counter, self.sid), key, value)
        self.log[w.wid] = w
        return w

    def lookup(self, key: str) -> Optional[Write]:
        cands = [w for w in self.log.values() if w.key == key]
        return max(cands, key=lambda w: w.stamp) if cands else None

    def snapshot(self) -> dict[WriteId, Write]:
        return dict(self.log)

    def receive(self, snap: dict[WriteId, Write]) -> None:
        self.log.update(snap)


def dominates(a: list[int], b: list[int]) -> bool:
    return all(x >= y for x, y in zip(a, b))


def vmax(a: list[int], b: list[int]) -> list[int]:
    return [max(x, y) for x, y in zip(a, b)]


@dataclass
class Violation:
    guarantee: str
    detail: str


@dataclass
class Monitor:
    """Checks the guarantees of every session against the server logs."""

    servers: list[Server]
    violations: list[Violation] = field(default_factory=list)
    # per session: own writes so far, and the relevant writes of each read so far
    writes: dict[int, list[WriteId]] = field(default_factory=dict)
    reads: dict[int, set[WriteId]] = field(default_factory=dict)
    wfr_deps: dict[WriteId, set[WriteId]] = field(default_factory=dict)
    mw_deps: dict[WriteId, set[WriteId]] = field(default_factory=dict)

    def on_read(self, cid: int, s: Server, key: str) -> None:
        have = s.log.keys()
        if not set(self.writes.get(cid, [])) <= have:
            self.violations.append(Violation(RYW, f"session {cid} read at server {s.sid}"))
        if not self.reads.get(cid, set()) <= have:
            self.violations.append(Violation(MR, f"session {cid} read at server {s.sid}"))
        relevant = {wid for wid, w in s.log.items() if w.key == key}
        self.reads.setdefault(cid, set()).update(relevant)

    def on_write(self, cid: int, w: Write) -> None:
        self.wfr_deps[w.wid] = set(self.reads.get(cid, set()))
        self.mw_deps[w.wid] = set(self.writes.get(cid, []))
        self.writes.setdefault(cid, []).append(w.wid)

    def check_servers(self) -> None:
        for s in self.servers:
            for wid, w in s.log.items():
                for g, deps in ((WFR, self.wfr_deps.get(wid)), (MW, self.mw_deps.get(wid))):
                    if not deps:
                        continue
                    ok = deps <= s.log.keys() and all(s.log[d].stamp < w.stamp for d in deps)
                    if not ok:
                        self.violations.append(Violation(g, f"server {s.sid} holds {wid}"))

    def kinds(self) -> set[str]:
        return {v.guarantee for v in self.violations}


class Session:
    def __init__(self, cid: int, m: int, monitor: Monitor, guarantees: frozenset = ALL) -> None:
        self.cid = cid
        self.rv = [0] * m
        self.wv = [0] * m
        self.monitor = monitor
        self.g = guarantees

    def read(self, s: Server, key: str) -> Optional[int]:
        if RYW in self.g and not dominates(s.vv(), self.wv):
            raise Unavailable(RYW)
        if MR in self.g and not dominates(s.vv(), self.rv):
            raise Unavailable(MR)
        self.monitor.on_read(self.cid, s, key)
        self.rv = vmax(self.rv, s.vv())
        w = s.lookup(key)
        return None if w is None else w.value

    def write(self, s: Server, key: str, value: int) -> Write:
        if WFR in self.g and not dominates(s.vv(), self.rv):
            raise Unavailable(WFR)
        if MW in self.g and not dominates(s.vv(), self.wv):
            raise Unavailable(MW)
        w = s.accept(key, value)
        self.monitor.on_write(self.cid, w)
        self.wv[s.sid] = max(self.wv[s.sid], w.wid[1])
        return w
