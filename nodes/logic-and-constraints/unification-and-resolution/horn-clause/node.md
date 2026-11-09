---
tag: 034J5V
kind: definition
slug: horn-clause
name: Horn clause
aliases:
- Horn clauses
- Horn formula
area: logic-and-constraints/unification-and-resolution
level: intro
summary: A clause with at most one positive literal. Definite clauses (facts and rules) have exactly one, and goal clauses have none. Sets of definite clauses always have a least Herbrand model.
prereqs: [clause, literal, conjunctive-normal-form]
see_also: [logic-programming, sld-resolution, horn-sat, horn-sat-forward-chaining, datalog, herbrand-universe, unit-resolution, input-resolution]
sources:
  - paper: doi:10.2307/2268661
    title: Alfred Horn, On sentences which are true of direct unions of algebras, Journal of Symbolic Logic 16(1), 14 to 21 (1951)
    locator: the class of sentences, later called Horn sentences, that are preserved under direct products
  - book: isbn:9783540181996
    title: John W. Lloyd, Foundations of Logic Programming, second edition, Springer (1987)
    locator: Chapter 1, Sections 2 to 6 (clauses, definite programs and goals, the model intersection property and the least Herbrand model)
  - paper: doi:10.1145/321978.321991
    title: Maarten H. van Emden and Robert A. Kowalski, The semantics of predicate logic as a programming language, Journal of the ACM 23(4), 733 to 742 (1976)
    locator: Horn clauses as programs and the minimal model semantics
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)
    locator: the linear-time satisfiability test for propositional Horn formulas
---

A Horn clause is a [clause](/clause/), a disjunction of [literals](/literal/), that contains at most one positive literal. Written as an implication, it says that one atom follows from a conjunction of atoms, or that a conjunction of atoms is false. Horn clauses are the clauses of [logic programming](/logic-programming/) and of [Datalog](/datalog/). They have two properties that general clauses lack: each satisfiable set of Horn clauses has a least model, and their propositional satisfiability problem, [Horn-SAT](/horn-sat/), is solvable in linear time. The name honours Alfred Horn, who studied the corresponding class of first-order sentences in 1951.

## Definition

An *atom* is $p(t_1, \ldots, t_n)$ for a predicate symbol $p$ and terms $t_i$. A *literal* is an atom $A$ or its negation $\neg A$. A *clause* is a finite disjunction of literals, read with all its variables universally quantified.

A *Horn clause* is a clause with at most one positive literal. There are three kinds:

| kind | literals | implication form | logic programming name |
|---|---|---|---|
| definite clause, $m \ge 1$ | $A \vee \neg B_1 \vee \cdots \vee \neg B_m$ | $A \leftarrow B_1 \wedge \cdots \wedge B_m$ | rule |
| definite clause, $m = 0$ | $A$ | $A \leftarrow$ | fact (unit clause) |
| goal clause, $m \ge 1$ | $\neg B_1 \vee \cdots \vee \neg B_m$ | $\leftarrow B_1 \wedge \cdots \wedge B_m$ | query, or negative clause |

The empty clause $\square$, with no literals, is also a Horn clause; it stands for false. In a definite clause $A \leftarrow B_1, \ldots, B_m$, the atom $A$ is the *head* and $B_1, \ldots, B_m$ is the *body*. A *definite program* is a finite set of definite clauses. A *Horn formula* is a conjunction of Horn clauses.

**The least model.** For a definite program $P$, the set of ground atoms true in every Herbrand model of $P$ is itself a Herbrand model, the *least Herbrand model* $M_P$. It is the least fixed point of the immediate consequence operator $T_P$ (van Emden and Kowalski 1976; the proof is on the [SLD resolution](/sld-resolution/) page). A ground atom $A$ is a logical consequence of $P$ if and only if $A \in M_P$. A set of Horn clauses with goal clauses is satisfiable if and only if no goal clause has all its atoms, in some ground instance, in $M_P$ of its definite part.

## Examples and non-examples

