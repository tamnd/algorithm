---
tag: JDM3S7
kind: theorem
slug: efx-existence-for-three-agents
name: EFX existence for three agents
aliases:
- Chaudhury-Garg-Mehlhorn theorem
area: algorithmic-game-theory/fair-division
level: research
summary: Every instance with three agents and additive valuations has an allocation that is envy-free up to any good.
prereqs: [envy-freeness-up-to-any-good, envy-cycle-elimination]
see_also: [indivisible-goods-allocation, envy-freeness-up-to-one-good, divide-and-choose, pareto-optimality, maximum-nash-welfare, unreasonable-fairness-of-mnw, maximin-share, mms-nonexistence-theorem]
sources:
  - paper: doi:10.1145/3616009
    title: "Bhaskar Ray Chaudhury, Jugal Garg and Kurt Mehlhorn, EFX exists for three agents, Journal of the ACM 71(1) (2024), 1-27 (conference version EC 2020; arXiv:2002.05119)"
    locator: "Section 2 (Lemma 1 on non-degenerate instances, the potential, most envious agents and champions, Observation 3, Fact 5, Observation 6 and Corollary 7), Sections 3 and 4 (Lemmas 15 and 19), Theorem 20, and Section 5 (Theorems 21 and 24, Conjecture 23); numbers as in arXiv:2002.05119v3"
  - paper: "Benjamin Plaut and Tim Roughgarden, Almost envy-freeness with general valuations, SIAM Journal on Discrete Mathematics 34(2) (2020), 1039-1068 (conference version SODA 2018)"
    locator: the existence of EFX allocations for two agents and for identical valuations
  - paper: "Bhaskar Ray Chaudhury, Telikepalli Kavitha, Kurt Mehlhorn and Alkmini Sgouritsa, A little charity guarantees almost envy-freeness, Proceedings of the 31st ACM-SIAM Symposium on Discrete Algorithms (SODA 2020), 2658-2672"
    locator: the most envious agent and the update rule cited as Observation 6 by Chaudhury, Garg and Mehlhorn
  - paper: "Richard J. Lipton, Evangelos Markakis, Elchanan Mossel and Amin Saberi, On approximately fair allocations of indivisible goods, Proceedings of the 5th ACM Conference on Electronic Commerce (EC 2004), 125-131"
    locator: the envy graph and the rotation of envy cycles (cited as Fact 5 by Chaudhury, Garg and Mehlhorn)
  - paper: "Ioannis Caragiannis, Nick Gravin and Xin Huang, Envy-freeness up to any item with high Nash welfare: the virtue of donating items, Proceedings of the 20th ACM Conference on Economics and Computation (EC 2019), 527-545"
    locator: partial EFX allocations with half of the maximum Nash welfare, and the conjecture on adding a good
  - paper: doi:10.1145/3355902
    title: "Ioannis Caragiannis, David Kurokawa, Herve Moulin, Ariel D. Procaccia, Nisarg Shah and Junxing Wang, The unreasonable fairness of maximum Nash welfare, ACM Transactions on Economics and Computation 7(3) (2019), article 12 (conference version EC 2016)"
    locator: Definition 4.4 (EFX) and the open question on its existence
---

The EFX existence theorem for three agents, by Chaudhury, Garg and Mehlhorn, states that three agents with additive valuations can always share a set of indivisible goods so that the allocation is [envy-free up to any good](/envy-freeness-up-to-any-good/) (EFX). Before it, existence was known only for two agents and for agents with identical valuations. The proof is an algorithm that improves a partial EFX allocation step by step. Its main new tool is a lexicographic potential, which lets the algorithm make one fixed agent better off when no [Pareto](/pareto-optimality/) improvement exists. For four or more agents with additive valuations, the question is an open problem in the 2026 sources cited on the EFX page.

## Statement

