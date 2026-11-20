---
tag: B2BYV7
kind: technique
slug: marginal-cost-tolls
name: Marginal cost tolls
aliases:
- Pigouvian tolls
- congestion pricing
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: Charging each edge the toll x l'(x) at the optimal flow makes the optimal flow a Wardrop equilibrium of the tolled network.
prereqs: [system-optimal-flow, wardrop-equilibrium, selfish-routing-model]
see_also: [pigou-example, braess-paradox, beckmann-potential, price-of-anarchy, stackelberg-routing, kkt-conditions, vcg-mechanism, braess-paradox-detection-hardness]
sources:
  - book: "Arthur C. Pigou, The Economics of Welfare, Macmillan, 1920"
    locator: the proposal to tax a congested road so that private and social cost agree
  - book: "Martin Beckmann, C. B. McGuire and Christopher B. Winsten, Studies in the Economics of Transportation, Yale University Press, 1956"
    locator: "Part I (the optimal flow as an equilibrium for marginal costs, and congestion tolls)"
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: "Chapter 18, Tim Roughgarden, Routing games (optimal flows as equilibria for marginal cost functions, and marginal cost taxes)"
  - paper: "Richard Cole, Yevgeniy Dodis and Tim Roughgarden, How much can taxes help selfish routing?, Journal of Computer and System Sciences 72(3) (2006), 444-467; EC 2003"
    locator: "the cost of marginal cost taxes when taxes count in the cost, and the comparison of taxes with edge removal"
  - paper: "Richard Cole, Yevgeniy Dodis and Tim Roughgarden, Pricing network edges for heterogeneous selfish users, STOC 2003"
    locator: tolls that induce the optimal flow when users differ in how much they care about tolls
  - paper: "Lisa Fleischer, Kamal Jain and Mohammad Mahdian, Tolls for heterogeneous selfish users in multicommodity networks and generalized congestion games, FOCS 2004, 277-285"
    locator: existence and computation of optimal tolls for heterogeneous users in multicommodity networks
  - paper: "George Karakostas and Stavros G. Kolliopoulos, Edge pricing of multicommodity networks for heterogeneous selfish users, FOCS 2004, 268-276"
    locator: "the same result, proved independently"
---

Marginal cost tolls are the oldest fix for the cost of selfish routing: charge each user, on each edge, the delay that the user causes to all the others. Pigou proposed it in 1920 for a congested road, and Beckmann, McGuire and Winsten made it exact for networks in 1956. The [system optimal flow](/system-optimal-flow/) page proves that an optimal flow is a [Wardrop equilibrium](/wardrop-equilibrium/) for the marginal cost latencies; this page uses that fact as a technique, turns it into fixed tolls, and shows where the technique stops working.

## In plain words

When a driver enters a busy road, the driver is slowed down, and also slows down everyone else a little. The driver feels the first effect but not the second. So too many drivers take busy roads. A toll can make the driver pay for the second effect. Set each road's toll equal to the extra delay that one more driver would cause to the others, measured at the best traffic pattern. Then drivers who pick the cheapest route, time plus toll, end up in the best traffic pattern on their own. The toll needs no knowledge of who the drivers are, only of the roads.

## When it applies

The technique applies to a nonatomic [selfish routing model](/selfish-routing-model/) $(G, r, \ell)$:

- each user controls a tiny amount of traffic, so the equilibrium notion is a [Wardrop equilibrium](/wardrop-equilibrium/), which always exists;
- each latency $\ell_e$ is continuous and nondecreasing, and $x\, \ell_e(x)$ is convex and differentiable, which holds for example for all polynomials with nonnegative coefficients;
- all users value time against money in the same way, so a toll adds to the latency at the same rate for everyone;
- the planner cares about the total latency $C(f) = \sum_e f_e\, \ell_e(f_e)$, and the tolls are a transfer, not a cost.

If one of these fails, see Variations and Pitfalls.

## The template

The marginal cost of edge $e$ is $\ell_e^*(x) = (x\, \ell_e(x))' = \ell_e(x) + x\, \ell_e'(x)$. The term $x\, \ell_e'(x)$ is the extra delay that a small amount of new traffic causes to the $x$ units already on $e$.

