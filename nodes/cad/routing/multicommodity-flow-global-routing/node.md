---
tag: 6WN748
kind: algorithm
slug: multicommodity-flow-global-routing
name: Multicommodity flow global routing
aliases:
- Albrecht global routing
area: cad/routing
level: advanced
summary: Global routing as fractional multicommodity flow, solved approximately by multiplicative length updates over shortest paths, then rounded to one route per net.
solves: [global-routing]
model: word-ram
complexity:
  vars: {T: the number of rounds, k: the number of nets, V: the number of gcells, E: the number of grid edges}
  time: {worst: O(T k E log V)}
  space: {extra: O(E + T k V)}
properties: {deterministic: false, recursive: false, exact: false}
history:
  year: 2001
  people: [Christoph Albrecht]
  note: Raghavan and Thompson (1987) solved the linear relaxation of global wiring and rounded it at random. Albrecht (ISPD 2000, IEEE TCAD 2001) made this practical for chip global routing with an approximation algorithm for the fractional problem based on the method of Garg and Könemann with extensions by Fleischer.
prereqs: [global-routing, multi-commodity-flow-problem, multiplicative-weights-update, randomized-rounding]
see_also: [negotiated-congestion-routing, rip-up-and-reroute, lp-relaxation, integrality-gap, weak-duality, dijkstra, packing-integer-program, lagrangian-relaxation]
sources:
  - paper: "Christoph Albrecht, Global routing by new approximation algorithms for multicommodity flow, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 20(5), 622 to 632, 2001"
    locator: the approximation algorithm for the fractional global routing problem, based on the method of Garg and Könemann with Fleischer's extensions, and the rounding to one route per net (general locator)
  - paper: "Christoph Albrecht, Provably good global routing by a new approximation algorithm for multicommodity flow, Proceedings of the International Symposium on Physical Design (ISPD), 19 to 25, 2000"
    locator: the conference version (general locator)
  - paper: doi:10.1137/S0097539704446232
    title: Naveen Garg and Jochen Könemann, Faster and simpler algorithms for multicommodity flow and other fractional packing problems, SIAM Journal on Computing 37(2), 630 to 652, 2007
    locator: the length-function method, with multiplicative length updates along shortest paths and the dual bound
  - paper: doi:10.1007/BF02579324
    title: Prabhakar Raghavan and Clark D. Thompson, Randomized rounding, a technique for provably good algorithms and algorithmic proofs, Combinatorica 7(4), 365 to 374, 1987
    locator: the 0-1 multicommodity flow form of global wiring, its linear relaxation and the bound after randomized rounding
  - paper: doi:10.4086/toc.2012.v008a006
    title: Sanjeev Arora, Elad Hazan and Satyen Kale, The multiplicative weights update method, a meta-algorithm and applications, Theory of Computing 8, 121 to 164, 2012
    locator: the multiplicative weights method for packing and covering linear programs with an oracle, and the role of the width
---

Multicommodity flow global routing solves the [LP relaxation](/lp-relaxation/) of [global routing](/global-routing/), in which each net may split over several routes, and then rounds it to one route per net. The relaxation is a fractional [multicommodity flow](/multi-commodity-flow-problem/) that minimizes the congestion $\lambda$, the largest ratio of usage to capacity. This page solves it with [multiplicative weights](/multiplicative-weights-update/): each edge has a weight, each net takes a shortest route under lengths proportional to the weights, and the weights of the edges that the routes use grow by a factor. The average of the rounds is within a factor $1 + \varepsilon$ of the fractional optimum, up to an additive term that falls as $1/T$ in the number of rounds $T$, and each round also gives a proved lower bound. [Randomized rounding](/randomized-rounding/) then picks one route per net, and [rip-up and reroute](/rip-up-and-reroute/) removes the overflow that remains.

## In plain words

Suppose every net could split into many thin wires that take different roads. Then the best plan is easy to compute well, and it tells you how crowded the chip must be at least.

The method finds such a plan by playing many rounds. Each road has a price. In each round, every net takes its cheapest road. Then each road that was used gets a little more expensive, more so when many nets used it. Over many rounds, the nets spread over the roads, and the share of rounds in which a net took a road becomes the fraction of that net on it.

