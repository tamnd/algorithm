---
tag: Q2T1JE
kind: algorithm
slug: thorup-zwick-oracle
name: Thorup-Zwick approximate distance oracle
aliases:
- Thorup-Zwick oracle
- approximate distance oracle
area: graphs/shortest-paths
level: research
summary: Preprocesses a graph into a compact structure answering approximate distance queries with stretch 2k-1.
solves: [distance-oracle]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the stretch parameter}
  time: {expected: O(k n^(1/k) (m + n log n))}
  space: {extra: O(k n^(1 + 1/k))}
properties: {deterministic: false, recursive: false}
prereqs: [dijkstra, distance-oracle, all-pairs-shortest-paths]
see_also: [hub-labeling, distance-oracle, all-pairs-shortest-paths, dijkstra, apsp-conjecture, dynamic-spanner, geometric-spanner, single-pair-shortest-path]
sources:
  - paper: doi:10.1145/1044731.1044732
    title: Mikkel Thorup and Uri Zwick, Approximate distance oracles, Journal of the ACM 52(1), 1 to 24 (2005)
    locator: Section 3, the oracle with stretch 2k-1, its query algorithm and the bound on the bunch sizes; Section 4, the preprocessing by cluster growing; the lower bound from the girth conjecture
  - paper: "Mikkel Thorup and Uri Zwick, Approximate distance oracles, Proceedings of the 33rd ACM Symposium on Theory of Computing (STOC), 2001, 183 to 192"
    locator: the conference version of the same results
  - paper: "Surender Baswana and Sandeep Sen, Approximate distance oracles for unweighted graphs in expected O(n^2) time, ACM Transactions on Algorithms 2(4), 557 to 577 (2006)"
    locator: the faster preprocessing for unweighted graphs
  - paper: "Surender Baswana and Sandeep Sen, A simple and linear time randomized algorithm for computing sparse spanners in weighted graphs, Random Structures and Algorithms 30(4), 532 to 563 (2007)"
    locator: (2k-1)-spanners with O(k n^{1+1/k}) edges from the same kind of sampled clusters
  - paper: "Christian Wulff-Nilsen, Approximate distance oracles with improved preprocessing time, Proceedings of the 23rd ACM-SIAM Symposium on Discrete Algorithms (SODA), 2012, 202 to 208"
    locator: the preprocessing time below O(k m n^{1/k}) for dense graphs
  - paper: "Shiri Chechik, Approximate distance oracles with constant query time, Proceedings of the 46th ACM Symposium on Theory of Computing (STOC), 2014, 654 to 663"
    locator: stretch 2k-1, space O(k n^{1+1/k}) and query time O(1)
  - paper: "Manor Mendel and Assaf Naor, Ramsey partitions and proximity data structures, Journal of the European Mathematical Society 9(2), 253 to 275 (2007)"
    locator: oracles with stretch O(k), space O(n^{1+1/k}) and constant query time
---

A distance oracle answers distance queries in a graph from a structure much smaller than the $n \times n$ table of all distances. The oracle of Thorup and Zwick works on an undirected graph with nonnegative weights and a parameter $k \ge 1$. It keeps $O(k n^{1 + 1/k})$ numbers in expectation and answers a query in $O(k)$ time with an estimate $\hat d(u, v)$ that satisfies $d(u, v) \le \hat d(u, v) \le (2k - 1)\, d(u, v)$. The ratio $2k - 1$ is the *stretch*. For $k = 1$ the oracle is the full table, for $k = 2$ it keeps $O(n^{1.5})$ numbers with stretch 3, and for $k = \lceil \log n \rceil$ it keeps $O(n \log n)$ numbers with stretch $O(\log n)$. If Erdős's girth conjecture is true, no oracle with stretch less than $2k + 1$ can use fewer than $\Omega(n^{1 + 1/k})$ bits for all graphs, so the trade-off cannot be much better.

## In plain words

Pick a few places at random as landmarks, then a few of those as more important landmarks, and so on for a fixed number of levels.

Every place remembers, for each level, its nearest landmark and the distance to it. It also remembers its *bunch*: each landmark that is nearer to it than every landmark of the next level up, with the distance.

To estimate the distance between two places, check if the first place is in the bunch of the second. If not, take the nearest landmark of the next level from the other side, and check again. Repeat until a landmark is in a bunch. The answer is the distance through that landmark. Each step can at most add a fixed amount of error, so the answer is never too far from the truth.

