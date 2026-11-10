# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fork-join-model/. The authors are listed in prov/CRAW0D.jsonl.
"""The fork-join model: programs with spawn and sync, their DAG, and their work and span.

A program is a procedure body, which is a list of instructions:

    ("work", k)     k unit-time strands in series (k >= 0)
    ("spawn", body) start the child procedure body; the parent goes on
    ("call", body)  run the child procedure body and wait for it
    ("sync",)       wait for all children that this procedure spawned

Each procedure ends with an implicit sync, as in Cilk.

Three things are computed:

    sp_term(body)   the series-parallel term of the program
    work_span(t)    W and S of a term by the composition rules
    build_dag(body) the DAG of the run, with a weight on each node
"""

# -------------------------------------------------------------- terms


def sp_term(body):
    """Return the series-parallel term of a procedure body.

    A term is ("strand", k), ("seq", a, b) or ("par", a, b).
    A spawn puts the child in parallel with the code that follows it,
    up to the next sync of the same procedure.
    """
    blocks, cur = [], []
    for ins in body:
        if ins[0] == "sync":
            blocks.append(cur)
            cur = []
        else:
            cur.append(ins)
    blocks.append(cur)  # the implicit sync at the end
    term = ("strand", 0)
    for block in reversed(blocks):
        term = ("seq", _block_term(block), term)
    return term


def _block_term(block):
    term = ("strand", 0)
    for ins in reversed(block):
        op = ins[0]
        if op == "work":
            term = ("seq", ("strand", ins[1]), term)
        elif op == "call":
            term = ("seq", sp_term(ins[1]), term)
        elif op == "spawn":
            term = ("par", sp_term(ins[1]), term)
        else:
            raise ValueError(f"unknown instruction {ins!r}")
    return term


def work_span(term):
    """W and S of a term: series adds both; parallel adds W and takes the max of S."""
    kind = term[0]
    if kind == "strand":
        return term[1], term[1]
    w1, s1 = work_span(term[1])
    w2, s2 = work_span(term[2])
    if kind == "seq":
        return w1 + w2, s1 + s2
    return w1 + w2, max(s1, s2)


# ---------------------------------------------------------------- DAG


class Dag:
    """A DAG with a weight on each node: 1 for a strand, 0 for a spawn or sync point."""

    def __init__(self):
        self.weight = []
        self.succ = []

    def node(self, w, preds):
        v = len(self.weight)
        self.weight.append(w)
        self.succ.append([])
        for u in preds:
            self.succ[u].append(v)
        return v


def build_dag(body):
    """Build the DAG of one run of body, in the style of CLRS Section 27.1.

    Return (dag, source, sink). Each unit strand is a node of weight 1.
    A spawn edge goes from the current node to the first node of the child.
    A sync node of weight 0 has edges from the current node and from the
    last node of each child spawned since the last sync.
    """
    dag = Dag()
    source = dag.node(0, [])
    sink = _build(dag, body, source)
    return dag, source, sink


def _build(dag, body, start):
    cur = start
    outstanding = []
    for ins in list(body) + [("sync",)]:
        op = ins[0]
        if op == "work":
            for _ in range(ins[1]):
                cur = dag.node(1, [cur])
        elif op == "spawn":
            fork = dag.node(0, [cur])
            outstanding.append(_build(dag, ins[1], fork))
            cur = dag.node(0, [fork])  # the continuation
        elif op == "call":
            cur = _build(dag, ins[1], cur)
        elif op == "sync":
            cur = dag.node(0, [cur] + outstanding)
            outstanding = []
        else:
            raise ValueError(f"unknown instruction {ins!r}")
    return cur


def topological_order(dag):
    indeg = [0] * len(dag.weight)
    for v in range(len(dag.weight)):
        for u in dag.succ[v]:
            indeg[u] += 1
    order = [v for v in range(len(dag.weight)) if indeg[v] == 0]
    i = 0
    while i < len(order):
        for u in dag.succ[order[i]]:
            indeg[u] -= 1
            if indeg[u] == 0:
                order.append(u)
        i += 1
    if len(order) != len(dag.weight):
        raise ValueError("the graph has a cycle")
    return order


def dag_work_span(dag):
    """W = the total weight, S = the largest weight of a path."""
    longest = [0] * len(dag.weight)
    for v in topological_order(dag):
        longest[v] += dag.weight[v]
        for u in dag.succ[v]:
            longest[u] = max(longest[u], longest[v])
    return sum(dag.weight), max(longest)


def greedy_time(dag, p):
    """Run a greedy schedule of the unit strands on p processors and return T_p.

    Nodes of weight 0 take no time: they finish as soon as they are ready.
    In each step, up to p ready unit strands run; the lowest numbers go first.
    """
    n = len(dag.weight)
    indeg = [0] * n
    for v in range(n):
        for u in dag.succ[v]:
            indeg[u] += 1
    ready = [v for v in range(n) if indeg[v] == 0]
    done = 0
    steps = 0

    def finish(v, newly):
        for u in dag.succ[v]:
            indeg[u] -= 1
            if indeg[u] == 0:
                newly.append(u)

    while done < n:
        # finish all ready nodes of weight 0 first
        while any(dag.weight[v] == 0 for v in ready):
            zero = [v for v in ready if dag.weight[v] == 0]
            ready = [v for v in ready if dag.weight[v] != 0]
            for v in zero:
                done += 1
                finish(v, ready)
        if done == n:
            break
        ready.sort()
        run, ready = ready[:p], ready[p:]
        steps += 1
        newly = []
        for v in run:
            done += 1
            finish(v, newly)
        ready += newly
    return steps


# ----------------------------------------------------------- examples


def parallel_for(lo, hi, body_work, split_work=1):
    """A parallel loop over [lo, hi) compiled to a tree of spawns.

    Each leaf does body_work strands, and each split does split_work strands.
    """
    if hi - lo == 1:
        return [("work", body_work)]
    mid = (lo + hi) // 2
    return [("work", split_work),
            ("spawn", parallel_for(lo, mid, body_work, split_work)),
            ("call", parallel_for(mid, hi, body_work, split_work)),
            ("sync",)]


def p_fib(n):
    """P-FIB as a fork-join program: one strand per call, plus the spawned recursion."""
    if n < 2:
        return [("work", 1)]
    return [("work", 1), ("spawn", p_fib(n - 1)), ("call", p_fib(n - 2)), ("sync",), ("work", 1)]


def random_program(rng, depth, max_len=4):
    """A random fork-join program for tests."""
    body = []
    for _ in range(rng.randint(0, max_len)):
        r = rng.random()
        if depth > 0 and r < 0.3:
            body.append(("spawn", random_program(rng, depth - 1, max_len)))
        elif depth > 0 and r < 0.45:
            body.append(("call", random_program(rng, depth - 1, max_len)))
        elif r < 0.6:
            body.append(("sync",))
        else:
            body.append(("work", rng.randint(0, 3)))
    return body
