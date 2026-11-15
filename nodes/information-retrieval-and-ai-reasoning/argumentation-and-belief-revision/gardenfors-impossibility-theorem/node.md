---
tag: 95APNV
kind: theorem
slug: gardenfors-impossibility-theorem
name: Gardenfors impossibility theorem
aliases:
- Ramsey test impossibility
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: No nontrivial belief revision system satisfies both the AGM preservation postulate and the Ramsey test for conditionals.
prereqs: [agm-postulates]
see_also: [belief-revision, belief-update, grove-spheres, katsuno-mendelzon-revision, nonmonotonic-reasoning, knaster-tarski-theorem]
sources:
  - paper: doi:10.2307/2185133
    title: Peter Gärdenfors, Belief revisions and the Ramsey test for conditionals, The Philosophical Review 95(1), starting p. 81 (1986)
    locator: the whole paper (the impossibility theorem and its proof)
  - paper: "Peter Gärdenfors, Belief revision: an introduction, in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)"
    locator: Section 4.6 (the Ramsey test, Theorem 14 and its Corollary, with footnote 11 on the domain of belief sets)
  - book: isbn:9780262071093
    title: "Peter Gärdenfors, Knowledge in Flux: Modeling the Dynamics of Epistemic States, MIT Press (1988)"
    locator: the chapters on conditionals and the Ramsey test
---

The Ramsey test says that you accept "if $p$ then $q$" exactly when you would accept $q$ after revising your beliefs by $p$. It is an attractive bridge between conditionals and [belief revision](/belief-revision/). Peter Gärdenfors proved in 1986 that the bridge cannot carry the conditionals into the belief sets themselves: no belief revision system that is not trivial can satisfy the Ramsey test together with the preservation principle, a weak form of the [AGM postulate](/agm-postulates/) K*4, and two mild conditions. The reason is that the Ramsey test makes revision monotone in the belief set, and preservation then forces some consistent belief set to become inconsistent.

## Statement

**Setting.** The language contains classical propositional logic and is closed under a conditional connective $>$, so $p > q$ is a sentence. A belief revision system is a pair $(\mathcal{K}, *)$, where $\mathcal{K}$ is a set of belief sets and $*$ maps each $K \in \mathcal{K}$ and each sentence $p$ to a belief set $K * p \in \mathcal{K}$. The set $\mathcal{K}$ is closed under expansion: if $K \in \mathcal{K}$ then $K + p \in \mathcal{K}$ (Gärdenfors 1992, footnote 11). $K_\bot$ is the inconsistent belief set.

**Conditions.**

| | name | condition |
|---|---|---|
| K*2 | success | $p \in K * p$ |
| K*5w | weak consistency | if $K \ne K_\bot$ and $K * p = K_\bot$, then $\vdash \neg p$ |
| K*P | preservation | if $\neg p \notin K$ and $q \in K$, then $q \in K * p$ |
| K*M | monotonicity | if $K \subseteq K'$, then $K * p \subseteq K' * p$ |
| RT | Ramsey test | $(p > q) \in K$ if and only if $q \in K * p$ |

**Non-triviality.** The system is non-trivial when there are three sentences $A$, $B$, $C$ that are pairwise disjoint, that is $\vdash \neg(A \wedge B)$, $\vdash \neg(A \wedge C)$ and $\vdash \neg(B \wedge C)$, and a belief set $K \in \mathcal{K}$ that is consistent with each of them: $\neg A \notin K$, $\neg B \notin K$ and $\neg C \notin K$.

**Theorem** (Gärdenfors 1986; Gärdenfors 1992, Theorem 14). There is no non-trivial belief revision system that satisfies K*2, K*5w, K*M and K*P.

**Corollary.** There is no non-trivial belief revision system that satisfies K*2, K*5w, K*P and RT.

## In plain words

Suppose you know that exactly one of three things is the case, but not which one. The Ramsey test says that your conditional beliefs are part of your beliefs. If you know more, you then also hold more conditionals, and so after any revision you believe at least as much as someone who knows less. Preservation says that if new information fits your beliefs, you keep all of them. Now take a person who knows that the first thing is the case. Compare two people who know less: one knows "first or second", the other "first or third". Tell all three "second or third". The first of the two less informed people ends up believing "second", the other ends up believing "third". The best informed person must believe at least as much as each of them, so both, which is impossible.

## Proof

*The corollary from the theorem.* RT implies K*M: if $K \subseteq K'$ and $q \in K * p$, then $p > q \in K$ by RT, so $p > q \in K'$, and $q \in K' * p$ by RT again. So a system with RT has K*M, and the theorem applies.

*The theorem.* Let $A$, $B$, $C$ and $K$ witness non-triviality, and suppose the system satisfies K*2, K*5w, K*M and K*P. Let

$$H_1 = K + (A \vee B), \qquad H_2 = K + (A \vee C), \qquad H_3 = K + A.$$

All three are in $\mathcal{K}$, by closure under expansion. $H_3$ is consistent, since $\neg A \notin K$. Since $A$ implies $A \vee B$ and $A \vee C$, we have $H_1 \subseteq H_3$ and $H_2 \subseteq H_3$.

Revise each by $B \vee C$.

