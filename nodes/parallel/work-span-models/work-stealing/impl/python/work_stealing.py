# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/work-stealing/. The authors are listed in prov/D9FWRC.jsonl.

"""Randomized work stealing, simulated step by step on a fork-join DAG.

A fork-join program is a dict that maps a procedure name to its body, a list
of statements:

    ("work", k)     k unit strands in a chain, k >= 1
    ("spawn", g)    start procedure g; the code after it may run in parallel
    ("call", g)     run procedure g and wait for it
    ("sync",)       wait for all children spawned so far by this procedure

Each procedure ends with an implicit sync. build_dag() turns a program into
a DAG of unit-time nodes, in which each node has at most two successors.
A spawn node has two: the first node of the child and the continuation.

work_stealing() runs the scheduler of Blumofe and Leiserson on p simulated
processors in synchronous steps. In each step, a processor with an assigned
node executes it; a processor without one makes one steal attempt at a
victim chosen uniformly at random. Deques are pushed and popped at the
bottom by their owner, and thieves take from the top. The run is exact and
deterministic for a given random.Random object. Cost: O(T_p * p) Python
operations for T_p steps.
"""

import random
from collections import deque
from typing import Callable, Hashable, Mapping, Sequence

Stmt = tuple
Program = Mapping[Hashable, Sequence[Stmt]]


class Dag:
    """A DAG of unit-time nodes 0 .. n-1, with node 0 as the root."""

    def __init__(self) -> None:
        self.succ: list[list[int]] = []
        self.child: dict[int, int] = {}  # spawn node -> first node of the child

    def new_node(self, preds: Sequence[int] = ()) -> int:
        v = len(self.succ)
        self.succ.append([])
        for u in preds:
            self.succ[u].append(v)
        return v

    def __len__(self) -> int:
        return len(self.succ)

    def preds(self) -> list[list[int]]:
        pr: list[list[int]] = [[] for _ in self.succ]
        for u, vs in enumerate(self.succ):
            for v in vs:
                pr[v].append(u)
        return pr

    def span(self) -> int:
        """The number of nodes on a longest path (T_infinity)."""
        longest = [1] * len(self.succ)
        for u in range(len(self.succ)):  # node ids are a topological order
            for v in self.succ[u]:
                longest[v] = max(longest[v], longest[u] + 1)
        return max(longest, default=0)


def build_dag(program: Program, root: Hashable) -> Dag:
    """Unfold the program from procedure `root` into a DAG of unit nodes.

    Each procedure instance gets an entry node and an exit node, each spawn
    gets one node, and each sync with pending children gets one node. Node
    ids increase along every edge, so they are a topological order.
    """
    dag = Dag()

    def instance(name: Hashable, pred: int | None) -> tuple[int, int]:
        entry = dag.new_node([] if pred is None else [pred])
        cur, pending = entry, []
        for st in program[name]:
            op = st[0]
            if op == "work":
                for _ in range(st[1]):
                    cur = dag.new_node([cur])
            elif op == "spawn":
                s = dag.new_node([cur])
                c_entry, c_exit = instance(st[1], s)
                dag.child[s] = c_entry
                pending.append(c_exit)
                cur = s
            elif op == "call":
                _, cur = instance(st[1], cur)
            elif op == "sync":
                if pending:
                    cur = dag.new_node([cur, *pending])
                    pending = []
            else:
                raise ValueError(f"unknown statement {st!r}")
        if pending:
            cur = dag.new_node([cur, *pending])
        return entry, dag.new_node([cur])

    instance(root, None)
    return dag


def work_stealing(dag: Dag, p: int, rng: random.Random,
                  on_step: Callable[[int, list, list], None] | None = None) -> dict:
    """Schedule `dag` on p processors by randomized work stealing.

    Returns a dict with the time T_p (steps), the number of steal attempts,
    the number of successful steals, the step at which each node ran, the
    processor that ran it, and the largest deque length seen. If on_step is
    given, it is called after each step with (step, assigned, deques).
    """
    n = len(dag)
    missing = [len(ps) for ps in dag.preds()]
    assigned: list[int | None] = [None] * p
    deques = [deque() for _ in range(p)]  # left end = top, right end = bottom
    ran_at = [0] * n
    ran_by = [-1] * n
    if n:
        assigned[0] = 0
    done = attempts = steals = max_deque = t = 0
    while done < n:  # @line L1
        t += 1
        thieves = []
        for q in range(p):
            u = assigned[q]
            if u is not None:  # @line L2
                ran_at[u], ran_by[u] = t, q  # @line L3
                done += 1
                enabled = []
                for v in dag.succ[u]:
                    missing[v] -= 1
                    if missing[v] == 0:
                        enabled.append(v)
                if len(enabled) == 2:  # @line L4
                    c = dag.child[u]  # work first: run the child, push the continuation
                    k = enabled[0] if enabled[1] == c else enabled[1]
                    deques[q].append(k)  # @line L5
                    assigned[q] = c
                elif len(enabled) == 1:
                    assigned[q] = enabled[0]  # @line L6
                elif deques[q]:
                    assigned[q] = deques[q].pop()  # @line L7
                else:
                    assigned[q] = None  # @line L8
                max_deque = max(max_deque, len(deques[q]))
            else:
                thieves.append(q)  # @line L9
        for q in thieves:
            attempts += 1
            r = rng.randrange(p - 1) if p > 1 else q  # @line L10
            if p > 1 and r >= q:
                r += 1
            if deques[r]:  # @line L11
                assigned[q] = deques[r].popleft()
                steals += 1
        if on_step is not None:
            on_step(t, assigned, deques)
    return {"time": t, "attempts": attempts, "steals": steals,
            "ran_at": ran_at, "ran_by": ran_by, "max_deque": max_deque}


def fib_program(n: int) -> dict:
    """The fork-join program of P-FIB(n): spawn fib(n-1), call fib(n-2), sync."""
    prog: dict = {}
    for k in range(n + 1):
        prog[("fib", k)] = ([("work", 1)] if k <= 1 else
                            [("spawn", ("fib", k - 1)), ("call", ("fib", k - 2)), ("sync",), ("work", 1)])
    return prog


def sum_program(n: int) -> tuple[dict, Hashable]:
    """Divide-and-conquer sum of n items: spawn the left half, call the right half."""
    prog: dict = {}

    def add(lo: int, hi: int) -> Hashable:
        name = ("sum", lo, hi)
        if name not in prog:
            if hi - lo <= 1:
                prog[name] = [("work", 1)]
            else:
                mid = (lo + hi) // 2
                prog[name] = [("spawn", add(lo, mid)), ("call", add(mid, hi)), ("sync",), ("work", 1)]
        return name

    return prog, add(0, max(n, 1))


def random_program(rng: random.Random, depth: int, width: int = 4) -> tuple[dict, Hashable]:
    """A seeded random fork-join program with nesting depth at most `depth`."""
    prog: dict = {}
    counter = [0]

    def make(d: int) -> Hashable:
        counter[0] += 1
        name = ("r", counter[0])
        body: list = []
        for _ in range(rng.randint(1, width)):
            x = rng.random()
            if d > 0 and x < 0.5:
                body.append(("spawn", make(d - 1)))
            elif d > 0 and x < 0.6:
                body.append(("call", make(d - 1)))
            elif x < 0.7:
                body.append(("sync",))
            else:
                body.append(("work", rng.randint(1, 4)))
        prog[name] = body
        return name

    return prog, make(depth)
