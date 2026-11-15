# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/most-popular-completion/. The authors are listed in prov/PB06E3.jsonl.
"""Most popular completion with a scored trie.

The log maps each past query to its count. For a prefix p, the answer is
the k logged queries that start with p, in the order count descending,
then query string ascending (Python string order). This is the tie rule
of the page.

Each trie node stores the largest count in its subtree (best) and its
preorder number (pre) in a traversal that visits the children in
character order, so pre orders the nodes as their strings sort. The
children of each node are also kept in the order (-best, pre), as in the
Completion Trie of Hsu and Ottaviano (2013). The search is best-first on
a heap with the key (-best, pre, kind): popping a node pushes its first
child and its next sibling, and the query that ends at it.
"""

import heapq

_QUERY = 0  # a finished query sorts before the node with the same string
_NODE = 1


class _Node:
    __slots__ = ("children", "order", "count", "query", "best", "pre", "next")

    def __init__(self):
        self.children = {}  # character -> child node
        self.order = []  # children sorted by (-best, pre)
        self.count = 0  # count of the query that ends here, 0 if none
        self.query = None  # the query that ends here
        self.best = 0  # largest count in the subtree
        self.pre = 0  # preorder number in character order
        self.next = None  # next sibling in the order (-best, pre)


class CompletionTrie:
    """A trie over a query log, with the top-k search of the page."""

    def __init__(self, log: dict[str, int]):
        self.root = _Node()
        self.pops = 0  # node pops of the last call of top_k
        for query, count in log.items():
            if not isinstance(query, str) or query == "":
                raise ValueError("queries must be non-empty strings")
            if count <= 0:
                raise ValueError("counts must be positive")
            node = self.root
            node.best = max(node.best, count)
            for ch in query:
                node = node.children.setdefault(ch, _Node())
                node.best = max(node.best, count)
            node.count = count
            node.query = query
        self._number()

    def _number(self) -> None:
        """Give preorder numbers in character order, then link the siblings."""
        counter = 0
        stack = [self.root]
        nodes = []
        while stack:
            node = stack.pop()
            node.pre = counter
            counter += 1
            nodes.append(node)
            for ch in sorted(node.children, reverse=True):
                stack.append(node.children[ch])
        for node in nodes:
            node.order = sorted(node.children.values(), key=lambda c: (-c.best, c.pre))
            for a, b in zip(node.order, node.order[1:]):
                a.next = b

    def top_k(self, prefix: str, k: int) -> list[tuple[str, int]]:
        """The k most frequent logged queries that start with prefix."""
        self.pops = 0
        node = self.root  # @line L1
        for ch in prefix:  # @line L2
            child = node.children.get(ch)
            if child is None:  # @line L3
                return []
            node = child  # @line L4
        start = node
        heap = [(-start.best, start.pre, _NODE, start)]  # @line L5
        out: list[tuple[str, int]] = []  # @line L6
        while heap and len(out) < k:  # @line L7
            _, _, kind, x = heapq.heappop(heap)  # @line L8
            if kind == _QUERY:  # @line L9
                out.append((x.query, x.count))
                continue
            self.pops += 1  # @line L10
            if x.count > 0:  # @line L11
                heapq.heappush(heap, (-x.count, x.pre, _QUERY, x))
            if x.order:  # @line L12
                first = x.order[0]
                heapq.heappush(heap, (-first.best, first.pre, _NODE, first))
            if x is not start and x.next is not None:  # @line L13
                y = x.next
                heapq.heappush(heap, (-y.best, y.pre, _NODE, y))
        return out  # @line L14


def scan_top_k(log: dict[str, int], prefix: str, k: int) -> list[tuple[str, int]]:
    """The baseline without an index: filter the whole log and sort it."""
    hits = [(q, c) for q, c in log.items() if q.startswith(prefix)]
    hits.sort(key=lambda qc: (-qc[1], qc[0]))
    return hits[: max(k, 0)]
