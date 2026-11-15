---
tag: Z1MD5D
kind: model
slug: default-logic
name: Default logic
aliases:
- Reiter's default logic
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: Extends first-order logic with default rules of the form a:b/c, read as from a, if b is consistent, conclude c.
prereqs: [nonmonotonic-reasoning, fixed-point]
see_also: [default-extension, default-logic-complexity, autoepistemic-logic, circumscription, stable-model-semantics, system-p, closed-world-assumption]
sources:
  - paper: doi:10.1016/0004-3702(80)90014-4
    title: Raymond Reiter, A logic for default reasoning, Artificial Intelligence 13(1-2), 81 to 132 (1980)
    locator: Section 2 (defaults, default theories, the operator Gamma and extensions), Section 3 (normal default theories, existence, semi-monotonicity and orthogonality) and Section 4 (proof theory for normal defaults)
  - paper: doi:10.1093/logcom/2.3.397
    title: Georg Gottlob, Complexity results for nonmonotonic logics, Journal of Logic and Computation 2(3), 397 to 425 (1992)
    locator: the Sigma2P-completeness of extension existence and credulous reasoning and the Pi2P-completeness of skeptical reasoning for finite propositional default theories
  - paper: doi:10.1016/0004-3702(90)90101-5
    title: Sarit Kraus, Daniel Lehmann and Menachem Magidor, Nonmonotonic reasoning, preferential models and cumulative logics, Artificial Intelligence 44(1-2), 167 to 207 (1990)
    locator: Section 3.1 (default logic, even with normal defaults only, fails Cautious Monotonicity)
  - paper: "Michael Thomas and Heribert Vollmer, Complexity of non-monotonic logics, Bulletin of the EATCS 102 (2010), arXiv:1009.1990"
    locator: Section 3, Theorem 3.5 (the complexity of default logic) and the discussion of the fragments studied by Kautz and Selman and by Stillman
---

Default logic adds rules with exceptions to classical logic. A default $\alpha : \beta / \gamma$ reads "if $\alpha$ holds and it is consistent to assume $\beta$, conclude $\gamma$". Reiter (1980) gave it a fixed-point semantics: a set of beliefs is acceptable, an [extension](/default-extension/), when it is exactly what the facts and the defaults that it does not block derive. A theory can have one extension, several or none, so a reasoner must choose between credulous consequence (in some extension) and skeptical consequence (in every extension). For finite propositional theories both questions sit on the second level of the [polynomial hierarchy](/polynomial-hierarchy/).

## The machine

For a logic, the machine is its syntax and its semantics.

**Syntax.** A *default* is an expression

$$\frac{\alpha : \beta_1, \ldots, \beta_n}{\gamma}$$

where the *prerequisite* $\alpha$, the *justifications* $\beta_1, \ldots, \beta_n$ and the *conclusion* $\gamma$ are formulas. A prerequisite $\top$ is often left out, as in $: \beta / \gamma$. A *default theory* is a pair $(W, D)$ of a set $W$ of formulas (the facts) and a set $D$ of defaults. Reiter allows first-order formulas, and a default with free variables stands for all its ground instances. The rest of this page uses the propositional case: finitely many atoms, $W$ and $D$ finite.

Important special forms:

- *normal* defaults $\alpha : \gamma / \gamma$, where the justification is the conclusion,
- *semi-normal* defaults $\alpha : \gamma \wedge \delta / \gamma$,
- *prerequisite-free* defaults $: \beta / \gamma$.

**Semantics.** Write $\mathrm{Th}(S)$ for the classical consequences of $S$. For a set $S$ of formulas, $\Gamma(S)$ is the smallest set $T$ that contains $W$, is closed under $\mathrm{Th}$, and contains $\gamma$ for each default whose prerequisite is in $T$ and none of whose justifications has its negation in $S$. An *extension* is a set $E$ with $\Gamma(E) = E$. So $E$ is used only to test the justifications, and everything in $E$ must be derived from $W$. The page on [extensions](/default-extension/) gives Reiter's iterative test, the generating defaults and a brute-force algorithm.

**Steps.** A derivation in an extension has two kinds of steps: classical inference, and the application of a default whose prerequisite is already derived and whose justifications are consistent with the final extension. The second kind refers to the end result. This is why a default step cannot be checked locally, and why the logic is nonmonotonic: a new fact can make a justification inconsistent and so remove a conclusion.

## What it counts

Default logic defines three decision tasks for a finite propositional theory $(W, D)$ and a formula $\varphi$:

