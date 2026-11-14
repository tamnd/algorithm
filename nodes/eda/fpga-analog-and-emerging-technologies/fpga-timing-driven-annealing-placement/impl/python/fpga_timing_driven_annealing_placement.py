# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fpga-timing-driven-annealing-placement/. The authors are listed in prov/ZDNXW1.jsonl.

"""Timing-driven simulated annealing placement for an island-style FPGA, after VPR.

Blocks are placed on the sites (x, y) of an nx by ny grid, one block per site.
A net is a list of blocks, the driver first. The cost of a move is

    dC = lam * dT / prev_T + (1 - lam) * dBB / prev_BB,

where BB is the bounding box cost and T the timing cost, and prev_T, prev_BB
are their values at the start of the temperature.
"""

import itertools
import math
import random
from dataclasses import dataclass, field

# Cheng's crossing-count correction q(n) for a net with n terminals. The values for n <= 10 and
# the growth above 50 follow the table of VPR; between 10 and 50 this file interpolates linearly.
Q_TABLE = [1.0, 1.0, 1.0, 1.0, 1.0828, 1.1536, 1.2206, 1.2823, 1.3385, 1.3991, 1.4493]


def q(n: int) -> float:
    if n < len(Q_TABLE):
        return Q_TABLE[n]
    if n <= 50:
        return 1.4493 + (n - 10) * (2.7933 - 1.4493) / 40
    return 2.7933 + 0.02616 * (n - 50)


