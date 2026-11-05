---
tag: RZ0Y75
kind: problem
slug: multi-commodity-flow-problem
name: Multi-commodity flow problem
aliases:
- multicommodity flow
area: graphs/flows-and-cuts
level: advanced
summary: Route several commodities with distinct source-sink pairs sharing edge capacities.
prereqs: [max-flow-problem, flow-network, linear-programming-problem, lp-duality]
see_also: [max-flow-min-cut-theorem, integrality-theorem, sparsest-cut-problem, multicut-problem, min-cost-flow-problem, edge-disjoint-paths, multiplicative-weights-update, integrality-gap]
sources:
  - paper: doi:10.1287/opre.11.3.344
    title: T. C. Hu, Multi-commodity network flows, Operations Research 11(3), 344 to 360 (1963)
    locator: the whole paper (the two-commodity max-flow min-cut theorem in undirected networks)
  - paper: doi:10.1137/0205048
    title: S. Even, A. Itai and A. Shamir, On the complexity of timetable and multicommodity flow problems, SIAM Journal on Computing 5(4), 691 to 703 (1976)
    locator: the result that integral two-commodity flow is NP-complete
  - paper: doi:10.1287/opre.34.2.250
    title: Éva Tardos, A strongly polynomial algorithm to solve combinatorial linear programs, Operations Research 34(2), 250 to 256 (1986)
    locator: the whole paper (linear programs with small integer constraint matrices, which include multicommodity flow)
  - paper: doi:10.1145/331524.331526
    title: Tom Leighton and Satish Rao, Multicommodity max-flow min-cut theorems and their use in designing approximation algorithms, Journal of the ACM 46(6), 787 to 832 (1999)
    locator: the whole paper (the O(log n) gap between uniform concurrent flow and sparsest cut)
  - paper: doi:10.1137/S0097539704446232
    title: Naveen Garg and Jochen Könemann, Faster and simpler algorithms for multicommodity flow and other fractional packing problems, SIAM Journal on Computing 37(2), 630 to 652 (2007)
    locator: the whole paper (the length-function method for approximate maximum and concurrent flow)
---

The multi-commodity flow problem asks for several [flows](/max-flow-problem/) at once in one [network](/flow-network/). There are $k$ commodities, each with its own source $s_i$, sink $t_i$ and demand $d_i$, and every edge has one capacity that the commodities share. Each commodity must obey conservation on its own, so units of one commodity cannot be swapped for units of another. As a [linear program](/linear-programming-problem/) the problem is solvable in polynomial time, and even in strongly polynomial time by Tardos's method. But the nice facts of one commodity fail: an integral solution may not exist when a fractional one does, finding an integral one is NP-complete already for two commodities, and the largest routable flow can be smaller than every cut bound suggests. The gap between flows and cuts is at most $O(\log k)$, and this gap is the base of the approximation algorithms for [sparsest cut](/sparsest-cut-problem/) and [multicut](/multicut-problem/).

## In plain words

Many shippers use the same road network. Each shipper has its own start, its own destination and an amount to move. Each road can carry a limited total load, shared by all shippers. Can everyone's goods get through? If not, what is the largest equal share of each order that can?

With one shipper, the answer is simple: the most you can move equals the narrowest bottleneck between start and goal. With many shippers, goods of different shippers cannot be exchanged, so they compete for the same roads. The narrowest bottleneck is still a limit, but it is no longer the whole story, and splitting a load into fractions can be needed where whole units would not fit.

## Definition

**Input.** A directed graph $G = (V, E)$ with real capacities $c : E \to \mathbb{R}_{\ge 0}$, integer in the integral variant, and $k$ commodities $(s_i, t_i, d_i)$ with $s_i \ne t_i$ and $d_i \ge 0$. Parallel and antiparallel edges are allowed. Each edge of an antiparallel pair has its own capacity, shared by all commodities that use it in its own direction.

**Flows.** A multicommodity flow is a family $f_1, \ldots, f_k$ where each $f_i : E \to \mathbb{R}_{\ge 0}$ is an $s_i$-$t_i$ flow of value $|f_i|$, that is, it obeys conservation at every vertex other than $s_i$ and $t_i$, and the *joint capacity constraint*

$$\sum_{i=1}^{k} f_i(e) \le c(e) \qquad (e \in E)$$

holds. No commodity has its own capacity on an edge; only the sum is bounded.

**Undirected networks.** In an undirected graph, an edge $\{u, v\}$ of capacity $c$ is shared by all commodities in both directions: $\sum_i \bigl(f_i(u, v) + f_i(v, u)\bigr) \le c$. This is not the same as two opposite directed edges of capacity $c$ each, which would allow $c$ units each way.

**Objectives.**

- **Feasibility.** Is there a flow with $|f_i| = d_i$ for all $i$?
- **Maximum concurrent flow.** The largest $\lambda$ such that $\lambda d_i$ units of each commodity can be routed at once.
- **Maximum total flow.** The largest $\sum_i |f_i|$, with no demands.
- **Minimum cost.** Edge costs, possibly per commodity, and the cheapest flow that meets all demands.

## Variants

