# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slotted-aloha/. The authors are listed in prov/S3TWTY.jsonl.
"""Slotted ALOHA on one shared channel with ternary feedback (idle, success, collision).

Time is a count of slots. A frame takes one slot. A slot is a success when exactly
one station sends in it, idle when none sends, and a collision when two or more send.
"""

from fractions import Fraction
import math


def success_probability(n, p):
    """Exact probability that one slot is a success when n stations each send with probability p."""
    p = Fraction(p)
    return n * p * (1 - p) ** (n - 1)


def best_success_probability(n):
    """The maximum over p of success_probability(n, p). It is reached at p = 1/n."""
    return success_probability(n, Fraction(1, n))


def poisson_throughput(g, slotted=True):
    """Throughput S for a Poisson offered load of g frames per frame time.

    Slotted: S = g e^(-g). Pure (unslotted) ALOHA: S = g e^(-2g).
    """
    return g * math.exp(-g if slotted else -2 * g)


def slot_outcome(senders):
    """Feedback of one slot from the number of senders: 'idle', 'success' or 'collision'."""
    if senders == 0:
        return "idle"
    return "success" if senders == 1 else "collision"


def saturated_slotted_aloha(n, p, slots, rng):
    """Each of n stations always has a frame and sends it with probability p in each slot.

    Returns (per-station success counts, idle slots, collision slots).
    """
    wins = [0] * n
    idle = coll = 0
    for _ in range(slots):
        senders = [i for i in range(n) if rng.random() < p]
        out = slot_outcome(len(senders))
        if out == "success":
            wins[senders[0]] += 1
        elif out == "idle":
            idle += 1
        else:
            coll += 1
    return wins, idle, coll


def slotted_aloha_stations(arrivals, q, slots, rng):
    """The protocol of the page, run by each of a finite set of stations.

    arrivals[i] is the sorted list of the slots in which station i gets a new frame.
    Each station keeps a FIFO queue of [arrival slot, backlogged flag] entries.
    Returns the list of (station, arrival slot, delivery slot) for the frames delivered.
    """
    n = len(arrivals)
    queues = [[] for _ in range(n)]
    nxt = [0] * n
    done = []
    for t in range(slots):
        for i in range(n):
            while nxt[i] < len(arrivals[i]) and arrivals[i][nxt[i]] <= t:
                queues[i].append([arrivals[i][nxt[i]], False])
                nxt[i] += 1
        sent = []
        for i in range(n):
            if not queues[i]:  # @line L1
                continue
            frame = queues[i][0]  # @line L2
            if not frame[1]:  # @line L3 a new frame goes out in this slot
                sent.append(i)
            elif rng.random() < q:  # @line L4 a backlogged frame goes out with probability q
                sent.append(i)
        out = slot_outcome(len(sent))  # @line L5 the feedback that all stations read
        for i in sent:
            if out == "success":  # @line L6
                arrived, _ = queues[i].pop(0)
                done.append((i, arrived, t))
            else:
                queues[i][0][1] = True  # @line L7 the frame collided and is kept
    return done


def poisson_sample(lam, rng):
    """A Poisson(lam) sample by inversion of the distribution function."""
    k, prob = 0, math.exp(-lam)
    cum, u = prob, rng.random()
    while u > cum:
        k += 1
        prob *= lam / k
        cum += prob
    return k


def slotted_aloha(lam, slots, rng, q_r=None, backlog0=0):
    """Slotted ALOHA with infinitely many stations and Poisson(lam) new frames per slot.

    Plain rule (q_r a number): a new frame is sent in its first slot, and each
    backlogged frame is sent again in each slot with probability q_r.
    Pseudo-Bayesian rule (q_r None): every waiting frame, new or backlogged, is sent
    with probability min(1, 1/est); after the slot, est becomes est + lam + 1/(e - 2)
    on a collision and max(lam, est + lam - 1) on an idle slot or a success.
    Returns (frames delivered, backlog after each slot).
    """
    backlog = backlog0
    est = max(1.0, float(backlog0))
    delivered = 0
    trace = []
    for _ in range(slots):
        new = poisson_sample(lam, rng)
        if q_r is None:
            q = min(1.0, 1.0 / est)
            senders = sum(rng.random() < q for _ in range(backlog + new))
        else:
            senders = new + sum(rng.random() < q_r for _ in range(backlog))
        out = slot_outcome(senders)
        backlog += new
        if out == "success":
            backlog -= 1
            delivered += 1
        if q_r is None:
            est = est + lam + 1 / (math.e - 2) if out == "collision" else max(lam, est + lam - 1)
        trace.append(backlog)
    return delivered, trace
