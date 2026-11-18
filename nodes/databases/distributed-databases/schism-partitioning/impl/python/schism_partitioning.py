# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schism-partitioning/. The authors are listed in prov/RGG5F9.jsonl.

"""Schism: workload-driven partitioning and replication of the tuples of a database.

A workload is a list of transactions. A transaction is a pair (reads, writes) of
frozensets of tuple ids; a tuple that is both read and written counts as written.
A placement maps each tuple id to the nonempty set of the parts (0 .. k-1) that
hold a copy of it.

A transaction is local under a placement when one part holds a copy of every
tuple it touches and every tuple it writes has exactly one copy (a write must
update all copies). Otherwise it is distributed. Schism tries to find a placement
with few distributed transactions and balanced parts:

1. build a graph with a node per tuple and an edge for each pair of tuples that
   a transaction touches together (weight: the number of such transactions);
2. with replication, replace each tuple by a star: a center and one replica node
   per transaction that touches it, joined by edges whose weight is the number
   of transactions that write the tuple;
3. cut the graph into k balanced parts with a small total weight of cut edges;
4. read the placement off the parts;
5. learn a decision tree that predicts the placement of a tuple from its
   attributes (a set of range predicates);
6. count the distributed transactions of the lookup table, the tree, hash
   partitioning and full replication, and keep the best.

Step 3 uses METIS in the paper. Here a small balanced k-way local search (single
moves and swaps, from several random starts) takes its place.
"""

from __future__ import annotations

import math
import random
import zlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from itertools import combinations, product
from collections.abc import Hashable, Iterable, Mapping, Sequence

Txn = tuple[frozenset, frozenset]
Placement = dict[Hashable, frozenset]


def make_txn(reads: Iterable = (), writes: Iterable = ()) -> Txn:
    w = frozenset(writes)
    return (frozenset(reads) - w, w)


def touched(x: Txn) -> frozenset:
    return x[0] | x[1]


def stable_hash(v) -> int:
    return zlib.crc32(repr(v).encode())


def _ordered(items: Iterable) -> list:
    return sorted(items, key=repr)


# ---------------------------------------------------------------- graphs


@dataclass
class Graph:
    weight: dict = field(default_factory=dict)   # node -> node weight (its number of accesses)
    edges: Counter = field(default_factory=Counter)  # frozenset({u, v}) -> edge weight

    def add_edge(self, u, v, w: int = 1) -> None:
        if u == v or w == 0:
            return
        self.edges[frozenset((u, v))] += w


def build_graph(workload: Sequence[Txn]) -> Graph:
    """A node per tuple, weighted by the number of transactions that touch it; an edge
    per pair of tuples, weighted by the number of transactions that touch both."""
    g = Graph()
    for x in workload:
        ts = _ordered(touched(x))
        for t in ts:
            g.weight[t] = g.weight.get(t, 0) + 1
        for u, v in combinations(ts, 2):
            g.add_edge(u, v)
    return g


def build_replicated_graph(workload: Sequence[Txn]) -> Graph:
    """The graph with replication: tuple t becomes a center ('c', t) of weight 0 and a
    replica ('r', t, i) of weight 1 for each transaction i that touches t. The star edges
    weigh the number of transactions that write t; the edges of transaction i join its
    replicas with weight 1."""
    writes = Counter(t for x in workload for t in x[1])
    g = Graph()
    for i, x in enumerate(workload):
        ts = _ordered(touched(x))
        for t in ts:
            g.weight[("c", t)] = 0
            g.weight[("r", t, i)] = 1
            g.add_edge(("c", t), ("r", t, i), writes[t])
        for u, v in combinations(ts, 2):
            g.add_edge(("r", u, i), ("r", v, i))
    return g


def cut_weight(g: Graph, part: Mapping) -> int:
    total = 0
    for e, w in g.edges.items():
        u, v = tuple(e)
        if part[u] != part[v]:
            total += w
    return total


def placement_from(g: Graph, part: Mapping, replicated: bool) -> Placement:
    """Read the placement of the tuples off a partition of the graph."""
    if not replicated:
        return {t: frozenset([part[t]]) for t in g.weight}
    out: dict = defaultdict(set)
    for node in g.weight:
        out[node[1]].add(part[node])
    return {t: frozenset(s) for t, s in out.items()}


# ---------------------------------------------------------------- partitioner


