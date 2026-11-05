---
tag: SX075V
kind: algorithm
slug: itai-rodeh-girth-algorithm
name: Itai-Rodeh girth algorithm
area: graphs/paths-and-cycles
level: advanced
summary: Computes the girth of an undirected unweighted graph, and a shortest cycle, by one breadth-first search from every vertex in O(n(n + m)) time.
solves: [shortest-cycle-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n(n + m)), best: Θ(n(n + m))}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1978
  people: [Alon Itai, Michael Rodeh]
  note: Finding a minimum circuit in a graph, SIAM Journal on Computing; the paper also gives an O(n^2) algorithm that is off by at most one.
prereqs: [girth, breadth-first-search, simple-cycle]
see_also: [shortest-cycle-problem, cycle-detection, fundamental-cycle, bipartite-graph, multigraph, self-loop, tree-diameter, spanning-forest]
sources:
  - paper: doi:10.1137/0207033
    title: Alon Itai and Michael Rodeh, Finding a minimum circuit in a graph, SIAM Journal on Computing 7(4), 413 to 423 (1978)
    locator: the breadth-first search algorithm for a minimum circuit, the approximation that errs by at most one, and the algorithms for triangles
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search (shortest-path distances and the breadth-first tree)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.3, Paths and cycles (the definition of girth)
---

The Itai-Rodeh girth algorithm finds a shortest cycle of an undirected unweighted graph, and so its [girth](/girth/). It runs a [breadth-first search](/breadth-first-search/) from every vertex. In a search from $r$, every edge that is not in the search tree closes a walk from $r$ out to one end of the edge and back from the other, whose length is the two distances plus 1. The smallest such value over all roots is the girth, and climbing the search tree from the two ends of the best edge gives the cycle. The time is $O(n(n + m))$, and the graph may have [self-loops](/self-loop/), parallel edges and isolated vertices.

## In plain words

You want the shortest round trip in a road network where every road has the same length.

Pick a town and spread out from it, one ring of neighbours at a time, remembering how far each town is and by which road you first reached it. Sometimes a road joins two towns you have already reached by other roads. Then you have found a round trip: out to one end, across the road, and back from the other end. Its length is the two distances plus one.

Do this from every town and keep the shortest round trip. When you start from a town that lies on a shortest round trip, the search finds that trip exactly, so the best value is the answer.

## The problem

Given an undirected graph $G = (V, E)$ with $V = \{0, \ldots, n - 1\}$ and $m$ numbered edges, where loops and parallel edges are allowed, return a shortest [simple cycle](/simple-cycle/) of $G$, as its vertices and its edges, or report that $G$ is a forest. The length counts edges: a loop is a cycle of length 1, two parallel edges form a cycle of length 2, and in a simple graph every cycle has length at least 3. For directed or weighted graphs, see the [shortest cycle problem](/shortest-cycle-problem/).

## The algorithm

The search from $r$ computes $\mathrm{dist}[v]$, the distance from $r$, and $\mathrm{pe}[v]$, the edge by which $v$ was reached. Edges are compared by their numbers, so that two parallel edges are different. An edge $e$ seen from $u$ that is not $\mathrm{pe}[u]$ and leads to a vertex that was already reached is a *non-tree edge*; it gives the candidate $\mathrm{dist}[u] + \mathrm{dist}[v] + 1$.

```pseudo id=main
GIRTH(G)
L1  best ← ∞; found ← NIL
L2  for each vertex r do
L3      dist[v] ← ∞, pv[v] ← NIL and pe[v] ← NIL for all v; dist[r] ← 0; Q ← queue holding r
L4      while Q is not empty do
L5          u ← DEQUEUE(Q)
L6          for each edge e = {u, v} at u do
L7              if dist[v] = ∞ then dist[v] ← dist[u] + 1; pv[v] ← u; pe[v] ← e; ENQUEUE(Q, v)
L8              else if e ≠ pe[u] and dist[u] + dist[v] + 1 < best then
L9                  best ← dist[u] + dist[v] + 1; found ← (r, e, u, v)
L10 if found = NIL then return "G is a forest"
L11 (r, e, u, v) ← found; repeat the search from r to rebuild pv, pe and dist
L12 climb from u and from v by pv to their lowest common ancestor w, and return the path w … u, the edge e, and the path v … w
```

