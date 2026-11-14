---
tag: V8CQHN
kind: algorithm
slug: negotiated-congestion-routing
name: Negotiated congestion routing
aliases:
- PathFinder
area: eda/routing
level: core
summary: McMurchie and Ebeling's router that reroutes all nets each round with costs raised on resources by present and past overuse, until no resource is shared.
solves: [global-routing]
model: word-ram
complexity:
  vars: {I: the number of iterations, m: the number of nets, P: the number of pins, V: the number of gcells, E: the number of grid edges}
  time: {worst: O(I (P E log V + m E))}
  space: {extra: O(E + m V)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1995
  people: [Larry McMurchie, Carl Ebeling]
  note: McMurchie and Ebeling presented PathFinder for FPGA routing at FPGA '95. It reroutes every net in every iteration, as in Nair's global router of 1987, and adds a history cost of past overuse. Global routers such as NTHU-Route 2.0 (2008) later used the same cost scheme on gcell grids.
prereqs: [global-routing, dijkstra, rip-up-and-reroute]
see_also: [rip-up-and-reroute, lee-maze-routing, a-star-search, pattern-routing, multicommodity-flow-global-routing, lagrangian-relaxation, static-timing-analysis, detailed-routing]
sources:
  - paper: doi:10.1145/201310.201328
    title: Larry McMurchie and Carl Ebeling, PathFinder, a negotiation-based performance-driven router for FPGAs, Proceedings of the ACM Symposium on Field-Programmable Gate Arrays (FPGA '95), 111 to 117, 1995
    locator: the cost of a node (b + h) p, the update of the history term, the growth of the present sharing factor and the timing term with criticality
  - paper: doi:10.1109/ICCAD.2008.4681595
    title: Yen-Jung Chang, Yu-Ting Lee and Ting-Chi Wang, NTHU-Route 2.0, a fast and stable global router, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 338 to 343, 2008
    locator: the history-based cost function for rip-up and reroute on a gcell grid, and the results on the ISPD 2008 benchmarks
  - paper: doi:10.1109/TCAD.2010.2061590
    title: Yen-Jung Chang, Yu-Ting Lee, Jhih-Rong Gao, Pei-Ci Wu and Ting-Chi Wang, NTHU-Route 2.0, a robust global router for modern designs, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 29(12), 1931 to 1944, 2010
    locator: the journal version, with the cost scheme and the experiments (general locator)
  - paper: "Ravi Nair, A simple yet effective technique for global wiring, IEEE Transactions on Computer-Aided Design CAD-6(2), 165 to 172, 1987"
    locator: the rerouting of every net in each pass with the other nets in place (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 5, Section 5.8 Modern Global Routing (negotiated congestion routing; general locator)
---

Negotiated congestion routing, introduced by McMurchie and Ebeling as the PathFinder router, is a form of [rip-up and reroute](/rip-up-and-reroute/) for [global routing](/global-routing/) and FPGA routing. In each iteration it rips up and reroutes every net with a shortest path search such as [Dijkstra's algorithm](/dijkstra/). The cost of a resource is its base cost plus a *history* term that grows each time the resource is overused, times a *present* term that grows with the number of other nets on it now. Early iterations let nets share resources cheaply. Later iterations make sharing expensive, so the nets with good alternatives move away and the net that needs a resource most keeps it. There is no general proof that the loop reaches a legal routing; its success is measured on benchmarks.

## In plain words

Imagine many drivers who all want the best roads. In the first round, each driver takes the shortest way and ignores the others, so some roads get too many cars.

Then every driver plans again, one after the other. A road that is too full now costs more, and a road that was too full in earlier rounds also costs more, as a memory of past jams. A driver with a good second road takes it. A driver with no other choice pays the price and stays.

Round after round the penalty for crowding grows, until each road carries no more cars than it can hold. The drivers do not talk to each other: they only react to the prices, so the price of each road sets who gets it.

## The problem

The input is a global routing grid $G = (V, E)$ with an integer capacity $c_e$ on each edge, and $m$ nets, where net $i$ has a set $T_i$ of terminal gcells with $|T_i| \ge 2$ and $P = \sum_i |T_i|$. The output is a route $R_i$ for each net, a tree in $G$ that holds all of $T_i$ and whose leaves are terminals. The usage of edge $e$ is $u_e = |\{ i : e \in R_i \}|$. The goal is a legal routing, $u_e \le c_e$ for all $e$, with small wirelength $\sum_i |R_i|$. When no legal routing is found, the goal is the least total overflow $\sum_e \max(0, u_e - c_e)$. The exact definitions are on the [global routing](/global-routing/) page.

PathFinder works on the routing-resource graph of an FPGA, where the resources are the nodes (wire segments and pins) and each node has capacity 1. This page puts the capacities on the edges of a gcell grid, the form that global routers use. The algorithm is the same.

## The algorithm

The cost of edge $e$ when a net is routed is

$$\mathrm{cost}(e) = (b_e + h_e) \cdot p_e, \qquad p_e = 1 + \mathrm{pres\_fac} \cdot \max(0,\ u_e + 1 - c_e),$$

where $u_e$ counts the other nets on $e$ at that moment. Here $b_e$ is the base cost (1 on this page), $h_e$ is the history cost and $p_e$ is the present congestion penalty: it is 1 when one more net still fits on $e$, and it grows with the overflow that this net would cause.

```pseudo id=main
NEGOTIATED-CONGESTION(G, c, nets T_1..T_m)
L1  h_e ← 0 for every edge e;  pres_fac ← pres_first
L2  for it ← 1 to max_iters do
L3      for i ← 1 to m do
L4          rip up R_i:  u_e ← u_e − 1 for each e in R_i
L5          cost(e) ← (b_e + h_e) · (1 + pres_fac · max(0, u_e + 1 − c_e)) for each e
L6          R_i ← ROUTE-TREE(T_i, cost)
L7          u_e ← u_e + 1 for each e in R_i
L8      record the routing if it is the best so far;  if no edge has u_e > c_e then stop
L9      h_e ← h_e + hist_fac · max(0, u_e − c_e) for each e
L10     pres_fac ← pres_init if pres_fac = 0, else pres_fac · pres_mult
L11 return the best routing recorded
```

$\textsc{Route-Tree}(T_i, \mathrm{cost})$ grows a tree from one terminal. At each step it runs Dijkstra's algorithm with all tree gcells as sources at distance 0, stops at the nearest terminal that is not yet in the tree, and adds the path to that terminal. This is the expansion of PathFinder for one sink at a time. The defaults of the implementation are $\mathrm{pres\_first} = 0$, $\mathrm{pres\_init} = 1/2$, $\mathrm{pres\_mult} = 3/2$ and $\mathrm{hist\_fac} = 1$, all as exact fractions. With $\mathrm{pres\_first} = 0$ the first iteration routes every net by its cheapest tree and ignores the other nets.

## Example

Take a $3 \times 3$ grid of gcells $(x, y)$ with capacity 1 on each of its 12 edges. Net A joins $(1,0)$ and $(0,1)$. Net B joins $(0,0)$ and $(2,2)$. Ties in Dijkstra's algorithm go to the gcell with the lower index $3y + x$.

**Iteration 1.** $\mathrm{pres\_fac} = 0$ and $h = 0$, so every edge costs 1.

- A has two routes of cost 2. The tie goes to the route through the corner, on the edges $(1,0)(0,0)$ and $(0,0)(0,1)$.
- B takes $(0,0)$, $(1,0)$, $(2,0)$, $(2,1)$, $(2,2)$, of cost 4.

The edge $(0,0)(1,0)$ carries both nets: total overflow 1, wirelength 6. Line L9 sets $h = 1$ on that edge, and line L10 sets $\mathrm{pres\_fac} = 1/2$.

**Iteration 2.** Rip up A. B is on its 4 edges, so each of them has $u_e + 1 - c_e = 1$ and $p_e = 3/2$.

| edge | $b + h$ | $p$ | cost |
| --- | --- | --- | --- |
| $(0,0)(1,0)$ | 2 | 3/2 | 3 |
| other edges of B | 1 | 3/2 | 3/2 |
| all other edges | 1 | 1 | 1 |

The corner route of A now costs $3 + 1 = 4$, and the route through the center, on $(1,0)(1,1)$ and $(1,1)(0,1)$, costs 2. A moves to the center. Then rip up B. Its old route costs $2 + 1 + 1 + 1 = 5$, since the history term stays on $(0,0)(1,0)$. The route up the left column and along the top row costs 4, and every route through the edges of A costs at least $4 + 1/2$. B moves to $(0,0)$, $(0,1)$, $(0,2)$, $(1,2)$, $(2,2)$.

Now no edge is overflowed, and the loop stops after 2 iterations with wirelength 6. An exhaustive search over all $8 \cdot 12 = 96$ pairs of routes gives the same least wirelength for a legal routing. A single pass of sequential routing in the order A, B, where B avoids full edges when it can, ends with overflow 1: B has no free edge out of the corner. The order B, A works. Negotiation finds a legal routing here without a choice of order.

## Correctness

The [proof](proofs/correctness.md) shows the following. It does not show that the loop reaches a legal routing, because that is not true in general.

- **Valid trees.** $\textsc{Route-Tree}$ returns a tree that holds all terminals of the net, and every leaf is a terminal.
- **Cheapest step.** Each step of $\textsc{Route-Tree}$ adds a cheapest path, under the current costs, from the tree to the nearest unreached terminal. All costs are at least $b_e > 0$, so Dijkstra's algorithm applies.
- **Exact usage.** After line L7, $u_e$ is the number of nets whose route contains $e$.
- **Legal on early stop.** If the loop stops at line L8, the returned routing has no overflow. In every case it returns the routing with the least total overflow, then the least wirelength, of all iterations.
- **Growing penalties.** $h_e$ never decreases, and it grows by at least $\mathrm{hist\_fac}$ in each iteration that ends with $e$ overflowed. $\mathrm{pres\_fac}$ never decreases after the first iteration.
- **Termination.** The loop runs at most $\mathrm{max\_iters}$ iterations, and each call of $\textsc{Route-Tree}$ makes at most $|T_i| - 1$ searches.

## Complexity

- **One search.** Dijkstra's algorithm with a binary heap takes $O(E \log V)$ time on the grid.
- **One net.** $\textsc{Route-Tree}$ adds at least one terminal per search, so it makes at most $|T_i| - 1$ searches. Line L5 computes all edge costs in $O(E)$ time. A router can update only the costs of the edges whose usage changed.
- **One iteration.** Over all nets there are at most $P - m$ searches, so an iteration takes $O(P E \log V + m E)$ time. Lines L9 and L10 take $O(E)$.
- **Whole run.** $O(I (P E \log V + m E))$ for $I$ iterations. The number of iterations is not bounded by any proved function of the input; it is a parameter.
- **Space.** $O(E)$ for the costs, the usage and the history, and $O(m V)$ for the routes, since each tree has fewer than $V$ edges.

## Properties

- **What is proved.** Each net gets a valid tree, each search step is a cheapest path for the current costs, the usage counts are exact, a stop at line L8 means a legal routing, and the run ends after at most $\mathrm{max\_iters}$ iterations.
- **What is not proved.** There is no general proof that negotiated congestion reaches a legal routing when one exists, or that it reaches the least overflow. On the $2 \times 2$ grid with capacity 1 and two nets between opposite corners, no legal routing exists, and the loop runs to its limit with overflow 1.
- **What is measured.** NTHU-Route 2.0, built on this cost scheme, won the ISPD 2008 global routing contest, and its authors report routing 12 of the 16 ISPD 2008 benchmarks with no overflow. On 300 random toy instances made by the implementation's test generator with seed 2 (a $3 \times 3$ grid, capacities drawn from 0, 1, 1, 2, and 2 or 3 nets), an exhaustive search found a legal routing for 141 of them. The implementation found a legal routing for all 141 within 30 iterations, and the least wirelength for 135. These are results on toy inputs, not benchmark results.
- **Deterministic.** With exact costs and a fixed order of nets and ties, a run always gives the same routing.
- **Order of nets.** The order still matters inside an iteration, but much less than in a single pass, because every net is rerouted in each iteration with the costs left by the others.
- **Relation to Lagrangian methods.** The history term acts like a price on each edge that rises while the edge is overused, close in spirit to the multipliers of [Lagrangian relaxation](/lagrangian-relaxation/). This is an analogy, not a proof of convergence.

## Variants and improvements

- **Timing-driven cost.** PathFinder routes the connection from a source to sink $j$ with the cost $A_{ij} d_n + (1 - A_{ij}) c_n$ of resource $n$, where $d_n$ is its delay, $c_n$ is the congestion cost above and $A_{ij} \in [0, 1]$ is the criticality of the connection from [static timing analysis](/static-timing-analysis/). Critical connections take fast resources even when they are crowded.
- **Other cost forms.** Some later routers multiply the base cost, the history cost and the present penalty instead of adding the first two, or they use an exponential present penalty. NTHU-Route 2.0 uses a history-based cost on a gcell grid with further changes of its own.
- **Search with a target.** Replace Dijkstra's algorithm by [A* search](/a-star-search/) with the Manhattan distance to the target as the estimate, which visits fewer gcells.
- **Partial rip-up.** Reroute only the nets that use an overflowed edge, not every net. This is faster per iteration, and global routers often do it after the first iterations.
- **Patterns first.** Start from [pattern routing](/pattern-routing/), then negotiate only on the connections that still overflow.
- **Fractional start.** Start from the rounded solution of [multicommodity flow routing](/multicommodity-flow-global-routing/) and negotiate away the overflow that the rounding leaves.

## When to use it

- FPGA routing, where every resource has capacity 1 and a legal routing is required.
- Global routing of large netlists, where overflow must reach zero and a strong single-net search is available.
- As the repair stage after a fast first routing, such as pattern routing or the rounding of a fractional solution.

When the run must have a proved bound, use the fractional method of [multicommodity flow routing](/multicommodity-flow-global-routing/), whose fractional solution has a proved approximation ratio.

## Pitfalls

- **Present penalty too large too soon.** If $\mathrm{pres\_fac}$ is large in the first iteration, the first nets take the good resources and the later nets are pushed away, as in a single sequential pass. The usual schedule starts at 0 or at a small value and grows by a constant factor.
- **No history.** Without the history term, two nets can trade the same two routes in every iteration.
- **Counting the current net.** The present penalty must use the usage without the current net, which is why line L4 rips up the net before line L5 computes the costs. Otherwise a net pays for its own old route.
- **Shared edges inside one net.** A tree uses each edge at most once, so a net adds 1 to the usage of an edge even when two of its connections pass there.
- **Unbounded history.** In a long run the history terms grow without limit and dominate the base cost, so the routes get long. Routers bound the number of iterations, scale the history term or reset it.
- **Expecting a proof.** The results are measured, not proved. A claim that the method "converges" holds only for the instances on which it was run.

## Implementations

## History

Ravi Nair described in 1987 a global router that rerouted every net in turn, with all others in place, over several passes. Larry McMurchie and Carl Ebeling presented PathFinder at FPGA '95. They added the history cost of past overuse to the present sharing cost, and gave the timing-driven form with criticality. PathFinder became the base of FPGA routers. For chip global routing, NTHU-Route 2.0 by Chang, Lee and Wang used a history-based cost on the gcell grid and won the ISPD 2008 global routing contest, and later global routers kept the same scheme.

## References
