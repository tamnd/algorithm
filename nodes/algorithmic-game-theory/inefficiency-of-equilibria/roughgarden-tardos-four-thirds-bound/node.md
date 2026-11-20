---
tag: K6989X
kind: theorem
slug: roughgarden-tardos-four-thirds-bound
name: Price of anarchy for linear latencies
aliases:
- Roughgarden-Tardos theorem
- 4/3 bound for selfish routing
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: In nonatomic selfish routing with affine latency functions, the cost of a Wardrop equilibrium is at most 4/3 times the optimal cost.
prereqs: [price-of-anarchy, wardrop-equilibrium, system-optimal-flow, pigou-example]
see_also: [pigou-bound, braess-paradox, beckmann-potential, smoothness-framework, atomic-linear-congestion-price-of-anarchy, marginal-cost-tolls, selfish-routing-model, price-of-stability]
sources:
  - paper: doi:10.1145/506147.506153
    title: "Tim Roughgarden and Eva Tardos, How bad is selfish routing?, Journal of the ACM 49(2) (2002), 236-259"
    locator: the 4/3 bound for linear latency functions and the bicriteria bound for general latency functions
  - paper: doi:10.1287/moor.1040.0098
    title: "Jose R. Correa, Andreas S. Schulz and Nicolas E. Stier-Moses, Selfish routing in capacitated networks, Mathematics of Operations Research 29(4) (2004), 961-976"
    locator: the short proof of the price of anarchy bounds from the variational inequality, without convexity assumptions
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 18, Tim Roughgarden, Routing games, Section 18.4.1 (Theorem 18.21 and Remark 18.22), Exercise 18.6 (concave latencies), Section 18.5.2 (Example 18.28, Theorem 18.29 and Corollary 18.30) and Section 18.6 (notes)
  - paper: doi:10.1016/S0022-0000(03)00044-8
    title: "Tim Roughgarden, The price of anarchy is independent of the network topology, Journal of Computer and System Sciences 67(2) (2003), 341-364"
    locator: the Pigou bound and the reduction of the worst case to two-link networks
  - paper: doi:10.1007/3-540-49116-3_38
    title: "Elias Koutsoupias and Christos Papadimitriou, Worst-case equilibria, STACS 1999, Lecture Notes in Computer Science 1563, 404-413"
    locator: the worst-case ratio of equilibrium cost to optimal cost
  - book: isbn:9780262182430
    title: Tim Roughgarden, Selfish Routing and the Price of Anarchy, MIT Press, 2005
    locator: Chapter 3, How Bad Is Selfish Routing?, Section 3.2 (linear cost functions)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 11 (selfish routing and the price of anarchy)
  - paper: doi:10.1016/0191-2615(79)90022-5
    title: "M. J. Smith, The existence, uniqueness and stability of traffic equilibria, Transportation Research Part B 13(4) (1979), 295-304"
    locator: the variational inequality form of the equilibrium
---