```pseudo id=main
MARGINAL-COST-TOLLS(G, r, ℓ)
L1  hole: check that each x ℓ_e(x) is convex and differentiable
L2  f* ← an optimal flow, a minimizer of Σ_e f_e ℓ_e(f_e)      ▷ hole: a convex program over the flows
L3  for each edge e:
L4      τ_e ← f*_e · ℓ_e'(f*_e)                                  ▷ a fixed number, not a function of the flow
L5  return τ                                                     ▷ users now pay ℓ_e(x) + τ_e on edge e
```

**Why it works.** By the Karush-Kuhn-Tucker conditions of the convex program in line L2 ([KKT conditions](/kkt-conditions/)), a flow $f^*$ is optimal if and only if, for each commodity $i$, every path $P$ with $f^*_P > 0$ has the least marginal cost $\sum_{e \in P} \ell_e^*(f^*_e)$ among the paths of commodity $i$. That is, $f^*$ is a Wardrop equilibrium for the latencies $\ell^*$. With the tolls of line L4, the tolled cost of a path at $f^*$ is

$$\sum_{e \in P} \left( \ell_e(f^*_e) + \tau_e \right) = \sum_{e \in P} \left( \ell_e(f^*_e) + f^*_e\, \ell_e'(f^*_e) \right) = \sum_{e \in P} \ell_e^*(f^*_e).$$

So at $f^*$ the tolled costs and the marginal costs agree on every path, and $f^*$ is a Wardrop equilibrium of the tolled network. The tolled latencies $\ell_e + \tau_e$ are continuous and nondecreasing, so by the [Beckmann potential](/beckmann-potential/) every equilibrium of the tolled network has the same edge costs, and the same edge flows if every $\ell_e$ is strictly increasing. Then the tolled equilibrium is $f^*$, and the [price of anarchy](/price-of-anarchy/) of the tolled network is 1. This is a theorem (Beckmann, McGuire and Winsten 1956).

The holes are the two steps that depend on the instance: the convexity check of line L1 and the solution of the convex program in line L2. For latencies $\ell_e(x) = a_e x + b_e$, line L2 is a convex quadratic program, and in general any method for convex flow problems, such as the Frank-Wolfe method, solves it to any accuracy.

## Classic examples

**Pigou's network** ([Pigou example](/pigou-example/)). Two parallel links carry one unit of traffic; link 1 has $\ell_1(x) = x$ and link 2 has $\ell_2(x) = 1$. The equilibrium sends everything on link 1 at cost 1. The optimum splits $1/2$ and $1/2$ at cost $3/4$.

| | link 1 | link 2 |
|---|---|---|
| optimal flow $f^*_e$ | $1/2$ | $1/2$ |
| toll $\tau_e = f^*_e\, \ell_e'(f^*_e)$ | $1/2$ | 0 |
| tolled cost at $f^*$ | $1/2 + 1/2 = 1$ | 1 |

Both links cost 1 with the toll, so the split $1/2, 1/2$ is an equilibrium, and it is the only one since $\ell_1$ is strictly increasing. The total latency drops from 1 to $3/4$. The tolls collected are $1/2 \cdot 1/2 = 1/4$, so each user pays 1 in time plus toll, the same as with no tolls.

**Braess's network** ([Braess's paradox](/braess-paradox/)). Edges $s \to v$ and $w \to t$ have latency $x$, edges $v \to t$ and $s \to w$ have latency 1, the edge $v \to w$ has latency 0, and $r = 1$. The equilibrium sends all traffic on $s \to v \to w \to t$ at cost 2. The optimum sends $1/2$ on each of the two outer paths, at cost $3/2$. The tolls are $1/2$ on each $x$ edge and 0 elsewhere. At $f^*$ the tolled path costs are

- $s \to v \to t$: $(1/2 + 1/2) + 1 = 2$;
- $s \to w \to t$: $1 + (1/2 + 1/2) = 2$;
- $s \to v \to w \to t$: $(1/2 + 1/2) + 0 + (1/2 + 1/2) = 2$.

All three paths cost 2, so $f^*$ is an equilibrium. The total latency drops from 2 to $3/2$, and the tolls collected are $1/2$. The toll does what the removal of the edge $v \to w$ does, without a change of the network.

