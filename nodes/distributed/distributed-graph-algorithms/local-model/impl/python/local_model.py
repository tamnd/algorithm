# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-model/. The authors are listed in prov/Y75PP5.jsonl.

"""A deterministic synchronous round simulator for the LOCAL and CONGEST models.

The network is an adjacency list adj: adj[v][i] is the neighbour of v behind
port i of v. Every node v has a unique identifier ids[v] and an input
inputs[v]. At the start a node knows its identifier, its input and its
degree, but not the identifiers of its neighbours.

An algorithm is an object with three methods:

    init(ident, inp, deg)     -> the initial state of a node
    send(state, rnd)          -> a list with one message per port; None means no message
    receive(state, rnd, inbox) -> the new state; inbox[i] is the message that arrived on port i

In one round every node sends, then every node receives, then every node
computes. In LOCAL mode a message can be any value. In CONGEST mode every
message must fit in c * ceil(log2(n + 1)) bits of a fixed encoding (see
bits()); a longer message raises CongestViolation.

Also here: the full-information algorithm, the radius-r ball of a node and
the view computed from the ball alone, and an algorithm that collects the
whole graph and detects that it has done so after ecc(v) + 1 rounds.
"""

from collections import deque


class CongestViolation(Exception):
    pass


def gamma_len(k: int) -> int:
    """Length of the Elias gamma code of a positive integer k."""
    return 2 * (k.bit_length() - 1) + 1


def bits(msg: object) -> int:
    """Length of a self-delimiting encoding of msg.

    Each value has a 2-bit type tag. A bool has 1 more bit. An integer x is
    sent as the gamma code of its zigzag image plus 1. A tuple, list or
    frozenset is sent as the gamma code of its length plus 1, then its items
    (a set in sorted order). Strings are not allowed.
    """
    total = 0
    stack = [msg]
    while stack:
        x = stack.pop()
        total += 2
        if isinstance(x, bool):
            total += 1
        elif isinstance(x, int):
            z = 2 * x if x >= 0 else -2 * x - 1
            total += gamma_len(z + 1)
        elif isinstance(x, (tuple, list, frozenset)):
            total += gamma_len(len(x) + 1)
            stack.extend(x)
        else:
            raise TypeError(f"cannot encode {type(x).__name__}")
    return total


def budget(n: int, c: int) -> int:
    return c * max(1, n.bit_length())


def back_ports(adj: list[list[int]]) -> list[list[int]]:
    """back[v][i] is the port of adj[v][i] that leads back to v."""
    where = [{w: j for j, w in enumerate(nbrs)} for nbrs in adj]
    return [[where[w][v] for w in adj[v]] for v in range(len(adj))]


def run(adj, ids, inputs, alg, rounds, mode="LOCAL", c=None, stop=None):
    """Run alg for the given number of rounds, or until stop(states) is true.

    Returns (states, stats) where stats has the number of rounds, the number
    of messages and the largest message length in bits.
    """
    n = len(adj)
    assert len(set(ids)) == n, "identifiers must be unique"
    back = back_ports(adj)
    limit = budget(n, c) if mode == "CONGEST" else None
    states = [alg.init(ids[v], inputs[v], len(adj[v])) for v in range(n)]
    stats = {"rounds": 0, "messages": 0, "max_bits": 0}
    for rnd in range(1, rounds + 1):
        if stop is not None and stop(states):
            break
        inbox = [[None] * len(adj[v]) for v in range(n)]
        for v in range(n):
            out = alg.send(states[v], rnd)
            assert len(out) == len(adj[v])
            for i, msg in enumerate(out):
                if msg is None:
                    continue
                b = bits(msg)
                if limit is not None and b > limit:
                    raise CongestViolation(f"round {rnd}, node {v}, port {i}: {b} bits > {limit}")
                stats["messages"] += 1
                stats["max_bits"] = max(stats["max_bits"], b)
                inbox[adj[v][i]][back[v][i]] = msg
        states = [alg.receive(states[v], rnd, inbox[v]) for v in range(n)]
        stats["rounds"] = rnd
    return states, stats


