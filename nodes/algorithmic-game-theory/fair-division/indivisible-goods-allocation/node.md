---
tag: HB9XJZ
kind: problem
slug: indivisible-goods-allocation
name: Fair allocation of indivisible goods
aliases:
- fair division of indivisible items
area: algorithmic-game-theory/fair-division
level: core
summary: Allocate a set of indivisible goods among agents with additive or general valuations so that the allocation satisfies a fairness notion.
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of goods}
  time: {worst: O(n m log m)}
prereqs: [envy-freeness, proportional-division, pareto-optimality]
see_also: [envy-freeness-up-to-one-good, envy-freeness-up-to-any-good, maximin-share, round-robin-allocation, envy-cycle-elimination, maximum-nash-welfare, cake-cutting-problem, chore-division]
sources:
  - paper: "Eric Budish, The combinatorial assignment problem: approximate competitive equilibrium from equal incomes, Journal of Political Economy 119(6) (2011), 1061-1103"
    locator: the definitions of the maximin share guarantee and of envy bounded by a single good
  - paper: "Richard J. Lipton, Evangelos Markakis, Elchanan Mossel and Amin Saberi, On approximately fair allocations of indivisible goods, Proceedings of the 5th ACM Conference on Electronic Commerce (EC 2004), 125-131"
    locator: the envy-graph algorithm, which bounds envy by the largest value of one good
  - paper: doi:10.1145/3355902
    title: "Ioannis Caragiannis, David Kurokawa, Herve Moulin, Ariel D. Procaccia, Nisarg Shah and Junxing Wang, The unreasonable fairness of maximum Nash welfare, ACM Transactions on Economics and Computation 7(3) (2019), article 12 (conference version EC 2016)"
    locator: Section 2 (EF1, MMS and PO) and Theorem 3.2 (maximum Nash welfare is EF1 and PO)
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: Chapter 12, Sylvain Bouveret, Yann Chevaleyre and Nicolas Maudet, Fair allocation of indivisible goods
---

The fair allocation of indivisible goods asks how to give a set of goods, each of which must go whole to one agent, to agents who value the goods differently, so that the result is fair by a stated rule. Unlike the [cake cutting problem](/cake-cutting-problem/), the goods cannot be split, so [envy-freeness](/envy-freeness/) and [proportional division](/proportional-division/) can fail for every allocation, even with two agents and one good. The field therefore uses weaker goals: [envy-freeness up to one good](/envy-freeness-up-to-one-good/) (EF1), [envy-freeness up to any good](/envy-freeness-up-to-any-good/) (EFX) and the [maximin share](/maximin-share/) (MMS), often together with [Pareto optimality](/pareto-optimality/). EF1 can be reached in polynomial time; EFX and good MMS guarantees are still research questions.

## In plain words

A family must share an inheritance: a house, a car, a painting, some jewels. Nobody can get half a car. Each person has their own idea of what each thing is worth. If there is only one valuable thing, somebody gets it and the others feel cheated, whatever we do. So "nobody envies anybody" is too strong a goal.

Weaker goals still make sense. One goal says: if you envy someone, the envy goes away when you take away one item from that person's share. Another goal says: you get at least what you could secure if you split the items into piles yourself and the others chose first. A third goal is efficiency: no other split is better for someone and worse for nobody. The problem is to find a split that meets such goals, and to find it fast.

## Definition

**Input.** A set $N = \{1, \dots, n\}$ of agents, a set $M$ of $m$ indivisible goods, and for each agent $i$ a valuation $v_i : 2^M \to \mathbb{R}_{\ge 0}$ with $v_i(\emptyset) = 0$. The valuation is monotone if $S \subseteq T$ implies $v_i(S) \le v_i(T)$, and additive if $v_i(S) = \sum_{g \in S} v_i(g)$. Additive valuations are given as an $n \times m$ table of numbers; general valuations are given by a value oracle that returns $v_i(S)$ for a query $S$.

**Output.** An allocation $A = (A_1, \dots, A_n)$: disjoint bundles with $A_1 \cup \dots \cup A_n = M$. Agent $i$ gets $A_i$ and has utility $v_i(A_i)$.

**Goal.** The allocation must satisfy a fairness notion, sometimes together with an efficiency notion. The main notions, for all agents $i$ and $j$:

- envy-free (EF): $v_i(A_i) \ge v_i(A_j)$;
- proportional (PROP): $v_i(A_i) \ge v_i(M)/n$;
- [EF1](/envy-freeness-up-to-one-good/): if $A_j \ne \emptyset$, then $v_i(A_i) \ge v_i(A_j \setminus \{g\})$ for some $g \in A_j$;
- [EFX](/envy-freeness-up-to-any-good/): $v_i(A_i) \ge v_i(A_j \setminus \{g\})$ for every $g \in A_j$ (some papers require this only for goods with $v_i(g) > 0$);
- [MMS](/maximin-share/): $v_i(A_i) \ge \mathrm{MMS}_i$, where $\mathrm{MMS}_i$ is the largest value $\min_k v_i(B_k)$ over all partitions $(B_1, \dots, B_n)$ of $M$; the allocation is $\alpha$-MMS if $v_i(A_i) \ge \alpha\, \mathrm{MMS}_i$ for every $i$;
- Pareto optimal (PO): no allocation $A'$ has $v_k(A'_k) \ge v_k(A_k)$ for all $k$ with strict inequality for some $k$.

The measure is either a yes or no (is the notion met?) or an approximation factor (the largest $\alpha$ that is met). The complexity bound in the front matter is for EF1 with additive valuations, by [round-robin allocation](/round-robin-allocation/).

## Variants

- **Valuation classes.** Additive, [submodular](/submodular-function/), subadditive or general monotone valuations. Many results hold only for additive valuations; envy-cycle elimination gives EF1 for all monotone valuations.
- **Chores.** Items with costs instead of values, as in [chore division](/chore-division/). Each fairness notion reverses its inequalities, and the results differ.
- **Mixed items.** Some items are goods for some agents and chores for others.
- **Constraints.** Bundles of bounded size (cardinality constraints), connected bundles of goods on a line or a graph, or matroid constraints.
- **Unequal entitlements.** Agents have weights, and the fairness notions are weighted.
- **Unit demand.** If each agent can use one good only, the problem becomes the [house allocation problem](/house-allocation-problem/), with rules such as [serial dictatorship](/serial-dictatorship/).
- **Randomized allocation.** A lottery over allocations that is envy-free in expectation, as in [probabilistic serial](/probabilistic-serial/), can be combined with EF1 for each allocation in its support.

## Examples

**One good.** Two agents both value one good at 1. Whoever gets it is envied by the other, and the other gets $0 < 1/2$, so no allocation is EF or PROP. Both allocations are EF1, EFX and MMS, because each agent's MMS is 0: one of the two bundles of any partition is empty.

**Three agents and six goods.** Let the goods be $a, \dots, f$ and the additive values be

| agent | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | total |
|---|---|---|---|---|---|---|---|
| 1 | 8 | 7 | 4 | 3 | 2 | 1 | 25 |
| 2 | 8 | 2 | 6 | 5 | 1 | 3 | 25 |
| 3 | 6 | 7 | 5 | 1 | 4 | 2 | 25 |

Every agent has MMS 8. No partition can give an agent three bundles worth at least 9 each, because that needs a total of at least 27 and each total is 25. Agent 1 reaches 8 with $\{a\}, \{b, e\}, \{c, d, f\}$ (worth 8, 9 and 8), agent 2 with $\{a, e\}, \{b, c\}, \{d, f\}$ (worth 9, 8 and 8), and agent 3 with $\{a, f\}, \{b, d\}, \{c, e\}$ (worth 8, 8 and 9).

- [Round-robin allocation](/round-robin-allocation/) in the order 1, 2, 3 gives $\{a, d\}$, $\{c, f\}$, $\{b, e\}$ with utilities 11, 9 and 11. Agent 2 values the bundle of agent 1 at $8 + 5 = 13 > 9$, so the allocation is not EF; after removing $a$, agent 2 values it at 5, so the envy is EF1. The allocation is also EFX, MMS and PO.
- The allocation $\{b, d\}$, $\{a, f\}$, $\{c, e\}$ is envy-free: the three agents value the three bundles at $(10, 9, 6)$, $(7, 11, 7)$ and $(8, 8, 9)$, and each agent values its own bundle highest. Three of the 729 allocations are envy-free.
- The [maximum Nash welfare](/maximum-nash-welfare/) allocation is $\{a\}$, $\{c, d, f\}$, $\{b, e\}$, with utilities 8, 14 and 11 and product 1232. Agent 1 envies agent 3 ($9 > 8$), but not after removing $b$.

## Known algorithms

