---
tag: BBEKKP
kind: definition
slug: envy-freeness-up-to-one-good
name: Envy-freeness up to one good
aliases:
- EF1
area: algorithmic-game-theory/fair-division
level: core
summary: An allocation in which any envy of one agent for another disappears after removing some single good from the other's bundle.
prereqs: [envy-freeness, indivisible-goods-allocation]
see_also: [envy-freeness-up-to-any-good, maximin-share, round-robin-allocation, envy-cycle-elimination, unreasonable-fairness-of-mnw, ef1-and-pareto-optimal-algorithm, proportional-division]
sources:
  - paper: "Richard J. Lipton, Evangelos Markakis, Elchanan Mossel and Amin Saberi, On approximately fair allocations of indivisible goods, Proceedings of the 5th ACM Conference on Electronic Commerce (EC 2004), 125-131"
    locator: the envy-graph algorithm, whose output has envy at most the largest marginal value of a single good
  - paper: "Eric Budish, The combinatorial assignment problem: approximate competitive equilibrium from equal incomes, Journal of Political Economy 119(6) (2011), 1061-1103"
    locator: the definition of envy bounded by a single good
  - paper: doi:10.1145/3355902
    title: "Ioannis Caragiannis, David Kurokawa, Herve Moulin, Ariel D. Procaccia, Nisarg Shah and Junxing Wang, The unreasonable fairness of maximum Nash welfare, ACM Transactions on Economics and Computation 7(3) (2019), article 12 (conference version EC 2016)"
    locator: Definition 2.2 (EF1) and Theorem 3.2
---

Envy-freeness up to one good (EF1) is a fairness notion for the [allocation of indivisible goods](/indivisible-goods-allocation/): an agent may envy another agent, but the envy must disappear when some single good is removed from the envied bundle. It relaxes [envy-freeness](/envy-freeness/), which can fail for every allocation of indivisible goods. Unlike envy-freeness, an EF1 allocation always exists for monotone valuations, and simple algorithms such as [round-robin allocation](/round-robin-allocation/) and [envy-cycle elimination](/envy-cycle-elimination/) find one. The stronger notion [EFX](/envy-freeness-up-to-any-good/) asks that the envy disappear whichever good is removed.

## Definition

Let $N = \{1, \dots, n\}$ be the agents, $M$ the set of $m$ goods, and $v_i$ the valuation of agent $i$, with $v_i(\emptyset) = 0$. An allocation $A = (A_1, \dots, A_n)$ is a list of disjoint bundles that cover $M$. Agent $i$ envies agent $j$ when $v_i(A_j) > v_i(A_i)$.

The allocation is **EF1** if for all agents $i$ and $j$ with $A_j \ne \emptyset$ there is a good $g \in A_j$ with

$$v_i(A_i) \ge v_i(A_j \setminus \{g\}).$$

The condition on $A_j \ne \emptyset$ is needed only to make the quantifier over $g$ meaningful: an empty bundle is never envied when $v_i$ is nonnegative.

For additive valuations, the best good to remove is the one that $i$ values most in $A_j$, so the test becomes

$$v_i(A_i) \ge v_i(A_j) - \max_{g \in A_j} v_i(g).$$

With the $n \times m$ table of values, all sums $v_i(A_j)$ and all maxima take $O(n m)$ time in total, since each good adds to one sum and one maximum per agent. So EF1 is checked in $O(n m)$ time. For general valuations given by an oracle, the test takes $\sum_{i} \sum_{j \ne i} |A_j| \le n m$ value queries.

**EF1 gives proportionality up to one good.** For additive valuations, let $g^*$ be a good outside $A_i$ of largest value to $i$ (if $A_i = M$, agent $i$ has everything). Each $j \ne i$ has a good $g_j$ with $v_i(A_i) \ge v_i(A_j) - v_i(g_j) \ge v_i(A_j) - v_i(g^*)$. Adding these $n - 1$ inequalities to $v_i(A_i) = v_i(A_i)$ gives $n\, v_i(A_i) \ge v_i(M) - (n - 1) v_i(g^*)$, so

$$v_i(A_i) + \tfrac{n - 1}{n} v_i(g^*) \ge \tfrac{1}{n} v_i(M).$$

