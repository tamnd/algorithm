---
tag: KA2E95
kind: definition
slug: system-optimal-flow
name: System optimal flow
aliases:
- system optimum
- socially optimal flow
area: algorithmic-game-theory/inefficiency-of-equilibria
level: intro
summary: A feasible flow of least total latency. If each x l(x) is convex and differentiable, it is the Wardrop equilibrium for the marginal cost latencies l(x) + x l'(x).
prereqs: [wardrop-equilibrium, beckmann-potential]
see_also: [price-of-anarchy, pigou-example, braess-paradox, marginal-cost-tolls, roughgarden-tardos-four-thirds-bound, min-cost-flow-problem, stackelberg-routing, convex-optimization-problem]
sources:
  - paper: doi:10.1680/ipeds.1952.11259
    title: "J. G. Wardrop, Some theoretical aspects of road traffic research, Proceedings of the Institution of Civil Engineers 1(3) (1952), 325-362"
    locator: the second principle (the average journey time is a minimum)
  - book: "Martin Beckmann, C. B. McGuire and Christopher B. Winsten, Studies in the Economics of Transportation, Yale University Press, 1956"
    locator: Part I (efficient use of a road network compared with the equilibrium, and congestion tolls)
  - paper: doi:10.6028/jres.073b.010
    title: "Stella C. Dafermos and Frederick T. Sparrow, The traffic assignment problem for a general network, Journal of Research of the National Bureau of Standards, Section B 73B(2) (1969), 91-118"
    locator: the terms user-optimized and system-optimized, and the conditions for a system-optimized flow
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 18, Tim Roughgarden, Routing games, Proposition 18.9 and Corollary 18.10 (optimal flows as equilibria for marginal cost functions) and Theorem 18.27 (marginal cost taxes)
  - paper: doi:10.1145/506147.506153
    title: "Tim Roughgarden and Eva Tardos, How bad is selfish routing?, Journal of the ACM 49(2) (2002), 236-259"
    locator: the characterization of optimal flows by marginal cost latencies and the bicriteria bound
---

A system optimal flow is a feasible flow of least total cost in the [selfish routing model](/selfish-routing-model/). It is the flow that a central planner picks when it can assign every traveler a route. Wardrop's second principle describes it: the average journey time is a minimum. It is the benchmark in the [price of anarchy](/price-of-anarchy/) of selfish routing, and in general it is not a [Wardrop equilibrium](/wardrop-equilibrium/), because some travelers on it have a shorter path that they do not use.

## Definition

Use the notation of the [selfish routing model](/selfish-routing-model/): an instance $(G, r, \ell)$ with commodities $i = 1, \ldots, k$, path sets $\mathcal{P}_i$, continuous nondecreasing latencies $\ell_e \ge 0$ and edge flows $f_e$. The cost of a flow is

$$C(f) = \sum_{P} f_P \, \ell_P(f) = \sum_{e \in E} f_e \, \ell_e(f_e).$$

**Definition.** A feasible flow $f^*$ is *system optimal* if $C(f^*) \le C(g)$ for every feasible flow $g$.

**Existence.** The feasible path flows form a compact polytope, a product of simplices scaled by the rates $r_i$, and $C$ is continuous. So a system optimal flow exists in every instance. The optimal cost is unique, but the optimal flow need not be. If every function $x \ell_e(x)$ is strictly convex, the optimal edge flows are unique.

**Semiconvex latencies and marginal costs.** A latency $\ell$ is *semiconvex* if $x \ell(x)$ is convex on $[0, \infty)$. Every nondecreasing convex latency is semiconvex, so this covers affine functions and polynomials with nonnegative coefficients. If every $\ell_e$ is semiconvex, finding $f^*$ is a convex program: minimize a separable convex function over the flow polytope ([convex optimization problem](/convex-optimization-problem/)). For a differentiable latency, the *marginal cost* latency is

$$\ell^*_e(x) = \frac{d}{dx}\big(x \, \ell_e(x)\big) = \ell_e(x) + x \, \ell'_e(x).$$

It is the extra total cost of one more unit of traffic on $e$. A new traveler pays $\ell_e(x)$, and the $x$ travelers already there each pay about $\ell'_e(x)$ more.

**Characterization.** Let every $\ell_e$ be semiconvex and continuously differentiable. Then a feasible flow $f^*$ is system optimal if and only if it is a Wardrop equilibrium for the latencies $\ell^*_e$. That is, for every commodity $i$ and paths $P, P' \in \mathcal{P}_i$,

