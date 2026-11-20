---
tag: PJAWQT
kind: model
slug: selfish-routing-model
name: Selfish routing model
aliases:
- nonatomic routing game
- nonatomic selfish routing
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: A directed network with a continuous nondecreasing latency on each edge and a continuum of travelers per commodity, each of whom picks a path of least latency.
prereqs: [nash-equilibrium, flow-network]
see_also: [wardrop-equilibrium, system-optimal-flow, beckmann-potential, price-of-anarchy, roughgarden-tardos-four-thirds-bound, braess-paradox, atomic-congestion-game, min-cost-flow-problem]
sources:
  - paper: doi:10.1680/ipeds.1952.11259
    title: "J. G. Wardrop, Some theoretical aspects of road traffic research, Proceedings of the Institution of Civil Engineers 1(3) (1952), 325-362"
    locator: the traffic model on a road network and the two principles of route choice (the equilibrium and the minimum of the average journey time)
  - book: "Martin Beckmann, C. B. McGuire and Christopher B. Winsten, Studies in the Economics of Transportation, Yale University Press, 1956"
    locator: Part I (the network model with continuous flows, the equilibrium conditions and the convex program for them)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 18, Tim Roughgarden, Routing games, Section 18.2.1 (nonatomic selfish routing, Definition 18.1), Section 18.3.1 (Theorem 18.8) and Section 18.4.1 (the price of anarchy)
  - book: isbn:9780262182430
    title: Tim Roughgarden, Selfish Routing and the Price of Anarchy, MIT Press, 2005
    locator: Chapter 2 (the model, flows, equilibria and Section 2.3 on the price of anarchy) and Chapter 3 (How bad is selfish routing?)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 11 (selfish routing and the price of anarchy) and Lecture 12 (over-provisioning and atomic selfish routing)
  - paper: doi:10.1016/0041-1647(75)90030-1
    title: "Larry J. LeBlanc, Edward K. Morlok and William P. Pierskalla, An efficient approach to solving the road network equilibrium traffic assignment problem, Transportation Research 9(5) (1975), 309-318"
    locator: the Frank-Wolfe method applied to the convex program of the equilibrium
---

The selfish routing model is a game in which a large population of travelers each choose a path through a directed network, and the delay of each edge grows with the traffic on it. Each traveler is so small that a single change of path does not change any delay, so the traffic is a continuous [flow](/flow-network/) and the players are *nonatomic*. Its equilibria are the [Wardrop equilibria](/wardrop-equilibrium/), and the model is the base of the [price of anarchy](/price-of-anarchy/) for networks. In the [atomic congestion game](/atomic-congestion-game/) each player is one unit of traffic and does change the delays; that model has other equilibria and other bounds.

## The machine

**The network.** $G = (V, E)$ is a directed graph, and parallel edges are allowed. There are $k$ commodities (on this page $k$ is the number of commodities). Commodity $i$ has a source $s_i$, a sink $t_i$ and a traffic rate $r_i > 0$. $\mathcal{P}_i$ is the set of simple $s_i$-$t_i$ paths, assumed nonempty, and $\mathcal{P} = \mathcal{P}_1 \cup \cdots \cup \mathcal{P}_k$.

**Latencies.** Each edge $e$ has a latency function $\ell_e : [0, \infty) \to [0, \infty)$. The standing assumptions are that each $\ell_e$ is continuous and nondecreasing. Some results add a condition on the class of latency functions:

- affine: $\ell_e(x) = a_e x + b_e$ with $a_e, b_e \ge 0$;
- polynomial of degree at most $d$ with nonnegative coefficients;
- semiconvex: $x \, \ell_e(x)$ is convex (this is needed for the marginal cost form of the [system optimal flow](/system-optimal-flow/)).

**Flows.** A flow is a vector $f = (f_P)_{P \in \mathcal{P}}$ with $f_P \ge 0$ and $\sum_{P \in \mathcal{P}_i} f_P = r_i$ for each commodity $i$. The flow on edge $e$ is $f_e = \sum_{P \ni e} f_P$. The same object in edge form is a flow $f^i_e \ge 0$ for each commodity that satisfies flow conservation at every vertex $v$:

$$\sum_{e \text{ leaves } v} f^i_e \;-\; \sum_{e \text{ enters } v} f^i_e \;=\; \begin{cases} r_i & \text{if } v = s_i, \\ -r_i & \text{if } v = t_i, \\ 0 & \text{otherwise,} \end{cases} \qquad f_e = \sum_{i=1}^{k} f^i_e .$$

A path flow gives an edge flow by $f^i_e = \sum_{P \in \mathcal{P}_i,\, P \ni e} f_P$. Conversely, by flow decomposition, an edge flow splits into flows on $s_i$-$t_i$ paths and flows around cycles. Removing the cycle parts lowers some edge flows and so raises no latency. The set of feasible path flows is a polytope, so it is convex and compact.

**The players and their costs.** The travelers of commodity $i$ form the interval $[0, r_i]$ with its length as the measure. Each traveler chooses one path in $\mathcal{P}_i$, and the choices of all travelers give the flow $f$. A traveler on path $P$ has the cost

$$\ell_P(f) = \sum_{e \in P} \ell_e(f_e),$$

and wants it small. This is a cost game: costs are minimized on all pages of this group. One traveler has measure 0, so a change of path by one traveler does not change $f$. A traveler on $P$ gains by a switch to $P' \in \mathcal{P}_i$ exactly when $\ell_{P'}(f) < \ell_P(f)$. A flow in which no traveler gains is a [Nash equilibrium](/nash-equilibrium/) of the game, called a [Wardrop equilibrium](/wardrop-equilibrium/): for every $i$ and every pair $P, P' \in \mathcal{P}_i$ with $f_P > 0$, $\ell_P(f) \le \ell_{P'}(f)$. Each traveler picks one path, so these equilibria are pure. A mixed strategy adds nothing, because a flow already describes a split of the traffic.

An *instance* is the triple $(G, r, \ell)$. Example: Pigou's network has two vertices $s$ and $t$, two parallel edges with $\ell_1(x) = 1$ and $\ell_2(x) = x$, and one commodity with $r = 1$. A flow is a pair $(1 - x, x)$ with $0 \le x \le 1$ ([Pigou's example](/pigou-example/)).

## What it counts

The model measures a flow by its **total latency**, the social cost

$$C(f) = \sum_{P \in \mathcal{P}} f_P \, \ell_P(f) = \sum_{e \in E} f_e \, \ell_e(f_e).$$

The two sums are equal: expand $\ell_P(f)$ as a sum over the edges of $P$ and exchange the order of summation. $C(f)$ divided by the total rate is the average travel time. A flow $f^*$ of least cost is a [system optimal flow](/system-optimal-flow/). It exists, because $C$ is continuous on the compact set of flows.

The price of anarchy of an instance is $C(f) / C(f^*)$ for an equilibrium $f$. All equilibria of an instance have the same cost ([Beckmann potential](/beckmann-potential/)), so the ratio does not depend on the choice of $f$, and the [price of stability](/price-of-stability/) of an instance equals its price of anarchy. If $C(f^*) = 0$, then every edge used by $f^*$ has latency 0 on the range $[0, f^*_e]$, so the Beckmann potential of $f^*$ is 0, its least possible value. Then $f^*$ is an equilibrium, every equilibrium has cost 0, and the convention $0/0 = 1$ gives the ratio 1. For a class of instances (for example all networks with affine latencies) the price of anarchy is the supremum of the ratio over the class.

Other objectives are also studied, for example the largest latency of a used path. The results below are for the total latency.

## Relation to other models