# ----------------------------------------------------------------------------
# The full-information algorithm and the radius-r ball.


class FullInfo:
    """Each node sends its whole state on every port; the state after r rounds is the view."""

    def init(self, ident, inp, deg):
        return (ident, inp, deg)

    def send(self, state, rnd):
        return [state] * state[2]

    def receive(self, state, rnd, inbox):
        ident, inp, deg = state[0], state[1], state[2]
        return (ident, inp, deg, tuple(inbox))


def distances(adj, s, limit=None):
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        if limit is not None and dist[u] == limit:
            continue
        for w in adj[u]:
            if w not in dist:
                dist[w] = dist[u] + 1
                q.append(w)
    return dist


def ball_view(adj, ids, inputs, v, r):
    """The radius-r ball of v, as v can know it after r rounds.

    It has the identifier, input and degree of every node at distance at most
    r, and the port-ordered neighbour list of every node at distance at most
    r - 1. Node names are positions in adj; the view built from it uses only
    identifiers, inputs, degrees and port order.
    """
    dist = distances(adj, v, r)
    nodes = {u: (ids[u], inputs[u], len(adj[u])) for u in dist}
    edges = {u: tuple(adj[u]) for u in dist if dist[u] <= r - 1}
    return {"center": v, "radius": r, "dist": dist, "nodes": nodes, "edges": edges}


def view_from_ball(ball):
    """Compute what FullInfo holds at the centre after r rounds, from the ball alone."""
    r, dist, nodes, edges = ball["radius"], ball["dist"], ball["nodes"], ball["edges"]
    level = {u: nodes[u] for u in nodes}  # states after 0 rounds, for dist <= r
    for k in range(1, r + 1):
        level = {
            u: nodes[u] + (tuple(level[w] for w in edges[u]),)
            for u in nodes
            if dist[u] <= r - k
        }
    return level[ball["center"]]


# ----------------------------------------------------------------------------
# Collect the whole graph and detect it: every problem in O(D) rounds.


class Gather:
    """Learn the whole graph; a node is done after exactly ecc(v) + 1 rounds.

    State: (ident, inp, deg, nbr_ids, known, done_round) where known maps an
    identifier to (input, tuple of neighbour identifiers in port order).
    Round 1 sends the own identifier; later rounds send all known records.
    """

    def init(self, ident, inp, deg):
        return (ident, inp, deg, None, {}, None)

    def send(self, state, rnd):
        ident, _, deg, nbr_ids, known, _ = state
        if rnd == 1:
            return [ident] * deg
        return [tuple(sorted((u, rec) for u, rec in known.items()))] * deg

    def receive(self, state, rnd, inbox):
        ident, inp, deg, nbr_ids, known, done = state
        known = dict(known)
        if rnd == 1:
            nbr_ids = tuple(inbox)
            known[ident] = (inp, nbr_ids)
        else:
            for msg in inbox:
                for u, rec in msg:
                    known[u] = rec
        if done is None and all(w in known for rec in known.values() for w in rec[1]):
            done = rnd
        return (ident, inp, deg, nbr_ids, known, done)


def all_done(states):
    return all(s[5] is not None for s in states)


def greedy_colouring(known):
    """The same colouring at every node: greedy in the order of identifiers."""
    colour = {}
    for u in sorted(known):
        used = {colour[w] for w in known[u][1] if w in colour}
        c = 0
        while c in used:
            c += 1
        colour[u] = c
    return colour


# ----------------------------------------------------------------------------
# A small CONGEST-friendly algorithm: synchronous BFS from the node with input 1.


class SyncBFS:
    """The root (input 1) sends 0 in round 1; a node that first hears d - 1 sets dist d and sends d."""

    def init(self, ident, inp, deg):
        return (deg, 0 if inp == 1 else None, inp == 1)

    def send(self, state, rnd):
        deg, d, fresh = state
        return [d] * deg if fresh else [None] * deg

    def receive(self, state, rnd, inbox):
        deg, d, _ = state
        if d is None:
            heard = [x for x in inbox if x is not None]
            if heard:
                return (deg, min(heard) + 1, True)
        return (deg, d, False)
