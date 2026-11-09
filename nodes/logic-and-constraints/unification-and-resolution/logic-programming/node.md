---
tag: W59X5Z
kind: concept
slug: logic-programming
name: Logic programming
aliases:
- Horn-clause logic programming
area: logic-and-constraints/unification-and-resolution
level: intro
summary: A program is a set of Horn clauses, a run is a proof, and answers come from unification. SLD resolution gives the procedural reading and the least Herbrand model the declarative one.
prereqs: [horn-clause, unification-problem]
see_also: [sld-resolution, sldnf-resolution, answer-substitution, warren-abstract-machine, datalog, datalog-evaluation, horn-sat-forward-chaining, chronological-backtracking]
sources:
  - paper: "Robert A. Kowalski, Predicate logic as programming language, Information Processing 74 (Proceedings of the IFIP Congress), North-Holland, 569 to 574 (1974)"
    locator: the procedural interpretation of Horn clauses
  - paper: doi:10.1145/359131.359136
    title: Robert A. Kowalski, Algorithm = logic + control, Communications of the ACM 22(7), 424 to 436 (1979)
    locator: the separation of the logic component from the control component of an algorithm
  - paper: doi:10.1145/321978.321991
    title: Maarten H. van Emden and Robert A. Kowalski, The semantics of predicate logic as a programming language, Journal of the ACM 23(4), 733 to 742 (1976)
    locator: the operational, model-theoretic and fixpoint semantics of Horn-clause programs
  - book: isbn:9783540181996
    title: John W. Lloyd, Foundations of Logic Programming, second edition, Springer (1987)
    locator: Chapters 1 and 2 (definite programs, their declarative semantics and SLD resolution)
  - book: isbn:9780262691635
    title: Leon Sterling and Ehud Shapiro, The Art of Prolog, second edition, MIT Press (1994)
    locator: Part I (logic programs, their declarative and procedural readings) and the chapters on the computation model of Prolog
  - paper: doi:10.1145/154766.155362
    title: Alain Colmerauer and Philippe Roussel, The birth of Prolog, Second ACM SIGPLAN Conference on History of Programming Languages (HOPL-II), 37 to 52 (1993)
    locator: the history of the first Prolog systems in Marseille and the role of Kowalski's interpretation
---

Logic programming is a style of programming in which a program is a set of logical formulas, usually [Horn clauses](/horn-clause/), and running the program means proving a query from them. A clause $A \leftarrow B_1, \ldots, B_m$ has two readings. Read *declaratively*, it says that $A$ is true if all $B_i$ are true. Read *procedurally*, it says that to solve $A$, solve $B_1, \ldots, B_m$. [SLD resolution](/sld-resolution/) is the procedure that connects the two, and [unification](/unification-problem/) passes data in and out. The results of a run are [answer substitutions](/answer-substitution/), values for the variables of the query. Prolog is the best-known logic programming language, and [Datalog](/datalog/) is its database form.

## In plain words

In most languages you tell the computer what steps to take. In logic programming you tell it what is true, in rules of the form "this holds if those hold", and then you ask a question. The computer searches for a proof of the question from the rules. On the way it finds values for the unknowns in the question, and these values are the answers. One program can answer many kinds of questions: the same rules about joining lists can join two lists, split a list in all possible ways, or check a join.

## The idea

**Programs and queries.** A *definite program* is a finite set of definite clauses: facts $A \leftarrow$ and rules $A \leftarrow B_1, \ldots, B_m$. A *query* is a conjunction of atoms $\leftarrow B_1, \ldots, B_k$ with variables. The question is for which values of the variables the query follows from the program.

**Three semantics that agree.** Van Emden and Kowalski (1976) gave three meanings to a definite program $P$ and showed that they coincide on ground atoms:

- *Model-theoretic.* The least Herbrand model $M_P$: the ground atoms true in every model of $P$.
- *Fixpoint.* The least fixed point of the immediate consequence operator $T_P$, which adds the heads of rules whose bodies hold. It is reached by iterating $T_P$ from the empty set, which is the basis of bottom-up [Datalog evaluation](/datalog-evaluation/).
- *Operational.* The ground atoms $A$ for which the query $\leftarrow A$ has an SLD refutation.