def _greedy_start(nodes: Sequence, weight: Mapping, k: int) -> tuple[dict, list[int]]:
    """Largest weight first, each node to the lightest part (lowest index on a tie)."""
    load = [0] * k
    part = {}
    for v in sorted(nodes, key=lambda v: -weight[v]):  # stable: ties keep the given order
        q = min(range(k), key=lambda j: (load[j], j))
        part[v] = q
        load[q] += weight[v]
    return part, load


def balance_cap(weight: Mapping, k: int, eps: float) -> float:
    """The largest allowed load of a part: (1 + eps) W / k, raised to the largest load
    of the greedy start if that is higher (so that a balanced partition always exists)."""
    if not weight:
        return 0
    total = sum(weight.values())
    _, load = _greedy_start(_ordered(weight), weight, k)
    return max((1 + eps) * total / k, max(load))


def _connections(g: Graph, part: Mapping, k: int) -> dict:
    conn = {v: [0] * k for v in g.weight}
    for e, w in g.edges.items():
        u, v = tuple(e)
        conn[u][part[v]] += w
        conn[v][part[u]] += w
    return conn


def _best_step(g: Graph, part: dict, load: list, conn: dict, cap: float, nodes: Sequence):
    """The single move or swap that keeps every load at most cap and lowers the cut most."""
    w = g.weight
    best_gain, best = 0, None
    for u in nodes:
        a = part[u]
        for q in range(len(load)):
            if q != a and load[q] + w[u] <= cap:
                gain = conn[u][q] - conn[u][a]
                if gain > best_gain:
                    best_gain, best = gain, ((u, q),)
    # A swap of two nodes that have no neighbor outside their own parts cannot lower the
    # cut, so one end of a useful swap is a boundary node.
    boundary = [u for u in nodes if conn[u][part[u]] < sum(conn[u])]
    for u in boundary:
        for v in nodes:
            a, b = part[u], part[v]
            if a == b:
                continue
            if load[a] - w[u] + w[v] > cap or load[b] - w[v] + w[u] > cap:
                continue
            wuv = g.edges.get(frozenset((u, v)), 0)
            gain = conn[u][b] - conn[u][a] + conn[v][a] - conn[v][b] - 2 * wuv
            if gain > best_gain:
                best_gain, best = gain, ((u, b), (v, a))
    return best


def local_search(g: Graph, part: dict, k: int, cap: float) -> dict:
    """Apply the best improving move or swap until none is left. The cut drops by at
    least 1 per step, so this ends."""
    part = dict(part)
    nodes = _ordered(g.weight)
    load = [0] * k
    for v in nodes:
        load[part[v]] += g.weight[v]
    while True:
        conn = _connections(g, part, k)
        step = _best_step(g, part, load, conn, cap, nodes)
        if step is None:
            return part
        for v, q in step:
            load[part[v]] -= g.weight[v]
            load[q] += g.weight[v]
            part[v] = q


def _loads(g: Graph, part: Mapping, k: int) -> list:
    load = [0] * k
    for v, q in part.items():
        load[q] += g.weight[v]
    return load


def coarsen(g: Graph, rng: random.Random, limit: float) -> tuple[Graph, dict]:
    """One level of heavy edge matching: visit the nodes in random order and match each
    free node with the free neighbor of the heaviest edge, if the pair weighs at most limit.
    Return the contracted graph and the map from the nodes of g to the coarse nodes."""
    adj: dict = defaultdict(dict)
    for e, w in g.edges.items():
        u, v = tuple(e)
        adj[u][v] = w
        adj[v][u] = w
    nodes = _ordered(g.weight)
    rng.shuffle(nodes)
    mate = {}
    for u in nodes:
        if u in mate:
            continue
        best = None
        for v in _ordered(adj[u]):
            if v not in mate and g.weight[u] + g.weight[v] <= limit:
                if best is None or adj[u][v] > adj[u][best]:
                    best = v
        mate[u] = u if best is None else best
        if best is not None:
            mate[best] = u
    cmap, count = {}, 0
    for u in nodes:
        if u not in cmap:
            cmap[u] = cmap[mate[u]] = count
            count += 1
    coarse = Graph()
    for u in nodes:
        coarse.weight[cmap[u]] = coarse.weight.get(cmap[u], 0) + g.weight[u]
    for e, w in g.edges.items():
        u, v = tuple(e)
        coarse.add_edge(cmap[u], cmap[v], w)
    return coarse, cmap