- **Atomic congestion games.** In an [atomic congestion game](/atomic-congestion-game/) there are $n$ players, each routes one unit (or a weight) on one path, and a player's change does change the edge loads. Pure equilibria exist by [Rosenthal's potential](/rosenthal-potential-theorem/), but their costs can differ, and the price of anarchy for affine costs is $5/2$ instead of $4/3$ ([atomic linear congestion bound](/atomic-linear-congestion-price-of-anarchy/)). The nonatomic model is the limit in which each player's share goes to 0.
- **Nonatomic congestion games.** Replace the paths of a network by arbitrary subsets of a set of resources. The potential and the Pigou bound arguments carry over without change, since they never use the graph structure.
- **Potential games.** The selfish routing model is a nonatomic [potential game](/potential-game/): its equilibria are the minimizers of one function, the Beckmann potential.
- **Min-cost flow.** With constant latencies $\ell_e(x) = a_e$, an equilibrium sends each commodity on shortest paths for the lengths $a_e$, and it is also optimal. With semiconvex latencies the optimum is a convex cost multicommodity flow, a nonlinear form of the [min-cost flow problem](/min-cost-flow-problem/).
- **Load balancing.** Parallel links with atomic weighted jobs and the makespan as the cost give the [load balancing game](/load-balancing-game/).
- **Dynamics, leaders and tolls.** [Nash flows over time](/nash-flows-over-time/) add travel times and queues. [Stackelberg routing](/stackelberg-routing/) lets a central leader route a part of the traffic first. [Marginal cost tolls](/marginal-cost-tolls/) change the latencies so that the optimum becomes an equilibrium.
- **Traffic planning.** In transportation the equilibrium is the *user equilibrium* of traffic assignment, and a common latency function is the Bureau of Public Roads function, a polynomial of degree 4 in the flow. In communication networks with source routing, a common latency is the M/M/1 delay $1/(u_e - x)$ of a link with capacity $u_e$, which is finite only for $x < u_e$.

## Known results in the model

All results hold for any number of commodities and any directed network, with continuous nondecreasing latencies, unless the item says otherwise.

- **Existence and uniqueness.** An equilibrium exists, and all equilibria have the same latency on every edge, so the same cost. The equilibria are exactly the minimizers of the convex function $\Phi(f) = \sum_e \int_0^{f_e} \ell_e(x)\,dx$ (Beckmann, McGuire and Winsten 1956; [Beckmann potential](/beckmann-potential/)).
- **Variational inequality.** A feasible flow $f$ is an equilibrium if and only if $\sum_e \ell_e(f_e) f_e \le \sum_e \ell_e(f_e) g_e$ for every feasible flow $g$ ([Wardrop equilibrium](/wardrop-equilibrium/)).
- **The optimum as an equilibrium.** With semiconvex, continuously differentiable latencies, a flow is optimal if and only if it is an equilibrium for the marginal cost latencies $\ell_e(x) + x \ell_e'(x)$ ([system optimal flow](/system-optimal-flow/)). Tolls equal to $f^*_e \ell_e'(f^*_e)$ make the optimum an equilibrium ([marginal cost tolls](/marginal-cost-tolls/)).
- **Price of anarchy, affine latencies.** At most $4/3$ in every network, and $4/3$ is reached by two parallel links ([Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/), [Pigou's example](/pigou-example/)).
- **Price of anarchy, any class.** For any class of latency functions, the price of anarchy is at most the Pigou bound of the class, the worst ratio on two parallel links. If the class contains the constant functions, the bound is tight, so the worst network is always a two-link network. For polynomials of degree at most $d$ with nonnegative coefficients the value is $\big(1 - d (d+1)^{-(d+1)/d}\big)^{-1}$, about $2.151$ for $d = 4$ ([Pigou bound](/pigou-bound/)).
- **Extra capacity instead of coordination.** For any continuous nondecreasing latencies, the cost of an equilibrium at rates $r$ is at most the cost of an optimal flow at rates $2r$ (Roughgarden and Tardos 2002; NRTV Theorem 18.29).
- **Braess's paradox.** Adding an edge can raise the equilibrium cost; with affine latencies by a factor of at most $4/3$ ([Braess's paradox](/braess-paradox/)). Finding the best subnetwork is hard ([Braess paradox detection hardness](/braess-paradox-detection-hardness/)).
- **Computation.** The equilibrium and the optimum are solutions of convex programs over the flow polytope. For affine latencies both are convex quadratic programs. The Frank-Wolfe method, a first-order method that solves a shortest path problem in each step, is the classical method of traffic planning for the equilibrium.

## References
