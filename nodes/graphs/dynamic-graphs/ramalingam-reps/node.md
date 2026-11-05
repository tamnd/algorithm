---
tag: Q56GAS
kind: algorithm
slug: ramalingam-reps
name: Ramalingam-Reps algorithm
aliases:
- Ramalingam-Reps dynamic SSSP
area: graphs/dynamic-graphs
level: research
summary: Incrementally repairs shortest-path distances after edge changes, affecting only the changed region.
solves: [dynamic-single-source-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, A: the number of vertices whose distance changes plus the number of edges at those vertices}
  time: {worst: O(A log A)}
  space: {extra: O(m + n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [dijkstra, shortest-path-tree, dynamic-single-source-shortest-paths]
see_also: [even-shiloach-tree, decremental-sssp, dynamic-all-pairs-shortest-paths, fully-dynamic-graph, worst-case-update-time, update-query-tradeoff, incremental-graph, decremental-graph]
sources:
  - paper: "G. Ramalingam and Thomas Reps, An incremental algorithm for a generalization of the shortest-path problem, Journal of Algorithms 21(2), 267 to 305 (1996)"
    locator: the algorithms for edge insertion and edge deletion (the affected vertices, the counts of tight in-edges, the restricted Dijkstra search), and the O(‖δ‖ log ‖δ‖) bound
  - paper: "G. Ramalingam and Thomas Reps, On the computational complexity of dynamic graph problems, Theoretical Computer Science 158(1-2), 233 to 277 (1996)"
    locator: the model of bounded incremental computation, where cost is measured in the size of the change ‖δ‖
  - paper: "Daniele Frigioni, Alberto Marchetti-Spaccamela and Umberto Nanni, Fully dynamic algorithms for maintaining shortest paths trees, Journal of Algorithms 34(2), 251 to 281 (2000)"
    locator: Section 1 (comparison with Ramalingam and Reps, and output-bounded algorithms for weight changes)
---

The Ramalingam-Reps algorithm keeps the distances from one source in a directed graph with positive edge weights while edges are inserted, deleted, or change weight. After an insertion or a decrease, it runs [Dijkstra's algorithm](/dijkstra/) from the head of the changed edge, only over the vertices whose distance drops. After a deletion or an increase, it first finds the **affected** vertices, those that lose every shortest path, with a count of tight in-edges per vertex, and then runs Dijkstra's algorithm over the affected vertices only, seeded from their unaffected in-neighbors. Each update takes $O(A \log A)$ time, where $A$ is the number of vertices whose distance changes plus the edges at them. It is fully dynamic, deterministic, and has no amortization, but $A$ can be as large as the whole graph. Ramalingam and Reps published it in 1996 as the main example of bounded incremental computation.

## In plain words

Keep the cheapest travel cost from home to every place on a road map with one-way roads. Roads open, close, and change their cost.

When a road gets cheaper, some places get closer. Start at the end of that road and spread the good news, as in the usual shortest path search, but stop wherever the news does not help.

When a road closes or gets dearer, find the places that relied on it. Each place counts how many of its incoming roads give it its current cost. A place whose count drops to zero has lost its cost, and it passes the bad news on. Then compute new costs for just those places, starting from their neighbors that did not change.

The work depends on how many places change, not on the size of the map.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices, $m$ edges and positive weights $w$, a source $s$, and a sequence of updates, each of which inserts an edge, deletes an edge, or changes the weight of an edge. After each update, the algorithm must answer distance queries $d(v) = \mathrm{dist}(s, v)$, with $d(v) = \infty$ when $v$ is not reachable. This is fully dynamic [single-source shortest paths](/dynamic-single-source-shortest-paths/). An insertion is a decrease from $\infty$ and a deletion is an increase to $\infty$, so two kinds of update are enough.

An edge $(u, v)$ is **tight** if $d(u) + w(u, v) = d(v) < \infty$. The tight edges form the shortest path subgraph, a DAG when the weights are positive, and any choice of one tight in-edge per vertex gives a [shortest path tree](/shortest-path-tree/).

## The algorithm

The structure stores $d(v)$ and, for $v \ne s$ with $d(v) < \infty$, the number $c(v)$ of tight in-edges of $v$.

```pseudo id=main
INIT
L1  d ← Dijkstra from s; c(v) ← the number of tight in-edges of v

DECREASE(u, v, w)                  ▷ also an insertion
L2  set w(u, v) ← w; if d(u) + w ≥ d(v) then update c(v) if the edge became tight; return
L3  d(v) ← d(u) + w; Q ← a priority queue holding v
L4  while Q is not empty: take x with the least d(x)
        for each edge (x, z): if d(x) + w(x, z) < d(z) then d(z) ← d(x) + w(x, z); put z into Q
L5  recount c at the changed vertices and fix c at their unchanged out-neighbors

INCREASE(u, v, w)                  ▷ also a deletion, with w = ∞
L6  if (u, v) was tight: set w(u, v); c(v) ← c(v) − 1; if c(v) > 0 then return
L7  phase 1: A ← {v}; for each x taken from A and each tight edge (x, z):
        c(z) ← c(z) − 1; if c(z) = 0 then add z to A
L8  phase 2: for x in A: d(x) ← min over edges (y, x) with y ∉ A of d(y) + w(y, x); put x into Q
L9  Dijkstra over A: take x with the least d(x); relax the edges (x, z) with z in A
L10 recount c at the vertices of A and fix c at their out-neighbors outside A

QUERY(v)
L11 return d(v)
```

Line L2 handles a decrease that changes no distance. Lines L3 and L4 are Dijkstra's algorithm started at $v$, which only goes on at vertices whose distance drops. Line L6 handles an increase of a non-tight edge, which changes nothing, or of a tight edge when $v$ keeps another one. Line L7 finds the affected vertices: a vertex is affected when all its tight in-edges come from affected vertices. Line L8 gives each affected vertex its best distance through an unaffected in-neighbor, whose distance is already final, and line L9 finishes with Dijkstra's algorithm inside the affected set. Lines L5 and L10 keep the counts right; only edges at changed vertices can change their tightness.

## Example

Take five vertices, source 0, and the edges $0 \to 1$ (2), $0 \to 2$ (5), $1 \to 2$ (1), $1 \to 3$ (6), $2 \to 3$ (2), $3 \to 4$ (1).

| update | $d(0)$ | $d(1)$ | $d(2)$ | $d(3)$ | $d(4)$ | vertices changed |
|---|---|---|---|---|---|---|
| none | 0 | 2 | 3 | 5 | 6 | |
| delete $1 \to 2$ | 0 | 2 | 5 | 7 | 8 | 2, 3, 4 |
| insert $4 \to 1$ (1) | 0 | 2 | 5 | 7 | 8 | none |
| insert $0 \to 3$ (3) | 0 | 2 | 5 | 3 | 4 | 3, 4 |
| delete $0 \to 1$ | 0 | 5 | 5 | 3 | 4 | 1 |

Deleting $1 \to 2$ removes the only tight in-edge of 2, since $0 + 5 \ne 3$. Phase 1 then removes the tight edge $2 \to 3$ from the count of 3, which drops to zero because $1 \to 3$ gives $8 \ne 5$, and in the same way 4 is affected. Phase 2 sets $d(2) = 5$ through 0, $d(3) = 8$ through 1, and $d(4) = \infty$, and Dijkstra's algorithm inside $\{2, 3, 4\}$ lowers $d(3)$ to 7 and $d(4)$ to 8. Inserting $4 \to 1$ gives $8 + 1 > 2$ and changes nothing. Inserting $0 \to 3$ with weight 3 lowers $d(3)$, and the search from 3 lowers $d(4)$ and stops. Deleting $0 \to 1$ affects only 1, which gets $d(1) = 4 + 1 = 5$ through the edge inserted before.

## Correctness

For a decrease of the edge $(u, v)$, every new shortest path that is shorter than before uses the new edge, so its vertices after $v$ are exactly those reached by the search of line L4, which is Dijkstra's algorithm with the other distances as fixed upper bounds. For an increase, a vertex keeps its distance exactly when it has a tight in-edge from a vertex that keeps its distance; with positive weights the tight edges form a DAG, so phase 1 finds exactly the vertices whose distance grows. Their new distances are shortest paths in the graph where the unaffected vertices are fixed sources with their final distances, which phase 2 solves with Dijkstra's algorithm. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Bounded by the change.** Let $\delta$ be the set of vertices whose distance changes, and $A$ the size of $\delta$ plus the number of edges with an end in $\delta$. Each phase touches only vertices of $\delta$, their edges, and the far ends of those edges. With a binary heap holding only vertices of $\delta$, an update costs $O(A \log A)$ time.
- **Not bounded by $n$ in a useful way.** In the worst case $A = \Theta(m)$, and an update costs $O(m + n \log n)$, no better than recomputation. There is no amortization: the bound is per update, in terms of the size of its own change.
- **Initialization.** $O(m + n \log n)$, one run of Dijkstra's algorithm with a Fibonacci heap.
- **Queries.** $O(1)$.
- **Space.** $O(m + n)$ for the graph, the distances and the counts.
- **Deterministic.**

## Properties

- **Fully dynamic.** Insertions, deletions and weight changes in any order.
- **Output sensitive.** Ramalingam and Reps call an algorithm bounded when its cost is a function of $\|\delta\|$, the size of the change in input and output, and not of the size of the graph. This algorithm is bounded in that sense; they also proved that some dynamic graph problems have no bounded algorithm.
- **Worst case in terms of $A$.** Every bound holds for each single update, with no amortization, but $A$ is not bounded by a function of $n$ smaller than $m$.
- **Positive weights.** The paper allows zero weights when no cycle has length zero; the version here asks for positive weights so that tight edges form a DAG.

## Variants and improvements

- **Generalized grammar problem.** The paper solves a generalization of shortest paths, the grammar problem of Knuth with superior functions, by the same two phases.
- **Weight changes only.** Frigioni, Marchetti-Spaccamela and Nanni (2000) gave output-bounded algorithms that charge the work to the changed vertices more finely, with better bounds for some classes of sparse graphs.
- **Deletions only, total bound.** For decremental graphs, the [Even-Shiloach tree](/even-shiloach-tree/) gives a total bound of $O(mD)$ for distances up to $D$, which this algorithm does not give.
- **All pairs.** One structure per source gives a simple fully dynamic [all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/) method; the algorithm of [Demetrescu and Italiano](/demetrescu-italiano-apsp/) has a bound in terms of $n$.
- **Batches.** Several edge changes can be applied at once: phase 1 starts from all heads of increased tight edges, and the Dijkstra phase from all heads of decreased edges.

## When to use it

Use it when a weighted graph changes by small local updates and each update moves few distances, as in road networks with traffic changes, routing protocols, or incremental program analysis. In those settings it is often far faster than recomputation and simple to add to a Dijkstra implementation. When one update can change most distances, it gives no gain, and a worst-case or amortized bound in terms of $n$ needs other methods, such as the [Even-Shiloach tree](/even-shiloach-tree/) for deletions only.

## Pitfalls

- **Lowering instead of resetting.** After an increase, the affected vertices must take their distance from unaffected in-neighbors only; reading an affected in-neighbor gives the old, too small value.
- **Counting tight edges with floating point.** Tightness is an equality test. With floating point weights, rounding can make a tight edge look non-tight, and the counts go wrong. Use integers, or compare with a fixed tolerance and accept the risk.
- **Forgetting the out-neighbors.** When $d(x)$ changes, an edge $(x, z)$ to an unchanged vertex $z$ can start or stop being tight, so $c(z)$ must be fixed too.
- **Zero-weight cycles.** With a cycle of weight zero, two vertices can keep each other's counts positive after the real path is gone, and phase 1 misses them.
- **Recounting too much.** Recounting $c(z)$ from all in-edges of every out-neighbor $z$ is correct but can cost more than $O(A)$. Adjust only for the edge from the changed vertex.

## Implementations

## History

Ramalingam and Reps studied incremental computation in the 1990s with the aim of measuring the cost of an update by the size of the change rather than the size of the input. Their 1996 papers gave this algorithm for shortest paths and the grammar problem, and showed that some dynamic graph problems are unbounded. Frigioni, Marchetti-Spaccamela and Nanni refined the output-bounded analysis. The two-phase method is the basis of many practical dynamic shortest path codes, for example in network routing.

## References
