---
tag: 2SESDD
kind: algorithm
slug: edmonds-karp
name: Edmonds-Karp algorithm
aliases:
- shortest augmenting path algorithm
area: graphs/flows-and-cuts
level: core
summary: Ford-Fulkerson with BFS shortest augmenting paths, running in O(VE^2).
solves: [max-flow-problem, min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m^2)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1972
  people: [Jack Edmonds, Richard M. Karp, Yefim Dinitz]
  note: Dinitz published shortest augmenting paths in 1970 as part of his blocking flow algorithm; Edmonds and Karp published the O(nm^2) bound in 1972.
prereqs: [ford-fulkerson, breadth-first-search, residual-graph]
see_also: [dinic, level-graph, fattest-augmenting-path, capacity-scaling, push-relabel, max-flow-min-cut-theorem, bipartite-matching]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.2, The Ford-Fulkerson method, subsection The Edmonds-Karp algorithm (the monotone distance lemma, the critical edge argument and the O(VE^2) bound)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (Edmonds and Karp's shortest augmenting paths)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 7, Maximum Flows, Polynomial Algorithms (the shortest augmenting path algorithm with distance labels)
  - paper: doi:10.1145/321694.321699
    title: Jack Edmonds and Richard M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2), 248 to 264 (1972)
    locator: the section on the maximum flow problem (shortest augmenting paths and the bound on their number)
---

The Edmonds-Karp algorithm is the [Ford-Fulkerson method](/ford-fulkerson/) in which each [augmenting path](/augmenting-path-flow/) is a shortest one, in number of edges, found by [breadth-first search](/breadth-first-search/) in the [residual graph](/residual-graph/). This one rule makes the number of augmentations at most $nm/2$ whatever the capacities are, so the algorithm runs in $O(nm^2)$ time for real capacities and never loops forever. It solves the [maximum flow problem](/max-flow-problem/) and returns a [minimum cut](/min-cut-problem/) with it, and it is the usual first polynomial algorithm taught for flows.

## In plain words

The plain augmenting path method can make bad choices: it can take a long, winding route that fixes almost nothing, again and again. Edmonds-Karp always takes a route with the fewest pipes. A breadth-first search from the source finds one, because it visits places in order of how many steps away they are.

Why does this help? Pushing flow along a shortest route fills at least one pipe on it. Filling pipes never makes any place closer to the source. So the distance to the drain can only grow, and it can grow at most to the number of places. While the distance stays the same, each push fills a pipe that cannot be used again at that distance. So only a limited number of pushes can happen at each distance, and the total is bounded by the size of the network, not by the capacities.

## The problem

The input is a [flow network](/flow-network/) $N = (G, c, s, t)$ with a directed graph $G = (V, E)$ of $n$ vertices and $m$ edges, real capacities $c(e) \ge 0$, and $s \ne t$. The output is a maximum [s-t flow](/s-t-flow/) and the source side of a minimum s-t cut.

**Assumptions.** Capacities may be any nonnegative reals; the bound on the number of rounds does not use integrality, and integer capacities give an integral flow. The graph is directed; give an undirected edge as two directed edges. Antiparallel, parallel and zero-capacity edges and self-loops are allowed; each edge has its own pair of residual arcs. A zero-capacity edge never appears in $G_f$. If $t$ is not reachable from $s$, the first search fails and the answer is the zero flow with $S$ the set of vertices reachable from $s$.

## The algorithm

```pseudo id=main
EDMONDS-KARP(G, c, s, t)
L1  for each edge e do c_f(e⁺) ← c(e), c_f(e⁻) ← 0
L2  repeat: for each v do π[v] ← nil;  mark s
L3      Q ← a queue holding s
L4      while Q is not empty and t is not marked do
L5          u ← DEQUEUE(Q); for each arc x = (u, v) of u do
L6              if c_f(x) > 0 and v is not marked then
L7                  mark v, π[v] ← x, ENQUEUE(Q, v)
L8      if t is not marked then leave the repeat loop
L9      Δ ← min { c_f(x) : x on the path π from s to t }
L10     for each arc x on that path do c_f(x) ← c_f(x) − Δ, c_f(reverse x) ← c_f(reverse x) + Δ
L11 return f with f(e) = c_f(e⁻), and S = the marked vertices
```

Lines L2 to L7 are a breadth-first search in $G_f$ that stops as soon as $t$ is marked. The parent arcs $\pi$ form a BFS tree, so the tree path from $s$ to $t$ is a shortest path in $G_f$. Lines L9 and L10 augment along it, as in Ford-Fulkerson. When the search does not reach $t$, it has run to the end, so the marked vertices are exactly those reachable from $s$ in $G_f$, which line L11 returns as the source side of a minimum cut.

## Example

The network is the running example: $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10. Each vertex scans its arcs in input order. The table gives the BFS distances $\delta_f$ in $G_f$ before each round, for $s\,a\,b\,c\,d\,t$, and the path found.

| round | $\delta_f$ for $s\,a\,b\,c\,d\,t$ | shortest path | $\Delta$ | arcs that become full | value |
|---|---|---|---|---|---|
| 1 | 0 1 2 1 2 3 | $s\,a\,b\,t$ | 4 | $a b$ | 4 |
| 2 | 0 1 3 1 2 3 | $s\,a\,d\,t$ | 6 | $s a$ | 10 |
| 3 | 0 3 3 1 2 3 | $s\,c\,d\,t$ | 4 | $d t$ | 14 |
| 4 | 0 3 3 1 2 4 | $s\,c\,d\,b\,t$ | 5 | $c d$ | 19 |
| 5 | 0 ∞ ∞ 1 ∞ ∞ | none | | | |

