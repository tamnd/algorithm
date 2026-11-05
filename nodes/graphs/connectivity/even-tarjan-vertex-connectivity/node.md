---
tag: NX705H
kind: algorithm
slug: even-tarjan-vertex-connectivity
name: Even-Tarjan vertex connectivity algorithm
aliases:
- Even-Tarjan k-connectivity test
area: graphs/connectivity
level: advanced
summary: Tests and computes vertex connectivity by running a bounded number of max-flow computations.
solves: [vertex-connectivity]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the vertex connectivity}
  time: {worst: "O((k + 1) n^(3/2) m)"}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1975
  people: [Shimon Even, Robert Tarjan]
  note: Even gave a test for k-connectivity by a bounded number of flows in 1975, and Even and Tarjan bounded the flows by Dinic's method on unit networks in the same year.
prereqs: [vertex-connectivity, menger-theorem, vertex-capacities-flow]
see_also: [k-vertex-connected-graph, vertex-cut, dinic, vertex-disjoint-paths, edge-connectivity, hopcroft-tarjan-biconnectivity, nagamochi-ibaraki-certificate]
sources:
  - paper: doi:10.1137/0204043
    title: Shimon Even and Robert E. Tarjan, Network flow and testing graph connectivity, SIAM Journal on Computing 4(4), 507 to 518 (1975)
    locator: the bound for Dinic's algorithm on networks with unit vertex capacities, and the vertex connectivity algorithm
  - paper: doi:10.1137/0204034
    title: Shimon Even, An algorithm for determining whether the connectivity of a graph is at least k, SIAM Journal on Computing 4(3), 393 to 396 (1975)
    locator: the test for k-connectivity by a bounded number of flows
  - book: isbn:9780521736534
    title: Shimon Even, Graph Algorithms, second edition, edited by Guy Even, Cambridge University Press (2012)
    locator: Chapter 6, Applications of network flow techniques (vertex connectivity of undirected graphs)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 3.3, Menger's theorem
---

The Even-Tarjan algorithm computes the [vertex connectivity](/vertex-connectivity/) $\kappa(G)$ of an [undirected graph](/undirected-graph/): the least number of vertices whose removal disconnects it. By [Menger's theorem](/menger-theorem/), the least [vertex cut](/vertex-cut/) between two non-adjacent vertices $s$ and $t$ equals the most $s$-$t$ paths that share no inner vertex, and one [maximum flow](/max-flow-problem/) with [unit vertex capacities](/vertex-capacities-flow/) finds that number. The naive method runs such a flow for every non-adjacent pair, about $n^2/2$ flows. Even and Tarjan run flows only from the first $\kappa + 1$ vertices, which is at most $(\kappa + 1)(n - 1)$ flows. With [Dinic's algorithm](/dinic/) each flow costs $O(n^{1/2} m)$, and the total is $O(n^{1/2} m^2)$.

## In plain words

You want to know how many towns of a road network must close before some two towns can no longer reach each other.

For two towns that do not share a road, count the routes between them that share no town on the way. The number of such routes is the number of towns you must close to cut the two apart. A flow computation counts these routes.

You do not need to try every pair. Take the towns in a fixed order. The best set of towns to close is too small to hold all of the first few towns. So one of the first few towns is left standing, and some town is cut off from it. Try the pairs that start at the first towns, and stop as soon as you have tried one more town than your best answer so far.

## The problem

**Input.** An undirected graph $G = (V, E)$ with $n \ge 1$ vertices $v_1, \ldots, v_n$ and $m$ edges. Parallel edges and [self-loops](/self-loop/) are allowed and do not change the answer: the algorithm only asks whether two distinct vertices are adjacent.

**Output.** The vertex connectivity

$$\kappa(G) = \begin{cases} n - 1 & \text{if any two distinct vertices are adjacent,} \\ \min \{\, |X| : X \subseteq V,\ G - X \text{ is disconnected} \,\} & \text{otherwise.} \end{cases}$$

For non-adjacent $s \neq t$, let $\kappa(s, t)$ be the least size of a set $X \subseteq V \setminus \{s, t\}$ such that $G - X$ has no $s$-$t$ path. By Menger's theorem, $\kappa(s, t)$ is also the most $s$-$t$ paths that pairwise share only $s$ and $t$. If $G$ is not complete, then $\kappa(G) = \min \kappa(s, t)$ over the non-adjacent pairs.

