---
tag: KW61N9
kind: concept
slug: refutation
name: Refutation
aliases:
- proof by refutation
- refutation proof
- resolution refutation
area: logic-and-constraints/unification-and-resolution
level: intro
summary: A derivation of the empty clause from a set of clauses with sound rules, which shows that the set has no model. To prove a goal, refute the axioms together with the negated goal.
prereqs: [clause, sat]
see_also: [resolvent, robinson-resolution, robinson-completeness-theorem, first-order-theorem-proving, sld-resolution, answer-substitution, haken-resolution-lower-bound, cdcl-simulates-resolution]
sources:
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: the resolution principle as a refutation method, and the theorem that a finite set of clauses is unsatisfiable exactly when the empty clause can be derived from it
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 5, The resolution principle (deductions, refutations, and the completeness of resolution), and Chapter 4, Section 4.2 (why the proof procedures are refutation procedures)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (refutational completeness of saturation)
---

A **refutation** of a set $S$ of [clauses](/clause/) is a finite derivation of the empty clause $\square$ from $S$, in which each new clause follows from earlier ones by a sound rule such as taking a [resolvent](/resolvent/). Since $\square$ is false in every structure, a refutation shows that $S$ has no model. **Proof by refutation** uses this to prove a goal: to show that axioms $\Gamma$ imply $\varphi$, refute $\Gamma \cup \{\lnot\varphi\}$. A resolvent is one step; a refutation is a whole derivation that ends in $\square$.

## In plain words

To show that something must be true, assume that it is false and look for a contradiction. If the rules plus the assumption "it is false" lead to nonsense, then the assumption cannot hold together with the rules, so the thing is true whenever the rules are.

A theorem prover does the same in a fixed form. It writes the rules and the denied goal as a list of simple "or" statements. Then it combines two statements at a time into a new one that must also hold. When it produces the empty statement, which can never hold, it has found the contradiction. The list of steps that led there is the refutation, and anyone can check it one step at a time.

## The idea

**Consequence as unsatisfiability.** For a set $\Gamma$ of closed formulas and a closed formula $\varphi$,

$$\Gamma \models \varphi \iff \Gamma \cup \{\lnot \varphi\} \text{ is unsatisfiable}.$$

If every model of $\Gamma$ satisfies $\varphi$, no model of $\Gamma$ satisfies $\lnot\varphi$. If no structure satisfies $\Gamma$ and $\lnot\varphi$ together, then every model of $\Gamma$ makes $\lnot\varphi$ false, so it makes $\varphi$ true. The [clausal normal form](/clausal-normal-form/) then turns $\Gamma \cup \{\lnot\varphi\}$ into an equisatisfiable set of clauses $S$.

**Derivations.** A derivation from $S$ is a sequence $C_1, \ldots, C_m$ in which each $C_i$ is in $S$ or follows by a rule from earlier clauses. It is a refutation if $C_m = \square$. With [binary resolution](/binary-resolution/) and [factoring](/factoring/) every rule is sound, so each $C_i$ is true in every model of $S$, and $C_m = \square$ means that $S$ has no model. A derivation is usually drawn as a directed acyclic graph, or as a tree when shared clauses are copied.

**Two kinds of completeness.** An inference system is **refutation complete** if every unsatisfiable set of clauses has a refutation. Resolution with factoring is refutation complete by the [Robinson completeness theorem](/robinson-completeness-theorem/). It is **not deductively complete**: it does not derive every consequence. From $\{P\}$ no rule applies, although $P \models P \vee Q$. Refutation covers this: to prove $P \vee Q$ from $P$, refute $\{P, \lnot P, \lnot Q\}$, which takes one step.

**Search.** A refutation exists or not, but finding it is a search problem. A prover saturates the clause set under the rules, often with a restriction such as [set of support](/set-of-support/) or an [ordering](/ordered-resolution/), and stops when $\square$ appears. For first-order clauses the search may run forever on a satisfiable set, since [first-order theorem proving](/first-order-theorem-proving/) is undecidable.

**Size.** The length of the shortest refutation is a measure of difficulty. For propositional clauses, resolution refutations of the pigeonhole formulas need exponential length, by the [Haken lower bound](/haken-resolution-lower-bound/).

## Examples

**A first-order goal.** From "every man is mortal" and "Socrates is a man", prove "Socrates is mortal". The clauses of the axioms and of the negated goal are

$$1: \lnot \mathit{Man}(x) \vee \mathit{Mortal}(x), \quad 2: \mathit{Man}(s), \quad 3: \lnot \mathit{Mortal}(s).$$

Resolving 1 and 3 with $x \mapsto s$ gives $4: \lnot \mathit{Man}(s)$. Resolving 4 and 2 gives $5: \square$. The refutation is $1, 2, 3, 4, 5$.

**A propositional set.** The four clauses $P \vee Q$, $\lnot P \vee Q$, $P \vee \lnot Q$, $\lnot P \vee \lnot Q$ exclude all four assignments of $P$ and $Q$. A refutation: $Q$ from the first two, $\lnot Q$ from the last two, then $\square$. It has 3 steps, and none shorter exists: $\square$ needs two complementary unit parents, the input has no unit clause, and each step makes one clause, so two steps must come before the step that gives $\square$.

**An answer.** With $\mathit{Par}(a, b)$, $\mathit{Par}(b, c)$ and $\lnot \mathit{Par}(x, y) \vee \lnot \mathit{Par}(y, z) \vee \mathit{Gp}(x, z)$, the goal $\exists w \, \mathit{Gp}(a, w)$ is negated to $\lnot \mathit{Gp}(a, w)$. Resolving it with the rule ($x \mapsto a$, $z \mapsto w$) gives $\lnot \mathit{Par}(a, y) \vee \lnot \mathit{Par}(y, w)$. Then $\mathit{Par}(a, b)$ binds $y \mapsto b$ and leaves $\lnot \mathit{Par}(b, w)$, and $\mathit{Par}(b, c)$ binds $w \mapsto c$ and gives $\square$. The binding of the goal variable $w$ is the answer $c$; see [answer substitution](/answer-substitution/).

**Not a refutation.** Resolving $P \vee Q$ and $\lnot P \vee \lnot Q$ on both pairs at once would give $\square$, but the two clauses are satisfied by $P$ true and $Q$ false. That step is not sound, so the sequence is not a refutation. [Binary resolution](/binary-resolution/) removes exactly one pair.

## Where it is used

- **Resolution and superposition provers.** [Robinson's resolution](/robinson-resolution/), [ordered resolution](/ordered-resolution/) and [superposition](/superposition/) search for refutations of the clausal form of the axioms plus the negated goal, and print the refutation as the proof.
- **Logic programming.** An [SLD resolution](/sld-resolution/) derivation that ends in the empty goal is a refutation of the program plus the negated query, and its unifiers give the answer.
- **SAT solvers.** An UNSAT answer of [CDCL](/cdcl/) can be turned into a resolution refutation of the input, and [CDCL can simulate resolution](/cdcl-simulates-resolution/). Proof checkers accept such certificates in place of trust in the solver.
- **Proof complexity.** The minimum size of a refutation in a proof system measures the hardness of a formula, as in the [Haken lower bound](/haken-resolution-lower-bound/).

## References
