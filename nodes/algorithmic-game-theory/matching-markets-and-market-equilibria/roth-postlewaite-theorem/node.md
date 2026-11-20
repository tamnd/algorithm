---
tag: YFGBG6
kind: theorem
slug: roth-postlewaite-theorem
name: Roth-Postlewaite theorem
aliases:
- uniqueness of the strict core of housing markets
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: In a housing market with strict preferences, the top trading cycles allocation is the unique strict core allocation and the unique competitive allocation.
prereqs: [shapley-scarf-housing-market, top-trading-cycles, competitive-equilibrium]
see_also: [top-trading-cycles, shapley-scarf-housing-market, core-of-a-cooperative-game, pareto-optimality, individual-rationality, random-serial-dictatorship, top-trading-cycles-and-chains]
sources:
  - paper: doi:10.1016/0304-4068(77)90004-0
    title: Alvin E. Roth and Andrew Postlewaite, Weak versus strong domination in a market with indivisible goods, Journal of Mathematical Economics 4(2), 131 to 137 (1977)
    locator: the main theorem (with strict preferences, the strict core is one allocation, and it is the competitive allocation)
  - paper: doi:10.1016/0304-4068(74)90033-0
    title: Lloyd Shapley and Herbert Scarf, On cores and indivisibility, Journal of Mathematical Economics 1(1), 23 to 37 (1974)
    locator: the housing market, the existence of competitive allocations and the top trading cycle algorithm
  - paper: doi:10.1016/0165-1765(82)90003-9
    title: Alvin E. Roth, Incentive compatibility in a market with indivisible goods, Economics Letters 9(2), 127 to 132 (1982)
    locator: the strategyproofness of the rule that the theorem defines
---

The Roth-Postlewaite theorem says that a [Shapley-Scarf housing market](/shapley-scarf-housing-market/) with strict preferences has exactly one allocation in the strict core, and that this allocation is also the only competitive allocation. It is the allocation that [top trading cycles](/top-trading-cycles/) computes. So the core rule of the housing market is well defined, and it can be computed in $O(n^2)$ time. The theorem is about the strict core, where a coalition blocks if its members are all at least as well off and one is better off. The larger core, where every member of a blocking coalition must be better off, can contain several allocations.

## Statement

Let $N = \{1, \dots, n\}$ be the agents, let agent $i$ own house $h_i$, and let each agent have a strict ranking $\succ_i$ of the $n$ houses. An allocation is a permutation $x$ with $x(i)$ the house of agent $i$. A coalition $S$ weakly blocks $x$ if a permutation $y$ of the houses of $S$ among the agents of $S$ gives $y(i) \succeq_i x(i)$ for all $i \in S$ and $y(i) \succ_i x(i)$ for some $i \in S$. A pair $(x, p)$ of an allocation and a price vector on the houses is a competitive equilibrium if, for each $i$, $x(i)$ is the best house of $i$ among the houses $h$ with $p(h) \le p(h_i)$.

**Theorem (Roth and Postlewaite 1977).** Let $x^*$ be the allocation found by top trading cycles.

1. $x^*$ is the only allocation that no coalition weakly blocks.
2. There are prices $p$ such that $(x^*, p)$ is a competitive equilibrium, and $x^*$ is the only allocation with this property.

## In plain words

Look for a way to swap houses that no group of owners would undo. A group would undo a plan if, by swapping only among themselves, nobody in the group loses and somebody gains. With strict tastes there is exactly one plan that no group would undo, and the top trading cycles algorithm finds it. The same plan is also the only one that a price system can support, where each owner can afford the houses that cost no more than its own.

## Proof

Run top trading cycles. It removes cycles $C_1, \dots, C_r$ in this order, and each agent of a cycle gets the house of the next agent on the cycle. Let $H_k$ be the set of the houses of the agents of $C_1 \cup \dots \cup C_k$, with $H_0 = \emptyset$. Then $x^*$ maps the agents of $C_1 \cup \dots \cup C_k$ onto $H_k$, and each agent $i$ of $C_k$ gets its best house outside $H_{k-1}$. (When $C_k$ is removed, every remaining agent points to the owner of its best remaining house, and the remaining houses are exactly the houses outside $H_{k-1}$.)

**Step 1: no coalition weakly blocks $x^*$.** Suppose that $S$ and $y$ weakly block $x^*$. Some agent of $S$ is better off, so $y(i) \ne x^*(i)$ for some $i \in S$; choose such an $i$ in the cycle $C_k$ with the smallest $k$. The preferences are strict, so $y(i) \succ_i x^*(i)$, and as $x^*(i)$ is the best house of $i$ outside $H_{k-1}$, we get $y(i) \in H_{k-1}$. Let $E = S \cap (C_1 \cup \dots \cup C_{k-1})$. By the choice of $k$, $y = x^*$ on $E$, so $y(E) = x^*(E)$, a set of $|E|$ houses in $H_{k-1}$. These are houses of agents of $S$, since $y$ only uses such houses, and the houses in $H_{k-1}$ that belong to agents of $S$ are exactly the $|E|$ houses of $E$. So $y(E)$ is the set of all houses of $E$. The house $y(i)$ is also a house of an agent of $S$ in $H_{k-1}$, so it is a house of $E$, and $i \notin E$. Then $y$ gives one house to two agents, which is impossible.

