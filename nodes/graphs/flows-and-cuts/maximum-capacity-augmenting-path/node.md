---
tag: QFY05A
kind: algorithm
slug: maximum-capacity-augmenting-path
name: Maximum-capacity augmenting path algorithm
aliases:
- Maximum-capacity augmenting path
area: graphs/flows-and-cuts
level: core
summary: Augmenting path method for maximum flow that always chooses the path with the largest bottleneck capacity.
solves: [max-flow-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, U: the largest capacity}
  time: {worst: O(m^2 log n log(n U))}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [ford-fulkerson, residual-graph, widest-path, dijkstra]
see_also: [fattest-augmenting-path, edmonds-karp, capacity-scaling, dinic, flow-decomposition, max-flow-problem, binary-heap]
sources:
  - paper: doi:10.1145/321694.321699
    title: Jack Edmonds and Richard M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2), 248 to 264 (1972)
    locator: the section on the maximum flow problem (augmenting along a path of maximum capacity, and the bound on the number of augmentations)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (Edmonds and Karp's fat pipes)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 7, Maximum Flows, Polynomial Algorithms (the maximum capacity augmenting path rule and the capacity scaling algorithm)
---

The maximum-capacity augmenting path algorithm is the [Ford-Fulkerson method](/ford-fulkerson/) with one rule: in each round it augments along an $s$-$t$ path of the [residual graph](/residual-graph/) whose smallest residual capacity is as large as possible. Such a path is a [widest path](/widest-path/), found by a version of [Dijkstra's algorithm](/dijkstra/) in $O(m \log n)$ time. With integer capacities each round takes at least a $1/m$ share of the flow that is still missing, so there are at most $m \ln f^{*} + 1$ rounds, where $f^{*}$ is the maximum flow value. Edmonds and Karp proposed it in 1972, together with the shortest-path rule of [Edmonds-Karp](/edmonds-karp/). The page [fattest augmenting path](/fattest-augmenting-path/) describes the same rule.

## In plain words

Water flows from a source to a drain through pipes of different sizes. Each round, you pick one route and send as much water along it as its thinnest pipe allows. Then you account for what is left in each pipe, and repeat until no route has room.

The rule here is greedy: always pick the route whose thinnest pipe is the widest. A wide route moves a lot of water at once, so few rounds are needed. One can show that the best route always carries at least a fixed share of the water still missing, so the missing amount shrinks by a constant factor every few rounds, as a debt does under a fixed rate of repayment.

## The problem

The input is a [flow network](/flow-network/): a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, integer capacities $c(e) \ge 0$, a source $s$ and a sink $t \ne s$. Parallel edges and antiparallel edges $(u, v)$, $(v, u)$ are allowed and each keeps its own forward and backward residual edge; they are never merged. An edge of capacity 0 never carries flow. Self-loops carry no flow. The output is a [maximum flow](/max-flow-problem/) $f$ and, as a by-product, the source side of a [minimum cut](/min-cut-problem/). If $t$ is not reachable from $s$, the answer is the zero flow.

## The algorithm

```pseudo id=main
MAX-CAPACITY-AUGMENT(G, c, s, t)
L1  f ← 0
L2  loop
L3      (P, δ) ← WIDEST-PATH(G_f, s, t)
L4      if P is empty then break
L5      augment f by δ along P
L6  return f, and the set S of vertices that s reaches in G_f

WIDEST-PATH(G_f, s, t)
L7  b[v] ← 0 and via[v] ← nil for each v; b[s] ← ∞
L8  Q ← a max-priority queue holding s with key ∞; while Q is not empty do
L9      u ← EXTRACT-MAX(Q)
L10     for each residual edge r = (u, v) of G_f do
L11         if v ≠ s and min(b[u], c_f(r)) > b[v] then
L12             b[v] ← min(b[u], c_f(r)); via[v] ← r; insert v into Q with key b[v]
L13 if b[t] = 0 then return (empty, 0) else return (the path to t along via, b[t])
```

Here $b[v]$ is the largest bottleneck of an $s$-$v$ path found so far. Line L5 lowers the residual capacity of each edge of $P$ by $\delta$ and raises its reverse by $\delta$: on a forward edge this adds flow, on a backward edge it cancels flow. Line L11 skips residual edges of capacity 0, since $\min(b[u], 0) = 0$ is never larger than $b[v] \ge 0$. A vertex that comes out of $Q$ a second time is skipped (lazy deletion).

## Example

The network has the edges $s \to a$ (10), $s \to b$ (10), $a \to b$ (2), $a \to c$ (4), $a \to d$ (8), $b \to d$ (9), $d \to c$ (6), $c \to t$ (10), $d \to t$ (10).

| round | widest path | $\delta$ | value |
|---|---|---|---|
| 1 | $s, b, d, t$ | 9 | 9 |
| 2 | $s, a, d, c, t$ | 6 | 15 |
| 3 | $s, a, c, t$ | 4 | 19 |
| 4 | none | | 19 |

In round 2, $d \to t$ has only 1 left, so the widest route from $d$ goes through $c$; the path $s, a, c, t$ has bottleneck 4 and loses. After round 3, $s \to a$ and $b \to d$ are full, $s \to b$ has 1 left, and $s$ reaches only $\{s, b\}$. That set is the minimum cut, of capacity $10 + 9 = 19$. [Edmonds-Karp](/edmonds-karp/) on the same network also uses three augmentations, but its first path has bottleneck at most 8.

Edge cases. With an extra edge $s \to t$ of capacity 0, line L11 never uses it, and the answer is still 19. With only the edges $s \to a$ (3) and $b \to t$ (3), round 1 finds $b[t] = 0$ and the answer is 0 with $S = \{s, a\}$.

## Correctness

At the end, $G_f$ has no $s$-$t$ path with positive capacity, so $f$ is maximum by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), and $S$ is a minimum cut. WIDEST-PATH is correct by the same exchange argument as Dijkstra: when $u$ is extracted, $b[u]$ is the largest bottleneck of any $s$-$u$ path, because every other path leaves the extracted set through an edge whose bottleneck is at most the current maximum key. Termination with integer capacities: each $\delta$ is a positive integer, so the value grows by at least 1 per round. The proof file below gives the full proof and the bound on the number of rounds.

## Complexity

The model is the [word RAM](/word-ram/) with capacities that fit in a word.

- **Rounds.** Let $r = f^{*} - |f|$ be the missing flow. A maximum flow of $G_f$ has value $r$, and it can be split into at most $m$ paths and cycles ([flow decomposition](/flow-decomposition/)), so some path carries at least $r / m$. Hence $\delta \ge r/m$, and after the round the missing flow is at most $r (1 - 1/m)$. After $k$ rounds it is at most $f^{*} e^{-k/m}$, which is below 1, hence 0, once $k > m \ln f^{*}$. So there are at most $m \ln f^{*} + 1 \le m \ln(nU) + 1$ rounds.
- **One round.** WIDEST-PATH with a [binary heap](/binary-heap/) takes $O(m \log n)$; the augmentation takes $O(n)$.
- **Total.** $O(m \log f^{*} \cdot m \log n) = O(m^2 \log n \log(nU))$ time and $\Theta(n + m)$ space.

## Properties

- **Weakly polynomial.** The bound depends on $\log U$. It is polynomial in the input size, unlike plain Ford-Fulkerson, but not strongly polynomial.
- **Greedy per round.** Each round takes the largest single augmentation, but the sum of the rounds is not maximized greedily: the order of the paths still matters for the count.
- **Integral.** With integer capacities every $\delta$ is an integer, so the result is an integral flow, as in the [integrality theorem](/integrality-theorem/).

## Variants and improvements

- **[Capacity scaling](/capacity-scaling/).** Instead of the widest path, take any path of bottleneck at least $\Delta$ with a [breadth-first search](/breadth-first-search/), and halve $\Delta$ when none is left. This gives $O(m^2 \log U)$ time with simpler searches and keeps the same idea.
- **Bucket queues.** With small integer capacities, a [bucket queue](/bucket-queue/) replaces the heap in WIDEST-PATH.
- **Shortest paths instead.** [Edmonds-Karp](/edmonds-karp/) takes a shortest path and gets the strongly polynomial bound $O(nm^2)$; [Dinic](/dinic/) takes all shortest paths at once.
- **Minimum-cost flow.** The same "largest improvement" idea appears in [cycle canceling](/cycle-canceling/) that cancels the cycle of largest total improvement.

## When to use it

Use it when capacities are integers of moderate size and the network is sparse, or when a simple augmenting-path code with a good bound is wanted. For a strongly polynomial bound use Edmonds-Karp or Dinic, and for large networks use [push-relabel](/push-relabel/) or Dinic. Capacity scaling has the same flavor and a better bound.

## Pitfalls

- **Taking the shortest path.** The widest path is found with (max, min) in Dijkstra, not (min, +). Mixing them gives a different algorithm.
- **Ignoring backward edges.** The widest path is taken in $G_f$, with backward edges of capacity $f(e)$; the example needs no backward edge, but in general the algorithm is wrong without them.
- **Merging antiparallel edges.** If $u \to v$ and $v \to u$ are stored as one pair of residual edges, the flow on each can no longer be read back. The code keeps residual edges $2i$ and $2i + 1$ for edge $i$.
- **Real capacities.** The round bound uses integers; the code does not promise termination for irrational capacities.
- **Using $b[s] = 0$.** The source must start with key $\infty$; otherwise no path ever gets a positive bottleneck.

## Implementations

## History

Edmonds and Karp proposed both the maximum-capacity rule and the shortest-path rule in their 1972 paper, and proved the bound on the number of augmentations for the maximum-capacity rule by the decomposition argument above. The capacity scaling variant was made explicit later; Ahuja, Magnanti and Orlin present it next to the maximum-capacity rule.

## References