At the end, each net must take one real road. It draws one at random, with the chance of each road equal to its share. A few roads may then be too full, and a repair step moves some nets away.

## The problem

Let $G = (V, E)$ be the routing graph with capacities $c_e > 0$, and let there be $k$ nets. Net $i$ has a set $\mathcal{R}_i$ of routes: all paths between its two pins, or a given list of candidate trees. The fractional problem is

$$\lambda^* = \min \lambda \quad \text{subject to} \quad \sum_{P \in \mathcal{R}_i} x_{iP} = 1 \ (\text{each net } i), \qquad x \ge 0, \qquad \sum_i \sum_{P \in \mathcal{R}_i,\ P \ni e} x_{iP} \le \lambda c_e \ (\text{each edge } e).$$

It is a linear program with one variable per route, which can be exponentially many, so the method only touches routes through an *oracle* that returns a shortest route of a net for given edge lengths. For two-pin nets the oracle is [Dijkstra's algorithm](/dijkstra/). The integral problem, with each $x_{iP} \in \{0, 1\}$, is the minimum congestion form of global routing, and $\lambda^* \le \lambda_{\mathrm{int}}$.

## The algorithm

The width is $\rho = k / \min_e c_e$. No edge carries more than $k$ nets, so $\mathrm{load}_e / (\rho c_e) \le 1$ in every round. The step size $\varepsilon \in (0, 1]$ is a parameter.

```pseudo id=main
MCF-GLOBAL-ROUTE(G, c, nets, ε, T)
L1  w_e ← 1 for every edge e;  ρ ← k / min_e c_e;  LB ← 0
L2  for t ← 1 to T do
L3      ℓ_e ← w_e / (W c_e) for every e, where W = Σ_e w_e
L4      for each net i:  P_i ← a shortest route of net i under ℓ   (the oracle)
L5      count(i, P_i) ← count(i, P_i) + 1 for each i;  load_e ← |{ i : e ∈ P_i }|
L6      LB ← max(LB, Σ_e ℓ_e · load_e)
L7      w_e ← w_e · (1 + ε · load_e / (ρ c_e)) for every e
L8  x_iP ← count(i, P) / T;   λ_frac ← max_e (Σ_i Σ_{P ∋ e} x_iP) / c_e
L9  for each net i, independently:  pick one route P with probability x_iP
L10 return x, λ_frac, LB and the picked routes
```

Lines L2 to L7 are the fractional solver. The lengths of line L3 satisfy $\sum_e \ell_e c_e = 1$, so the value of line L6 is a lower bound on $\lambda^*$ by [weak duality](/weak-duality/). Line L8 averages the routes of the $T$ rounds. Line L9 is the rounding of Raghavan and Thompson.

Albrecht's router uses the method of Garg and Könemann with Fleischer's extensions, which routes the nets in phases with a step size and a stopping rule of its own. This page uses the averaged multiplicative weights form above, which has the same kind of guarantee and a short proof, and it is not Albrecht's exact procedure.

## Example

**Two crossing nets.** Take the $2 \times 2$ grid of gcells $(x, y)$ with capacity 1 on its 4 edges: bottom $(0,0)(1,0)$, top $(0,1)(1,1)$, left $(0,0)(0,1)$ and right $(1,0)(1,1)$. Net A joins $(0,0)$ and $(1,1)$, net B joins $(1,0)$ and $(0,1)$. Then $k = 2$, $\rho = 2$, and take $\varepsilon = 1/4$. A route of A meets each route of B in one edge, so $\lambda_{\mathrm{int}} = 2$.

| round | weights (bottom, top, left, right) | route of A | route of B | loads | $\sum_e \ell_e \mathrm{load}_e$ |
| --- | --- | --- | --- | --- | --- |
| 1 | 1, 1, 1, 1 | bottom, right | bottom, left | 2, 0, 1, 1 | 1 |
| 2 | 5/4, 1, 9/8, 9/8 | top, left | top, right | 0, 2, 1, 1 | 17/18 |
| 3 | 5/4, 5/4, 81/64, 81/64 | bottom, right | bottom, left | 2, 0, 1, 1 | 1 |
| 4 | 25/16, 5/4, 729/512, 729/512 | top, left | top, right | 0, 2, 1, 1 | 1369/1449 |

In round 1 all lengths are $1/4$, both routes of each net cost $1/2$, and the ties go to the routes through the bottom edge. Its load is 2, so its weight becomes $1 \cdot (1 + \frac14 \cdot \frac22) = 5/4$, and the left and right weights become $1 + \frac14 \cdot \frac12 = 9/8$. In round 2 the routes through the top cost $(1 + 9/8)/W$ against $(5/4 + 9/8)/W$ through the bottom, so both nets switch. The rounds alternate. For every even $T$ the average gives each route weight $1/2$, every edge has average load 1, and $\lambda_{\mathrm{frac}} = 1$. Round 1 gives $\mathrm{LB} = 1$, so $\lambda_{\mathrm{frac}} = \mathrm{LB} = \lambda^* = 1$: the lower bound proves that this fractional solution is optimal. The rounding picks one route per net, and every pick has congestion 2, the integral optimum. The gap between $\lambda^* = 1$ and $\lambda_{\mathrm{int}} = 2$ is the [integrality gap](/integrality-gap/) of this instance.

**Three nets on a $3 \times 3$ grid.** Take capacity 1 on all 12 edges and the nets $(0,0)$ to $(2,2)$, $(2,0)$ to $(0,2)$ and $(1,0)$ to $(1,2)$, with the Dijkstra oracle and $\varepsilon = 1/4$. All three nets must cross the 3 vertical edges between row 0 and row 1, so $\lambda^* \ge 1$.

| rounds $T$ | $\lambda_{\mathrm{frac}}$ | LB |
| --- | --- | --- |
| 10 | 1 | 0.8547 |
| 40 | 1 | 0.9179 |
| 160 | 1 | 0.9965 |

So $\lambda^* = 1$ here, and the lower bound of line L6 approaches it as the weights settle. An exhaustive search over the 12, 12 and 9 simple paths of the three nets gives $\lambda_{\mathrm{int}} = 2$, and each rounding in these runs had congestion 2.

## Correctness

The [proof](proofs/correctness.md) shows the following, for any route sets $\mathcal{R}_i$ for which the oracle returns a shortest route.

- **Feasible average.** For each net, the weights $x_{iP}$ are nonnegative and add up to 1.
- **Lower bound.** Each value $\sum_e \ell_e \mathrm{load}_e$ of line L6 is at most $\lambda^*$, so $\mathrm{LB} \le \lambda^* \le \lambda_{\mathrm{frac}}$.
- **Upper bound.** $\lambda_{\mathrm{frac}} \le \frac{\varepsilon}{\ln(1 + \varepsilon)} \lambda^* + \frac{\rho \ln |E|}{T \ln(1 + \varepsilon)} \le (1 + \varepsilon) \lambda^* + \frac{\rho \ln |E|}{T \ln(1 + \varepsilon)}$.
- **Rounds needed.** For $0 < \varepsilon \le 1$ and $T \ge 2 \rho \ln |E| / (\varepsilon^2 \lambda^*)$, $\lambda_{\mathrm{frac}} \le (1 + 2\varepsilon) \lambda^*$.
- **Rounding.** The expected load of each edge after rounding is its average load, at most $\lambda_{\mathrm{frac}} c_e$.

## Complexity

- **One round.** $k$ oracle calls, each a Dijkstra search in $O(E \log V)$ time with a binary heap, and $O(E)$ for the weights and lengths. So a round costs $O(k E \log V)$.
- **All rounds.** $O(T k E \log V)$. The bound above needs $T = O(\rho \log E / (\varepsilon^2 \lambda^*))$ rounds for a $(1 + 2\varepsilon)$ factor. This number depends on the width $\rho$, so it is pseudo-polynomial when capacities are small and nets are many. The method of Garg and Könemann, with variable steps, removes the dependence on the width.
- **Space.** $O(E)$ for the weights, and one counter for each distinct route that the oracle returns, at most $T$ per net, each with up to $V$ edges.
- **Rounding.** $O(k T)$ to pick the routes from the counters.
- **Exact arithmetic.** The test implementation uses fractions, whose size grows with $T$. Real routers use floating point and normalize the weights.

## Properties

- **What is proved.** The fractional solution is within the factor and the additive term above, and the lower bound is valid. For two-pin nets with unit capacities, randomized rounding gives congestion $O(\log |E| / \log \log |E|) \cdot \max(\lambda_{\mathrm{frac}}, 1)$ with high probability, by the proof on the [randomized rounding](/randomized-rounding/) page, which uses only the bound on the expected load of each edge.
- **A certificate.** $\lambda_{\mathrm{frac}} / \mathrm{LB}$ is a proved bound on how far the fractional solution is from optimal, computed during the run.
- **What is measured.** The final quality after rounding and repair is measured on benchmarks. The integral solution can be twice the fractional optimum or more, as in the examples above, and the repair stage has no proof.
- **Randomized.** The fractional part is deterministic for a fixed tie rule. The rounding uses random choices, with a fixed seed in the implementation.
- **Splittable by design.** Each round adds at most one route per net, so after $T$ rounds a net uses at most $T$ routes, often far fewer.

## Variants and improvements

- **Garg and Könemann steps.** Increase the lengths along one shortest route at a time, with a step that depends on the bottleneck capacity of that route, and stop when the dual value reaches a threshold. This removes the width from the number of steps.
- **Multi-pin nets.** Let $\mathcal{R}_i$ be the Steiner trees of net $i$ and let the oracle return a cheapest tree. A minimum Steiner tree is NP-hard to find, so routers use a heuristic tree, and then the factor of the method is multiplied by the ratio of the heuristic.
- **Exact LP.** For small instances, solve the path LP with column generation by the [simplex method](/simplex-method/), with the same shortest path oracle as the pricing step.
- **Derandomized rounding.** Replace line L9 by the method of conditional expectations with a pessimistic estimator, which gives the same congestion bound without random choices.
- **Negotiation after rounding.** Feed the rounded routes to [negotiated congestion routing](/negotiated-congestion-routing/), which removes the remaining overflow.

## When to use it

- When a proved lower bound on congestion is wanted, to know how far a routing is from the best possible.
- When the nets are many and the grid is crowded, so that the order of a sequential router matters much.
- As a start for a rip-up and reroute stage, since the rounded routes spread the nets well.

When speed is the first goal and the congestion is mild, [pattern routing](/pattern-routing/) and [negotiated congestion routing](/negotiated-congestion-routing/) are simpler and faster.

## Pitfalls

- **Treating $\lambda_{\mathrm{frac}}$ as the answer.** It is the congestion of a split routing. A real routing can need much more, and the rounding can make edges overflow.
- **Wrong width.** If $\rho$ is too small, some $\mathrm{load}_e / (\rho c_e)$ exceeds 1 and the proof fails. If it is much too large, the run needs many more rounds.
- **Edges of capacity 0.** The lengths divide by $c_e$. Remove such edges from the graph before the run, or give them a huge length.
- **Oracle that is not shortest.** The lower bound needs the oracle to return a true shortest route. A heuristic Steiner tree oracle gives a weaker bound.
- **Few rounds.** The additive term $\rho \ln |E| / (T \ln(1 + \varepsilon))$ can dominate. In the crossing example with $T = 10$ it is about 1.24, so the proved bound is about 2.36 while the true value is 1.
- **Rounding many nets on thin edges.** The rounding bound is weakest when the expected load of each edge is small, as on edges of capacity 1 or 2. Large overflow after rounding is common on crowded grids, and the repair step does the rest.

## Implementations

## History

Raghavan and Thompson (1987) wrote global wiring as a 0-1 multicommodity flow, solved its linear relaxation and rounded it at random, which gave the first congestion bound for the rounded routing. Approximation schemes for fractional multicommodity flow with shortest path oracles followed, among them the method of Garg and Könemann (FOCS 1998, journal version 2007) and its speedup by Fleischer. Albrecht (ISPD 2000 and IEEE TCAD 2001) used this method for chip global routing, followed by rounding to one route per net.

## References
