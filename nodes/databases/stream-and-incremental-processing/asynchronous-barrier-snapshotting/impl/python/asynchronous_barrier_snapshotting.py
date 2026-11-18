# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asynchronous-barrier-snapshotting/. The authors are listed in prov/8TJ3Y4.jsonl.

"""Asynchronous barrier snapshotting, simulated on one thread.

A job is a directed graph of tasks joined by FIFO channels. Sources read
records from input lists at an offset. Every other task has a state (a
Counter) and an operator op(state, sender, value) that updates the state and
returns a list of (receiver, value) pairs to send.

A snapshot n starts at the sources: each source stores its offset and sends
barrier n on its outputs. A task blocks each regular input on which barrier n
has arrived. When it has arrived on all regular inputs, the task sends the
barrier on, copies its state and unblocks. Back edges, found by depth-first
search from the sources, are never blocked: the task logs the records that
arrive on them after its copy, until the barrier comes back on each of them.

A scheduler picks a random enabled step at each turn, so channels are FIFO
but their speeds are arbitrary. With aligned=False the tasks copy their state
at the first barrier and do not block, which is not consistent.
"""

import copy
import random
from collections import Counter, deque

class Barrier:
    """Barrier n, sent on a channel between records."""

    __slots__ = ("n",)

    def __init__(self, n: int) -> None:
        self.n = n


def back_edges(tasks, channels, sources) -> set:
    """The channels that close a cycle in a depth-first search from the sources."""
    outs = {t: [c for c in channels if c[0] == t] for t in tasks}
    color = {t: 0 for t in tasks}  # 0 new, 1 on the stack, 2 done
    back = set()

    def visit(t):
        color[t] = 1
        for c in outs[t]:
            if color[c[1]] == 1:
                back.add(c)
            elif color[c[1]] == 0:
                visit(c[1])
        color[t] = 2

    for s in sources:
        if color[s] == 0:
            visit(s)
    for t in tasks:
        if color[t] == 0:
            visit(t)
    return back