def _rebalance(g: Graph, part: dict, k: int, cap: float) -> dict:
    """Move nodes out of parts above cap, the least harmful move first."""
    part = dict(part)
    load = _loads(g, part, k)
    while max(load) > cap:
        conn = _connections(g, part, k)
        a = max(range(k), key=lambda j: load[j])
        best = None
        for u in _ordered(v for v in g.weight if part[v] == a and g.weight[v] > 0):
            for q in range(k):
                if q != a and load[q] + g.weight[u] <= cap:
                    gain = conn[u][q] - conn[u][a]
                    if best is None or gain > best[0]:
                        best = (gain, u, q)
        if best is None:
            return part
        _, u, q = best
        load[a] -= g.weight[u]
        load[q] += g.weight[u]
        part[u] = q
    return part


def multilevel(g: Graph, k: int, cap: float, rng: random.Random) -> dict:
    """Coarsen by heavy edge matching, partition the small graph, then project the
    partition back level by level and refine it with local search at each level."""
    levels, cur = [], g
    while len(cur.weight) > max(2 * k, 8):
        coarse, cmap = coarsen(cur, rng, cap / 2)
        if len(coarse.weight) > 0.9 * len(cur.weight):
            break
        levels.append((cur, cmap))
        cur = coarse
    order = _ordered(cur.weight)
    rng.shuffle(order)
    part = local_search(cur, _greedy_start(order, cur.weight, k)[0], k, cap)
    for fine, cmap in reversed(levels):
        part = {v: part[cmap[v]] for v in fine.weight}
        part = local_search(fine, _rebalance(fine, part, k, cap), k, cap)
    if max(_loads(g, part, k)) > cap:  # the projection could not be balanced: start at the finest level
        part = local_search(g, _greedy_start(_ordered(g.weight), g.weight, k)[0], k, cap)
    return part


def partition(g: Graph, k: int, eps: float = 0.1, seed: int = 0, restarts: int = 4) -> dict:
    """A balanced k-way partition with a small cut, in the style of METIS: multilevel
    runs from several random seeds; keep the best. A heuristic."""
    if k < 1:
        raise ValueError("k must be at least 1")
    if not g.weight:
        return {}
    cap = balance_cap(g.weight, k, eps)
    rng = random.Random(seed)
    best, best_cut = None, None
    for _ in range(max(1, restarts)):
        part = multilevel(g, k, cap, rng)
        c = cut_weight(g, part)
        if best is None or c < best_cut:
            best, best_cut = part, c
    return best


def brute_force_partition(g: Graph, k: int, eps: float = 0.1) -> tuple[int, dict]:
    """The smallest cut over all partitions that respect the same cap (tiny graphs only)."""
    nodes = _ordered(g.weight)
    if len(nodes) > 10:
        raise ValueError("brute force is for at most 10 nodes")
    cap = balance_cap(g.weight, k, eps)
    best = None
    for labels in product(range(k), repeat=len(nodes)):
        load = [0] * k
        for v, q in zip(nodes, labels):
            load[q] += g.weight[v]
        if max(load, default=0) > cap:
            continue
        part = dict(zip(nodes, labels))
        c = cut_weight(g, part)
        if best is None or c < best[0]:
            best = (c, part)
    return best


# ---------------------------------------------------------------- cost of a placement


def is_distributed(x: Txn, placement: Mapping) -> bool:
    reads, writes = x
    for t in writes:
        if len(placement[t]) != 1:
            return True
    common = None
    for t in touched(x):
        common = set(placement[t]) if common is None else common & placement[t]
        if not common:
            return True
    return False


def distributed_count(workload: Sequence[Txn], placement: Mapping) -> int:
    return sum(1 for x in workload if is_distributed(x, placement))


def hash_placement(ids: Iterable, k: int, h=stable_hash) -> Placement:
    return {t: frozenset([h(t) % k]) for t in ids}


def replication_placement(ids: Iterable, k: int) -> Placement:
    return {t: frozenset(range(k)) for t in ids}


# ---------------------------------------------------------------- explanation


def _entropy(labels: Counter) -> float:
    n = sum(labels.values())
    return -sum(c / n * math.log2(c / n) for c in labels.values() if c)


