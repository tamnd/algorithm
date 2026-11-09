---
tag: A3C2MV
kind: definition
slug: clause
name: Clause
aliases:
- disjunction of literals
- propositional clause
area: logic-and-constraints/sat-solving
level: intro
summary: A finite set of literals read as their disjunction. It is true when one of its literals is true. Clauses are the units of CNF, of resolution and of SAT solvers.
prereqs: [literal]
see_also: [conjunctive-normal-form, unit-clause, binary-resolution, clause-subsumption, horn-clause, clause-learning, sat, dimacs-cnf-format]
sources:
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability, the opening definitions (clauses as sets of literals, the empty clause, and the problem of satisfying a set of clauses)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, 2016
    locator: Chapter 1, Section 1.3 (normal forms), and Chapter 2, Section 2.2 (clauses under a partial assignment, unit and conflicting clauses)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik, the preliminaries (satisfied, falsified, unit and unresolved clauses)
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: pages 23 to 41 (clauses as sets of literals, the empty clause, and the resolution rule)
---

A clause is a finite set of [literals](/literal/), read as their disjunction: the clause $\{x_1, \neg x_2, x_3\}$ means $x_1 \vee \neg x_2 \vee x_3$, and it is true when at least one of its literals is true. A formula in [conjunctive normal form](/conjunctive-normal-form/) is a set of clauses, so clauses are the units that SAT solvers store, propagate and learn, and that [resolution](/binary-resolution/) combines. The empty clause has no true literal under any assignment, so it stands for false.

## Definition

Fix the variables $x_1, \ldots, x_n$.

**Clause.** A clause $C$ is a finite set of literals over these variables. It denotes the disjunction $\bigvee_{\ell \in C} \ell$. Its *width* or *length* is $|C|$. The empty clause is written $\bot$ or $\square$. A clause with one literal is a unit clause in the static sense, with two a binary clause, with three a ternary clause.

**Tautology.** A clause that holds a literal and its complement is a tautology. It is true under every assignment, so solvers and resolution procedures remove it.

**Truth under a total assignment.** An assignment $\alpha$ satisfies $C$ when $\alpha(\ell) = 1$ for some $\ell \in C$. If $C$ is not a tautology and has $k$ literals, exactly $2^{n-k}$ of the $2^n$ assignments falsify it: those that make each of its literals false.

**Status under a partial assignment.** Under a partial assignment $\tau$, a clause is

- *satisfied* if some literal of $C$ is true;
- *falsified*, or *conflicting*, if every literal of $C$ is false;
- *unit* if it is not satisfied and exactly one literal is unassigned, see [unit clause](/unit-clause/);
- *unresolved* otherwise: not satisfied, with at least two unassigned literals.

**Clause and forbidden assignment.** A clause $C$ that is not a tautology is false exactly on the assignments that extend $\{\bar\ell : \ell \in C\}$. So a clause is the same as a forbidden partial assignment, which is why [nogood learning](/nogood-learning/) in constraint solvers and [clause learning](/clause-learning/) in SAT solvers are one idea.

**Subsumption.** A clause $C$ subsumes a clause $D$ when $C \subseteq D$. Then every model of $C$ is a model of $D$, and $D$ can be removed from a formula that contains $C$, see [clause subsumption](/clause-subsumption/).

**Resolvent.** For clauses $C \ni x$ and $D \ni \neg x$, the resolvent on $x$ is $(C \setminus \{x\}) \cup (D \setminus \{\neg x\})$. Every assignment that satisfies $C$ and $D$ satisfies it. The propositional rule is the ground case of [binary resolution](/binary-resolution/).

## Examples and non-examples

Let $C = \{x_1, \neg x_2, x_3\}$ with $n = 3$. It is false only under $x_1 = 0, x_2 = 1, x_3 = 0$, so 7 of the 8 assignments satisfy it, which is $2^3 - 2^{3-3}$. Its status under some partial assignments:

| partial assignment $\tau$ | status of $C$ | reason |
|---|---|---|
| $\{x_3\}$ | satisfied | $x_3$ is true |
| $\{x_2\}$ | unresolved | $x_1$ and $x_3$ are unassigned |
| $\{\neg x_1, x_2\}$ | unit | only $x_3$ is left, so it is forced |
| $\{\neg x_1, x_2, \neg x_3\}$ | falsified | all three literals are false |
| $\emptyset$ | unresolved | nothing is assigned |

Other cases:

- $\{x_4\}$ is a clause of width 1. As part of a formula it forces $x_4$ to be true.
- $\{x_1, \neg x_1, x_2\}$ is a clause, but a tautology, true under all 8 assignments.
- $\emptyset$ is the empty clause. A formula that holds it is unsatisfiable, and deriving it by resolution refutes a formula.
- The resolvent of $\{x_1, x_2\}$ and $\{\neg x_1, x_3\}$ on $x_1$ is $\{x_2, x_3\}$. The resolvent of $\{x_1, x_2\}$ and $\{\neg x_1, \neg x_2\}$ on $x_1$ is the tautology $\{x_2, \neg x_2\}$, which tells nothing.
- $x_1 \wedge \neg x_2$ is not a clause: it is a conjunction, which is the CNF $\{x_1\}, \{\neg x_2\}$ of two unit clauses.
- $(x_1 \wedge x_2) \vee x_3$ is not a clause. Its CNF is $\{x_1, x_3\}, \{x_2, x_3\}$.
- A list such as $[x_1, x_1, x_2]$ with a repeated literal is not a set. It denotes the clause $\{x_1, x_2\}$, and code must remove the repeat, because a repeated literal breaks the watch scheme of [two watched literals](/two-watched-literals/).

## Related definitions

- **[Literal](/literal/).** The elements of a clause.
- **[Conjunctive normal form](/conjunctive-normal-form/).** A conjunction of clauses.
- **[Unit clause](/unit-clause/).** A clause with exactly one literal that is not false under the current assignment, the trigger of [unit propagation](/unit-propagation/).
- **[Horn clause](/horn-clause/).** At most one positive literal; satisfiability of a set of Horn clauses is decided in linear time by [Horn-SAT](/horn-sat/).
- **Learned clause.** A clause implied by the formula and added by a solver after a conflict, see [clause learning](/clause-learning/).
- **[DIMACS CNF format](/dimacs-cnf-format/).** The text form of a clause: its literals as signed integers, ended by 0.
- **Clause in first-order logic.** A set of first-order literals with free variables read as universally quantified, see [clausal normal form](/clausal-normal-form/).

## References
