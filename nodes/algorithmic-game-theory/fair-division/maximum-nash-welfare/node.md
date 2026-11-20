---
tag: MP0NH0
kind: problem
slug: maximum-nash-welfare
name: Maximum Nash welfare allocation
aliases:
- MNW
- Nash social welfare maximization
area: algorithmic-game-theory/fair-division
level: core
summary: Find an allocation of goods that maximizes the product of the agents' utilities. It is APX-hard for indivisible goods.
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of goods}
  time: {worst: O(n^m (n + m))}
prereqs: [indivisible-goods-allocation, pareto-optimality]
see_also: [unreasonable-fairness-of-mnw, nash-bargaining-solution, eisenberg-gale-program, fisher-market, proportional-fairness, ef1-and-pareto-optimal-algorithm, apx, partition-problem]
sources:
  - paper: doi:10.1145/3355902
    title: "Ioannis Caragiannis, David Kurokawa, Herve Moulin, Ariel D. Procaccia, Nisarg Shah and Junxing Wang, The unreasonable fairness of maximum Nash welfare, ACM Transactions on Economics and Computation 7(3) (2019), article 12 (conference version EC 2016)"
    locator: Definition 3.1 (the MNW rule with the case of zero welfare), Section 1.1 (Spliddit) and Section 5 (the mixed integer program)
  - paper: "Trung Thanh Nguyen, Magnus Roos and Joerg Rothe, A survey of approximability and inapproximability results for social welfare optimization in multiagent resource allocation, Annals of Mathematics and Artificial Intelligence (2013)"
    locator: the strong NP-hardness of maximizing Nash welfare
  - paper: "Euiwoong Lee, APX-hardness of maximizing Nash social welfare with indivisible items, Information Processing Letters 122 (2017), 17-20"
    locator: the APX-hardness of MNW for additive valuations
  - paper: "Jugal Garg, Martin Hoefer and Kurt Mehlhorn, Approximating the Nash social welfare with budget-additive valuations, Proceedings of the 29th ACM-SIAM Symposium on Discrete Algorithms (SODA 2018)"
    locator: the hardness factor sqrt(8/7) for additive valuations
  - paper: "Richard Cole and Vasilis Gkatzelis, Approximating the Nash social welfare with indivisible items, Proceedings of the 47th ACM Symposium on Theory of Computing (STOC 2015)"
    locator: the first constant-factor approximation algorithm
  - paper: "Siddharth Barman, Sanath Kumar Krishnamurthy and Rohit Vaish, Finding fair and efficient allocations, Proceedings of the 19th ACM Conference on Economics and Computation (EC 2018), 557-574 (arXiv:1707.04731)"
    locator: Theorem 3 (approximation factor about 1.45)
---

A maximum Nash welfare (MNW) allocation gives indivisible goods to agents so that the product of their utilities is as large as possible. This page treats MNW as an optimization problem: its definition, its hardness and the algorithms that solve it exactly or approximately. The separate page on [the unreasonable fairness of MNW](/unreasonable-fairness-of-mnw/) states and proves the theorem that every MNW allocation is [EF1](/envy-freeness-up-to-one-good/) and [Pareto optimal](/pareto-optimality/) for additive valuations, which is the main reason to solve this problem. The objective comes from the [Nash bargaining solution](/nash-bargaining-solution/); for divisible goods it is the [Eisenberg-Gale program](/eisenberg-gale-program/), which is solved in polynomial time, but for indivisible goods the problem is NP-hard and APX-hard.

## In plain words

Each agent says how much it likes each item. We want to split the items so that the result is both efficient and fair. Adding up the happiness of all agents is efficient but can give everything to one enthusiastic agent. Taking only the least happy agent into account is fair but ignores everyone else. Multiplying the happiness values is a middle road: a split in which one agent gets nothing scores zero, and a small gain for a poor agent counts as much as a large gain for a rich one. The product also ignores the units that each agent uses, so an agent cannot gain by stating bigger numbers on every item. The cost is that finding the best split is hard when items cannot be divided.

## Definition

**Input.** Agents $N = \{1, \dots, n\}$, goods $M$ with $|M| = m$, and for each agent an additive valuation given by values $v_i(g) \ge 0$.

**Output.** An allocation $A = (A_1, \dots, A_n)$ of all goods that maximizes the Nash welfare

$$\mathrm{NW}(A) = \Big( \prod_{i=1}^{n} v_i(A_i) \Big)^{1/n}.$$

The $n$-th root does not change the maximizer; it makes the value scale like a single utility.

**Zero welfare.** If every allocation gives some agent the value 0, the product is 0 for all allocations and the plain rule says nothing. The rule of Caragiannis et al. (Definition 3.1) then first finds a largest set $S$ of agents that can get positive values at the same time, and among the allocations that give every agent in $S$ a positive value it maximizes $\prod_{i \in S} v_i(A_i)$. For additive valuations, a set $S$ can be served this way exactly when the bipartite graph between agents and goods with an edge for each positive value has a matching that covers $S$, so a largest $S$ comes from a [maximum bipartite matching](/bipartite-matching/).

**Scale invariance.** Replacing $v_i$ by $c_i v_i$ with $c_i > 0$ multiplies the product by $\prod_i c_i$ and so keeps the same maximizers. The utilitarian rule, which maximizes $\sum_i v_i(A_i)$, does not have this property.

