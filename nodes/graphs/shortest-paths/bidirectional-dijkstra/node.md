---
tag: BPW9SV
kind: algorithm
slug: bidirectional-dijkstra
name: Bidirectional Dijkstra
aliases:
- bidirectional shortest path search
area: graphs/shortest-paths
level: core
summary: Runs Dijkstra forward from s and backward from t, stopping when the searches meet.
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m log n), best: O(1)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [dijkstra, single-pair-shortest-path, bidirectional-search]
see_also: [dijkstra, a-star-search, bidirectional-heuristic-search, alt-algorithm, contraction-hierarchies, highway-hierarchies, binary-heap, dijkstra-correctness]
sources:
  - paper: doi:10.1093/comjnl/9.3.275
    title: T. A. J. Nicholson, Finding the shortest route between two points in a network, The Computer Journal 9(3), 275 to 280 (1966)
    locator: the whole paper (searching from both ends at once)
  - url: https://www.microsoft.com/en-us/research/publication/computing-the-shortest-path-a-search-meets-graph-theory/
    title: Andrew V. Goldberg and Chris Harrelson, Computing the shortest path, A* search meets graph theory, SODA 2005 (Microsoft Research technical report MSR-TR-2004-24)
    locator: the section on bidirectional Dijkstra and its stopping rule (the sum of the two queue minima against the best path seen)
  - paper: doi:10.1007/978-3-319-49487-6_2
    title: Hannah Bast, Daniel Delling, Andrew Goldberg, Matthias Müller-Hannemann, Thomas Pajor, Peter Sanders, Dorothea Wagner and Renato F. Werneck, Route planning in transportation networks, in Algorithm Engineering, LNCS 9220, 19 to 80 (2016)
    locator: Section 2.1, Shortest paths (Dijkstra's algorithm and bidirectional search)
---

Bidirectional Dijkstra finds a shortest path from $s$ to $t$ by running [Dijkstra's algorithm](/dijkstra/) forward from $s$ and, on the reversed graph, backward from $t$, and stopping as soon as the two searches together prove that no path shorter than the best one seen can exist. The stopping rule is that the smallest keys of the two queues add up to at least $\mu$, the length of the shortest $s$-$t$ path found so far through an edge between the two searches. It needs nonnegative weights, has the same worst case as Dijkstra, and on road-like graphs scans roughly half as many vertices. It is the base of almost every fast route-planning method.

## In plain words

To find the fastest drive between two cities, one search spreads out from the start in growing circles, always finishing the nearest unfinished place first. A second search does the same from the goal, following roads backward.

Whenever one search looks at a road whose far end the other search has reached, the two halves join into a full route. Keep the best full route seen so far.

You may stop when the nearest unfinished place of the first search plus that of the second search is already no closer than the best route. Any route still unseen would have to pass through places that far away, so it cannot be shorter.

The two circles are each about half as wide as one circle from start to goal, so together they cover less ground.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a weight $w(u, v) \ge 0$ on each edge, and two vertices $s$ and $t$. The output is $\delta(s, t)$ and a shortest path from $s$ to $t$, or $+\infty$ and no path if $t$ is not reachable from $s$. This is the [single-pair shortest-path problem](/single-pair-shortest-path/).

**Weight assumptions.** All weights are nonnegative real numbers; they need not be integers, and zero weights are allowed. Since no weight is negative, there is no negative cycle. With a negative edge, both searches lose the property that a scanned vertex is final, and the stopping rule fails; the implementation rejects such input. For negative weights use [Bellman-Ford](/bellman-ford/), or [reduced costs](/potential-function-reduced-costs/) to make the weights nonnegative first.

## The algorithm

The forward search uses the edges of $G$; the backward search uses each edge $(u, v)$ as an edge from $v$ to $u$. Index the two sides by $X \in \{f, b\}$, with $Y$ the other side. The minimum of an empty queue is $\infty$.

```pseudo id=main
BIDIRECTIONAL-DIJKSTRA(G, w, s, t)
L1  d_f[v], d_b[v] ← ∞ for all v; d_f[s] ← 0; d_b[t] ← 0
L2  Q_f ← {(0, s)}; Q_b ← {(0, t)}; μ ← ∞ (μ ← 0 if s = t)
L3  loop
L4      if min(Q_f) + min(Q_b) ≥ μ then exit the loop
L5      X ← the side with the smaller queue minimum; Y ← the other side
L6      extract (k, u) with the least key from Q_X; if u is done on side X, go to L4
L7      mark u done on side X
L8      for each edge (u, v) of side X do
L9          if d_X[u] + w(u, v) < d_X[v] then d_X[v] ← d_X[u] + w(u, v), π_X[v] ← u, insert (d_X[v], v) into Q_X
L10         if d_X[u] + w(u, v) + d_Y[v] < μ then μ ← d_X[u] + w(u, v) + d_Y[v], remember the edge (u, v)
L11 return μ, and the path π_f from s to the remembered edge, then π_b to t
```

Each side is a plain Dijkstra search with a lazy-deletion heap (lines L6, L7 and L9). The new parts are line L10, which records every $s$-$t$ path that joins a scanned vertex of one side to a labeled vertex of the other, and the stopping test of line L4. Line L10 must run for every edge scanned, not only when line L9 improves $d_X[v]$. Line L5 can also simply alternate the sides; the stopping rule is correct for any choice.

## Example

The vertices are $s, a, b, x, t$ and the edges $s \to a$ (3), $a \to b$ (4), $b \to t$ (3), $s \to x$ (6), $x \to t$ (6). The shortest path is $s \to a \to b \to t$ with weight 10; the path through $x$ has weight 12.

| step | side, vertex | new labels | $\mu$ | $\min Q_f + \min Q_b$ after |
|---|---|---|---|---|
| 1 | forward $s$ | $d_f$: $a = 3$, $x = 6$ | ∞ | $3 + 0$ |
| 2 | backward $t$ | $d_b$: $b = 3$, $x = 6$ | 12 by $x \to t$, since $d_f[x] = 6$ | $3 + 3$ |
| 3 | forward $a$ | $d_f$: $b = 7$ | 10 by $a \to b$, since $d_b[b] = 3$ | $6 + 3$ |
| 4 | backward $b$ | $d_b$: $a = 7$ | 10 | $6 + 6 = 12 \ge 10$ |

The loop stops before step 5 with $\mu = 10$ and the edge $a \to b$, giving the path $s, a, b, t$. No vertex was scanned by both searches. The vertex $x$ was labeled by both with $d_f[x] + d_b[x] = 12$, and a rule that stops at the first vertex scanned by both sides would, with the sides alternating, scan $x$ forward and then backward and return 12.

**Unreachable.** If the edges $b \to t$ and $x \to t$ are removed, the backward search scans only $t$ and its queue empties, so $\min(Q_b) = \infty$ and the loop stops at once with $\mu = \infty$: no path.

**A negative edge.** With the edge $a \to b$ of weight $-4$ instead, the true distance is $3 - 4 + 3 = 2$. The precondition fails and the implementation raises an error rather than run; with no check, the stopping rule could end with a larger $\mu$, as for Dijkstra itself. A negative cycle makes $\delta(s, t)$ undefined, and the algorithm is not meant to detect one.

## Correctness

**Theorem.** If all weights are nonnegative, the algorithm returns $\mu = \delta(s, t)$, and if $\mu < \infty$, the returned vertex sequence has weight $\mu$ (with zero-weight edges it can contain a closed part of weight 0, which can be cut out).

Two facts carry over from [Dijkstra's algorithm](/dijkstra-correctness/). (a) When a vertex $u$ is marked done on side $X$, $d_X[u]$ is its distance on that side ($\delta(s, u)$ forward, $\delta(u, t)$ backward). (b) At any time, every vertex $v$ not done on side $X$ has its distance on that side at least $\min(Q_X)$.

Line L10 only records weights of real $s$-$t$ walks, so $\mu \ge \delta(s, t)$ always. Suppose the loop stops with $\mu > \delta(s, t)$, and let $P$ be a shortest path. Each vertex $v$ of $P$ has $\delta(s, v) + \delta(v, t) = \delta(s, t) < \mu \le \min(Q_f) + \min(Q_b)$, so $\delta(s, v) < \min(Q_f)$ or $\delta(v, t) < \min(Q_b)$; by (b), $v$ is done forward in the first case and done backward in the second. Distances from $s$ grow along $P$, so the vertices of the first kind form a prefix of $P$. Take the edge $(x, y)$ of $P$ where the prefix ends (with $x = s$ or $y = t$ at the ends, whose labels 0 are final from the start). When the later of the two scans happened, line L10 examined $(x, y)$ with both labels final and set $\mu \le \delta(s, x) + w(x, y) + \delta(y, t) = \delta(s, t)$. That is a contradiction. The full proof, with the path, is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/), with weights added and compared in $O(1)$.

- **Worst case.** Each side scans each vertex at most once and each edge at most once, like one Dijkstra run. With [binary heaps](/binary-heap/) and lazy deletion, the time is $O(m \log m) = O(m \log n)$ for simple graphs, plus $\Theta(n)$ to set up the arrays and the reversed graph. With a [Fibonacci heap](/fibonacci-heap/) it is $O(m + n \log n)$, as for Dijkstra.
- **Best case.** If $s = t$, the answer is immediate. Ignoring the $\Theta(n + m)$ setup (which a long-lived data structure pays once for many queries), the searches may stop after scanning a handful of vertices.
- **Space.** Two copies of the labels, predecessors and queues, and the reversed adjacency lists: $\Theta(n + m)$.
- **In practice.** If the number of vertices within distance $r$ grows like $r^2$, as on road maps, one search from $s$ scans the ball of radius $\delta(s, t)$, while the two searches scan two balls of radius about $\delta(s, t)/2$: about half the work. On graphs that grow exponentially the saving can be much larger, and on a path graph there is none.

## Properties

- **Exact.** It returns a true shortest path, unlike heuristic two-sided searches.
- **Needs the reversed graph.** The backward search follows edges against their direction, so the graph must provide incoming edges.
- **Single pair only.** It stops early, so it does not give distances from $s$ to all vertices.
- **Side choice.** Any rule for choosing the side in line L5 is correct. Choosing the smaller minimum keeps the two radii equal; alternating keeps the work equal.
- **Not a meeting point.** The shortest path may pass through no vertex that both searches scanned, as in the example.

## Variants and improvements

- **Bidirectional A\*.** Run [A\* search](/a-star-search/) from both ends. With two consistent heuristics the stopping rule needs care; one standard fix uses the average of the forward potential and the negated backward potential, so that both sides see the same reduced costs. See [bidirectional heuristic search](/bidirectional-heuristic-search/).
- **[ALT](/alt-algorithm/).** Bidirectional A\* with landmark lower bounds.
- **[Contraction hierarchies](/contraction-hierarchies/).** The query is a bidirectional Dijkstra in which each side only goes up in a vertex order; there the sum rule is not valid, and each side stops only when its own queue minimum reaches $\mu$.
- **[Highway hierarchies](/highway-hierarchies/)** and reach-based pruning restrict each side further with precomputed data.
- **Undirected graphs.** The backward graph is the graph itself.
- **[Bidirectional BFS](/bidirectional-search/).** With unit weights, both sides are breadth-first searches that advance one layer at a time.

## When to use it

Use it for one-off point-to-point queries on large graphs with nonnegative weights, when no preprocessing is available: it is a few lines more than Dijkstra and rarely slower. For many queries on the same road network, preprocessing methods such as [contraction hierarchies](/contraction-hierarchies/) are orders of magnitude faster, and most of them run a bidirectional search on top. For distances from one source to all vertices, use plain Dijkstra.

## Pitfalls

- **Stopping at the first meeting vertex.** Stopping when some vertex is scanned by both searches and returning $d_f + d_b$ at that vertex is wrong, as the example shows: it returns 12 instead of 10. Use the rule of line L4.
- **Updating $\mu$ only on improvement.** Line L10 must run even when line L9 does not change $d_X[v]$, since the label of the other side may be what makes the path short.
- **Stopping on one side's key alone.** Stopping when $\min(Q_f) \ge \mu$ is correct but loses most of the saving, since the forward search then scans the whole ball of radius $\delta(s, t)$.
- **Negative weights.** A negative edge breaks fact (a), and the answer can be too large.
- **Forgetting the reversed graph.** Running the backward search on the forward edges solves a different problem on directed graphs.

## Implementations

The Python version builds the reversed adjacency lists, keeps both sides in two-element lists indexed by side, moves the side with the smaller queue minimum, and rebuilds the path from the remembered edge.

## History

Nicholson (1966) proposed searching from both ends of a route at once. Pohl (1971) studied bidirectional search in heuristic search. The stopping rule on the sum of the two queue minima is the one used in the route-planning work of Goldberg and Harrelson (2005) and in the survey of Bast et al. (2016), where bidirectional Dijkstra is the baseline that preprocessing methods are measured against.

## References
