---
tag: J10R6J
kind: algorithm
slug: thorup-undirected-sssp
name: Thorup's linear-time undirected SSSP
aliases:
- Thorup's SSSP
area: graphs/shortest-paths
level: research
summary: Solves SSSP on undirected graphs with positive integer weights in O(m) time, beating Dijkstra without sorting.
solves: [single-source-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m + n)}
  space: {extra: O(m + n)}
properties: {deterministic: true, recursive: true}
prereqs: [dijkstra, single-source-shortest-paths, minimum-spanning-tree, bucket-queue, word-ram]
see_also: [sorting-barrier, dijkstra, dial-algorithm, bucket-queue, minimum-spanning-tree, kruskal, breaking-sorting-barrier-sssp, radix-heap]
sources:
  - paper: doi:10.1145/316542.316548
    title: Mikkel Thorup, Undirected single-source shortest paths with positive integer weights in linear time, Journal of the ACM 46(3), 362 to 394 (1999)
    locator: Sections 2 to 4 (the component hierarchy, the bucketing lemma and the Visit procedure) and Sections 5 to 8 (the linear-time data structures)
  - paper: "Michael L. Fredman and Dan E. Willard, Trans-dichotomous algorithms for minimum spanning trees and shortest paths, Journal of Computer and System Sciences 48(3), 533 to 551 (1994)"
    locator: atomic heaps and the linear-time minimum spanning tree on the word RAM, both used by Thorup
  - paper: "Mikkel Thorup, Floats, integers, and single source shortest paths, Journal of Algorithms 35(2), 189 to 201 (2000)"
    locator: the extension of the algorithm to floating-point weights
  - paper: "Seth Pettie and Vijaya Ramachandran, A shortest path algorithm for real-weighted undirected graphs, SIAM Journal on Computing 34(6), 1398 to 1431 (2005)"
    locator: the hierarchy approach in the comparison-addition model and its relation to Thorup's algorithm
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.3, Dijkstra's algorithm, and the chapter notes of Chapter 22 (Thorup's linear-time algorithm for undirected graphs)
---

Thorup's algorithm computes [single-source shortest paths](/single-source-shortest-paths/) in an undirected graph with positive integer weights in $O(m)$ time on the [word RAM](/word-ram/). It is the first algorithm to beat [Dijkstra](/dijkstra/) for this problem by more than a constant factor, and it does so by not visiting the vertices in order of distance, which avoids the [sorting barrier](/sorting-barrier/). It builds a *component hierarchy*: the level-$i$ components are the connected components of the edges of weight below $2^i$. Two different components on level $i - 1$ inside one level-$i$ component are joined only by edges of weight at least $2^{i-1}$, so the vertices of a component can be settled in buckets of width $2^{i-1}$, in any order inside a bucket, without waiting for the rest of the graph. The hierarchy comes from a [minimum spanning tree](/minimum-spanning-tree/), and special data structures make the whole run linear.

## In plain words

Dijkstra's method always continues from the closest unfinished place. To find that place quickly it keeps the places sorted by distance, and sorting costs extra time.

Thorup's idea: group the places into clusters joined by short roads. Every road that leaves a cluster is long. So while you work inside one cluster, nothing outside can reach it soon, and you can finish its places without checking the rest of the map.

Groups are nested: small clusters of very short roads inside larger clusters of short roads, and so on. At each size you only need to know roughly which cluster is closest, by putting clusters in buckets, and rough order needs no sorting.

## The problem

Given an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges, weights $w : E \to \{1, 2, 3, \ldots\}$ and a source $s$, compute $\delta(s, v)$ for every vertex $v$.

**Weight assumptions.** Weights are positive integers that fit in a machine word. The algorithm uses $\lfloor D / 2^i \rfloor$ by bit shifts, so integrality matters; Thorup gave a separate extension to floating-point weights. Zero weights are handled by first contracting the components of zero-weight edges, which all have the same distance. Negative weights are not allowed: in an undirected graph a negative edge $\{u, v\}$ already gives the negative closed walk $u, v, u$, so shortest walks do not exist. There are no negative cycles. Vertices not reachable from $s$ get $\delta(s, v) = +\infty$.

**The hierarchy.** Let $r$ be the least integer with $2^r$ greater than every weight. For $i = 0, \ldots, r$, the *level-$i$ components* are the connected components of the graph with only the edges of weight less than $2^i$. Level 0 has only single vertices, because all weights are at least 1, and level $r$ has the connected components of $G$. Each level-$i$ component is a union of level-$(i-1)$ components, its *children*, so the components form a tree.

## The algorithm

$D(v)$ is the tentative distance. A vertex is *settled* when its distance is final.