## The problem

Given an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges, weights $w : E \to \mathbb{R}_{\ge 0}$ and an integer $k \ge 1$, build a structure that answers a query $(u, v)$ with a value $\hat d(u, v)$ such that $d(u, v) \le \hat d(u, v) \le (2k - 1)\, d(u, v)$, and $\hat d(u, v) = +\infty$ exactly when $u$ and $v$ are in different components. This is an approximate version of the [distance oracle](/distance-oracle/) problem, and a compact replacement for [all-pairs shortest paths](/all-pairs-shortest-paths/).

**Weight assumptions.** Weights are nonnegative real numbers; weight 0 is allowed, and integer weights are not needed. Negative weights are not allowed. In an undirected graph an edge of negative weight is a [negative cycle](/negative-cycle/) by itself, since a walk can go back and forth along it, so distances are not defined; the implementation rejects negative, infinite and non-numeric weights. The graph may be disconnected. The graph must be undirected: the proof uses $d(u, v) = d(v, u)$ and the triangle inequality in both directions. For directed graphs no oracle with any finite stretch can use $o(n^2)$ bits, because it would answer reachability, and the $2^{n^2/4}$ bipartite digraphs with arcs from one half to the other all have different reachability.

## The algorithm

Write $d(A, v) = \min_{a \in A} d(a, v)$, which is $+\infty$ when $A$ is empty or holds no vertex of the component of $v$, and let $p_i(v)$ be a vertex of $A_i$ with $d(p_i(v), v) = d(A_i, v)$, or *undefined* if $d(A_i, v) = +\infty$. For $w \in A_i \setminus A_{i+1}$ the *cluster* is $C(w) = \{ v : d(w, v) < d(A_{i+1}, v) \}$, and the *bunch* of $v$ is $B(v) = \{ w : v \in C(w) \}$. The bunch of each vertex is stored as a hash table that maps $w$ to $d(w, v)$.

```pseudo id=main
TZ-PREPROCESS(G, w, k)
L1  A_0 ← V
L2  for i ← 1 to k − 1 do A_i ← each vertex of A_{i−1}, kept on its own with probability n^{−1/k}
L3  for i ← 0 to k − 1 do compute d(A_i, v) and p_i(v) for all v by one Dijkstra run from all of A_i at once
L4  A_k ← ∅; d(A_k, v) ← ∞ and p_k(v) undefined for all v
L5  for i ← 0 to k − 1 do for each w in A_i \ A_{i+1} do
L6      run Dijkstra from w, but push a vertex x with key D only if D < d(A_{i+1}, x); this settles exactly C(w)
L7      for each x settled with key D do store B(x)[w] ← D
L8  return the tables d(A_i, ·), p_i(·) and B(·)

TZ-QUERY(u, v)
L9  w ← u; i ← 0
L10 while w is not a key of B(v) do
L11     i ← i + 1
L12     swap u and v
L13     if i = k or p_i(u) is undefined then return ∞
L14     w ← p_i(u)
L15 return d(A_i, u) + B(v)[w]
```

At line L15, $w = p_i(u)$, so $d(A_i, u) = d(w, u)$ and the value is $d(u, w) + d(w, v)$, the weight of a walk from $u$ to $v$ through $w$. For $i = 0$, $p_0(u) = u$ and $d(A_0, u) = 0$.

## Example

Take $k = 2$ and the vertices $a, b, c, d, e, f$ with the edges $ab$ (2), $bc$ (2), $cd$ (1), $de$ (2), $ef$ (1), $fa$ (3) and $be$ (4). Suppose the sample in line L2 is $A_1 = \{c, f\}$; $A_2 = \emptyset$.

**Pivots.** Line L3 for $i = 1$ gives, for $a, b, c, d, e, f$ in order, $p_1 = f, c, c, c, f, f$ with $d(A_1, \cdot) = 3, 2, 0, 1, 1, 0$.

**Bunches.** A vertex $w \in A_0 \setminus A_1 = \{a, b, d, e\}$ is in $B(v)$ when $d(w, v) < d(A_1, v)$, and every vertex of $A_1$ is in every bunch, since $d(A_2, v) = \infty$.