1. $\neg(B \vee C) \notin H_1$. Indeed $(A \vee B) \wedge (B \vee C)$ is equivalent to $B \vee (A \wedge C)$, which is equivalent to $B$ because $A \wedge C$ is inconsistent. So $H_1 + (B \vee C) = K + B$, which is consistent since $\neg B \notin K$.
2. By K*P, $A \vee B \in H_1 * (B \vee C)$, and by K*2, $B \vee C \in H_1 * (B \vee C)$. Together they imply $B$, and $H_1 * (B \vee C)$ is a belief set, so $B \in H_1 * (B \vee C)$.
3. In the same way, $C \in H_2 * (B \vee C)$.
4. By K*M, $H_1 * (B \vee C) \subseteq H_3 * (B \vee C)$ and $H_2 * (B \vee C) \subseteq H_3 * (B \vee C)$. So $B$ and $C$ are both in $H_3 * (B \vee C)$. Since $\vdash \neg(B \wedge C)$, $H_3 * (B \vee C) = K_\bot$.
5. $H_3$ is consistent and $B \vee C$ is consistent (it follows from $B$, which is consistent with $K$), so K*5w says $H_3 * (B \vee C) \ne K_\bot$. This is a contradiction. $\square$

*A check by brute force.* Without conditionals, the theorem is about K*2, K*5w, K*M and K*P alone, and on a finite language it can be tested. Represent each belief set and each sentence by its set of models. For each pair $(K, p)$ start with the largest allowed result $U(K, p) = \mathrm{Mod}(p)$, or $\mathrm{Mod}(K) \cap \mathrm{Mod}(p)$ when that is nonempty (by K*2 and K*P). Then repeat until nothing changes: for $K \subseteq K'$, shrink $U(K', p)$ to $U(K', p) \cap U(K, p)$, as K*M demands. This is a greatest fixed point in the sense of the [Knaster and Tarski theorem](/knaster-tarski-theorem/), and every system with the four conditions has $\mathrm{Mod}(K * p) \subseteq U(K, p)$. Over two atoms, 22 pairs of a consistent $K$ and a consistent $p$ end with $U(K, p) = \emptyset$, so K*5w cannot hold. One of them is the pair of the proof with $A = \neg a \wedge \neg b$, $B = \neg a \wedge b$, $C = a \wedge \neg b$, $K = \mathrm{Cn}(\emptyset)$: here $H_3 = \mathrm{Cn}(\neg a \wedge \neg b)$ and $p = B \vee C$, which says that exactly one of $a$ and $b$ is true.

## Consequences

- **Conditionals cannot be ordinary beliefs if revision preserves.** Since the AGM postulate K*4 implies K*P, no AGM revision on a language with Ramsey-test conditionals in the belief sets is non-trivial. Something must give: the Ramsey test, preservation, or the idea that conditionals are in the belief sets.
- **K*4 in place of K*P.** If K*P is replaced by K*4, the proof goes through without K*2: K*4 gives $H_1 + (B \vee C) \subseteq H_1 * (B \vee C)$ directly, and $B$ is in it.
- **Ways out.** Isaac Levi keeps conditionals out of the belief sets, so RT is a rule for evaluating them, not a condition on $\mathcal{K}$. Others keep RT and drop preservation: an [update](/belief-update/) changes each possible world on its own and is monotone in the belief set, as in the work of Morreau and of Katsuno and Mendelzon on update. Cross and Thomason change the underlying logic to a four-valued one.
- **Monotonicity is the culprit.** The proof uses K*M only for $H_1 \subseteq H_3$ and $H_2 \subseteq H_3$. A revision that satisfies the [Katsuno and Mendelzon](/katsuno-mendelzon-revision/) postulates is generally not monotone in $K$. In the two-atom example, Dalal's operator gives $H_1 * (B \vee C) = \mathrm{Cn}(B)$, because $H_1$ is consistent with $B \vee C$. But $H_3 * (B \vee C) = \mathrm{Cn}(B \vee C)$, because both models of $B \vee C$ differ from the one model of $H_3$ in one atom. So $H_1 \subseteq H_3$ while $H_1 * (B \vee C) \not\subseteq H_3 * (B \vee C)$.

## Tightness

- **Non-triviality is needed.** With one atom there are only two worlds, so there are no three pairwise disjoint consistent sentences. The fixed-point computation above then leaves every $U(K, p)$ nonempty for consistent $K$ and $p$, and choosing $\mathrm{Mod}(K * p) = U(K, p)$ gives a system with K*2, K*5w, K*M and K*P.
- **Each condition is used.** Without K*5w the inconsistent result is allowed. Without K*P (or K*4) there is no reason for $B$ to enter $H_1 * (B \vee C)$: the revision $K * p = \mathrm{Cn}(p)$ satisfies K*2, K*5w and K*M. Without K*M the three revisions are independent, and an AGM revision such as full meet revision satisfies the other three conditions.
- **The domain matters.** The proof needs $K + A$, $K + (A \vee B)$ and $K + (A \vee C)$ in $\mathcal{K}$. On a domain that is not closed under expansion the argument does not start.

## History

Frank Ramsey suggested in 1929 that one evaluates "if $p$ then $q$" by adding $p$ to one's stock of beliefs. Robert Stalnaker and others developed the idea, and Gärdenfors built a theory of conditionals on it within his study of epistemic states. In 1986 he showed that the Ramsey test and preservation clash, in a short paper in The Philosophical Review. The result started a long discussion on the status of conditionals in belief revision, and it was one reason to separate revision from update.

## References