The Roughgarden-Tardos theorem says that selfish routing with affine latencies loses at most a third of the optimal cost. In any network, with any number of commodities, the cost of a [Wardrop equilibrium](/wardrop-equilibrium/) is at most $4/3$ times the cost of a [system optimal flow](/system-optimal-flow/). The bound is reached exactly by [Pigou's example](/pigou-example/), and it does not depend on the size or shape of the network. The same paper proved a second bound that needs no condition on the latencies: an equilibrium costs no more than an optimal flow that routes twice the traffic.

## Statement

**Theorem (Roughgarden and Tardos 2002).** Let $(G, r, \ell)$ be a nonatomic [selfish routing](/selfish-routing-model/) instance with $k$ commodities in which every latency is affine, $\ell_e(x) = a_e x + b_e$ with $a_e, b_e \ge 0$. Let $f$ be a Wardrop equilibrium and $f^*$ any feasible flow. Then

$$C(f) \le \tfrac{4}{3}\, C(f^*).$$

The equilibrium is the pure equilibrium of the nonatomic game. It exists, and all equilibria have the same cost ([Beckmann potential](/beckmann-potential/)). So the [price of anarchy](/price-of-anarchy/) and the [price of stability](/price-of-stability/) of every such instance are equal and at most $4/3$, and the bound is tight.

**Theorem (bicriteria bound, Roughgarden and Tardos 2002).** Let $(G, r, \ell)$ be a nonatomic instance with continuous nondecreasing latencies of any form. If $f$ is a Wardrop equilibrium for the rates $r$ and $f^*$ is a feasible flow for the rates $2r$, then $C(f) \le C(f^*)$.

## In plain words

Take any road network in which the delay on each road grows in a straight line with its traffic. Let every driver pick a fastest route. Then the total travel time is at most a third more than the best total that a central planner could reach. The size and shape of the network do not matter. A network with only two roads already loses that third, so no better bound is possible. For roads whose delay grows in any other way, selfish routing can be very bad. But it is never worse than the best plan for twice as many drivers.

## Proof

**A one-edge inequality.** Let $\ell(x) = a x + b$ with $a, b \ge 0$. For all $x, y \ge 0$,

$$y \, \ell(x) \le y \, \ell(y) + \tfrac{1}{4} x \, \ell(x).$$

Indeed, $y \ell(x) - y \ell(y) = a y (x - y)$. The product $y(x - y)$ is at most $x^2/4$, with equality at $y = x/2$. So $y \ell(x) - y \ell(y) \le a x^2 / 4 \le (a x^2 + b x)/4 = x \ell(x)/4$.

**The 4/3 bound.** Let $f$ be an equilibrium and $f^*$ feasible. By the variational inequality of a Wardrop equilibrium (Smith 1979; [Wardrop equilibrium](/wardrop-equilibrium/) proves it), $\sum_e \ell_e(f_e) f_e \le \sum_e \ell_e(f_e) f^*_e$. Apply the one-edge inequality with $x = f_e$ and $y = f^*_e$ on each edge:

$$C(f) = \sum_e f_e \, \ell_e(f_e) \le \sum_e f^*_e \, \ell_e(f_e) \le \sum_e f^*_e \, \ell_e(f^*_e) + \tfrac{1}{4} \sum_e f_e \, \ell_e(f_e) = C(f^*) + \tfrac{1}{4} C(f).$$

So $\tfrac{3}{4} C(f) \le C(f^*)$. $\square$

The first step compares $f$ with $f^*$ at the frozen latencies $\ell_e(f_e)$. The second step pays for the change from frozen to actual latencies with a quarter of the equilibrium cost.

**The bicriteria bound.** Let $f$ be an equilibrium for the rates $r$, let $L_i$ be the shortest path latency of commodity $i$ under $f$, so $C(f) = \sum_i r_i L_i$, and let $f^*$ be feasible for $2r$. Define new latencies $\bar\ell_e(x) = \max\{\ell_e(f_e), \ell_e(x)\}$ and let $\bar C$ be the cost under them.

First, $\bar\ell_e(x) - \ell_e(x)$ is 0 for $x \ge f_e$ and at most $\ell_e(f_e)$ for $x < f_e$. So $x(\bar\ell_e(x) - \ell_e(x)) \le f_e \ell_e(f_e)$ for all $x \ge 0$, and

$$\bar C(f^*) - C(f^*) = \sum_e f^*_e \big(\bar\ell_e(f^*_e) - \ell_e(f^*_e)\big) \le \sum_e f_e \, \ell_e(f_e) = C(f).$$

Second, $\bar\ell_e \ge \ell_e(f_e)$, so every path $P \in \mathcal{P}_i$ has $\bar\ell_P(f^*) \ge \ell_P(f) \ge L_i$. Then

$$\bar C(f^*) = \sum_i \sum_{P \in \mathcal{P}_i} \bar\ell_P(f^*) \, f^*_P \ge \sum_i L_i \cdot 2 r_i = 2\, C(f).$$

Together, $C(f^*) \ge \bar C(f^*) - C(f) \ge 2C(f) - C(f) = C(f)$. $\square$

**Example.** In Pigou's network, $\ell_1(x) = 1$, $\ell_2(x) = x$ and rate 1, the equilibrium is $f = (0, 1)$ and the optimum is $f^* = (1/2, 1/2)$. On link 2 the one-edge inequality with $x = 1$ and $y = 1/2$ reads $1/2 \le 1/4 + 1/4$, an equality. On link 1, with $a = 0$ and $x = 0$, it reads $1/2 \le 1/2$. The variational inequality reads $1 \le 1/2 \cdot 1 + 1/2 \cdot 1 = 1$. Every step is tight, and $C(f) = 1 = \tfrac{4}{3} \cdot \tfrac{3}{4}$. For the bicriteria bound, the optimum of the same network at rate 2 is $(3/2, 1/2)$ with cost $3/2 + 1/4 = 7/4 \ge 1$.

## Consequences

- **Independence of the network.** The worst ratio for affine latencies over all multicommodity networks is the same as over two parallel links. Roughgarden (2003) proved the same for every class of latencies that contains the constants ([Pigou bound](/pigou-bound/)).
- **Polynomial latencies.** The same proof with the inequality $y \ell(x) \le y \ell(y) + \beta x \ell(x)$ gives $C(f) \le (1 - \beta)^{-1} C(f^*)$. For polynomials of degree at most $d$ with nonnegative coefficients the best $\beta$ gives $[1 - d (d + 1)^{-(d + 1)/d}]^{-1}$, which is about $1.626$ for $d = 2$ and $1.896$ for $d = 3$.
- **Braess's paradox is bounded.** The old equilibrium stays feasible after edges are added, so it costs at least the new optimum. So for affine latencies the new equilibrium costs at most $4/3$ times the old one, and Braess's network reaches this: 2 against $3/2$ ([Braess's paradox](/braess-paradox/); NRTV Remark 18.22).
- **Concave latencies.** The bound $4/3$ also holds for all nonnegative, nondecreasing, concave latencies, because the Pigou bound of that class is $4/3$ (NRTV Exercise 18.6).
- **Smoothness.** The one-edge inequality is a nonatomic form of the condition in the [smoothness framework](/smoothness-framework/), with $\lambda = 1$ and $\mu = 1/4$, and $1/(1 - 1/4) = 4/3$. For atomic players with unit demands and affine costs the smoothness bound is $5/2$ instead ([atomic linear congestion bound](/atomic-linear-congestion-price-of-anarchy/)).
- **Faster links beat central control.** The bicriteria bound has an equivalent form: the equilibrium for the latencies $\ell_e(x/2)/2$ costs at most the optimum for $\ell_e$ (NRTV Corollary 18.30). For the M/M/1 delay $\ell_e(x) = 1/(u_e - x)$ the new latency is $1/(2u_e - x)$, so doubling every capacity is as good as optimal routing.
- **Tolls.** If tolls are allowed, the marginal cost tolls make the optimum an equilibrium, and the price of anarchy becomes 1 for the latency cost ([marginal cost tolls](/marginal-cost-tolls/)).

## Tightness

- **The constant 4/3.** Pigou's network reaches $4/3$ exactly, at rate 1. At rate $r$ the ratio is $r^2/(r - 1/4)$ for $1/2 < r \le 1$ and 1 for $r \le 1/2$, so the worst rate is 1 ([Pigou's example](/pigou-example/)).
- **Affine is needed.** With $\ell_2(x) = x^d$ in Pigou's network the ratio grows without bound as $d$ grows, like $d / \ln d$. No constant bound holds for all continuous nondecreasing latencies.
- **The factor 2.** With $\ell_1(x) = 1$, $\ell_2(x) = x^d$, the equilibrium at rate 1 costs 1. At rate 2 an optimal flow puts a little less than 1 on link 2 at almost no cost and the rest on link 1, so its cost tends to 1 as $d$ grows (NRTV Example 18.28). So the rate $2r$ cannot be replaced by $(2 - \varepsilon) r$ for a fixed $\varepsilon > 0$ and all latencies.
- **Atomic players.** Neither bound holds when players control a positive amount of traffic. The atomic affine case has price of anarchy $5/2$, and the bicriteria bound has an atomic counterexample (NRTV, notes to Chapter 18).

## History

Koutsoupias and Papadimitriou (1999) proposed the worst-case ratio of an equilibrium to the optimum for a simple routing game on parallel links. Roughgarden and Tardos (2002) studied the ratio for nonatomic routing in general networks. They proved the $4/3$ bound for linear latencies, the $d + 1$ bound from the potential, and the bicriteria bound. Their original argument was different. The short proof above uses the variational inequality of Smith (1979), and it follows Correa, Schulz and Stier-Moses (2004), who proved the general bound with no convexity assumption. Roughgarden (2003) introduced the Pigou bound and showed, under a convexity assumption, that the worst instance is a two-link network for every class that contains the constants.

## References