| $v$ | $d(A_1, v)$ | $B(v)$ with distances |
|---|---|---|
| $a$ | 3 | $a$ (0), $b$ (2), $c$ (4), $f$ (3) |
| $b$ | 2 | $b$ (0), $c$ (2), $f$ (5) |
| $c$ | 0 | $c$ (0), $f$ (4) |
| $d$ | 1 | $d$ (0), $c$ (1), $f$ (3) |
| $e$ | 1 | $e$ (0), $c$ (3), $f$ (1) |
| $f$ | 0 | $c$ (4), $f$ (0) |

There are 17 entries, against 36 in the full table. The vertex $a$ is not in $B(b)$, because $d(a, b) = 2$ is not less than $d(A_1, b) = 2$.

**Query $(a, b)$.** Line L10 finds $a \notin B(b)$. Lines L11 to L14 set $i = 1$, swap to $u = b$, $v = a$, and take $w = p_1(b) = c$. Now $c \in B(a)$, so line L15 returns $d(A_1, b) + B(a)[c] = 2 + 4 = 6$. The true distance is 2, so the stretch is exactly $3 = 2k - 1$: the bound is tight for this graph.

**Query $(b, a)$.** Line L10 finds $b \in B(a)$ at once and returns $0 + 2 = 2$, the exact distance. The answer depends on the order of $u$ and $v$.

**Query $(c, d)$.** $c \in B(d)$, so the answer is $0 + 1 = 1$, exact.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md); the main steps are these.

1. **Clusters are found exactly.** If $x \in C(w)$, every vertex $y$ on a shortest path from $w$ to $x$ is also in $C(w)$: $d(w, y) = d(w, x) - d(y, x) < d(A_{i+1}, x) - d(y, x) \le d(A_{i+1}, y)$. So the restricted Dijkstra in line L6 settles every vertex of $C(w)$ with its distance, and it settles no other vertex, since a key $D \ge d(w, x)$ with $D < d(A_{i+1}, x)$ puts $x$ in $C(w)$.
2. **Upper and lower bounds.** Every returned value is $d(u, w) + d(w, v)$ for some $w$, which is at least $d(u, v)$ by the triangle inequality.
3. **The stretch.** Let $\delta = d(u, v)$, which does not change when $u$ and $v$ swap. Before each test of line L10, $d(w, u) \le i \delta$ for the current $u$. This is true for $i = 0$. If $w \notin B(v)$, then $d(A_{i+1}, v) \le d(w, v)$: either $w \in A_{i+1}$, or $w \in A_i \setminus A_{i+1}$ and $v \notin C(w)$. So $d(A_{i+1}, v) \le d(w, u) + \delta \le (i + 1) \delta$, and after the swap the new $w = p_{i+1}(v)$ is that close to the new $u$. When the loop stops, the answer is at most $2 d(w, u) + \delta \le (2i + 1) \delta$.
4. **The loop stops in time.** If $\delta < \infty$, step 3 shows that $A_{i+1}$ meets the component when the test fails at level $i$. If $j$ is the last level that meets the component, every vertex of $A_j$ in the component is in every bunch there, since $d(A_{j+1}, v) = \infty$. So the loop stops with $i \le j \le k - 1$ and $p_i(u)$ defined, and the stretch is at most $2k - 1$. If $\delta = \infty$, no vertex of the component of $u$ is in $B(v)$, so line L13 returns $\infty$ by the time $i = k$.

Preprocessing runs $k$ plus at most $n$ Dijkstra searches, and a query makes at most $k$ steps, so both terminate.

## Complexity

- **Space.** For a fixed $v$ and $i \le k - 2$, list the vertices of $A_i$ by distance from $v$. Each is in $A_{i+1}$ with probability $n^{-1/k}$, independently, and only the vertices before the first one in $A_{i+1}$ can be in $B(v)$, so the expected number is less than $n^{1/k}$. For $i = k - 1$, $\mathbb{E}|A_{k-1}| = n^{1/k}$. So $\mathbb{E}|B(v)| \le k n^{1/k}$, and the total space is $O(k n^{1 + 1/k})$ in expectation, plus $O(kn)$ for the pivots.
- **Preprocessing.** Line L3 is $k$ Dijkstra runs, $O(k(m + n \log n))$. In line L6, a vertex $x$ is settled in $C(w)$ once for each $w \in B(x)$ and scans its edges then. With Fibonacci heaps the expected total is $O(k n^{1/k} (m + n \log n))$; Thorup and Zwick state it as $O(k m n^{1/k})$. The implementation uses a binary heap, which adds a factor $\log n$.
- **Query.** At most $k$ steps, each a hash-table lookup, so $O(k)$ time.

