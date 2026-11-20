---
tag: BYDJ2X
kind: theorem
slug: deferred-acceptance-strategyproofness
name: Strategyproofness of deferred acceptance
aliases:
- Dubins-Freedman theorem
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: In deferred acceptance, truth is a dominant strategy for every proposer, and no coalition of proposers can make all its members strictly better off (Dubins and Freedman 1981).
prereqs: [gale-shapley, stable-matching, dominant-strategy-incentive-compatibility]
see_also: [roth-impossibility-theorem, lattice-of-stable-matchings, school-choice-problem, boston-mechanism, hospitals-residents-problem, top-trading-cycles, gibbard-satterthwaite-theorem, revelation-principle]
sources:
  - paper: doi:10.1080/00029890.1981.11995301
    title: Lester E. Dubins and David A. Freedman, Machiavelli and the Gale-Shapley algorithm, American Mathematical Monthly 88(7), 485 to 494 (1981)
    locator: the whole paper (the theorem for single men and for coalitions of men)
  - paper: doi:10.1287/moor.7.4.617
    title: Alvin E. Roth, The economics of matching, stability and incentives, Mathematics of Operations Research 7(4), 617 to 628 (1982)
    locator: the whole paper (the man-proposing mechanism is strategyproof for men, and no stable mechanism is strategyproof for all agents)
  - paper: doi:10.1016/0166-218X(85)90074-5
    title: David Gale and Marilda Sotomayor, Some remarks on the stable matching problem, Discrete Applied Mathematics 11(3), 223 to 232 (1985)
    locator: the whole paper (the blocking lemma and a short proof of the Dubins-Freedman theorem)
  - book: isbn:9780521437882
    title: Alvin E. Roth and Marilda A. Oliveira Sotomayor, Two-Sided Matching, a Study in Game-Theoretic Modeling and Analysis, Cambridge University Press (1990)
    locator: the chapter on strategic questions in the marriage model
---

The theorem says that the side that proposes in the [deferred acceptance](/gale-shapley/) algorithm cannot gain by lying: for each proposer, reporting the true preference list is a dominant strategy, and a group of proposers cannot lie together so that each of them ends strictly better off. It is a statement about one side only. The [impossibility theorem of Roth](/roth-impossibility-theorem/) shows that the receiving side can gain, and that no stable mechanism removes the incentive to lie for both sides. The theorem is the reason why school districts use student-proposing deferred acceptance instead of the [Boston mechanism](/boston-mechanism/).

## Statement

A marriage market has a set $M$ of men and a set $W$ of women. Each man has a strict order over $W \cup \{\text{single}\}$ and each woman a strict order over $M \cup \{\text{single}\}$; a partner below "single" is unacceptable. A preference profile $P$ lists all these orders. A matching is *stable* for $P$ when every agent finds the partner acceptable and no man and woman both prefer each other to their partners. For a profile $P$, let $\mu_M(P)$ be the matching that the man-proposing deferred acceptance algorithm outputs on $P$; it is the man-optimal stable matching for $P$. The *man-proposing mechanism* asks every agent for an order and outputs $\mu_M$ of the reports.

**Theorem (Dubins and Freedman 1981).** Let $P$ be the true profile, let $C \subseteq M$ be a nonempty set of men, and let $P'$ be a profile that differs from $P$ only in the orders of the men of $C$. Then some man $m \in C$ does not strictly prefer $\mu_M(P')(m)$ to $\mu_M(P)(m)$ under his true order.

**Corollary (Dubins and Freedman 1981; Roth 1982).** In the man-proposing mechanism, truthful reporting is a dominant strategy for every man: whatever the others report, no false order gives him a partner he truly prefers.

The corollary is the case $C = \{m\}$, applied to the profile in which the other agents' orders are their reports.

## In plain words

Each person on the proposing side asks partners in order, starting with the one they like most. Lying can only change the order in which you ask. If you skip someone you like more, you may lose a chance you would have had. If you ask someone you like less first, you can only end up with someone you like less. So telling the truth is always at least as good as any lie, whatever the others do. The same holds for a group that lies together: at least one member of the group does not gain. The other side, the side that receives proposals, has no such protection. A person who receives proposals can sometimes gain by saying no to a partner she actually would accept.

## Proof

The proof is the one of Gale and Sotomayor (1985). It rests on one lemma about the man-optimal stable matching.

**Blocking lemma.** Let $\mu_M = \mu_M(P)$, and let $\mu$ be a matching in which every agent finds the partner acceptable under $P$. Let $M' = \{m \in M : \mu(m) \succ_m \mu_M(m)\}$. If $M'$ is not empty, there is a pair $(m, w)$ that blocks $\mu$ under $P$ with $m \notin M'$ and $w \in \mu(M')$.

