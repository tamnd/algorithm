---
tag: Y80G0W
kind: theorem
slug: beckmann-potential
name: Beckmann potential for selfish routing
aliases:
- Beckmann-McGuire-Winsten program
- equilibrium as convex minimization
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: Wardrop equilibria are the minimizers of the sum over edges of the integral of latency, so they exist and are found by convex optimization.
prereqs: [wardrop-equilibrium, convex-optimization-problem]
see_also: [system-optimal-flow, selfish-routing-model, rosenthal-potential-theorem, potential-game, price-of-stability, price-of-anarchy, convex-function, kkt-conditions]
sources:
  - book: "Martin Beckmann, C. B. McGuire and Christopher B. Winsten, Studies in the Economics of Transportation, Yale University Press, 1956"
    locator: Part I (the equilibrium of a road network as the solution of an optimization problem)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 18, Tim Roughgarden, Routing games, Proposition 18.11 (the potential function), Theorem 18.8 (existence and uniqueness) and Theorem 18.16 (price of anarchy bound from the potential)
  - paper: doi:10.1016/0191-2615(79)90022-5
    title: "M. J. Smith, The existence, uniqueness and stability of traffic equilibria, Transportation Research Part B 13(4) (1979), 295-304"
    locator: the variational inequality form of the equilibrium
  - paper: doi:10.1016/0041-1647(75)90030-1
    title: "Larry J. LeBlanc, Edward K. Morlok and William P. Pierskalla, An efficient approach to solving the road network equilibrium traffic assignment problem, Transportation Research 9(5) (1975), 309-318"
    locator: the Frank-Wolfe method applied to the Beckmann program
  - paper: doi:10.1680/ipeds.1952.11259
    title: "J. G. Wardrop, Some theoretical aspects of road traffic research, Proceedings of the Institution of Civil Engineers 1(3) (1952), 325-362"
    locator: the first principle of route choice
  - paper: doi:10.6028/jres.073b.010
    title: "Stella C. Dafermos and Frederick T. Sparrow, The traffic assignment problem for a general network, Journal of Research of the National Bureau of Standards, Section B 73B(2) (1969), 91-118"
    locator: algorithms for the user-optimized and system-optimized flows
  - paper: doi:10.1145/506147.506153
    title: "Tim Roughgarden and Eva Tardos, How bad is selfish routing?, Journal of the ACM 49(2) (2002), 236-259"
    locator: the use of the equilibrium and optimum characterizations in the price of anarchy analysis
---

The Beckmann potential is the function $\Phi(f) = \sum_e \int_0^{f_e} \ell_e(x)\,dx$ on the flows of a [selfish routing](/selfish-routing-model/) instance. Beckmann, McGuire and Winsten showed in 1956 that the [Wardrop equilibria](/wardrop-equilibrium/) are exactly the minimizers of this convex function. So an equilibrium always exists, all equilibria have the same edge latencies and the same cost, and an equilibrium can be computed by convex optimization. The cost $C(f) = \sum_e f_e \ell_e(f_e)$ has a different integrand, and this is why the equilibrium and the [system optimal flow](/system-optimal-flow/) differ.

## Statement

**Theorem (Beckmann, McGuire and Winsten 1956).** Let $(G, r, \ell)$ be a nonatomic selfish routing instance with $k$ commodities and continuous nondecreasing latencies $\ell_e : [0, \infty) \to [0, \infty)$. Let $\mathcal{F}$ be the set of feasible flows and

$$\Phi(f) = \sum_{e \in E} \int_0^{f_e} \ell_e(x)\,dx.$$

1. A flow $f \in \mathcal{F}$ is a Wardrop equilibrium if and only if $\Phi(f) = \min_{g \in \mathcal{F}} \Phi(g)$.
2. A Wardrop equilibrium exists.
3. If $f$ and $\tilde f$ are Wardrop equilibria, then $\ell_e(f_e) = \ell_e(\tilde f_e)$ for every edge $e$. So the shortest path latencies $L_i$ and the cost $C(f) = \sum_i r_i L_i(f)$ are the same for all equilibria.

The equilibrium is a pure equilibrium of the nonatomic game. No mixed strategies are needed.

## In plain words

Give each road a score that grows with its traffic. The score of a road is the area under its delay curve up to the current traffic. Add the scores of all roads. When one driver moves to a faster route, the total score goes down by an amount equal to the time that driver saves. So the total score is a hidden quantity that selfish drivers always push down. Where it cannot go down any more, no driver can save time, and that is an equilibrium. The score is a bowl shape with no false bottoms, so a lowest point exists, and every lowest point gives each road the same delay.