class Job:
    def __init__(self, ops: dict, channels: list, inputs: dict, aligned: bool = True) -> None:
        self.ops = ops                    # task -> operator, or None for a source
        self.inputs = inputs              # source -> list of records
        self.tasks = list(ops)
        self.sources = [t for t in self.tasks if ops[t] is None]
        self.channels = list(channels)
        self.ins = {t: [c for c in channels if c[1] == t] for t in self.tasks}
        self.outs = {t: [c for c in channels if c[0] == t] for t in self.tasks}
        self.back = back_edges(self.tasks, self.channels, self.sources)
        self.aligned = aligned
        self.queue = {c: deque() for c in self.channels}
        self.state = {t: Counter() for t in self.tasks}
        self.offset = {s: 0 for s in self.sources}
        self.blocked = {t: set() for t in self.tasks}
        self.seen = {t: set() for t in self.tasks}        # regular inputs that gave the barrier
        self.back_seen = {t: set() for t in self.tasks}   # back edges that gave the barrier
        self.logging = {t: None for t in self.tasks}      # (state copy, log) while logging
        self.done_for = {t: -1 for t in self.tasks}       # the last snapshot copied
        self.parts: dict = {}                             # snapshot -> task -> part
        self.complete: list = []                          # finished snapshots, in order
        self.in_flight = None
        self.to_trigger: set = set()
        self.next_id = 0

    # ---- the algorithm -------------------------------------------------

    def trigger(self) -> None:
        self.in_flight = self.next_id
        self.next_id += 1
        self.parts[self.in_flight] = {}
        self.to_trigger = set(self.sources)

    def source_barrier(self, s) -> None:
        n = self.in_flight
        self.to_trigger.discard(s)
        self.parts[n][s] = {"offset": self.offset[s]}  # @line L10
        for c in self.outs[s]:
            self.queue[c].append(Barrier(n))
        self._check_complete()

    def _copy(self, t, n) -> None:
        for c in self.outs[t]:
            self.queue[c].append(Barrier(n))  # @line L3
        self.done_for[t] = n
        self.logging[t] = (copy.deepcopy(self.state[t]), [])  # @line L4
        self.blocked[t] = set()  # @line L5
        self.seen[t] = set()

    def _finish_if_ready(self, t, n) -> None:
        back_in = [c for c in self.ins[t] if c in self.back]
        if self.logging[t] is not None and all(c in self.back_seen[t] for c in back_in):  # @line L6
            st, log = self.logging[t]
            self.parts[n][t] = {"state": st, "log": log}  # @line L7
            self.logging[t] = None
            self.back_seen[t] = set()
            self._check_complete()

    def on_barrier(self, t, c, n) -> None:
        regular = [x for x in self.ins[t] if x not in self.back]
        if c in self.back:
            self.back_seen[t].add(c)
        elif self.aligned:
            self.blocked[t].add(c)  # @line L1
            self.seen[t].add(c)
        if self.done_for[t] < n and (not self.aligned or set(regular) <= self.seen[t]):  # @line L2
            self._copy(t, n)
        self._finish_if_ready(t, n)

    def on_record(self, t, c, x) -> None:
        if self.logging[t] is not None and c in self.back:
            self.logging[t][1].append((c, x))  # @line L8
        for dst, y in self.ops[t](self.state[t], c[0], x):  # @line L9
            self.queue[(t, dst)].append(y)

    def _check_complete(self) -> None:
        n = self.in_flight
        if n is not None and len(self.parts[n]) == len(self.tasks):
            self.complete.append(n)
            self.in_flight = None

    # ---- the scheduler -------------------------------------------------

    def actions(self, may_trigger: bool) -> list:
        acts = []
        if may_trigger and self.in_flight is None:
            acts.append(("trigger",))
        for s in self.sources:
            if s in self.to_trigger:
                acts.append(("barrier", s))
            if self.offset[s] < len(self.inputs[s]):
                acts.append(("emit", s))
        for t in self.tasks:
            for c in self.ins[t]:
                if self.queue[c] and c not in self.blocked[t]:
                    acts.append(("take", t, c))
        return acts

    def do(self, act) -> None:
        if act[0] == "trigger":
            self.trigger()
        elif act[0] == "barrier":
            self.source_barrier(act[1])
        elif act[0] == "emit":
            s = act[1]
            x = self.inputs[s][self.offset[s]]
            self.offset[s] += 1
            for c in self.outs[s]:
                self.queue[c].append(x)
        else:
            _, t, c = act
            m = self.queue[c].popleft()
            if isinstance(m, Barrier):
                self.on_barrier(t, c, m.n)
            else:
                self.on_record(t, c, m)

    def run(self, rng: random.Random, steps=None, snapshots: int = 0, p_trigger: float = 0.05) -> bool:
        """Run up to steps turns (or to the end), starting up to `snapshots` snapshots.

        Returns True when the job has nothing left to do.
        """
        k = 0
        while steps is None or k < steps:
            may = len(self.complete) + (self.in_flight is not None) < snapshots
            acts = self.actions(may)
            if not acts:
                return True
            if acts[0][0] == "trigger" and (len(acts) == 1 or rng.random() < p_trigger):
                self.do(acts[0])
            else:
                rest = [a for a in acts if a[0] != "trigger"]
                self.do(rng.choice(rest))
            k += 1
        return not self.actions(False)

    # ---- recovery ------------------------------------------------------

    def last_snapshot(self):
        """The parts of the last finished snapshot, or of the empty start state."""
        if self.complete:
            return self.parts[self.complete[-1]]
        empty = {s: {"offset": 0} for s in self.sources}
        empty.update({t: {"state": Counter(), "log": []} for t in self.tasks if t not in self.sources})
        return empty

    def restored(self, parts, inputs=None) -> "Job":
        """A new job that starts from a snapshot: states and offsets, regular channels empty,
        and the logged back-edge records in front of their channels."""
        job = Job(self.ops, self.channels, self.inputs if inputs is None else inputs, self.aligned)
        for t in self.tasks:
            if t in self.sources:
                job.offset[t] = parts[t]["offset"]
            else:
                job.state[t] = copy.deepcopy(parts[t]["state"])
                for c, x in parts[t]["log"]:
                    job.queue[c].append(x)
        return job

    def final_states(self) -> dict:
        return {t: +self.state[t] for t in self.tasks if t not in self.sources}


def drain(job: Job, rng: random.Random) -> dict:
    """Run to the end without snapshots and return the task states."""
    job.run(rng)
    return job.final_states()


# ---- two example jobs ----------------------------------------------------

def op_key(dst, m):
    def op(state, sender, x):
        return [(dst, x % m)]
    return op


def op_count(dst):
    def op(state, sender, x):
        state[x] += 1
        return [(dst, (x, state[x]))]
    return op


def op_sink(state, sender, x):
    state[x] += 1
    return []


def acyclic_job(a, b, aligned=True) -> Job:
    """Two sources, a map on each, a keyed count with two inputs, and a sink."""
    ops = {"s1": None, "s2": None, "m1": op_key("cnt", 3), "m2": op_key("cnt", 3),
           "cnt": op_count("sink"), "sink": op_sink}
    ch = [("s1", "m1"), ("s2", "m2"), ("m1", "cnt"), ("m2", "cnt"), ("cnt", "sink")]
    return Job(ops, ch, {"s1": list(a), "s2": list(b)}, aligned)


def op_dec(state, sender, x):
    state[x] += 1
    out = [("sink", x)]
    if x > 0:
        out.append(("fb", x - 1))
    return out


def op_fb(state, sender, x):
    state["passes"] += 1
    return [("dec", x)]


def cyclic_job(a, b) -> Job:
    """Two sources feed a loop: dec sends x - 1 around the cycle dec -> fb -> dec while x > 0."""
    ops = {"s1": None, "s2": None, "dec": op_dec, "fb": op_fb, "sink": op_sink}
    ch = [("s1", "dec"), ("s2", "dec"), ("dec", "fb"), ("fb", "dec"), ("dec", "sink")]
    return Job(ops, ch, {"s1": list(a), "s2": list(b)})
