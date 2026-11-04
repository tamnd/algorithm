# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-prediction-and-resolution/. The authors are listed in prov/F02YVH.jsonl.

"""Hard disks in the unit box: predict the next contact, resolve it elastically.

Each disk has a position (rx, ry), a velocity (vx, vy), a radius s > 0 and a
mass m > 0. The disks move in straight lines in the box [0, 1] x [0, 1]. The
predictions need disks that do not overlap and that lie inside the box.
"""

import heapq
import math
from dataclasses import dataclass

INF = math.inf


@dataclass
class Particle:
    rx: float
    ry: float
    vx: float
    vy: float
    s: float = 0.01
    m: float = 1.0
    count: int = 0

    def move(self, dt: float) -> None:
        """Advance the disk in a straight line for dt units of time."""
        self.rx += self.vx * dt
        self.ry += self.vy * dt

    def kinetic_energy(self) -> float:
        return 0.5 * self.m * (self.vx * self.vx + self.vy * self.vy)


def time_to_hit(p: Particle, q: Particle) -> float:
    """Return the time until p and q first touch, or INF if they never do.

    Precondition: p and q do not overlap. Cost: O(1).
    """
    if p is q:  # @line L1
        return INF
    dx, dy = q.rx - p.rx, q.ry - p.ry  # @line L2
    dvx, dvy = q.vx - p.vx, q.vy - p.vy
    b = dvx * dx + dvy * dy  # @line L3
    if b >= 0:  # @line L4
        return INF
    a = dvx * dvx + dvy * dvy  # @line L5
    sigma = p.s + q.s
    d = b * b - a * (dx * dx + dy * dy - sigma * sigma)  # @line L6
    if d < 0:  # @line L7
        return INF
    return -(b + math.sqrt(d)) / a  # @line L8


def time_to_hit_vertical_wall(p: Particle) -> float:
    """Time until p touches the wall x = 0 or x = 1, or INF. Needs s <= rx <= 1 - s."""
    if p.vx > 0:  # @line L9
        return (1.0 - p.s - p.rx) / p.vx
    if p.vx < 0:  # @line L10
        return (p.s - p.rx) / p.vx
    return INF  # @line L11


def time_to_hit_horizontal_wall(p: Particle) -> float:
    """Time until p touches the wall y = 0 or y = 1, or INF. Needs s <= ry <= 1 - s."""
    if p.vy > 0:  # @line L12
        return (1.0 - p.s - p.ry) / p.vy
    if p.vy < 0:
        return (p.s - p.ry) / p.vy
    return INF


def bounce_off(p: Particle, q: Particle) -> None:
    """Resolve an elastic collision of p and q, which touch. Cost: O(1)."""
    dx, dy = q.rx - p.rx, q.ry - p.ry  # @line L13
    dvx, dvy = q.vx - p.vx, q.vy - p.vy
    sigma = p.s + q.s
    j = 2.0 * p.m * q.m * (dvx * dx + dvy * dy) / (sigma * (p.m + q.m))  # @line L14
    jx, jy = j * dx / sigma, j * dy / sigma  # @line L15
    p.vx += jx / p.m  # @line L16
    p.vy += jy / p.m
    q.vx -= jx / q.m  # @line L17
    q.vy -= jy / q.m
    p.count += 1  # @line L18
    q.count += 1


def bounce_off_vertical_wall(p: Particle) -> None:
    p.vx = -p.vx  # @line L19
    p.count += 1


def bounce_off_horizontal_wall(p: Particle) -> None:
    p.vy = -p.vy  # @line L20
    p.count += 1


# An event is (time, seq, a, b, count_a, count_b). The index a or b is -1
# for a wall: (i, -1) is a vertical wall, (-1, i) a horizontal wall.
Event = tuple[float, int, int, int, int, int]


def predict(
    ps: list[Particle], i: int, t: float, limit: float, pq: list[Event], seq: list[int]
) -> None:
    """Push every future event of particle i that happens by time limit."""
    if i < 0:  # @line L21
        return
    p = ps[i]

    def push(dt: float, a: int, b: int) -> None:
        if dt < INF and t + dt <= limit:
            ca = ps[a].count if a >= 0 else -1
            cb = ps[b].count if b >= 0 else -1
            seq[0] += 1
            heapq.heappush(pq, (t + dt, seq[0], a, b, ca, cb))

    for k in range(len(ps)):  # @line L22
        push(time_to_hit(p, ps[k]), i, k)  # @line L23
    push(time_to_hit_vertical_wall(p), i, -1)  # @line L24
    push(time_to_hit_horizontal_wall(p), -1, i)


def simulate(ps: list[Particle], limit: float) -> list[tuple[float, int, int]]:
    """Run the event-driven simulation of ps up to time limit.

    Return the list of resolved events (time, a, b), with -1 for a wall as in
    Event. On return, every particle is at its position at time limit.
    Precondition: no two disks overlap and every disk is inside the box.
    Cost: O(n^2 log n) to start, then O(n log n) per resolved event.
    """
    pq: list[Event] = []  # @line L25
    seq = [0]
    t = 0.0
    for i in range(len(ps)):  # @line L26
        predict(ps, i, t, limit, pq, seq)
    done: list[tuple[float, int, int]] = []
    while pq:  # @line L27
        te, _, a, b, ca, cb = heapq.heappop(pq)  # @line L28
        if (a >= 0 and ps[a].count != ca) or (b >= 0 and ps[b].count != cb):  # @line L29
            continue
        for p in ps:  # @line L30
            p.move(te - t)
        t = te  # @line L31
        if a >= 0 and b >= 0:  # @line L32
            bounce_off(ps[a], ps[b])
        elif b < 0:
            bounce_off_vertical_wall(ps[a])
        else:
            bounce_off_horizontal_wall(ps[b])
        done.append((te, a, b))
        predict(ps, a, t, limit, pq, seq)  # @line L33
        predict(ps, b, t, limit, pq, seq)
    for p in ps:  # @line L34
        p.move(limit - t)
    return done
