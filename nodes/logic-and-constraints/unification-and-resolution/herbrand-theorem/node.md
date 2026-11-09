---
tag: QGMANS
kind: theorem
slug: herbrand-theorem
name: Herbrand's theorem
aliases:
- Herbrand theorem
- Skolem-Herbrand-Gödel theorem
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: A set of clauses is unsatisfiable if and only if some finite set of its ground instances over the Herbrand universe is propositionally unsatisfiable. This reduces refutation to SAT problems.
prereqs: [herbrand-universe, clausal-normal-form, skolemization]
see_also: [herbrand-universe, robinson-completeness-theorem, first-order-theorem-proving, skolemization, sat, quantifier-instantiation, davis-putnam-elimination, lifting-lemma]
sources:
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 4, Herbrand's theorem (Section 4.3 on the Herbrand universe, Section 4.4 on semantic trees, Section 4.5 on Herbrand's theorem, Section 4.6 on its implementation by Gilmore)
  - paper: "Jacques Herbrand, Recherches sur la théorie de la démonstration, thesis, University of Paris, 1930"
    locator: the fundamental theorem, which reduces first-order provability to the truth-functional validity of a finite disjunction of instances
  - paper: "Paul C. Gilmore, A proof method for quantification theory: its justification and realization, IBM Journal of Research and Development 4(1), 1960"
    locator: a program that generates ground instances level by level and tests them for propositional unsatisfiability
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (Herbrand interpretations and the reduction to ground clauses)
---

**Herbrand's theorem**, in the form used in automated reasoning, says that a set $S$ of first-order [clauses](/clause/) is unsatisfiable if and only if some finite set of ground instances of its clauses, with variables replaced by terms of the [Herbrand universe](/herbrand-universe/), is unsatisfiable as a set of propositional clauses. It reduces a question about all structures to a sequence of propositional problems, each of which a [SAT](/sat/) solver can decide. Together with [Skolemization](/skolemization/) and [clausal normal form](/clausal-normal-form/), it gives a semi-decision procedure for first-order validity, and it is Step 1 in the proof of the [Robinson completeness theorem](/robinson-completeness-theorem/).

## Statement

Let $S$ be a set of clauses over a countable signature, with variables read universally. A ground instance of $C \in S$ is $C\tau$ with $\tau$ mapping the variables of $C$ into the Herbrand universe $H(S)$. A set of ground clauses is **propositionally unsatisfiable** if no assignment of truth values to the ground atoms makes every clause true.

**Theorem (Herbrand).** $S$ is unsatisfiable if and only if there is a finite set $G$ of ground instances of clauses of $S$ that is propositionally unsatisfiable.

**Validity form.** Let $\varphi$ be a closed formula and let $\forall \vec x \, M(\vec x)$ be a Skolem form of $\lnot \varphi$, with $M$ quantifier-free. Then $\varphi$ is valid if and only if there are finitely many tuples $\vec t_1, \ldots, \vec t_k$ of ground terms such that $\lnot M(\vec t_1) \vee \cdots \vee \lnot M(\vec t_k)$ is a propositional tautology. This follows from the theorem applied to the clauses of $M$, since $\varphi$ is valid iff $\lnot\varphi$ is unsatisfiable iff its Skolem form is.

## In plain words

A set of general rules, such as "every number has a successor", talks about infinitely many things. To show that the rules contradict each other, it would seem that one must look at every possible world.

Herbrand's theorem says that this is not needed. Build the names that the rules themselves can make, such as "zero", "the successor of zero", and so on. Fill those names into the rules in all ways. If the rules contradict each other at all, then some finite list of these filled-in copies already contradicts itself as plain true-or-false statements. So a computer can try more and more copies and check each batch like a puzzle of switches.

## Proof

**If.** Every ground instance $C\tau$ is true in every model of $C$, because the variables of $C$ are universally quantified. So a model of $S$ would satisfy $G$, read as a structure, and the truth values it gives the ground atoms would satisfy $G$ propositionally. Since $G$ has no such assignment, $S$ has no model.

**Only if.** Suppose every finite set of ground instances is propositionally satisfiable. We build a model of $S$. Let $\mathcal{G}$ be the set of all ground instances of clauses of $S$. The signature is countable, so the ground atoms can be listed as $A_1, A_2, A_3, \ldots$.

*Compactness for $\mathcal{G}$.* Call a truth assignment $v$ of $A_1, \ldots, A_n$ **good** if every finite $F \subseteq \mathcal{G}$ has a satisfying assignment that agrees with $v$ on $A_1, \ldots, A_n$. The empty assignment ($n = 0$) is good by assumption. Let $v$ be good on $A_1, \ldots, A_n$, and let $v^+$ and $v^-$ extend it with $A_{n+1}$ true and false. Suppose neither is good: there are finite $F^+$ and $F^-$ such that no satisfying assignment of $F^+$ extends $v^+$ and none of $F^-$ extends $v^-$. Since $v$ is good, the finite set $F^+ \cup F^-$ has a satisfying assignment $w$ that extends $v$. Then $w$ extends $v^+$ or $v^-$, and it satisfies both $F^+$ and $F^-$, a contradiction. So one extension is good, and we choose it. This defines good assignments $v_0 \subseteq v_1 \subseteq v_2 \subseteq \cdots$, and their union $v$ assigns every atom.

