---
tag: 7JFD40
kind: theorem
slug: unreasonable-fairness-of-mnw
name: Unreasonable fairness of maximum Nash welfare
aliases:
- Caragiannis et al. theorem on MNW
area: algorithmic-game-theory/fair-division
level: advanced
summary: With additive values, every allocation of maximum Nash welfare is EF1 and Pareto optimal. If no allocation has positive welfare, the rule first maximizes the set of agents with positive value.
prereqs: [maximum-nash-welfare, envy-freeness-up-to-one-good, pareto-optimality]
see_also: [maximin-share, ef1-and-pareto-optimal-algorithm, envy-freeness-up-to-any-good, indivisible-goods-allocation, competitive-equilibrium-from-equal-incomes, nash-bargaining-solution, eisenberg-gale-program]
sources:
  - paper: doi:10.1145/3355902
    title: "Ioannis Caragiannis, David Kurokawa, Herve Moulin, Ariel D. Procaccia, Nisarg Shah and Junxing Wang, The unreasonable fairness of maximum Nash welfare, ACM Transactions on Economics and Computation 7(3) (2019), article 12 (conference version EC 2016)"
    locator: Definition 3.1 and Algorithm 1 (the MNW rule), Theorem 3.2 and its proof, Theorems 3.3 and 3.5, Theorem 4.1, Corollary 4.5, Example C.3 and Section 1.1 (Spliddit)
  - paper: "Siddharth Barman, Sanath Kumar Krishnamurthy and Rohit Vaish, Finding fair and efficient allocations, Proceedings of the 19th ACM Conference on Economics and Computation (EC 2018), 557-574 (arXiv:1707.04731)"
    locator: Theorem 1 (EF1 and Pareto optimal allocations in pseudo-polynomial time)
  - paper: "Ryoga Mahara, A polynomial-time algorithm for fair and efficient allocation with a fixed number of agents, arXiv:2411.01810 (November 2024)"
    locator: abstract (the open problem, and an EF1 and fPO algorithm for a fixed number of agents)
---

The unreasonable fairness of maximum Nash welfare is the theorem of Caragiannis, Kurokawa, Moulin, Procaccia, Shah and Wang that every allocation of indivisible goods that maximizes the product of the agents' additive values is both [envy-free up to one good](/envy-freeness-up-to-one-good/) (EF1) and [Pareto optimal](/pareto-optimality/) (PO). This page is about that fairness theorem and its proof. The page on [maximum Nash welfare](/maximum-nash-welfare/) treats the optimization problem itself: its definition, its NP-hardness and the algorithms that compute or approximate it. The theorem is called "unreasonable" because the product rule was not designed for EF1, yet it gives EF1 and efficiency at once.

## Statement

Let $N = \{1, \dots, n\}$ be the agents and $M$ the goods, with additive valuations $v_i(S) = \sum_{g \in S} v_i(g)$ and $v_i(g) \ge 0$. The **MNW rule** (Caragiannis et al., Definition 3.1 and Algorithm 1) picks an allocation as follows.

- If some allocation gives every agent a positive value, pick an allocation $A$ that maximizes $\prod_{i \in N} v_i(A_i)$.
- Otherwise, let $S$ be a largest set of agents that can all get positive values in one allocation. Give the goods to the agents of $S$ only, in an allocation that maximizes $\prod_{i \in S} v_i(A_i)$.

**Theorem** (Caragiannis et al., Theorem 3.2). Every allocation chosen by the MNW rule is EF1 and Pareto optimal.

## In plain words

Pick the split of the items that makes the product of everybody's happiness as large as possible. Then two things are true. First, nobody can be made happier without someone else losing, because that change would raise the product. Second, if you envy someone, the envy goes away after one item leaves their pile. The reason is that if your envy were large, one of their items would be worth more to you, compared with what it is worth to them, than their whole pile is on average. Handing that item over would then raise the product, which is impossible. If some agents must get nothing whatever we do, the rule first gives something of value to as many agents as possible, and the same reasoning works for them.

## Proof

**Case 1: positive welfare.** Here $v_k(A_k) > 0$ for every agent $k$.

*Pareto optimality.* If an allocation $A'$ had $v_k(A'_k) \ge v_k(A_k)$ for all $k$, with strict inequality for one agent, then its product would be strictly larger, because all factors are positive. This contradicts the choice of $A$.

*EF1.* Suppose that agent $i$ envies agent $j$ beyond one good: $v_i(A_i) < v_i(A_j \setminus \{g\})$ for every $g \in A_j$. Then $A_j$ has a good that $i$ values positively, since otherwise the right side would be 0. Among the goods $g \in A_j$ with $v_i(g) > 0$, let $g^*$ be one that minimizes the ratio $v_j(g)/v_i(g)$. Move $g^*$ from $j$ to $i$; the other bundles do not change.

If $v_j(g^*) = 0$, agent $j$ loses nothing and agent $i$ gains $v_i(g^*) > 0$, so the product grows: a contradiction.

If $v_j(g^*) > 0$, write $r = v_j(g^*)/v_i(g^*)$. Every good $g \in A_j$ with $v_i(g) > 0$ has $v_j(g) \ge r\, v_i(g)$, and the other goods of $A_j$ add nothing to $v_i(A_j)$, so

