---
tag: F3YDFE
kind: definition
slug: competitive-equilibrium-from-equal-incomes
name: Competitive equilibrium from equal incomes
aliases:
- CEEI
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: A competitive equilibrium in which every agent has the same budget. Its allocation is envy-free and Pareto optimal.
prereqs: [competitive-equilibrium, envy-freeness, fisher-market]
see_also: [eisenberg-gale-program, maximum-nash-welfare, pareto-optimality, first-welfare-theorem, arrow-debreu-existence-theorem, hylland-zeckhauser-mechanism, approximate-ceei, indivisible-goods-allocation]
sources:
  - paper: doi:10.1016/0022-0531(74)90075-1
    title: "Hal R. Varian, Equity, envy, and efficiency, Journal of Economic Theory 9(1), 63-91 (1974)"
    locator: the whole paper (fair allocations as envy-free and efficient ones, and the competitive equilibrium from equal division as a fair allocation)
  - paper: doi:10.1214/aoms/1177706369
    title: "Edmund Eisenberg and David Gale, Consensus of subjective probabilities: the pari-mutuel method, Annals of Mathematical Statistics 30(1), 165-168 (1959)"
    locator: the whole paper (the convex program whose optimum is the equilibrium of a market with budgets and linear utilities)
  - paper: doi:10.1086/664613
    title: "Eric Budish, The combinatorial assignment problem: approximate competitive equilibrium from equal incomes, Journal of Political Economy 119(6), 1061-1103 (2011)"
    locator: the whole paper (CEEI may fail to exist with indivisible goods, and its approximate version)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 5, Vijay V. Vazirani, Combinatorial algorithms for market equilibria (the Fisher model and the Eisenberg-Gale program)
---

A competitive equilibrium from equal incomes, or CEEI, is a way to divide goods fairly among agents by using a market. Every agent gets the same budget of artificial money, the goods get prices, each agent buys a bundle she likes best among those she can pay for, and the prices are set so that the market clears. Because all agents face the same prices with the same budget, every agent could have bought the bundle of any other agent, so no agent envies another. By the [first welfare theorem](/first-welfare-theorem/), the allocation is also [Pareto optimal](/pareto-optimality/). Varian (1974) put these two facts at the center of the theory of fair division. For divisible goods and additive utilities, a CEEI is the [Fisher market](/fisher-market/) equilibrium with equal budgets and maximizes the [Nash social welfare](/maximum-nash-welfare/). For indivisible goods it may not exist, which is why [approximate CEEI](/approximate-ceei/) gives slightly unequal budgets.

## Definition

There are $n$ agents and $m$ goods, with supply $s_j > 0$ of good $j$. Agent $i$ has a utility function $u_i$ over bundles $x_i \in \mathbb{R}^m_{\ge 0}$ (or over the allowed bundles, when goods are indivisible).

**CEEI.** A *competitive equilibrium from equal incomes* is a price vector $p \in \mathbb{R}^m_{\ge 0}$ and an allocation $x = (x_1, \ldots, x_n)$ such that:

1. **Equal budgets and optimal bundles.** Every agent has the same budget, which we normalize to $1$, and $x_i$ maximizes $u_i$ over the bundles $y$ with $p \cdot y \le 1$.
2. **Market clearing.** $\sum_i x_{ij} \le s_j$ for every good, with equality when $p_j > 0$.

This is a [competitive equilibrium](/competitive-equilibrium/) of the [Fisher market](/fisher-market/) in which all budgets are equal. Equivalently, it is a competitive equilibrium of the exchange economy in which every agent starts with the equal share $s / n$ of every good; then every agent has the income $p \cdot s / n$, which is the same for all. Varian calls this an equilibrium from equal division.

**Fairness properties.** An allocation is *[envy-free](/envy-freeness/)* if $u_i(x_i) \ge u_i(x_k)$ for all agents $i$ and $k$, *proportional* if $u_i(x_i) \ge u_i(s / n)$ for every agent, and *fair* in the sense of Varian if it is envy-free and Pareto optimal. A CEEI has these properties:

- **Envy-free, for any utilities.** The bundle $x_k$ costs at most $1$, so agent $i$ can pay for it, and $x_i$ is a best bundle for $i$ among those she can pay for.
- **Pareto optimal, when utilities are locally nonsatiated.** This is the first welfare theorem.
- **Proportional, for divisible goods and locally nonsatiated utilities.** Every agent spends her whole budget, so $p \cdot s = n$ by market clearing, the equal share $s / n$ costs exactly $1$, and agent $i$ can pay for it.

**Existence.** For divisible goods with continuous, concave and monotone utilities, a CEEI exists: it is an equilibrium of an exchange economy in which every agent owns a positive amount of every good, and the [Arrow-Debreu existence theorem](/arrow-debreu-existence-theorem/) applies. For additive (linear) utilities $u_i(x_i) = \sum_j u_{ij} x_{ij}$, the [Eisenberg-Gale program](/eisenberg-gale-program/) with equal budgets is
$$
\max \sum_i \log u_i(x_i) \quad \text{subject to} \quad \sum_i x_{ij} \le s_j, \; x \ge 0,
$$
so the CEEI allocations are exactly the allocations of maximum Nash social welfare $\prod_i u_i(x_i)$, and the CEEI prices are unique. With indivisible goods, a CEEI may not exist.

## Examples and non-examples

- **Three agents and two goods.** Let $u_1 = u_2 = (2, 1)$, $u_3 = (1, 1)$, one unit of each good, and budgets $1$. The prices $p = (2, 1)$ give a CEEI: agents 1 and 2 have bang per buck $(1, 1)$, so they are indifferent, and each spends $1$ on half of good 1; agent 3 has bang per buck $(1/2, 1)$ and spends $1$ on good 2. Every agent gets utility $1$. Agent 1 values agent 3's bundle at $1$ and agent 3 values agent 1's bundle at $1/2$, so there is no envy. The Nash welfare is $1$, larger than the $2/3$ of giving everyone a third of every good.
- **Two agents with opposite tastes.** With $u_1 = (2, 1)$, $u_2 = (1, 2)$ and budgets $1$, the prices $(1, 1)$ give each agent the good she likes more. This is a CEEI.
- **Non-example: unequal budgets.** Two agents with $u_1 = u_2 = (1, 1)$ and budgets $1$ and $2$ have the Fisher equilibrium prices $(3/2, 3/2)$, at which agent 1 gets goods worth $2/3$ to her and agent 2 gets goods worth $4/3$. Agent 1 envies agent 2. A competitive equilibrium is fair only when the budgets are equal.
- **Non-example: one indivisible good.** Two agents both want a single indivisible good, with equal budgets $1$. At a price of at most $1$ both demand it, and at a higher price neither does, so no price clears the market and no CEEI exists. No allocation of this good is envy-free at all.
- **Non-example: a fair allocation that is not a CEEI.** With $u_1 = (2, 1)$ and $u_2 = (1, 2)$, give agent 1 all of good 1 and a tenth of good 2, and agent 2 the rest of good 2. Agent 1 has utility $2.1$ and values the other bundle at $0.9$; agent 2 has utility $1.8$ and values the other bundle at $1.2$. So the allocation is envy-free, and it is Pareto optimal because agent 2 has none of good 1 to trade. But the CEEI prices of this market are unique, $(1, 1)$, and they give each agent only her own good. The CEEI is one fair allocation among possibly many, chosen by the market.

## Related definitions

- [Competitive equilibrium](/competitive-equilibrium/) and the [Fisher market](/fisher-market/) are the general notions; CEEI is the case of equal budgets.
- [Envy-freeness](/envy-freeness/) and [Pareto optimality](/pareto-optimality/) are the two fairness and efficiency notions that a CEEI satisfies.
- [Maximum Nash welfare](/maximum-nash-welfare/) is the allocation that a CEEI gives for additive utilities and divisible goods, through the [Eisenberg-Gale program](/eisenberg-gale-program/).
- The [Hylland-Zeckhauser mechanism](/hylland-zeckhauser-mechanism/) applies the CEEI idea to the random assignment of indivisible objects: agents buy probability shares of the objects with equal budgets.
- [Approximate CEEI](/approximate-ceei/) gives agents slightly unequal budgets and allows a small market clearing error, so that an equilibrium exists for [indivisible goods](/indivisible-goods-allocation/), as in course allocation.

## References