Let $C \in \mathcal{G}$. Its finitely many atoms are among $A_1, \ldots, A_n$ for some $n$. Since $v_n$ is good, $\{C\}$ has a satisfying assignment that agrees with $v_n$, and so with $v$, on all atoms of $C$. The truth of $C$ depends only on these atoms, so $v$ satisfies $C$. Thus $v$ satisfies all of $\mathcal{G}$.

*From $v$ to a model.* Let $I$ be the Herbrand interpretation in which a ground atom is true exactly when $v$ makes it true. It satisfies every ground instance of every clause of $S$, so by Proposition 1 on the [Herbrand universe](/herbrand-universe/) page, $I$ satisfies $S$. This contradicts the unsatisfiability of $S$. $\blacksquare$

If the signature has no constant, $H(S)$ uses one new constant, as in the definition of the universe, and the proof is the same.

## Consequences

- **Semi-decidability.** Let $G_d$ be the instances over the terms of depth at most $d$. For a finite $S$ each $G_d$ is finite, so testing $d = 0, 1, 2, \ldots$ by truth tables halts exactly on unsatisfiable $S$. This is Gilmore's 1960 method, and it shows that [first-order theorem proving](/first-order-theorem-proving/) is semi-decidable.
- **Completeness of resolution.** Ground resolution refutes the finite set $G$, and the [lifting lemma](/lifting-lemma/) turns the refutation into one from $S$; see the [Robinson completeness theorem](/robinson-completeness-theorem/).
- **Decidable classes.** If $S$ has no function symbols of arity at least 1, $H(S)$ is finite, $\mathcal{G}$ is finite, and one SAT test decides $S$. This decides the Bernays-Schönfinkel class $\exists^* \forall^*$ without function symbols.
- **Instance-based methods.** Davis and Putnam's 1960 procedure, the origin of [Davis-Putnam elimination](/davis-putnam-elimination/), and the [quantifier instantiation](/quantifier-instantiation/) of SMT solvers generate ground instances and pass them to a propositional solver.
- **Compactness for clause sets.** A set of clauses with no model has a finite subset with no model: the clauses that $G$ comes from.

## Tightness

- **No computable bound on the instances.** There is no computable function $b$ such that every unsatisfiable finite $S$ of size $n$ has an unsatisfiable $G_{b(n)}$. With such a $b$, testing $G_{b(n)}$ alone would decide unsatisfiability, which is undecidable by Church and Turing; see [first-order theorem proving](/first-order-theorem-proving/).
- **The number of instances grows with the problem.** Let $S_n = \{P(a), \lnot P(x) \vee P(f(x)), \lnot P(f^n(a))\}$. Every unsatisfiable set of ground instances contains $P(a)$, $\lnot P(f^n(a))$ and all $n$ links $\lnot P(f^i(a)) \vee P(f^{i+1}(a))$ for $0 \le i < n$: if link $i$ is missing, the assignment that makes $P(f^j(a))$ true exactly for $j \le i$ satisfies all other instances. So the least such set has $n + 2$ clauses and needs terms up to depth $n - 1$. For $n = 2$, the 3 instances at depth 0 are satisfiable and the 4 at depth 1 are not.
- **Clauses, not arbitrary formulas.** $\{\lnot P(a), \exists x \, P(x)\}$ is satisfiable, but the only ground term is $a$, and the "instance" $P(a)$ contradicts $\lnot P(a)$. Existential quantifiers must first be replaced by Skolem terms: $\{\lnot P(a), P(c)\}$ has no contradiction.
- **Equality.** If $=$ means identity, ground instances alone are not enough: $\{a = b, P(a), \lnot P(b)\}$ is unsatisfiable, but propositionally the three ground atoms are independent. Add the ground instances of the equality axioms, or use [paramodulation](/paramodulation/).
- **Satisfiable sets.** For a satisfiable $S$ with an infinite universe, every $G_d$ is satisfiable, and no finite stage proves this. The direction "every finite set is satisfiable" cannot be checked in finite time in general.

## History

Herbrand's 1930 thesis proved a theorem about formal provability: a formula is provable if and only if a certain finite disjunction of instances of a quantifier-free form is a tautology. The semantic form on this page, with Herbrand interpretations and compactness, is the one in Chang and Lee's Chapter 4, which proves it with semantic trees; it is close to the work of Skolem in the 1920s and to Gödel's completeness proof of 1930. In 1960 Gilmore programmed the level-by-level search, and Davis and Putnam improved the propositional test. Both suffered from the growth of the levels, and Robinson's 1965 resolution with unification replaced blind instantiation by instantiation on demand.

## References
