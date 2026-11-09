---
tag: A5ZA6H
kind: theorem
slug: robinson-completeness-theorem
name: Robinson completeness theorem
aliases:
- resolution completeness theorem
- completeness of resolution
- refutation completeness of resolution
area: logic-and-constraints/unification-and-resolution
level: core
summary: A set of clauses is unsatisfiable if and only if binary resolution and factoring derive the empty clause from it (Robinson 1965). The proof joins Herbrand's theorem, ground completeness and lifting.
prereqs: [herbrand-theorem, lifting-lemma, binary-resolution, factoring]
see_also: [robinson-resolution, refutation, lifting-lemma, herbrand-theorem, first-order-theorem-proving, set-of-support, ordered-resolution, haken-resolution-lower-bound]
sources:
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: the resolution theorem (a finite set of clauses is unsatisfiable if and only if its resolution closure contains the empty clause), proved from Herbrand's theorem with the lifting argument
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 5, The resolution principle (the lifting lemma and the completeness theorem of resolution, proved with semantic trees from Chapter 4)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (refutational completeness by a model construction for saturated sets, and lifting)
---

The **Robinson completeness theorem** says that a set of first-order [clauses](/clause/) is unsatisfiable if and only if the empty clause $\square$ can be derived from it by [binary resolution](/binary-resolution/) and [factoring](/factoring/). The "if" direction is soundness of the rules, and the "only if" direction is refutation completeness. The proof has three parts: [Herbrand's theorem](/herbrand-theorem/) reduces the question to finitely many ground instances, ground resolution refutes those, and the [lifting lemma](/lifting-lemma/) turns each ground step into a first-order step. The theorem is about the rules; [Robinson's resolution](/robinson-resolution/) is a procedure that applies them in a fair order, so it finds a [refutation](/refutation/) of every unsatisfiable set.

## Statement

A clause is a finite set of literals with its variables read universally. A **derivation** from a set $S$ of clauses is a sequence of clauses, each of which is a variant of a clause of $S$, a factor of an earlier clause, or a binary resolvent of two earlier clauses renamed apart. A **refutation** is a derivation that ends in $\square$.

**Theorem (Robinson 1965).** A set $S$ of clauses is unsatisfiable if and only if there is a refutation of $S$.

If $S$ is infinite, the refutation uses finitely many clauses of $S$, so some finite subset of $S$ is unsatisfiable.

**Corollary.** Let $S$ be a finite set of clauses. A procedure that forms all factors and all binary resolvents in a fair order, so that every possible inference is done at some time, derives $\square$ if and only if $S$ is unsatisfiable. So the unsatisfiable finite sets of clauses are recursively enumerable.

## In plain words

Resolution is a short list of simple steps that combine statements of a fixed form. The theorem says that these steps are enough. If the statements contradict each other in any way at all, then some finite list of steps shows the contradiction, by ending with the empty statement. And the steps never show a contradiction that is not there.

The proof first shows that a contradiction among general statements already appears among finitely many of their concrete cases. Then it refutes those concrete cases by an easy argument. Last, it shows that each step on concrete cases is a copy of a step on the general statements.

## Proof

**Soundness.** Each factor is an instance of its clause, and each binary resolvent is true in every model of its parents, as proved on the [resolvent](/resolvent/) page. By induction on the derivation, every clause in it is true in every model of $S$. The clause $\square$ is false in every structure, so if it is derived, $S$ has no model.

**Completeness.** Let $S$ be unsatisfiable. Three steps.

