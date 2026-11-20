---
tag: X0RVQ5
kind: theorem
slug: atomic-linear-congestion-price-of-anarchy
name: Price of anarchy of atomic linear congestion games
aliases:
- Christodoulou-Koutsoupias bound
- 5/2 bound for congestion games
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: In atomic congestion games with affine costs, every pure Nash equilibrium costs at most 5/2 times the optimum, and this is tight.
prereqs: [atomic-congestion-game, price-of-anarchy]
see_also: [smoothness-framework, roughgarden-tardos-four-thirds-bound, rosenthal-potential-theorem, price-of-stability, coarse-correlated-equilibrium, correlated-equilibrium, pigou-bound, price-of-anarchy-of-load-balancing]
sources:
  - paper: doi:10.1145/1060590.1060600
    title: "George Christodoulou and Elias Koutsoupias, The price of anarchy of finite congestion games, Proceedings of the 37th Annual ACM Symposium on Theory of Computing (STOC 2005), 67-73"
    locator: the upper bound 5/2 for pure equilibria with linear costs, the matching lower bound, and the bound (5n - 2)/(2n + 1) for symmetric games
  - paper: doi:10.1145/1060590.1060599
    title: "Baruch Awerbuch, Yossi Azar and Amir Epstein, The price of routing unsplittable flow, Proceedings of the 37th Annual ACM Symposium on Theory of Computing (STOC 2005), 57-66; SIAM Journal on Computing 42(1) (2013), 160-177"
    locator: the bound 5/2 for unweighted players with affine costs, (3 + 5^(1/2))/2 for weighted players, and the bounds for polynomial costs
  - paper: "Tim Roughgarden, Intrinsic robustness of the price of anarchy, Journal of the ACM 62(5) (2015), Article 32; STOC 2009, 513-522"
    locator: smooth games, and the extension of the bound 5/2 to mixed, correlated and coarse correlated equilibria
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 12 (atomic selfish routing and the proof of the bound 5/2) and Lecture 14 (robust price of anarchy bounds)
---

This page is about one number: the price of anarchy of atomic congestion games with affine costs is exactly $5/2$. The [smoothness framework](/smoothness-framework/) page describes the general method, a single inequality that bounds the price of anarchy of many games and many equilibrium notions at once. This page proves the inequality that the method needs for affine costs, gives the instance that shows that $5/2$ cannot be improved, and compares the number with the $4/3$ of nonatomic routing.

## Statement

Let a [congestion game](/atomic-congestion-game/) have $n$ players, resources $E$ and affine costs $c_e(x) = a_e x + b_e$ with $a_e, b_e \ge 0$. A profile $s$ has loads $x_e(s)$, player costs $c_i(s) = \sum_{e \in s_i} c_e(x_e(s))$, which each player minimizes, and social cost

$$C(s) = \sum_{i=1}^n c_i(s) = \sum_{e \in E} x_e(s)\, c_e(x_e(s)).$$

**Theorem (Christodoulou and Koutsoupias 2005; Awerbuch, Azar and Epstein 2005).** If $s$ is a pure Nash equilibrium and $s^*$ is any profile, then $C(s) \le \tfrac{5}{2} C(s^*)$. So the [price of anarchy](/price-of-anarchy/) of the class is at most $5/2$, and there are games in the class where it is exactly $5/2$.