## Proof

Write $h_e(y) = \int_0^y \ell_e(x)\,dx$, so $\Phi(f) = \sum_e h_e(f_e)$. Since $\ell_e$ is continuous, $h_e$ is continuously differentiable with $h'_e = \ell_e$. Since $\ell_e$ is nondecreasing, $h_e$ is convex. Each edge flow $f_e = \sum_{P \ni e} f_P$ is a linear function of the path flows, so $\Phi$ is a convex and continuously differentiable function of the path flows. The set $\mathcal{F}$ is a nonempty compact convex polytope: a product over the commodities of simplices scaled by $r_i$.

*Part 1.* For $f, g \in \mathcal{F}$ and $t \in [0, 1]$, the flow $f + t(g - f)$ is feasible, and the derivative of $\Phi(f + t(g - f))$ at $t = 0$ is

$$D(f; g) = \sum_e \ell_e(f_e) \, (g_e - f_e).$$

If $f$ minimizes $\Phi$, then $D(f; g) \ge 0$ for every $g$, or else $\Phi$ would decrease for small $t > 0$. If $D(f; g) \ge 0$ for every $g$, then convexity gives $\Phi(g) \ge \Phi(f) + D(f; g) \ge \Phi(f)$, so $f$ minimizes $\Phi$. So $f$ is a minimizer if and only if

$$\sum_e \ell_e(f_e) \, f_e \le \sum_e \ell_e(f_e) \, g_e \quad \text{for all } g \in \mathcal{F}.$$

This variational inequality holds if and only if $f$ is a Wardrop equilibrium. To see this, expand both sides in path flows: the right side is $\sum_P \ell_P(f) g_P$, and over feasible $g$ its least value is $\sum_i r_i L_i(f)$, reached by putting each commodity on a shortest path. The left side is $\sum_P \ell_P(f) f_P \ge \sum_i r_i L_i(f)$, with equality exactly when every used path is a shortest path ([Wardrop equilibrium](/wardrop-equilibrium/) gives the details).

*Part 2.* $\Phi$ is continuous on the nonempty compact set $\mathcal{F}$, so it has a minimizer. By part 1 it is an equilibrium.

*Part 3.* Let $f$ and $\tilde f$ be equilibria. By part 1 both minimize $\Phi$, with value $m$. For $t \in [0, 1]$ let $g = (1 - t) f + t \tilde f$, which is feasible. Then

$$m \le \Phi(g) = \sum_e h_e\big((1 - t) f_e + t \tilde f_e\big) \le \sum_e \big((1 - t) h_e(f_e) + t \, h_e(\tilde f_e)\big) = m.$$

So the middle inequality is an equality. Each edge term satisfies the convexity inequality on its own, so each term is an equality, for every $t \in [0, 1]$. So $h_e$ is affine on the interval between $f_e$ and $\tilde f_e$. Its derivative $\ell_e$ is constant on the open interval, and by continuity also at the two ends. So $\ell_e(f_e) = \ell_e(\tilde f_e)$. The path latencies and the $L_i$ depend only on the edge latencies, so they agree too, and $C(f) = \sum_i r_i L_i(f) = C(\tilde f)$. $\square$

**Example.** In Pigou's network, $\ell_1(x) = 1$, $\ell_2(x) = x$ and rate 1, put $x$ on link 2. Then $\Phi = (1 - x) + x^2/2$, with derivative $x - 1 \le 0$ on $[0, 1]$. The minimum is at $x = 1$, which is the equilibrium, with $\Phi = 1/2$ and cost 1. The cost $C = (1 - x) + x^2$ has its minimum at $x = 1/2$ instead ([Pigou's example](/pigou-example/)). For three links $\ell = x$, $x + 1$, $2x + 1$ and $r = 3$, the potential is $x_1^2/2 + (x_2^2/2 + x_2) + (x_3^2 + x_3)$. Setting the three partial derivatives equal gives $x_1 = x_2 + 1 = 2 x_3 + 1$, which is the equilibrium condition, with solution $(9/5, 4/5, 2/5)$.

## Consequences

