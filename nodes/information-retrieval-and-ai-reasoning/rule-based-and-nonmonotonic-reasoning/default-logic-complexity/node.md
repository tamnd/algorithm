---
tag: 5VZ41P
kind: theorem
slug: default-logic-complexity
name: Sigma2P-completeness of default logic
aliases:
- Gottlob default logic complexity
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: research
summary: Deciding whether a propositional default theory has an extension, or credulous entailment, is Sigma2P-complete.
prereqs: [default-logic, default-extension, polynomial-hierarchy, qbf]
see_also: [autoepistemic-logic, circumscription, abductive-reasoning, disjunctive-asp-sigma2-completeness, stable-model-np-completeness, np-complete]
sources:
  - paper: doi:10.1093/logcom/2.3.397
    title: Georg Gottlob, Complexity results for nonmonotonic logics, Journal of Logic and Computation 2(3), 397 to 425 (1992)
    locator: the results for default logic (Sigma2P-completeness of existence and credulous reasoning, Pi2P-completeness of skeptical reasoning) and for autoepistemic logic
  - paper: doi:10.1016/0004-3702(80)90014-4
    title: Raymond Reiter, A logic for default reasoning, Artificial Intelligence 13(1-2), 81 to 132 (1980)
    locator: Section 2 (the definition of extensions and the characterization by generating defaults)
  - paper: "Michael Thomas and Heribert Vollmer, Complexity of non-monotonic logics, Bulletin of the EATCS 102 (2010), arXiv:1009.1990"
    locator: Theorem 3.5 (default logic, citing Gottlob 1992 and Stillman 1992), Theorem 4.6 (autoepistemic logic), Theorem 6.1 (abduction) and the remarks on model checking (Liberatore and Schaerf 2005) and on the fragments of Kautz and Selman and of Stillman
---

Reasoning with defaults is harder than classical reasoning by exactly one level of the [polynomial hierarchy](/polynomial-hierarchy/). Gottlob (1992) proved that, for finite propositional [default theories](/default-logic/), deciding whether an [extension](/default-extension/) exists and deciding whether a formula is in some extension are $\Sigma_2^p$-complete, and deciding whether a formula is in every extension is $\Pi_2^p$-complete. The upper bound comes from guessing which defaults fire and checking the guess with polynomially many calls to a SAT oracle. The lower bound encodes a quantified Boolean formula $\exists X \forall Y \psi$ with one pair of defaults per variable of $X$.

## Statement

A finite propositional default theory is a pair $(W, D)$ of a finite set $W$ of propositional formulas and a finite set $D$ of defaults $\alpha : \beta_1, \ldots, \beta_n / \gamma$ over finitely many atoms. The input size is the total length of $W$, $D$ and the query $\varphi$.

**Theorem** (Gottlob 1992). For finite propositional default theories:

1. **EXT**, deciding whether $(W, D)$ has an extension, is $\Sigma_2^p$-complete.
2. **CRED**, deciding whether $\varphi$ is in some extension of $(W, D)$, is $\Sigma_2^p$-complete.
3. **SKEP**, deciding whether $\varphi$ is in every extension of $(W, D)$, is $\Pi_2^p$-complete.

CRED and SKEP are already hard for theories with $W = \emptyset$ and only normal, prerequisite-free defaults. EXT is already hard for such theories plus one default that is not normal. Hardness is under polynomial-time many-one reductions.

## In plain words

A default reasoner has to do two things. It must choose which rules with exceptions to use, and for each choice it must check, with ordinary logic, that the choice is stable: every rule used is allowed and every rule left out is really blocked. The choosing is like an NP search, and each check is a set of satisfiability tests. Gottlob showed that this "search over choices, each checked with a SAT solver" pattern is not only enough but needed: unless the polynomial hierarchy collapses, no method can turn default reasoning into a single SAT problem of polynomial size.

## Proof

Write $\mathrm{Th}(S)$ for the classical consequences of $S$, $\mathrm{cons}(G)$ for the conclusions of a set $G$ of defaults, and for $G \subseteq D$ let $E_G = \mathrm{Th}(W \cup \mathrm{cons}(G))$.

