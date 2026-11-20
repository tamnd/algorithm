---
tag: 4VE6T0
kind: definition
slug: maximin-share
name: Maximin share
aliases:
- MMS
- maximin share guarantee
area: algorithmic-game-theory/fair-division
level: core
summary: The best value an agent can ensure by splitting the goods into n bundles and getting the worst one. An MMS allocation gives each agent that much.
prereqs: [indivisible-goods-allocation, proportional-division]
see_also: [mms-nonexistence-theorem, approximate-mms-allocation, envy-freeness-up-to-one-good, envy-freeness-up-to-any-good, partition-problem, makespan-minimization, competitive-equilibrium-from-equal-incomes, divide-and-choose]
sources:
  - paper: "Eric Budish, The combinatorial assignment problem: approximate competitive equilibrium from equal incomes, Journal of Political Economy 119(6) (2011), 1061-1103"
    locator: the definition of the maximin share guarantee
  - paper: "David Kurokawa, Ariel D. Procaccia and Junxing Wang, Fair enough: guaranteeing approximate maximin shares, Journal of the ACM 65(2) (2018), article 8"
    locator: the instances with no MMS allocation and the existence of 2/3-MMS allocations
  - paper: "Uriel Feige, Ariel Sapir and Laliv Tauber, A tight negative example for MMS fair allocations, WINE 2021 (arXiv:2104.04977)"
    locator: the instance with three agents and nine goods, and the upper bound 39/40
  - paper: doi:10.1016/j.artint.2021.103547
    title: "Jugal Garg and Setareh Taki, An improved approximation algorithm for maximin shares, Artificial Intelligence 300 (2021), 103547"
    locator: the 3/4 + 1/(12n) existence result and the strongly polynomial 3/4 algorithm
  - paper: "Gerhard J. Woeginger, A polynomial-time approximation scheme for maximizing the minimum machine completion time, Operations Research Letters 20(4) (1997), 149-154"
    locator: the approximation scheme for the max-min partition of numbers into n parts
---

The maximin share (MMS) of an agent is a fairness threshold for the [allocation of indivisible goods](/indivisible-goods-allocation/). The agent splits all goods into $n$ bundles, one per agent, knowing that it will get the worst bundle; its maximin share is the value of the worst bundle under the best split. An allocation is an MMS allocation when every agent gets at least its maximin share. The notion replaces the [proportional](/proportional-division/) share $v_i(M)/n$, which indivisible goods often make impossible, with the best value that the agent could ensure in a split by itself, as in [divide and choose](/divide-and-choose/). Budish defined it in 2011.

## Definition

Let $N = \{1, \dots, n\}$ be the agents, $M$ the set of $m$ goods and $v_i$ the valuation of agent $i$. Write $\Pi_n(M)$ for the set of ordered partitions $(P_1, \dots, P_n)$ of $M$ into $n$ bundles, some of which may be empty. The **maximin share** of agent $i$ is

$$\mathrm{MMS}_i = \max_{(P_1, \dots, P_n) \in \Pi_n(M)} \ \min_{k} v_i(P_k).$$

A partition that reaches the maximum is an *MMS partition* of agent $i$. The value depends only on $v_i$, $M$ and $n$, not on the valuations of the other agents.

An allocation $A$ is an **MMS allocation** if $v_i(A_i) \ge \mathrm{MMS}_i$ for every agent $i$. For a factor $0 < \alpha \le 1$, it is **$\alpha$-MMS** if $v_i(A_i) \ge \alpha \cdot \mathrm{MMS}_i$ for every agent $i$.

**Bound by the proportional share.** For an additive $v_i$, the worst bundle of any partition is worth at most the average $v_i(M)/n$, so $\mathrm{MMS}_i \le v_i(M)/n$. Hence every proportional allocation is an MMS allocation.

**Two agents.** An MMS allocation always exists for two agents with additive valuations. Agent 1 makes one of its MMS partitions $(P_1, P_2)$. Agent 2 takes the bundle it prefers, worth at least $v_2(M)/2 \ge \mathrm{MMS}_2$, and agent 1 takes the other one, worth at least $\mathrm{MMS}_1$ by the choice of the partition.