- **The price of stability equals the price of anarchy.** All equilibria of a nonatomic instance have the same cost, so the best and the worst equilibrium agree ([price of stability](/price-of-stability/), [price of anarchy](/price-of-anarchy/)).
- **Computation.** An equilibrium is the solution of a convex program with linear constraints. It can be written with edge flows and one flow vector per commodity, so its size is polynomial in the network. For affine latencies $\Phi$ is a convex quadratic function. The standard method in transport planning is the Frank-Wolfe method, which solves one shortest path problem per commodity in each step (LeBlanc, Morlok and Pierskalla 1975). The [KKT conditions](/kkt-conditions/) of the program are the Wardrop conditions, with the multiplier of commodity $i$ equal to $L_i$.
- **Optimal flows.** The cost is $C(f) = \sum_e \int_0^{f_e} \ell^*_e(x)\,dx$ with $\ell^*_e(x) = \ell_e(x) + x \ell'_e(x)$. So the theorem applied to $\ell^*$ shows that, for semiconvex differentiable latencies, a [system optimal flow](/system-optimal-flow/) is an equilibrium for the marginal costs.
- **A first price of anarchy bound.** Suppose $x \ell_e(x) \le \gamma \int_0^x \ell_e(t)\,dt$ for all edges and all $x \ge 0$. Since $\ell_e$ is nondecreasing, $\int_0^x \ell_e \le x \ell_e(x)$, so $\Phi(g) \le C(g)$ for every flow. For an equilibrium $f$ and an optimal flow $f^*$, $C(f) \le \gamma \Phi(f) \le \gamma \Phi(f^*) \le \gamma C(f^*)$. For polynomials of degree at most $d$ with nonnegative coefficients, $\gamma = d + 1$, so the price of anarchy is at most $d + 1$ (NRTV Theorem 18.16). For affine latencies this gives 2. The exact value $4/3$ needs a different proof ([Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/)).
- **Potential games.** The nonatomic routing game is a [potential game](/potential-game/): a move of a small amount $\delta$ of traffic from path $P$ to path $P'$ changes $\Phi$ by about $\delta (\ell_{P'}(f) - \ell_P(f))$. The sum $\sum_e \sum_{j=1}^{f_e} c_e(j)$ of [Rosenthal's theorem](/rosenthal-potential-theorem/) for atomic congestion games is the discrete form of the same function.

## Tightness

- **Path flows are not unique.** Let $s \to v$ have two parallel edges $a, b$ and $v \to t$ two parallel edges $c, d$, each with $\ell(x) = x$, and rate 1. The path flows $(f_{ac}, f_{ad}, f_{bc}, f_{bd}) = (1/2, 0, 0, 1/2)$ and $(1/4, 1/4, 1/4, 1/4)$ are both equilibria, with the same edge flows. Part 3 speaks of edge latencies only.
- **Edge flows are not unique.** Two parallel links with $\ell_1(x) = \ell_2(x) = 1$ and rate 1: every split is an equilibrium. The edge latencies are all 1, as part 3 says. If every $\ell_e$ is strictly increasing, the edge flows are unique as well.
- **Monotone latencies are needed.** Let two parallel links have $\ell_1(x) = \ell_2(x) = 1 - x/2$ on $[0, 1]$ and rate 1. These latencies decrease. The flow $(1, 0)$ is an equilibrium: the used link has latency $1/2$ and the empty one has 1. Its cost is $1/2$. The flow $(1/2, 1/2)$ is also an equilibrium, with latency $3/4$ on both links and cost $3/4$. Here $\Phi$ is concave, and $(1/2, 1/2)$ is its maximum on the segment of feasible flows.
- **Atomic players.** If each player controls a positive amount of traffic, the game is an [atomic congestion game](/atomic-congestion-game/). Rosenthal's potential still gives a pure equilibrium, but different equilibria can have different costs, so the price of stability and the price of anarchy can differ.

## History

Wardrop stated the equilibrium principle for road traffic in 1952. Beckmann, McGuire and Winsten, in *Studies in the Economics of Transportation* (1956), wrote the equilibrium as the solution of the convex program with the objective $\Phi$. They used it to prove existence and the uniqueness of the edge latencies, and they also proved the marginal cost form of the optimum and the marginal cost tolls (NRTV, notes to Chapter 18). Dafermos and Sparrow (1969) gave algorithms for general networks, and LeBlanc, Morlok and Pierskalla (1975) applied the Frank-Wolfe method, which became the standard in traffic assignment. Smith (1979) gave the variational inequality form, which also covers latencies that depend on the flow of other edges, where no potential exists in general. In algorithmic game theory, the price of anarchy analysis of Roughgarden and Tardos (2002) starts from these characterizations of the equilibrium and the optimum.

## References
