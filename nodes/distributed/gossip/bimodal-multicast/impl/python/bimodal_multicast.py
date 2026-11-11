# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bimodal-multicast/. The authors are listed in prov/A2XR3K.jsonl.

"""Bimodal multicast (pbcast), after Birman et al., ACM TOCS 1999.

Stage 1 is an unreliable multicast: each copy is lost independently.
Stage 2 is anti-entropy in rounds: every process sends a digest of the
message ids in its buffer to one random process, the receiver solicits the
ids it lacks, and the gossiper retransmits them, up to a limit per round.
Every packet (digest, solicitation, retransmission) is lost with probability
loss. A process keeps a message in its buffer for keep rounds and then
garbage collects it.

The simulator is deterministic, seeded and runs in lock-step rounds.
The module also computes the delivery distribution of the simplified model of
Appendix A of the paper, by an exact chain-binomial recurrence.
"""

import math
import random


class PbcastProcess:
    """Message types: DIGEST(ids), SOLICIT(ids), DATA(id)."""

    def __init__(self, ident: int, keep: int, limit: int) -> None:
        self.id = ident
        self.keep = keep
        self.limit = limit
        self.buffer: dict[int, int] = {}  # message id -> round it arrived
        self.delivered: list[int] = []
        self.seen: set[int] = set()

    def deliver(self, mid: int, now: int) -> None:
        if mid not in self.seen:  # @line L2
            self.seen.add(mid)
            self.delivered.append(mid)
            self.buffer[mid] = now

    def on_round(self, partner: int) -> tuple[int, int, str, tuple[int, ...]]:
        return (self.id, partner, "DIGEST", tuple(sorted(self.buffer)))  # @line L4

    def on_message(self, src: int, kind: str, ids: tuple[int, ...], now: int) -> list[tuple[int, int, str, tuple[int, ...]]]:
        if kind == "DIGEST":
            missing = tuple(m for m in ids if m not in self.seen)  # @line L5
            return [(self.id, src, "SOLICIT", missing)] if missing else []
        if kind == "SOLICIT":
            # Most recent first, at most limit retransmissions per request.
            have = sorted((m for m in ids if m in self.buffer), reverse=True)[: self.limit]  # @line L6
            return [(self.id, src, "DATA", (m,)) for m in have]
        if kind == "DATA":
            self.deliver(ids[0], now)
        return []

    def collect(self, now: int) -> None:
        for mid in [m for m, t in self.buffer.items() if now - t >= self.keep]:  # @line L7
            del self.buffer[mid]


def pbcast(n: int, messages: int, rng: random.Random, loss: float = 0.0, keep: int = 10, limit: int = 8,
           multicast_fails: frozenset[int] = frozenset(), extra_rounds: int = 15) -> tuple[list[int], int]:
    """Process 0 multicasts one message per round for `messages` rounds.

    A message whose id is in multicast_fails reaches nobody in stage 1.
    Return (for each message, the number of processes that delivered it;
    the number of DATA retransmissions sent).
    """
    procs = [PbcastProcess(i, keep, limit) for i in range(n)]
    retrans = 0
    for now in range(messages + extra_rounds):
        if now < messages:
            procs[0].deliver(now, now)  # @line L1
            if now not in multicast_fails:
                for p in procs[1:]:
                    if rng.random() >= loss:
                        p.deliver(now, now)
        queue = []
        for p in procs:
            u = rng.randrange(n - 1)  # @line L3
            queue.append(p.on_round(u + 1 if u >= p.id else u))
        while queue:  # digest, solicitation and retransmission all happen within the round
            nxt = []
            for src, dst, kind, ids in queue:
                if rng.random() < loss:
                    continue
                if kind == "DATA":
                    retrans += 1
                nxt.extend(procs[dst].on_message(src, kind, ids, now))
            queue = nxt
        for p in procs:
            p.collect(now)
    counts = [sum(m in p.seen for p in procs) for m in range(messages)]
    return counts, retrans


# The simplified model of Appendix A: a process gossips only in the round after
# it receives the message, to each other process with probability beta.

def delivery_distribution(n: int, fanout: float, eps: float, rounds: int) -> list[float]:
    """Exact distribution of the number of processes that receive the message
    when the initial multicast fails (s0 = 1, r0 = n - 1). Process crashes are
    left out. Entry k is P(k processes have the message after `rounds` rounds).
    """
    p = fanout / n * (1 - eps)
    q = 1 - p
    dist = {(1, n - 1): 1.0}  # (processes that gossip this round, susceptible) -> probability
    final = [0.0] * (n + 1)
    for _ in range(rounds):
        nxt: dict[tuple[int, int], float] = {}
        for (s, r), pr in dist.items():
            if s == 0:
                final[n - r] += pr
                continue
            hit = 1 - q ** s
            for k in range(r + 1):
                pk = math.comb(r, k) * hit ** k * (1 - hit) ** (r - k)
                if pk > 0:
                    nxt[(k, r - k)] = nxt.get((k, r - k), 0.0) + pr * pk
        dist = nxt
    for (s, r), pr in dist.items():
        final[n - r] += pr
    return final


def delivery_sample(n: int, fanout: float, eps: float, rounds: int, rng: random.Random) -> int:
    """One run of the same simplified model, by simulation of each gossip packet."""
    beta = fanout / n
    have = [False] * n
    have[0] = True
    gossipers = [0]
    for _ in range(rounds):
        new = []
        for g in gossipers:
            for v in range(n):
                if v != g and not have[v] and rng.random() < beta and rng.random() >= eps:
                    have[v] = True
                    new.append(v)
        gossipers = new
    return sum(have)


def latency_recurrence(n: int, fanout: float, eps: float, tau: float, rounds: int) -> list[float]:
    """The mean-field recurrence of Appendix A in which every infected process
    gossips in every round. Return w_t, the probability that a correct
    process first receives the message in round t, for t = 1..rounds."""
    p = fanout / n * (1 - eps)
    q = 1 - p
    s, r = 1.0, n - 1.0
    v_prev, out = 0.0, []
    for _ in range(rounds):
        s, r = s * (1 - tau), r * (1 - tau)
        k = r * (1 - q ** s)
        s, r = s + k, r - k
        v = 1 - r / n
        out.append(v - v_prev)
        v_prev = v
    return out