**Step 2: no other allocation is in the strict core.** Let $z$ be an allocation that no coalition weakly blocks. We show by induction on $k$ that $z = x^*$ on $C_k$. Suppose this holds for $C_1, \dots, C_{k-1}$. Then $z$ maps the agents of these cycles onto $H_{k-1}$, so $z$ gives every agent of $C_k$ a house outside $H_{k-1}$. Each $i \in C_k$ gets under $x^*$ its best house outside $H_{k-1}$, so $x^*(i) \succeq_i z(i)$. The map $x^*$ on $C_k$ is a permutation of the houses of $C_k$. If $z(i) \ne x^*(i)$ for some $i \in C_k$, then $x^*(i) \succ_i z(i)$, and $C_k$ with this permutation weakly blocks $z$. This is a contradiction, so $z = x^*$ on $C_k$. Hence $z = x^*$. This proves part 1.

**Step 3: $x^*$ is competitive.** Give every house of $C_k$ the price $p(h) = r - k + 1$. An agent $i$ of $C_k$ can afford the houses with price at most $r - k + 1$, which are the houses outside $H_{k-1}$. Its house $x^*(i)$ is its best house among them. So $(x^*, p)$ is a competitive equilibrium.

**Step 4: every competitive allocation is in the strict core.** Let $(x, p)$ be a competitive equilibrium. Each agent can afford $x(i)$, so $p(x(i)) \le p(h_i)$. Summing over all agents gives $\sum_i p(x(i)) \le \sum_i p(h_i)$, and both sums are the total price of all houses because $x$ is a permutation. So $p(x(i)) = p(h_i)$ for every $i$. Suppose that $S$ and $y$ weakly block $x$. For $i \in S$ with $y(i) = x(i)$ we have $p(y(i)) = p(h_i)$. For $i \in S$ with $y(i) \ne x(i)$ we have $y(i) \succ_i x(i)$, so $y(i)$ is not affordable for $i$, that is, $p(y(i)) > p(h_i)$, and there is at least one such $i$. Summing over $S$ gives $\sum_{i \in S} p(y(i)) > \sum_{i \in S} p(h_i)$. But $y$ is a permutation of the houses of $S$, so the two sums are equal, a contradiction. So $x$ is in the strict core, and by part 1, $x = x^*$. This proves part 2. $\blacksquare$

## Consequences

- **A well-defined rule.** The map from a profile of strict rankings to the unique strict core allocation is a mechanism, the core rule. Top trading cycles computes it in $O(n^2)$ time, and in any order of the cycles, since every order ends at the same unique allocation.
- **Efficiency and participation.** The coalition of one agent and the coalition of all agents show that $x^*$ is individually rational and Pareto optimal.
- **Incentives.** Roth (1982) proved that the core rule is strategyproof. Ma (1994) proved that it is the only individually rational, Pareto optimal and strategyproof rule on housing markets with strict preferences.
- **Lotteries.** Abdulkadiroglu and Sonmez (1998) used the core rule with random endowments and proved that it gives the same lottery as [random serial dictatorship](/random-serial-dictatorship/).
- **Kidney exchange.** The rule [top trading cycles and chains](/top-trading-cycles-and-chains/) extends the core rule to patient-donor pairs and a waiting list.

## Tightness

**Strong blocking.** The theorem fails for the core defined by strong blocking. Let agent 1 rank $h_2 \succ h_1 \succ h_3$, agent 2 rank $h_1 \succ h_3 \succ h_2$, and agent 3 rank $h_1 \succ h_2 \succ h_3$. Top trading cycles gives $(h_2, h_1, h_3)$. The allocation $(h_2, h_3, h_1)$ is also in the core: agents 1 and 3 get their first choices, so they can never be strictly better off, and agent 2 alone can only keep $h_2$, which it ranks below $h_3$. But the coalition $\{1, 2\}$ weakly blocks it by a swap. A brute force check confirms that the core is exactly these two allocations.

**Ties.** The theorem needs strict preferences.

- Let agent 1 be indifferent between all houses, and let agents 2 and 3 both rank $h_1$ first and be indifferent between $h_2$ and $h_3$. Every allocation is weakly blocked: at least one agent $j$ among 2 and 3 does not get $h_1$, and the coalition $\{1, j\}$ trades so that $j$ gets $h_1$ and agent 1 gets $h_j$. Agent $j$ gains and agent 1 does not care. So the strict core is empty, while all six allocations are in the core.
- Let agents 1 and 2 be indifferent between all houses and let agent 3 rank $h_3$ first. Then the strict core has two allocations: the one without trade and the swap of agents 1 and 2.

In both examples a brute force check over all allocations and coalitions gives the stated sets.

## History

Shapley and Scarf (1974) introduced the housing market, proved that its core is not empty and that a competitive allocation exists, and gave the top trading cycle algorithm of David Gale. Roth and Postlewaite (1977) compared weak and strong domination. They proved that with strict preferences the strict core has one element, equal to the unique competitive allocation, and showed that the core under strong domination can be larger. Their result made the core rule a well-defined mechanism, and Roth (1982) then proved that it is strategyproof.

## References
