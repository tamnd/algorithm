# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-mapreduce/. The authors are listed in prov/T3JHYW.jsonl.
"""Iterative MapReduce: a driver runs one MapReduce job per iteration and
feeds the output of round t into round t + 1, until a stop test holds.

The job runner counts, for each round, the records that the mappers emit
(the shuffle volume) and the largest reducer input. Two programs:
  PageRank, with the graph either re-sent in every round (plain MapReduce)
  or cached at the reducers (the loop-invariant cache of HaLoop);
  connected components by minimum-label propagation.
"""


def map_reduce(records, mapper, reducer, keys=()):
    """One round. mapper(record) yields (key, value); reducer(key, values)
    yields output records. The reducer also runs, with an empty list, on each
    key in keys that got no value (the keys of a reducer-side cache).
    Returns (output, emitted, largest reducer input)."""
    groups = {k: [] for k in keys}
    emitted = 0
    for rec in records:
        for k, v in mapper(rec):
            groups.setdefault(k, []).append(v)
            emitted += 1
    out = []
    for k in sorted(groups):
        out.extend(reducer(k, groups[k]))
    biggest = max((len(v) for v in groups.values()), default=0)
    return out, emitted, biggest


# ---------------------------------------------------------------- PageRank


def pagerank_rounds(adj, alpha, rounds, cache_graph=False):
    """adj[u] is the list of out-neighbours of u; every vertex needs at least
    one. alpha is the follow probability. Each record is (u, rank, out-list).
    Without the cache, each mapper re-emits the out-list of u so that the
    reducer can rebuild the record: n + m records per round. With the cache
    the reducers keep the graph from round 1 on: m records per round.
    Returns (ranks, emitted records per round)."""
    n = len(adj)
    one = alpha - alpha + 1
    state = [(u, one / n, adj[u]) for u in range(n)]
    cache = {u: adj[u] for u in range(n)}  # the reducer-side cache
    volume = []

    def mapper(rec):
        u, x, out = rec
        if not cache_graph:
            yield u, ("graph", out)
        for v in out:
            yield v, ("rank", x / len(out))

    def reducer(v, values):
        total = 0
        out = cache[v]
        for kind, val in values:
            if kind == "graph":
                out = val
            else:
                total += val
        yield v, (1 - alpha) / n + alpha * total, out

    # With the cache, a vertex with no in-edges gets no record, but the
    # reducer still knows it from the cache and must output it.
    keys = range(n) if cache_graph else ()
    for _ in range(rounds):
        state, emitted, _ = map_reduce(state, mapper, reducer, keys)
        volume.append(emitted)
    ranks = [0] * n
    for u, x, _ in state:
        ranks[u] = x
    return ranks, volume


def rounds_for_error(alpha, eps):
    """The least k with 2 alpha^k <= eps: enough rounds for an L1 error at
    most eps, from the uniform start."""
    k = 0
    while 2 * alpha ** k > eps:
        k += 1
    return k


# ---------------------------------------------------------------- components


def min_label_components(n, edges):
    """Each round: every vertex sends its label to its neighbours and keeps
    the smallest label it sees. The driver stops after the first round in
    which no label changes. Returns (labels, rounds)."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    state = [(v, v) for v in range(n)]
    rounds = 0

    def mapper(rec):
        v, lab = rec
        yield v, lab
        for w in adj[v]:
            yield w, lab

    def reducer(v, labels):
        yield v, min(labels)

    while True:
        new, _, _ = map_reduce(state, mapper, reducer)
        rounds += 1
        if new == state:
            return [lab for _, lab in new], rounds
        state = new
