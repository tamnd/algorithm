# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/determinacy-race/. The authors are listed in prov/NHXTYV.jsonl.
"""Determinacy races in fork-join programs: the SP-bags algorithm of Feng and
Leiserson (1997) and a brute-force check over all pairs of accesses.

A program is a procedure body, a list of instructions:

    ("read", loc)          read a shared location
    ("write", loc)         write a shared location
    ("read", loc, locks)   the same, with a frozenset of locks held
    ("write", loc, locks)
    ("spawn", body)        spawn a child procedure
    ("sync",)              wait for all children spawned by this procedure

Each procedure ends with an implicit sync. There are no plain calls, as in
the "pure" Cilk programs of Feng and Leiserson.

A determinacy race is a pair of accesses to one location, at least one a
write, that are logically in parallel: neither comes before the other in
the DAG of the run.
"""

# ------------------------------------------------------- disjoint sets


class DisjointSets:
    """Union by rank and path compression. Each root carries a tag ("S" or "P", owner)."""

    def __init__(self):
        self.parent, self.rank, self.tag = {}, {}, {}

    def make_set(self, x, tag):
        self.parent[x], self.rank[x], self.tag[x] = x, 0, tag

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y, tag):
        """Union the sets of x and y, tag the result, and return its root. y may be None."""
        if y is None:
            r = self.find(x)
            self.tag[r] = tag
            return r
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            if self.rank[rx] < self.rank[ry]:
                rx, ry = ry, rx
            self.parent[ry] = rx
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1
        self.tag[rx] = tag
        return rx


# ------------------------------------------------------------ SP-bags


def sp_bags(body, record_relation=False):
    """Run body serially, depth first, with the SP-bags actions of Feng and Leiserson.

    Return the set of locations on which a determinacy race is reported. With
    record_relation, also return a dict that maps each pair (u, v) of access
    numbers, u executed before v, to True if the procedure of u was in a P-bag
    when v executed (that is, u and v are logically parallel).
    """
    ds = DisjointSets()
    reader, writer = {}, {}
    races = set()
    accesses = []  # (access number, procedure id) in serial order
    relation = {}
    counter = [0, 0]  # next procedure id, next access number

    def in_p_bag(proc):
        return ds.tag[ds.find(proc)][0] == "P"

    def run(proc, instrs):
        # spawn proc: S_F = MakeSet(F), P_F = empty. P_F is kept as one member of the bag, or None.
        ds.make_set(proc, ("S", proc))
        p_bag = None
        for ins in list(instrs) + [("sync",)]:
            op = ins[0]
            if op == "spawn":
                child = counter[0]
                counter[0] += 1
                run(child, ins[1])
                # return from child to proc: P_F = Union(P_F, S_child)
                p_bag = ds.union(child, p_bag, ("P", proc))
            elif op == "sync":
                # sync in proc: S_F = Union(S_F, P_F), P_F = empty
                if p_bag is not None:
                    ds.union(proc, p_bag, ("S", proc))
                    p_bag = None
            elif op in ("read", "write"):
                loc = ins[1]
                a = counter[1]
                counter[1] += 1
                if record_relation:
                    for u, pu in accesses:
                        relation[(u, a)] = in_p_bag(pu)
                accesses.append((a, proc))
                if op == "write":
                    if (loc in reader and in_p_bag(reader[loc])) or (loc in writer and in_p_bag(writer[loc])):
                        races.add(loc)
                    writer[loc] = proc
                else:
                    if loc in writer and in_p_bag(writer[loc]):
                        races.add(loc)
                    if loc not in reader or not in_p_bag(reader[loc]):
                        reader[loc] = proc
            else:
                raise ValueError(f"unknown instruction {ins!r}")

    counter[0] = 1
    run(0, body)
    return (races, relation) if record_relation else races


# --------------------------------------------------------- brute force


def access_dag(body):
    """Build the DAG of a run. Return (succ, accesses): accesses[k] = (node, op, loc, locks) in serial order."""
    succ = []
    accesses = []

    def node(preds):
        v = len(succ)
        succ.append([])
        for u in preds:
            succ[u].append(v)
        return v

    def build(instrs, start):
        cur, outstanding = start, []
        for ins in list(instrs) + [("sync",)]:
            op = ins[0]
            if op == "spawn":
                fork = node([cur])
                outstanding.append(build(ins[1], fork))
                cur = node([fork])
            elif op == "sync":
                cur = node([cur] + outstanding)
                outstanding = []
            else:
                cur = node([cur])
                accesses.append((cur, op, ins[1], ins[2] if len(ins) > 2 else frozenset()))
        return cur

    build(body, node([]))
    return succ, accesses


def reachability(succ):
    """reach[v] is a bit mask of the nodes reachable from v (v included)."""
    n = len(succ)
    reach = [0] * n
    for v in range(n - 1, -1, -1):  # node numbers are a topological order
        r = 1 << v
        for u in succ[v]:
            r |= reach[u]
        reach[v] = r
    return reach


def logically_parallel(body):
    """For the accesses in serial order, return a dict (i, j) -> True if access i and j are parallel."""
    succ, accesses = access_dag(body)
    reach = reachability(succ)
    par = {}
    for i, (u, *_rest) in enumerate(accesses):
        for j in range(i + 1, len(accesses)):
            v = accesses[j][0]
            par[(i, j)] = not (reach[u] >> v & 1) and not (reach[v] >> u & 1)
    return par


def brute_force_races(body):
    """The locations that have a pair of parallel accesses with at least one write."""
    _, accesses = access_dag(body)
    par = logically_parallel(body)
    races = set()
    for (i, j), p in par.items():
        _, op1, l1, _ = accesses[i]
        _, op2, l2, _ = accesses[j]
        if p and l1 == l2 and "write" in (op1, op2):
            races.add(l1)
    return races


def brute_force_data_races(body):
    """The locations with a parallel pair, at least one a write, that hold no lock in common."""
    _, accesses = access_dag(body)
    par = logically_parallel(body)
    races = set()
    for (i, j), p in par.items():
        _, op1, l1, k1 = accesses[i]
        _, op2, l2, k2 = accesses[j]
        if p and l1 == l2 and "write" in (op1, op2) and not (k1 & k2):
            races.add(l1)
    return races


def random_program(rng, depth, locs=3, max_len=5):
    body = []
    for _ in range(rng.randint(0, max_len)):
        r = rng.random()
        if depth > 0 and r < 0.3:
            body.append(("spawn", random_program(rng, depth - 1, locs, max_len)))
        elif r < 0.45:
            body.append(("sync",))
        elif r < 0.75:
            body.append(("read", rng.randrange(locs)))
        else:
            body.append(("write", rng.randrange(locs)))
    return body