**Cost of computing it.** For additive values, computing $\mathrm{MMS}_i$ is NP-hard. If $n = 2$ and $v_i(M) = S$, then $\mathrm{MMS}_i = S/2$ exactly when the values of the goods can be split into two sets of equal sum, which is the [partition problem](/partition-problem/). The same argument with three numbers per bundle gives strong NP-hardness when $n$ is part of the input. For a fixed $n$ and integer values with sum $S$, a dynamic program over the loads of $n - 1$ bundles takes $O(m S^{n-1})$ time. Computing $\mathrm{MMS}_i$ is the problem of covering $n$ identical machines, the max-min dual of [makespan minimization](/makespan-minimization/), and it has a polynomial-time approximation scheme (theorem, Woeginger 1997). An approximation algorithm can use such estimates in place of exact values.

## Examples and non-examples

- **One good, two agents.** Any partition leaves one bundle empty, so $\mathrm{MMS}_i = 0$ for both agents and every allocation is an MMS allocation. The proportional share is half the value of the good, and no allocation gives it to both.
- **Identical goods.** If agent $i$ values each of $m$ goods at 1, then $\mathrm{MMS}_i = \lfloor m/n \rfloor$.
- **Three agents and six goods.** The agents value goods $a, \dots, f$ at $(8, 7, 4, 3, 2, 1)$, $(8, 2, 6, 5, 1, 3)$ and $(6, 7, 5, 1, 4, 2)$; each total is 25. Each maximin share is 8. MMS partitions are $\{a\}, \{b, e\}, \{c, d, f\}$ for agent 1 (worth 8, 9 and 8), $\{a, e\}, \{b, c\}, \{d, f\}$ for agent 2 (worth 9, 8 and 8), and $\{a, f\}, \{b, d\}, \{c, e\}$ for agent 3 (worth 8, 8 and 9). No partition does better, since a total of 25 in three bundles of at least 9 would need 27. [Round-robin allocation](/round-robin-allocation/) gives $\{a, d\}$, $\{c, f\}$, $\{b, e\}$, worth 11, 9 and 11 to their owners, so it is an MMS allocation.
- **Not an MMS allocation.** In the same instance, $\{a, b\}$, $\{c, d\}$, $\{e, f\}$ gives agent 3 a value of 6, below 8.
- **No MMS allocation at all.** Some instances with three or more agents and additive valuations have no MMS allocation; see [the nonexistence of maximin share allocations](/mms-nonexistence-theorem/). The smallest known example has three agents and nine goods, and in it the best allocation gives every agent only $39/40$ of its share.

## Related definitions

- [Proportionality](/proportional-division/): implies MMS for additive valuations, by the bound above. The converse fails, as in the example with one good.
- [EF1](/envy-freeness-up-to-one-good/) and [EFX](/envy-freeness-up-to-any-good/) compare bundles, while MMS is a threshold for each agent. EF1 and MMS do not imply each other; the EF1 page has an example of each kind.
- **$\alpha$-MMS allocations.** Kurokawa, Procaccia and Wang proved that a $2/3$-MMS allocation always exists for additive valuations (theorem). Garg and Taki (2021) raised the factor to $3/4 + 1/(12n)$ (theorem). The [approximate MMS allocation](/approximate-mms-allocation/) page gives a $3/4$ algorithm, the history of the factor and the later bounds.
- **Upper bounds on $\alpha$.** Feige, Sapir and Tauber (2021) give an instance where no allocation is better than $39/40$-MMS (theorem).
- **The 1-of-$d$ share.** Budish also used the value an agent can ensure by splitting the goods into $d$ bundles for $d > n$, for example $d = n + 1$. This weaker threshold is an ordinal relaxation of MMS, and the approximate [competitive equilibrium from equal incomes](/competitive-equilibrium-from-equal-incomes/) of Budish gives each agent its 1-of-$(n + 1)$ share up to some error.
- **MMS for chores.** For costs, the share is the minimum over partitions of the largest bundle cost, and an allocation must keep each agent's cost at or below it.

## References