- **Existence:** does $(W, D)$ have an extension?
- **Credulous reasoning:** is $\varphi$ in some extension?
- **Skeptical reasoning:** is $\varphi$ in every extension? A theory with no extension skeptically entails every formula.

The relation "$\varphi$ is in every extension of $(W \cup \{\alpha\}, D)$" gives a consequence relation $\alpha \mathrel{|\!\sim} \varphi$. It is not monotonic: Tweety the bird flies by the default $\mathit{bird} : \mathit{flies} / \mathit{flies}$, but not after the fact $\neg\mathit{flies}$, or the facts $\mathit{penguin}$ and $\mathit{penguin} \supset \neg\mathit{flies}$, are added.

The cost measure is the usual one for propositional reasoning: the time as a function of the size of $W$, $D$ and $\varphi$, with an oracle for classical satisfiability when the tasks are placed in the polynomial hierarchy.

## Relation to other models

- **Classical logic.** With $D = \emptyset$ the unique extension is $\mathrm{Th}(W)$, and default logic is classical logic.
- **[Closed-world assumption](/closed-world-assumption/).** The defaults $: \neg p / \neg p$ for every atom $p$ give a form of the closed-world assumption. Unlike the classical CWA, they cannot make a consistent theory inconsistent: for $W = \{p \vee q\}$ there are two extensions, $\mathrm{Th}(\{p, \neg q\})$ and $\mathrm{Th}(\{\neg p, q\})$.
- **Logic programs.** The rule $p \leftarrow q_1, \ldots, q_k, \mathit{not}\ r_1, \ldots, \mathit{not}\ r_m$ reads as the default $q_1 \wedge \cdots \wedge q_k : \neg r_1, \ldots, \neg r_m / p$. Under this reading, the [stable models](/stable-model-semantics/) of a normal program are exactly the atoms of the extensions of the default theory with $W = \emptyset$. [Answer set programming](/answer-set-programming/) is therefore a restricted, decidable and fast fragment of default logic.
- **[Autoepistemic logic](/autoepistemic-logic/).** It expresses "consistent to assume $\beta$" as $\neg L \neg\beta$ inside the object language. Extensions and stable expansions are similar fixed points, but a premise such as $La \supset a$ has an expansion that contains $a$, while the default $a : a / a$ has no extension that contains $a$.
- **[Circumscription](/circumscription/).** It works with minimal models instead of fixed points, and it always gives one theory instead of a family of extensions. Skeptical default reasoning and circumscription agree on many small examples, such as the Nixon diamond, but not in general.
- **Preferential logics.** Skeptical default consequence fails Cautious Monotonicity even for normal defaults (Makinson's example in Kraus, Lehmann and Magidor 1990, Section 3.1, worked out on the [extension page](/default-extension/)). So it is not a [System P](/system-p/) relation.

## Known results in the model

- **Normal theories always have an extension** (Reiter 1980, Section 3). They are also *semi-monotonic*: adding a normal default keeps each old extension inside a new one. Two different extensions of a normal theory are inconsistent with each other. Reiter used these facts to give a goal-directed proof procedure for normal defaults.
- **Non-normal defaults can destroy all extensions.** The single default $: \neg a / a$ has none. Add it to any theory with consistent facts in which no formula mentions $a$, and the new theory has no extension: if $a$ is in a candidate $E$, the default that is the only source of $a$ is blocked, and if $a$ is not in $E$, the default applies and puts $a$ in.
- **First-order default logic is not semi-decidable.** A default step needs a consistency test, and consistency in first-order logic is not semi-decidable. As Reiter (1980) observed, the consequences of a first-order default theory therefore need not form a recursively enumerable set.
- **Exact complexity in the propositional case** (Gottlob 1992; see the [theorem page](/default-logic-complexity/)): existence and credulous reasoning are $\Sigma_2^p$-complete, and skeptical reasoning is $\Pi_2^p$-complete. Credulous and skeptical reasoning are already hard for normal theories with $W = \emptyset$. Existence is trivial for normal theories, and its hardness needs one non-normal default.
- **Fragments.** Kautz and Selman (1991) and Stillman (1990) studied default theories built from literals and Horn clauses, where some tasks drop to NP or to polynomial time (Thomas and Vollmer 2010, Section 3).
- **Algorithms.** For small theories, the [brute-force search](/default-extension/) over the generating defaults decides every task. Larger propositional theories are handled by reduction to [QBF](/qbf/) or by a guess-and-check loop with a [SAT](/sat/) solver, which matches the $\Sigma_2^p$ upper bound. The program fragment is handled by ASP solvers.

## References
