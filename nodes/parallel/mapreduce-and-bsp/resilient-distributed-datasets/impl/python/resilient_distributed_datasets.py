# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resilient-distributed-datasets/. The authors are listed in prov/RWTK7Z.jsonl.
"""A small model of resilient distributed datasets (RDDs).

An RDD is a read-only list of partitions. It knows its parents and how to
compute partition i from them (its lineage). Nothing is computed until an
action (collect) asks for it. A persisted RDD keeps its computed partitions
in memory; a failure drops some of them, and the next action computes them
again from the lineage. A checkpoint writes an RDD to stable storage and cuts
its lineage. The counter `computed[rdd.name]` counts partition computations.

Dependencies:
  narrow: partition i of the child needs only partition i of each parent
          (map, filter, mapValues, join of co-partitioned inputs);
  wide:   a partition of the child needs all partitions of the parent
          (partitionBy, reduceByKey, join of inputs that are not co-partitioned).
          The parent partitions are stored once as shuffle outputs, so each
          is computed once and not once for each child partition.
Keys are integers, and the hash partitioner puts key k in partition k mod n.
"""


class Context:
    def __init__(self):
        self.cache = {}       # (rdd id, partition) -> list, in memory
        self.shuffle = {}     # (child id, side, parent partition) -> list, map-side shuffle output
        self.stable = {}      # (rdd id, partition) -> list, checkpointed
        self.computed = {}    # rdd name -> number of partition computations
        self.next_id = 0

    def parallelize(self, data, n, name="input"):
        parts = [data[(i * len(data)) // n:((i + 1) * len(data)) // n] for i in range(n)]
        return RDD(self, name, n, [], lambda i: list(parts[i]), partitioner=None)

    def lose(self, rng, fraction):
        """A failure: each cached partition and each shuffle output is lost
        with the given probability. Returns the number of lost cached
        partitions. Stable storage is never lost."""
        lost = [k for k in sorted(self.cache) if rng.random() < fraction]
        for k in lost:
            del self.cache[k]
        for k in [k for k in sorted(self.shuffle) if rng.random() < fraction]:
            del self.shuffle[k]
        return len(lost)


class RDD:
    def __init__(self, ctx, name, n, deps, fn, partitioner):
        self.ctx, self.name, self.n = ctx, name, n
        self.deps = deps              # list of (parent, "narrow" or "wide")
        self.fn = fn                  # i -> list of records, from the parents
        self.partitioner = partitioner
        self.persisted = False
        self.id = ctx.next_id
        ctx.next_id += 1

    # ---- evaluation

    def partition(self, i):
        key = (self.id, i)
        if key in self.ctx.stable:
            return self.ctx.stable[key]
        if key in self.ctx.cache:
            return self.ctx.cache[key]
        self.ctx.computed[self.name] = self.ctx.computed.get(self.name, 0) + 1
        out = self.fn(i)
        if self.persisted:
            self.ctx.cache[key] = out
        return out

    def collect(self):
        return [x for i in range(self.n) for x in self.partition(i)]

    def persist(self):
        self.persisted = True
        return self

    def checkpoint(self):
        """Write all partitions to stable storage and forget the lineage."""
        for i in range(self.n):
            self.ctx.stable[(self.id, i)] = self.partition(i)
        self.deps = []
        self.fn = None
        return self

    def lineage_depth(self):
        return 1 + max((p.lineage_depth() for p, _ in self.deps), default=0)

    # ---- narrow transformations

    def map(self, f, name=None):
        return RDD(self.ctx, name or self.name + ".map", self.n, [(self, "narrow")],
                   lambda i: [f(x) for x in self.partition(i)], None)

    def filter(self, f, name=None):
        return RDD(self.ctx, name or self.name + ".filter", self.n, [(self, "narrow")],
                   lambda i: [x for x in self.partition(i) if f(x)], self.partitioner)

    def flat_map(self, f, name=None):
        return RDD(self.ctx, name or self.name + ".flatMap", self.n, [(self, "narrow")],
                   lambda i: [y for x in self.partition(i) for y in f(x)], None)

    def map_values(self, f, name=None):
        return RDD(self.ctx, name or self.name + ".mapValues", self.n, [(self, "narrow")],
                   lambda i: [(k, f(v)) for k, v in self.partition(i)], self.partitioner)

    # ---- transformations that may be wide

    def map_output(self, sid, j):
        """The map side of a shuffle: partition j of this RDD, stored once for
        the shuffle sid (as MapReduce stores its map outputs). A lost map
        output is computed again from the lineage."""
        key = (sid, j)
        if key not in self.ctx.shuffle:
            self.ctx.shuffle[key] = self.partition(j)
        return self.ctx.shuffle[key]

    def new_shuffle(self):
        self.ctx.next_id += 1
        return self.ctx.next_id - 1

    def partition_by(self, n, name=None):
        sid = self.new_shuffle()

        def fn(i):
            return [(k, v) for j in range(self.n) for k, v in self.map_output(sid, j) if k % n == i]
        return RDD(self.ctx, name or self.name + ".partitionBy", n, [(self, "wide")], fn, n)

    def reduce_by_key(self, f, n, name=None):
        sid = self.new_shuffle()

        def fn(i):
            acc = {}
            for j in range(self.n):
                for k, v in self.map_output(sid, j):
                    if k % n == i:
                        acc[k] = f(acc[k], v) if k in acc else v
            return sorted(acc.items())
        return RDD(self.ctx, name or self.name + ".reduceByKey", n, [(self, "wide")], fn, n)

    def join(self, other, name=None):
        """Inner join on the key. Narrow when both sides have the same hash
        partitioner, else both sides are shuffled into self.n partitions."""
        name = name or self.name + ".join"
        if self.partitioner is not None and self.partitioner == other.partitioner:
            def fn(i):
                right = {}
                for k, w in other.partition(i):
                    right.setdefault(k, []).append(w)
                return [(k, (v, w)) for k, v in self.partition(i) for w in right.get(k, [])]
            return RDD(self.ctx, name, self.n, [(self, "narrow"), (other, "narrow")], fn,
                       self.partitioner)
        n = self.n
        sid_left, sid_right = self.new_shuffle(), other.new_shuffle()

        def fn(i):
            right = {}
            for j in range(other.n):
                for k, w in other.map_output(sid_right, j):
                    if k % n == i:
                        right.setdefault(k, []).append(w)
            return [(k, (v, w)) for j in range(self.n) for k, v in self.map_output(sid_left, j)
                    if k % n == i for w in right.get(k, [])]
        return RDD(self.ctx, name, n, [(self, "wide"), (other, "wide")], fn, n)


def pagerank_rdd(ctx, links, n_vertices, iterations, alpha, parts):
    """The PageRank program of Section 3.2.2 of the RDD paper. alpha is the
    probability of a random jump, as in the paper (so the follow probability
    is 1 - alpha). links is a list of (u, [targets]); every vertex must have
    at least one out-link and at least one in-link. As in the paper's program,
    a vertex with no in-link gets no contribution, so reduceByKey drops it
    from ranks, and its links are lost to the next join.
    Returns (the final ranks RDD, the links RDD)."""
    links_rdd = ctx.parallelize(links, parts).partition_by(parts, name="links").persist()
    one = alpha - alpha + 1
    ranks = links_rdd.map_values(lambda _: one / n_vertices, name="ranks0")
    for t in range(1, iterations + 1):
        contribs = links_rdd.join(ranks, name="join%d" % t).flat_map(
            lambda kv: [(d, kv[1][1] / len(kv[1][0])) for d in kv[1][0]], name="contribs%d" % t)
        ranks = contribs.reduce_by_key(lambda a, b: a + b, parts, name="sums%d" % t).map_values(
            lambda s: alpha / n_vertices + (1 - alpha) * s, name="ranks%d" % t)
    return ranks, links_rdd
