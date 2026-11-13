# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/task-network/. The authors are listed in prov/DKGG4M.jsonl.

"""Task networks: nodes labeled with task names, plus ordering constraints.

A network is consistent if its ordering constraints have no cycle; its
linearizations are the orders of the nodes that respect every constraint.
Decomposition replaces one node by the nodes of a smaller network, and the new
nodes inherit every ordering constraint of the node they replace.
"""

from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple


class TaskNetwork:
    def __init__(self, nodes: Dict[int, str], order: Iterable[Tuple[int, int]] = ()) -> None:
        self.nodes = dict(nodes)
        self.order: Set[Tuple[int, int]] = set(order)
        for u, v in self.order:
            if u not in self.nodes or v not in self.nodes:
                raise ValueError(f"ordering ({u}, {v}) names a node that is not in the network")

    @staticmethod
    def of(tasks: Sequence[str], order: Optional[Iterable[Tuple[int, int]]] = None) -> "TaskNetwork":
        """Nodes 0..k-1; without an explicit order the tasks are totally ordered."""
        if order is None:
            order = [(i, i + 1) for i in range(len(tasks) - 1)]
        return TaskNetwork(dict(enumerate(tasks)), order)

    def predecessors(self, n: int) -> Set[int]:
        return {u for u, v in self.order if v == n}

    def successors(self, n: int) -> Set[int]:
        return {v for u, v in self.order if u == n}

    def is_consistent(self) -> bool:
        """Kahn's algorithm: the constraints have a linearization iff they have no cycle."""
        indegree = {n: 0 for n in self.nodes}
        for _, v in self.order:
            indegree[v] += 1
        ready = [n for n, d in indegree.items() if d == 0]
        seen = 0
        while ready:
            n = ready.pop()
            seen += 1
            for v in self.successors(n):
                indegree[v] -= 1
                if indegree[v] == 0:
                    ready.append(v)
        return seen == len(self.nodes)

    def linearizations(self) -> Iterator[Tuple[int, ...]]:
        done: List[int] = []
        placed: Set[int] = set()

        def extend() -> Iterator[Tuple[int, ...]]:
            if len(done) == len(self.nodes):
                yield tuple(done)
                return
            for n in sorted(self.nodes):
                if n not in placed and self.predecessors(n) <= placed:
                    placed.add(n)
                    done.append(n)
                    yield from extend()
                    done.pop()
                    placed.remove(n)

        yield from extend()

    def task_sequences(self) -> Set[Tuple[str, ...]]:
        return {tuple(self.nodes[n] for n in lin) for lin in self.linearizations()}

    def decompose(self, n: int, sub: "TaskNetwork") -> Tuple["TaskNetwork", Dict[int, int]]:
        """Replace node n by a copy of sub. Every predecessor of n comes before every
        new node and every successor of n comes after every new node. If sub is empty,
        the predecessors of n stay before its successors. Returns the new network and
        the map from the nodes of sub to their new names."""
        start = max(self.nodes) + 1
        rename = {m: start + i for i, m in enumerate(sorted(sub.nodes))}
        before, after = self.predecessors(n), self.successors(n)
        nodes = {k: t for k, t in self.nodes.items() if k != n}
        nodes.update({rename[m]: t for m, t in sub.nodes.items()})
        order = {(u, v) for u, v in self.order if n not in (u, v)}
        order |= {(rename[u], rename[v]) for u, v in sub.order}
        order |= {(u, x) for u in before for x in rename.values()}
        order |= {(x, v) for x in rename.values() for v in after}
        if not sub.nodes:
            order |= {(u, v) for u in before for v in after}
        return TaskNetwork(nodes, order), rename

    def is_primitive(self, primitive: Iterable[str]) -> bool:
        primitive = set(primitive)
        return all(t in primitive for t in self.nodes.values())
