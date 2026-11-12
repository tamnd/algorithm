---
tag: 5KYFGE
kind: algorithm
slug: slink
name: SLINK
aliases:
- Sibson's algorithm
area: machine-learning/clustering
level: advanced
summary: "Sibson's single linkage algorithm: adds one point at a time to a pointer form (pi, lambda) of the tree, in O(n^2) time and O(n) memory."
solves: [hierarchical-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {worst: "Θ(n^2)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1973
  people: [Robin Sibson]
  note: Sibson (1973) introduced the pointer representation and SLINK, and proved that its time and memory are optimal for the single link method.
prereqs: [single-linkage-clustering, dendrogram]
see_also: [prim, minimum-spanning-tree, complete-linkage-clustering, nearest-neighbor-chain, ultrametric, agglomerative-clustering, hdbscan]
sources:
  - paper: doi:10.1093/comjnl/16.1.30
    title: "R. Sibson, SLINK: an optimally efficient algorithm for the single-link cluster method, The Computer Journal 16(1) (1973), 30-34"
    locator: the pointer representation (pi, lambda), the update when a point is added, and the O(n^2) time and O(n) memory bounds
  - paper: doi:10.1093/comjnl/20.4.364
    title: "D. Defays, An efficient algorithm for a complete link method, The Computer Journal 20(4) (1977), 364-366"
    locator: CLINK, the same pointer scheme for a complete link rule
  - paper: doi:10.1093/comjnl/26.4.354
    title: "Fionn Murtagh, A survey of recent advances in hierarchical clustering algorithms, The Computer Journal 26(4) (1983), 354-359"
    locator: SLINK among the O(n^2) algorithms for hierarchical clustering
  - url: https://arxiv.org/abs/1109.2378
    title: "Daniel Müllner, Modern hierarchical, agglomerative clustering algorithms, arXiv:1109.2378 (2011)"
    locator: the section on single linkage by a minimum spanning tree, and the pointer representation
---

SLINK is Sibson's algorithm for [single-linkage clustering](/single-linkage-clustering/). It adds the points one at a time, and after each point it holds the single linkage tree of the points so far in a *pointer representation*: two arrays $\pi$ and $\lambda$, where $\lambda(i)$ is the height at which point $i$ first joins a point with a larger index, and $\pi(i)$ is the largest index in the cluster that it joins. When point $m$ arrives, one pass over the earlier points with one scratch array $M$ updates both arrays. Each pair of points is read once, so the algorithm takes $\Theta(n^2)$ time and $\Theta(n)$ memory, which is optimal for a general dissimilarity: it needs no matrix. A sort of the pointer representation by $\lambda$ gives the merges of the [dendrogram](/dendrogram/).

## In plain words

Number the points. For each point, keep two notes. The first note is a height: how far up the tree the point must go before it shares a group with a point that has a higher number. The second note is the highest number in that group. Every point except the last one points up to a higher point, so the notes form a tree. These two notes are enough to rebuild the whole single linkage tree.

When a new point arrives, it has the highest number. Measure its distance to each old point. Then walk over the old points in order, and fix their notes: a point whose first meeting with a higher point now happens lower, at the new point, gets new notes. One small extra list carries the needed values up the tree. Nothing else is stored.

## The problem

The input is $n$ points and a function $d(i, j)$ that returns their dissimilarity. The output is the single linkage hierarchy, in the pointer representation. For the points $1, \ldots, N$ with the single linkage cophenetic distance $u$ (the minimax path distance), the representation is

$$\lambda(i) = \min_{k > i} u(i, k), \qquad \pi(i) = \max\{k : u(i, k) \le \lambda(i)\} \quad \text{for } i < N,$$

and $\pi(N) = N$, $\lambda(N) = \infty$. Sibson showed that $(\pi, \lambda)$ fixes the hierarchy. To list the merges, join point $i$ to the cluster of $\pi(i)$ at height $\lambda(i)$, in increasing order of $\lambda$.

## The algorithm

```pseudo id=main
SLINK(n, d)                           ▷ the points are 1, …, n
L1  for m ← 1 to n do
L2      π(m) ← m, λ(m) ← ∞
L3      M(j) ← d(j, m) for j = 1, …, m − 1
L4      for j ← 1 to m − 1 do
L5          if λ(j) ≥ M(j) then
L6              M(π(j)) ← min(M(π(j)), λ(j))
L7              λ(j) ← M(j), π(j) ← m
L8          else M(π(j)) ← min(M(π(j)), M(j))
L9      for j ← 1 to m − 1 do
L10         if λ(j) ≥ λ(π(j)) then π(j) ← m
```

The loop of line L4 visits the points in increasing order. Each point $j$ passes a value up to its parent $\pi(j)$, always the larger of $\lambda(j)$ and $M(j)$. When the loop reaches a point, its $M$ value is the cheapest way to reach the new point $m$ from it through the points below it in the pointer tree. Line L5 then tests whether $j$ now meets a higher point lower than before. The loop of line L9 repairs the pointers of the points where the test of line L5 met a tie.

## Example

Take the points $1, \ldots, 6$ at $0, 2, 3, 7, 13, 21$ on a line, with $d(i, j)$ the distance. The table shows $M$ after line L3, and $\pi$ and $\lambda$ after each point $m$.

| $m$ | $M$ at line L3 | $\pi$ | $\lambda$ |
|---|---|---|---|
| 1 | | 1 | $\infty$ |
| 2 | 2 | 2, 2 | 2, $\infty$ |
| 3 | 3, 1 | 3, 3, 3 | 2, 1, $\infty$ |
| 4 | 7, 5, 4 | 3, 3, 4, 4 | 2, 1, 4, $\infty$ |
| 5 | 13, 11, 10, 6 | 3, 3, 4, 5, 5 | 2, 1, 4, 6, $\infty$ |
| 6 | 21, 19, 18, 14, 8 | 3, 3, 4, 5, 6, 6 | 2, 1, 4, 6, 8, $\infty$ |

At $m = 3$, point 1 has $\lambda(1) = 2 < M(1) = 3$, so line L8 passes $3$ up to its parent 2, where $M(2) = \min(1, 3) = 1$. Point 2 has $\lambda(2) = \infty \ge 1$, so line L7 sets $\lambda(2) = 1$ and $\pi(2) = 3$. Then line L10 sees $\lambda(1) = 2 \ge \lambda(\pi(1)) = \lambda(2) = 1$ and moves the pointer of 1 to 3: point 1 now first meets a higher point in the cluster $\{1, 2, 3\}$, whose largest index is 3.

The final arrays say: 2 joins 3 at height 1, 1 joins the cluster of 3 at height 2, 3 joins 4 at 4, 4 joins 5 at 6, and 5 joins 6 at 8. These are the merges of single linkage on these points.

## Correctness

Adding point $m$ changes the minimax distances in a simple way. Let $u$ be the old distance on $1, \ldots, m - 1$ and $\mu(i) = \min_j \max(u(i, j), d(j, m))$ the new distance from $i$ to $m$. Then the new representation is $\lambda'(i) = \min(\lambda(i), \mu(i))$, with $\pi'(i) = m$ if $\mu(i) \le \lambda(i)$ and $\pi'(i) = \pi(i)$ if not. The loop of line L4 does not compute $\mu$ itself. It computes the minimum of $\max(d(j', m), u(j', j))$ over the points $j'$ below $j$ in the pointer tree, and those points are exactly the points with $u(j', j) < \lambda(j)$. This value equals $\mu(j)$ whenever $\mu(j) < \lambda(j)$, and it exceeds $\lambda(j)$ when $\mu(j) > \lambda(j)$. So line L5 decides right, except for a tie $\mu(j) = \lambda(j)$. Line L10 detects exactly the ties. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time.** Step $m$ does $O(m)$ work in each of its three loops, so the total is $\Theta(n^2)$. The function $d$ is called once for each pair, $n(n - 1)/2$ times.
- **Memory.** Three arrays of length $n$: $\pi$, $\lambda$ and $M$. No dissimilarity matrix is stored.
- **Merges.** The conversion to a list of merges sorts $\lambda$ and runs a [disjoint-set](/disjoint-set/) structure, in $O(n \log n)$ time.
- **Optimality.** Each exact single linkage algorithm on a general dissimilarity must read all $n(n - 1)/2$ values in the worst case, so $\Theta(n^2)$ time is optimal, and $\Theta(n)$ memory is needed for the output.

## Properties

- **Incremental.** After step $m$, the arrays hold the single linkage tree of the first $m$ points. New points can arrive later at a cost of $O(m)$ each.
- **One read per pair.** Line L3 is the only place that reads the data, so the dissimilarity can be computed on the fly from the points.
- **Exact.** The output is the single linkage hierarchy. With ties, its cophenetic distance is still the minimax path distance, and the pointer representation is unique.
- **Pointer tree.** The pointers $i \to \pi(i)$ form a tree rooted at $n$, and $\lambda$ strictly increases along each pointer path.

## Variants and improvements

- **CLINK.** Defays (1977) used the same scheme for a complete link rule, in $O(n^2)$ time and $O(n)$ memory. CLINK does not give the exact [complete linkage](/complete-linkage-clustering/) tree in general, and its result depends on the order of the points.
- **[Prim's algorithm](/prim/) on the dense graph.** It also gives single linkage in $\Theta(n^2)$ time and $\Theta(n)$ memory, through a [minimum spanning tree](/minimum-spanning-tree/), and it is often faster in practice. Müllner (2011) recommends it.
- **[Nearest-neighbor chain](/nearest-neighbor-chain/).** Exact for single linkage too, but it needs the $\Theta(n^2)$ matrix.
- **Parallel and external versions.** The per-point update is a single scan, which suits data that is read from disk in order.

## When to use it

Use SLINK for single linkage when the dissimilarity matrix does not fit in memory, or when points arrive one at a time and the tree must be ready after each one. For a one-time run on all points, Prim's algorithm has the same bounds and is simpler to check. For a different linkage, SLINK does not apply.

## Pitfalls

- **The second loop.** Code without the loop of line L9 is wrong on ties: a point whose new meeting height equals its old one keeps a stale pointer.
- **The order of the first loop.** Line L4 must visit the points in increasing order, so that each $M(j)$ has all values from below before $j$ is tested.
- **The old pointer.** Line L6 must use $\pi(j)$ before line L7 changes it.
- **The pointer form is not a merge list.** Sort the points by $\lambda$ and use a disjoint-set structure to get the merges. Do not read $\pi$ as a list of merges.
- **Do not use CLINK as exact complete linkage.** Its tree can differ from the tree of the greedy rule.

## Implementations

## History

Sibson (1973) introduced the pointer representation of a hierarchy, and with it the SLINK algorithm. He proved that its time and memory are optimal up to constant factors for the single link method. Defays (1977) adapted the method to a complete link rule as CLINK. Murtagh (1983) placed SLINK among the $O(n^2)$ algorithms for hierarchical clustering.

## References