Each agent misses its [proportional](/proportional-division/) share by less than the value of one good that it does not hold.

## Examples and non-examples

Two agents have the same additive values for three goods: $a$ is worth 5, $b$ is worth 3 and $c$ is worth 1, so the total is 9.

- **EF1 but not envy-free.** $A_1 = \{a\}$ and $A_2 = \{b, c\}$, with utilities 5 and 4. Agent 2 envies agent 1, since $5 > 4$. Removing $a$ leaves the empty bundle, worth $0 \le 4$, so the allocation is EF1. No allocation here is envy-free: with identical values, envy-freeness needs two bundles of equal value, and 9 is odd.
- **Not EF1.** $A_1 = \{a, b\}$ and $A_2 = \{c\}$. Agent 2 has 1. Removing $a$ from $A_1$ leaves 3, and removing $b$ leaves 5; both exceed 1.
- **EF1 but not EFX.** $A_1 = \{a, c\}$ and $A_2 = \{b\}$. Agent 2 has 3 and values $A_1$ at 6. Removing $a$ leaves $1 \le 3$, so the allocation is EF1. Removing $c$ leaves $5 > 3$, so it is not [EFX](/envy-freeness-up-to-any-good/).
- **Round-robin.** Three agents value six goods $a, \dots, f$ at $(8, 7, 4, 3, 2, 1)$, $(8, 2, 6, 5, 1, 3)$ and $(6, 7, 5, 1, 4, 2)$. [Round-robin allocation](/round-robin-allocation/) in the order 1, 2, 3 gives $\{a, d\}$, $\{c, f\}$ and $\{b, e\}$. Agent 2 values $\{a, d\}$ at 13 and its own bundle at 9, so it envies agent 1; without $a$ the bundle is worth 5, so the envy is EF1.
- **EF1 is not efficiency.** Two agents value goods $a$ and $b$ at $(1, 0)$ and $(0, 1)$. The allocation $A_1 = \{b\}$, $A_2 = \{a\}$ is EF1, since each bundle has one good, but both agents get 0, while the swap gives both 1. So EF1 does not imply [Pareto optimality](/pareto-optimality/).

## Related definitions

- [Envy-freeness](/envy-freeness/) (EF): no envy at all. EF implies EF1.
- [Envy-freeness up to any good](/envy-freeness-up-to-any-good/) (EFX): the envy disappears whichever good of $A_j$ is removed. EFX implies EF1. EF1 always exists, while the existence of EFX is proved only for some cases.
- [Maximin share](/maximin-share/) (MMS): a threshold for each agent that does not compare bundles. Neither EF1 nor MMS implies the other. In the first examples above, the MMS of each agent is 4 (from $\{a\}, \{b, c\}$), and $A_1 = \{a, c\}$, $A_2 = \{b\}$ is EF1 but gives agent 2 only 3. Conversely, let agents 1 and 2 value six goods at 1 each, and let agent 3 value only $a$ and $b$, at 1 each; the MMS values are 2, 2 and 0. The allocation $(\{a, b\}, \{c, d, e, f\}, \emptyset)$ meets every MMS, but agent 1 values $\{c, d, e, f\}$ at 3 after any removal, more than its own 2, so it is not EF1.
- EF$k$: the envy disappears after removing at most $k$ goods. EF1 is the case $k = 1$.
- EF1 for chores: each agent's envy disappears after removing one chore from its own bundle. The direction of the removal is reversed, because a chore lowers the value.
- EF1 and Pareto optimal together: every [maximum Nash welfare](/maximum-nash-welfare/) allocation has both properties for additive valuations ([the unreasonable fairness of MNW](/unreasonable-fairness-of-mnw/)), and the [Barman-Krishnamurthy-Vaish algorithm](/ef1-and-pareto-optimal-algorithm/) finds such an allocation in pseudo-polynomial time.

History: Lipton, Markakis, Mossel and Saberi (2004) gave an algorithm whose envy is at most the largest marginal value of a single good. Budish (2011) used the bound "envy bounded by a single good" in course allocation. The name EF1 is used by Caragiannis et al. (2019), who proved that maximum Nash welfare gives EF1 together with Pareto optimality.

## References
