---
tag: R3JT14
kind: theorem
slug: strong-equivalence
name: Strong equivalence of logic programs
aliases:
- Lifschitz-Pearce-Valverde theorem
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: research
summary: Two programs have the same stable models in every context exactly when they have the same SE-models, which is the same as equivalence in the logic of here-and-there.
prereqs: [stable-model-semantics, gelfond-lifschitz-reduct]
see_also: [splitting-set-theorem, answer-set-programming, co-np, sat, disjunctive-logic-program, choice-rule, fages-theorem, nonmonotonic-reasoning]
sources:
  - paper: "Vladimir Lifschitz, David Pearce and Agustín Valverde, Strongly equivalent logic programs, ACM Transactions on Computational Logic 2(4), 526 to 541 (2001)"
    locator: the definition of strong equivalence and the main theorem on equivalence in the logic of here-and-there
  - paper: "Hudson Turner, Strong equivalence made easy: nested expressions and weight constraints, Theory and Practice of Logic Programming 3(4-5), 609 to 622 (2003)"
    locator: the definition of SE-models and the characterization of strong equivalence by them
  - paper: "Fangzhen Lin, Reducing strong equivalence of logic programs to entailment in classical propositional logic, in Proceedings of the Eighth International Conference on Principles of Knowledge Representation and Reasoning (KR 2002), Morgan Kaufmann, 170 to 176 (2002)"
    locator: the reduction to classical entailment and the coNP-completeness of the check
  - book: isbn:9783030246570
    title: Vladimir Lifschitz, Answer Set Programming, Springer (2019)
    locator: the section on strong equivalence and its use to simplify programs
---

Two logic programs are *strongly equivalent* when one can replace the other inside any larger program without a change of the [stable models](/stable-model-semantics/). Ordinary equivalence, the same stable models, is not enough for this, because the stable model semantics is nonmonotonic: $\{p \leftarrow \mathit{not}\ q\}$ and $\{p\}$ have the same stable model, but after adding the fact $q$ they do not. Lifschitz, Pearce and Valverde (2001) proved that strong equivalence is equivalence in the logic of here-and-there, a logic between intuitionistic and classical logic. Turner (2003) restated this with SE-models, built from the [Gelfond-Lifschitz reduct](/gelfond-lifschitz-reduct/), which is the form given here.

## Statement

Let $P$ and $Q$ be finite ground normal programs, and let $A$ be the set of atoms that occur in $P$ or $Q$. For a set $Y$ of atoms, $P^Y$ is the reduct of $P$ by $Y$, and "$X \models P$" means that $X$ satisfies every rule of $P$ read as a classical implication.

- An *SE-model* of $P$ is a pair $(X, Y)$ with $X \subseteq Y \subseteq A$, $Y \models P$ and $X \models P^Y$. Write $\mathrm{SE}(P)$ for the set of SE-models.
- $P$ and $Q$ are *strongly equivalent* if, for every normal program $R$, the programs $P \cup R$ and $Q \cup R$ have the same stable models.

**Theorem** (Lifschitz, Pearce and Valverde 2001; Turner 2003). $P$ and $Q$ are strongly equivalent if and only if $\mathrm{SE}(P) = \mathrm{SE}(Q)$.

In the form of Lifschitz, Pearce and Valverde, the right side reads: $P$ and $Q$, as sets of formulas with $\mathit{not}$ read as negation, are equivalent in the logic of here-and-there. An SE-model $(X, Y)$ is a model of that logic, with $X$ the atoms true "here" and $Y$ the atoms true "there". Both papers prove the theorem for much more general programs: nested expressions, disjunctive heads and, in the later literature, arbitrary propositional theories. The proof below shows that the extra program $R$ can always be chosen to consist of facts and rules $a \leftarrow b$.

## In plain words

Two pieces of a program can give the same answers when they stand alone, and still behave differently once other rules are added. One rule may say "p unless q", the other just "p". Alone, both give p. Add the fact q, and only the second still gives p. Strong equivalence asks for the same answers in every possible surrounding, which is what a programmer needs before replacing one piece by another. The theorem turns this question about all programs into a check on one finite list of pairs of sets of atoms for each program. The lists can be compared directly, or the check can be passed to a standard solver for logic formulas.

## Proof

This is the proof through SE-models of Turner (2003). Lifschitz, Pearce and Valverde (2001) prove the same result in the logic of here-and-there.

**Lemma 1.** $Y$ is a stable model of $P$ if and only if $(Y, Y) \in \mathrm{SE}(P)$ and there is no $(X, Y) \in \mathrm{SE}(P)$ with $X \subsetneq Y$.

First, $Y \models P$ if and only if $Y \models P^Y$: a rule of $P$ whose body is true in $Y$ has no negative atom in $Y$, so its reduct is in $P^Y$ with the same positive body, and conversely. So $(Y, Y) \in \mathrm{SE}(P)$ means $Y \models P^Y$. Now $Y = \mathrm{lm}(P^Y)$ holds if and only if $Y$ is a model of $P^Y$ and no proper subset of $Y$ is, because the least model is contained in every model.

**Lemma 2.** $\mathrm{SE}(P \cup R) = \mathrm{SE}(P) \cap \mathrm{SE}(R)$, for SE-models over the atoms of $P$, $Q$ and $R$.

This holds because $(P \cup R)^Y = P^Y \cup R^Y$, and a set satisfies a union of rules exactly when it satisfies both parts.

