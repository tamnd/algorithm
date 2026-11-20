---
tag: VH9BQY
kind: theorem
slug: mms-nonexistence-theorem
name: Nonexistence of maximin share allocations
aliases:
- Kurokawa-Procaccia-Wang theorem
area: algorithmic-game-theory/fair-division
level: advanced
summary: There are additive instances in which no allocation gives every agent its maximin share, though a constant fraction is always possible.
prereqs: [maximin-share]
see_also: [approximate-mms-allocation, indivisible-goods-allocation, divide-and-choose, efx-existence-for-three-agents, envy-freeness-up-to-one-good, round-robin-allocation, chore-division, partition-problem]
sources:
  - paper: "David Kurokawa, Ariel D. Procaccia and Junxing Wang, Fair enough: guaranteeing approximate maximin shares, Journal of the ACM 65(2) (2018), article 8"
    locator: the instances with no MMS allocation and the existence of 2/3-MMS allocations
  - paper: "Uriel Feige, Ariel Sapir and Laliv Tauber, A tight negative example for MMS fair allocations, WINE 2021 (arXiv:2104.04977)"
    locator: "Theorem 1 and Section 2 (the instance with three agents and nine goods and its proof), Theorems 2 to 5, and Propositions 7 and 8"
  - paper: "Eric Budish, The combinatorial assignment problem: approximate competitive equilibrium from equal incomes, Journal of Political Economy 119(6) (2011), 1061-1103"
    locator: the definition of the maximin share guarantee
  - paper: "Ezra and Garbuz, arXiv:2609.15085 (September 2026), preprint"
    locator: the claimed instance with four agents and eleven goods with no allocation better than 20/21-MMS
  - paper: "Gupta and Seetharaman, arXiv:2609.15841 (September 2026), preprint"
    locator: the claimed Delta_2^P-completeness of deciding whether an MMS allocation exists
---

The nonexistence theorem for maximin share allocations states that, with three or more agents and additive valuations, there are instances of [indivisible goods allocation](/indivisible-goods-allocation/) in which no allocation gives every agent its [maximin share](/maximin-share/) (MMS). Kurokawa, Procaccia and Wang proved it, and they also proved that every agent can always get $2/3$ of its share. Feige, Sapir and Tauber later found the smallest such instance, with three agents and nine goods, where the best allocation gives some agent only $39/40$ of its share. The theorem is the reason that the field studies [approximate MMS allocations](/approximate-mms-allocation/).

## Statement

For $n$ agents with additive valuations $v_i \ge 0$ on a set $M$ of goods, $\mathrm{MMS}_i$ is the maximum over all partitions of $M$ into $n$ bundles of the smallest value $v_i$ of a bundle. An allocation $A$ is an MMS allocation if $v_i(A_i) \ge \mathrm{MMS}_i$ for every agent $i$.

**Theorem (Kurokawa, Procaccia and Wang; Feige, Sapir and Tauber, Theorems 1 and 4).**

1. There is an instance with three agents and nine goods in which every allocation gives some agent at most $\frac{39}{40}\mathrm{MMS}_i$.
2. For every $n \ge 4$ there is an instance with $n$ agents and at most $3n + 3$ goods in which every allocation gives some agent at most $(1 - 1/n^4)\,\mathrm{MMS}_i$.

So for every $n \ge 3$, MMS allocations need not exist. For $n \le 2$ they always exist (see Tightness).

## In plain words

Each person's fair share is what they could ensure by splitting the items into as many piles as there are people and then getting the worst pile. With two people this share can always be met: one splits, the other picks.

With three people it can fail. In the example below, nine items sit in a three by three grid. One person is happy only with the rows, another only with the columns, and a third with a third way of splitting. Each person has several piles that meet their share, but every way to split the items into three piles leaves some person below their share. The fix is small: everybody can still get almost all of their share, and the gap in this example is one fortieth.

## Proof

The proof of part 1 is the instance of Feige, Sapir and Tauber (Section 2), with a full check by hand. Part 2 is cited.

**The instance.** Put the goods in a grid with rows $r_1, r_2, r_3$ and columns $c_1, c_2, c_3$:

$$\begin{pmatrix} e_1 & e_2 & e_3 \\ e_4 & e_5 & e_6 \\ e_7 & e_8 & e_9 \end{pmatrix}.$$

The three agents are $R$ (rows), $C$ (columns) and $U$ (unbalanced), with these values:

$$R: \begin{pmatrix} 1 & 16 & 23 \\ 26 & 4 & 10 \\ 12 & 19 & 9 \end{pmatrix}, \quad C: \begin{pmatrix} 1 & 16 & 22 \\ 26 & 4 & 9 \\ 13 & 20 & 9 \end{pmatrix}, \quad U: \begin{pmatrix} 1 & 15 & 23 \\ 25 & 4 & 10 \\ 13 & 20 & 9 \end{pmatrix}.$$

**Every share is 40.** Each agent values all goods at 120, so no partition into three bundles has a smallest bundle above 40. For $R$, every row is worth 40. For $C$, every column is worth 40. For $U$, the bundles $p = \{e_2, e_4\}$, $d = \{e_3, e_5, e_7\}$ and $q = \{e_1, e_6, e_8, e_9\}$ are each worth 40. So $\mathrm{MMS}_R = \mathrm{MMS}_C = \mathrm{MMS}_U = 40$.

