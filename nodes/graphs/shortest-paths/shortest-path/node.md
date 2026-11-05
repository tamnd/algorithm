---
tag: 7KEEDK
kind: definition
slug: shortest-path
name: Shortest path
aliases:
- minimum-weight path
area: graphs/shortest-paths
level: intro
summary: A path from s to t whose total edge weight is minimum among all s-t paths.
prereqs: [weighted-graph, directed-graph, walk, simple-path]
see_also: [single-pair-shortest-path, single-source-shortest-paths, all-pairs-shortest-paths, negative-cycle, shortest-path-optimal-substructure, shortest-path-tree, dijkstra, bellman-ford]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, introduction (the definition of path weight and of the shortest-path weight, negative-weight edges, cycles, representing shortest paths)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths (the definitions and the discussion of negative edges)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 8, Shortest paths, arbitrary lengths
---

A shortest path from a vertex $s$ to a vertex $t$ of a [weighted](/weighted-graph/) [directed graph](/directed-graph/) is a [walk](/walk/) from $s$ to $t$ whose total edge weight is the least among all walks from $s$ to $t$. Its weight is the *distance* $\delta(s, t)$. A shortest path exists exactly when $t$ is reachable from $s$ and no walk from $s$ to $t$ can enter a [negative cycle](/negative-cycle/); then one shortest path is a [simple path](/simple-path/). Every shortest-path problem and algorithm on this site uses this definition.

## Definition

Let $G = (V, E)$ be a directed graph with a weight function $w : E \to \mathbb{R}$. A *walk* from $u$ to $v$ is a sequence $p = \langle v_0, v_1, \ldots, v_k \rangle$ with $v_0 = u$, $v_k = v$, $k \ge 0$ and $(v_{i-1}, v_i) \in E$ for $1 \le i \le k$. CLRS calls this a path and calls it *simple* when the $v_i$ are distinct. The *weight* of $p$ is

$$w(p) = \sum_{i=1}^{k} w(v_{i-1}, v_i).$$

The walk with $k = 0$ has weight 0. The *shortest-path weight* or *distance* from $u$ to $v$ is

$$\delta(u, v) = \begin{cases} \inf\{\, w(p) : p \text{ is a walk from } u \text{ to } v \,\} & \text{if such a walk exists,} \\ +\infty & \text{otherwise.} \end{cases}$$

A *shortest path* from $u$ to $v$ is a walk $p$ from $u$ to $v$ with $w(p) = \delta(u, v)$.

**The three cases.** For each pair $(u, v)$ exactly one of these holds.

1. $v$ is not reachable from $u$. Then $\delta(u, v) = +\infty$ and there is no shortest path.
2. Some walk from $u$ to $v$ passes through a vertex of a cycle $C$ with $w(C) < 0$. Then $\delta(u, v) = -\infty$ and there is no shortest path: go around $C$ one more time and the weight drops by $|w(C)|$.
3. Otherwise $\delta(u, v)$ is a finite number, and some simple path from $u$ to $v$ has weight $\delta(u, v)$.

*Proof of case 3.* Each walk from $u$ to $v$ that repeats a vertex $x$ contains a closed walk from $x$ to $x$. That closed walk splits into cycles, and each of them passes through a vertex of a walk from $u$ to $v$, so each has weight at least 0 by the assumption of case 3. Remove the closed walk: the result is a shorter walk from $u$ to $v$ whose weight is at most the old weight. Repeat until no vertex repeats; this ends because the number of edges drops by at least one each time. So for each walk there is a simple path of no larger weight. There are finitely many simple paths, and one exists because $v$ is reachable. The least weight among them is the infimum, it is finite, and that simple path attains it. $\square$

**The weight assumptions.** Pages on this site state which of these they assume.