*Step 1 (Herbrand).* By [Herbrand's theorem](/herbrand-theorem/), there is a finite set $G$ of ground instances $C\tau$ of clauses $C \in S$, with $\tau$ mapping the variables of $C$ to ground terms of the [Herbrand universe](/herbrand-universe/), such that $G$ is unsatisfiable as a set of propositional clauses whose atoms are the ground atoms.

*Step 2 (ground completeness).* **Lemma.** If $G$ is a finite unsatisfiable set of ground clauses, then $\square$ can be derived from $G$ by ground binary resolution.

*Proof of the lemma.* Induction on the number $n$ of ground atoms that occur in $G$. If $n = 0$, every clause of $G$ is $\square$, and $G$ is not empty because the empty set of clauses is satisfiable, so $\square \in G$. Let $n \ge 1$ and choose an atom $A$ of $G$. Let

$$G_A = \{ C \setminus \{\lnot A\} : C \in G, \; A \notin C \}, \qquad G_{\lnot A} = \{ C \setminus \{A\} : C \in G, \; \lnot A \notin C \}.$$

The set $G_A$ does not contain $A$, and it is unsatisfiable: if an assignment of its atoms satisfied it, the same assignment with $A$ true would satisfy every clause of $G$, those that contain $A$ through $A$, and the others through $G_A$. In the same way $G_{\lnot A}$ is unsatisfiable. Both have at most $n - 1$ atoms, so by induction each has a refutation.

Take the refutation of $G_A$ and replace each input clause $C \setminus \{\lnot A\}$ by $C$. No step of it resolves on $A$, because $A$ does not occur in $G_A$. So by induction along the derivation, each replayed clause is the old clause $E$ or $E \cup \{\lnot A\}$: if the parents are $E_1 \cup X_1$ and $E_2 \cup X_2$ with $X_i \subseteq \{\lnot A\}$, and the step resolves on an atom $B \ne A$, the new resolvent is the old one plus $X_1 \cup X_2$. The replayed derivation is a derivation from $G$, and it ends in $\square$ or in $\{\lnot A\}$. In the same way $G$ derives $\square$ or $\{A\}$. If either derivation ends in $\square$ we are done; otherwise one more step resolves $\{A\}$ with $\{\lnot A\}$ to $\square$. $\square$

*Step 3 (lifting).* Take the ground refutation $E_1, \ldots, E_m = \square$ from $G$ given by Step 2. We show by induction on $i$ that there is a clause $D_i$, derived from $S$ by binary resolution and factoring, and a substitution $\theta_i$ with $E_i = D_i\theta_i$.

- If $E_i \in G$, then $E_i = C\tau$ for some $C \in S$; take $D_i = C$ and $\theta_i = \tau$.
- If $E_i$ is the resolvent of $E_j$ and $E_k$ with $j, k < i$, then $E_j = D_j \theta_j$ and $E_k = D_k \theta_k$. Rename $D_k$ apart from $D_j$, which changes $\theta_k$ but not $E_k$. By the [lifting lemma](/lifting-lemma/), there are factors $F_j$ of $D_j$ and $F_k$ of $D_k$, where a clause counts as its own factor, and a binary resolvent $R$ of $F_j$ and $F_k$, such that $E_i = R\lambda$ for some $\lambda$. The factors and $R$ are derived from $S$, so take $D_i = R$ and $\theta_i = \lambda$.

For $i = m$ this gives a derived clause $D_m$ with $D_m \theta_m = \square$. A substitution maps a literal to a literal, so $D_m = \square$, and the derivation of $D_m$ is a refutation of $S$. $\blacksquare$

**The corollary.** If $S$ is unsatisfiable, a refutation exists, and its finitely many steps are each done at some time by a fair procedure, up to renaming. If $S$ is satisfiable, soundness forbids $\square$. Enumerating all finite sets of clauses and running the procedure on all of them in turns, one step at a time, lists the unsatisfiable ones.

## Consequences

- **Correctness of resolution provers.** [Robinson's resolution](/robinson-resolution/), with the deletion of tautologies and subsumed clauses, answers UNSAT exactly on unsatisfiable sets; its proof page gives a saturation proof of the same theorem.
- **Proof by refutation.** With [clausal normal form](/clausal-normal-form/), a formula $\varphi$ follows from axioms $\Gamma$ if and only if resolution refutes the clauses of $\Gamma \cup \{\lnot \varphi\}$. This gives a semi-decision procedure for [first-order theorem proving](/first-order-theorem-proving/).
- **Completeness of refinements.** The same three steps, with a sharper ground lemma, prove the completeness of [set of support](/set-of-support/), [hyperresolution](/hyperresolution/), [linear resolution](/linear-resolution/) and [ordered resolution](/ordered-resolution/). Each refinement changes Step 2 and keeps Steps 1 and 3.
- **Compactness for clauses.** A set of clauses with no model has a finite subset with no model, since a refutation uses finitely many input clauses.

## Tightness

- **Factoring is needed.** $\{P(x) \vee P(y), \lnot P(u) \vee \lnot P(v)\}$ is unsatisfiable, but binary resolution alone derives only clauses with two literals; the proof is on the [factoring](/factoring/) page. Step 3 fails there because a ground instance such as $P(a) \vee P(a)$ is the one-literal clause $P(a)$, and only a factor of the first-order clause has it as an instance.
- **Renaming apart is needed.** $\{P(x), \lnot P(f(x))\}$ is unsatisfiable, but without renaming apart, $P(x)$ and $P(f(x))$ do not unify. The lifting lemma needs parents with disjoint variables.
- **Most general unifiers are needed in the lemma, not in the theorem.** Resolution with any unifier is still sound, but if the rule uses only some unifiers, a step of Step 3 may have no lifted copy; the lifting lemma needs the mgu to cover every ground instance.
- **Refutation completeness, not deductive completeness.** From $\{P\}$ no step applies, although $P$ implies $P \vee Q$. Only unsatisfiability is detected; to prove a consequence, negate it first.
- **No decision procedure.** On a satisfiable set the search can go on forever: from $\{P(a), \lnot P(x) \vee P(f(x))\}$ resolution derives $P(f(a))$, $P(f(f(a)))$ and so on, with no end. No other method can do better in general, because unsatisfiability of clause sets is undecidable; see [first-order theorem proving](/first-order-theorem-proving/).
- **No short refutations in general.** Completeness says nothing about length. Ground pigeonhole clauses have refutations, but all of them are exponentially long, by the [Haken lower bound](/haken-resolution-lower-bound/).

## History

Herbrand's 1930 thesis reduced first-order provability to propositional questions about ground instances. Gilmore in 1960 and Davis and Putnam in 1960 built provers that generate ground instances level by level and test them, and the instances grew too fast. Robinson's 1965 paper introduced unification and the resolution principle, which works on clauses with variables and instantiates them only as much as a step needs. His completeness proof is the lifting argument above, built on Herbrand's theorem. The textbook of Chang and Lee proves it with semantic trees, and Bachmair and Ganzinger later gave a proof by a model construction for saturated sets, which also covers ordered resolution and [superposition](/superposition/).

## References