**The three partitions above fail.** In the partition into rows, $C$ and $U$ each value only $r_3$ at 40 or more ($C$ values $r_1, r_2$ at 39; $U$ values them at 39); so one of them gets less than 40. In the partition into columns, $R$ and $U$ each value only $c_3$ at 40 or more. In the partition $(p, d, q)$, $R$ and $C$ each value only $p$ at 40 or more ($R$ values $d$ at 39 and $q$ at 39; $C$ values them at 39 and 39).

**No other partition can work.** Let $w(e)$ be the largest value of $e$ over the three agents:

$$w: \begin{pmatrix} 1 & 16 & 23 \\ 26 & 4 & 10 \\ 13 & 20 & 9 \end{pmatrix}, \qquad w(M) = 122.$$

Suppose an allocation gives every agent at least 40. Then each of its three bundles has $w$-value at least 40, and since the total is 122, each bundle has $w$-value at most 42. No single good is worth 40, so each bundle has at least two goods.

- If some bundle has two goods, it is a pair with $w$-value from 40 to 42. The only such pair is $p = \{e_2, e_4\}$, with $w(p) = 42$. Then the other two bundles have $w$-value exactly 40 each. The bundle with $e_3$ must reach 40 from 23, which only $e_5$ and $e_7$ (values 4 and 13) do, so the bundles are $d$ and $q$. This is the partition $(p, d, q)$, which fails.
- Otherwise every bundle has three goods. The bundle with $e_9$ has $w$-value from 40 to 42, and the only such triples are $r_3 = \{e_7, e_8, e_9\}$ and $c_3 = \{e_3, e_6, e_9\}$, both with $w$-value 42. The other two bundles then have $w$-value 40 each. The triples with $e_4$ and $w$-value 40 are $r_2$ and $c_1$. With $r_3$, the bundle with $e_4$ is $r_2$ and the last bundle is $r_1$; with $c_3$, it is $c_1$ and then $c_2$. These are the partitions into rows and columns, which fail.

So no allocation gives every agent 40. All values are integers, so some agent gets at most $39 = \frac{39}{40}\mathrm{MMS}_i$. $\square$

**Part 2** is Theorem 4 of Feige, Sapir and Tauber. It uses a group of row agents and a group of column agents, at least two in each, with goods on the border and the main diagonal of an $n \times n$ grid. Every row and every column is worth the share, and a lemma on the other partitions into bundles of that value (Lemma 11) shows that no allocation satisfies both groups. It is cited, not proved here. $\blacksquare$

## Consequences

- **Approximation is the right goal.** Since an exact MMS allocation can fail to exist, the question is the largest $\alpha$ such that an $\alpha$-MMS allocation always exists. Kurokawa, Procaccia and Wang proved $\alpha \ge 2/3$ (theorem). The later lower bounds and the algorithms are on the [approximate MMS allocation](/approximate-mms-allocation/) page. Part 1 gives the upper bound $\alpha \le 39/40$ (theorem).
- **A contrast with EF1.** [EF1](/envy-freeness-up-to-one-good/) allocations always exist, for example by [round-robin](/round-robin-allocation/). With two agents, an EF1 allocation can give an agent only half of its share: if both agents value three goods at 10, 1 and 1, each share is 2, and the allocation that gives agent 1 one good worth 1 and agent 2 the other two goods is EF1 but gives agent 1 only 1.
- **Deciding existence is hard.** A preprint shows that deciding whether a given instance has an MMS allocation is $\Delta_2^P$-complete (Gupta and Seetharaman, arXiv:2609.15841, September 2026, preprint).
- **Chores.** For [chores](/chore-division/) with additive costs, Feige, Sapir and Tauber (Theorem 5) give three agents and nine chores in which every allocation gives some agent a cost of at least $44/43$ of its share (theorem).

## Tightness

- **Two agents.** MMS allocations always exist for $n = 2$. Agent 1 splits the goods into two bundles, each worth at least $\mathrm{MMS}_1$ to it, and agent 2 takes the bundle it prefers. By additivity, agent 2 values that bundle at least half of the total, which is at least $\mathrm{MMS}_2$; this is [divide and choose](/divide-and-choose/) for goods. More generally, an MMS allocation exists whenever all agents, or all agents but one, have the same valuation, by the same argument (Feige, Sapir and Tauber, Proposition 7).
- **Nine goods is the minimum.** Every instance with $n$ agents and at most $n + 5$ goods has an MMS allocation (Feige, Sapir and Tauber, Theorem 2), so with three agents a counterexample needs at least nine goods.
- **The gap $1/40$ is the largest with three agents and nine goods.** Every such instance has an allocation that gives each agent at least $39/40$ of its share (Feige, Sapir and Tauber, Theorem 3). The proof reduces the instances to finitely many classes and solves a linear program for each class with a standard solver.
- **Four agents.** Part 2 gives only $1 - 1/4^4$ for $n = 4$. A preprint gives four agents and eleven goods where no allocation is better than $20/21$-MMS (Ezra and Garbuz, arXiv:2609.15085, September 2026, preprint).

## History

Budish (2011) defined the maximin share guarantee for the allocation of indivisible goods. Kurokawa, Procaccia and Wang proved that MMS allocations need not exist and that $2/3$-MMS allocations always exist; the journal version appeared in the Journal of the ACM in 2018. Feige, Sapir and Tauber (WINE 2021) found the instance with three agents and nine goods, showed that no smaller counterexample exists, and gave the examples for every $n \ge 4$.

## References
