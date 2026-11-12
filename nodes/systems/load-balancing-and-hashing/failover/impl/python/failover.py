# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/failover/. The authors are listed in prov/D00TZM.jsonl.

"""Lease-based failover with fencing tokens.

Model: an integer clock that all parties read (no drift; see the page for
drift). A lease service, which stands for a replicated lock service such as one
built on Raft, grants one lease at a time. A lease lasts `lease` ticks and
carries a fencing token that grows by one with each new grant. The primary
renews its lease; a standby polls the service and takes over when the lease of
the primary has run out. The storage accepts a write only if its token is at
least the largest token it has seen. A node can crash (it stops for good) or
pause (it stops for a while and then resumes the step it was in).
"""

import random
from dataclasses import dataclass, field
from fractions import Fraction


class LeaseService:
    def __init__(self, lease: int) -> None:
        self.lease = lease
        self.holder: int | None = None
        self.expiry = 0
        self.token = 0
        self.grants: list[tuple[int, int, int, int]] = []  # (time, node, token, expiry)
        self.ends: list[int] = []

    def acquire(self, node: int, now: int) -> tuple[int, int] | None:
        """Grant or renew. Return (token, expiry), or None if another node holds
        an unexpired lease."""
        if self.holder == node and now < self.expiry:  # @line L2
            self.expiry = now + self.lease  # renewal keeps the token
            return self.token, self.expiry
        if self.holder is not None and now < self.expiry:  # @line L1
            return None
        if self.holder is not None:
            self.ends.append(self.expiry)  # the final expiry of the lease that ends here
        self.token += 1  # @line L3
        self.holder, self.expiry = node, now + self.lease
        self.grants.append((now, node, self.token, self.expiry))
        return self.token, self.expiry


class Storage:
    def __init__(self, fencing: bool = True) -> None:
        self.fencing = fencing
        self.max_token = 0
        self.accepted: list[tuple[int, int, int]] = []  # (time, node, token)
        self.rejected: list[tuple[int, int, int]] = []

    def write(self, node: int, token: int, now: int) -> bool:
        if self.fencing and token < self.max_token:  # @line L8
            self.rejected.append((now, node, token))
            return False
        self.max_token = max(self.max_token, token)  # @line L9
        self.accepted.append((now, node, token))
        return True


def vrrp_master_down_interval(adver_cs: int, priority: int) -> Fraction:
    """RFC 5798, Section 6.1: 3 * Master_Adver_Interval + Skew_Time, in
    centiseconds, with Skew_Time = ((256 - priority) * Master_Adver_Interval) / 256."""
    skew = Fraction((256 - priority) * adver_cs, 256)
    return 3 * adver_cs + skew


@dataclass
class FailoverRun:
    acquire_time: int  # when the standby got the lease
    first_new_write: int  # first accepted write of the new primary
    last_old_write: int  # last accepted write of the old primary
    storage: Storage
    service: LeaseService
    stale_rejected: bool = False


def run_failover(lease: int, renew: int, poll: int, promote: int, fail_time: int,
                 pause: int | None = None, fencing: bool = True, horizon: int = 1000) -> FailoverRun:
    """Node 0 is the primary from time 0 and writes on every tick. It renews at
    multiples of `renew`. At `fail_time` it crashes, or, if `pause` is given, it
    stops for `pause` ticks just after it decided to write, and then sends that
    write with its old token. Node 1 polls at multiples of `poll`, and after it
    gets the lease it needs `promote` ticks before it writes."""
    svc, st = LeaseService(lease), Storage(fencing)
    tok0, exp0 = svc.acquire(0, 0)
    alive0, pending, wake = True, None, -1
    tok1, ready1, acq1 = None, None, None
    for t in range(horizon):
        # node 0, the old primary
        if alive0:
            if pending is not None and t == wake:
                st.write(0, pending, t)  # the stale write after the pause
                pending = None
            elif pending is None:
                if t == fail_time:
                    if pause is None:
                        alive0 = False
                    else:
                        pending, wake = tok0, t + pause
                else:
                    if t % renew == 0 and t > 0:
                        g = svc.acquire(0, t)
                        if g is None:
                            alive0 = False  # it learns it lost the lease and steps down
                        else:
                            tok0, exp0 = g
                    if alive0 and t < exp0:
                        st.write(0, tok0, t)
        # node 1, the standby
        if tok1 is None and t % poll == 0:
            g = svc.acquire(1, t)  # @line L4
            if g is not None:
                tok1, acq1, ready1 = g[0], t, t + promote  # @line L5
        elif tok1 is not None and t >= ready1:
            if t % renew == 0:
                svc.acquire(1, t)  # @line L6
            st.write(1, tok1, t)  # @line L7
        if acq1 is not None and pending is None and t > max(wake, ready1 or 0):
            break
    new = [a for a in st.accepted if a[1] == 1]
    old = [a for a in st.accepted if a[1] == 0]
    return FailoverRun(acq1, new[0][0] if new else -1, old[-1][0] if old else -1, st, svc,
                       any(r[1] == 0 for r in st.rejected))


def takeover_time_formula(lease: int, renew: int, poll: int, fail_time: int) -> int:
    """The standby gets the lease at the first poll at or after the expiry of
    the last renewal before the failure."""
    last_renew = (fail_time - 1) // renew * renew if fail_time > 0 else 0
    expiry = last_renew + lease
    return -(-expiry // poll) * poll


@dataclass
class _Node:
    token: int = 0
    expiry: int = 0
    pending: int | None = None
    wake: int = -1
    crashed: bool = False


def random_cluster(rng: random.Random, fencing: bool, n: int = 3, lease: int = 10,
                   steps: int = 300, p_pause: float = 0.02, max_pause: int = 30,
                   p_crash: float = 0.002) -> tuple[Storage, LeaseService]:
    """n nodes compete for one lease. Each tick, in a random order, each live
    node renews or acquires, and if it believes it holds the lease it writes.
    Sometimes it pauses between the decision and the write."""
    svc, st = LeaseService(lease), Storage(fencing)
    nodes = [_Node() for _ in range(n)]
    for t in range(steps):
        order = list(range(n))
        rng.shuffle(order)
        for i in order:
            nd = nodes[i]
            if nd.crashed:
                continue
            if nd.pending is not None:
                if t >= nd.wake:
                    st.write(i, nd.pending, t)
                    nd.pending = None
                continue
            if rng.random() < p_crash:
                nd.crashed = True
                continue
            g = svc.acquire(i, t)
            if g is not None:
                nd.token, nd.expiry = g
            if t < nd.expiry:  # it believes it is the primary
                if rng.random() < p_pause:
                    nd.pending, nd.wake = nd.token, t + rng.randint(1, max_pause)
                else:
                    st.write(i, nd.token, t)
    return st, svc


def tokens_monotone(st: Storage) -> bool:
    toks = [a[2] for a in st.accepted]
    return all(a <= b for a, b in zip(toks, toks[1:]))


def leases_disjoint(svc: LeaseService) -> bool:
    """Each new grant starts no earlier than the final expiry of the lease
    before it, by the clock of the service."""
    return all(svc.grants[i + 1][0] >= svc.ends[i] for i in range(len(svc.ends)))
