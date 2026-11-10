---
tag: CXP7SG
kind: algorithm
slug: delta-stepping
name: Delta-stepping
aliases:
- Δ-stepping
- parallel Dijkstra with buckets
area: parallel/parallel-graph-algorithms
level: advanced
summary: Parallel SSSP that groups tentative distances into buckets of width Δ and relaxes each bucket in parallel.
solves: [single-source-shortest-paths]
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of arcs, k: the number of nonempty buckets that are processed, l: the most arcs on a piece of weight below Δ of a shortest path with fewest arcs}
  time: {worst: O((n + m)(l + 1) + k log n)}
  depth: {worst: O(k (l + 1) log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [single-source-shortest-paths, edge-relaxation, dijkstra, bellman-ford, frontier-based-processing, work-span-model]
see_also: [dial-algorithm, bucket-queue, parallel-bfs, hopset, thorup-undirected-sssp, relaxed-priority-queue, multiqueue, radix-heap]
sources:
  - paper: doi:10.1016/S0196-6774(03)00076-2
    title: Ulrich Meyer and Peter Sanders, Δ-stepping, a parallelizable shortest path algorithm, Journal of Algorithms 49(1), 114 to 152 (2003)
    locator: the definition with light and heavy edges, the analysis in terms of Δ-paths, and the average-case bounds for random edge weights; section numbers and DOI to be checked
  - paper: "Ulrich Meyer and Peter Sanders, Δ-stepping, a parallel single source shortest path algorithm, ESA 1998, LNCS 1461"
    title: Δ-stepping, a parallel single source shortest path algorithm
    locator: the conference version of the algorithm; pages to be checked
  - paper: "Kamesh Madduri, David A. Bader, Jonathan W. Berry and Joseph R. Crobak, An experimental study of a parallel shortest path algorithm for solving large-scale graph instances, ALENEX 2007"
    title: An experimental study of a parallel shortest path algorithm for solving large-scale graph instances
    locator: the shared-memory implementation of Δ-stepping and the choice of Δ in practice; pages to be checked
  - paper: doi:10.1145/3087556.3087580
    title: Laxman Dhulipala, Guy E. Blelloch and Julian Shun, Julienne, a framework for parallel graph algorithms using work-efficient bucketing, SPAA 2017
    locator: the bucketing interface and the work-efficient Δ-stepping built on it; DOI to be checked
---

Delta-stepping computes single-source shortest paths with nonnegative weights in parallel. It keeps the tentative distances in buckets of width $\Delta$, and it takes the smallest nonempty bucket as the next frontier. All vertices of that bucket relax their light arcs, those of weight at most $\Delta$, at the same time, and this repeats in phases until the bucket stays empty. Then the heavy arcs of all vertices that left the bucket are relaxed once. A small $\Delta$ gives the order of [Dijkstra's algorithm](/dijkstra/) with little parallel work per step; a large $\Delta$ gives the many rounds of [Bellman-Ford](/bellman-ford/) with repeated work. A good $\Delta$ is between the two.

Notation on this page: $G = (V, A)$ is a directed graph with $n$ vertices, $m$ arcs and weights $w \ge 0$; $s$ is the source; $d(v)$ is the true distance and $dist(v)$ the tentative one. Bucket $B[i]$ holds the vertices with $dist(v) \in [i\Delta, (i + 1)\Delta)$. For each $v$, take a shortest path from $s$ with the fewest arcs; $l$ is the most arcs on a piece of such a path whose weight is below $\Delta$, and $k$ is the number of nonempty buckets that are processed. $W$ is the work and $S$ the span, in the [work-span model](/work-span-model/) with a minimum concurrent write. The bounds in the front matter are worst case in terms of $k$ and $l$ and are proved here. The bounds for random weights are average case and are cited from Meyer and Sanders (2003).

## In plain words

Think of a fire that spreads along roads of different lengths, and of a clock that moves in steps of fixed size. In each step, every town that the fire reaches inside the current time window starts to burn, and it sends fire along its short roads at once. Fire along a short road can arrive in the same window, so the step repeats until the window is quiet.

Then all the towns that burned in this window send fire along their long roads. Long roads always end in a later window, so they need to be sent only once. The clock then jumps to the next window in which something burns.

Small windows keep the order exact but give few towns per step. Big windows give many towns per step, but some towns burn again because a faster route arrives later.

## The problem

The input is a directed graph with nonnegative arc weights and a source $s$. The output is the distance $d(v)$ from $s$ to every vertex, or $\infty$ if $s$ does not reach $v$. This is the [single-source shortest paths](/single-source-shortest-paths/) problem. Dijkstra's algorithm solves it in $O(m + n \log n)$ time, but it settles one vertex at a time, so its span is $\Omega(n)$. The goal here is to handle many vertices per step without too much extra work.

## The algorithm

Relaxing $v$ with the value $x$ means: if $x < dist(v)$, set $dist(v) \leftarrow x$ and move $v$ to the bucket $\lfloor x/\Delta \rfloor$. Light arcs have $w \le \Delta$ and heavy arcs $w > \Delta$.

```pseudo id=main
DELTA-STEPPING(G, s, Δ)
L1  dist(v) ← ∞ for all v; relax s with 0
L2  while some bucket is not empty do
L3      i ← the smallest index of a nonempty bucket
L4      R ← ∅
L5      while B[i] is not empty do      ▷ one phase
L6          Req ← {(u, dist(v) + w(v, u)) : v in B[i], (v, u) light}
L7          R ← R ∪ B[i]; B[i] ← ∅
L8          for all (u, x) in Req in parallel do relax u with x      ▷ minimum write per target
L9      Req ← {(u, dist(v) + w(v, u)) : v in R, (v, u) heavy}
L10     for all (u, x) in Req in parallel do relax u with x
L11 return dist
```

Line L6 reads the light arcs of the whole bucket before line L7 empties it, so a vertex whose distance goes down in line L8 comes back to $B[i]$ for the next phase. The heavy arcs wait for line L9, since each of them leads to a later bucket.

## Example

The arcs are $0 \to 1$ (1), $0 \to 2$ (4), $1 \to 2$ (1), $1 \to 3$ (5), $2 \to 3$ (1), $3 \to 4$ (3) and $2 \to 4$ (7), with $s = 0$ and $\Delta = 2$. The light arcs are $0 \to 1$, $1 \to 2$ and $2 \to 3$.

| bucket | phase | $B[i]$ (L6) | light relaxations (L8) | heavy relaxations (L9, L10) |
|---|---|---|---|---|
| 0 | 1 | $\{0\}$ | $dist(1) = 1$, into $B[0]$ | |
| 0 | 2 | $\{1\}$ | $dist(2) = 2$, into $B[1]$ | from $R = \{0, 1\}$: $dist(3) = 6$, into $B[3]$; $0 \to 2$ gives 4, no change |
| 1 | 3 | $\{2\}$ | $dist(3) = 3$, from $B[3]$ into $B[1]$ | |
| 1 | 4 | $\{3\}$ | none | from $R = \{2, 3\}$: $dist(4) = \min(9, 6) = 6$, into $B[3]$ |
| 3 | 5 | $\{4\}$ | none | none |

The result is $dist = (0, 1, 2, 3, 6)$ after $k = 3$ buckets and 5 phases. Bucket 2 is never selected, since no distance falls in $[4, 6)$. Vertex 3 first goes to bucket 3 through a heavy arc, and then moves down to bucket 1 when the shorter path through vertex 2 is found; it is handled only once, in bucket 1.

## Correctness

The proof file proves, in full:

1. a vertex in the current bucket $i$ has its true distance in $[i\Delta, (i + 1)\Delta)$, so it is handled only in the bucket of its final distance, and heavy arcs always lead to a later bucket;
2. inside one bucket, the light part of a shortest path is followed one arc per phase, so every vertex of the bucket has its final distance after at most $l + 1$ phases, and it is handled at most $l + 1$ times;
3. when a bucket is selected, every vertex with a smaller distance is final and has relaxed all its arcs, so at the end $dist = d$, with $\infty$ for the vertices that $s$ does not reach.

## Complexity

**Proved bounds.** Each vertex is handled at most $l + 1$ times, each time with its light arcs, and its heavy arcs are read once. A phase costs $O(\log n)$ span for the minimum writes and the pack of the next bucket, and there are at most $l + 1$ phases per bucket. So

$$W = O((n + m)(l + 1) + k \log n), \qquad S = O(k (l + 1) \log n).$$

Here $k \le \min(n, \lfloor L/\Delta \rfloor + 1)$, where $L$ is the largest finite distance. With $\Delta$ below the smallest arc weight, all arcs are heavy, $l = 0$, and there is one phase per bucket, as in [Dial's algorithm](/dial-algorithm/). With $\Delta = \infty$, all arcs are light and there is one bucket, and the phases are the rounds of a frontier-based Bellman-Ford, at most the largest number of arcs on a shortest path, plus 1. The tests check both cases.

**Random weights (cited).** Meyer and Sanders (2003) show that for weights drawn independently and uniformly from $[0, 1]$ and $\Delta = \Theta(1/d)$, where $d$ is the largest degree, the expected work is $O(n + m + d L)$ and the expected span is $O(d L \log n + \log^2 n)$. For many random graph classes, $d L$ is polylogarithmic, so the span is polylogarithmic and the work is linear.

**Measured.** On random digraphs with $m = 4n$ arcs, weights uniform in $[0, 1)$ and $\Delta = 1/4$, the tests measure, over 5 runs each, for $n = 64$, 256 and 1,024:

| $n$ | mean buckets $k$ | mean phases | phases over $\log_2 n$ | work over $n + m$ |
|---|---|---|---|---|
| 64 | 8.6 | 16.8 | 2.8 | 1.35 |
| 256 | 11.0 | 24.4 | 3.1 | 1.27 |
| 1,024 | 14.6 | 35.6 | 3.6 | 1.21 |

The tests assert a mean below $c \log_2 n$ phases with $c = 5$, and a mean work below $2(n + m)$.

## Properties

- **Deterministic.** The result and the cost depend only on the graph, $s$ and $\Delta$.
- **Label-correcting inside a bucket.** A vertex can be handled more than once in its bucket, but never in another bucket, so the repeated work is limited by $l$.
- **One parameter.** $\Delta$ trades the number of buckets, $L/\Delta$, against the repeated work inside each bucket.
- **Nonnegative weights only.** The bucket order needs $d$ to grow along every path.

## Variants and improvements

- **Choosing $\Delta$.** Meyer and Sanders suggest $\Delta = \Theta(1/d)$ for random weights in $[0, 1]$. In practice, $\Delta$ is tuned per graph class; Madduri, Bader, Berry and Crobak (2007) report results for several choices.
- **Bucket structures.** Only a window of buckets is needed at a time, since while bucket $i$ is current, every finite tentative distance is below $(i + 1)\Delta + w_{\max}$, where $w_{\max}$ is the largest arc weight. Dhulipala, Blelloch and Shun (2017) give a work-efficient bucketing structure and build Δ-stepping on it.
- **Shortcut arcs.** Adding arcs for the light paths of weight below $\Delta$, so that one phase is enough per bucket, gives the variant with preprocessing in the paper by Meyer and Sanders. [Hopsets](/hopset/) follow the same idea in a general form.
- **Relaxed priority queues.** Concurrent queues such as the [MultiQueue](/multiqueue/) take the next vertices in an order that is close to the distance order, which gives an asynchronous form of the same trade-off.

## When to use it

Use it for single-source shortest paths with nonnegative weights on a shared-memory machine or a GPU, when the graph is large and the shortest paths have many arcs, such as road networks with tuned $\Delta$, or random and social graphs. For unweighted graphs, [parallel BFS](/parallel-bfs/) is simpler. For graphs with few, very long shortest paths, the number of buckets is large and the span stays high, whatever $\Delta$ is.

## Pitfalls

- **Relaxing heavy arcs too early.** Heavy arcs can be relaxed after the bucket is empty, from all vertices that left it. Relaxing them in every phase gives the same result but repeats work.
- **Forgetting to move a vertex.** When $dist(v)$ goes down, $v$ must leave its old bucket, or it is handled from a stale bucket with a later value.
- **Zero weights.** Arcs of weight 0 are light, and a long chain of them makes $l$ large; the result is still correct.
- **Floating point.** The proof assumes that $\lfloor x/\Delta \rfloor$ is exact. With rounding, a vertex can land one bucket off. Use integer weights and an integer $\Delta$ where you can, and compute the index in one place only.
- **Concurrent writes.** Two requests for the same target in one phase need a minimum write, or a sort or group step, not a plain write.

## Implementations

## History

Meyer and Sanders presented Δ-stepping at ESA 1998 and published the full version with the average-case analysis in the Journal of Algorithms in 2003. Madduri, Bader, Berry and Crobak (2007) studied it on large graphs on shared-memory machines. Dhulipala, Blelloch and Shun (2017) included a work-efficient version in the Julienne framework.

## References