- $\mathit{ancestor}(X, Y) \vee \neg \mathit{parent}(X, Y)$ is a definite clause: $\mathit{ancestor}(X, Y) \leftarrow \mathit{parent}(X, Y)$.
- $\mathit{ancestor}(X, Y) \vee \neg \mathit{parent}(X, Z) \vee \neg \mathit{ancestor}(Z, Y)$ is a definite clause with two body atoms.
- $\mathit{parent}(\mathit{ann}, \mathit{bob})$ is a fact.
- $\neg \mathit{ancestor}(\mathit{ann}, W)$ is a goal clause. It is the negation of the query "is Ann an ancestor of someone?". Refuting it, together with the program, answers the query with a value for $W$.
- $\neg p \vee \neg q$ is a Horn clause with no positive literal. It says that $p$ and $q$ are not both true.
- $p \vee q$ is **not** a Horn clause: it has two positive literals. The set $\{p \vee q\}$ has the models $\{p\}$ and $\{q\}$, and neither is contained in the other, so it has no least model. This is the property that Horn clauses guarantee.
- $p \leftarrow \neg q$, written as the clause $p \vee q$, is not Horn either. In logic programming, $p \leftarrow \mathit{not}\ q$ is a *normal* clause, where $\mathit{not}$ is negation as failure and not classical negation; see [SLDNF resolution](/sldnf-resolution/).
- $\neg p \vee q \vee r$ is not Horn. After renaming $q$ to $\neg q'$, it becomes $\neg p \vee \neg q' \vee r$, which is Horn. A set of clauses that becomes Horn after a consistent renaming of some atoms is *renamable Horn*.

A worked least model: the program $\mathit{parent}(\mathit{ann}, \mathit{bob})$, $\mathit{parent}(\mathit{bob}, \mathit{cal})$, $\mathit{ancestor}(X, Y) \leftarrow \mathit{parent}(X, Y)$, $\mathit{ancestor}(X, Y) \leftarrow \mathit{parent}(X, Z), \mathit{ancestor}(Z, Y)$ has $M_P$ with the 2 parent facts and the 3 atoms $\mathit{ancestor}(\mathit{ann}, \mathit{bob})$, $\mathit{ancestor}(\mathit{bob}, \mathit{cal})$ and $\mathit{ancestor}(\mathit{ann}, \mathit{cal})$. The iteration of $T_P$ from the empty set reaches it in 3 steps, with 2, 4 and 5 atoms. Adding the goal clause $\leftarrow \mathit{ancestor}(\mathit{cal}, Y)$ keeps the set satisfiable, since no atom $\mathit{ancestor}(\mathit{cal}, \cdot)$ is in $M_P$. Adding $\leftarrow \mathit{ancestor}(\mathit{ann}, Y)$ makes it unsatisfiable.

## Related definitions

- **Definite program and goal.** A set of definite clauses, and a goal clause to refute. [SLD resolution](/sld-resolution/) refutes the goal and computes [answer substitutions](/answer-substitution/).
- **Horn-SAT.** The satisfiability problem for propositional Horn formulas. [Forward chaining](/horn-sat-forward-chaining/) decides it in linear time (Dowling and Gallier 1984), while general SAT is NP-complete.
- **Datalog clause.** A definite clause with no function symbols, so that $M_P$ is finite.
- **Normal clause.** A clause $A \leftarrow L_1, \ldots, L_m$ whose body literals may be negated by negation as failure. Normal programs need other semantics, such as the completion or the perfect model.
- **Dual-Horn clause.** A clause with at most one negative literal. It is Horn after negating all atoms, and dual-Horn SAT is also linear.
- **Horn sentence (Horn 1951).** A first-order sentence in prenex form whose matrix is a conjunction of Horn clauses. Horn showed that such sentences are preserved under direct products of structures, which is a model-theoretic reason for the least model.
- **Unit and input resolution.** For Horn clauses, [unit resolution](/unit-resolution/) and [input resolution](/input-resolution/) are complete for refutation, while they are not complete for general clauses.

## References