**If.** If $\mathrm{SE}(P) = \mathrm{SE}(Q)$, then by Lemma 2 $\mathrm{SE}(P \cup R) = \mathrm{SE}(Q \cup R)$ for every $R$, and by Lemma 1 the two programs have the same stable models. (An atom outside $A$ is in $P$ only through $R$, and the SE-models of $P$ over a larger set of atoms are determined by those over $A$, so the equality carries over.)

**Only if.** Suppose $(X, Y) \in \mathrm{SE}(P) \setminus \mathrm{SE}(Q)$; the other case is symmetric. We build $R$ such that $Y$ is stable for exactly one of $P \cup R$ and $Q \cup R$.

*Case 1: $Y \not\models Q$.* Let $R$ be the facts $Y$. Then $(P \cup R)^Y = P^Y \cup Y$, and since $Y \models P^Y$, its least model is $Y$. So $Y$ is stable for $P \cup R$. It is not stable for $Q \cup R$, because $Y$ does not satisfy $Q$.

*Case 2: $Y \models Q$.* Then $(Y, Y) \in \mathrm{SE}(Q)$, so $X \neq Y$, and $(Y, Y) \in \mathrm{SE}(P)$ as well. Let $R$ be the facts $X$ together with all rules $a \leftarrow b$ for $a, b \in Y \setminus X$. The reduct of $R$ is $R$, and a set $Z$ with $X \subseteq Z \subseteq Y$ satisfies $R$ exactly when $Z = X$ or $Z = Y$, since one atom of $Y \setminus X$ forces all the others. So the SE-models of $R$ with second part $Y$ are $(X, Y)$ and $(Y, Y)$. By Lemma 2, $P \cup R$ has both, so $Y$ is not stable for it by Lemma 1. $Q \cup R$ has $(Y, Y)$ but not $(X, Y)$, so $Y$ is stable for it.

**A check by hand.** Take $P = \{p \leftarrow \mathit{not}\ q\}$ and $Q = \{p\}$ over $A = \{p, q\}$. For $Q$, a pair needs $p \in X$, which gives $(\{p\}, \{p\})$, $(\{p\}, \{p, q\})$ and $(\{p, q\}, \{p, q\})$. For $P$ and $Y = \{q\}$, the reduct $P^Y$ is empty, so $(\emptyset, \{q\})$ is an SE-model of $P$; and $Y = \{q\}$ does not satisfy $Q$. This is Case 1: with $R = \{q\}$, the program $P \cup R$ has the stable model $\{q\}$, while $Q \cup R$ has the stable model $\{p, q\}$. In all, $P$ has four SE-models that $Q$ lacks: $(\emptyset, \{q\})$, $(\{q\}, \{q\})$, $(\emptyset, \{p, q\})$ and $(\{q\}, \{p, q\})$.

## Consequences

- **Safe simplification.** A rule whose head is also in its positive body, such as $p \leftarrow p, q$, can be deleted from any program, and so can a rule with both $b$ and $\mathit{not}\ b$ in its body: in both cases the empty program has the same SE-models. Optimizers and grounders of [answer set programming](/answer-set-programming/) use such strong equivalences to rewrite rules.
- **Positive parts.** $\{a \leftarrow b,\ b \leftarrow a,\ a\}$ is strongly equivalent to $\{a,\ b\}$: both have the single SE-model $(\{a, b\}, \{a, b\})$. For programs without negation, strong equivalence is the same as classical equivalence.
- **Complexity.** To decide whether two finite programs are strongly equivalent is [coNP](/co-np/)-complete. A pair $(X, Y)$ in one set but not the other is a short certificate of non-equivalence. Lin (2002) reduced the problem to classical entailment over the atoms and a primed copy of each, so a [SAT](/sat/) solver can check it.
- **A logical view of rules.** The theorem gives answer set programs a monotonic logic, here-and-there, in which replacement of equivalents is valid, although the stable model semantics itself is nonmonotonic. Pearce's equilibrium logic defines stable models as particular models of this logic.

## Tightness

The class of added programs matters. With $R$ ranging only over the empty program, the condition is ordinary equivalence, and $\{p \leftarrow \mathit{not}\ q\}$ and $\{p\}$ pass it. With $R$ ranging over sets of facts, the condition is *uniform equivalence*, which is strictly weaker. For example, $P = \{a\}$ and $Q = \{a \leftarrow \mathit{not}\ b,\ a \leftarrow b\}$ have the same stable models after adding any set of facts. They are not strongly equivalent: $(\emptyset, \{a, b\})$ is an SE-model of $Q$, because $Q^{\{a, b\}} = \{a \leftarrow b\}$, but not of $P$. Case 2 of the proof gives $R = \{a \leftarrow b,\ b \leftarrow a\}$: then $P \cup R$ has the stable model $\{a, b\}$ and $Q \cup R$ has no stable model. The proof shows that facts and rules with one positive body atom are always enough.

The theorem is about the stable model semantics. It does not carry over to the [completion](/clark-completion/): $\{p \leftarrow p\}$ and the empty program are strongly equivalent, but their completions, $p \leftrightarrow p$ and $\neg p$, have different models.

## History

Pearce introduced equilibrium logic in the 1990s, which defines stable models within the logic of here-and-there. Lifschitz, Pearce and Valverde (2001) used it to characterize strong equivalence. Turner gave the SE-model form in 2001 and extended it to weight constraints in 2003. Lin (2002) gave the reduction to classical logic, and the coNP-completeness was shown in the same period by several groups. Uniform equivalence and relativized notions, where $R$ is restricted to some atoms, were studied later.

## References