def delay(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Delay of a connection between sites a and b: 1 plus the Manhattan distance."""
    return 1 + abs(a[0] - b[0]) + abs(a[1] - b[1])


def net_bb(net: list[int], loc: list[tuple[int, int]]) -> float:
    xs = [loc[b][0] for b in net]
    ys = [loc[b][1] for b in net]
    return q(len(net)) * ((max(xs) - min(xs) + 1) + (max(ys) - min(ys) + 1))


def bb_cost(nets: list[list[int]], loc: list[tuple[int, int]]) -> float:
    return sum(net_bb(net, loc) for net in nets)


def connections(nets: list[list[int]]) -> list[tuple[int, int]]:
    return [(net[0], s) for net in nets for s in net[1:]]


def criticalities(n_blocks: int, conns: list[tuple[int, int]], loc: list[tuple[int, int]]) -> list[float]:
    """Static timing analysis: crit(c) = 1 - slack(c) / Dmax for each connection c.

    The connections must form a directed acyclic graph; blocks have delay 0.
    """
    fanin: list[list[int]] = [[] for _ in range(n_blocks)]
    fanout: list[list[int]] = [[] for _ in range(n_blocks)]
    for i, (u, v) in enumerate(conns):
        fanin[v].append(i)
        fanout[u].append(i)
    indeg = [len(fanin[v]) for v in range(n_blocks)]
    order = [v for v in range(n_blocks) if indeg[v] == 0]
    for v in order:
        for i in fanout[v]:
            w = conns[i][1]
            indeg[w] -= 1
            if indeg[w] == 0:
                order.append(w)
    d = [delay(loc[u], loc[v]) for u, v in conns]
    arrival = [0] * n_blocks
    for v in order:
        for i in fanout[v]:
            arrival[conns[i][1]] = max(arrival[conns[i][1]], arrival[v] + d[i])
    dmax = max(arrival, default=0)
    if dmax == 0:
        return [0.0] * len(conns)
    required = [dmax] * n_blocks
    for v in reversed(order):
        for i in fanout[v]:
            required[v] = min(required[v], required[conns[i][1]] - d[i])
    return [1 - (required[v] - arrival[u] - d[i]) / dmax for i, (u, v) in enumerate(conns)]


def alpha(r_acc: float) -> float:
    if r_acc > 0.96:
        return 0.5
    if r_acc > 0.8:
        return 0.9
    if r_acc > 0.15:
        return 0.95
    return 0.8


@dataclass
class Placer:
    nx: int
    ny: int
    n_blocks: int
    nets: list[list[int]]
    lam: float = 0.5
    inner: float = 1.0
    check_every_move: bool = False
    loc: list[tuple[int, int]] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.conns = connections(self.nets)
        self.nets_of: list[list[int]] = [[] for _ in range(self.n_blocks)]
        for i, net in enumerate(self.nets):
            for b in set(net):
                self.nets_of[b].append(i)
        self.conns_of: list[list[int]] = [[] for _ in range(self.n_blocks)]
        for i, (u, v) in enumerate(self.conns):
            self.conns_of[u].append(i)
            if v != u:
                self.conns_of[v].append(i)
        self.weight = [0.0] * len(self.conns)  # crit ** CE, fixed during a temperature

    def timing_cost(self) -> float:
        return sum(w * delay(self.loc[u], self.loc[v]) for w, (u, v) in zip(self.weight, self.conns))

    def _move_delta(self, a: int, b, target: tuple[int, int]) -> tuple[float, float]:
        """dBB and dT of moving a to target and b (or nothing) to a's site, from the affected nets only."""
        moved = [a] if b is None else [a, b]
        net_ids = sorted({i for m in moved for i in self.nets_of[m]})
        conn_ids = sorted({i for m in moved for i in self.conns_of[m]})
        old_bb = sum(net_bb(self.nets[i], self.loc) for i in net_ids)
        old_t = sum(self.weight[i] * delay(self.loc[self.conns[i][0]], self.loc[self.conns[i][1]]) for i in conn_ids)
        src = self.loc[a]
        self.loc[a] = target
        if b is not None:
            self.loc[b] = src
        new_bb = sum(net_bb(self.nets[i], self.loc) for i in net_ids)
        new_t = sum(self.weight[i] * delay(self.loc[self.conns[i][0]], self.loc[self.conns[i][1]]) for i in conn_ids)
        self.loc[a] = src
        if b is not None:
            self.loc[b] = target
        return new_bb - old_bb, new_t - old_t

    def place(self, rng: random.Random) -> list[tuple[int, int]]:
        sites = [(x, y) for x in range(self.nx) for y in range(self.ny)]
        if self.n_blocks > len(sites):
            raise ValueError("more blocks than sites")
        n = self.n_blocks
        rng.shuffle(sites)
        self.loc = sites[:n]  # @line L1
        at = {self.loc[i]: i for i in range(n)}
        r_max = max(self.nx, self.ny) - 1
        rlimit = float(max(r_max, 1))
        ce = 1.0

        def set_weights() -> None:
            crit = criticalities(n, self.conns, self.loc)
            self.weight = [c ** ce for c in crit]

        def try_move(t: float, prev_bb: float, prev_t: float, totals: list[float]) -> bool:
            a = rng.randrange(n)  # @line L5
            r = max(1, int(rlimit))
            ax, ay = self.loc[a]
            target = (
                rng.randint(max(0, ax - r), min(self.nx - 1, ax + r)),
                rng.randint(max(0, ay - r), min(self.ny - 1, ay + r)),
            )
            if target == self.loc[a]:
                return False
            b = at.get(target)
            d_bb, d_t = self._move_delta(a, b, target)
            d_c = (1 - self.lam) * d_bb / prev_bb + (self.lam * d_t / prev_t if prev_t > 0 else 0.0)  # @line L6
            if d_c <= 0 or (t > 0 and rng.random() < math.exp(-d_c / t)):  # @line L7
                src = self.loc[a]
                self.loc[a] = target
                at[target] = a
                if b is None:
                    del at[src]
                else:
                    self.loc[b] = src
                    at[src] = b
                totals[0] += d_bb
                totals[1] += d_t
                if self.check_every_move:
                    assert math.isclose(totals[0], bb_cost(self.nets, self.loc), rel_tol=1e-9, abs_tol=1e-9)
                    assert math.isclose(totals[1], self.timing_cost(), rel_tol=1e-9, abs_tol=1e-9)
                return True
            return False

        # Initial temperature: 20 times the standard deviation of the cost over n random moves.
        set_weights()
        prev_bb, prev_t = bb_cost(self.nets, self.loc), self.timing_cost()
        if prev_bb == 0:
            return self.loc
        samples = []
        totals = [prev_bb, prev_t]
        for _ in range(n):
            try_move(math.inf, prev_bb, prev_t, totals)
            samples.append((1 - self.lam) * totals[0] / prev_bb + (self.lam * totals[1] / prev_t if prev_t > 0 else 0.0))
        mean = sum(samples) / len(samples)
        t = 20 * math.sqrt(sum((s - mean) ** 2 for s in samples) / len(samples))
        moves = max(1, int(self.inner * n ** (4 / 3)))
        temps = 0
        while t >= 0.005 / len(self.nets):  # @line L2
            set_weights()  # @line L3
            prev_bb, prev_t = bb_cost(self.nets, self.loc), self.timing_cost()
            totals = [prev_bb, prev_t]
            accepted = sum(try_move(t, prev_bb, prev_t, totals) for _ in range(moves))  # @line L4
            r_acc = accepted / moves
            t *= alpha(r_acc)  # @line L8
            rlimit = min(max(rlimit * (1 - 0.44 + r_acc), 1.0), max(r_max, 1))  # @line L9
            ce = 1 + 7 * (1 - (rlimit - 1) / (r_max - 1)) if r_max > 1 else 8.0
            temps += 1
        set_weights()  # @line L10
        prev_bb, prev_t = bb_cost(self.nets, self.loc), self.timing_cost()
        totals = [prev_bb, prev_t]
        for _ in range(moves):
            try_move(0.0, prev_bb, prev_t, totals)
        self.stats = {"temperatures": temps, "moves_per_temperature": moves}
        return self.loc  # @line L11


def exhaustive_min_bb(nx: int, ny: int, n_blocks: int, nets: list[list[int]]) -> float:
    """Least bounding box cost over all placements, by trying every injective map of blocks to sites."""
    sites = [(x, y) for x in range(nx) for y in range(ny)]
    return min(bb_cost(nets, list(p)) for p in itertools.permutations(sites, n_blocks))