$$v_j(A_j) \ge r\, v_i(A_j). \tag{1}$$

The assumption with $g = g^*$ gives

$$v_i(A_i) + v_i(g^*) < v_i(A_j). \tag{2}$$

Multiplying (2) by $r > 0$ and using (1) gives $r\,(v_i(A_i) + v_i(g^*)) < v_j(A_j)$, that is,

$$v_j(g^*)\,\big(v_i(A_i) + v_i(g^*)\big) < v_i(g^*)\, v_j(A_j).$$

The product of the two changed values after the move is

$$\big(v_i(A_i) + v_i(g^*)\big)\big(v_j(A_j) - v_j(g^*)\big) = v_i(A_i) v_j(A_j) + v_i(g^*) v_j(A_j) - v_j(g^*)\big(v_i(A_i) + v_i(g^*)\big),$$

which is strictly larger than $v_i(A_i) v_j(A_j)$ by the inequality above. Hence the Nash welfare grows: a contradiction. So $A$ is EF1. $\square$

**Case 2: zero welfare.** Let $S$ be the set chosen by the rule. Every agent outside $S$ gets no goods and has value 0.

*Pareto optimality.* Let $A'$ be at least as good as $A$ for every agent. Then all agents of $S$ have positive values in $A'$. No agent $k \notin S$ can have $v_k(A'_k) > 0$, because then $S \cup \{k\}$ could all be served, against the maximality of $S$. And no agent of $S$ can be strictly better off, because that would raise $\prod_{i \in S} v_i$, which $A$ maximizes. So nobody is strictly better off in $A'$.

*EF1 inside $S$.* For $i, j \in S$, the argument of Case 1 applies to the agents of $S$: the move of $g^*$ keeps every value in $S$ positive and raises the product over $S$.

*EF1 toward agents outside $S$.* Their bundles are empty, so nobody envies them.

*EF1 from agents outside $S$.* Let $i \notin S$ and $j \in S$, and suppose $i$ envies $j$ beyond one good. Since $v_j(A_j) > 0$, there is a good $g_j \in A_j$ with $v_j(g_j) > 0$. The assumption gives $v_i(A_j \setminus \{g_j\}) > v_i(A_i) = 0$, so some $g_i \in A_j \setminus \{g_j\}$ has $v_i(g_i) > 0$. Moving $g_i$ to $i$ gives $i$ a positive value, keeps $g_j$ with $j$, and does not touch the other agents of $S$. Then $S \cup \{i\}$ can all be served: a contradiction. $\blacksquare$

## Consequences

- **Existence.** For additive valuations, an allocation that is EF1 and PO always exists. Example C.3 of Caragiannis et al. shows that the allocations of maximum utilitarian welfare and of maximum egalitarian welfare need not be EF1, so among the three classical welfare rules only the Nash rule has this property.
- **Maximin share.** Every MNW allocation gives each agent at least $\frac{2}{1 + \sqrt{4n - 3}}$ of its [maximin share](/maximin-share/), and this factor is tight (Theorem 4.1). It is also $\Phi$-pairwise MMS for $\Phi = (\sqrt{5} - 1)/2 \approx 0.618$ (Corollary 4.5).
- **Practice.** The Spliddit website uses the MNW rule for dividing goods (Section 1.1).
- **Computation.** The theorem does not make EF1 with PO easy to compute, since MNW is NP-hard. The [Barman-Krishnamurthy-Vaish algorithm](/ef1-and-pareto-optimal-algorithm/) finds an EF1 and PO allocation in pseudo-polynomial time (theorem). Whether one can be found in polynomial time is open (open problem, as stated by Mahara, arXiv:2411.01810, November 2024); Mahara gives a polynomial algorithm for EF1 with fractional Pareto optimality when the number of agents is fixed.

## Tightness

- **Additivity.** For subadditive valuations and for supermodular valuations there are instances with no allocation that is both EF1 and PO (theorem, Theorem 3.3), so no rule can extend the result to those classes.
- **Submodular valuations.** MNW allocations need not be EF1 and PO, but they satisfy PO and a weaker notion, marginal envy-freeness up to one good, $v_i(A_i) \ge v_i(A_i \cup A_j \setminus \{g\}) - v_i(A_i)$ for some $g \in A_j$ (theorem, Theorem 3.5).
- **Not EFX.** Two agents value goods $a, b, c$ at $(1, 3, 4)$ and $(4, 3, 6)$. The unique MNW allocation gives $\{b\}$ to agent 1 and $\{a, c\}$ to agent 2, with product $3 \cdot 10 = 30$; every other allocation has product at most 28. Agent 1 values $\{a, c\}$ minus $a$ at $4 > 3$, so the allocation is EF1 but not [EFX](/envy-freeness-up-to-any-good/).
- **The rule for zero welfare.** Without it, the plain product is 0 for every allocation in an instance where some agent values nothing, and an allocation that gives all goods to one agent would also maximize it, though it is not EF1.

## History

Caragiannis, Kurokawa, Moulin, Procaccia, Shah and Wang presented the theorem at EC 2016, and the journal version appeared in 2019. They proposed the MNW rule for the goods division tool of Spliddit, where it replaced an earlier algorithm based on the maximin share.

## References