Soundness and completeness of SLD resolution extend this agreement to queries with variables: the computed answers are exactly the most general correct answers.

**Logic plus control.** Kowalski (1979) summed up the approach as *algorithm = logic + control*. The clauses fix what is computed. The control decides how: which atom of a goal to solve next (the computation rule) and which clause to try first (the search rule). Prolog fixes the control to the leftmost atom and depth-first search over the clauses in program order, with [backtracking](/chronological-backtracking/). This makes Prolog a practical language, but it can loop on a query that has an answer, so the programmer must order clauses and body atoms with care.

**The parts of a system.** A Horn clause program is the logic. [SLD resolution](/sld-resolution/) is the proof procedure. [SLDNF resolution](/sldnf-resolution/) adds negation as failure. The [Warren Abstract Machine](/warren-abstract-machine/) is the standard way to compile Prolog. Unification with or without the [occurs check](/occurs-check/) is the basic operation of all of them.

## Examples

**Lists in several directions.** The program

```text
app([], L, L).
app([H | T], L, [H | R]) ← app(T, L, R).
```

defines when one list joined to another gives a third. The query $\leftarrow \mathit{app}([a], [b], Z)$ computes $Z = [a, b]$. The query $\leftarrow \mathit{app}(X, Y, [a, b])$ has three answers, found in this order: $X = [\,], Y = [a, b]$; $X = [a], Y = [b]$; and $X = [a, b], Y = [\,]$. The query $\leftarrow \mathit{app}([a], Y, Z)$ has the single answer $Z = [a \mid Y]$, which still has a variable: it stands for all its instances.

**A recursive relation.** With the facts $e(a, b)$ and $e(b, c)$ and the rules $\mathit{path}(X, Y) \leftarrow e(X, Y)$ and $\mathit{path}(X, Y) \leftarrow e(X, Z), \mathit{path}(Z, Y)$, the query $\leftarrow \mathit{path}(a, W)$ has the answers $W = b$ and $W = c$. Bottom-up, $T_P$ reaches the least model in 3 steps, with 2, 4 and 5 atoms. If the second rule is written $\mathit{path}(X, Y) \leftarrow \mathit{path}(X, Z), e(Z, Y)$, the logic is the same, but Prolog's search finds the two answers and then loops forever. This is the gap between logic and control.

**A computation as a proof.** Natural numbers as $0, s(0), s(s(0)), \ldots$ and the clauses $\mathit{add}(0, Y, Y)$ and $\mathit{add}(s(X), Y, s(Z)) \leftarrow \mathit{add}(X, Y, Z)$ define addition. The query $\leftarrow \mathit{add}(X, Y, s(s(0)))$ has three answers, the three ways to write 2 as a sum. With function symbols, definite programs can compute every computable function, so whether a query has an answer is undecidable in general.

## Where it is used

- **Prolog.** Colmerauer and Roussel built the first Prolog in Marseille in 1972, for natural language processing, after discussions with Kowalski. Prolog is used for symbolic AI, parsing, expert systems and rapid prototyping. The [Warren Abstract Machine](/warren-abstract-machine/) of 1983 became the standard way to compile it.
- **Datalog and deductive databases.** Datalog is logic programming without function symbols. Its programs are evaluated bottom-up with [semi-naive evaluation](/semi-naive-evaluation/) and [magic sets](/magic-sets/). It is used for recursive database queries and for static program analysis.
- **Theorem proving and type checking.** Logic programming engines run type inference rules, proof search in logical frameworks, and the rules of program analyzers. Higher-order logic programming (λProlog) uses [pattern unification](/pattern-unification-problem/).
- **Constraint logic programming.** Replacing unification by constraint solving over a domain, such as integers or reals, gives CLP, used for scheduling and planning.
- **Answer set programming.** A related declarative style based on stable models of normal programs, solved bottom-up with SAT techniques rather than with SLD resolution.

## References