The game is finite and has pure equilibria by [Rosenthal's theorem](/rosenthal-potential-theorem/). The same bound holds for mixed Nash, correlated and coarse correlated equilibria, by the [smoothness framework](/smoothness-framework/).

## In plain words

Players share resources whose price grows in a straight line with the number of users. Each player picks the cheapest choice for itself, and the players reach a state where nobody wants to change. This state can be worse for the group than the best plan, but never by much: the total cost is at most two and a half times the best total. A small example with three players shows that two and a half can happen. When players are tiny parts of a flow, as in road traffic models, the loss is smaller, at most one third more than the best.

## Proof

**Lemma.** For all nonnegative integers $y$ and $z$,

$$y(z+1) \le \tfrac{5}{3} y^2 + \tfrac{1}{3} z^2.$$

*Proof.* If $y = 0$ both sides are at least 0. If $y = 1$ the claim is $z + 1 \le \tfrac{5}{3} + \tfrac{1}{3} z^2$, that is $z^2 - 3z + 2 = (z-1)(z-2) \ge 0$, which holds for every integer $z$. If $y \ge 2$, the square $\left(\tfrac{\sqrt{3}}{2} y - \tfrac{1}{\sqrt{3}} z\right)^2 \ge 0$ gives $yz \le \tfrac{3}{4} y^2 + \tfrac{1}{3} z^2$, and $y \le \tfrac{11}{12} y^2$ because $y \ge 12/11$. Adding the two gives the claim. Equality holds only for $(y, z) = (0, 0)$, $(1, 1)$ and $(1, 2)$. $\square$

**Smoothness.** Let $s$ and $s^*$ be any two profiles, and write $x_e = x_e(s)$ and $x_e^* = x_e(s^*)$. If player $i$ alone switches from $s_i$ to $s_i^*$, the load of each $e \in s_i^*$ is at most $x_e + 1$, so $c_i(s_i^*, s_{-i}) \le \sum_{e \in s_i^*} c_e(x_e + 1)$. Each resource $e$ is in $s_i^*$ for exactly $x_e^*$ players, so

$$\sum_{i=1}^n c_i(s_i^*, s_{-i}) \le \sum_{e \in E} x_e^* \big(a_e (x_e + 1) + b_e\big).$$

By the lemma with $y = x_e^*$ and $z = x_e$, $a_e x_e^* (x_e + 1) \le a_e \left(\tfrac{5}{3} (x_e^*)^2 + \tfrac{1}{3} x_e^2\right)$, and $b_e x_e^* \le \tfrac{5}{3} b_e x_e^* + \tfrac{1}{3} b_e x_e$. Since $C(s) = \sum_e (a_e x_e^2 + b_e x_e)$,

$$\sum_{i=1}^n c_i(s_i^*, s_{-i}) \le \tfrac{5}{3} C(s^*) + \tfrac{1}{3} C(s).$$

**The bound.** Now let $s$ be a pure Nash equilibrium. No player gains by switching to $s_i^*$, so $c_i(s) \le c_i(s_i^*, s_{-i})$ for each $i$. Adding over the players,

$$C(s) = \sum_{i=1}^n c_i(s) \le \sum_{i=1}^n c_i(s_i^*, s_{-i}) \le \tfrac{5}{3} C(s^*) + \tfrac{1}{3} C(s),$$

so $\tfrac{2}{3} C(s) \le \tfrac{5}{3} C(s^*)$, that is $C(s) \le \tfrac{5}{2} C(s^*)$. $\blacksquare$

The proof uses the equilibrium condition only for the one deviation of each player to its strategy in $s^*$. That is why it carries over to mixed, correlated and coarse correlated equilibria: the smoothness inequality holds for each profile, so it holds in expectation, and a coarse correlated equilibrium is defined by exactly these expected deviations.

### Example

The instance of Christodoulou and Koutsoupias has 3 players and 6 resources $h_1, h_2, h_3, g_1, g_2, g_3$, each with cost $c(x) = x$. Indices are taken modulo 3. Player $i$ has two strategies:

- $A_i = \{h_i, g_i\}$,
- $B_i = \{h_{i+1}, g_{i+1}, g_{i+2}\}$.

| profile | loads | player costs | social cost |
|---|---|---|---|
| all play $A$ | every resource 1 | 2, 2, 2 | 6 |
| all play $B$ | each $h_j$ 1, each $g_j$ 2 | 5, 5, 5 | 15 |

The profile "all play $B$" is a pure Nash equilibrium. Player $i$ pays $1 + 2 + 2 = 5$. If it moves to $A_i$, it joins player $i - 1$ on $h_i$, at load 2, and players $i - 1$ and $i - 2$ on $g_i$, at load 3, so it pays $2 + 3 = 5$, no less. The optimum is at most 6, and among all 8 profiles the costs are 6, 13, 15 and 16, so it is 6. The ratio is $15/6 = 5/2$. Each $h_j$ has $(y, z) = (1, 1)$ and each $g_j$ has $(y, z) = (1, 2)$, the equality cases of the lemma, and each deviation leaves the player indifferent, so every inequality of the proof is tight.

The profile "all play $A$" is also an equilibrium, so the [price of stability](/price-of-stability/) of this instance is 1. The bad equilibrium is not the only one.

## Consequences

- **Atomic against nonatomic.** In the nonatomic [selfish routing model](/selfish-routing-model/) with affine costs the price of anarchy is $4/3$ ([Roughgarden and Tardos](/roughgarden-tardos-four-thirds-bound/)). The atomic bound is larger because one player is a whole unit of load: its deviation raises the cost of a resource by a full step, and the term $z + 1$ in the lemma is the cost of that step.
- **Robust bounds.** By the [smoothness framework](/smoothness-framework/), the bound $5/2$ holds for mixed Nash equilibria, for [correlated equilibria](/correlated-equilibrium/) and for [coarse correlated equilibria](/coarse-correlated-equilibrium/). Players who use [no-regret dynamics](/no-regret-dynamics/) have a time-averaged social cost that tends to at most $5/2$ times the optimum. No pure equilibrium need be computed, which matters because computing one is [PLS-complete](/pls-completeness-of-congestion-games/).
- **Subclasses.** Network routing of unsplittable unit demands, singleton games and matroid games with affine costs are all affine congestion games, so the upper bound $5/2$ holds for each of them. The lower bound needs other instances in some subclasses, and the worst case there can be smaller.

## Tightness

- **The constant.** The example above reaches $5/2$ exactly, so no smaller constant holds for the class.
- **Symmetric games.** If all players have the same strategy set, the price of anarchy is $(5n - 2)/(2n + 1)$ for $n$ players (Christodoulou and Koutsoupias 2005), which tends to $5/2$.
- **Weighted players.** If player $i$ adds a weight $w_i$ to the load and pays per unit of weight, the price of anarchy for affine costs is $(3 + \sqrt{5})/2 \approx 2.618$ (Awerbuch, Azar and Epstein 2005).
- **Polynomial costs.** For polynomials of degree $d$ with nonnegative coefficients, the price of anarchy grows exponentially in $d$ (Awerbuch, Azar and Epstein 2005), while the nonatomic one grows like $d / \ln d$.
- **The best equilibrium.** The price of stability of the class is $1 + 1/\sqrt{3} \approx 1.577$ (lower bound by Christodoulou and Koutsoupias, ESA 2005; upper bound by Caragiannis and coauthors, ICALP 2006), well below $5/2$.
- **The social cost.** The theorem uses the total cost. With the largest player cost as social cost, the bounds are different and depend on $n$.

## History

Christodoulou and Koutsoupias, and independently Awerbuch, Azar and Epstein, proved the bound $5/2$ at STOC 2005; the second paper phrased it as the cost of routing unsplittable flow selfishly and also treated weighted players and polynomial costs. In 2009 Roughgarden observed that both proofs are smoothness arguments, which led to the [smoothness framework](/smoothness-framework/) and to the extension of the bound to correlated and coarse correlated equilibria.

## References