A loop $e = \{u, u\}$ appears twice in the list of $u$. When $u$ is scanned, $u$ is already reached and $e \ne \mathrm{pe}[u]$, so line L9 gets the candidate $2\,\mathrm{dist}[u] + 1$, which is 1 at the root $u$. Two parallel edges $e, e'$ between $u$ and $v$ give the candidate 2 at the root $u$: one of them becomes $\mathrm{pe}[v]$ and the other one is a non-tree edge. So loops and parallel edges need no special case. Isolated vertices give searches of size 1 and no candidate.

## Example

Take the vertices 0 to 7 and the edges $\{0,1\}, \{1,2\}, \{2,3\}, \{3,4\}, \{4,0\}$, which form a 5-cycle, and $\{4,5\}, \{5,6\}, \{6,3\}$, which with $\{3,4\}$ form a 4-cycle. Vertex 7 is isolated. The girth is 4.

| root $r$ | distances of $0, \ldots, 6$ | non-tree edges and candidates |
|---|---|---|
| 0 | 0, 1, 2, 2, 1, 2, 3 | $\{2,3\}$: $2 + 2 + 1 = 5$; $\{5,6\}$: $2 + 3 + 1 = 6$ |
| 1 | 1, 0, 1, 2, 2, 3, 3 | $\{3,4\}$: 5; $\{5,6\}$: 7 |
| 3 | 2, 2, 1, 0, 1, 2, 1 | $\{5,6\}$: $2 + 1 + 1 = 4$; $\{0,1\}$: 5 |
| 4 | 1, 2, 2, 1, 0, 1, 2 | $\{5,6\}$: 4; $\{1,2\}$: 5 |
| 7 | only vertex 7 | none |

The value 6 from root 0 is not the length of a cycle: the walk $0, 4, 5, 6, 3, 4, 0$ passes through 4 twice. It is still at least the girth, because the walk contains the 4-cycle $4, 5, 6, 3$. Root 3 lies on a shortest cycle and finds the value 4 exactly. The first value 4 is found at root 3 from the edge $\{5, 6\}$. Line L12 climbs from 5 (parent 4, then 3) and from 6 (parent 3), and returns the cycle $3, 4, 5, 6$ with the edge $\{6, 3\}$ closing it.

## Correctness

Every candidate is at least the girth: the tree path from $r$ to $u$, the edge $e$, and the tree path from $v$ back to $r$ form a closed walk that uses $e$ exactly once, and such a walk contains a cycle through $e$ that is no longer than the walk. Conversely, let $C$ be a shortest cycle, of length $g$, and $r$ a vertex of $C$. The search tree from $r$ has no cycle, so some edge $\{u, v\}$ of $C$ is a non-tree edge, and since distances in $G$ are at most distances along $C$, its candidate is at most $g$. Line L12 returns a cycle of length at most the best candidate, so of length exactly $g$. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model with incidence lists.

- **One search, lines L3 to L9.** $\Theta(n)$ to reset the arrays and $O(n + m)$ for the search, since each vertex is dequeued at most once and each of its $\deg(u)$ list entries costs $O(1)$.
- **All searches, line L2.** $n$ searches, $\Theta(n(n + m))$ in total. Without pruning, every search scans the whole component of its root, so this is also the best case.
- **Lines L11 and L12.** One more search, $O(n + m)$, and a climb of $O(n)$ steps.

The extra space is $\Theta(n + m)$: the arrays of one search, the queue and the lists. Only the record $\mathrm{found}$ survives from one search to the next, which is why line L11 repeats the best search instead of storing all trees.