## Variants

- **Weighted Nash welfare.** Maximize $\prod_i v_i(A_i)^{w_i}$ for agent weights $w_i > 0$; equal weights give MNW.
- **Divisible goods.** If goods can be split, maximizing $\sum_i \log v_i(x_i)$ is the Eisenberg-Gale convex program. Its optimum is the competitive equilibrium of a [Fisher market](/fisher-market/) in which every agent has the same budget, and the [DPSV algorithm](/dpsv-algorithm/) computes it for linear values.
- **Other valuation classes.** The same objective is studied for budget-additive, submodular and general monotone valuations; the hardness results below already hold for additive ones.

## Examples

- **Sum against product.** Agent 1 values goods $a$ and $b$ at 2 each and agent 2 at 1 each. The utilitarian rule gives both goods to agent 1, for a sum of 4; agent 2 has 0 and values agent 1's bundle at 1 even after removing a good, so this is not EF1. MNW gives one good to each agent, with product $2 \cdot 1 = 2$, and nobody envies anybody.
- **Three agents and six goods.** The agents value goods $a, \dots, f$ at $(8, 7, 4, 3, 2, 1)$, $(8, 2, 6, 5, 1, 3)$ and $(6, 7, 5, 1, 4, 2)$. The unique MNW allocation is $\{a\}$, $\{c, d, f\}$, $\{b, e\}$, with values 8, 14 and 11 and product 1232. The round-robin allocation $\{a, d\}$, $\{c, f\}$, $\{b, e\}$ has product $11 \cdot 9 \cdot 11 = 1089$. In the MNW allocation agent 1 values $\{b, e\}$ at 9, more than its own 8, so MNW is not envy-free here; without $b$ the bundle is worth 2, so the envy is within EF1.
- **Zero welfare.** Add a fourth agent that values every good at 0. Every allocation then has product 0. The rule gives agents 1 to 3 the allocation above and the fourth agent nothing.

## Known algorithms

- **Exhaustive search.** Try all $n^m$ allocations and evaluate each in $O(n + m)$ time. This is the bound in the front matter.
- **Mixed integer programs.** For integer values, a continuous variable $W_i$ stands for $\log v_i(A_i)$ and is bounded from above by linear constraints whose tightest bound at every integer point $x$ is $\log x$; this is exact because $\log$ is concave. The result is a [mixed integer linear program](/mixed-integer-programming/) with $n m$ binary variables and $n$ continuous ones. Caragiannis et al. (Section 5) use it on Spliddit, where values are integers that sum to 1000 for each agent, and report that it solves every Spliddit instance in under 3 seconds (measurement).
- **Approximation.** Cole and Gkatzelis (2015) gave the first constant-factor algorithm, with factor about $2.89$, by rounding a market equilibrium with spending limits (theorem). Barman, Krishnamurthy and Vaish (2018) reach $e^{1/e} \approx 1.45$ (theorem, Theorem 3) with the price-rise method of the [Barman-Krishnamurthy-Vaish algorithm](/ef1-and-pareto-optimal-algorithm/): its EF1 and Pareto optimal output is also an approximate MNW allocation.

## Bounds

- **NP-hard for two agents.** See the reduction below. For a fixed $n$ the problem is only weakly NP-hard: a dynamic program that stores, for each list of values of agents 1 to $n - 1$, the best value of agent $n$ runs in time polynomial in $m$ and the largest value.
- **Strongly NP-hard.** When $n$ is part of the input, a reduction from exact cover by 3-sets shows strong NP-hardness (theorem, Nguyen, Roos and Rothe 2013, as cited by Caragiannis et al.), so no pseudo-polynomial algorithm exists unless P = NP.
- **APX-hard.** Lee (2017) proved that MNW has no polynomial-time approximation scheme unless P = NP (theorem). Garg, Hoefer and Mehlhorn (2018) raised the hardness factor to $\sqrt{8/7} \approx 1.069$ for additive valuations (theorem).
- **Fairness of the optimum.** Every MNW allocation is EF1 and Pareto optimal for additive valuations, and gives every agent at least $2/(1 + \sqrt{4n - 3})$ of its [maximin share](/maximin-share/), which is tight. Both results are on the [unreasonable fairness](/unreasonable-fairness-of-mnw/) page.

## Reductions

**From [PARTITION](/partition-problem/).** Given positive integers $a_1, \dots, a_m$ with sum $2T$, make two agents with the same values $v_1(g_k) = v_2(g_k) = a_k$. If the two bundles have values $x$ and $2T - x$, the product is $x(2T - x) \le T^2$, with equality exactly when $x = T$. So the maximum product is $T^2$ if and only if the numbers can be split into two halves of equal sum, and MNW with two agents is NP-hard.

**To convex programming.** Dropping integrality gives the Eisenberg-Gale program, whose optimum bounds the MNW value from above. The approximation algorithms above round such a market solution.

## Applications

- **Spliddit.** The website Spliddit uses MNW in its tool for dividing goods, such as items of an estate, because the result is EF1 and Pareto optimal (Caragiannis et al.).
- **Bandwidth and resource sharing.** The same objective, under the name [proportional fairness](/proportional-fairness/), is used to share divisible network capacity.

## References