**The tight examples of the price of anarchy.** For each class of latency functions, the worst ratio of the [price of anarchy](/price-of-anarchy/), such as $4/3$ for linear latencies ([Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/)), is reached on a network of two parallel links like Pigou's. On all of them marginal cost tolls bring the ratio to 1.

## Variations

- **Tolls as functions of the flow.** One can charge $x\, \ell_e'(x)$ at the current flow $x$ instead of the fixed number $\tau_e$. Then the users face the latencies $\ell^*$, and the equilibrium is again $f^*$. Fixed tolls are simpler to post, but they must be computed from $f^*$ first.
- **Other optimal tolls.** For a fixed optimal flow $f^*$, the tolls that make $f^*$ an equilibrium are the solutions of a set of linear inequalities in $\tau$. So a planner can pick, among them, the tolls with the smallest total revenue or tolls on few edges, with a [linear program](/linear-programming-problem/). Marginal cost tolls are one point of this set.
- **Heterogeneous users.** If user $u$ pays $\ell_P + a_u \tau_P$ for a value $a_u > 0$ that differs between users, marginal cost tolls no longer work, because different users react to the same toll in different ways. Cole, Dodis and Roughgarden (2003) proved that tolls that induce the optimal flow still exist for one commodity, and Fleischer, Jain and Mahdian (2004) and Karakostas and Kolliopoulos (2004) proved it for many commodities, by linear programming duality. These are theorems.
- **Atomic users.** In an [atomic congestion game](/atomic-congestion-game/) a user is not tiny, and the tolled game may have equilibria other than the optimum. Toll rules for atomic games are a separate topic (for example Caragiannis, Kaklamanis and Kanellopoulos, 2006).
- **A leader instead of a toll.** [Stackelberg routing](/stackelberg-routing/) controls part of the traffic instead of the prices.

## Pitfalls

- **The tolls cost the users.** If the toll counts in the cost of the users and is not given back, the users can be worse off. In both classic examples each user pays the same amount as with no tolls. Cole, Dodis and Roughgarden (2006) proved that with linear latencies, marginal cost taxes never lower the total cost, latency plus taxes, below that of the untolled equilibrium. They also proved that with linear latencies the best taxes help no more than the best removal of edges ([detecting Braess's paradox](/braess-paradox-detection-hardness/)), a problem that is hard to approximate.
- **Use $f^*$, not the equilibrium flow.** A toll $f_e\, \ell_e'(f_e)$ at the equilibrium flow $f$ is not the right toll in general. In Pigou's network the equilibrium puts 1 on link 1 and gives the toll 1, which pushes the flow too far toward link 2.
- **Convexity.** If $x\, \ell_e(x)$ is not convex, the KKT conditions only describe local optima, and the tolled equilibrium can be a flow that is not optimal.
- **More than one equilibrium.** If some $\ell_e$ is constant on an interval, the tolled network can have equilibria with the same edge costs but other edge flows. The theorem gives edge costs, not edge flows, in that case.
- **The planner's objective.** The tolls minimize the total latency. For another objective, such as the largest latency on a used path, the optimal flow is a different flow, and the marginal cost formula does not apply.

## Exercises

1. In Pigou's network, replace $\ell_1(x) = x$ with $\ell_1(x) = x^d$ for an integer $d \ge 1$. Show that the optimal flow puts $(d + 1)^{-1/d}$ on link 1, that the toll on link 1 is $d/(d + 1)$, and that both links then cost 1.
2. In Pigou's network, show that the tolls $(\tau_1, \tau_2)$ make the optimal flow an equilibrium if and only if $\tau_1 - \tau_2 = 1/2$. Which pair has the smallest revenue, if tolls must be nonnegative?
3. In Braess's network with $r = 2$ instead of 1, find the optimal flow and the marginal cost tolls, and check that every used path has the same tolled cost.
4. Prove the "if" part of the KKT claim directly: if $f^*$ is a Wardrop equilibrium for $\ell^*$ and each $x\, \ell_e(x)$ is convex, then $C(g) \ge C(f^*)$ for every feasible flow $g$. Use $C(g) - C(f^*) \ge \sum_e \ell_e^*(f^*_e)(g_e - f^*_e)$.

## References
