---
tag: PZB80S
kind: definition
slug: envy-freeness-up-to-any-good
name: Envy-freeness up to any good
aliases:
- EFX
area: algorithmic-game-theory/fair-division
level: advanced
summary: Envy disappears after removing any one good from the envied bundle. EFX allocations exist for two agents and for three additive agents; for four or more additive agents it is open.
prereqs: [envy-freeness-up-to-one-good]
see_also: [efx-existence-for-three-agents, envy-freeness, indivisible-goods-allocation, envy-cycle-elimination, maximin-share, unreasonable-fairness-of-mnw, maximum-nash-welfare]
sources:
  - paper: doi:10.1145/3355902
    title: "Ioannis Caragiannis, David Kurokawa, Herve Moulin, Ariel D. Procaccia, Nisarg Shah and Junxing Wang, The unreasonable fairness of maximum Nash welfare, ACM Transactions on Economics and Computation 7(3) (2019), article 12 (conference version EC 2016)"
    locator: Definition 4.4 (EFX, for goods of positive value) and the open question on its existence
  - paper: "Benjamin Plaut and Tim Roughgarden, Almost envy-freeness with general valuations, SIAM Journal on Discrete Mathematics 34(2) (2020), 1039-1068 (conference version SODA 2018)"
    locator: the existence of EFX allocations for two agents and for identical valuations
  - paper: doi:10.1145/3616009
    title: "Bhaskar Ray Chaudhury, Jugal Garg and Kurt Mehlhorn, EFX exists for three agents, Journal of the ACM 71(1) (2024), 1-27 (conference version EC 2020; arXiv:2002.05119)"
    locator: Section 1 (definition, the example with values 1, 1 and 2, and the state of the question) and Section 2 (strong envy)
  - paper: "Bhaskar Ray Chaudhury, Telikepalli Kavitha, Kurt Mehlhorn and Alkmini Sgouritsa, A little charity guarantees almost envy-freeness, Proceedings of the 31st ACM-SIAM Symposium on Discrete Algorithms (SODA 2020), 2658-2672"
    locator: EFX with charity, with fewer than n unallocated goods that no agent envies
---

Envy-freeness up to any good (EFX) is a fairness notion for the [allocation of indivisible goods](/indivisible-goods-allocation/): if agent $i$ envies agent $j$, the envy must disappear when any single good, even the one that $i$ values least, is removed from the bundle of $j$. It is stronger than [envy-freeness up to one good](/envy-freeness-up-to-one-good/) (EF1), which removes only the best good, and weaker than [envy-freeness](/envy-freeness/). Caragiannis et al. defined it in 2016. EFX allocations are known to exist for two agents, for identical valuations and for [three agents with additive valuations](/efx-existence-for-three-agents/); for four or more agents with additive valuations, existence is an open problem.

## Definition

Let $N = \{1, \dots, n\}$ be the agents, $M$ the set of $m$ goods, $v_i$ the monotone valuation of agent $i$ with $v_i(\emptyset) = 0$, and $A = (A_1, \dots, A_n)$ an allocation of all goods. The allocation is **EFX** if

$$v_i(A_i) \ge v_i(A_j \setminus \{g\}) \quad \text{for all agents } i \ne j \text{ and every good } g \in A_j.$$

Following Chaudhury, Garg and Mehlhorn, agent $i$ *strongly envies* a bundle $S$ if $v_i(A_i) < v_i(S \setminus \{g\})$ for some $g \in S$. An allocation is EFX exactly when no agent strongly envies the bundle of another agent.

**Two versions.** Caragiannis et al. (Definition 4.4) require the inequality only for goods $g \in A_j$ with $v_i(g) > 0$. Chaudhury, Garg and Mehlhorn, and many later papers, require it for every $g \in A_j$, as above. When all values of single goods are positive, the two versions agree. The version for every good is stronger, and the existence results on this page use it unless a line says otherwise. (Some papers call the version for every good EFX$_0$.)

For additive valuations, the test for the pair $(i, j)$ uses the good of $A_j$ that $i$ values least:

$$v_i(A_i) \ge v_i(A_j) - \min_{g \in A_j} v_i(g),$$

so EFX is checked in $O(n m)$ time from the $n \times m$ table of values, the same as EF1. For a general valuation given by an oracle, the test takes at most $n m$ value queries.

## Examples and non-examples

