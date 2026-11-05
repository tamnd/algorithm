---
tag: VS2KBW
kind: algorithm
slug: even-shiloach-tree
name: Even-Shiloach tree
aliases:
- ES-tree
- Even-Shiloach trees
area: graphs/dynamic-graphs
level: research
summary: Maintains bounded-depth shortest-path distances under edge deletions.
solves: [decremental-sssp]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, D: the depth bound}
  time: {worst: O(m D + n)}
  space: {extra: O(m + n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [breadth-first-search, decremental-graph, shortest-path-tree]
see_also: [decremental-sssp, decremental-connectivity, dynamic-single-source-shortest-paths, ramalingam-reps, dynamic-all-pairs-shortest-paths, dynamic-reachability, amortized-update-time, dijkstra]
sources:
  - paper: "Shimon Even and Yossi Shiloach, An on-line edge-deletion problem, Journal of the ACM 28(1), 1 to 4 (1981)"
    locator: the whole paper (levels of a breadth-first search tree under deletions in an undirected graph, O(mn) total time, used for decremental connectivity)
  - paper: "Valerie King, Fully dynamic algorithms for maintaining all-pairs shortest paths and transitive closure in digraphs, Proceedings of the 40th IEEE Symposium on Foundations of Computer Science (FOCS 1999), 81 to 89"
    locator: Section 2 (the decremental shortest path tree for directed graphs with positive integer weights up to a depth d, in O(m d) total time)
  - paper: "Monika R. Henzinger and Valerie King, Fully dynamic biconnectivity and transitive closure, Proceedings of the 36th IEEE Symposium on Foundations of Computer Science (FOCS 1995), 664 to 672"
    locator: the use of decremental breadth-first search trees from many sources for reachability
---

The Even-Shiloach tree keeps the distances from one source vertex in a graph whose edges are only deleted, up to a chosen depth bound $D$. Each vertex holds a level that is its distance from the source, and a pointer into its list of incoming edges. After a deletion, a vertex that loses all edges that give its level moves down one level at a time, and its out-neighbors are checked in turn. A level only grows and is at most $D$, so the total time over all deletions is $O(mD)$, which is $O(mn)$ for exact distances in an unweighted graph. Even and Shiloach (1981) introduced it for undirected graphs, and King (1999) extended it to directed graphs with positive integer weights; it is deterministic and is a building block of most decremental shortest path and reachability algorithms.

## In plain words

Think of the source as the ground floor. Each vertex lives on the floor that equals its distance from the source, and it holds on to one edge from a vertex one floor below (or, with weights, from the right floor below).

When an edge is deleted, a vertex may lose its hold. It looks through its other incoming edges for a new hold on its floor. Edges it has already checked on this floor need not be checked again, because floors only go up. If it finds none, it moves up one floor and starts looking again, and it tells the vertices that hold on to it that they must check too.

A vertex can move up at most $D$ times before it is too far away to care about, so the total work stays bounded.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices, $m$ edges and positive integer weights $w$, a source $s$, and a depth bound $D \ge 0$. A sequence of edge deletions arrives one at a time; the graph is [decremental](/decremental-graph/). After each deletion, the algorithm must answer, for any $v$, the value

$$d_D(v) = \begin{cases} d(s, v) & \text{if } d(s, v) \le D, \\ \infty & \text{otherwise,} \end{cases}$$

where $d(s, v)$ is the current distance. It can also report a [shortest path tree](/shortest-path-tree/) of the vertices with finite $d_D$. Undirected graphs are the special case with two opposite arcs per edge. With $D = n - 1$ and unit weights, $d_D = d$ exactly. This is a bounded form of [decremental single-source shortest paths](/decremental-sssp/).

## The algorithm

Each vertex $v$ keeps a level $\ell(v)$, its list $\mathrm{in}(v)$ of incoming edges in a fixed order, and a scan pointer $p(v)$ into that list. An edge $(u, v)$ **supports** $v$ if it is present and $\ell(u) + w(u, v) = \ell(v)$.

```pseudo id=main
INIT
L1  ℓ ← the distances from s by BFS or Dijkstra, with ℓ(v) = ∞ if it is above D; p(v) ← the first supporting edge

DELETE(u, v)
L2  mark the edge (u, v) as deleted
L3  Q ← {v}
L4  while Q is not empty: take x from Q; skip it if x = s or ℓ(x) = ∞
L5      advance p(x) over the edges of in(x) that do not support x
        if p(x) is at a supporting edge then continue with the next x
L6      ℓ(x) ← ℓ(x) + 1; p(x) ← the first edge of in(x)
L7      if ℓ(x) > D then ℓ(x) ← ∞ else put x into Q
L8      put the head of every present out-edge of x into Q

QUERY(v)
L9  return ℓ(v)
```

Line L5 is the key to the bound. While $\ell(x)$ stays the same, an edge that did not support $x$ never supports it later, because levels only grow and deleted edges stay deleted. So the pointer moves only forward at each level. Line L6 raises $x$ by one when no edge supports it. Then all edges must be checked again at the new level, and the vertices that may have been supported by $x$ must check their own support (line L8). Line L7 drops a vertex whose level passes $D$.

The tree edge of $v$ is the edge at $p(v)$, which gives the shortest path tree.

## Example

Take the directed graph with unit weights and the edges $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 4$, $2 \to 4$, $4 \to 5$, $1 \to 5$, source 0 and $D = 4$.

| deletion | $\ell(0)$ | $\ell(1)$ | $\ell(2)$ | $\ell(3)$ | $\ell(4)$ | $\ell(5)$ | level steps |
|---|---|---|---|---|---|---|---|
| none | 0 | 1 | 1 | 2 | 2 | 2 | |
| $2 \to 4$ | 0 | 1 | 1 | 2 | 3 | 2 | 1 |
| $0 \to 1$ | 0 | $\infty$ | 1 | 2 | 3 | 4 | 6 |
| $2 \to 3$ | 0 | $\infty$ | 1 | $\infty$ | $\infty$ | $\infty$ | 6 |

After the deletion of $2 \to 4$, vertex 4 finds no support at level 2, rises to 3 and is supported by $3 \to 4$. Vertex 5 is checked and keeps its support $1 \to 5$. After the deletion of $0 \to 1$, vertex 1 has no incoming edge left, so it rises one level at a time until it passes $D$, four steps. Vertex 5 follows it up: at level 3 it is supported by $1 \to 5$ while $\ell(1) = 2$, and at level 4 by $4 \to 5$. Vertex 3 keeps the support $2 \to 3$. After the deletion of $2 \to 3$, vertices 3, 4 and 5 lose all paths from 0 and each rises until it passes $D$. The last column counts the raises of line L6. In the second row, for example, vertex 1 rises four times and vertex 5 twice.

## Correctness

Three facts hold at all times. First, levels never drop below the true capped distances: $\ell(v) \le d_D(v)$. A vertex rises from $\ell$ to $\ell + 1$ only when no in-neighbor $u$ has $\ell(u) + w(u, v) = \ell$, while every in-neighbor has $\ell(u) + w(u, v) \ge \ell$; if $d(s, v)$ were $\ell$, its last edge on a shortest path would come from a $u$ with $\ell(u) \le d(s, u) = \ell - w(u, v)$, which would support $v$. Second, the edges before $p(v)$ do not support $v$. Third, when the queue is empty, every finite vertex other than $s$ is supported, so following the supporting edges back gives a path from $s$ of length $\ell(v)$, which shows $\ell(v) \ge d(s, v)$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Initialization.** $O(m + n)$ with [breadth-first search](/breadth-first-search/) for unit weights, or $O(m + n \log n)$ with [Dijkstra's algorithm](/dijkstra/).
- **Scanning.** At a fixed level, the pointer of $v$ passes each edge of $\mathrm{in}(v)$ at most once. The level of $v$ takes at most $D + 2$ values before it becomes $\infty$. So all scans of $v$ cost $O(\deg_{\mathrm{in}}(v) \cdot D)$ in total.
- **Raises.** Each raise of $x$ puts $O(\deg_{\mathrm{out}}(x))$ vertices into the queue, and each queue entry costs $O(1)$ beyond the scanning. Over at most $D + 1$ raises per vertex, this is $O(\deg_{\mathrm{out}}(x) \cdot D)$.
- **Total.** $O(mD + n)$ time over the whole sequence of deletions, plus $O(1)$ per deletion, in the worst case for the whole sequence. Per deletion the bound is amortized: one deletion can raise many vertices. With unit weights and $D = n$, this is $O(mn)$ in total. Queries take $O(1)$.
- **Space.** $O(m + n)$.
- **Deterministic.** No random choices; the bound holds against an [adaptive adversary](/adaptive-adversary/).

## Properties

- **Deletions only.** An insertion can lower levels, which breaks the pointer argument. Weight increases are allowed, since they also only raise distances.
- **Total time bound.** The bound is for all deletions together, so it is an amortized bound per deletion.
- **Bounded depth.** The cost grows with $D$, not with $n$, so the tree is cheap for short distances. Many algorithms run it with a small $D$ on graphs with shortcuts.
- **Exact.** For distances up to $D$ it is exact, with integer weights.

## Variants and improvements

- **Directed and weighted.** King (1999) gave the form on this page, for directed graphs with positive integer weights, in $O(mD)$ total time.
- **Many sources.** Running one tree from each vertex keeps all distances up to $D$ in $O(mnD)$ total time; this is a part of decremental and fully dynamic [all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/) and of [dynamic reachability](/dynamic-reachability/) algorithms, for example those of Henzinger and King and of King.
- **Approximate distances.** With weights rounded to powers of $1 + \varepsilon$ at different scales, or on graphs with added shortcut edges (hop sets), Even-Shiloach trees give $(1 + \varepsilon)$-approximate decremental distances much faster; see [decremental single-source shortest paths](/decremental-sssp/).
- **Undirected connectivity.** Even and Shiloach used the tree for [decremental connectivity](/decremental-connectivity/): a vertex whose level passes $n$ is no longer connected to the source.
- **Fully dynamic repair.** For both insertions and deletions, the [Ramalingam-Reps algorithm](/ramalingam-reps/) repairs only the affected part, without a total bound.

## When to use it

Use an Even-Shiloach tree when edges only disappear, as in failure analysis or as a part of a larger decremental algorithm, and the distances of interest are small. It is simple and deterministic, and with small $D$ it is fast. For large distances on large graphs, the $O(mn)$ total can be too slow, and approximate methods are better. For graphs that also gain edges, use a fully dynamic method or recompute.

## Pitfalls

- **Restarting the scan at the wrong time.** The pointer may only move forward while the level stays the same, and must go back to the start when the level rises. Starting the scan from the beginning on every check loses the $O(mD)$ bound, and not resetting it after a raise misses supporting edges.
- **Raising more than one at a time.** Jumping a vertex directly to the minimum over its in-neighbors seems faster, but it charges the scan of a vertex to fewer levels and needs a priority queue; the simple bound counts single steps.
- **Forgetting the children.** After a raise, every out-neighbor that may have been supported by $x$ must be checked; otherwise a vertex keeps a level that is too small.
- **Zero weights.** With a zero-weight cycle, two vertices can support each other after the real path is gone. The weights must be positive.

## Implementations

## History

Even and Shiloach (1981) solved decremental connectivity in undirected graphs with this tree, in $O(mn)$ total time for the breadth-first search levels. Henzinger and King (1995) used such trees from many sources for dynamic transitive closure, and King (1999) extended the tree to directed graphs with integer weights and a depth bound, as a part of her fully dynamic all-pairs shortest paths algorithm. Since then it has been a building block of most decremental shortest path algorithms, including the approximate algorithms with almost-linear total time.

## References