**Theorem (Chaudhury, Garg and Mehlhorn, Theorem 20).** Let three agents have additive valuations $v_1, v_2, v_3$ with $v_i(g) \ge 0$ on a finite set $M$ of goods. Then there is an allocation $X = (X_1, X_2, X_3)$ of all goods with

$$v_i(X_i) \ge v_i(X_j \setminus \{g\}) \quad \text{for all } i \ne j \text{ and every } g \in X_j.$$

This is the stronger version of EFX, in which goods of value zero also count.

## In plain words

Three people split a pile of items that cannot be cut, and each person adds up their own values. The theorem says that there is always a split in which nobody is jealous of another person's pile once any single item is taken out of that pile, even the item the jealous person cares least about.

The proof starts with nobody holding anything and hands out items one at a time. Sometimes it must take items back and swap half-piles between people to keep the rule. To show that this ends, it ranks the splits: first by how happy one chosen person is, then the second, then the third. Every step moves to a split with a higher rank, so the process cannot run forever.

## Proof

The proof for two agents is short and complete. The proof for three agents is long, and this section gives its structure.

**Two agents.** Agent 1 sorts the goods by its own value, largest first, and puts each good into the bundle of smaller current value for $v_1$. When good $g$ joins bundle $B$, every good already in $B$ is worth at least $g$ to agent 1, and $v_1(B) \le v_1(C)$ for the other bundle $C$. So $v_1(B \cup \{g\}) - v_1(g) \le v_1(C)$, and since $C$ only grows later and the last good of a bundle is its least valuable one, the final bundles satisfy $v_1(B) \ge v_1(C \setminus \{h\})$ and $v_1(C) \ge v_1(B \setminus \{h\})$ for every good $h$ of the other bundle. Agent 2 takes the bundle it prefers, as in [divide and choose](/divide-and-choose/), and agent 1 takes the other. Agent 2 envies nobody, and agent 1 meets EFX with either bundle. $\square$

**Three agents.** The steps below follow Sections 2 to 4 of Chaudhury, Garg and Mehlhorn.

1. **No ties.** Number the goods $g_1, \dots, g_m$ and set $v'_i(g_j) = v_i(g_j) + \varepsilon 2^j$, with $\varepsilon\, 2^{m+1}$ smaller than every nonzero difference $|v_i(S) - v_i(T)|$. Then every strict preference of $v_i$ stays strict under $v'_i$, no agent values two different sets the same, and an EFX allocation for $v'$ is EFX for $v$ (Lemma 1). From here on every agent values every good positively and has no ties.
2. **A potential.** Name the agents $a, b, c$ and compare partial allocations by the triple $\varphi(X) = (v_a(X_a), v_b(X_b), v_c(X_c))$ in lexicographic order. Start from the empty allocation, which is EFX. The goal is: for every partial EFX allocation $X$ and every unallocated good $g$, find a partial EFX allocation $Y$ with $\varphi(Y) > \varphi(X)$. There are finitely many allocations, so the process ends, and it can end only when every good is allocated.
3. **Acyclic envy graph.** In the [envy graph](/envy-cycle-elimination/) $E_X$, an edge $i \to j$ means that $i$ envies $j$. Rotating the bundles along a cycle keeps EFX and makes every agent on the cycle better off (Fact 5, after Lipton et al.), so $E_X$ can be taken acyclic.
4. **Champions.** For a set $S$ that agent $i$ envies, let $\kappa_X(i, S)$ be the size of a smallest subset of $S$ that $i$ still envies. Agent $i$ *champions* $j$ if $i$ envies $X_j \cup \{g\}$ and has the smallest $\kappa_X(i, X_j \cup \{g\})$ among the agents. Every bundle $X_j \cup \{g\}$ has a champion, since $j$ itself envies it, so the champion graph $M_X$ has an incoming edge at every agent and contains a [cycle](/cycle-detection/) (Observation 3).
5. **Easy cases.** If $i$ champions $s$ and $i$ is reachable from $s$ in $E_X$, each agent on the path from $s$ to $i$ takes the bundle it envies, $i$ takes a smallest subset of $X_s \cup \{g\}$ that it envies, and the other goods return to the pool. Nobody strongly envies the new bundle of $i$, because $i$ is a most envious agent, and the result is an EFX allocation that Pareto dominates $X$ (Observation 6, from Chaudhury, Kavitha, Mehlhorn and Sgouritsa). This settles the cases where $E_X$ has a single source, since then every agent is reachable from it, and where some agent champions itself (Corollary 7).
6. **Hard cases.** What remains is an acyclic $E_X$ with two or three sources and no self-champion. Here each bundle $X_j \cup \{g\}$ is split into an upper half and a lower half, defined by the smallest subset that the champion of $j$ envies, and the halves are moved between agents. With three sources, this always gives a Pareto improvement (Lemma 15). With two sources, there is a configuration where no Pareto improvement exists; the case analysis then makes agent $a$ strictly better off, which raises $\varphi$ even if another agent loses (Lemma 19).

