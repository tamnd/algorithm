---
tag: TSX9P1
kind: theorem
slug: first-welfare-theorem
name: First welfare theorem
aliases:
- first fundamental theorem of welfare economics
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: With locally nonsatiated preferences, every competitive equilibrium allocation is Pareto optimal.
prereqs: [competitive-equilibrium, pareto-optimality]
see_also: [arrow-debreu-market, fisher-market, arrow-debreu-existence-theorem, competitive-equilibrium-from-equal-incomes, assignment-game, demange-gale-sotomayor-auction, eisenberg-gale-program, price-of-anarchy]
sources:
  - paper: doi:10.1525/9780520411586-038
    title: "Kenneth J. Arrow, An extension of the basic theorems of classical welfare economics, in Jerzy Neyman (ed.), Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability, University of California Press, 507-532 (1951)"
    locator: the whole paper (both welfare theorems without differentiability, the second by a separating hyperplane)
  - book: isbn:9780195073409
    title: Andreu Mas-Colell, Michael D. Whinston and Jerry R. Green, Microeconomic Theory, Oxford University Press, 1995
    locator: Chapter 16 (equilibrium and its basic welfare properties, the first and second fundamental theorems)
  - paper: doi:10.2307/1907353
    title: "Kenneth J. Arrow and Gerard Debreu, Existence of an equilibrium for a competitive economy, Econometrica 22(3), 265-290 (1954)"
    locator: the introduction (the welfare theorems as the reason to study competitive equilibrium)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 5, Vijay V. Vazirani, Combinatorial algorithms for market equilibria (the welfare theorems as motivation for computing equilibria)
---

The first welfare theorem says that a competitive market wastes nothing: when every agent always wants a little more, the allocation of a [competitive equilibrium](/competitive-equilibrium/) is [Pareto optimal](/pareto-optimality/). No other way to split the goods makes some agent better off without making another agent worse off. The hypothesis is weak and the proof takes a few lines. It is the formal version of Adam Smith's invisible hand, and it explains why algorithmic game theory computes market equilibria at all: a price vector that clears the market is also a certificate that the allocation is efficient. It says nothing about fairness, and nothing about whether an equilibrium exists; for that see the [Arrow-Debreu existence theorem](/arrow-debreu-existence-theorem/).

## Statement

Take an exchange economy with $n$ agents and $m$ divisible goods. Agent $i$ has an endowment $w_i \in \mathbb{R}^m_{\ge 0}$ and a utility function $u_i$ on the consumption set $\mathbb{R}^m_{\ge 0}$. An allocation $x = (x_1, \dots, x_n)$ is *feasible* if $x_i \ge 0$ and $\sum_i x_i \le \sum_i w_i$. A feasible allocation $x'$ *Pareto dominates* $x$ if $u_i(x'_i) \ge u_i(x_i)$ for every $i$, with strict inequality for at least one $i$. A feasible allocation is *Pareto optimal* if no feasible allocation Pareto dominates it.