## The algorithm

The vertices are taken in a fixed order $v_1, \ldots, v_n$. The variable $k$ is the best bound so far, and the outer loop reads its current value at each test.

```pseudo id=main
VERTEX-CONNECTIVITY(G)
L1  k ← n − 1
L2  i ← 1
L3  while i ≤ k do
L4      for j ← i + 1 to n do
L5          if v_i and v_j are not adjacent then
L6              k ← min(k, LOCAL(v_i, v_j, k))
L7      i ← i + 1
L8  return k

LOCAL(s, t, c)                         ▷ min(c, κ(s, t)), for s ≠ t not adjacent
L9  D ← the split digraph: an arc w_in → w_out for each vertex w, and arcs a_out → b_in, b_out → a_in for each edge {a, b}; every arc has capacity 1
L10 f ← 0
L11 while f < c and D has an augmenting path from s_out to t_in do
L12     send one unit along the path, f ← f + 1
L13 return f
```

A flow of value $f$ from $s_{\mathrm{out}}$ to $t_{\mathrm{in}}$ in $D$ is a set of $f$ paths from $s$ to $t$ that share no inner vertex, because each inner vertex $w$ has one arc $w_{\mathrm{in}} \to w_{\mathrm{out}}$ of capacity 1. The digraph $D$ can be built once and its residual capacities reset after each call. The cap $c$ stops a flow as soon as it cannot lower $k$.

## Example

The graph has the vertices $1, \ldots, 8$ and 21 edges: the edge $\{1, 2\}$ twice, the edges from 1 and from 2 to each of $3, \ldots, 8$, the triangles $3, 4, 5$ and $6, 7, 8$, and a loop at 8. The set $\{1, 2\}$ separates the two triangles, and no single vertex does, so $\kappa(G) = 2$.

| step | $i$ | pairs $(v_i, v_j)$ that are not adjacent | $\kappa(v_i, v_j)$ | $k$ after |
|---|---|---|---|---|
| start | | | | 7 |
| 1 | 1 | none: 1 is adjacent to all | | 7 |
| 2 | 2 | none: 2 is adjacent to all | | 7 |
| 3 | 3 | $(3, 6)$, $(3, 7)$, $(3, 8)$ | 2, 2, 2 | 2 |
| test | 4 | $4 > k = 2$, stop | | 2 |

Three flows find the answer. The naive method tries all nine non-adjacent pairs $(x, y)$ with $x \in \{3, 4, 5\}$ and $y \in \{6, 7, 8\}$. The first two vertices are both in the cut $\{1, 2\}$, so the loop must reach $i = 3 = \kappa + 1$. The paths that LOCAL finds for $(3, 6)$ are $3, 1, 6$ and $3, 2, 6$; the parallel edge and the loop add no path.

## Correctness

The claim is that the algorithm returns $\kappa(G)$. A full proof is on the [correctness page](proofs/correctness/). In short:

1. **LOCAL is right.** Paths in $G$ with disjoint inner vertices map to unit flow paths in $D$ and back, so the maximum flow value is $\kappa(s, t)$ by Menger's theorem, and the cap returns $\min(c, \kappa(s, t))$.
2. **$k$ never drops below $\kappa(G)$.** Each value that line L6 takes is $n - 1$ or some $\kappa(v_i, v_j) \ge \kappa(G)$.
3. **$k$ reaches $\kappa(G)$.** If $G$ is complete, no pair is tested and $k = n - 1$. Otherwise let $X$ be a smallest vertex cut, so $|X| = \kappa(G) \le n - 2$. Among $v_1, \ldots, v_{\kappa(G) + 1}$ some vertex is not in $X$; let $v_i$ be the first one. A vertex $v_j$ in another component of $G - X$ is not adjacent to $v_i$ and is not in $X$, so $j > i$, since all earlier vertices are in $X$. So when line L4 runs for this $i$, it tests the pair $(v_i, v_j)$, and $\kappa(v_i, v_j) \le |X|$. The loop does reach this $i$: if $k = \kappa(G)$ before that, there is nothing left to show, and otherwise $k \ge \kappa(G) + 1 \ge i$.

## Complexity

**Number of flows.** Line L3 lets $i$ go up to $\kappa(G) + 1$ at most, by step 3 above, so at most $(\kappa + 1)(n - 1)$ calls of LOCAL run. A naive method needs up to $n(n-1)/2$ flows.

