# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/store-and-forward/. The authors are listed in prov/TC3XFV.jsonl.

"""An event-driven simulation of store-and-forward switching.

Each link has a rate (bits per second) and a propagation delay, and serves
its packets one at a time in FIFO order. A node may start to send a packet
on its next link only after the whole packet has arrived: that is the
store-and-forward rule. The simulator returns the time at which each packet
has fully arrived at its destination.
"""

import heapq
import math


class Link:
    __slots__ = ("rate", "prop", "queue", "busy")

    def __init__(self, rate, prop=0.0):
        self.rate, self.prop = rate, prop
        self.queue, self.busy = [], False


def simulate(links, packets):
    """links: dict name -> Link. packets: list of (inject time, size in bits,
    route as a list of link names). Returns the list of arrival times at the
    end of each route, in the order of the packets."""
    events, seq = [], 0
    done = [None] * len(packets)

    def push(t, kind, k, hop):
        nonlocal seq
        heapq.heappush(events, (t, seq, kind, k, hop))
        seq += 1

    def start(name, t):
        link = links[name]
        if link.busy or not link.queue:
            return
        k, hop = link.queue.pop(0)
        link.busy = True
        push(t + packets[k][1] / link.rate, "sent", k, hop)

    for k, (t0, _, route) in enumerate(packets):
        push(t0, "stored", k, 0)
    while events:
        t, _, kind, k, hop = heapq.heappop(events)
        route = packets[k][2]
        if kind == "stored":
            # the whole packet is in this node's buffer
            if hop == len(route):
                done[k] = t
                continue
            links[route[hop]].queue.append((k, hop))
            start(route[hop], t)
        else:
            # the last bit has left; it arrives after the propagation delay
            link = links[route[hop]]
            link.busy = False
            push(t + link.prop, "stored", k, hop + 1)
            start(route[hop], t)
    return done


def path(h, rate, prop=0.0):
    """A chain of h equal links, named 0 .. h-1."""
    return {i: Link(rate, prop) for i in range(h)}, list(range(h))


def message_time(M, p, H, h, R):
    """Time to send a message of M bits as packets of p payload bits plus an
    H-bit header over h equal store-and-forward links of rate R, with no
    propagation delay: (h - 1 + ceil(M / p)) (p + H) / R when p divides M."""
    n = math.ceil(M / p)
    return (h - 1 + n) * (p + H) / R


def best_payload(M, H, h):
    """The payload that minimizes (h - 1 + M/p)(p + H): sqrt(M H / (h - 1))."""
    if h <= 1:
        return M
    return math.sqrt(M * H / (h - 1))