- **Integral multicommodity flow.** Each $f_i$ must be integral. With unit capacities and unit demands this is the edge-disjoint paths problem for $k$ pairs, NP-complete when $k$ is part of the input and, in directed graphs, already for $k = 2$. Even, Itai and Shamir showed that integral two-commodity flow is NP-complete.
- **Unsplittable flow.** Each commodity must use one path.
- **Uniform demands.** One commodity for each pair of vertices, all with demand 1: the setting of Leighton and Rao, tied to the uniform [sparsest cut](/sparsest-cut-problem/).
- **Single source.** All commodities share a source and differ only in their sinks. If the demands need not be kept apart, this is one commodity with a super-sink and is easy; it is the commodity identity that makes the problem hard.

## Examples

**Fractional but not integral.** Take the undirected cycle $a, b, c, d$ with unit capacities and the commodities $a \to c$ and $b \to d$, each with demand 1. Routing half of each commodity each way around the cycle puts exactly 1 unit on every edge, so the fractional problem is feasible. An integral solution would need one path of two edges for each commodity; each of the four pairs of such paths shares an edge, so none exists. See the [integrality theorem](/integrality-theorem/), which holds only for one commodity.

**Cuts do not suffice.** In $K_{3,2}$ with sides $\{a, b, c\}$ and $\{x, y\}$, unit capacities on the six undirected edges, and unit demands between $a b$, $a c$, $b c$ and $x y$, every cut has at least as much capacity as the demand it separates. But every one of the four pairs is at distance 2, so routing $\lambda$ of each demand uses at least $2 \cdot 4\lambda$ units of capacity, while only 6 exist. So $\lambda \le 3/4$ although the cut condition holds with ratio 1.

**A zero-capacity edge** carries no flow of any commodity, so it can be deleted.

**No $s_i$-$t_i$ path.** If some commodity with $d_i > 0$ has no path from $s_i$ to $t_i$, the feasibility problem has no solution and the maximum concurrent flow is $\lambda = 0$; the maximum total flow ignores that commodity.

## Known algorithms

| method | result | notes |
|---|---|---|
| linear programming | exact, polynomial | the LP has $k m$ variables; interior-point or ellipsoid methods |
| Tardos (1986) | exact, strongly polynomial | the constraint matrix has entries in $\{-1, 0, 1\}$ |
| length-function methods (Garg-Könemann and others) | $(1 + \varepsilon)$-approximation | repeated shortest paths, with edge lengths that grow with their load |
| two commodities, undirected (Hu) | exact, combinatorial | the two-commodity max-flow min-cut theorem, with half-integral flows |
| integral version | NP-complete | already for two commodities |

**The length-function method.** Give each edge a length $\ell_e$, start all lengths at a small $\delta$, and repeat: route some flow along a shortest $s_i$-$t_i$ path under $\ell$, and multiply the length of each used edge by $1 + \varepsilon$ times the fraction of its capacity used. Scaling the result at the end gives a feasible flow within a factor $1 + O(\varepsilon)$ of the optimum. The analysis is the duality below: the lengths are a dual solution, and the method is an instance of [multiplicative weights](/multiplicative-weights-update/).

## Bounds

**Duality.** Writing the maximum concurrent flow with one variable for each $s_i$-$t_i$ path, its [LP dual](/lp-duality/) is

$$\lambda^{*} = \min_{\ell \ge 0} \frac{\sum_{e} c(e)\, \ell_e}{\sum_{i} d_i \operatorname{dist}_\ell(s_i, t_i)}.$$

*Why "at most" holds:* if $\lambda d_i$ units of each commodity are routed, each unit of commodity $i$ uses edges of total length at least $\operatorname{dist}_\ell(s_i, t_i)$, so $\lambda \sum_i d_i \operatorname{dist}_\ell(s_i, t_i) \le \sum_e \ell_e \sum_i f_i(e) \le \sum_e c(e) \ell_e$. Equality for some $\ell$ is LP strong duality.

**The cut condition.** Taking $\ell$ to be 1 on the edges of a cut $\delta(S)$ and 0 elsewhere gives $\lambda^{*} \le c(\delta(S)) / D(S)$, where $D(S)$ is the demand that $S$ separates. For one commodity this bound is tight by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). For two commodities in undirected graphs it is still tight (Hu). For more commodities it is not, as $K_{3,2}$ shows.

**The flow-cut gap.** In undirected graphs, the smallest cut ratio is at most $O(\log k)$ times $\lambda^{*}$, and there are graphs, expanders with uniform demands, where the gap is $\Theta(\log n)$. Leighton and Rao proved the uniform case; the general case uses embeddings of finite metrics into $\ell_1$, see [sparsest cut](/sparsest-cut-problem/).

**Lower bound.** Any exact method must read the input, $\Omega(n + m + k)$.

## Reductions

- **One commodity is max flow**, and a single source with a super-sink is one commodity.
- **Edge-disjoint paths to integral multicommodity flow**, with unit capacities and demands.
- **Multicut and sparsest cut** are the integral versions of the dual LPs of maximum total flow and maximum concurrent flow; rounding the dual gives their approximations.
- **Multicommodity flow to LP** directly, with $O(k m)$ variables and $O(k n + m)$ constraints.

## Applications

- Routing traffic in communication and transport networks, where many origin-destination pairs share links.
- Planning freight, where goods of different kinds cannot be swapped.
- VLSI routing, where wires between many pairs of pins share channels.
- The basis of approximation algorithms for sparsest cut, balanced separators, multicut, minimum linear arrangement and other cut problems.

## References
