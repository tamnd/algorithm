# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/push-pull-gossip/. The authors are listed in prov/JCK6B9.jsonl.

"""Push, pull and push-pull rumor spreading, with the median-counter rule.

A deterministic, seeded, lock-step simulator of the random phone call model
(Karp, Schindelhauer, Shenker and Vocking, FOCS 2000). In each round every
process calls one partner: uniform over the other processes, or uniform over
its neighbours in an overlay graph. Along each call, a process that knew the
rumor at the start of the round may send it to the other end. All state
changes take effect at the end of the round.

spread() runs push, pull or push-pull until everybody knows the rumor (an
outside observer stops the run). median_counter() runs the address-oblivious
median-counter algorithm of Section 3 of Karp et al., which stops by itself.

The graph helpers compute the conductance of a small graph by brute force and
the eigenvalues of its normalized Laplacian by the cyclic Jacobi method, for
checks of Cheeger's inequality.
"""

import math
import random
from collections.abc import Callable, Sequence

Partner = Callable[[int, random.Random], int]
Graph = Sequence[Sequence[int]]


def complete_partner(n: int) -> Partner:
    def pick(v: int, rng: random.Random) -> int:
        u = rng.randrange(n - 1)
        return u + 1 if u >= v else u

    return pick


def overlay_partner(adj: Graph) -> Partner:
    def pick(v: int, rng: random.Random) -> int:
        return adj[v][rng.randrange(len(adj[v]))]

    return pick


class Process:
    """A process for push, pull and push-pull. Message type: RUMOR."""

    def __init__(self, ident: int, informed: bool, mode: str) -> None:
        self.id = ident
        self.informed = informed
        self.mode = mode
        self.heard = False

    def on_call(self, partner: int) -> list[tuple[int, int, str]]:
        """This process called partner. Push along the call if allowed."""
        if self.informed and self.mode in ("push", "push-pull"):
            return [(self.id, partner, "RUMOR")]  # @line L2
        return []

    def on_called(self, caller: int) -> list[tuple[int, int, str]]:
        """caller called this process. Pull along the call if allowed."""
        if self.informed and self.mode in ("pull", "push-pull"):
            return [(self.id, caller, "RUMOR")]  # @line L3
        return []

    def on_message(self, src: int, msg: str) -> None:
        if msg == "RUMOR":
            self.heard = True

    def end_round(self) -> bool:
        new = self.heard and not self.informed  # @line L4
        self.informed = self.informed or self.heard
        self.heard = False
        return new


def spread(n: int, mode: str, rng: random.Random, adj: Graph | None = None, source: int = 0,
           max_rounds: int = 10**6) -> tuple[int, int, list[int]]:
    """Run until all n processes know the rumor.

    Return (rounds, rumor transmissions, informed count after each round,
    starting with 1 before round 1).
    """
    pick = complete_partner(n) if adj is None else overlay_partner(adj)
    procs = [Process(i, i == source, mode) for i in range(n)]
    informed, tx, history, rounds = 1, 0, [1], 0
    while informed < n and rounds < max_rounds:
        rounds += 1
        out: list[tuple[int, int, str]] = []
        for p in procs:
            u = pick(p.id, rng)  # @line L1
            out.extend(p.on_call(u))
            out.extend(procs[u].on_called(p.id))
        for src, dst, msg in out:
            procs[dst].on_message(src, msg)
        tx += len(out)
        informed += sum(p.end_round() for p in procs)
        history.append(informed)
    return rounds, tx, history


# The median-counter algorithm (Karp et al., Section 3).

A, B, C, D = "A", "B", "C", "D"


class MedianCounterProcess:
    """States A (does not know), B-m (knows, counter m), C (knows, counting
    down), D (done). A process in B or C pushes and pulls along every call."""

    def __init__(self, ident: int, ctr_max: int, c_rounds: int, informed: bool = False) -> None:
        self.id = ident
        self.state = B if informed else A
        self.ctr = 1 if informed else 0
        self.age = 0
        self.ctr_max = ctr_max
        self.c_rounds = c_rounds
        self.seen: list[tuple[str, int]] = []

    def active(self) -> bool:
        return self.state in (B, C)

    def message(self) -> tuple[str, int] | None:
        """What this process sends along a call: its state and counter."""
        return (self.state, self.ctr) if self.active() else None

    def on_partner(self, partner_state: str, partner_ctr: int) -> None:
        """Record the state, at the start of the round, of one partner."""
        self.seen.append((partner_state, partner_ctr))

    def end_round(self) -> None:
        seen, self.seen = self.seen, []
        got_c = any(s == C for s, _ in seen)
        got_b = any(s == B for s, _ in seen)
        if self.state == A:  # @line L5
            if got_c:
                self.state, self.age = C, 0
            elif got_b:
                self.state, self.ctr = B, 1
        elif self.state == B:
            if got_c:
                self.state, self.age = C, 0
                return
            m = self.ctr
            at_least = sum(1 for s, c in seen if s == B and c >= m)
            below = sum(1 for s, c in seen if s == A or (s == B and c < m))
            if at_least > below:  # @line L6
                self.ctr += 1
                if self.ctr >= self.ctr_max:
                    self.state, self.age = C, 0
        elif self.state == C:
            self.age += 1
            if self.age >= self.c_rounds:  # @line L7
                self.state = D