## Properties

- **Exact.** It returns a shortest cycle, not only its length.
- **Deterministic and not recursive.** The searches use a queue.
- **Undirected only.** In a directed graph, a non-tree arc $(u, v)$ does not close a directed walk through $r$, because the tree path from $r$ to $v$ cannot be followed backwards. Directed girth is computed differently (see Variants).
- **Unweighted only.** Breadth-first distances count edges. With weights the same idea needs Dijkstra searches and more care (see the [shortest cycle problem](/shortest-cycle-problem/)).
- **Parallel by roots.** The $n$ searches are independent and can run at the same time.

## Variants and improvements

- **Pruning.** When $u$ is dequeued, every neighbour $v$ has $\mathrm{dist}[v] \ge \mathrm{dist}[u] - 1$, so every later candidate of this search is at least $2\,\mathrm{dist}[u]$. The search can stop at the first $u$ with $2\,\mathrm{dist}[u] \ge \mathrm{best}$. This does not change the worst case.
- **Off by at most one in $O(n^2)$ time.** Itai and Rodeh also stop each search at its first non-tree edge. A search that has seen no non-tree edge has only met tree edges, at most $n - 1$ of them, so each search costs $O(n)$, and the smallest value found is at most $g + 1$.
- **Directed graphs.** The shortest directed cycle through $r$ has length $1 + \min \mathrm{dist}(r, u)$ over arcs $(u, r)$; a breadth-first search from each vertex gives the directed girth in $O(n(n + m))$ time.
- **Triangles.** Girth 3 means a triangle. Itai and Rodeh find one in $O(m^{3/2})$ time, or with fast matrix multiplication in $O(n^\omega)$ time.
- **Fast matrix multiplication.** Itai and Rodeh also compute the girth of an undirected unweighted graph in $O(n^\omega)$ time with Boolean matrix products, which is faster than $O(nm)$ on dense graphs.
- **Weighted graphs.** For nonnegative weights, run Dijkstra's algorithm from each vertex. Roditty and Vassilevska Williams show that a minimum weight cycle is as hard to find as a minimum weight triangle; see the [shortest cycle problem](/shortest-cycle-problem/).

## When to use it

Use it to compute the girth and a shortest cycle of a sparse or medium-sized undirected graph, for example to check that a code graph or a network has no short cycles. If only the presence of some cycle matters, a single search suffices: a graph is a forest exactly when no search finds a non-tree edge, which is [cycle detection](/cycle-detection/) in $O(n + m)$. If the graph is dense and large, use the matrix multiplication version or the $O(n^2)$ approximation.

## Pitfalls

- **Comparing parents by vertex.** If the test at line L8 is $v \ne$ parent of $u$ instead of $e \ne \mathrm{pe}[u]$, two parallel edges between $u$ and its parent are never seen as a cycle of length 2.
- **Taking a candidate as a cycle.** A candidate from a root that is not on a shortest cycle can be a walk that repeats vertices, as the value 6 in the example. Build the cycle from the common ancestor, as line L12 does, not by joining the two root paths.
- **One root only.** The minimum over the non-tree edges of one search is not the girth in general; in the example, root 0 gives 5. All roots, or at least one root on a shortest cycle, must be searched.
- **Forgetting loops.** If loops are dropped when the lists are built, a graph whose only cycles are loops is reported as a forest.
- **Using it on directed graphs.** Treating a directed graph as undirected finds cycles that do not follow the arcs.

## Implementations

## History

Alon Itai and Michael Rodeh published "Finding a minimum circuit in a graph" in the SIAM Journal on Computing in 1978. The paper gives the breadth-first search method for a shortest cycle, the faster version that may return a cycle one edge too long, triangle finding in $O(m^{3/2})$ time, and the link between shortest cycles and Boolean matrix multiplication. Later work studies the same questions for directed and weighted graphs and for approximation.

## References
