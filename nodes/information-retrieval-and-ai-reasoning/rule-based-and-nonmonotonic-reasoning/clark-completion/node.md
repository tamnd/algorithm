---
tag: JRMWPA
kind: definition
slug: clark-completion
name: Clark's completion
aliases:
- program completion
- predicate completion
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: The completion of a logic program reads the rules for each predicate as an "if and only if" definition, so an atom holds exactly when the body of one of its rules holds.
prereqs: [negation-as-failure, logic-programming, horn-clause]
see_also: [sldnf-resolution, fages-theorem, loop-formulas, stable-model-semantics, closed-world-assumption, sat, unit-propagation, herbrand-universe]
sources:
  - paper: doi:10.1007/978-1-4684-3384-5_11
    title: Keith L. Clark, Negation as failure, in Hervé Gallaire and Jack Minker (eds.), Logic and Data Bases, Plenum Press, New York, 293 to 322 (1978)
    locator: the definition of the completed database and the soundness of negation as failure for it
  - book: isbn:9783540181996
    title: John W. Lloyd, Foundations of Logic Programming, 2nd edition, Springer (1987)
    locator: the chapter on normal programs, the completion and its equality axioms
  - paper: "Krzysztof R. Apt and Roland N. Bol, Logic programming and negation: a survey, Journal of Logic Programming 19/20, 9 to 71 (1994)"
    locator: the section on the completion semantics
  - paper: doi:10.1016/j.artint.2004.04.004
    title: "Fangzhen Lin and Yuting Zhao, ASSAT: computing answer sets of a logic program by SAT solvers, Artificial Intelligence 157(1-2), 115 to 137 (2004)"
    locator: the completion of a finite propositional program as a set of clauses
---

Clark's completion turns a logic program into a classical theory by reading the rules for each predicate as its full definition: an atom holds if and only if the body of one of its rules holds. Clark (1978) gave it as the declarative meaning of [negation as failure](/negation-as-failure/), and proved that a finite failure of $p$ in [SLDNF resolution](/sldnf-resolution/) is sound for $\neg p$ in the completion. The soundness and completeness results for the procedure are on the SLDNF page; this page gives the definition, the ground case that answer set solvers use, and how the completion relates to [stable models](/stable-model-semantics/).

## Definition

**Propositional case.** Let $P$ be a finite ground normal program over a set $A$ of atoms. A rule $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$ has the body formula $b_1 \wedge \cdots \wedge b_m \wedge \neg c_1 \wedge \cdots \wedge \neg c_k$, and an empty body is $\top$. The *completion* $\mathrm{Comp}(P)$ is the set of formulas

$$a \leftrightarrow \bigvee_{r \in P,\ \mathrm{head}(r) = a} \mathrm{body}(r) \qquad \text{for each } a \in A,$$

where the empty disjunction is $\bot$, so an atom with no rules gets $\neg a$. The models of $\mathrm{Comp}(P)$ are called the *supported models* of $P$. A set $M \subseteq A$ is a model of $\mathrm{Comp}(P)$ exactly when $M = T_P(M)$, where $T_P(M)$ is the set of heads of the rules whose body is true in $M$: the direction "$\leftarrow$" says $T_P(M) \subseteq M$, and the direction "$\rightarrow$" says that each true atom has a rule with a true body.

**First-order case.** For a predicate $p$ of arity $n$, each rule $p(t_1, \ldots, t_n) \leftarrow L_1, \ldots, L_k$ with variables $\vec{y}$ is rewritten as

$$\exists \vec{y}\, (x_1 = t_1 \wedge \cdots \wedge x_n = t_n \wedge L_1 \wedge \cdots \wedge L_k),$$

with fresh variables $x_1, \ldots, x_n$ and $\mathit{not}$ read as $\neg$. If $E_1, \ldots, E_j$ are these formulas for all rules of $p$, the completed definition of $p$ is $\forall \vec{x}\, (p(\vec{x}) \leftrightarrow E_1 \vee \cdots \vee E_j)$, and $\forall \vec{x}\, \neg p(\vec{x})$ if $p$ has no rules. The completion is the set of completed definitions together with Clark's equality theory, which says that distinct function symbols give distinct terms, that function symbols are injective, and that no term equals a proper subterm of itself. Lloyd's book states these axioms in full.

## Examples and non-examples

- $P = \{p \leftarrow \mathit{not}\ q\}$. Then $\mathrm{Comp}(P) = \{p \leftrightarrow \neg q,\ \neg q\}$, with the single model $\{p\}$. This is also the only stable model.
- $P = \{p \leftarrow \mathit{not}\ q,\ q \leftarrow \mathit{not}\ p\}$. The completion $\{p \leftrightarrow \neg q,\ q \leftrightarrow \neg p\}$ has the models $\{p\}$ and $\{q\}$, the same as the stable models.
- $P = \{p \leftarrow \mathit{not}\ p\}$. The completion $p \leftrightarrow \neg p$ is inconsistent. The program has no stable model either.
- **Non-example of agreement.** $P = \{p \leftarrow p\}$ has the completion $p \leftrightarrow p$, with models $\emptyset$ and $\{p\}$. The only stable model is $\emptyset$, because nothing derives $p$. The completion accepts support through a positive cycle, which the stable model semantics rejects. [Fages' theorem](/fages-theorem/) says that without positive cycles the two agree, and [loop formulas](/loop-formulas/) are the clauses that must be added to the completion to make them agree in general.
- **First order.** For $\mathit{even}(0)$ and $\mathit{even}(s(s(X))) \leftarrow \mathit{even}(X)$, the completed definition is $\forall x\, (\mathit{even}(x) \leftrightarrow x = 0 \vee \exists y\, (x = s(s(y)) \wedge \mathit{even}(y)))$. With the equality axioms it entails $\neg \mathit{even}(s(0))$, which SLDNF resolution derives by finite failure.

## Related definitions

- **Supported model.** A model $M$ of $P$ in which each true atom is the head of a rule whose body is true in $M$; the same as a model of the completion.
- **Stable model.** Every [stable model](/stable-model-semantics/) is supported, so it is a model of the completion. The converse holds for tight programs ([Fages' theorem](/fages-theorem/)).
- **Tight program.** A program whose positive dependency graph has no cycle. For a tight program, the completion and the stable models coincide.
- **Closed-world assumption.** For a definite program, the [closed-world assumption](/closed-world-assumption/) makes false every ground atom that is not a consequence. The completion is weaker: it makes false only what follows from the "only if" halves, so on $\{p \leftarrow p\}$ it leaves $p$ open, while the closed-world assumption makes $p$ false.
- **Clausal form.** For a finite ground program, the completion becomes a set of clauses of size linear in the program after one new atom is introduced for each rule body. Answer set solvers such as ASSAT and clasp give these clauses to a [SAT](/sat/) solver or use them in [unit propagation](/unit-propagation/).

## References