$$f^*_P > 0 \implies \sum_{e \in P} \ell^*_e(f^*_e) \le \sum_{e \in P'} \ell^*_e(f^*_e).$$

*Proof.* Since $\int_0^{y} \ell^*_e(x)\,dx = y \, \ell_e(y)$, the cost is $C(f) = \sum_e \int_0^{f_e} \ell^*_e(x)\,dx$. This is the potential of the [Beckmann theorem](/beckmann-potential/) for the instance with latencies $\ell^*_e$. Each $\ell^*_e$ is continuous, it is nondecreasing because it is the derivative of a convex function, and it is nonnegative because $\ell_e \ge 0$ and $\ell'_e \ge 0$. So the Beckmann theorem applies to $\ell^*$: the minimizers of $C$ are exactly the equilibria for $\ell^*$. $\square$

In words, a system optimal flow is a selfish flow in which every traveler pays its marginal cost. The variational inequality form is $\sum_e \ell^*_e(f^*_e) f^*_e \le \sum_e \ell^*_e(f^*_e) g_e$ for all feasible $g$.

**Affine latencies.** If $\ell_e(x) = a_e x + b_e$ with $a_e, b_e \ge 0$, then $\ell^*_e(x) = 2 a_e x + b_e = \ell_e(2x)$. So if $h$ is a Wardrop equilibrium for $\ell$ at the rates $2r$, then $h/2$ is a Wardrop equilibrium for $\ell^*$ at the rates $r$, and $h/2$ is system optimal at the rates $r$. An optimal flow is half of an equilibrium flow for twice the traffic.

## Examples and non-examples

**Pigou's network.** Links $\ell_1(x) = 1$ and $\ell_2(x) = x$, rate 1. The marginal costs are $\ell^*_1(x) = 1$ and $\ell^*_2(x) = 2x$. They are equal at $f_2 = 1/2$, so $f^* = (1/2, 1/2)$ with cost $1/2 \cdot 1 + 1/2 \cdot 1/2 = 3/4$. The Wardrop equilibrium $(0, 1)$ costs 1, so the ratio is $4/3$ ([Pigou's example](/pigou-example/)). Check with the affine rule: at rate 2 the equilibrium is $(1, 1)$, and half of it is $(1/2, 1/2)$.

**Three parallel links.** Let $\ell_1(x) = x$, $\ell_2(x) = x + 1$, $\ell_3(x) = 2x + 1$ and $r = 3$. The marginal costs are $2x$, $2x + 1$ and $4x + 1$. At a common marginal cost $M$ the flows are $M/2$, $(M - 1)/2$ and $(M - 1)/4$, with sum $(5M - 3)/4$. This is 3 when $M = 3$, so $f^* = (3/2, 1, 1/2)$. The cost is $9/4 + 2 + 1 = 21/4$. The Wardrop equilibrium $(9/5, 4/5, 2/5)$ costs $27/5$, so the ratio is $(27/5)/(21/4) = 36/35$. At rate 6 the equilibrium is $(3, 2, 1)$ with common latency 3, and half of it is $f^*$.

**Braess's network.** Vertices $s, v, w, t$, latency $x$ on $s \to v$ and $w \to t$, latency 1 on $v \to t$ and $s \to w$, latency 0 on the shortcut $v \to w$, and rate 1. The flow with $1/2$ on each of $s \to v \to t$ and $s \to w \to t$ costs $3/2$. Its marginal costs are $2 \cdot 1/2 = 1$ on $s \to v$ and $w \to t$, 1 on the constant edges and 0 on the shortcut. So all three paths have marginal cost 2, and the flow is optimal. The shortcut is not used. The Wardrop equilibrium sends all traffic on the shortcut and costs 2 ([Braess's paradox](/braess-paradox/)). An extra edge can never raise the optimal cost, because the old optimal flow stays feasible.

**A non-example: a latency that is not semiconvex.** Let $\ell_1(x) = \min(x, 1)$, $\ell_2(x) = 3/2$ and rate 2. Then $x \ell_1(x)$ is $x^2$ on $[0, 1]$ and $x$ after 1, which is not convex. Away from $x = 1$, the marginal cost on link 1 is $2x$ below 1 and 1 above 1, and on link 2 it is $3/2$. Two flows satisfy the marginal cost condition: $f_1 = 3/4$, with cost $9/16 + 3/2 \cdot 5/4 = 39/16$, and $f_1 = 2$, with cost 2. Only the second one is optimal. Without semiconvexity, the marginal cost condition is necessary at a smooth point but not sufficient.

**A non-example: an optimal flow that a planner cannot keep without help.** In Pigou's network, the travelers on link 1 of $f^* = (1/2, 1/2)$ pay 1 while link 2 has latency $1/2$. Each of them gains by a switch, so $f^*$ is not an equilibrium for $\ell$. A toll of $1/2$ on link 2 makes it one: then both links cost 1 ([marginal cost tolls](/marginal-cost-tolls/)).

## Related definitions

- **Wardrop equilibrium.** The first principle: every used path is a shortest path for the actual latencies. It is the [Wardrop equilibrium](/wardrop-equilibrium/), and its cost divided by $C(f^*)$ is the [price of anarchy](/price-of-anarchy/) of the instance.
- **Marginal cost tolls.** The toll $\tau_e = f^*_e \, \ell'_e(f^*_e)$ on each edge makes $f^*$ a Wardrop equilibrium for the latencies $\ell_e(x) + \tau_e$, since these agree with $\ell^*_e$ at $f^*$ (NRTV Theorem 18.27; [marginal cost tolls](/marginal-cost-tolls/)).
- **Minimum cost flow.** If every latency is a constant $c_e$, then $C(f) = \sum_e c_e f_e$, the problem is a [minimum cost flow](/min-cost-flow-problem/) with no capacities, and each commodity takes a shortest path. Then the equilibrium is optimal too. With semiconvex latencies the problem is a convex cost flow problem.
- **Bicriteria bound.** A Wardrop equilibrium at the rates $r$ costs at most a system optimal flow at the rates $2r$, for every continuous nondecreasing latency ([Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/)).
- **Stackelberg routing.** A leader controls a fraction of the traffic and routes it so that the selfish rest comes close to the optimum ([Stackelberg routing](/stackelberg-routing/)).
- **User-optimized and system-optimized.** Dafermos and Sparrow (1969) named the Wardrop equilibrium and the system optimal flow this way, after Wardrop's first and second principles.

## References