## Properties

- **Randomized preprocessing, deterministic queries.** The sample is random; the stretch bound holds for every sample, and only the space and time bounds are expectations. If the space is too large, sample again; the bound then holds with high probability after a few tries.
- **Not symmetric.** $\hat d(u, v)$ and $\hat d(v, u)$ can differ, as in the example. Returning their minimum keeps the bound and costs twice the time.
- **Tight stretch.** The example has a pair with stretch exactly $2k - 1$.
- **Spanner for free.** The union of the shortest-path trees of all clusters is a $(2k - 1)$-spanner with $O(k n^{1 + 1/k})$ edges in expectation.
- **Exact for $k = 1$.** Then $B(v)$ is the whole component of $v$, and the oracle is the distance table.
- **Lower bound.** Thorup and Zwick show, from the girth conjecture, that stretch less than $2k + 1$ needs $\Omega(n^{1 + 1/k})$ bits for some graphs; the conjecture is known for $k = 1, 2, 3$ and 5.

## Variants and improvements

- **Constant query time.** Mendel and Naor gave stretch $O(k)$ with $O(1)$ query time from Ramsey partitions, and Chechik gave stretch $2k - 1$, space $O(k n^{1 + 1/k})$ and $O(1)$ query time.
- **Faster preprocessing.** Baswana and Sen build the oracle for unweighted graphs in expected $O(n^2)$ time, and Wulff-Nilsen improves the time for dense weighted graphs.
- **Spanners.** Baswana and Sen grow the same kind of sampled clusters to build a $(2k - 1)$-spanner in expected $O(km)$ time.
- **Distance labels.** The pivots and bunch of $v$ can be stored with $v$ as a label of expected size $O(k n^{1/k})$; two labels alone give the estimate.
- **Exact oracles for special graphs.** For road networks and other graphs with small labels, [hub labeling](/hub-labeling/) gives exact answers in small space; for planar graphs, exact oracles with near-linear space exist.

## When to use it

Use it when a large undirected graph gets many distance queries, the full table does not fit in memory, and a bounded error is acceptable: network routing, the estimate of latencies between hosts, and the first step of algorithms that need approximate distances. Choose $k = 2$ or 3 for a small error, and $k \approx \log n$ for near-linear space. Do not use it when exact answers are needed and the graph has small exact labels; for a few queries, where [Dijkstra](/dijkstra/) is cheaper than the preprocessing; for directed graphs, where no compact oracle exists; or for graphs that change often.

## Pitfalls

- **Strict versus weak inequality.** The cluster condition is $d(w, v) < d(A_{i+1}, v)$. With $\le$ the bunches can grow without bound, for example on graphs with many equal distances, and the space bound is lost.
- **Forgetting the swap.** The swap in line L12 makes the bound on $d(w, u)$ grow by $\delta$ per level. Without it, the next pivot is taken on the same side, the bound grows by $2\delta$ per level, and the proof gives only stretch $4k - 3$.
- **An empty top level.** $A_{k-1}$ can be empty, or miss a component. The query must then return $\infty$ only when the pair is really disconnected; the test in line L13 does this, because a connected pair always stops at a level that meets its component.
- **Zero weights.** With an edge of weight 0 to a vertex of $A_{i+1}$, $d(A_{i+1}, w) = 0$ and $C(w)$ is empty, so line L6 must not start the search at all. Pushing $w$ with key 0 regardless would add $w$ to its own bunch and break the definition, though not the stretch.
- **Negative weights or directed graphs.** The proof needs symmetric distances and the triangle inequality. Reject both.
- **Reading the stretch as additive.** The error is a factor: a pair at distance 0 gets 0, but a pair at distance 1000 can get up to $1000(2k - 1)$.

## Implementations

## History

Awerbuch, Berger, Cowen and Peleg, and Cohen in the 1990s, studied compact routing and approximate distances with sampled hierarchies, with stretch and space trade-offs worse than $2k - 1$ and $n^{1 + 1/k}$. Thorup and Zwick introduced the term *approximate distance oracle* at STOC 2001, with the bunches, clusters and the swapping query of this page, and showed that the trade-off is optimal under the girth conjecture; the journal version appeared in 2005. The same construction gave compact routing schemes and spanners. Later work reduced the query time to a constant (Mendel and Naor 2007, Chechik 2014) and the preprocessing time (Baswana and Sen 2006, Wulff-Nilsen 2012).

## References
