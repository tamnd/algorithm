# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/causal-graph-heuristic/. The authors are listed in prov/WC1PNH.jsonl.

"""The causal graph heuristic of Helmert (2004, 2006) for SAS+ tasks.

A task has variables with domains {0, ..., k-1}, given as a dict from variable
to k. An Operator(name, pre, eff) has dicts pre and eff from variables to
values; pre holds every precondition, including the prevail conditions. The
module builds the domain transition graphs (Helmert 2006, Definition 5) and the
causal graph (Definition 6), prunes the causal graph to an acyclic graph with
the greedy order of Section 5.2.2, and computes the heuristic with the
Dijkstra-like procedure of Figure 18. There are no axioms or conditional
effects. The value is 0 exactly at goal states. It is not admissible, and it
can be infinite in a state from which the goal is reachable.
"""

import heapq
import math
from collections import namedtuple
from typing import Dict, Hashable, List, Tuple

Operator = namedtuple("Operator", "name pre eff")
Task = namedtuple("Task", "domains operators init goal")


def domain_transition_graph(task: Task, v: Hashable) -> List[Tuple[int, int, frozenset, Hashable]]:
    """The arcs (d, d2, condition, operator name) of DTG(v), as in Definition 5 without axioms."""
    arcs = []
    for o in task.operators:
        if v not in o.eff:
            continue
        d2 = o.eff[v]
        if v in o.pre:
            arcs.append((o.pre[v], d2, frozenset((u, e) for u, e in o.pre.items() if u != v), o.name))
        else:
            label = frozenset(o.pre.items())
            arcs.extend((d, d2, label, o.name) for d in range(task.domains[v]) if d != d2)
    return arcs


def causal_graph(task: Task) -> Dict[Tuple[Hashable, Hashable], int]:
    """The arcs of CG (Definition 6), each with the number of operators that induce it."""
    weight = {}
    for o in task.operators:
        arcs = set()
        for v in o.eff:
            arcs.update((u, v) for u in o.pre if u != v)
            arcs.update((u, v) for u in o.eff if u != v)
        for arc in arcs:
            weight[arc] = weight.get(arc, 0) + 1
    return weight


def _components(nodes, succ):
    """Strongly connected components in topological order (Tarjan's algorithm, reversed)."""
    index, low, stack, on, comps = {}, {}, [], set(), []

    def visit(v):
        index[v] = low[v] = len(index)
        stack.append(v)
        on.add(v)
        for w in succ[v]:
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)

    for v in nodes:
        if v not in index:
            visit(v)
    return comps[::-1]


def pruned_order(task: Task) -> Dict[Hashable, int]:
    """A level for each variable; the pruned causal graph keeps the arcs (u, v) with level[u] < level[v]."""
    weight = causal_graph(task)
    nodes = sorted(task.domains, key=repr)
    succ = {v: sorted({w for (u, w) in weight if u == v}, key=repr) for v in nodes}
    order = []
    for comp in _components(nodes, succ):
        rest = set(comp)
        while rest:
            v = min(rest, key=lambda x: (sum(weight.get((u, x), 0) for u in rest if u != x), repr(x)))
            order.append(v)
            rest.remove(v)
    return {v: i for i, v in enumerate(order)}


def pruned_transitions(task: Task, level: Dict[Hashable, int]):
    """DTG(v) for every v, with the conditions on higher variables removed and duplicate arcs merged."""
    out = {}
    for v in task.domains:
        seen, arcs = set(), []
        for d, d2, label, name in domain_transition_graph(task, v):
            cond = frozenset((u, e) for u, e in label if level[u] < level[v])
            if d != d2 and (d, d2, cond) not in seen:
                seen.add((d, d2, cond))
                arcs.append((d, d2, cond, name))
        out[v] = arcs
    return out


class CausalGraphHeuristic:
    """h_CG for one task; call it on a state, a dict from variables to values."""

    def __init__(self, task: Task):
        self.task = task
        self.level = pruned_order(task)  # @line L1
        dtgs = pruned_transitions(task, self.level)  # @line L2
        self.preds = {v: sorted({u for (_, _, c, _) in dtgs[v] for u, _ in c}, key=repr) for v in task.domains}
        self.out = {v: {} for v in task.domains}
        for v, arcs in dtgs.items():
            for d, d2, cond, _ in arcs:
                self.out[v].setdefault(d, []).append((d2, cond))

    def costs(self, state, v, d, cache):
        """cost_v(d, d2) for every value d2 (Figure 18), with the other variables as in the state."""
        if (v, d) in cache:
            return cache[(v, d)]
        cost = {d: 0}
        local = {d: {u: state[u] for u in self.preds[v]}}
        heap, done, tie = [(0, 0, d)], set(), 0
        while heap:
            c, _, x = heapq.heappop(heap)
            if x in done:
                continue
            done.add(x)
            for y, cond in self.out[v].get(x, []):
                if y in done:
                    continue
                step = 1
                for u, e in cond:
                    step += self.costs(state, u, local[x][u], cache).get(e, math.inf)  # @line L3
                if c + step < cost.get(y, math.inf):
                    cost[y] = c + step
                    local[y] = dict(local[x])
                    local[y].update(cond)
                    tie += 1
                    heapq.heappush(heap, (c + step, tie, y))
        cache[(v, d)] = cost
        return cost

    def __call__(self, state) -> float:
        cache, total = {}, 0
        for v, g in self.task.goal.items():
            c = self.costs(state, v, state[v], cache).get(g, math.inf)
            if c == math.inf:  # @line L4
                return math.inf
            total += c
        return total  # @line L5