**One flow.** With [Dinic's algorithm](/dinic/), a network in which every vertex other than the source and sink has one entering arc or one leaving arc of capacity 1 needs $O(\sqrt{n})$ phases, so one flow costs $O(n^{1/2} m)$ (Even and Tarjan, 1975). With plain augmenting paths found by [breadth-first search](/breadth-first-search/), as in the program below, a call costs $O(\min(c, n)(n + m))$.

**Total.** $O((\kappa + 1) n \cdot n^{1/2} m)$ with Dinic's algorithm. Each vertex has degree at least $\kappa$, so $\kappa n \le 2m$, and the bound is $O(n^{1/2} m^2)$ for a connected graph. The space is $\Theta(n + m)$ for $D$ and the search.

**Testing $\kappa(G) \ge k$.** For a fixed $k$, start with the bound $k$ instead of $n - 1$ and stop as soon as some flow is below $k$. This runs at most $k(n - 1)$ flows, each with at most $k$ augmenting paths of cost $O(n + m)$, so $O(k^2 n (n + m))$ time.

## Properties

- **Deterministic.** The vertex order is fixed, and the answer does not depend on it.
- **Exact.** It returns $\kappa(G)$, not a bound.
- **Gives a cut.** If $G$ is not complete, the last flow that lowered $k$ also gives a smallest vertex cut: the vertices $w$ with $w_{\mathrm{in}}$ reachable from $s_{\mathrm{out}}$ in the final residual digraph and $w_{\mathrm{out}}$ not reachable.
- **Uses only adjacency.** Parallel edges and loops change neither the answer nor the flows.

## Variants and improvements

- **The k-connectivity test.** Fix the target $k$ and answer yes or no; see the complexity section.
- **Sparse certificates.** For a test with a fixed $k$, a [sparse certificate](/nagamochi-ibaraki-certificate/) with $O(k n)$ edges keeps the answer, and the flows then run on the smaller graph.
- **Small $k$.** For $k \le 2$ one [depth-first search](/depth-first-search/) is enough: the graph is 2-connected when it is connected, has at least three vertices and has no [articulation point](/articulation-point/), which the [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-biconnectivity/) finds in $O(n + m)$ time. Hopcroft and Tarjan also gave a linear test for $k = 3$.
- **Edge version.** Splitting no vertex and giving each edge capacity 1 gives the local [edge connectivity](/edge-connectivity/) instead. For edges, flows from one fixed vertex suffice, since that vertex is never deleted.
- **Fewer flows.** Later work reduces the number of flow calls further, with randomization or with expander methods; Li, Nanongkai, Panigrahi, Saranurak and Yingchareonthawornchai (2021) need only a polylogarithmic number of maximum flows.

## When to use it

Use it when you need the exact vertex connectivity, or a smallest vertex cut, of a graph of moderate size, and $\kappa$ is small compared with $n$. For a yes or no test of $k \le 3$, use the linear depth-first search methods. For very large graphs, the newer methods based on fewer flows are faster in theory.

## Pitfalls

- **Adjacent pairs.** No vertex set separates two adjacent vertices, so a flow between them does not measure a cut. Skip them, as line L5 does.
- **Pairs with $j < i$.** They are not needed, because every vertex before the first vertex outside $X$ is in $X$. Adding them is safe but wastes flows.
- **Edge capacities only.** A flow with unit edge capacities and no split vertices counts edge-disjoint paths, which gives the edge connectivity, a larger number in general.
- **The loop bound.** Line L3 must read $k$ again at each test. A loop up to the first value $n - 1$ is still correct but runs all pairs.
- **The complete graph.** It has no vertex cut, and the convention $\kappa(K_n) = n - 1$ comes from line L1.
- **Recursion.** A depth-first augmenting search can recurse $n$ levels deep; use breadth-first search or an explicit stack.

## Implementations

## History

Menger proved in 1927 that the least vertex cut between two non-adjacent vertices equals the most paths that share no inner vertex. Ford and Fulkerson's flow theory in the 1950s turned this into an algorithm. In 1975 Even published a test for $\kappa(G) \ge k$ that needs only a bounded number of flows, and Even and Tarjan showed that Dinic's algorithm runs in $O(n^{1/2} m)$ time on networks with unit vertex capacities. Together these give $\kappa(G)$ in $O(n^{1/2} m^2)$ time. Their paper also bounds the edge connectivity by flows.

## References
