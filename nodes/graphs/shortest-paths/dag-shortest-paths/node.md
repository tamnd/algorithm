---
tag: 277N5Y
kind: algorithm
slug: dag-shortest-paths
name: Shortest paths in a DAG
aliases:
- DAG shortest path via topological order
area: graphs/shortest-paths
level: intro
summary: Relaxes edges in topological order, giving linear-time shortest paths in a DAG with arbitrary weights.
solves: [single-source-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [edge-relaxation, topological-sort, directed-acyclic-graph]
see_also: [kahns-algorithm, critical-path, pert-chart, longest-path-problem, longest-to-shortest-paths-reduction, dag-dynamic-programming, bellman-ford, dijkstra]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.2, Single-source shortest paths in directed acyclic graphs (DAG-SHORTEST-PATHS, its correctness theorem, and PERT charts)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths, Section 8.5 (directed acyclic graphs and the dynamic program over a topological order)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 4.7, Shortest paths in dags
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.4, Shortest Paths (acyclic edge-weighted digraphs, longest paths, and the critical path method for parallel job scheduling)
---

Shortest paths in a DAG is the algorithm that solves the [single-source shortest-path problem](/single-source-shortest-paths/) on a [directed acyclic graph](/directed-acyclic-graph/) by [relaxing](/edge-relaxation/) the edges out of each vertex in a [topological order](/topological-sort/). It takes $\Theta(n + m)$ time, the best possible, and it allows **negative** weights, because a DAG has no cycle at all. Negate the weights and the same pass finds longest paths, which is how the [critical path](/critical-path/) of a project is computed.

## In plain words

In a graph with no loops, you can line up the vertices so that every edge points forward. Then any route from the start visits vertices from left to right.

Walk along the line from left to right. When you reach a vertex, every edge that can bring you there starts at a vertex further left, and you have already handled all of those. So the best known cost of this vertex is already final. Use it to update the vertices that its edges point to, and move on.

Each edge is looked at once, so the work is about the size of the graph. Negative costs do no harm, because no loop can make a cost fall again and again.

## The problem

The input is a directed graph $G = (V, E)$ with no directed cycle, with $n$ vertices and $m$ edges, a real weight $w(u, v)$ on each edge, and a source $s$. The output is $\delta(s, v)$ for each $v$ and a [shortest-path tree](/shortest-path-tree/) in the predecessors $\pi$.

**Weight assumptions.** Weights are any real numbers; negative weights are allowed, and they need not be integers. A DAG has no cycle, so it has no negative cycle, and each distance is a finite number or $+\infty$. A vertex that $s$ cannot reach gets $\delta(s, v) = +\infty$. If the input has a directed cycle, the topological sort fails and the algorithm reports it; it never returns wrong distances for such an input.

## The algorithm

```pseudo id=main
DAG-SHORTEST-PATHS(G, w, s)
L1  order ← TOPOLOGICAL-SORT(G)                 ▷ reports a cycle if G has one
L2  for each v in V do d[v] ← ∞, π[v] ← nil
L3  d[s] ← 0
L4  for each u in order do
L5      if d[u] ≠ ∞ then                       ▷ skip vertices that s does not reach
L6          for each edge (u, v) out of u do
L7              if d[u] + w(u, v) < d[v] then  ▷ RELAX(u, v, w)
L8                  d[v] ← d[u] + w(u, v), π[v] ← u
L9  return d, π
```

Line L1 can use [Kahn's algorithm](/kahns-algorithm/) or the reverse finishing order of [depth-first search](/depth-first-search/); both take $\Theta(n + m)$ and detect a cycle. Lines L4 to L8 visit the vertices in that order and relax each edge out of each reachable vertex once. The vertices before $s$ in the order are not reachable from $s$, so a program may start the loop at $s$. Line L5 is not needed for correctness when $\infty + w = \infty$, but it keeps a stored large number from leaking through a negative edge.

## Example

The DAG has the vertices $q, s, a, b, c, d, e$ and the edges $q \to s$ (3), $q \to c$ ($-9$), $s \to a$ (5), $s \to b$ (3), $b \to a$ (1), $a \to c$ (6), $b \to c$ (7), $b \to d$ (4), $c \to d$ ($-1$), $c \to e$ (1), $d \to e$ ($-2$), $a \to d$ (2). The source is $s$. Kahn's algorithm gives the order $q, s, b, a, c, d, e$.

| vertex $u$ | relaxations that change $d$ | $d$ for $q\,s\,a\,b\,c\,d\,e$ after |
|---|---|---|
| start | | ∞ 0 ∞ ∞ ∞ ∞ ∞ |
| $q$ | none, $d[q] = \infty$ | ∞ 0 ∞ ∞ ∞ ∞ ∞ |
| $s$ | $a = 5$, $b = 3$ | ∞ 0 5 3 ∞ ∞ ∞ |
| $b$ | $a = 4$, $c = 10$, $d = 7$ | ∞ 0 4 3 10 7 ∞ |
| $a$ | $d = 6$ ($c$: $4 + 6 = 10$ is not smaller) | ∞ 0 4 3 10 6 ∞ |
| $c$ | $e = 11$ ($d$: $10 - 1 = 9$ is not smaller) | ∞ 0 4 3 10 6 11 |
| $d$ | $e = 4$ | ∞ 0 4 3 10 6 4 |
| $e$ | no edges | ∞ 0 4 3 10 6 4 |

So $\delta(s, \cdot) = (\infty, 0, 4, 3, 10, 6, 4)$, and the shortest path to $e$ is $s \to b \to a \to d \to e$ with weight $3 + 1 + 2 - 2 = 4$. The vertex $q$ is not reachable, and its edge $q \to c$ of weight $-9$ has no effect.

**Longest paths.** With all weights negated, the same run gives the longest path weights from $s$: $0, 5, 3, 11, 10, 12$ for $s, a, b, c, d, e$. The longest path to $e$ is $s \to a \to c \to e$, with weight $5 + 6 + 1 = 12$.

## Correctness

**Theorem.** If $G$ is a DAG, then at the end $d[v] = \delta(s, v)$ for each $v$, and for each $v \ne s$ with $d[v] < \infty$, $d[v] = d[\pi[v]] + w(\pi[v], v)$, so the predecessor edges form a shortest-path tree.

**Invariant.** When the loop of line L4 reaches the vertex $u$, $d[u] = \delta(s, u)$. A shortest path to $u$, if one exists, is $s \leadsto x \to u$, and $x$ comes before $u$ in the topological order. By induction $d[x] = \delta(s, x)$ when $x$ was visited, and then line L7 relaxed $(x, u)$, so by the convergence property $d[u] = \delta(s, u)$. This is the [path-relaxation property](/edge-relaxation/) with the edges of each path relaxed in path order. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Time.** The topological sort takes $\Theta(n + m)$. Lines L2 and L3 take $\Theta(n)$. The loop visits each vertex once and relaxes each edge at most once, in $O(1)$ each. The total is $\Theta(n + m)$ in every case, since the sort reads the whole graph.
- **Space.** The arrays $d$, $\pi$, the order and the in-degrees of Kahn's algorithm take $\Theta(n)$ extra space.
- **Optimality.** Any algorithm for this problem must read each edge in the worst case, since an unread edge could have a very negative weight and change an answer. So $\Omega(n + m)$ is a lower bound, and the algorithm is optimal.

## Properties

- **Any real weights.** Negative weights are allowed; only cycles are forbidden.
- **One pass.** Each edge is relaxed once, as in Dijkstra's algorithm, but the order comes from the graph, not from the distances.
- **No priority queue.** The order is fixed before the distances are known.
- **Longest paths.** Longest paths in a general graph are [NP-hard](/np-hard/), but in a DAG they are shortest paths with negated weights. See the [longest-to-shortest reduction](/longest-to-shortest-paths-reduction/).
- **Dynamic programming.** The loop is the [DAG dynamic program](/dag-dynamic-programming/) $\delta(s, v) = \min_{(u, v) \in E} (\delta(s, u) + w(u, v))$, evaluated in topological order with a "push" step.

## Variants and improvements

- **Pull form.** Visit $v$ in order and set $d[v] = \min_{(u, v) \in E} (d[u] + w(u, v))$ over the edges into $v$. Same cost; it needs the lists of incoming edges.
- **[Critical path](/critical-path/) and [PERT charts](/pert-chart/).** Jobs are vertices or edges, durations are weights, and the longest path is the least time to finish the project.
- **Counting shortest paths.** Keep with $d[v]$ the number of paths that reach it: add the count of $u$ on a tie and replace it on an improvement.
- **All sources.** Run the pass from each vertex: $O(n(n + m))$ for [all-pairs shortest paths](/all-pairs-shortest-paths/) in a DAG with any weights.

## When to use it

Use it whenever the graph is known to be acyclic: task graphs, schedules, the state graphs of many dynamic programs, and alignment grids. It beats [Dijkstra's algorithm](/dijkstra/) (no heap, no $\log n$) and [Bellman-Ford](/bellman-ford/) (one pass instead of $n - 1$), and it allows negative weights. If the graph may have cycles, it does not apply; use Bellman-Ford or, with nonnegative weights, Dijkstra.

## Pitfalls

- **The wrong order.** Relaxing in the order of vertex numbers, or in BFS order, is not enough: a vertex can be visited before one of its in-neighbors. Line L1 must give a topological order.
- **Assuming the graph is acyclic.** If the input may have a cycle, line L1 must detect it. Without the check, the pass returns values that are not distances.
- **Longest paths with infinity.** When weights are negated for longest paths, an unreachable vertex has $d = +\infty$, which turns into $-\infty$ after negating back. Treat it as "unreachable", not as a very short path.
- **Infinity as a large number.** Without line L5, a large constant for $\infty$ plus the weight $-9$ of the edge $q \to c$ in the example becomes a finite estimate for $c$ if the code does not compare against the constant.

## Implementations

The Python version computes the order with Kahn's algorithm and raises an error when the graph has a cycle.

## History

The method is the standard dynamic program on an acyclic graph. CLRS presents it with the PERT chart of project planning; Sedgewick and Wayne present it with the critical path method for job scheduling.

## References
