---
tag: NC7YNV
kind: problem
slug: maximum-throughput-routing
name: Maximum-throughput routing
area: systems/networking-algorithms
level: advanced
summary: "Route several demands through a capacitated network to carry the largest common fraction of all of them, or, with random arrivals, keep every rate in the capacity region stable."
prereqs: [routing-problem, multi-commodity-flow-problem, lp-duality]
see_also: [backpressure-routing, wireless-link-scheduling, sparsest-cut-problem, multiplicative-weights-update, oblivious-routing, valiant-routing, network-coding, dijkstra]
sources:
  - paper: doi:10.1145/77600.77620
    title: "Farhad Shahrokhi and David W. Matula, The maximum concurrent flow problem, Journal of the ACM 37(2), 1990"
    locator: pages 318 to 334 (the problem, its duality with cuts, and an approximation scheme for uniform capacities)
  - paper: doi:10.1137/S0097539704446232
    title: "Naveen Garg and Jochen Könemann, Faster and simpler algorithms for multicommodity flow and other fractional packing problems, SIAM Journal on Computing 37(2), 2007"
    locator: pages 630 to 652 (lengths updated multiplicatively, phases of shortest path routing, the maximum concurrent flow algorithm); first at FOCS 1998
  - paper: doi:10.1137/S0895480199355754
    title: "Lisa K. Fleischer, Approximating fractional multicommodity flow independent of the number of commodities, SIAM Journal on Discrete Mathematics 13(4), 2000"
    locator: pages 505 to 520
  - paper: doi:10.1145/331524.331526
    title: "Tom Leighton and Satish Rao, Multicommodity max-flow min-cut theorems and their use in designing approximation algorithms, Journal of the ACM 46(6), 1999"
    locator: pages 787 to 832 (the logarithmic gap between concurrent flow and sparsest cut)
  - paper: doi:10.1109/9.182479
    title: "Leandros Tassiulas and Anthony Ephremides, Stability properties of constrained queueing systems and scheduling policies for maximum throughput in multihop radio networks, IEEE Transactions on Automatic Control 37(12), 1992"
    locator: pages 1936 to 1948 (the capacity region and the throughput-optimal backpressure policy)
  - paper: "Leonidas Georgiadis, Michael J. Neely and Leandros Tassiulas, Resource allocation and cross-layer control in wireless networks, Foundations and Trends in Networking 1(1), 2006"
    locator: the network capacity region, stability, and Lyapunov drift arguments for throughput-optimal routing
---

Maximum-throughput routing asks how to route several flows of traffic through a network with link capacities so that the network carries as much as possible. In the static form, each *commodity* $j$ has a source, a destination and a demand $d_j$, and the goal is the largest $\lambda$ such that $\lambda d_j$ of every commodity can be routed at the same time without exceeding any capacity: the *maximum concurrent flow*, a [multicommodity flow](/multi-commodity-flow-problem/) linear program. In the dynamic form, packets arrive at random with unknown rates, and a routing policy is *throughput-optimal* if it keeps all queues stable for every vector of rates that some flow could carry. [Backpressure routing](/backpressure-routing/) is the classic throughput-optimal policy; for the static form, the Garg and Könemann algorithm finds a $\lambda$ within a factor $(1 - \varepsilon)^3$ of the optimum with a sequence of shortest path computations.

## In plain words

Several groups of trucks must cross a road network, each group from its own city to its own destination, and each road takes only so many trucks per hour. You want to move the same share of every group's load, and you want that share to be as large as possible. Sending each group on its shortest route can jam a few roads while others stay empty, so the best plan often splits a group over several routes. When the loads are not known in advance and change from hour to hour, the goal becomes a rule that keeps the waiting lines from growing whenever some plan could carry the load.

## Definition

**Network.** A directed graph $G = (V, E)$ with $n$ nodes, $m$ edges and capacities $c_e > 0$. An undirected link is two directed edges, or one edge whose capacity both directions share.

**Commodities.** $k$ triples $(s_j, t_j, d_j)$: a source, a destination and a demand.

**Maximum concurrent flow.** Find flows $f_j$, where $f_j$ sends $\lambda d_j$ units from $s_j$ to $t_j$ with conservation at every other node, such that $\sum_j f_j(e) \le c_e$ on every edge, and $\lambda$ is as large as possible. Call the optimum $\lambda^*$. In the path form, with $x_P \ge 0$ the flow on a path $P$:

$$\lambda^* = \max \Big\{ \lambda : \sum_{P \ni e} x_P \le c_e \text{ for all } e, \; \sum_{P \in \mathcal{P}_j} x_P \ge \lambda d_j \text{ for all } j \Big\}.$$

If $\lambda^* \ge 1$ all demands fit, and $1 / \lambda^*$ is the least possible *congestion*, the largest ratio of load to capacity over the edges.

**Dynamic form.** Packets of commodity $j$ arrive at $s_j$ at a long-run rate $a_j$. The *capacity region* $\Lambda$ is the set of rate vectors $a$ for which a multicommodity flow carries $a_j$ for each $j$ within the capacities; with $d = a$, these are the vectors with $\lambda^* \ge 1$. A policy decides at each time step which packets each link sends. It is *throughput-optimal* if, for every $a$ in the interior of $\Lambda$, all queues stay stable (their mean length stays bounded), without knowing $a$. No policy stabilizes a rate vector outside $\Lambda$.

## Variants

- **Maximum multicommodity flow.** Maximize the total flow $\sum_j |f_j|$, with no fairness between commodities.
- **Minimum congestion.** Route all demands in full and minimize the largest load to capacity ratio, which equals $1 / \lambda^*$.
- **Integral or unsplittable routing.** Each commodity on one path; the decision version is NP-hard even with two commodities, and it is the setting of [edge-disjoint paths](/edge-disjoint-paths/).
- **Wireless networks.** Links interfere, so the capacity region also depends on which sets of links may send together; routing is coupled with [wireless link scheduling](/wireless-link-scheduling/).
- **Oblivious routing.** Fix the routes in advance, independent of the demands, and compare the congestion with the best routing for each demand; see [oblivious routing](/oblivious-routing/) and [Valiant routing](/valiant-routing/).
- **Network coding.** For multicast, coding at the nodes can carry more than any routing; see [network coding](/network-coding/).

## Examples

**Splitting beats the shortest path.** Two paths join $s$ to $t$, each with capacity 1, one of them shorter. Routing every packet on the shortest path keeps the queue stable only for arrival rates below 1. Splitting the traffic over both paths keeps it stable for every rate below 2, which is the capacity region. So shortest path routing with fixed weights is not throughput-optimal.

**A gap between flow and cuts.** Take the complete bipartite graph $K_{2,3}$ with sides $\{a, b\}$ and $\{x, y, z\}$, each link of capacity 1 in each direction, and four unit demands: $a \to b$, $x \to y$, $y \to z$ and $x \to z$. Every set of nodes $S$ has at least as much capacity leaving it as demand that must leave it, so cuts alone allow $\lambda = 1$. The exact linear program gives $\lambda^* = 8/9$.

- *A flow of value 8/9.* $a \to b$ uses $a y b$ with $4/9$ and $a x b$, $a z b$ with $2/9$ each; $x \to y$ uses $x a y$ with $5/9$ and $x b y$ with $1/3$; $y \to z$ uses $y b z$ with $5/9$ and $y a z$ with $1/3$; $x \to z$ uses $x a z$ and $x b z$ with $4/9$ each. Every edge carries at most 1.
- *A proof that no flow does better.* Give lengths $1/9$ to the edges $x a$, $a y$, $y b$ and $b z$, and $2/9$ to $a z$ and $x b$, and $0$ to the others. Their total capacity times length is $8/9$. Under these lengths the shortest paths of the four commodities have lengths $2/9$, $2/9$, $2/9$ and $1/3$, which add up to 1. Each unit of $\lambda$ uses at least length 1 of capacity, so $\lambda \le 8/9$, by [LP duality](/lp-duality/).

**Garg and Könemann on this example.** The implementation below returns $\lambda = 0.7246$, $0.8071$, $0.8473$ and $0.8721$ for $\varepsilon = 0.2$, $0.1$, $0.05$ and $0.02$, against $8/9 \approx 0.8889$, and its flows respect every capacity. On 20 random networks (6 nodes, each pair joined with probability 1/2 by links of capacity 1 to 4 in each direction, 3 commodities with demands 1 to 3, seeds 0 to 19), with $\varepsilon = 0.1$, the ratio to the exact optimum was between 0.913 and 0.966; the guarantee is $0.9^3 = 0.729$.