**Lemma.** For a set $E$, define $G_0 = \emptyset$ and $G_{i+1} = \{d \in D : \mathrm{pre}(d) \in \mathrm{Th}(W \cup \mathrm{cons}(G_i)),\ \neg\beta \notin E \text{ for each justification } \beta \text{ of } d\}$. The sets grow, so they become constant at some $G^* = G_{|D|}$. Then $\Gamma(E) = \mathrm{Th}(W \cup \mathrm{cons}(G^*))$.

*Proof.* Let $T = \mathrm{Th}(W \cup \mathrm{cons}(G^*))$. It contains $W$ and is closed. If a default has its prerequisite in $T$ and its justifications consistent with $E$, it is in $G_{|D|+1} = G^*$, so its conclusion is in $T$. As $\Gamma(E)$ is the least such set, $\Gamma(E) \subseteq T$. Conversely, by induction on $i$, every conclusion of $G_i$ is in $\Gamma(E)$: a default of $G_{i+1}$ has its prerequisite in $\mathrm{Th}(W \cup \mathrm{cons}(G_i)) \subseteq \Gamma(E)$ and passes the justification test, so its conclusion is in $\Gamma(E)$. Hence $T \subseteq \Gamma(E)$. $\square$

So every extension $E$ equals $E_{G^*}$ for a subset $G^*$ of $D$.

**Membership.** For EXT, guess $G \subseteq D$ and accept when $E_G$ is an extension. To check this, compute $G^*$ for $E = E_G$ by the iteration of the lemma. Each round makes at most $|D|$ tests "$W \cup \mathrm{cons}(G_i) \models \mathrm{pre}(d)$" (one coNP question) and one test "$W \cup \mathrm{cons}(G) \cup \{\beta\}$ is satisfiable" (one NP question) for each justification $\beta$ in $D$, and there are at most $|D|$ rounds. Then test $\mathrm{Th}(W \cup \mathrm{cons}(G^*)) = E_G$ by checking that each side entails each formula of the other, again polynomially many coNP questions. By the lemma, the test succeeds exactly when $\Gamma(E_G) = E_G$. A nondeterministic polynomial-time machine with an NP oracle does all of this, so EXT is in $\Sigma_2^p$. For CRED, also check $W \cup \mathrm{cons}(G) \models \varphi$. For the complement of SKEP, check $W \cup \mathrm{cons}(G) \not\models \varphi$ instead. So CRED is in $\Sigma_2^p$ and SKEP is in $\Pi_2^p$.

**The gadget.** Let $\psi$ be a formula over disjoint sets of atoms $X$ and $Y$. Put $W = \emptyset$ and $D_X = \{ : x / x,\ : \neg x / \neg x \ \text{ for } x \in X\}$. For an assignment $\tau$ of $X$ let $L_\tau$ be the set of the literals over $X$ that $\tau$ makes true. Let $D$ be $D_X$ plus extra defaults whose conclusions are $\psi$ or a fresh atom. *Claim:* in every extension $E$ of $(\emptyset, D)$, exactly one of the two defaults for each $x \in X$ applies, so $E \supseteq L_\tau$ for one $\tau$. Indeed, if $E$ is inconsistent, every justification fails, so $E = \mathrm{Th}(\emptyset)$, which is consistent, a contradiction. As $E$ is consistent, $x$ or $\neg x$ is consistent with $E$, so at least one of the two defaults applies, and both cannot apply, since then $x, \neg x \in E$.

**CRED is $\Sigma_2^p$-hard.** Reduce from the truth of $\exists X \forall Y \psi$, which is $\Sigma_2^p$-complete (see [QBF](/qbf/)). Take $D = D_X$. By the claim and the lemma, each extension is $\mathrm{Th}(L_\tau)$, and for every $\tau$ the set $\mathrm{Th}(L_\tau)$ is one, because exactly the defaults for $L_\tau$ pass the test. Now $\psi \in \mathrm{Th}(L_\tau)$ exactly when $\psi$ holds for $\tau$ and every assignment of $Y$. So $\psi$ is in some extension exactly when $\exists X \forall Y \psi$ is true.