The utility $u_i$ is *locally nonsatiated* if for every bundle $y \ge 0$ and every $\varepsilon > 0$ there is a bundle $y' \ge 0$ with $\|y' - y\| < \varepsilon$ and $u_i(y') > u_i(y)$. Every strictly increasing utility is locally nonsatiated, and so is a linear utility $\sum_j u_{ij} y_j$ with some $u_{ij} > 0$.

**Theorem (first welfare theorem).** If every $u_i$ is locally nonsatiated and $(p, x)$ is a competitive equilibrium, then $x$ is Pareto optimal.

**Theorem (weak form).** With no assumption on the utilities, if $(p, x)$ is a competitive equilibrium then no feasible allocation makes every agent strictly better off.

The same statements hold, with the same proof, for a [Fisher market](/fisher-market/), where $p \cdot w_i$ is replaced by the fixed budget $e_i$ and Pareto optimality is among the allocations of the goods, and for economies with production, where firms maximize profit at the prices.

## In plain words

Suppose the market has settled at prices where every person buys what she likes best with what her own goods sell for, and every good is used up. Could a planner move goods around so that nobody is worse off and someone is better off? No. Anyone who would end up better off must be getting something she could not afford before, or she would have bought it. Anyone who ends up just as well off must be getting something at least as expensive, because a cheaper bundle would leave money to buy a bit more. So the new plan costs more, in total, than everything the market owns. That is impossible.

## Proof

Let $(p, x)$ be a competitive equilibrium and suppose, for a contradiction, that a feasible allocation $x'$ Pareto dominates $x$.

*Step 1: an agent who is strictly better off cannot afford her new bundle.* If $u_k(x'_k) > u_k(x_k)$, then $p \cdot x'_k > p \cdot w_k$. Otherwise $x'_k$ is in the budget set of agent $k$ and gives her more utility than $x_k$, which contradicts $x_k \in D_k(p)$.

*Step 2: an agent who is weakly better off pays at least her budget.* If $u_i(x'_i) \ge u_i(x_i)$, then $p \cdot x'_i \ge p \cdot w_i$. Suppose instead that $p \cdot x'_i < p \cdot w_i$, and let $\delta = p \cdot w_i - p \cdot x'_i > 0$. The map $y \mapsto p \cdot y$ is continuous, so there is an $\varepsilon > 0$ such that every bundle $y$ with $\|y - x'_i\| < \varepsilon$ has $p \cdot y < p \cdot x'_i + \delta = p \cdot w_i$. By local nonsatiation there is such a $y \ge 0$ with $u_i(y) > u_i(x'_i) \ge u_i(x_i)$. This $y$ is in the budget set of agent $i$ and beats $x_i$, which contradicts $x_i \in D_i(p)$.

*Step 3: sum up.* By Steps 1 and 2, $p \cdot x'_i \ge p \cdot w_i$ for every $i$, with strict inequality for the agent $k$ who is strictly better off. Adding these inequalities gives
$$
p \cdot \sum_i x'_i > p \cdot \sum_i w_i .
$$
But $x'$ is feasible, so $\sum_i x'_i \le \sum_i w_i$ coordinate by coordinate, and $p \ge 0$, so $p \cdot \sum_i x'_i \le p \cdot \sum_i w_i$. This is a contradiction, so no feasible $x'$ Pareto dominates $x$.

*The weak form.* If $x'$ makes every agent strictly better off, Step 1 applies to every agent, and the sum gives the same contradiction. Step 2, the only place that uses local nonsatiation, is not needed. $\blacksquare$

The proof does not use that the market clears at $x$. It uses only that each $x_i$ is optimal in its budget set and that the competing allocation $x'$ is feasible.

## Consequences

- **Quasilinear markets.** In a market of indivisible items with money, where agent $i$ has value $v_i(S)$ for bundle $S$ and utility $v_i(S) - p(S)$, a Walrasian equilibrium $(p, S_1, \dots, S_n)$ maximizes the total value $\sum_i v_i(S_i)$ over all assignments. For any assignment $T_1, \dots, T_n$, optimality gives $v_i(S_i) - p(S_i) \ge v_i(T_i) - p(T_i)$ for each $i$. Summing, and using that unsold items have price $0$ so that $\sum_i p(S_i) = p(M) \ge \sum_i p(T_i)$ for the set $M$ of all items, gives $\sum_i v_i(S_i) \ge \sum_i v_i(T_i)$. This is why the [Demange-Gale-Sotomayor auction](/demange-gale-sotomayor-auction/) ends at an optimal assignment, and why a Walrasian equilibrium of the [assignment game](/assignment-game/) is a pair of optimal primal and dual solutions of the assignment LP.
- **Fisher markets.** In a [Fisher market](/fisher-market/) with linear utilities, the equilibrium allocation is Pareto optimal, and it maximizes the budget-weighted product of utilities ([Eisenberg-Gale program](/eisenberg-gale-program/)). This gives a second, quantitative proof of efficiency in that model.
- **Fair and efficient division.** An equilibrium from equal incomes is Pareto optimal by this theorem and envy-free because all agents face the same budget set; see [competitive equilibrium from equal incomes](/competitive-equilibrium-from-equal-incomes/).
- **The second welfare theorem.** Conversely, with continuous, convex and locally nonsatiated preferences, every Pareto optimal allocation can be reached as an equilibrium after a transfer of wealth among the agents (Arrow 1951; Debreu 1951). Its proof needs convexity and a separating hyperplane, and it gives in general a quasi-equilibrium, which is an equilibrium under a mild extra condition such as positive endowments.

## Tightness

- **Local nonsatiation is needed.** Let agent 1 be indifferent among all bundles ($u_1 = 0$) and agent 2 have $u_2(y) = y_1 + y_2$. Endowments are $w_1 = (1, 0)$ and $w_2 = (0, 1)$. At prices $(1, 1)$, every bundle in her budget set is optimal for agent 1, so she may keep $(1, 0)$, and agent 2 keeps $(0, 1)$. This is a competitive equilibrium. Giving both goods to agent 2 leaves agent 1 at utility $0$ and raises agent 2 from $1$ to $2$, so the equilibrium allocation is not Pareto optimal. It is still weakly Pareto optimal, as the weak form says. The same happens with thick indifference curves, where an agent is satiated on a region of positive size.
- **Market failures.** The theorem assumes that every good is traded at a price that all agents take as given. With externalities, public goods, missing markets or agents who can move prices, equilibria can be inefficient; the [price of anarchy](/price-of-anarchy/) measures such losses in games.
- **Pareto optimal is not fair.** An agent who owns nothing of value gets nothing in equilibrium, and that allocation is Pareto optimal. Fairness comes from the endowments, as in CEEI, not from the theorem.
- **Existence is a separate question.** With indivisible goods and money of no outside value, or with complements in a quasilinear market, an equilibrium may fail to exist (see the non-examples on [competitive equilibrium](/competitive-equilibrium/)). The theorem is then empty.

## History

The idea that self-interested trade at market prices leads to a good outcome is Adam Smith's invisible hand (1776). Pareto (1906) defined the efficiency notion used here and argued for the theorem with calculus, and Lange (1942) gave a version with first-order conditions. Arrow (1951) and Debreu (1951) gave the modern proofs that need neither differentiability nor interior solutions: the first theorem by the budget argument above, the second by the separating hyperplane theorem for convex sets. Arrow and Debreu (1954) cited the welfare theorems as one reason to prove that equilibria exist.

## References
