---
tag: SJBDWT
kind: algorithm
slug: network-simplex
name: Network simplex method
aliases:
- network simplex
area: graphs/flows-and-cuts
level: advanced
summary: Simplex method specialized to min-cost flow, pivoting over spanning tree bases.
solves: [min-cost-flow-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, P: the number of pivots}
  time: {worst: O(P (n + m))}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [min-cost-flow-problem, simplex-method, spanning-tree, reduced-cost]
see_also: [successive-shortest-path, cycle-canceling, cost-scaling, big-m-method, lp-duality, complementary-slackness, assignment-problem, flow-decomposition]
sources:
  - paper: doi:10.1007/BF01580379
    title: William H. Cunningham, A network simplex method, Mathematical Programming 11(1), 105 to 116 (1976)
    locator: the whole paper (strongly feasible trees, the rule for the leaving edge, and finiteness without cycling)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 11, Minimum Cost Flows, Network Simplex Algorithms (spanning tree solutions, potentials, pivots, strongly feasible spanning trees)
  - paper: doi:10.1007/BF02614365
    title: James B. Orlin, A polynomial time primal network simplex algorithm for minimum cost flows, Mathematical Programming 78(2), 109 to 129 (1997)
    locator: the whole paper (a pivot rule with a polynomial number of pivots)
---

The network simplex method solves the [minimum-cost flow problem](/min-cost-flow-problem/) by running the [simplex method](/simplex-method/) on its linear program, with every step done on the graph. A basic solution is a [spanning tree](/spanning-tree/) of the network: the tree edges carry any flow, and every other edge is empty or full. The tree fixes vertex potentials, and from them each edge gets a [reduced cost](/reduced-cost/). If some non-tree edge has a reduced cost of the wrong sign, adding it to the tree closes one cycle; the method pushes as much flow as possible around that cycle, and a blocked edge of the cycle leaves the tree. When no edge has the wrong sign, the flow is optimal. Keeping a *strongly feasible* tree, with Cunningham's rule for the leaving edge, prevents cycling. Each pivot costs $O(n + m)$ here and $O(n)$ with careful tree updates; the number of pivots can be exponential for simple rules, but the method is among the fastest in practice.

## In plain words

Goods must move from some places to others through roads with limits and prices per unit. Start with a plan that uses a backbone of roads, a tree that touches every place, and keeps every other road either unused or full.

The backbone sets a price for each place: what it costs to bring one unit there along the backbone. Now look at a road off the backbone. If using it is cheaper than the backbone route between its ends, or emptying a full road would save money, then shifting goods around the loop that this road makes with the backbone lowers the cost. Shift as much as possible. Some road on the loop becomes empty or full; it leaves the backbone, and the new road joins it. Repeat until no road off the backbone can save anything.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a capacity $u(e) \ge 0$ and a cost $c(e)$ of any sign on each edge, integer or real, and a supply $b(v)$ at each vertex, with $b(v) < 0$ for a demand. A flow $x$ is feasible if $0 \le x(e) \le u(e)$ and, at each vertex, the flow out minus the flow in is $b(v)$. The output is a feasible flow of least cost $\sum_e c(e) x(e)$, or the report that none exists. Parallel and antiparallel edges are separate variables, never merged. A self-loop of negative cost is filled to capacity, and one of nonnegative cost stays empty. An edge of capacity 0 is fixed at 0 and never enters the tree. An $s$-$t$ flow of value $d$ is the case $b(s) = d$, $b(t) = -d$; if $t$ is not reachable from $s$ and $d > 0$, there is no feasible flow. Since all capacities are finite, the problem is never unbounded.

## The algorithm

Add a root $r$ and, for each vertex $v$, an *artificial* edge of cost $M$ and unlimited capacity: $v \to r$ carrying $b(v)$ if $b(v) \ge 0$, and $r \to v$ carrying $-b(v)$ otherwise. These $n$ edges form the first tree, and all real edges start empty. With $C$ the largest $|c(e)|$, the implementation takes $M = (C + 1)(n + 1)$, large enough that an optimum uses an artificial edge only when no feasible flow exists.

