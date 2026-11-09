---
tag: NHXWTD
kind: concept
slug: unit-clause
name: Unit clause
aliases:
- unit
- unit rule
- one-literal clause
area: logic-and-constraints/sat-solving
level: intro
summary: A clause with exactly one unassigned literal under the current assignment, all others false. That literal is forced. Unit clauses drive unit propagation.
prereqs: [clause]
see_also: [unit-propagation, unit-resolution, two-watched-literals, dpll, cdcl, horn-sat, first-uip, failed-literal-probing]
sources:
  - paper: doi:10.1145/321033.321034
    title: Martin Davis and Hilary Putnam, A computing procedure for quantification theory, Journal of the ACM 7(3), 1960
    locator: pages 201 to 215 (the rule for eliminating one-literal clauses)
  - paper: doi:10.1145/368273.368557
    title: Martin Davis, George Logemann and Donald Loveland, A machine program for theorem-proving, Communications of the ACM 5(7), 1962
    locator: pages 394 to 397 (the one-literal clause rule in the search procedure)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik, the preliminaries (unit clause rule, unit propagation and reasons)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, 2016
    locator: Chapter 2, Section 2.2 (unit clauses, the unit clause rule and the antecedent of an implied literal)
---

A unit clause is a [clause](/clause/) that has exactly one literal that is not false under the current partial assignment, while that literal is unassigned and all other literals are false. Every model that extends the assignment must make the remaining literal true, so a solver assigns it at once; this step is the unit rule, and its repeated use is [unit propagation](/unit-propagation/). In the static sense, a unit clause is a clause of length one, such as $\{x_4\}$, which is unit under the empty assignment.

## In plain words

A rule says "at least one of these must hold". If all but one of its options are already ruled out, and the last one is still open, the last one must hold. There is no choice left. Such a rule is a unit clause.

SAT solvers look for these rules all the time. Each time they set one value, some rules may drop to one open option, and those force new values, which may force more. This chain of forced values is what makes a solver fast: most values in a run are forced, not guessed. When all the options of a rule are ruled out, the solver has hit a dead end and must go back.

## The idea

Let $\tau$ be a partial assignment and $C$ a clause. Then $C$ is *unit under $\tau$ with the literal $\ell$* when $\ell \in C$ is unassigned and every other literal of $C$ is false under $\tau$.

**The unit rule.** If $C \in F$ is unit under $\tau$ with $\ell$, then every model of $F$ that extends $\tau$ makes $\ell$ true. *Proof.* Such a model satisfies $C$, and it makes every literal of $C$ other than $\ell$ false, because it extends $\tau$. So it makes $\ell$ true. $\blacksquare$

So adding $\ell$ to $\tau$ loses no model. The clause $C$ is the *reason*, or antecedent, of $\ell$, and solvers record it: [conflict analysis](/clause-learning/) reads the reasons as the edges of the [implication graph](/implication-graph/).

**Unit rule as resolution.** The unit rule is a sequence of [unit resolution](/unit-resolution/) steps: resolving $C$ with the unit clauses $\{\bar q\}$ for its false literals $q \ne \ell$ leaves $\{\ell\}$. So a literal forced by the rule is implied by $F$ together with the unit clauses of $\tau$, and it has a short resolution proof.

**Static and dynamic units.** A clause of length one in the input is unit under the empty assignment. Its literal holds in every model, and solvers assign it at decision level 0, before any decision. The dynamic notion depends on $\tau$ and changes during the search: a clause becomes unit when the second-to-last of its open literals turns false, and it stops being unit when the solver backtracks over one of its false literals or when its last literal is assigned.

**The four states of a clause.** Under $\tau$, a clause is satisfied, falsified (a conflict), unit, or unresolved, as defined on the [clause](/clause/) page. A solver must notice the moment a clause turns unit or falsified. The [two watched literals](/two-watched-literals/) scheme notices it by watching two literals that are not false: a clause can turn unit or false only when one of its watches turns false.

**Units after a conflict.** A clause learned by [first UIP](/first-uip/) learning has one literal at the conflict level, and all its literals are false at the conflict. After the backjump to the second highest level of its literals, it is unit, and the solver asserts its UIP literal. A learned clause of length one forces its literal at level 0.

## Examples

Let $F$ have the clauses $C_1 = \{\neg x_1, x_2\}$, $C_2 = \{\neg x_2, x_3\}$, $C_3 = \{\neg x_3, \neg x_1, x_4\}$ and $C_4 = \{x_5\}$.

| partial assignment $\tau$ | unit clauses | forced literals |
|---|---|---|
| $\emptyset$ | $C_4$ | $x_5$ |
| $\{x_5, x_1\}$ | $C_1$ | $x_2$ |
| $\{x_5, x_1, x_2\}$ | $C_2$ | $x_3$ |
| $\{x_5, x_1, x_2, x_3\}$ | $C_3$ | $x_4$ |
| $\{x_5, \neg x_1\}$ | none | none; $C_1$ and $C_3$ are satisfied by $\neg x_1$ |
| $\{x_5, x_1, \neg x_4\}$ | $C_1$ and $C_3$ | $x_2$ and $\neg x_3$; then $C_2 = \{\neg x_2, x_3\}$ is false |

The last row shows how unit clauses lead to a conflict: two clauses are unit at once, and their forced literals together make a third clause false. A solver that assigns $x_2$ first then finds $C_2$ unit with $x_3$ and $C_3$ false; one that assigns $\neg x_3$ first finds $C_2$ unit with $\neg x_2$ and $C_1$ false. Either way it reports a conflict.

Non-examples:

- $\{x_1, x_2\}$ under $\emptyset$ is not unit: two literals are open.
- $\{x_1, x_2\}$ under $\{x_2\}$ is not unit: it is satisfied, although only one literal is open.
- $\{x_1, x_2\}$ under $\{\neg x_1, \neg x_2\}$ is not unit: no literal is open, so the clause is false.
- A clause with a repeated literal, as the list $[x_1, x_1, x_2]$ under $\{\neg x_2\}$, has one open literal but two open positions. Code that counts positions instead of distinct literals misses that it is unit.

## Where it is used

- **[Unit propagation](/unit-propagation/).** Repeated use of the unit rule until no clause is unit or some clause is false. It is the main inference step of [DPLL](/dpll/) and [CDCL](/cdcl/), and takes most of their running time.
- **[DPLL](/dpll/) and [Davis-Putnam elimination](/davis-putnam-elimination/).** Both have the one-literal clause rule of Davis and Putnam (1960).
- **[Horn-SAT](/horn-sat/).** For Horn formulas, unit propagation alone decides satisfiability: if it ends without a conflict, setting every open variable to false gives a model.
- **[2-SAT](/2-sat/).** In a 2-CNF, setting a literal and propagating either reaches a conflict or satisfies every clause that it touches, so the assignment can be kept. Even, Itai and Shamir built a polynomial algorithm on this.
- **[Failed literal probing](/failed-literal-probing/).** Assign a literal, propagate, and if a conflict comes, the complement is implied and can be added as a unit clause.
- **Encodings.** A CNF encoding of a constraint is called propagation complete when unit propagation on it derives every implied literal; [cardinality encodings](/sequential-counter-encoding/) are designed for this.

## References
