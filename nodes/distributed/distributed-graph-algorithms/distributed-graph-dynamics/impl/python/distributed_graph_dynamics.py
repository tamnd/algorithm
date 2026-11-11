# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-graph-dynamics/. The authors are listed in prov/AN42TN.jsonl.

"""Token dissemination in dynamic networks with T-interval connectivity.

A dynamic graph on nodes 0..n-1 is a sequence of edge sets E(1), E(2), ...,
one per round. In round r every node broadcasts one message (here: at most
one token) to all its neighbours in E(r), without knowing who they are, and
receives the messages of its neighbours. The graph is T-interval connected
if for every T consecutive rounds the edges common to all of them form a
connected spanning subgraph.

An adversary is a function adversary(r, knows) that returns the edge set of
round r; it may look at the current knowledge of the nodes (adaptive).

Contents:
    is_t_interval_connected   brute-force check of a finite sequence
    t_interval_sequence       random T-interval connected sequences
    knowers_first_path        adaptive adversary: a path with the knowers first
    phased_dissemination      k phases of n - 1 rounds, broadcast min(A_v minus F_v)
    pipelined_dissemination   phases of 2T rounds; each node broadcasts the
                              smallest token not yet sent in the phase (after
                              Kuhn, Lynch and Oshman 2010, Section 6.1)
"""

import random

Edge = tuple[int, int]


def norm(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def connected(n: int, edges) -> bool:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    parts = n
    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            parts -= 1
    return parts <= 1


def is_t_interval_connected(n: int, graphs: list[set[Edge]], t: int) -> bool:
    """True if every window of t consecutive rounds has a connected common spanning subgraph."""
    if len(graphs) < t:
        return True
    for i in range(len(graphs) - t + 1):
        common = set(graphs[i])
        for g in graphs[i + 1 : i + t]:
            common &= g
        if not connected(n, common):
            return False
    return True


def random_tree(n: int, rng: random.Random) -> set[Edge]:
    order = list(range(n))
    rng.shuffle(order)
    return {norm(order[i], order[rng.randrange(i)]) for i in range(1, n)}


def t_interval_sequence(n: int, t: int, rounds: int, seed: int, p: float = 0.1) -> list[set[Edge]]:
    """Rounds are cut into blocks of t; every round of block b contains the trees of blocks b and b + 1.

    A window of t rounds meets at most two consecutive blocks b and b + 1,
    and all its rounds contain tree b + 1 (or tree b, if it meets one block).
    Extra random edges change from round to round.
    """
    rng = random.Random(seed)
    trees = [random_tree(n, rng) for _ in range(rounds // t + 2)]
    graphs = []
    for r in range(rounds):
        b = r // t
        g = set(trees[b]) | trees[b + 1]
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < p:
                    g.add((u, v))
        graphs.append(g)
    return graphs


def from_list(graphs: list[set[Edge]]):
    return lambda r, knows: graphs[r - 1]


def knowers_first_path(token: int):
    """A path that lists the nodes that know `token` first: one new knower per round at most."""

    def adversary(r: int, knows: list[set[int]]) -> set[Edge]:
        n = len(knows)
        order = sorted(range(n), key=lambda v: (token not in knows[v], v))
        return {norm(order[i], order[i + 1]) for i in range(n - 1)}

    return adversary


def fewest_tokens_path():
    """A path ordered by the number of known tokens: tries to slow down every token."""

    def adversary(r: int, knows: list[set[int]]) -> set[Edge]:
        n = len(knows)
        order = sorted(range(n), key=lambda v: (-len(knows[v]), v))
        return {norm(order[i], order[i + 1]) for i in range(n - 1)}

    return adversary


def broadcast_round(n, edges, send, knows):
    """Each node v with send[v] not None broadcasts it to all its neighbours in this round."""
    heard = [[] for _ in range(n)]
    for u, v in edges:
        if send[u] is not None:
            heard[v].append(send[u])
        if send[v] is not None:
            heard[u].append(send[v])
    for v in range(n):
        knows[v].update(heard[v])
    return sum(1 for x in send if x is not None)


def phased_dissemination(n: int, inputs: list[set[int]], k: int, adversary) -> dict:
    """k phases of n - 1 rounds. In every round of a phase, node v broadcasts min(A_v minus F_v).

    At the end of a phase, v adds min(A_v minus F_v) to F_v. On every
    1-interval connected graph, after phase j every node knows the j smallest
    tokens and has F_v equal to them. Returns the round in which every node
    knew every token, the total rounds and the number of broadcasts.
    """
    knows = [set(a) for a in inputs]
    done = [set() for _ in range(n)]
    allt = set().union(*inputs)
    first_full = 0 if all(a == allt for a in knows) else None
    r = 0
    sends = 0
    for _ in range(k):
        for _ in range(n - 1):
            r += 1
            send = [min(knows[v] - done[v]) if knows[v] - done[v] else None for v in range(n)]
            sends += broadcast_round(n, adversary(r, knows), send, knows)
            if first_full is None and all(a == allt for a in knows):
                first_full = r
        for v in range(n):
            rest = knows[v] - done[v]
            if rest:
                done[v].add(min(rest))
    return {"knows": knows, "done": done, "rounds": r, "first_full": first_full, "broadcasts": sends}


def pipelined_dissemination(n: int, inputs: list[set[int]], t: int, phases: int, adversary) -> dict:
    """Phases of 2t rounds; in each round a node broadcasts its smallest token not yet sent in this phase.

    Kuhn, Lynch and Oshman (2010, Section 6.1) show that on 2t-interval
    connected graphs, after ceil(n / t) phases every node knows the t
    smallest tokens.
    """
    knows = [set(a) for a in inputs]
    r = 0
    for _ in range(phases):
        sent = [set() for _ in range(n)]
        for _ in range(2 * t):
            r += 1
            send = []
            for v in range(n):
                rest = knows[v] - sent[v]
                x = min(rest) if rest else None
                if x is not None:
                    sent[v].add(x)
                send.append(x)
            broadcast_round(n, adversary(r, knows), send, knows)
    return {"knows": knows, "rounds": r}
