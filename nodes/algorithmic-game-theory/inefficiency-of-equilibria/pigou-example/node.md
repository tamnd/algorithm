---
tag: YNTJ6A
kind: concept
slug: pigou-example
name: Pigou's example
aliases:
- Pigou network
area: algorithmic-game-theory/inefficiency-of-equilibria
level: intro
summary: A two-link network with latencies 1 and x in which the equilibrium cost is 4/3 of the optimum, the worst case for affine latencies.
prereqs: [wardrop-equilibrium, system-optimal-flow, price-of-anarchy]
see_also: [roughgarden-tardos-four-thirds-bound, pigou-bound, braess-paradox, marginal-cost-tolls, stackelberg-routing, selfish-routing-model, beckmann-potential, price-of-anarchy-of-load-balancing]
sources:
  - book: "A. C. Pigou, The Economics of Welfare, Macmillan, London, 1920"
    locator: the example of two roads, one congested and one not, and the tax that corrects the overuse of the congested road
  - paper: doi:10.2307/1884592
    title: "Frank H. Knight, Some fallacies in the interpretation of social cost, Quarterly Journal of Economics 38(4) (1924)"
    locator: the discussion of the two-road example
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 17, Tim Roughgarden and Eva Tardos, Introduction to the inefficiency of equilibria, Example 17.1 (Pigou's example), and Chapter 18, Tim Roughgarden, Routing games, Example 18.3 (the nonlinear variant), Example 18.28 and Proposition 18.19
  - paper: doi:10.1145/506147.506153
    title: "Tim Roughgarden and Eva Tardos, How bad is selfish routing?, Journal of the ACM 49(2) (2002), 236-259"
    locator: the two-link example and its nonlinear variant as lower bounds on the price of anarchy
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 11 (Pigou's example and Pigou-like networks)
---

Pigou's example is the smallest network in which selfish routing is inefficient. One unit of traffic goes from $s$ to $t$ over two parallel links. The upper link has constant latency 1, and the lower link has latency $x$ when it carries $x$ units. At the [Wardrop equilibrium](/wardrop-equilibrium/) all traffic takes the lower link, at cost 1. The [system optimal flow](/system-optimal-flow/) splits the traffic in half, at cost $3/4$. The ratio $4/3$ is the largest possible [price of anarchy](/price-of-anarchy/) for affine latencies in any network ([Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/)), and networks of this two-link form give the worst case for every class of latencies that contains the constants ([Pigou bound](/pigou-bound/)).

## In plain words

There are two roads from home to work. The first road is long and wide, and it always takes one hour. The second road is short and narrow, and it takes as long as the share of drivers on it, so it takes one hour only when everyone uses it. Each driver sees that the narrow road is never slower, so everyone takes it, and everyone needs one hour. If half the drivers took the wide road, they would still need one hour, but the other half would need only half an hour. A driver on the narrow road slows down all the others there, and does not pay for it.

## The idea

**The network.** Vertices $s$ and $t$, link 1 with $\ell_1(x) = 1$, link 2 with $\ell_2(x) = x$, and rate $r = 1$. A flow is $(1 - y, y)$ with $y$ on link 2.

**The equilibrium.** Link 2 has latency $y \le 1 = \ell_1$. If $y < 1$, the travelers on link 1 pay 1 and link 2 is faster, so they move. So $y = 1$ is the unique equilibrium, with both links at latency 1 and cost $C = 1$.

**The optimum.** The cost is $C(y) = (1 - y) + y^2$. Its derivative $2y - 1$ is 0 at $y = 1/2$. So the optimum is $(1/2, 1/2)$ with cost $1/2 + 1/4 = 3/4$. In marginal cost terms, $\ell^*_1(x) = 1$ and $\ell^*_2(x) = 2x$, and they agree at $y = 1/2$.

**The ratio.** $C(\text{eq}) / C(\text{opt}) = 1 / (3/4) = 4/3$.

**Why it happens.** A traveler on link 2 pays $\ell_2(y) = y$, but the total cost grows by the marginal cost $\ell^*_2(y) = 2y$, because each extra traveler also slows the $y$ travelers already there. At the equilibrium, the last traveler on link 2 pays 1 and adds 2 to the total cost. This gap between private and social cost is a negative externality. Pigou's remedy is a tax equal to the gap at the optimum: a toll of $1/2$ on link 2. Then link 2 costs $y + 1/2$, the equilibrium becomes $y = 1/2$, and the latency cost is $3/4$ ([marginal cost tolls](/marginal-cost-tolls/)).

**Pigou-like networks.** Replace $\ell_2$ by any nondecreasing $\ell$, set the rate to $r$ and the constant link to $\ell(r)$. All traffic on link 2 is still an equilibrium, with cost $r \ell(r)$, and $x$ units on link 2 cost $x \ell(x) + (r - x) \ell(r)$. The worst ratio over such networks is the [Pigou bound](/pigou-bound/) of the class.

## Examples

**The rate matters.** Keep $\ell_1 = 1$ and $\ell_2 = x$ and change the rate $r$.

| rate $r$ | equilibrium | cost | optimum | cost | ratio |
|---|---|---|---|---|---|
| $1/4$ | $(0, 1/4)$ | $1/16$ | $(0, 1/4)$ | $1/16$ | 1 |
| $1/2$ | $(0, 1/2)$ | $1/4$ | $(0, 1/2)$ | $1/4$ | 1 |
| $3/4$ | $(0, 3/4)$ | $9/16$ | $(1/4, 1/2)$ | $1/2$ | $9/8$ |
| $1$ | $(0, 1)$ | $1$ | $(1/2, 1/2)$ | $3/4$ | $4/3$ |
| $2$ | $(1, 1)$ | $2$ | $(3/2, 1/2)$ | $7/4$ | $8/7$ |

For $r \le 1$ the equilibrium costs $r^2$, and for $r > 1/2$ the optimum costs $r - 1/4$. The ratio $r^2 / (r - 1/4)$ increases on $(1/2, 1]$, so rate 1 is the worst. Above rate 1 the extra traffic goes to link 1 in both flows, and the ratio falls toward 1.

**The nonlinear variant.** Let $\ell_2(x) = x^d$ with rate 1. The equilibrium is still all on link 2, with cost 1. The optimum puts $y = (d + 1)^{-1/d}$ on link 2, where the marginal cost $(d + 1) y^d$ equals 1.

| $d$ | $y$ on link 2 | optimal cost | ratio |
|---|---|---|---|
| 1 | 0.5 | 0.75 | 1.333 |
| 2 | 0.5774 | 0.6151 | 1.626 |
| 3 | 0.6300 | 0.5275 | 1.896 |
| 10 | 0.7868 | 0.2847 | 3.512 |

As $d$ grows, the optimal cost tends to 0: almost all traffic stays on link 2, where the latency is $y^d \approx 0$, and a small amount on link 1 pays 1. So the price of anarchy is unbounded for polynomials of unbounded degree, and grows like $d / \ln d$ (NRTV Example 18.3).

**Twice the traffic.** In the same variant at rate 2, an optimal flow puts a little less than 1 on link 2 and the rest on link 1, so its cost tends to 1 as $d$ grows. This is the equilibrium cost at rate 1. So the bound "an equilibrium costs at most the optimum for twice the traffic" is tight (NRTV Example 18.28).

**A leader on link 1.** If a central authority controls half of the traffic and puts it on link 1, the other half sees link 2 at latency at most $1/2$ and takes it. The result is the optimum $(1/2, 1/2)$ ([Stackelberg routing](/stackelberg-routing/)).

**Atomic players.** With two players of $1/2$ each who cannot split, the profile with both on link 2 costs each player 1, and a move to link 1 also costs 1, so it is an equilibrium with total cost 1. The profile with one player on each link costs $1/2 \cdot 1 + 1/2 \cdot 1/2 = 3/4$ and is also an equilibrium, because the player on link 2 would pay 1 on link 1 and the player on link 1 would pay 1 on link 2. Here the equilibria have different costs, unlike the nonatomic case.

## Where it is used

- **Lower bounds.** It shows that the $4/3$ bound for affine latencies is tight, and its nonlinear variant shows that no constant bound holds for all polynomials ([Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/)).
- **The Pigou bound.** Two-link networks of this form give the exact price of anarchy for every class that contains the constants ([Pigou bound](/pigou-bound/)).
- **Pricing.** It is the standard example of a negative externality and of a corrective tax, which is why marginal cost tolls are also called Pigouvian taxes ([marginal cost tolls](/marginal-cost-tolls/)).
- **A first test case.** It is small enough to check by hand any method that computes a [Wardrop equilibrium](/wardrop-equilibrium/), a system optimal flow, or a [Beckmann potential](/beckmann-potential/) minimizer: the potential $(1 - y) + y^2/2$ is least at $y = 1$, and the cost $(1 - y) + y^2$ is least at $y = 1/2$.
- **Other games.** The same gap between a self-interested choice and the planner's choice appears in [load balancing](/price-of-anarchy-of-load-balancing/), where jobs of sizes 2, 2, 1 and 1 on two identical machines have a pure equilibrium with makespan 4 against the optimum 3, again a ratio of $4/3$.

**History.** Pigou described a version with two roads in *The Economics of Welfare* (1920), one wide but poor and one narrow but good, to argue for a tax on the congested road. Knight (1924) answered that an owner of the good road would charge a toll with the same effect. Roughgarden and Tardos (2002) used the network, with the latencies 1 and $x$, as the basic lower bound for the price of anarchy of selfish routing.

## References