## Known algorithms

| Algorithm | Form | Result |
|---|---|---|
| Linear programming ([simplex](/simplex-method/), [interior point](/interior-point-method/)) | static | exact, polynomial time with interior point methods; $O(km)$ variables in the edge form |
| Shahrokhi and Matula (1990) | static | approximation scheme for uniform capacities |
| Leighton, Makedon, Plotkin, Stein, Tardos and Tragoudas (1995); Plotkin, Shmoys and Tardos (1995) | static | approximation schemes for general capacities through fractional packing |
| Garg and Könemann (1998) | static | $(1 - \varepsilon)^3$ approximation by shortest paths with multiplicatively updated lengths |
| Fleischer (2000) | static | running time for maximum multicommodity flow independent of $k$ |
| [Backpressure](/backpressure-routing/) (Tassiulas and Ephremides, 1992) | dynamic | throughput-optimal, uses only queue lengths |
| Shortest path routing, equal-cost multipath | dynamic | not throughput-optimal |

**The Garg and Könemann algorithm.** Give every edge a length $\ell_e = \delta / c_e$ for a small $\delta$. In each phase, route each commodity's demand along shortest paths with respect to $\ell$ ([Dijkstra](/dijkstra/)), in pieces no larger than the smallest capacity on the path, and after sending $u$ units over an edge multiply its length by $1 + \varepsilon u / c_e$. Stop when $\sum_e c_e \ell_e \ge 1$. An edge's length grows by a factor of at least $1 + \varepsilon$ for each $c_e$ units it carries and ends below $(1 + \varepsilon)/c_e$, so dividing all flows by $\log_{1+\varepsilon}((1 + \varepsilon)/\delta)$ gives a feasible flow. The lengths play the part of the dual variables in the example above, and the method is an instance of [multiplicative weights](/multiplicative-weights-update/). With $\delta = (1 + \varepsilon)((1 + \varepsilon) m)^{-1/\varepsilon}$ and demands scaled so that $1 \le \lambda^* \le k$, the result is at least $(1 - \varepsilon)^3 \lambda^*$, and the number of shortest path computations grows as $\varepsilon^{-2}$ times a polynomial in $m$ and $k$, up to logarithmic factors.

## Bounds

- **The cut bound.** For every set $S$, $\lambda^*$ is at most the capacity leaving $S$ divided by the demand that must leave $S$. The smallest such ratio is the *sparsest cut* ([sparsest cut problem](/sparsest-cut-problem/)).
- **One commodity.** The cut bound is exact: this is the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).
- **Several commodities.** The cut bound can be strict, as in the $K_{2,3}$ example. In undirected graphs the gap is $O(\log k)$ and this is tight up to a constant, through expander graphs (Leighton and Rao for uniform demands; Linial, London and Rabinovich and Aumann and Rabani in general). In directed graphs the gap can be much larger.
- **Stability.** A rate vector outside the capacity region makes some queue grow without bound under every policy, since some edge set would have to carry more than its capacity on average.
- **Lyapunov drift.** Backpressure is throughput-optimal: for rates inside the capacity region, the sum of squared queue lengths has negative expected drift whenever the queues are large, which bounds the mean queue lengths.

## Reductions

- **To linear programming.** The edge form has a variable for each commodity and edge; the path form has exponentially many variables but a separation oracle (shortest paths) for its dual, which is how the approximation algorithms work.
- **From the dynamic form.** A rate vector $a$ is in the capacity region exactly when the static problem with demands $a$ has $\lambda^* \ge 1$. A policy that knows $a$ can solve the static problem and split traffic in proportion to the path flows; backpressure reaches the same region without knowing $a$.
- **To sparsest cut.** Rounding the dual of the concurrent flow program gives an $O(\log k)$ approximation for the sparsest cut, the original use of the Leighton and Rao theorem.

## Applications

- **Traffic engineering.** Operators of backbone and data center networks compute splits of traffic over paths to minimize the most loaded link, which is the minimum congestion form.
- **Wireless multihop networks.** Backpressure and its variants route and schedule in sensor and mesh networks without knowing the traffic.
- **Approximation algorithms.** Concurrent flow is the relaxation behind algorithms for sparsest cut, balanced separators and minimum linear arrangement.
- **Capacity planning.** The value $\lambda^*$ of a demand matrix measures how much traffic growth a network can absorb.

## References