def median_counter(n: int, rng: random.Random, ctr_max: int | None = None, c_rounds: int | None = None,
                   source: int = 0, max_rounds: int | None = None) -> tuple[int, int, int]:
    """Run until no process is in state B or C, or for max_rounds rounds.

    Return (rounds, rumor transmissions, number of processes that know the
    rumor). The defaults use ctr_max and c_rounds of order log log n.
    """
    loglog = math.log2(max(2.0, math.log2(max(n, 4))))
    if ctr_max is None:
        ctr_max = max(3, math.ceil(loglog) - 1)
    if c_rounds is None:
        c_rounds = max(2, math.ceil(loglog) - 2)
    if max_rounds is None:
        max_rounds = 4 * math.ceil(math.log2(max(n, 2))) + 20
    pick = complete_partner(n)
    procs = [MedianCounterProcess(i, ctr_max, c_rounds, i == source) for i in range(n)]
    tx, rounds = 0, 0
    while rounds < max_rounds and any(p.active() for p in procs):
        rounds += 1
        for p in procs:
            if p.state == D:
                continue
            q = procs[pick(p.id, rng)]
            if q.state == D:
                continue
            mp, mq = p.message(), q.message()
            if mp is not None:
                tx += 1
            if mq is not None:
                tx += 1
            p.on_partner(q.state, q.ctr)
            q.on_partner(p.state, p.ctr)
        for p in procs:
            p.end_round()
    informed = sum(p.state != A for p in procs)
    return rounds, tx, informed


def push_pull_with_age(n: int, rng: random.Random, t_max: int, source: int = 0) -> tuple[int, int]:
    """Section 2 of Karp et al.: every informed process pushes and pulls while
    the age of the rumor is at most t_max. Return (informed, transmissions)."""
    procs = [Process(i, i == source, "push-pull") for i in range(n)]
    pick = complete_partner(n)
    tx = 0
    for _ in range(t_max):
        out: list[tuple[int, int, str]] = []
        for p in procs:
            u = pick(p.id, rng)
            out.extend(p.on_call(u))
            out.extend(procs[u].on_called(p.id))
        for src, dst, msg in out:
            procs[dst].on_message(src, msg)
        tx += len(out)
        for p in procs:
            p.end_round()
    return sum(p.informed for p in procs), tx


# Graphs and conductance.

def star(n: int) -> list[list[int]]:
    return [list(range(1, n))] + [[0] for _ in range(1, n)]


def cycle(n: int) -> list[list[int]]:
    return [[(i - 1) % n, (i + 1) % n] for i in range(n)]


def barbell(m: int) -> list[list[int]]:
    """Two complete graphs on m vertices, joined by the edge (m - 1, m)."""
    adj = [[j for j in range(m) if j != i] for i in range(m)]
    adj += [[m + j for j in range(m) if j != i] for i in range(m)]
    adj[m - 1].append(m)
    adj[m].append(m - 1)
    return adj


def two_stars(a: int, n: int) -> list[list[int]]:
    """Giakkoupis's example: stars with a and n - a vertices, centers 0 and a joined."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for leaf in range(1, a):
        adj[0].append(leaf)
        adj[leaf].append(0)
    for leaf in range(a + 1, n):
        adj[a].append(leaf)
        adj[leaf].append(a)
    adj[0].append(a)
    adj[a].append(0)
    return adj


def random_regular_cycles(n: int, cycles: int, rng: random.Random) -> list[list[int]]:
    """The union of random Hamiltonian cycles: 2 * cycles regular (multi)graph."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for _ in range(cycles):
        order = list(range(n))
        rng.shuffle(order)
        for i in range(n):
            u, v = order[i], order[(i + 1) % n]
            adj[u].append(v)
            adj[v].append(u)
    return adj


def conductance(adj: Graph) -> float:
    """min over S with 0 < vol(S) <= vol(V)/2 of |E(S, V - S)| / vol(S), by brute force."""
    n = len(adj)
    deg = [len(a) for a in adj]
    total = sum(deg)
    best = math.inf
    for mask in range(1, (1 << n) - 1):
        vol = sum(deg[i] for i in range(n) if mask >> i & 1)
        if vol == 0 or 2 * vol > total:
            continue
        cut = sum(1 for i in range(n) if mask >> i & 1 for j in adj[i] if not mask >> j & 1)
        best = min(best, cut / vol)
    return best


def normalized_laplacian(adj: Graph) -> list[list[float]]:
    n = len(adj)
    deg = [len(a) for a in adj]
    lap = [[0.0] * n for _ in range(n)]
    for i in range(n):
        lap[i][i] = 1.0
        for j in adj[i]:
            lap[i][j] -= 1.0 / math.sqrt(deg[i] * deg[j])
    return lap


def symmetric_eigenvalues(mat: list[list[float]], sweeps: int = 60) -> list[float]:
    """Eigenvalues of a symmetric matrix by the cyclic Jacobi method, ascending."""
    a = [row[:] for row in mat]
    n = len(a)
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-22:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


def is_connected(adj: Graph) -> bool:
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for u in adj[v]:
            if u not in seen:
                seen.add(u)
                stack.append(u)
    return len(seen) == len(adj)