For a tree $T$, the potentials $\pi$ satisfy $\pi(r) = 0$ and $c(e) + \pi(u) - \pi(v) = 0$ on each tree edge $e = (u, v)$. The reduced cost of any edge is $c^{\pi}(e) = c(e) + \pi(u) - \pi(v)$. A non-tree edge is *eligible* if it is empty with $c^{\pi}(e) < 0$, or full with $c^{\pi}(e) > 0$.

```pseudo id=main
NETWORK-SIMPLEX(G, u, c, b)
L1  add the root r and the artificial edges; T ← the artificial edges, with their flows
L2  repeat
L3      compute the potentials π of T and the reduced costs
L4      e ← the eligible edge with the largest |c^π(e)|; if there is none, leave the loop
L5      W ← the cycle of T + e, oriented along e if e is empty and against e if it is full; w ← the apex, where the two tree paths from the ends of e meet
L6      δ ← the least residual capacity along W; f ← the last edge with residual δ met when walking W in its orientation from w
L7      push δ units around W
L8      T ← T − f + e
L9  if an artificial edge carries flow then return "infeasible"
L10 return the flow on the real edges and its cost
```

A tree is *strongly feasible* if every vertex can send a positive amount of flow to $r$ along its tree path. The first tree is strongly feasible, and the rule for $f$ at line L6 keeps it so; this is what prevents cycling. When $e$ itself is the last blocking edge, it stays out of the tree and only moves from empty to full or back.

## Example

The network has the vertices $s, a, b, t$ and the edges $s \to a$ (capacity 3, cost 1), $s \to b$ (2, 4), $a \to b$ (2, 1), $a \to t$ (2, 5), $b \to t$ (3, 1), with $b(s) = 4$ and $b(t) = -4$. Here $C = 5$ and $M = 30$. The first tree is $s \to r$ (flow 4), $a \to r$ (0), $b \to r$ (0) and $r \to t$ (4), with potentials $\pi(s) = \pi(a) = \pi(b) = -30$, $\pi(t) = 30$.

| pivot | entering, reduced cost | cycle in its orientation | $\delta$ | leaving |
|---|---|---|---|---|
| 1 | $b \to t$, $-59$ | $r b$, $b t$, $t r$ | 0 | $b \to r$ |
| 2 | $a \to b$, $-58$ | $r a$, $a b$, $b t$, $t r$ | 0 | $a \to r$ |
| 3 | $s \to a$, $-57$ | $r s$, $s a$, $a b$, $b t$, $t r$ | 2 | $a \to b$, now full |
| 4 | $s \to b$, $-55$ | $r s$, $s b$, $b t$, $t r$ | 1 | $b \to t$, now full |
| 5 | $a \to t$, $-54$ | $r s$, $s a$, $a t$, $t r$ | 1 | $r \to t$ |

The cycles are written as the walk from the apex $r$; an artificial edge walked against its direction, such as $r b$ for the edge $b \to r$, loses flow. Pivots 1 and 2 are degenerate: they move no flow, but they change the tree and raise potentials. After pivot 5 the artificial edges are empty. The tree is $s \to r$, $s \to a$, $s \to b$, $a \to t$, with $\pi = (-30, -29, -26, -24)$ for $s, a, b, t$; the full edges $a \to b$ and $b \to t$ have reduced costs $-2$ and $-1$, so none is eligible. The flow is $s a = 3$, $s b = 1$, $a b = 2$, $a t = 1$, $b t = 3$, of cost 17, which matches the [successive shortest path](/successive-shortest-path/) result for value 4.

Edge cases. With $b(s) = 6$, which exceeds the cut $\{s\}$ of capacity 5, the method ends with flow on an artificial edge and reports infeasible. An edge of capacity 0 never enters. If $t$ is not reachable from $s$, the artificial edges stay in use and the answer is infeasible, unless $b = 0$.

## Correctness