- **EF1 but not EFX.** Two agents both value goods $g_1, g_2, g_3$ at $1, 1, 2$ (the example of Chaudhury, Kavitha, Mehlhorn and Sgouritsa). The allocation $\{g_1\}$, $\{g_2, g_3\}$ is EF1: the first agent has 1, and removing $g_3$ from the other bundle leaves 1. It is not EFX: removing $g_2$ leaves 2. The allocations that give one agent $\{g_3\}$ and the other $\{g_1, g_2\}$ are EFX, and they are the only ones: if one agent holds $g_3$ and another good, the other agent has at most 1 and values that bundle at 2 or more after the removal of the good worth 1.
- **The two versions differ.** Agent 1 values goods $a$ and $b$ at 1 and 0, agent 2 values both at 1. The allocation $A_1 = \emptyset$, $A_2 = \{a, b\}$ satisfies the version with positive goods only: the only good of $A_2$ that agent 1 values is $a$, and $v_1(\{b\}) = 0 \le 0$. It violates the version for every good, because $v_1(A_2 \setminus \{b\}) = 1 > 0$. The allocation $\{a\}$, $\{b\}$ meets both versions.
- **EFX but not envy-free.** With values $1, 1, 2$ for both agents and the bundles $\{g_3\}$ and $\{g_1, g_2\}$, both agents have 2 and value the other bundle at 2, so this one is envy-free too. Change the values to $1, 1, 3$: now the agent with $\{g_1, g_2\}$ has 2 and envies the bundle worth 3, but $\{g_3\}$ minus its only good is empty, so the allocation is still EFX.
- **Not EF1, so not EFX.** Any allocation in which some agent $i$ values $A_j$ minus its best good above $v_i(A_i)$ fails both notions.
- **Identical additive valuations.** Sort the goods by value, largest first, and give each one to a bundle of smallest current value. The result is EFX for the common valuation: when good $g$ joins bundle $B$, every good already in $B$ is worth at least $g$, and $v(B) \le v(C)$ for every other bundle $C$, so $v(B \cup \{g\}) - v(g) = v(B) \le v(C)$; bundles only grow afterwards, and the last good added to a bundle is its least valuable one. The [EFX existence for three agents](/efx-existence-for-three-agents/) page uses this step for two agents.

## Related definitions

- [Envy-freeness](/envy-freeness/) implies EFX, which implies [EF1](/envy-freeness-up-to-one-good/). Each implication is strict, by the examples above.
- **Partial EFX and EFX with charity.** An allocation of a subset of the goods that is EFX among the agents. Chaudhury, Kavitha, Mehlhorn and Sgouritsa (SODA 2020) show that for general monotone valuations there is a partial EFX allocation whose pool $P$ of unallocated goods has fewer than $n$ goods and no agent envies the pool (theorem).
- **$\alpha$-EFX.** The inequality is relaxed to $v_i(A_i) \ge \alpha\, v_i(A_j \setminus \{g\})$ for a factor $\alpha \le 1$.
- [Maximin share](/maximin-share/): a threshold notion that does not compare bundles. Like EFX, MMS allocations need not be easy to find, but unlike EFX it is known that they may fail to exist.
- [Maximum Nash welfare](/maximum-nash-welfare/) allocations are EF1 and Pareto optimal for additive valuations, but EFX is a different requirement.

**State of the existence question.** These results are for the version for every good unless a line says otherwise.

- Two agents with monotone valuations, and any number of agents with identical monotone valuations: EFX allocations exist (theorem, Plaut and Roughgarden 2020).
- Three agents with additive valuations: EFX allocations exist (theorem, [Chaudhury, Garg and Mehlhorn](/efx-existence-for-three-agents/), JACM 2024).
- Four or more agents with additive valuations: open. The question was posed by Caragiannis et al. (EC 2016) and is still open in the 2026 sources listed here. Partial results: with four additive agents, there is an EFX allocation that leaves at most one good unallocated (Berger, Cohen, Feldman and Fiat, AAAI 2022, theorem); and with four additive agents and at most nine goods, an EFX allocation exists by a computer-assisted proof (Alkassar, Fouz and Mehlhorn, arXiv:2608.08590, 2026, preprint).
- Beyond additive valuations: a preprint gives three agents with submodular (weighted coverage) valuations and eight goods with no EFX allocation ("EFX Need Not Exist", arXiv:2604.18216, first version April 2026, preprint). For chores with additive costs, a preprint shows that EFX can fail for four or more agents (arXiv:2606.08872, June 2026, preprint).

## References