*Proof of the lemma.* Every $m \in M'$ prefers $\mu(m)$ to $\mu_M(m)$, and $\mu_M(m)$ is at least as good as single for him, so $\mu(m)$ is a woman. Let $W' = \mu(M')$.

*Case 1: $\mu_M(M') \ne W'$.* Then some $w \in W'$ is not in $\mu_M(M')$; let $w = \mu(m')$ with $m' \in M'$. As $m'$ prefers $w$ to $\mu_M(m')$ and $\mu_M$ is stable, $w$ prefers $\mu_M(w)$ to $m'$. Since $w$ finds $m'$ acceptable under $P$ (because $\mu$ is individually rational), $\mu_M(w)$ is a man $m$, and $m \notin M'$ because $w \notin \mu_M(M')$. As $m \notin M'$ and $\mu(m) \ne w$ (because $\mu(w) = m'$), $m$ prefers $w = \mu_M(m)$ to $\mu(m)$. So $(m, w)$ blocks $\mu$.

*Case 2: $\mu_M(M') = W'$.* Consider a run of deferred acceptance on $P$ in which the men propose one at a time; it outputs $\mu_M$. Each $m \in M'$ proposes to $\mu(m)$ before $\mu_M(m)$, so $\mu(m)$ rejects him at some point. Let $m_0 \in M'$ be the man of $M'$ who makes his last proposal latest, to $w_0 = \mu_M(m_0)$, and let $m_1 = \mu(w_0) \in M'$; then $m_1 \ne m_0$, because $\mu(m_0) \ne \mu_M(m_0)$. The man $m_1$ proposed to $w_0$ and was rejected before his own last proposal, so before $m_0$ proposes to $w_0$. A woman who has rejected someone always holds a proposal, so when $m_0$ proposes, $w_0$ holds some man $m$, and she rejects him for $m_0$. Then $m \notin M'$, because a man of $M'$ rejected at that time would propose again later than $m_0$'s last proposal. The man $w_0$ holds only gets better for her, so $w_0$ prefers $m$ to $m_1$. The man $m$ proposed to $w_0$ before $\mu_M(m)$, so he prefers $w_0$ to $\mu_M(m)$, and as $m \notin M'$, he weakly prefers $\mu_M(m)$ to $\mu(m)$. So $(m, w_0)$ blocks $\mu$, and $w_0 \in W'$. $\square$

*Proof of the theorem.* Suppose that every man of $C$ strictly prefers $\mu' = \mu_M(P')$ to $\mu_M(P)$ under $P$. The matching $\mu'$ is stable for $P'$. It is individually rational for $P$: the agents outside $C$ have the same orders in $P$ and $P'$, and each $m \in C$ prefers $\mu'(m)$ to $\mu_M(P)(m)$, which is acceptable to him. Apply the blocking lemma to $\mu'$ and $P$. The set $M'$ contains $C$, so it is not empty, and the lemma gives a pair $(m, w)$ that blocks $\mu'$ under $P$ with $m \notin M'$, so $m \notin C$. The orders of $m$ and of $w$ are the same in $P$ and $P'$, so $(m, w)$ also blocks $\mu'$ under $P'$. This contradicts the stability of $\mu'$ for $P'$. $\blacksquare$

## Consequences

- **School choice and residency matching.** With student-proposing (or doctor-proposing) deferred acceptance, students and doctors can report their true lists safely. This is the main reason why Boston and New York City adopted it for school assignment (see [school choice problem](/school-choice-problem/)).
- **Many-to-one markets.** In the [hospitals-residents problem](/hospitals-residents-problem/), resident-proposing deferred acceptance is strategyproof for residents, by the same proof applied to the related marriage market in which each hospital is split into one copy per seat.
- **Weak Pareto optimality.** No individually rational matching is strictly better than $\mu_M$ for every man (Roth 1982). With $M' = M$, the blocking lemma would give a blocking man outside $M$, which cannot exist.
- **Revelation.** Since truth is dominant for men, any equilibrium analysis of the mechanism can assume truthful men and study only the strategies of the women.

## Tightness

- **The receiving side can gain.** Take two men and two women with $m_1$: $w_1, w_2$; $m_2$: $w_2, w_1$; $w_1$: $m_2, m_1$; $w_2$: $m_1, m_2$. Truthful man-proposing deferred acceptance gives $m_1 w_1$, $m_2 w_2$. If $w_1$ reports that only $m_2$ is acceptable, the algorithm gives $m_1 w_2$, $m_2 w_1$, so $w_1$ gets her first choice. See [Roth's impossibility theorem](/roth-impossibility-theorem/).
- **A coalition can gain weakly.** The theorem does not exclude that some members gain while the others stay the same. Take three men and three women with $m_1$: $w_3, w_2, w_1$; $m_2$: $w_3, w_2, w_1$; $m_3$: $w_2, w_3, w_1$; $w_1$: $m_2, m_3, m_1$; $w_2$: $m_1, m_2, m_3$; $w_3$: $m_3, m_1, m_2$. The truthful outcome is $m_1 w_2$, $m_2 w_1$, $m_3 w_3$. If $m_2$ alone ranks $w_1$ first, the outcome is $m_1 w_3$, $m_2 w_1$, $m_3 w_2$: $m_2$ keeps $w_1$, and $m_1$ and $m_3$ get their first choices. So the mechanism is not strongly group strategyproof for men.
- **Strategyproofness costs efficiency.** Student-proposing deferred acceptance can be Pareto dominated for the students by an unstable matching; see the second example of the [school choice problem](/school-choice-problem/). Top trading cycles is strategyproof and efficient, but not stable.
- **Short lists.** If an agent may list only $k$ partners, truthful reporting of the top $k$ is no longer dominant.

## History

Gale and Shapley (1962) gave the deferred acceptance algorithm. Roth (1982) proved that the man-proposing mechanism makes truth a dominant strategy for men, and that no stable mechanism does so for all agents. Dubins and Freedman (1981) proved the stronger statement for coalitions of men, with a combinatorial argument on the run of the algorithm. Gale and Sotomayor (1985) gave the short proof through the blocking lemma, which is the proof above.

## References
