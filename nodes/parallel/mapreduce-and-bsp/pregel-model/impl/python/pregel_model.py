# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pregel-model/. The authors are listed in prov/VS4KBS.jsonl.
"""A small Pregel simulator on a BSP machine, with single-source shortest
paths, PageRank and the maximum value example.

Vertex v lives on worker v mod p. In each superstep every worker runs
compute() on each of its vertices that is active or has messages. A message
sent in superstep k arrives in superstep k + 1. A vertex that votes to halt
becomes inactive, and a message wakes it again. The run ends when all
vertices are inactive and no message is in transit.

Costs per superstep, in the BSP sense:
  w = the largest number of compute calls plus messages read on one worker,
  h = the largest number of messages that one worker sends to or receives
      from other workers (after the combiner, if there is one).
The sum aggregator adds one more exchange of p words in each superstep; it is
not counted in h.
"""

from dataclasses import dataclass


@dataclass
class Step:
    w: int
    h: int
    messages: int   # all messages, including the ones inside a worker
    active: int     # vertices that ran compute()


class Context:
    def __init__(self, run, v):
        self._run = run
        self.id = v
        self.superstep = run.superstep
        self.messages = run.inbox.get(v, [])
        self.out_edges = run.out[v]
        self.num_vertices = run.n
        self.aggregated = run.aggregated  # the sum from the previous superstep

    @property
    def value(self):
        return self._run.value[self.id]

    @value.setter
    def value(self, x):
        self._run.value[self.id] = x

    def send(self, dest, msg):
        self._run.outbox.append((self.id, dest, msg))

    def vote_to_halt(self):
        self._run.active[self.id] = False

    def aggregate(self, x):
        self._run.agg_next += x


class Pregel:
    def __init__(self, n, out, p, value, combiner=None):
        """out[v] is a list of (target, weight). value[v] is the start value."""
        self.n, self.out, self.p = n, out, p
        self.value = list(value)
        self.combiner = combiner
        self.active = [True] * n
        self.inbox = {}
        self.superstep = 0
        self.aggregated = 0
        self.log = []

    def run(self, compute, max_supersteps=10000):
        p = self.p
        while any(self.active) or self.inbox:
            if self.superstep >= max_supersteps:
                raise RuntimeError("too many supersteps")
            self.outbox, self.agg_next = [], 0
            work = [0] * p
            ran = 0
            # The parallel step: each worker handles its own vertices only.
            for v in range(self.n):
                if self.active[v] or v in self.inbox:
                    self.active[v] = True
                    ctx = Context(self, v)
                    compute(ctx)
                    work[v % p] += 1 + len(ctx.messages)
                    ran += 1
            # The combiner merges the messages of one worker to one vertex.
            if self.combiner is not None:
                merged = {}
                for src, dest, msg in self.outbox:
                    key = (src % p, dest)
                    merged[key] = msg if key not in merged else self.combiner(merged[key], msg)
                outbox = [(w, dest, msg) for (w, dest), msg in merged.items()]
            else:
                outbox = [(src % p, dest, msg) for src, dest, msg in self.outbox]
            sent, recv = [0] * p, [0] * p
            inbox = {}
            for w, dest, msg in outbox:
                inbox.setdefault(dest, []).append(msg)
                if w != dest % p:
                    sent[w] += 1
                    recv[dest % p] += 1
            # The barrier: messages and the aggregate become visible together.
            self.inbox = inbox
            self.aggregated = self.agg_next
            self.log.append(Step(max(work), max(sent + recv), len(outbox), ran))
            self.superstep += 1
        return self.value


INF = float("inf")


def sssp(n, out, source, p=4, combine=True):
    """Single-source shortest paths, as in the Pregel paper (Section 5.2)."""
    def compute(ctx):
        best = 0 if (ctx.superstep == 0 and ctx.id == source) else INF
        for m in ctx.messages:
            best = min(best, m)
        if best < ctx.value:
            ctx.value = best
            for t, wt in ctx.out_edges:
                ctx.send(t, best + wt)
        ctx.vote_to_halt()

    g = Pregel(n, out, p, [INF] * n, combiner=min if combine else None)
    return g.run(compute), g


def pagerank(n, out, iterations, alpha, p=4):
    """PageRank with follow probability alpha (0.85 in the paper). In superstep
    k >= 1 a vertex sets its value to (1 - alpha)/n + alpha * (the sum of its
    messages + D/n), where D is the value held by vertices without out-edges
    in superstep k - 1, collected by a sum aggregator. After `iterations`
    updates every vertex votes to halt, so the run has iterations + 1 supersteps."""
    def compute(ctx):
        if ctx.superstep >= 1:
            ctx.value = (1 - alpha) / ctx.num_vertices + alpha * (
                sum(ctx.messages) + (zero + ctx.aggregated) / ctx.num_vertices)
        if ctx.superstep < iterations:
            if ctx.out_edges:
                share = ctx.value / len(ctx.out_edges)
                for t, _ in ctx.out_edges:
                    ctx.send(t, share)
            else:
                ctx.aggregate(ctx.value)
        else:
            ctx.vote_to_halt()

    zero = alpha - alpha  # 0 in the number type of alpha (float or Fraction)
    g = Pregel(n, out, p, [(zero + 1) / n] * n)
    return g.run(compute), g


def max_value(n, out, values, p=4):
    """The example of Section 2 of the paper: every vertex learns the largest
    value that can reach it."""
    def compute(ctx):
        changed = ctx.superstep == 0
        for m in ctx.messages:
            if m > ctx.value:
                ctx.value = m
                changed = True
        if changed:
            for t, _ in ctx.out_edges:
                ctx.send(t, ctx.value)
        ctx.vote_to_halt()

    g = Pregel(n, out, p, values, combiner=max)
    return g.run(compute), g