At the end no edge is eligible: tree edges have reduced cost 0, empty edges have $c^{\pi} \ge 0$, and full edges have $c^{\pi} \le 0$. These are the [complementary slackness](/complementary-slackness/) conditions of the flow LP, and for any other feasible flow $y$ of the extended network, $c(y) - c(x) = \sum_e c^{\pi}(e)(y(e) - x(e)) \ge 0$, so $x$ is optimal there. If a feasible flow $z$ of $G$ exists, then $x - z$ splits into cycles, and any cycle through $r$ uses two artificial edges, so it costs at least $2M - (n - 1) C > 0$; removing such cycles from $x$ would lower its cost, so an optimal $x$ uses no artificial edge. Termination: a pivot with $\delta > 0$ lowers the cost strictly. In a degenerate pivot, strong feasibility puts the leaving edge between the apex and the start of $e$, and the potentials of the part of the tree that moves rise by $|c^{\pi}(e)| > 0$, while the others stay fixed. So the pair (cost, minus the sum of potentials) falls strictly in every pivot, no tree repeats, and the method stops. The proof file below gives all steps, including why line L6 keeps the tree strongly feasible.

## Complexity

The model is the [word RAM](/word-ram/); arithmetic on capacities and costs takes constant time.

- **One pivot.** Computing the potentials, pricing all $m$ edges and walking the cycle take $O(n + m)$ in the implementation. Real codes keep the tree in parent, depth and thread arrays and update only the moved subtree, so the tree part costs $O(n)$ or less, and they price only a block of candidate edges per pivot.
- **Number of pivots.** With the most violating edge (Dantzig's rule), the count can be exponential in $n$ on special networks; in practice it is far smaller. Orlin gave a rule with a polynomial number of pivots.
- **Total.** $O(P(n + m))$ for $P$ pivots. Space is $\Theta(n + m)$.

## Properties

- **Integrality.** With integer capacities and supplies, every basic solution is integral, so the result is an integral optimal flow.
- **Dual solution for free.** The final potentials are an optimal dual solution, a certificate of optimality.
- **Negative costs.** Negative costs and negative cycles need no special care, since capacities are finite.
- **Warm starts.** After a small change of costs or capacities, the old tree is a good start, which helps in branch and bound and in sensitivity analysis.

## Variants and improvements

- **Pricing rules.** First eligible edge, block search over a rotating window of edges, or candidate lists; block search is the default in common libraries.
- **Two-phase start.** Instead of big $M$, first minimize the artificial flow, then the real cost; this is the two-phase simplex method on the graph.
- **Polynomial rules.** Orlin's primal rule bounds the number of pivots by a polynomial in $n$, $m$ and $\log C$.
- **Special cases.** For the [assignment problem](/assignment-problem/) and transportation problems, the trees have special shapes and the method becomes the classical stepping-stone method.

## When to use it

Use it for medium and large minimum-cost flow problems in practice, where it is often the fastest exact method together with [cost scaling](/cost-scaling/), and when the optimal potentials or warm starts are needed. When a strongly polynomial worst-case bound matters, prefer Orlin's algorithm or cost scaling; for small integer flow values, [successive shortest paths](/successive-shortest-path/) is simpler.

## Pitfalls

- **Cycling on degenerate pivots.** Any choice of leaving edge among the blocking ones can cycle. Keep a strongly feasible tree and take the last blocking edge from the apex.
- **Too small $M$.** If $M$ is not larger than the cost of any path through the network, an optimal solution may keep flow on artificial edges and the method reports a false "infeasible". Use $M > (n - 1) C / 2$ at least, or a two-phase start.
- **Sign of the reduced cost for full edges.** A full edge is eligible when $c^{\pi}(e) > 0$, and its cycle is oriented against it.
- **Unbalanced supplies.** If $\sum_v b(v) \ne 0$, no flow is feasible; check this first, or add a dummy vertex for the excess.
- **Rounding with real data.** With floating-point costs, a reduced cost of $-10^{-15}$ can make the method pivot forever; compare with a tolerance or use exact arithmetic.

## Implementations

## History

Dantzig specialized the simplex method to the transportation problem in 1951 and later to general network flows. Cunningham introduced strongly feasible trees in 1976 and showed that they prevent cycling. Many fast codes followed from the 1970s on. Orlin gave the first primal network simplex rule with a polynomial number of pivots, published in 1997.

## References