def _label_key(label) -> tuple:
    return tuple(sorted(label)) if isinstance(label, (set, frozenset)) else (label,)


def _majority(labels: Counter):
    return min(labels, key=lambda lab: (-labels[lab], _label_key(lab)))


def train_tree(rows: Sequence[Mapping], labels: Sequence, max_depth: int | None = None, depth: int = 0):
    """A decision tree on numeric attributes. A leaf is ('leaf', label). A split is
    ('split', attr, thr, left, right): rows with row[attr] <= thr go left. Each split has
    the largest information gain among the splits with two nonempty sides; an impure
    node is split even when the gain is 0, so that distinct rows end in pure leaves."""
    counts = Counter(labels)
    if len(counts) <= 1 or (max_depth is not None and depth >= max_depth):
        return ("leaf", _majority(counts))
    base = _entropy(counts)
    n = len(rows)
    best = None
    for attr in sorted(rows[0]):
        values = sorted({r[attr] for r in rows})
        for thr in values[:-1]:
            left = Counter(lab for r, lab in zip(rows, labels) if r[attr] <= thr)
            right = counts - left
            nl = sum(left.values())
            gain = base - nl / n * _entropy(left) - (n - nl) / n * _entropy(right)
            if best is None or gain > best[0] + 1e-12:
                best = (gain, attr, thr)
    if best is None:  # all rows are equal on every attribute
        return ("leaf", _majority(counts))
    _, attr, thr = best
    li = [i for i, r in enumerate(rows) if r[attr] <= thr]
    ri = [i for i, r in enumerate(rows) if r[attr] > thr]
    return ("split", attr, thr,
            train_tree([rows[i] for i in li], [labels[i] for i in li], max_depth, depth + 1),
            train_tree([rows[i] for i in ri], [labels[i] for i in ri], max_depth, depth + 1))


def predict(tree, row: Mapping):
    while tree[0] == "split":
        _, attr, thr, left, right = tree
        tree = left if row[attr] <= thr else right
    return tree[1]


def tree_rules(tree, path: tuple = ()) -> list[tuple[tuple, object]]:
    """The tree as a list of (conjunction of range predicates, label)."""
    if tree[0] == "leaf":
        return [(path, tree[1])]
    _, attr, thr, left, right = tree
    return tree_rules(left, path + ((attr, "<=", thr),)) + tree_rules(right, path + ((attr, ">", thr),))


# ---------------------------------------------------------------- Schism


SIMPLICITY = ("hash", "replication", "tree", "lookup")


@dataclass
class Result:
    choice: str
    costs: dict
    placements: dict
    part: dict
    graph: Graph
    tree: object


def schism(db: Mapping[Hashable, Mapping], workload: Sequence[Txn], k: int, replicate: bool = True,
           eps: float = 0.1, seed: int = 0, restarts: int = 4, max_depth: int | None = None,
           h=stable_hash) -> Result:
    """db maps each tuple id to its attributes (numbers). Return the chosen strategy, the
    number of distributed transactions of each candidate, and the placements."""
    for x in workload:
        missing = touched(x) - db.keys()
        if missing:
            raise KeyError(f"transaction touches unknown tuples {sorted(missing, key=repr)}")
    ids = _ordered(db)
    g = build_graph(workload)  # @line L1
    if replicate:
        g = build_replicated_graph(workload)  # @line L2
    part = partition(g, k, eps, seed, restarts)  # @line L3
    from_graph = placement_from(g, part, replicate)  # @line L4
    lookup = hash_placement(ids, k, h)  # tuples that no transaction touches fall back to hashing
    lookup.update(from_graph)
    seen = [t for t in ids if t in from_graph]
    tree = train_tree([db[t] for t in seen], [lookup[t] for t in seen], max_depth) if seen else ("leaf", frozenset([0]))  # @line L5
    placements = {
        "hash": hash_placement(ids, k, h),
        "replication": replication_placement(ids, k),
        "tree": {t: frozenset(predict(tree, db[t])) for t in ids},
        "lookup": lookup,
    }
    costs = {name: distributed_count(workload, p) for name, p in placements.items()}  # @line L6
    choice = min(SIMPLICITY, key=lambda name: (costs[name], SIMPLICITY.index(name)))
    return Result(choice, costs, placements, part, g, tree)  # @line L7