Steps 5 and 6 cover every partial EFX allocation that is not complete, so step 2 gives a complete EFX allocation (Theorem 20). $\blacksquare$

## Consequences

- **EFX for three additive agents** (theorem). The question of Caragiannis et al. (EC 2016) is settled for $n = 3$. The proof is constructive, but the potential argument shows only that the process is finite; it gives no polynomial bound on the number of steps.
- **Pareto improvements are not enough.** Chaudhury, Garg and Mehlhorn (Theorem 21) give three agents and seven goods with a partial EFX allocation of the first six goods that no complete EFX allocation Pareto dominates. So methods that only make Pareto improvements, such as those of Plaut and Roughgarden and of Chaudhury et al. (SODA 2020), cannot always reach a complete allocation; this is why step 2 uses a lexicographic potential.
- **A conjecture fails.** Caragiannis, Gravin and Huang (EC 2019) showed that some partial EFX allocation has at least half of the [maximum Nash welfare](/maximum-nash-welfare/), and they conjectured that adding a good to an instance with an EFX allocation gives an instance with an EFX allocation of at least the same Nash welfare. Chaudhury, Garg and Mehlhorn (Theorem 24 and Conjecture 23) give three agents and seven goods where a partial EFX allocation has higher Nash welfare than every complete EFX allocation, so the conjecture is false (theorem).
- **More agents.** For four or more additive agents, existence is an open problem; the partial results, with dates, are on the [EFX](/envy-freeness-up-to-any-good/) page.

## Tightness

- **Additivity matters.** For two agents, EFX allocations exist for all monotone valuations (Plaut and Roughgarden), but the three-agent theorem is proved for additive valuations only. A preprint gives three agents with submodular valuations and eight goods with no EFX allocation ("EFX Need Not Exist", arXiv:2604.18216, first version April 2026, preprint). If it is correct, the theorem cannot be extended to all monotone valuations.
- **Not with efficiency for free.** The theorem gives no Pareto optimality and no Nash welfare bound, and the instance of Theorem 24 shows that the complete EFX allocations can all have lower Nash welfare than a partial one. For EF1, by contrast, [maximum Nash welfare](/unreasonable-fairness-of-mnw/) gives fairness and Pareto optimality together.

## History

Caragiannis, Kurokawa, Moulin, Procaccia, Shah and Wang defined EFX at EC 2016 and asked whether EFX allocations always exist. Plaut and Roughgarden (SODA 2018) proved existence for two agents and for identical valuations. Chaudhury, Kavitha, Mehlhorn and Sgouritsa (SODA 2020) proved that a partial EFX allocation with a small pool of unallocated goods always exists, using most envious agents. Chaudhury, Garg and Mehlhorn proved the three-agent case at EC 2020, and the journal version appeared in the Journal of the ACM in 2024.

## References