```pseudo id=main
THORUP-SSSP(G, w, s)
L1  build the component hierarchy for levels 0, ..., r
L2  D(s) ← 0; D(v) ← ∞ for every other v
L3  VISIT(the level-r component of s, r, ∞)
L4  return D

VISIT(x, i, hi)                       ▷ settles the vertices of x with distance below hi
L5  if i = 0 then
L6      let v be the only vertex of x; settle v
L7      for each edge {v, u} with u not settled do D(u) ← min(D(u), D(v) + w(v, u))
L8  else while the least D(v) over the unsettled vertices v of x is less than hi do
L9      let v be such a vertex of least D(v); b ← ⌊D(v) / 2^(i−1)⌋
L10     VISIT(the level-(i−1) component of v, i − 1, (b + 1) · 2^(i−1))
```

Line L9 puts the children of $x$ into buckets of width $2^{i-1}$ by their least tentative distance and takes a child in the lowest bucket. Line L10 lets that child settle everything below the end of the bucket. Any child in the lowest bucket would do; taking the child of the vertex with the least $D$ is one valid choice.

**Why buckets are safe.** Take a level-$i$ component $x$. A path that enters a child $y$ of $x$ from outside $y$ crosses an edge of weight at least $2^{i-1}$, since otherwise its vertices would be in the same level-$(i-1)$ component. If every other unsettled vertex has $D \ge b \cdot 2^{i-1}$, any path through it into $y$ has weight at least $(b + 1) \cdot 2^{i-1}$. So inside $y$, every vertex with distance below $(b + 1) \cdot 2^{i-1}$ can be found from $y$ alone. At level 0 this says that the single vertex has its final distance.

**Linear time.** Thorup adds three things to make the run $O(m)$:

- The hierarchy is built from a minimum spanning tree, since the level-$i$ components of $G$ and of its minimum spanning tree are the same. On the word RAM a minimum spanning tree with integer weights takes $O(m)$ time (Fredman and Willard). Levels where a component has only one child are skipped, so the tree has $O(n)$ nodes.
- Each component keeps a bucket array over the range of its children's distances, at the scale $2^{i-1}$. The range is bounded by the total weight of the component in the minimum spanning tree divided by $2^{i-1}$, and the sum of these ranges over the hierarchy is $O(n)$.
- The least tentative distance of a child, which changes as edges are relaxed, is kept by a split-findmin structure and atomic heaps in $O(m)$ total time.

## Example

Take the undirected edges $s$-$a$ (1), $a$-$b$ (2), $s$-$c$ (5), $b$-$c$ (1), $c$-$d$ (3) and $b$-$d$ (6). The largest weight is 6, so $r = 3$. Level 1 joins the edges of weight below 2 and has the components $\{s, a\}$, $\{b, c\}$ and $\{d\}$. Level 2 adds the edges of weight 2 and 3 and has one component, $V$; level 3 is the same.

| call | what happens |
|---|---|
| VISIT($V$, 3, $\infty$) | least $D$ is $D(s) = 0$, so $b = 0$ and the bound is 4 |
| VISIT($V$, 2, 4) | $b = 0$, bound 2, child $\{s, a\}$ |
| VISIT($\{s, a\}$, 1, 2) | settles $s$ at 0, which sets $D(a) = 1$ and $D(c) = 5$; then settles $a$ at 1, which sets $D(b) = 3$ |
| VISIT($V$, 2, 4), again | least $D$ is $D(b) = 3$, so $b = 1$, bound 4, child $\{b, c\}$ |
| VISIT($\{b, c\}$, 1, 4) | settles $b$ at 3, which sets $D(c) = 4$ and $D(d) = 9$; now $D(c) = 4$ is not below 4, so it returns |
| VISIT($V$, 2, 4) returns | least $D$ is 4, not below 4 |
| VISIT($V$, 3, $\infty$), again | $b = \lfloor 4 / 4 \rfloor = 1$, bound 8 |
| VISIT($V$, 2, 8) | child $\{b, c\}$ with bound 6 settles $c$ at 4, which sets $D(d) = 7$; then child $\{d\}$ with bound 8 settles $d$ at 7 |

The distances are $(0, 1, 3, 4, 7)$ for $(s, a, b, c, d)$. Here the vertices happen to be settled in order of distance, but the algorithm never compared $D(c)$ with $D(d)$ in a heap: it only computed bucket numbers by shifts.

**Unreachable.** Add a vertex $e$ with no edges. It is in its own level-$r$ component, VISIT never enters it, and $D(e) = \infty$.

**A negative edge.** With an edge $a$-$b$ of weight $-2$, the closed walk $a, b, a$ has weight $-4$, and walks from $s$ to $b$ of any weight below every bound exist. The algorithm rejects such input.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). The main points:

1. **Settled is final.** A vertex is settled only in line L6, and then, by the bucket argument and the precondition carried down the calls, no path through an unsettled vertex can be shorter than $D(v)$. So $D(v) = \delta(s, v)$ when $v$ is settled.
2. **The precondition.** Each call VISIT($x$, $i$, hi) other than the root call starts with every unsettled vertex of $x$ at $D \ge \mathrm{hi} - 2^i$, and every unsettled vertex $z$ outside $x$ with $D(z) + 2^\ell \ge \mathrm{hi}$, where $2^\ell$ is a lower bound on any edge on a path from $z$ into $x$. Line L9 picks the lowest bucket, which makes the precondition hold for the child, and relaxations during the call keep it.
3. **Everything reachable is settled.** If an unsettled vertex is reachable, the first unsettled vertex on a shortest path to it has a finite exact label, so the loop of the root call does not stop.

Each call to a child settles at least one vertex, so there are at most $n$ calls per level, and the algorithm terminates.

## Complexity

- **Time.** $O(m + n)$ on the word RAM with Thorup's data structures: $O(m)$ for the minimum spanning tree and the hierarchy, $O(n)$ for all buckets, and $O(m)$ for the split-findmin updates on relaxations.
- **Space.** $O(m + n)$.
- **The simple version.** With a binary heap per component in place of the buckets, as in the implementation here, the time is $O(m r \log n)$, where $r$ is about $\log_2$ of the largest weight. This version is only meant to show the order of work, not the speed.

## Properties

- **Not in distance order.** Vertices of different children can be settled out of the order of their distances; only the order of buckets is respected.
- **Deterministic.** No randomness.
- **Model.** Word RAM with integer weights. In the comparison-addition model, the analogous algorithm of Pettie and Ramachandran is slightly slower than linear.
- **Undirected only.** The argument needs that an edge leaving a component also enters it with the same weight. For directed graphs the best known bound with integer weights is $O(m + n \log \log n)$, from Thorup's priority queue.

## Variants and improvements

- **Floating-point weights.** Thorup (2000) extended the algorithm to floats, using that floats compare like integers of the same bits.
- **Real weights, comparison-addition model.** Pettie and Ramachandran build a similar hierarchy from a minimum spanning tree and get $O(m \alpha(m, n) + \min(n \log n, n \log \log r))$ time, where $r$ is the ratio of the largest to the smallest weight.
- **Many sources.** After the hierarchy is built once, each further source costs $O(m)$, which gives all-pairs shortest paths in $O(nm)$ time for undirected graphs with integer weights.
- **Directed graphs.** The [breaking the sorting barrier](/breaking-sorting-barrier-sssp/) algorithm of Duan and others handles directed graphs with real weights in $O(m \log^{2/3} n)$ time by a different method.

## When to use it

Rarely in practice. The atomic heaps and the split-findmin structure have large constants, and experiments found Dijkstra with a good heap faster on real inputs. Thorup's algorithm matters as a proof that undirected SSSP with integer weights needs no sorting, and the component hierarchy is used in other algorithms on integer-weighted graphs. For small integer weights in practice, [Dial's algorithm](/dial-algorithm/) or a [radix heap](/radix-heap/) is simpler.

## Pitfalls

- **Directed graphs.** In a directed graph an edge into a component can be short while the edges out of it are long, and the bucket argument fails. The algorithm is only for undirected graphs.
- **Zero weights.** With a zero-weight edge, level 0 has components with more than one vertex, and line L6 does not apply. Contract zero-weight components first.
- **Wrong bound for the child.** The bound in line L10 must be the end of the bucket, $(b + 1) \cdot 2^{i-1}$, not $\mathrm{hi}$; with $\mathrm{hi}$ the child can settle a vertex that a path through another child would still improve.
- **Rounding.** Using $\lfloor D / 2^i \rfloor$ in place of $\lfloor D / 2^{i-1} \rfloor$ in line L9 makes the buckets too wide for the edges between children.
- **Skipping the unvisited vertices.** A vertex with $D = \infty$ must not be put in a bucket; it is not reachable yet.

## Implementations

## History

Dijkstra's algorithm with Fibonacci heaps, $O(m + n \log n)$, was the best bound for many years. On the word RAM, Fredman and Willard (1990) beat it with atomic heaps, reaching $O(m + n \log n / \log \log n)$, and later work reduced the $n$ term further, but all these methods kept the distance order and so stayed at sorting time. Thorup published the linear-time algorithm for undirected graphs in 1997 at FOCS and in the Journal of the ACM in 1999. It uses an idea that goes back to Dinitz: a vertex whose tentative distance is within the smallest edge weight of the minimum can be settled at once. Thorup applied that idea at every scale of the component hierarchy.

## References
