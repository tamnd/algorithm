---
tag: TAVT54
kind: definition
slug: competitive-equilibrium
name: Competitive equilibrium
aliases:
- Walrasian equilibrium
- market equilibrium
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Prices and allocations such that each agent gets an optimal bundle at the prices and every good with positive price clears the market.
prereqs: []
see_also: [arrow-debreu-market, fisher-market, first-welfare-theorem, arrow-debreu-existence-theorem, tatonnement, competitive-equilibrium-from-equal-incomes, gross-substitutes, pareto-optimality]
sources:
  - book: "Leon Walras, Elements d'economie politique pure, Corbaz, Lausanne, 1874"
    locator: the theory of exchange (equilibrium prices as the prices at which the demand for each good equals its supply)
  - paper: doi:10.2307/1907353
    title: "Kenneth J. Arrow and Gerard Debreu, Existence of an equilibrium for a competitive economy, Econometrica 22(3), 265-290 (1954)"
    locator: the definition of a competitive equilibrium for an economy with production and exchange
  - book: isbn:9780195073409
    title: Andreu Mas-Colell, Michael D. Whinston and Jerry R. Green, Microeconomic Theory, Oxford University Press, 1995
    locator: Chapter 15 (general equilibrium in the Edgeworth box) and Chapter 17 (equilibrium and its basic properties, excess demand and Walras' law)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 5, Vijay V. Vazirani, Combinatorial algorithms for market equilibria (the Fisher and Arrow-Debreu models and their equilibria)
  - paper: doi:10.2307/1913392
    title: "Alexander S. Kelso and Vincent P. Crawford, Job matching, coalition formation, and gross substitutes, Econometrica 50(6), 1483-1504 (1982)"
    locator: the whole paper (competitive equilibrium with indivisible items and money, and existence under gross substitutes)
---

A competitive equilibrium, or Walrasian equilibrium, is a price vector together with an allocation of the goods such that every agent gets a bundle she likes best among the bundles she can pay for at these prices, and the market clears: the agents together take exactly the supply of every good that has a positive price. No central planner chooses the allocation. Each agent reacts only to the prices, and the prices do the coordination. The notion goes back to Walras (1874), and its modern form is due to Arrow and Debreu (1954). It is the solution concept of the [Arrow-Debreu market](/arrow-debreu-market/), the [Fisher market](/fisher-market/) and many auction and matching models, and the [first welfare theorem](/first-welfare-theorem/) says that it is [Pareto optimal](/pareto-optimality/).

## Definition

**Exchange economy.** There are $n$ agents and $m$ divisible goods. Agent $i$ has an endowment $w_i \in \mathbb{R}^m_{\ge 0}$ and a utility function $u_i : \mathbb{R}^m_{\ge 0} \to \mathbb{R}$, which she maximizes. A price vector is $p \in \mathbb{R}^m_{\ge 0}$ with $p \ne 0$. At prices $p$, agent $i$ can sell her endowment for $p \cdot w_i$, so her *budget set* is
$$
B_i(p) = \{x_i \in \mathbb{R}^m_{\ge 0} : p \cdot x_i \le p \cdot w_i\},
$$
and her *demand set* $D_i(p)$ is the set of maximizers of $u_i$ on $B_i(p)$.

**Competitive equilibrium.** A pair $(p, x)$, where $p$ is a price vector and $x = (x_1, \dots, x_n)$ is an allocation, is a competitive equilibrium when

1. (optimality) $x_i \in D_i(p)$ for every agent $i$, and
2. (market clearing) $\sum_i x_{ij} \le \sum_i w_{ij}$ for every good $j$, with equality whenever $p_j > 0$.

The inequality in condition 2 allows free disposal: a good can be left over only if it is free. Some texts require equality for all goods; with strictly monotone utilities the two definitions agree, because then every price is positive.

**Excess demand.** When each $D_i(p)$ has one element $x_i(p)$, the *excess demand* is $z(p) = \sum_i x_i(p) - \sum_i w_i$, and $p$ is an equilibrium price vector if and only if $z(p) \le 0$ and $z_j(p) = 0$ for every $j$ with $p_j > 0$. Two facts are used everywhere. Demand does not change when all prices are multiplied by the same $\lambda > 0$, so prices are only determined up to scale, and one normalizes them (for example $\sum_j p_j = 1$). If utilities are locally nonsatiated, every agent spends her whole budget, so $p \cdot z(p) = 0$ for every $p$ (*Walras' law*).

**Variants.**
- In a [Fisher market](/fisher-market/) the budget of agent $i$ is a fixed amount of money $e_i$ instead of $p \cdot w_i$.
- With indivisible items and money, as in the [assignment game](/assignment-game/), agent $i$ has a value $v_i(S)$ for each bundle $S$ and a [quasilinear utility](/quasilinear-utility/) $v_i(S) - p(S)$, with no budget. A Walrasian equilibrium is a price vector and an assignment of disjoint bundles such that each agent gets a bundle in her demand set and every unassigned item has price $0$.
- An *approximate* equilibrium relaxes optimality, clearing, or both, by a stated amount; see [approximate CEEI](/approximate-ceei/) for one form.

## Examples and non-examples

- **Edgeworth box.** Two agents and two goods. Agent 1 owns $w_1 = (1, 0)$ and has $u_1 = x^{1/2} y^{1/2}$; agent 2 owns $w_2 = (0, 1)$ and has $u_2 = x^{1/4} y^{3/4}$. With a Cobb-Douglas utility an agent spends the fixed share $a_j$ of her income on good $j$. At prices $(p_1, p_2)$, agent 1 earns $p_1$ and buys $(1/2, p_1 / (2 p_2))$; agent 2 earns $p_2$ and buys $(p_2 / (4 p_1), 3/4)$. The market for good 1 clears when $1/2 + p_2 / (4 p_1) = 1$, that is $p_2 = 2 p_1$. So $p = (1, 2)$, $x_1 = (1/2, 1/4)$ and $x_2 = (1/2, 3/4)$ is the equilibrium (up to the scale of $p$), and good 2 clears too: $1/4 + 3/4 = 1$, as Walras' law predicts.
- **Fisher check value.** Budgets $1$ and $1$, linear utilities $u_1 = (2, 1)$ and $u_2 = (1, 2)$, one unit of each good: prices $(1, 1)$, and buyer $i$ buys all of good $i$.
- **One item, quasilinear.** One item and two bidders with values $10$ and $7$. Every price $p \in [7, 10]$ with the item given to the first bidder is a Walrasian equilibrium: she wants it, and the second bidder does not want it at that price. At $p < 7$ both bidders demand the item, and at $p > 10$ nobody does. So equilibrium prices need not be unique; here they form an interval, and its lowest point is the Vickrey price.
- **Non-example: complements.** Two items $a$ and $b$. Bidder 1 values only the pair, at $3$; bidder 2 wants one item and values either at $2$. Suppose $(p, x)$ is an equilibrium. An item that is unsold, or that adds no value to the bundle of its holder (one item alone for bidder 1, a second item for bidder 2), must have price $0$. If bidder 1 gets the pair, then $p_a + p_b \le 3$, while bidder 2 must not want either item, so $p_a \ge 2$ and $p_b \ge 2$, a contradiction. Otherwise some item, say $b$, is unsold or adds no value, so $p_b = 0$. Bidder 1 then has utility at most $0$ and must not want the pair, so $p_a \ge 3$. At that price nobody wants $a$, so $a$ is unsold and $p_a = 0$, a contradiction. So there is no Walrasian equilibrium. [Gross substitutes](/gross-substitutes/) valuations exclude this case (Kelso and Crawford 1982).
- **Non-example: indivisible goods with money of no value.** One indivisible seat and two students who each have a budget of $1$ token and want the seat. At a price at most $1$ both demand it; above $1$ neither does. No price clears the market. This is why [CEEI](/competitive-equilibrium-from-equal-incomes/) for indivisible goods needs unequal budgets and approximate clearing.
- **Non-example: not optimal.** In the Fisher check value, prices $(1, 1)$ with buyer 1 spending $1/2$ on each good and buyer 2 doing the same clears the market, but buyer 1 spends money on good 2, whose bang per buck $1$ is below her best $2$. Optimality fails, so it is not an equilibrium.

## Related definitions

- **[Pareto optimality](/pareto-optimality/).** An allocation is Pareto optimal if no other feasible allocation makes some agent better off and nobody worse off. The [first welfare theorem](/first-welfare-theorem/) says that equilibrium allocations are Pareto optimal when utilities are locally nonsatiated; the second welfare theorem gives a converse under convexity, after a transfer of endowments.
- **Existence.** Equilibria exist under continuity, convexity, local nonsatiation and positive endowments (or an irreducibility condition); see the [Arrow-Debreu existence theorem](/arrow-debreu-existence-theorem/). Computing them is hard in general; see [PPAD-hardness of market equilibria](/ppad-hardness-of-arrow-debreu/).
- **Nash equilibrium.** A competitive equilibrium is not a [Nash equilibrium](/nash-equilibrium/) of a game: agents are price takers and do not consider how their demand moves the prices.
- **Core.** Under local nonsatiation every equilibrium allocation is in the core of the exchange economy: no coalition can do better for all its members by trading only among themselves. The proof is the same as for the first welfare theorem.
- **[Competitive equilibrium from equal incomes](/competitive-equilibrium-from-equal-incomes/).** The equilibrium of the economy in which all agents start with the same budget; it is envy-free and Pareto optimal.
- **Dynamics.** [Tatonnement](/tatonnement/) raises the prices of goods in excess demand and lowers the others. Its rest points are the equilibria, but it need not reach them.

## References