- [Round-robin allocation](/round-robin-allocation/): agents pick in turn. EF1 for additive valuations, in $O(n m \log m)$ time. Not PO in general.
- [Envy-cycle elimination](/envy-cycle-elimination/) (Lipton, Markakis, Mossel and Saberi 2004): EF1 for all monotone valuations, with $O(m n^3)$ value queries.
- [Maximum Nash welfare](/maximum-nash-welfare/): EF1 and PO for additive valuations ([the unreasonable fairness of MNW](/unreasonable-fairness-of-mnw/)), but NP-hard to compute.
- [The Barman-Krishnamurthy-Vaish algorithm](/ef1-and-pareto-optimal-algorithm/): EF1 and PO for additive valuations in pseudo-polynomial time, by a market with prices.
- [Approximate MMS allocation](/approximate-mms-allocation/): a $3/4$-MMS allocation for additive valuations in polynomial time (Garg and Taki).
- Exhaustive search over all $n^m$ allocations, or [mixed integer programming](/mixed-integer-programming/), for small instances and for exact checks of any notion.

## Bounds

The following results are for additive valuations unless a line says otherwise. Each is a theorem unless it is marked open or preprint.

- **EF and PROP.** May not exist (one good). Deciding whether an EF allocation exists is NP-complete even for two agents with identical valuations, by a reduction from the [partition problem](/partition-problem/): an EF allocation for two identical agents is a split into two halves of equal value.
- **EF1.** Always exists for monotone valuations, and is found in polynomial time (round-robin for additive, envy-cycle elimination for monotone).
- **EF1 and PO.** Exist for additive valuations (Caragiannis et al. 2019). An EF1 and fractionally PO allocation is found in pseudo-polynomial time (Barman, Krishnamurthy and Vaish 2018). Whether it can be found in polynomial time for any number of agents is open (stated as open by Mahara, arXiv:2411.01810, 2024); for a fixed number of agents a polynomial algorithm is known (same preprint). For subadditive and for supermodular valuations, EF1 and PO allocations may not exist (Caragiannis et al. 2019, Theorem 3.3).
- **EFX.** Exists for two agents with monotone valuations and for identical valuations (Plaut and Roughgarden 2020), and for three agents with additive valuations ([Chaudhury, Garg and Mehlhorn 2024](/efx-existence-for-three-agents/)). Existence for four or more additive agents is open (as of the 2026 sources cited on the EFX page).
- **MMS.** May not exist ([Kurokawa, Procaccia and Wang 2018](/mms-nonexistence-theorem/)); with three agents and nine goods, some instance gives some agent at most $39/40$ of its MMS in every allocation (Feige, Sapir and Tauber 2021). A $3/4$-MMS allocation exists and is found in polynomial time (Garg and Taki 2021); the best proved existence factor is above $3/4$ (see [approximate MMS allocation](/approximate-mms-allocation/)). The best factor is open.
- **Maximum Nash welfare.** NP-hard already for two agents, APX-hard (Lee 2017), and approximable within a constant factor (see [maximum Nash welfare](/maximum-nash-welfare/)).

## Reductions

- With two agents and identical additive values, an EF or PROP allocation exists exactly when the values can be split into two halves of equal sum. So deciding EF or PROP is as hard as the [partition problem](/partition-problem/), and computing $\mathrm{MMS}_i$ for $n = 2$ is the optimization form of it.
- Computing $\mathrm{MMS}_i$ for $n$ bundles is the max-min version of scheduling on identical machines: goods are jobs, bundles are machines, and the goal is to maximize the smallest load. [Bin packing](/bin-packing/) is a close relative.
- For divisible goods with linear values, the [competitive equilibrium from equal incomes](/competitive-equilibrium-from-equal-incomes/) gives an EF and PO allocation and maximizes the Nash welfare (the [Eisenberg-Gale program](/eisenberg-gale-program/)). The methods for indivisible goods often start from this market view: the Barman-Krishnamurthy-Vaish algorithm keeps prices so that each agent buys only goods of maximum value per price.
- Ordered instances: for MMS, it is enough to solve instances in which all agents rank the goods in the same order. A solution there maps back by a picking sequence; the [approximate MMS allocation](/approximate-mms-allocation/) page proves this.

## Applications

- Inheritance, divorce and the split of household items. The website Spliddit uses maximum Nash welfare for its "divide goods" application (Caragiannis et al. 2019).
- Course allocation: Budish defined EF1 and MMS for the assignment of courses to students, where each student takes several courses with limited seats.

## References