- *Nonnegative weights*: $w(e) \ge 0$ for all $e$. Then case 2 never occurs, and [Dijkstra's algorithm](/dijkstra/) applies.
- *Integer weights*: $w(e) \in \mathbb{Z}$, often with $|w(e)| \le W$. Algorithms that use buckets or scaling need this.
- *No negative cycles*: $w(C) \ge 0$ for each directed cycle $C$. Negative edges are allowed. Then case 2 never occurs, and the [Bellman-Ford algorithm](/bellman-ford/) applies.

**Undirected graphs.** In an undirected graph each edge $\{u, v\}$ is read as the two arcs $(u, v)$ and $(v, u)$ of the same weight. With nonnegative weights this is correct. With a negative edge it is not: the two arcs form a cycle of weight $2w(u, v) < 0$, while a walk in the undirected graph may not want to use the edge twice. Shortest simple paths in undirected graphs with negative edges and no negative cycles need methods based on matchings, not the algorithms of this area.

## Examples and non-examples

The examples use the graph of CLRS Figure 22.4 on the vertices $s, t, x, y, z$, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7). It has eight simple cycles, with weights 0, 1, 3, 3, 4, 18, 22 and 25, so it has no negative cycle. The cycle $s \to y \to x \to t \to z \to s$ has weight exactly 0: a walk can go around it any number of times and keep its weight, so a vertex can have infinitely many shortest walks, but it still has a simple shortest path.

| pair | the shortest path | distance | the next simple path |
|---|---|---|---|
| $s, t$ | $s \to y \to x \to t$ | 2 | $s \to t$, weight 6 |
| $s, x$ | $s \to y \to x$ | 4 | $s \to t \to z \to x$, weight 9 |
| $s, y$ | $s \to y$ | 7 | $s \to t \to y$, weight 14 |
| $s, z$ | $s \to y \to x \to t \to z$ | $-2$ | $s \to t \to z$, weight 2 |
| $s, s$ | $\langle s \rangle$ | 0 | none |

- **The path with the fewest edges is not the shortest.** From $s$ to $z$ the two-edge path $s \to t \to z$ has weight 2, and the four-edge path has weight $-2$.
- **A shortest path need not be unique.** If every arc has weight 1, the distance is the number of edges, as in [breadth-first search](/breadth-first-search/), and a grid has many shortest paths between two far corners.
- **Non-example: a negative cycle.** Change the weight of $x \to t$ to $-6$. The cycle $t \to x \to t$ has weight $-1$ and $s$ reaches it, so $\delta(s, v) = -\infty$ for $v \in \{s, t, x, y, z\}$: each of them is reachable from that cycle. No walk is a shortest path.
- **Non-example: an unreachable vertex.** Add a vertex $u$ with only the arc $u \to s$. Then $\delta(s, u) = +\infty$ and there is no path at all, while $\delta(u, s) = 0$.
- **Non-example: the shortest simple path with a negative cycle.** When negative cycles exist, one can still ask for the least weight of a *simple* path. This is a different problem and it is [NP-hard](/np-hard/): with all weights $-1$, a simple path of weight $-(n - 1)$ from $s$ to $t$ is a [Hamiltonian path](/hamiltonian-path/).

## Related definitions

- [Walk](/walk/) and [simple path](/simple-path/): the objects whose weight is minimized.
- [Negative cycle](/negative-cycle/): the reason for case 2.
- [Edge relaxation](/edge-relaxation/): the step that improves an estimate of $\delta(s, v)$ along one arc.
- [Optimal substructure of shortest paths](/shortest-path-optimal-substructure/): each subpath of a shortest path is a shortest path.
- [Shortest-path tree](/shortest-path-tree/): one shortest path from a source to each vertex, stored as a tree.
- [Single-pair](/single-pair-shortest-path/), [single-source](/single-source-shortest-paths/) and [all-pairs](/all-pairs-shortest-paths/) shortest paths: the problems that ask for $\delta$ on one pair, one row or the whole matrix.
- [Longest path problem](/longest-path-problem/): the maximum version, which is hard for simple paths in general graphs.

## References
