---
tag: 15XTPV
kind: algorithm
slug: fattest-augmenting-path
name: Fattest augmenting path
aliases:
- maximum capacity augmenting path
- widest augmenting path
area: graphs/flows-and-cuts
level: core
summary: A maximum flow method that always augments along the path with the largest bottleneck capacity, giving a polynomial bound on the number of augmentations.
solves: [max-flow-problem, min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, F: the maximum flow value, integer capacities}
  time: {worst: O(m^2 log n log F)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1972
  people: [Jack Edmonds, Richard M. Karp]
  note: Edmonds and Karp proposed the rule and its bound in the same paper as shortest augmenting paths.
prereqs: [ford-fulkerson, widest-path, dijkstra]
see_also: [edmonds-karp, capacity-scaling, dinic, flow-decomposition, augmenting-path-flow, binary-heap]
sources:
  - paper: doi:10.1145/321694.321699
    title: Jack Edmonds and Richard M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2), 248 to 264 (1972)
    locator: the section on the maximum flow problem (augmenting along a path of maximum capacity)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (Edmonds and Karp's fat pipes rule)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 7, Maximum Flows, Polynomial Algorithms (the maximum capacity augmenting path algorithm, beside capacity scaling)
---

The fattest augmenting path algorithm is the [Ford-Fulkerson method](/ford-fulkerson/) in which each [augmenting path](/augmenting-path-flow/) is one whose bottleneck, the least residual capacity on it, is as large as possible. Such a path is a [widest path](/widest-path/) in the [residual graph](/residual-graph/) and is found by a variant of [Dijkstra's algorithm](/dijkstra/). Each augmentation then carries at least a $1/m$ share of the flow still missing, so with integer capacities the number of augmentations is $O(m \log F)$, where $F$ is the maximum flow value. Edmonds and Karp gave the rule and the bound in 1972.

## In plain words

Plain augmenting paths can creep: a route with one thin pipe carries one unit, and the method may take such routes again and again. The fattest path rule always takes the route whose thinnest pipe is as thick as possible.

Why does this help? The water still missing can always be split into at most one route per pipe. So the thickest route carries at least that missing amount divided by the number of pipes. Each step thus removes a fixed share of what is left, like paying off a debt by a fixed percentage. The missing amount shrinks fast, and with whole numbers it reaches zero after a number of steps that grows only with the number of pipes and the number of digits of the answer.

## The problem

The input is a [flow network](/flow-network/) $N = (G, c, s, t)$ with a directed graph $G = (V, E)$ of $n$ vertices and $m$ edges, capacities $c(e) \ge 0$, and $s \ne t$. The output is a maximum [s-t flow](/s-t-flow/) and the source side of a minimum s-t cut.

**Assumptions.** Capacities are integers; rational capacities work after scaling by a common denominator. With irrational capacities each step still removes a $1/m$ share of the missing flow, so the value converges, but the method need not stop after finitely many steps. The graph is directed; give an undirected edge as two directed edges. Antiparallel, parallel and zero-capacity edges and self-loops are allowed, and each edge has its own pair of residual arcs. A zero-capacity edge is never in $G_f$. If $t$ is not reachable from $s$, the first search fails and the answer is the zero flow with $S$ the set of vertices reachable from $s$.

## The algorithm

```pseudo id=main
FATTEST-AUGMENTING-PATH(G, c, s, t)
L1  for each edge e do c_f(e⁺) ← c(e), c_f(e⁻) ← 0
L2  repeat
L3      for each v do b[v] ← 0, π[v] ← nil;  b[s] ← ∞;  Q ← a max-heap holding s with key ∞
L4      while Q is not empty do
L5          u ← EXTRACT-MAX(Q);  if u is done then skip it;  mark u done;  if u = t then leave the while loop
L6          for each arc x = (u, v) of u do
L7              if c_f(x) > 0 and v is not done and min(b[u], c_f(x)) > b[v] then b[v] ← min(b[u], c_f(x)), π[v] ← x, INSERT(Q, v, b[v])
L8      if b[t] = 0 then leave the repeat loop
L9      Δ ← b[t]
L10     for each arc x on the path π from s to t do c_f(x) ← c_f(x) − Δ, c_f(reverse x) ← c_f(reverse x) + Δ
L11 return f with f(e) = c_f(e⁻), and S = { v : b[v] > 0 }
```

Lines L3 to L7 are Dijkstra's algorithm with the rule "width of a path = least residual capacity on it" in place of "length = sum of weights". The heap may hold a vertex several times; only its first extraction counts (lazy deletion). When $u$ is extracted for the first time, $b[u]$ is the width of a widest path from $s$ to $u$ in $G_f$, so line L9 takes the bottleneck of a fattest augmenting path. When $t$ is not reached the search runs to the end, and the vertices with $b > 0$ are exactly those reachable from $s$ in $G_f$.

## Example

The network is the running example: $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10.

| round | fattest path | $\Delta$ | other candidates and their widths | value |
|---|---|---|---|---|
| 1 | $s\,c\,d\,t$ | 9 | $s\,a\,d\,t$ 8, $s\,a\,b\,t$ 4 | 9 |
| 2 | $s\,a\,d\,b\,t$ | 6 | $s\,a\,b\,t$ 4, $s\,a\,d\,t$ 1 | 15 |
| 3 | $s\,a\,b\,t$ | 4 | none wider | 19 |
| 4 | none: only $s$ and $c$ are reachable | | | |

The cut is $S = \{s, c\}$ with capacity $c(s, a) + c(c, d) = 19$. Three augmentations suffice here, against four for [Edmonds-Karp](/edmonds-karp/) and five for the depth-first order on the page [Ford-Fulkerson](/ford-fulkerson/). In round 1 the share bound promises at least $19/9$, and the path carries 9.

**A bad case for plain Ford-Fulkerson.** With $s a$, $s b$, $a t$, $b t$ of capacity $X$ and $a b$ of capacity 1, plain augmenting paths may alternate through $a b$ and its reverse for $2X$ rounds. The fattest path rule takes $s\,a\,t$ and $s\,b\,t$ with $X$ each and stops after 2 rounds.

**Fattest is not shortest.** On $s x_1$, $s x_2$, $x_1 y_1$, $x_1 y_2$, $x_2 y_1$, $y_1 t$, $y_2 t$, all of capacity 1, every path has width 1 and ties decide. The implementation first takes $s\,x_1\,y_1\,t$ and then needs the backward arc $(y_1, x_1)$, in $s\,x_2\,y_1\,x_1\,y_2\,t$.

**Edge cases.** With $s \to a$ 5 and $t \to a$ 5 the search does not reach $t$, the flow is 0 and $S = \{s, a\}$. A zero-capacity edge is never in a path. With the antiparallel edges $s \to a$ 3, $a \to b$ 2, $b \to a$ 1, $b \to t$ 2, $s \to b$ 1, the answer is 2 and each of $a b$ and $b a$ keeps its own flow.

## Correctness

The method is Ford-Fulkerson with one rule for choosing the path, so the proof of [Ford-Fulkerson](/ford-fulkerson/) applies once the search is shown to return an augmenting path, or none exactly when none exists. The search is Dijkstra's algorithm for the bottleneck order: when a vertex is extracted first, its key is the largest width of an s-u path in $G_f$, by the same exchange argument as for shortest paths, since extending a path never makes it wider. So line L9 gets a path of positive width $\Delta$, the augmentation keeps a feasible flow and adds $\Delta$, and if $t$ is not reached the set $S$ is the reachable set of $G_f$, whose cut capacity equals the flow value. Termination with integer capacities follows from the bound below. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/) with integer capacities.

- **One search.** Each arc is relaxed once, and each relaxation pushes at most one heap entry, so a [binary heap](/binary-heap/) costs $O(m \log n)$ per search, and the augmentation $O(n)$.
- **The share lemma.** Let $f$ be the current flow and $r = F - |f|$ the missing value. The maximum flow of the residual network has value $r$; choose one that never uses both arcs of an edge, so it lives on at most $m$ arcs. By [flow decomposition](/flow-decomposition/) it is a sum of at most $m$ paths and cycles, and the paths carry $r$ in total. So one s-t path in $G_f$ carries at least $r/m$, and its width is at least $r/m$: the fattest path has $\Delta \ge r/m$.
- **Rounds.** After $k$ rounds the missing value is at most $F(1 - 1/m)^k \le F e^{-k/m}$. With integer capacities the missing value is an integer, so it is 0 once $F e^{-k/m} < 1$, that is, once $k > m \ln F$. So there are at most $m \ln F + 1$ rounds.
- **Total.** $O(m \log F)$ rounds of $O(m \log n)$ each: $O(m^2 \log n \log F)$. With capacities at most $U$, $F \le mU$, so this is $O(m^2 \log n \log(mU))$. Space is $\Theta(n + m)$.

This bound is polynomial in the input size but not strongly polynomial: it grows with $\log F$. Compare $O(nm^2)$ for Edmonds-Karp, which does not depend on the capacities. The full argument is in the proof file below.

## Properties

- **Weakly polynomial.** The number of rounds depends on $\log F$, not on $F$.
- **Integral.** With integer capacities every $\Delta$ is an integer, so the flow is integral.
- **Certificate.** $S$ is the source side of a minimum cut.
- **Large first steps.** The early rounds carry most of the flow; after $m$ rounds at most a $1/e$ share of $F$ is missing.

## Variants and improvements

- **[Capacity scaling](/capacity-scaling/).** Instead of the fattest path, take any path of width at least $\Delta$, and halve $\Delta$ when none is left. This keeps the $O(m \log U)$ round bound with a plain search per round: $O(m^2 \log U)$ total, with no heap.
- **Bottleneck search by sorting.** Sort the residual capacities, or binary search on a threshold $\theta$ and test reachability over arcs with $c_f \ge \theta$; this finds the width in $O(m \log m)$ without a heap.
- **Monotone heaps.** Integer keys with a radix heap or a bucket structure lower the cost of each search.
- **Other rules.** [Edmonds-Karp](/edmonds-karp/) picks shortest paths and [Dinic's algorithm](/dinic/) blocking flows; both are strongly polynomial.

## When to use it

Use the fattest path rule when the capacities vary widely and a few large paths carry most of the flow, or when you already have a widest path routine. For a simple bound with less code per round, [capacity scaling](/capacity-scaling/) does as well. For general use, [Dinic's algorithm](/dinic/) is faster and strongly polynomial, and it also works for real capacities.

## Pitfalls

- **Irrational or real capacities.** The round bound needs integers. With irrational capacities the value converges but the method can run forever; floats terminate in practice, because they are rationals with a common power-of-two denominator, but with no useful bound.
- **Widest path in $G$ instead of $G_f$.** The search must run on residual capacities and must include backward arcs.
- **Sum instead of min.** Line L7 must use $\min(b[u], c_f(x))$; the order of the heap is by largest key first.
- **Reading the cut after an early stop.** The search leaves its loop as soon as $t$ is extracted; only a search that did not reach $t$ gives the reachable set.
- **Merging antiparallel edges wrongly.** One residual entry per ordered pair must add the forward residual of $(u, v)$ and the backward residual of $(v, u)$. Keep one arc pair per edge, as in line L1.

## Implementations

The Python version takes the vertex count, a list of edges $(u, v, c)$ and $s, t$, and returns the value, the flow on each input edge and the sorted source side of a minimum cut. It uses `heapq` with negated keys and lazy deletion. Capacities should be `int` or `Fraction`; `float` is accepted. An optional callback reports each path and its bottleneck; the tests use it to check that each path is a widest one and that the number of rounds is at most $m \ln F + 1$.

## History

Jack Edmonds and Richard Karp proposed the fattest path rule in their 1972 paper in the Journal of the ACM, together with shortest augmenting paths, and proved the bound on the number of augmentations through the share argument. The same paper introduced scaling for minimum-cost flows, which became [capacity scaling](/capacity-scaling/) for maximum flows.

## References
