---
tag: 13QZ7V
kind: algorithm
slug: successive-shortest-path
name: Successive shortest path algorithm
aliases:
- SSP algorithm
area: graphs/flows-and-cuts
level: core
summary: Send flow along shortest-cost augmenting paths in the residual graph repeatedly.
solves: [min-cost-flow-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, F: the value of the returned flow}
  time: {worst: O(n m + F m log n)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [min-cost-flow-problem, residual-graph, dijkstra, bellman-ford, potential-function-reduced-costs]
see_also: [cycle-canceling, cost-scaling, network-simplex, hungarian-algorithm, johnson, edmonds-karp, assignment-problem, negative-cycle-detection]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 9, Minimum Cost Flows, Basic Algorithms (reduced cost optimality conditions and the successive shortest path algorithm), and Chapter 10 (capacity scaling)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 12, Minimum-cost flows and circulations (minimum-cost flows by successive shortest paths)
  - paper: doi:10.1145/321694.321699
    title: Jack Edmonds and Richard M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2), 248 to 264 (1972)
    locator: the section on minimum-cost flows (node potentials that keep edge lengths nonnegative, so that Dijkstra's algorithm can be used, and the scaling method)
---

The successive shortest path algorithm solves the [minimum-cost flow problem](/min-cost-flow-problem/) by building the flow one augmenting path at a time, always along a path of least cost in the [residual graph](/residual-graph/). After each augmentation the flow is the cheapest flow of its value. Vertex potentials, updated with the shortest-path distances, keep all residual reduced costs nonnegative, so each round is one run of [Dijkstra's algorithm](/dijkstra/) after one initial [Bellman-Ford](/bellman-ford/). With integer capacities, a flow of value $F$ takes at most $F$ rounds, which is pseudo-polynomial; capacity scaling turns it into a polynomial method.

## In plain words

You must ship a number of units from one place to another through roads with limits and prices. Ship them one batch at a time. Each time, look for the cheapest route that still has room, counting the option of taking back units already sent on some road, which refunds its price. Send as much as that route allows, and repeat until enough has been sent.

Because each batch takes the cheapest route at that moment, the plan is always the cheapest plan for the amount sent so far. The extra cost per unit only grows. A bookkeeping trick, one number per place, turns all route prices into nonnegative ones, so the fast method for cheapest routes can be used each time.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a source $s$, a sink $t \ne s$, a target value $d$ (possibly $\infty$), and for each edge an integer capacity $u(e) \ge 0$ and an integer or real cost $c(e)$ of any sign. Parallel edges, also with different costs, and antiparallel edges are allowed; each edge has its own forward residual edge and its own backward residual edge of cost $-c(e)$, and the pairs are never merged. Self-loops carry no flow. The edges of positive capacity must contain no cycle of negative cost; otherwise the zero flow is not optimal for value 0, and the method does not apply. The output is a flow of value $\min(d, f^{*})$, where $f^{*}$ is the maximum flow value, of least cost among all flows of that value. With $d = \infty$ it is a min-cost maximum flow. If $t$ is not reachable from $s$, the output is the zero flow.

## The algorithm

```pseudo id=main
SUCCESSIVE-SHORTEST-PATH(G, u, c, s, t, d)
L1  x ← 0; value ← 0
L2  π ← BELLMAN-FORD distances from a new root joined to every vertex by edges of cost 0, using the edges with u(e) > 0; stop if a negative cycle is found
L3  while value < d do
L4      dist ← DIJKSTRA(G_x, s) with lengths c^π(v, w) = c(v, w) + π(v) − π(w)
L5      if dist(t) = ∞ then break
L6      for each v with dist(v) < ∞ do π(v) ← π(v) + dist(v)
L7      P ← the shortest s-t path found; δ ← min(d − value, the least residual capacity on P)
L8      augment x by δ along P; value ← value + δ
L9  return x, value, and the cost Σ c(e) x(e)
```

Line L2 makes $c^{\pi} \ge 0$ on every edge of positive capacity: Bellman-Ford distances satisfy $\pi(w) \le \pi(v) + c(v, w)$. Line L6 keeps this true in each residual graph, and makes $c^{\pi} = 0$ along the path $P$, so the backward edges that line L8 creates also have reduced cost 0. Vertices that $s$ does not reach keep their potentials; they stay unreachable for the rest of the run. The real cost of $P$ is $\pi(t) - \pi(s)$ after line L6.

## Example

The network has the edges, with (capacity, cost): $s \to a$ (3, 1), $s \to b$ (2, 4), $a \to b$ (2, 1), $a \to t$ (2, 5), $b \to t$ (3, 1), and $d = \infty$. All costs are nonnegative, so line L2 gives $\pi = 0$. The potentials are listed in the order $s, a, b, t$, after line L6.

| round | $\pi$ | path | cost per unit | $\delta$ | value | total cost |
|---|---|---|---|---|---|---|
| 1 | 0, 1, 2, 3 | $s, a, b, t$ | 3 | 2 | 2 | 6 |
| 2 | 0, 1, 4, 5 | $s, b, t$ | 5 | 1 | 3 | 11 |
| 3 | 0, 1, 4, 6 | $s, a, t$ | 6 | 1 | 4 | 17 |
| 4 | 0, 3, 4, 8 | $s, b, a, t$ | 8 | 1 | 5 | 25 |
| 5 | | none | | | 5 | 25 |

Round 4 uses the backward residual edge $b \to a$ of cost $-1$: it moves one unit off $a \to b$. The costs per unit, 3, 5, 6, 8, never go down, and each partial flow is the cheapest of its value (checked by exhaustive search). The final flow on $sa, sb, ab, at, bt$ is $3, 2, 1, 2, 3$.

Edge cases. An extra edge $s \to t$ of capacity 0 and cost $-100$ has no residual edge and never carries flow. With only $s \to a$ and $b \to t$, line L5 stops at once with the zero flow.

## Correctness

The invariant is: before each round, $c^{\pi}(v, w) \ge 0$ for every residual edge $(v, w)$ with $v$ reachable from $s$ in $G_x$, and $x$ is a cheapest flow of its value. Line L6 preserves the first part because shortest distances satisfy $\mathrm{dist}(w) \le \mathrm{dist}(v) + c^{\pi}(v, w)$, and edges of $P$ hold this with equality, so their reverses also get reduced cost 0. Nonnegative reduced costs mean no negative cycle in $G_x$, and a flow with no negative residual cycle is a cheapest flow of its value by the negative cycle optimality theorem. The proof file below gives the details, including the vertices that $s$ cannot reach.

## Complexity

The model is the [word RAM](/word-ram/) with numbers that fit in a word.

- **Start.** Bellman-Ford over $n + 1$ vertices: $O(nm)$.
- **One round.** Dijkstra with a [binary heap](/binary-heap/): $O(m \log n)$; or $O(m + n \log n)$ with a [Fibonacci heap](/fibonacci-heap/).
- **Rounds.** With integer capacities, each $\delta \ge 1$, so there are at most $F$ rounds for a flow of value $F$. Each round also either saturates an edge or reaches $d$, which does not bound the count by a polynomial: the method is pseudo-polynomial.
- **Total.** $O(nm + F m \log n)$ time and $\Theta(n + m)$ extra space.

On the [assignment problem](/assignment-problem/) with $n$ workers, $F = n$ and the time is $O(n (m + n \log n))$ with a Fibonacci heap; this is the [Hungarian algorithm](/hungarian-algorithm/) in this form.

## Properties

- **Each partial flow is optimal.** After round $k$, $x$ is a cheapest flow of value $|x|$. So the run gives the whole cost curve, which is convex and piecewise linear in the value.
- **Path costs do not decrease.** The cost per unit of the augmenting paths is nondecreasing, because $\pi(t)$ only grows.
- **Integral.** With integer capacities and $d$ an integer or $\infty$, every $\delta$ is an integer, so the flow is integral, whatever the costs.
- **Potentials are dual variables.** At the end, $\pi$ and $x$ satisfy the reduced cost optimality conditions, an LP dual certificate.

## Variants and improvements

- **Capacity scaling.** Augment only along paths with room at least $\Delta$, halving $\Delta$; this gives $O(m \log U (m + n \log n))$ with integer data (Edmonds and Karp).
- **Primal-dual.** After computing $\pi$, send a whole maximum flow in the subgraph of residual edges of reduced cost 0, instead of one path.
- **General supplies.** For supplies $b(v)$ at many vertices, add a super-source and a super-sink, or choose any excess vertex and any deficit vertex in each round.
- **Without Dijkstra.** Using Bellman-Ford in every round avoids the potentials, at $O(nm)$ per round.
- **Strongly polynomial methods.** Orlin's algorithm builds on scaling and successive shortest paths; see the [min-cost flow problem](/min-cost-flow-problem/).

## When to use it

Use it when the flow value $F$ is small, as in assignment problems, $k$ disjoint paths of least cost, or min-cost bipartite matching. It is short to code and gives the cost of every intermediate value. For large capacities use capacity scaling, [cost scaling](/cost-scaling/) or the [network simplex method](/network-simplex/).

## Pitfalls

- **Negative costs without the first Bellman-Ford.** Dijkstra needs nonnegative lengths. Line L2 gives potentials that make them so; skipping it breaks the method on negative costs.
- **A negative cycle in the input.** Then no potentials exist, and even the zero flow is not optimal. Line L2 must detect it.
- **Forgetting backward edges or their negated costs.** Round 4 of the example needs $b \to a$ with cost $-1$.
- **Merging antiparallel edges.** Edges $(v, w)$ and $(w, v)$ with their own costs must stay separate residual pairs; merging them adds their capacities with the wrong costs.
- **Updating the potentials of unreached vertices.** Their distance is $\infty$; adding it corrupts $\pi$. Line L6 skips them.
- **Treating the time as polynomial.** The number of rounds grows with the flow value, not with $n$ and $m$.

## Implementations

## History

The method of augmenting along cheapest paths goes back to work on transportation problems in the 1950s by Jewell, Busacker and Gowen, and others, as recorded in the chapter notes of Ahuja, Magnanti and Orlin. Edmonds and Karp (1972), and independently Tomizawa, used vertex potentials to keep edge lengths nonnegative, so that each shortest path is a run of Dijkstra's algorithm; Edmonds and Karp also added capacity scaling for a polynomial bound.

## References