The distances never go down, as the proof shows. After round 2, $a$ is at distance 3: $s a$ is full, and the only way back to $a$ is $s\,c\,d\,a$, through the backward arc of $a d$. In round 4 the distance to $t$ grows from 3 to 4. After round 4 only $c$ is reachable, so $S = \{s, c\}$ and the cut has capacity $c(s, a) + c(c, d) = 19$, equal to the flow value.

## Correctness

Edmonds-Karp is Ford-Fulkerson with a particular choice of path, so the proof of [Ford-Fulkerson](/ford-fulkerson/) applies: each round keeps a feasible flow and raises its value by $\Delta > 0$, and when no augmenting path is left, the set $S$ of line L11 is the source side of a cut whose capacity equals the flow value, so the flow is maximum and the cut is minimum. What is new is termination for every real capacity, which follows from the bound on the number of rounds below. The full proof is in the proof files below.

## Complexity

The model is the [word RAM](/word-ram/) (or the real RAM for real capacities); an arithmetic operation or comparison costs $O(1)$.

- **One round.** BFS takes $O(n + m)$, and lines L9 and L10 take $O(n)$.
- **Distances never decrease.** Let $\delta_f(v)$ be the BFS distance from $s$ in $G_f$. After an augmentation along a shortest path, $\delta_{f'}(v) \ge \delta_f(v)$ for each $v$. An augmentation only removes arcs of the path and adds reverses of arcs $(u, w)$ of the path, which go from distance $\delta_f(u) + 1$ to $\delta_f(u)$; such an arc never gives a shortcut.
- **Each arc is critical at most $n/2$ times.** An arc $x = (u, v)$ is *critical* in a round if its residual capacity equals $\Delta$, so it leaves $G_f$. Then $\delta_f(v) = \delta_f(u) + 1$. Before $x$ can be critical again, its reverse $(v, u)$ must be on an augmenting path, at a moment with $\delta_g(u) = \delta_g(v) + 1 \ge \delta_f(v) + 1 = \delta_f(u) + 2$. So the distance of $u$ grows by at least 2 between two critical rounds of $x$. While $x$ can be critical, $v$ is reachable at distance at most $n - 1$, so $\delta(u) \le n - 2$. So $x$ is critical at most $n/2$ times.
- **Rounds.** Each round has at least one critical arc, and there are $2m$ arcs, so the number of rounds is at most $2m \cdot n/2 = nm$.
- **Total.** $O(nm)$ rounds of $O(n + m)$ time each: $O(nm^2)$ when $m \ge n - 1$, for any real capacities. With integer capacities it is also at most $O(mF)$, the Ford-Fulkerson bound, so the time is $O(\min(nm^2, mF))$.
- **Space.** $\Theta(n + m)$ for the residual capacities, the adjacency lists, the queue and $\pi$.

The full argument is in the complexity proof below.

## Properties

- **Strongly polynomial.** The number of rounds does not depend on the capacities.
- **Integral.** With integer capacities each $\Delta$ is an integer and the flow is integral.
- **Certificate.** $S$ gives a minimum cut; checking the answer takes $O(n + m)$.
- **Monotone distances.** The distance from $s$ to each vertex in the residual graph never decreases. This is the key invariant, reused by [Dinic's algorithm](/dinic/) and by the distance labels of [push-relabel](/push-relabel/).

## Variants and improvements

- **[Dinic's algorithm](/dinic/).** Build the [level graph](/level-graph/) once per distance and push a [blocking flow](/blocking-flow/) in it, which does all the augmentations of one distance together: $O(n^2 m)$ time.
- **Distance labels.** Ahuja and Orlin keep exact distance labels and advance and retreat along admissible arcs, which gives the shortest augmenting path algorithm in $O(n^2 m)$ time without a BFS per path.
- **[Fattest augmenting path](/fattest-augmenting-path/) and [capacity scaling](/capacity-scaling/).** Choose paths by capacity instead of length; better when capacities are small integers.
- **Bidirectional BFS.** Search from $s$ and from $t$ at once to find each path faster in practice.

## When to use it

Use Edmonds-Karp when you want a short, safe maximum flow code that works for real capacities and small or medium graphs. For larger graphs, [Dinic's algorithm](/dinic/) is as short and much faster, and [push-relabel](/push-relabel/) is the usual choice in practice for large dense networks. For unit capacities and bipartite matching, Dinic (as Hopcroft-Karp) is faster.

## Pitfalls

- **Using DFS.** Line L5 must take vertices from a queue in first-in first-out order. A stack gives a path that is not shortest, and the $O(nm)$ bound on rounds is lost.
- **Searching in $G$ instead of $G_f$.** The test $c_f(x) > 0$ of line L6 must use the residual capacity; backward arcs must be in the lists of line L5.
- **Merging antiparallel edges wrongly.** One residual entry per ordered pair must hold the sum of the forward residual of $(u, v)$ and the backward residual of $(v, u)$. Keep one arc pair per edge, as in line L1, to avoid this.
- **Reading the cut from a partial search.** The marks of line L11 are only the reachable set after a search that did not find $t$. A search that stops early at line L4 has not marked all reachable vertices.
- **Floating point.** The critical arc becomes exactly 0, because $x - x = 0$ in floating point, so the bound on rounds still holds; but values computed by sums can differ from the exact maximum by rounding errors.

## Implementations

The Python version takes the vertex count, a list of edges $(u, v, c)$ and $s, t$, and returns the value, the flow on each input edge and the sorted source side of a minimum cut. Capacities may be `int`, `Fraction` or `float`.

## History

Yefim Dinitz published the use of shortest augmenting paths in 1970, together with the blocking flow method that bears his name. Jack Edmonds and Richard Karp published the bound on the number of shortest augmenting paths in the Journal of the ACM in 1972, independently, together with the scaling idea for min-cost flow.

## References
