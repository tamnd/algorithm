---
tag: WC91FF
kind: algorithm
slug: reverse-delete
name: Reverse-delete algorithm
aliases:
- inverse Kruskal algorithm
area: graphs/spanning-trees
level: core
summary: Scan edges from heaviest to lightest and delete each edge whose removal keeps the graph connected.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m (n + m)), best: Ω(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1956
  people: [Joseph B. Kruskal]
  note: Kruskal described the method in his paper of 1956, next to the method now called Kruskal's algorithm.
prereqs: [minimum-spanning-tree, cycle-property, bridge, graph-traversal]
see_also: [kruskal, prim, boruvka, cut-property, dynamic-connectivity, holm-de-lichtenberg-thorup, mst-optimality-conditions, spanning-forest]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5, The minimum spanning tree problem (the Reverse-Delete algorithm and its proof by the cycle property)
  - paper: doi:10.1090/S0002-9939-1956-0078686-7
    title: "Joseph B. Kruskal, On the shortest spanning subtree of a graph and the traveling salesman problem, Proceedings of the American Mathematical Society 7(1) (1956), 48-50"
    locator: the construction of the paper that deletes the longest edges whose removal keeps the graph connected
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms
    locator: Chapter 6, Minimum spanning trees (the red rule)
  - paper: doi:10.1145/335305.335345
    title: Mikkel Thorup, Near-optimal fully-dynamic graph connectivity, Proceedings of the 32nd ACM Symposium on Theory of Computing (2000), 343-350
    locator: the main theorem, O(log n (log log n)^3) amortized time per update
---

The reverse-delete algorithm finds a [minimum spanning tree](/minimum-spanning-tree/) by removing edges: it scans the edges from the heaviest to the lightest, and deletes each edge whose two ends stay connected without it. Each deleted edge is a heaviest edge of a cycle, so the [cycle property](/cycle-property/) proves it correct. With a graph search for each test, it runs in $O(m (n + m))$ time, which is slow next to [Kruskal's](/kruskal/) and [Prim's](/prim/) algorithms. It matters as the mirror image of Kruskal's algorithm and as the example of the "red rule", the other half of the MST theory.

## In plain words

You start with every road of the map, and you want to close the expensive roads that you do not need. Look at the roads from the most expensive to the cheapest. For each road, ask: if I close it, can I still drive between its two ends on the roads that are left? If yes, close it, because it only made a loop. If no, keep it, because without it some towns would be cut off.

At the end no loop remains, every town that was reachable is still reachable, and the roads left are the cheapest network. The method never closes the last link between two parts of the map, so it works the same way when the map is in several pieces.

## The problem

The input is an undirected graph $G = (V, E)$ with $n = |V|$ vertices and $m = |E|$ edges, and a real weight $w(e)$ on each edge. Weights may be negative and may tie. Parallel edges and [self-loops](/self-loop/) are allowed. The graph does not have to be [connected](/connected-graph/).

The output is a minimum spanning forest: a [spanning forest](/spanning-forest/) of $G$ of least total weight. When $G$ is connected it is a minimum spanning tree with $n - 1$ edges. The algorithm never changes which vertices are connected, so on a disconnected graph it returns a minimum spanning tree of each component. With ties, the order of the sort decides which of the minimum forests is returned.

## The algorithm

```pseudo id=main
REVERSE-DELETE(G, w)
L1  F ← E
L2  sort the edges of E into non-increasing order of w
L3  for each edge e = (u, v) ∈ E, in this order do
L4      if u and v are connected in the graph (V, F \ {e}) then   ▷ e lies on a cycle of F
L5          F ← F \ {e}
L6  return F
```

Line L4 asks if $e$ is a [bridge](/bridge/) of the current graph $(V, F)$. If $e$ is not a bridge, it lies on a cycle of $F$, and line L5 deletes it. A bridge is kept, and it stays a bridge until the end, because $F$ only loses edges. A self-loop always passes the test of line L4, since $u = v$, so it is deleted.

The test of line L4 is a [graph traversal](/graph-traversal/) from $u$ in $(V, F \setminus \{e\})$ that stops when it reaches $v$. It takes $O(n + m)$ time.

## Example

The graph has the vertices $a$ to $f$ and nine edges. Two pairs of weights tie. The sort puts the heavier edge first and, among equal weights, the edge listed later first.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

| step | edge | weight | path between the ends without the edge | action | $w(F)$ after |
|---|---|---|---|---|---|
| 0 | | | | start, $F = E$ | 34 |
| 1 | $de$ | 7 | $d, b, c, e$ | delete | 27 |
| 2 | $df$ | 6 | $d, b, c, e, f$ | delete | 21 |
| 3 | $ce$ | 5 | none: $de$ and $df$ are gone | keep | 21 |
| 4 | $cd$ | 4 | $c, b, d$ | delete | 17 |
| 5 | $ab$ | 4 | $a, c, b$ | delete | 13 |
| 6 | $ac$ | 3 | none: it is the last edge at $a$ | keep | 13 |
| 7 | $ef$ | 2 | none: it is the last edge at $f$ | keep | 13 |
| 8 | $bd$ | 2 | none: it is the last edge at $d$ | keep | 13 |
| 9 | $bc$ | 1 | none: without it, $\{b, d\}$ is cut off | keep | 13 |

The result is $\{ce, ac, ef, bd, bc\}$ with weight 13, the same tree that [Kruskal's algorithm](/kruskal/) and [Prim's algorithm](/prim/) find on this graph. After step 5, $F$ already has $n - 1 = 5$ edges, so the last four tests can only keep edges. A program that counts can stop there.

## Correctness

**Theorem.** For each finite undirected graph with real edge weights, REVERSE-DELETE returns a minimum spanning forest. Ties, negative weights, parallel edges, self-loops and disconnected graphs are allowed.

Two invariants hold before each test of line L4. (a) $(V, F)$ has the same connected components as $G$, because line L5 deletes only an edge whose ends stay connected. (b) $F$ contains some minimum spanning forest $F^*$. When line L5 deletes $e$, take a cycle $C$ in $F$ through $e$. Each edge of $C$ that was scanned before $e$ was kept, so it was a bridge then, and it is still a bridge; but a bridge lies on no cycle. So the other edges of $C$ come later in the order, and $w(f) \le w(e)$ for each $f \in C$. If $e \in F^*$, removing it splits a tree of $F^*$, and the path $C \setminus \{e\}$ has an edge $g \notin F^*$ that joins the two parts; then $F^* - e + g$ is a minimum spanning forest inside $F \setminus \{e\}$. At the end, every edge of $F$ was kept as a bridge, so $F$ is a forest with the components of $G$, and $F \supseteq F^*$ forces $F = F^*$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM, with a comparison of two weights in $O(1)$ time.

- **Line L2** sorts $m$ edges in $O(m \log m)$ time.
- **Line L4** runs $m$ times. Each run is a depth-first or breadth-first search in $(V, F \setminus \{e\})$, which has at most $n$ vertices and $m$ edges, so it takes $O(n + m)$ time.
- **Lines L1, L5 and L6** take $O(m)$ time in total.

So the time is $O(m \log m + m(n + m)) = O(m(n + m))$ in the worst case, since $\log m \le m$. Each edge is read on every input, so the time is $\Omega(n + m)$ in the best case. The extra space is $O(n + m)$ for the adjacency lists, the marks of the search and the sorted order.

| claim | bound | case |
|---|---|---|
| time | $O(m(n + m))$ | worst |
| time | $\Omega(n + m)$ | best |
| extra space | $O(n + m)$ | worst |

**With a dynamic connectivity structure.** Line L4 is a connectivity query after a deletion. A fully [dynamic connectivity](/dynamic-connectivity/) structure answers it fast. With the structure of [Holm, de Lichtenberg and Thorup](/holm-de-lichtenberg-thorup/), each deletion costs $O(\log^2 n)$ amortized time and each query $O(\log n / \log \log n)$, so the algorithm runs in $O(m \log^2 n)$ time. With Thorup's improvement to $O(\log n (\log \log n)^3)$ amortized time per update, it runs in $O(m \log n (\log \log n)^3)$ time. Both are still slower than Kruskal's algorithm.

## Properties

- **Deterministic.** The order of the sort fixes the output. With the order "non-increasing weight, then decreasing index", the output is the same as the output of Kruskal's algorithm with the order "non-decreasing weight, then increasing index": both are the unique minimum forest for that total order of the edges.
- **Removes, never adds.** $F$ starts with all edges and only shrinks. At each moment $(V, F)$ has the components of $G$, so the algorithm can stop at any time with a connected spanning subgraph that is lighter than before.
- **Only the order of the weights matters.** The algorithm compares weights and never adds them.
- **The red rule.** Each deletion removes a heaviest edge of a cycle. Kruskal's algorithm applies the blue rule (take a lightest edge of a cut) in the opposite order.

## Variants and improvements

- **Dynamic connectivity.** Replace the search of line L4 by a dynamic connectivity structure, as above.
- **Stop when the count is reached.** Stop when $|F| = n - c$, where $c$ is the number of components of $G$, which one search finds in $O(n + m)$ time. This saves the tests of the lightest edges, but not the worst case.
- **Maximum spanning tree.** Scan from the lightest edge to the heaviest. This gives a [maximum spanning tree](/maximum-spanning-tree/).
- **General red rule.** Any order of deletions of a heaviest edge on a cycle of $F$ ends with a minimum spanning forest. Reverse-delete is the order that makes the check simple: in its order, any non-bridge edge is a heaviest edge on its cycles.

## When to use it

Use reverse-delete when the graph changes by deletions, or when you want to keep a connected subgraph at every moment and stop early with a partial answer. For a one-time MST computation, [Kruskal's algorithm](/kruskal/) does the same job in $O(m \log m)$ time with a [disjoint-set](/disjoint-set/) structure instead of a search, and [Prim's algorithm](/prim/) is better for dense graphs. Reverse-delete is mainly a teaching tool for the cycle property.

## Pitfalls

- **The wrong order.** Sorting into non-decreasing order in line L2 deletes light edges first and returns a heavy tree. The test with the triangle of weights 1, 5 and 5 catches it: the edge of weight 1 must stay.
- **Deleting bridges.** Deleting each edge in order, or each edge that is heavier than some other edge, without the test of line L4, can disconnect the graph. The test with a triangle and a pendant edge of weight 100 catches it: that edge is a bridge and must stay.
- **Testing in the original graph.** The test of line L4 must use the current set $F$, not $E$. In $E$, almost every edge lies on some cycle, and deleting all of them disconnects the graph. The example catches it: in step 3, $ce$ lies on a cycle of $E$ but not of $F$.
- **Expecting $n - 1$ edges.** On a disconnected graph the output has $n - c$ edges. The disconnected test checks this.

## Implementations

## History

Joseph Kruskal's paper of 1956 gives the method now called Kruskal's algorithm, and also a construction that works from the other end: it deletes, as long as possible, the longest edge whose removal leaves the graph connected. This is the reverse-delete algorithm. Kleinberg and Tardos (Section 4.5) give it the name Reverse-Delete and prove it by the cycle property. Tarjan's book (Chapter 6) places it in the framework of the red rule.

## References