**SKEP is $\Pi_2^p$-hard.** Reduce from $\forall X \exists Y \psi$. Take $D = D_X \cup \{ : \psi / \psi\}$. By the claim, an extension is $\mathrm{Th}(L_\tau)$ or $\mathrm{Th}(L_\tau \cup \{\psi\})$. If $L_\tau \cup \{\psi\}$ is satisfiable, the default $: \psi / \psi$ is not blocked by either set, so only $\mathrm{Th}(L_\tau \cup \{\psi\})$ is a fixed point, and it is one. If it is unsatisfiable, the default is blocked, and the extension is $\mathrm{Th}(L_\tau)$, which does not contain $\psi$. So $\psi$ is in every extension exactly when $\psi$ is satisfiable together with every $L_\tau$, that is, when $\forall X \exists Y \psi$ is true.

**EXT is $\Sigma_2^p$-hard.** Reduce from $\exists X \forall Y \psi$. Take a fresh atom $z$ and $D = D_X \cup \{d_z\}$ with $d_z = : \neg\psi \wedge \neg z / z$. If $d_z$ applies in an extension $E$, then $z \in E$, so its own justification is inconsistent with $E$, which is a contradiction. So $d_z$ does not apply, and by the claim $E = \mathrm{Th}(L_\tau)$. This is an extension exactly when $d_z$ is blocked, that is, when $L_\tau \models \psi \vee z$. As $z$ does not occur in $L_\tau$ or $\psi$, this holds exactly when $L_\tau \models \psi$. So an extension exists exactly when $\exists X \forall Y \psi$ is true.

Each reduction builds $2|X| + 1$ defaults of total size $O(|\psi| + |X|)$ in polynomial time. $\blacksquare$

## Consequences

- **No polynomial encoding into SAT.** If any of the three tasks had a polynomial-time reduction to SAT, then $\Sigma_2^p = \mathrm{NP}$ and the polynomial hierarchy would collapse to its first level. Practical default reasoners therefore use a [QBF](/qbf/) solver, or a guess-and-check loop in which one [SAT](/sat/) solver proposes generating sets and another refutes them, in the style of [CEGAR](/cegar/).
- **Autoepistemic logic.** The same three results hold for stable expansions of finite propositional [autoepistemic](/autoepistemic-logic/) theories (Niemelä 1990, Gottlob 1992; Thomas and Vollmer 2010, Theorem 4.6). Membership uses Niemelä's finite characterization of expansions by full sets of subformulas $L\varphi$.
- **Related second-level problems.** Propositional [circumscription](/circumscription/) inference is $\Pi_2^p$-complete, the existence of an [abductive](/abductive-reasoning/) explanation is $\Sigma_2^p$-complete, and so is the existence of an answer set of a [disjunctive program](/disjunctive-asp-sigma2-completeness/). All of these come from the same pattern: a minimality or fixed-point test that needs a coNP check inside an NP guess.
- **The program fragment.** When the justifications are negated atoms, the prerequisites are conjunctions of atoms, the conclusions are atoms and $W = \emptyset$, the theory is a normal logic program, and the entailment checks become polynomial. Existence then drops to NP, as the page on [stable model existence](/stable-model-np-completeness/) shows.
- **Model checking.** Deciding whether a given interpretation is a model of some extension stays on the second level: Liberatore and Schaerf (2005) showed that this model-checking problem is $\Sigma_2^p$-complete (Thomas and Vollmer 2010, Section 3).

## Tightness

The upper bounds match the lower bounds, so the classes are exact. The hardness also survives strong restrictions: in the proof, $W$ is empty, every default for CRED and SKEP is normal and prerequisite-free, and only one default is not normal for EXT. That one default cannot be removed: every normal theory has an extension (Reiter 1980), so EXT is trivial for normal theories. The hardness disappears only when the formulas themselves are restricted, for example to literals and Horn clauses. Kautz and Selman (1991) and Stillman (1990) found such fragments in which some tasks drop to NP or to polynomial time (Thomas and Vollmer 2010, Section 3).

## History

Reiter (1980) defined default logic and observed that it is not semi-decidable in the first-order case. The exact propositional complexity was open until 1992. Gottlob (1992) proved the $\Sigma_2^p$ and $\Pi_2^p$ completeness results for default logic and for autoepistemic logic, and Stillman (1992) obtained results for default logic independently. Earlier, Kautz and Selman (1991) and Stillman (1990) had shown NP-completeness and polynomial cases for restricted default theories, and Niemelä (1990) had placed autoepistemic reasoning in the second level. Liberatore and Schaerf (2005) later settled the complexity of model checking.

## References
