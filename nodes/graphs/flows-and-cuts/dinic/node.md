---
tag: K5ZN3K
kind: algorithm
slug: dinic
name: Dinic's algorithm
aliases:
- Dinitz algorithm
- blocking flow algorithm
area: graphs/flows-and-cuts
level: core
summary: Augment along blocking flows in successive level graphs, running in O(V^2E).
solves: [max-flow-problem, min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^2 m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1970
  people: [Yefim Dinitz, Shimon Even, Alon Itai]
  note: Dinitz published the layered network method in 1970; the version with a depth-first search and current-arc pointers taught today is due to Even and Itai.
prereqs: [edmonds-karp, blocking-flow, level-graph]
see_also: [mpm-algorithm, push-relabel, hopcroft-karp, link-cut-tree, capacity-scaling, max-flow-min-cut-theorem, edge-disjoint-paths]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (Dinitz's blocking flow algorithm)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 7, Maximum Flows, Polynomial Algorithms (layered networks and Dinic's algorithm)
  - book: isbn:9780898711875
    title: Robert Endre Tarjan, Data Structures and Network Algorithms
    locator: Chapter 8, Network Flows (Dinic's algorithm and blocking flows with dynamic trees)
  - paper: doi:10.1007/11685654_10
    title: Yefim Dinitz, Dinitz' algorithm, the original version and Even's version, in Theoretical Computer Science, Essays in Memory of Shimon Even, LNCS 3895, 218 to 240 (2006)
    locator: the whole chapter (the 1970 algorithm and the current-arc version)
  - paper: doi:10.1137/0204043
    title: Shimon Even and Robert Endre Tarjan, Network flow and testing graph connectivity, SIAM Journal on Computing 4(4), 507 to 518 (1975)
    locator: the analysis of Dinic's algorithm on networks with unit capacities
---

Dinic's algorithm (also written Dinitz) computes a [maximum flow](/max-flow-problem/) in phases. Each phase builds the [level graph](/level-graph/) of the [residual graph](/residual-graph/) by one breadth-first search and then pushes a [blocking flow](/blocking-flow/) in it with a depth-first search that never looks at an arc twice. Each phase makes the distance from $s$ to $t$ grow, so there are at most $n - 1$ phases, and the whole algorithm runs in $O(n^2 m)$ time for any real capacities. It is the standard maximum flow code in practice and in programming contests, and on unit-capacity networks it is much faster still.

## In plain words

[Edmonds-Karp](/edmonds-karp/) finds one shortest route from the source to the drain, pushes water along it, and then searches the whole network again. Dinic does all the shortest routes of the same length in one go.

First it labels each place with its distance from the source. Then it walks forward from the source, always to a place one step farther, until it reaches the drain, and pushes water along that walk. When a place turns out to be a dead end, it walks back one step and never tries that way again in this round. When the source itself is stuck, every shortest route has a full pipe. The next round has only longer routes, and routes cannot be longer than the number of places, so there are few rounds.

## The problem

The input is a [flow network](/flow-network/) $N = (G, c, s, t)$ with a directed graph $G = (V, E)$ of $n$ vertices and $m$ edges, capacities $c(e) \ge 0$, and $s \ne t$. The output is a maximum [s-t flow](/s-t-flow/) and the source side of a minimum s-t cut.

**Assumptions.** Capacities may be any nonnegative reals; the bound on phases and on the work per phase does not use integrality, and integer capacities give an integral flow. The graph is directed; give an undirected edge as two directed edges. Antiparallel, parallel and zero-capacity edges and self-loops are allowed, and each edge has its own pair of residual arcs. A zero-capacity edge is never in $G_f$, so never in a level graph. If $t$ is not reachable from $s$, the first search fails and the answer is the zero flow with $S$ the set of vertices reachable from $s$.

## The algorithm

```pseudo id=main
DINIC(G, c, s, t)
L1  for each edge e do c_f(e⁺) ← c(e), c_f(e⁻) ← 0
L2  repeat
L3      level ← BFS distances from s in G_f, using only arcs with c_f > 0 (−1 if unreached)
L4      if level[t] < 0 then leave the repeat loop
L5      for each v do it[v] ← the first arc in the list of v
L6      P ← the empty path;  u ← s
L7      loop
L8          if u = t then
L9              Δ ← min { c_f(x) : x on P };  augment by Δ along P;  P ← empty;  u ← s
L10         else if it[u] is an arc x = (u, w) with c_f(x) > 0 and level[w] = level[u] + 1 then
L11             append x to P;  u ← w
L12         else if it[u] is an arc then it[u] ← the next arc in the list of u
L13         else if u = s then leave the loop
L14         else remove the last arc (v, u) of P;  u ← v;  it[v] ← the next arc in the list of v
L15 return f with f(e) = c_f(e⁻), and S = { v : level[v] ≥ 0 }
```

Line L3 is a [breadth-first search](/breadth-first-search/); the arcs $(v, w)$ with $c_f > 0$ and $\text{level}[w] = \text{level}[v] + 1$ form the level graph $L_f$. Lines L5 to L14 compute a blocking flow in $L_f$. The walk of lines L10 and L11 advances along level arcs, line L9 augments when it reaches $t$, line L12 skips an arc that cannot be used, and line L14 retreats from a dead end $u$, whose pointer has run past its last arc. The pointer $it[v]$ is the *current arc* of $v$: arcs before it are never tried again in this phase. Line L9 augments exactly as in [Ford-Fulkerson](/ford-fulkerson/): $c_f(x) \leftarrow c_f(x) - \Delta$ and $c_f(\bar x) \leftarrow c_f(\bar x) + \Delta$ for each arc $x$ of $P$ and its reverse $\bar x$.

## Example

The network is the running example: $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10. Each vertex lists its arcs in input order, forward and backward arcs mixed.

**Phase 1.** The levels are $s$: 0, $a, c$: 1, $b, d$: 2, $t$: 3. The level graph drops $a c$ (both ends at level 1) and $d b$ (both at level 2).

| step | walk | $\Delta$ | arcs that become full | value |
|---|---|---|---|---|
| 1 | $s\,a\,b\,t$ | 4 | $a b$ | 4 |
| 2 | $s\,a\,d\,t$ (the pointer of $a$ skips the full $a b$ and the arc $a c$) | 6 | $s a$ | 10 |
| 3 | $s\,c\,d\,t$ (the pointer of $s$ skips the full $s a$) | 4 | $d t$ | 14 |
| 4 | at $d$ the pointer runs out, retreat to $c$; $c$ runs out, retreat to $s$; $s$ runs out | | | 14 |

The blocking flow of this phase has value 14.

**Phase 2.** Now $s a$ and $a b$ are full and $d t$ is full. The new levels are $s$: 0, $c$: 1, $d$: 2, $a, b$: 3, $t$: 4, where $a$ is reached through the backward arc of $a d$ and $b$ through $d b$. The distance to $t$ grew from 3 to 4. The walk goes $s\,c\,d\,a$, finds that $a$ is a dead end (its arcs lead to levels 0 and 1 or are full), retreats to $d$, and then finds $s\,c\,d\,b\,t$ with $\Delta = 5$, which fills $c d$. Then the pointers run out and the phase ends with value 19.

**Phase 3.** The search reaches only $s$ and $c$, so the algorithm stops with $S = \{s, c\}$, a cut of capacity $c(s, a) + c(c, d) = 10 + 9 = 19$. Edmonds-Karp does the same four augmentations but runs five breadth-first searches, one per augmentation and a last one; Dinic runs three.

**A blocking flow that is not maximum.** On the network $s x_1$, $s x_2$, $x_1 y_1$, $x_1 y_2$, $x_2 y_1$, $y_1 t$, $y_2 t$, all of capacity 1, phase 1 pushes 1 along $s\,x_1\,y_1\,t$ and stops, because every path of length 3 now has a full arc. Phase 2 uses the backward arc $(y_1, x_1)$ in the path $s\,x_2\,y_1\,x_1\,y_2\,t$ of length 5 and reaches the maximum 2.

**Edge cases.** With $s \to a$ of capacity 5 and $t \to a$ of capacity 5, the first search does not reach $t$, the flow is 0 and $S = \{s, a\}$. A zero-capacity edge $s \to t$ is never used. With the antiparallel edges $s \to a$ 3, $a \to b$ 2, $b \to a$ 1, $b \to t$ 2, $s \to b$ 1, the answer is 2, and the two edges between $a$ and $b$ keep separate flows.

## Correctness

Each augmentation in line L9 is an augmentation along an s-t path of $G_f$ by its bottleneck, so by the augmentation lemma of [augmenting path](/augmenting-path-flow/) the flow stays feasible and its value grows by $\Delta > 0$. During a phase, arcs of $L_f$ only lose residual capacity, because the reverse of a level arc goes down a level and is never a level arc. A vertex whose pointer has run out has no path to $t$ in what is left of $L_f$, and the pointer skips only arcs that are full, not level arcs, or lead to such a dead vertex. So when $s$ runs out (line L13), every s-t path of $L_f$ has a full arc: the phase found a blocking flow. By the lemma on [blocking flows](/blocking-flow/), the distance from $s$ to $t$ grows, so after at most $n - 1$ phases $t$ is unreachable. Then $S$ of line L15 is the set of vertices reachable from $s$ in $G_f$, every edge leaving $S$ is full and every edge entering it is empty, so $|f| = c(S, V \setminus S)$ and the flow is maximum and the cut minimum. The full proof is in the proof files below.

## Complexity

The model is the [word RAM](/word-ram/), or the [real RAM](/real-ram/) for real capacities; an arithmetic operation or comparison costs $O(1)$.

- **Phases.** At most $n - 1$, since $1 \le d_f(t) \le n - 1$ while $t$ is reachable and $d_f(t)$ grows by at least 1 per phase.
- **One phase.** The search of line L3 costs $O(n + m)$. In the loop, each pass of line L12 or L14 moves a pointer, and there are at most $2m$ arcs, so at most $2m$ such passes. Each augmentation fills an arc of $L_f$ that stays full for the rest of the phase, so it is not on any later path; $L_f$ has at most $m$ arcs (the two arcs of one edge cannot both go up a level), so there are at most $m$ augmentations. A path has at most $n - 1$ arcs, so each augmentation costs $O(n)$, and each forward step of line L11 is later undone by an augmentation or by a retreat. So one phase costs $O(m + nm) = O(nm)$.
- **Total.** $O(n^2 m)$ time for any real capacities, with $\Theta(n + m)$ space.
- **Unit capacities.** If every capacity is 1, an augmentation fills every arc of its path, so a phase costs $O(m)$, and Even and Tarjan showed that there are $O(\min(\sqrt m, n^{2/3}))$ phases: $O(m \min(\sqrt m, n^{2/3}))$ time. If moreover every vertex other than $s$ and $t$ has in-degree 1 or out-degree 1, as in the network of [bipartite matching](/bipartite-matching/), there are $O(\sqrt n)$ phases, which is [Hopcroft-Karp](/hopcroft-karp/).
- **Integer capacities.** Each phase raises the value by at least 1, so there are also at most $F$ phases, where $F$ is the maximum flow value.

The full argument is in the complexity proof below.

## Properties

- **Strongly polynomial.** The bound does not depend on the capacities.
- **Integral.** With integer capacities each $\Delta$ is an integer and the flow is integral.
- **Certificate.** $S$ is the source side of a minimum cut; checking the answer takes $O(n + m)$.
- **Monotone distances.** The distance from $s$ to $t$ in the residual graph grows strictly with each phase, and the distance to every vertex never decreases.
- **Fast in practice.** The bound $O(n^2 m)$ is rarely reached; the number of phases is usually far below $n$.

## Variants and improvements

- **[MPM algorithm](/mpm-algorithm/).** Computes each blocking flow in $O(n^2)$ by pushing from the vertex of least throughput: $O(n^3)$ total.
- **Dynamic trees.** Sleator and Tarjan keep the partial paths of the current arcs in [link-cut trees](/link-cut-tree/), so a blocking flow costs $O(m \log n)$ and the maximum flow $O(nm \log n)$.
- **Capacity scaling.** Run Dinic only on arcs of residual capacity at least $\Delta$, halving $\Delta$; with integer capacities up to $U$ this takes $O(nm \log U)$, as on the page [capacity scaling](/capacity-scaling/).
- **Dinitz's original version.** The 1970 paper kept the layered network explicitly and deleted dead vertices and full arcs from it, rather than using a depth-first search with pointers; the bound is the same.
- **Goldberg and Rao.** Binary blocking flows with length functions that depend on the capacities give $O(\min(n^{2/3}, m^{1/2})\, m \log(n^2/m) \log U)$ for integer capacities.

## When to use it

Dinic is the default maximum flow code when you need a short, robust program: about forty lines, real capacities, and fast in practice on most inputs. It is the best simple choice for unit-capacity networks, such as [edge-disjoint paths](/edge-disjoint-paths/), matchings and connectivity tests. For very large dense networks, highest-label [push-relabel](/push-relabel/) with heuristics is often faster; for the best known theoretical bounds, see the [almost-linear algorithm](/almost-linear-max-flow/).

## Pitfalls

- **Resetting the pointers.** The pointers are set once per phase, in line L5. If each new walk from $s$ scans every list from its first arc again, one phase can take far more than $O(nm)$.
- **Not advancing past a dead end.** Line L14 must advance the pointer of $v$ past the arc to $u$. Otherwise the walk returns to $u$ again and again.
- **Level test.** The test must be $\text{level}[w] = \text{level}[u] + 1$, not $\text{level}[w] > \text{level}[u]$; arcs that jump levels can make paths longer than $d_f(t)$, and the distance argument fails.
- **Recursion depth.** A recursive depth-first search can go $n$ deep; in languages with a small stack, use the explicit path of lines L6 to L14.
- **Merging antiparallel edges wrongly.** One residual entry per ordered pair must add the forward residual of $(u, v)$ and the backward residual of $(v, u)$. Keep one arc pair per edge, as in line L1.
- **Floating point.** The bottleneck arc becomes exactly 0, so termination holds, but the value can differ from the exact maximum by rounding errors.

## Implementations

The Python version takes the vertex count, a list of edges $(u, v, c)$ and $s, t$, and returns the value, the flow on each input edge and the sorted source side of a minimum cut. Capacities may be `int`, `Fraction` or `float`. The depth-first search keeps the path as a list of arcs instead of using recursion, and an optional callback reports each phase and path.

## History

Yefim Dinitz, a student in Georgy Adelson-Velsky's group in Moscow, published the algorithm in 1970 in Soviet Mathematics Doklady, together with the use of shortest augmenting paths. Shimon Even and Alon Itai worked out the version with a depth-first search and current-arc pointers, which Even taught and spread in the West; Dinitz described both versions in a 2006 essay. Even and Tarjan analyzed it on unit-capacity networks in 1975, Malhotra, Kumar and Maheshwari gave the $O(n^3)$ blocking flow in 1978, and Sleator and Tarjan the $O(nm \log n)$ version with dynamic trees in 1983.

## References
