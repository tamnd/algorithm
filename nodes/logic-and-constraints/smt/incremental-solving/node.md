---
tag: 7N922A
kind: technique
slug: incremental-solving
name: Incremental solving
aliases:
- push and pop
- solving under assumptions
- incremental SMT
- assertion stack
area: logic-and-constraints/smt
level: core
summary: Solve a sequence of related queries with one solver, adding and removing assertions with push and pop, or passing temporary assumptions, so that learned facts carry over between the queries.
prereqs: [smt-problem, incremental-sat]
see_also: [smt-lib, unsat-core, cdcl-t, bounded-model-checking, symbolic-execution, optimization-modulo-theories, maxsmt, cegis]
sources:
  - url: https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-07-07.pdf
    title: Clark Barrett, Pascal Fontaine and Cesare Tinelli, The SMT-LIB Standard, Version 2.7, release of July 7, 2025
    locator: Section 4.1.4 (the assertion stack), Section 4.2.2 (push, pop and reset-assertions), Section 4.2.5 (check-sat-assuming), Section 4.2.7 (get-unsat-assumptions)
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, LNCS 2919, pages 502 to 518
    locator: incremental SAT with assumptions, and the removal of clauses by activation literals
  - paper: doi:10.1016/s1571-0661(05)82542-3
    title: Niklas Eén and Niklas Sörensson, Temporal induction by incremental SAT solving, Electronic Notes in Theoretical Computer Science 89(4), 2003, pages 543 to 560
    locator: one incremental solver for all the bounded model checking and induction queries
  - paper: doi:10.1016/0743-1066(93)90018-c
    title: John N. Hooker, Solving the incremental satisfiability problem, The Journal of Logic Programming 15(1-2), 1993, pages 177 to 186
    locator: the incremental satisfiability problem, adding clauses to a solved formula
  - paper: doi:10.1145/378239.379019
    title: Jesse Whittemore, Joonyoung Kim and Karem A. Sakallah, SATIRE, a new incremental satisfiability engine, DAC 2001, pages 542 to 545
    locator: reuse of learned clauses between related SAT queries
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.4.1 (incrementality and backtrackability of theory solvers)
---

Many uses of an SMT solver ask not one question but a long sequence of related ones: the same program with one more path condition, the same circuit unrolled one step further, the same constraints with a tighter bound on the cost. Incremental solving answers them with one solver object that keeps its state. New assertions are added to a *context*, a `push` marks a point to which a later `pop` can return, and `check-sat-assuming` checks the context together with *assumptions* that hold for this one check only. Between the checks the solver keeps its learned clauses, its theory lemmas, its variable activities and its theory state, as far as they stay sound. The [SMT-LIB](/smt-lib/) standard defines the interface. Inside the solver, the main tool is the *activation literal*, and the main danger is a learned fact that depends on an assertion that was popped.

## In plain words

Suppose you solve a large puzzle and then someone asks: "and what if this one extra rule also held?" You would not throw away all your notes and start again. You would keep everything you learned, add the new rule, and go on.

That is incremental solving. The solver keeps what it has learned. When the user says "push", the solver marks the place. When the user says "pop", it removes the rules added since that mark.

The hard part is the notes. A note that was learned with the help of a removed rule may now be false. So the solver tags each rule with a switch, and every note that used the rule keeps the switch in it. When the rule is removed, its switch is turned off, and those notes stop having any effect.

## When it applies

- The queries share most of their assertions, so the work spent on the shared part can be reused.
- The changes are mostly additions, or removals in the reverse order of the additions (a stack). Removals in any order can be done with assumptions.
- The solver can undo its theory state cheaply: the theory solver is *backtrackable*, in the words of the Handbook, and it is already built to undo work when the SAT search backjumps.

## The template

The holes are the way pop removes assertions, which learned facts are kept, and how assumptions are chosen.

```pseudo id=main
INCREMENTAL SOLVER
L1  state: clause set F, stack S of activation literals, empty at the start
L2  PUSH:   create a fresh Boolean variable a; push a onto S
L3  ASSERT φ: for each clause C of the CNF of φ, add (¬top(S) ∨ C) to F, or C if S is empty   ▷ hole: activation literals, or a real undo log
L4  CHECK(L):  solve F under the assumptions S ∪ L, keeping the learned clauses and theory lemmas   ▷ hole: what to keep and what to forget
L5      if UNSAT: the final conflict, written over the assumptions, gives the failed subset of L
L6  POP:    a ← pop(S); add the unit clause ¬a to F                ▷ hole: also delete every clause with ¬a, now satisfied
L7  the theory solver keeps one level of its own state per assertion level, and undoes it on POP
```

**Assumptions.** A check under assumptions $L$ decides the literals of $L$ first, as decisions at the lowest levels, before any other decision. If the search derives a conflict that needs one of them, the solver resolves the conflict back to the assumptions, and the literals that remain form a *failed* subset of $L$: the context with these literals alone is already unsatisfiable. This is the source of `get-unsat-assumptions` and of [unsat cores](/unsat-core/) by selector variables.

**Why the activation literals keep learned clauses sound.** The variable $a$ occurs in $F$ only in the negative literal $\neg a$, and it is set only as an assumption, which is a decision without a reason clause. Conflict analysis resolves only on literals with a reason. So it never resolves on $a$, and every learned clause that used an input clause $\neg a \vee C$ still contains $\neg a$. After the pop, the unit clause $\neg a$ makes all these clauses true, and they have no effect. A learned clause without $\neg a$ was derived without the popped assertions, so it is a consequence of the assertions that remain. Theory lemmas are $T$-valid, so they can always stay.

### A worked example

Let $e_1$ be $x = y$, $e_2$ be $x = z$, $e_3$ be $f(x) = f(y)$ and $e_4$ be $f(x) = f(z)$.

1. ASSERT $e_1 \vee e_2$ at the base level.
2. PUSH, with the activation literal $a$. ASSERT $\neg e_3$ and $\neg e_4$. The clause set is now $(e_1 \vee e_2)$, $(\neg a \vee \neg e_3)$ and $(\neg a \vee \neg e_4)$.
3. CHECK. The solver decides $a$, and unit propagation gives $\neg e_3$ and $\neg e_4$. Congruence closure gives the theory lemmas $\neg e_1 \vee e_3$ and $\neg e_2 \vee e_4$, so $\neg e_1$ and $\neg e_2$ follow, and $e_1 \vee e_2$ is false. Conflict analysis resolves back to the decision $a$ and learns the unit clause $\neg a$. The answer is UNSAT, and the failed assumption is $a$, that is, the pushed level.
4. POP. Add $\neg a$, which the solver has already learned. The clauses with $\neg a$ are now true.
5. CHECK. The solver sets $e_1$ and $e_3$, which is consistent. The answer is SAT, with $x = y$ and $f(x) = f(y)$. The two theory lemmas from step 3 were kept, and they gave $e_3$ at once.

*Without activation literals.* If step 2 added $\neg e_3$ and $\neg e_4$ as plain units, the solver would learn the units $\neg e_1$ and $\neg e_2$ at level 0. If it kept them after a pop that removes only $\neg e_3$ and $\neg e_4$, the formula $e_1 \vee e_2$ alone would get the wrong answer UNSAT. This is why a solver must either guard the clauses or delete every learned clause that used a popped assertion.

## Classic examples

- **[Bounded model checking](/bounded-model-checking/) and induction.** Eén and Sörensson used one incremental SAT solver to unroll a circuit step by step. Each new depth adds clauses, and the property at the old depth is removed by an activation literal.
- **[Symbolic execution](/symbolic-execution/).** The path condition grows along a path. At each branch the tool pushes, adds the branch condition, checks, and pops when it goes back.
- **Program verifiers.** Tools such as Boogie and Dafny send many verification conditions over one background theory, each one between a push and a pop.
- **Optimization and [MaxSMT](/maxsmt/).** [Optimization modulo theories](/optimization-modulo-theories/) adds tighter and tighter bounds on the cost, and core-guided MaxSMT solves under assumptions on soft constraints, using the failed assumptions as cores.
- **[CEGIS](/cegis/).** The synthesizer adds one counterexample at a time to the same solver.

## Variations

- **Real removal.** The solver keeps a log of the clauses and lemmas that each level added, and deletes them on pop, with every learned clause that depends on them. This is more work than activation literals, but it keeps the clause set small.
- **Assumptions only.** Without push and pop, a client can guard each assertion with its own literal and pass the active ones as assumptions at every check. Assertions can then be switched in any order.
- **Global or scoped declarations.** In SMT-LIB, symbols declared after a push are removed by the matching pop, unless the option `:global-declarations` is true.
- **Theory state.** Theory solvers keep trails, so that pop is a backtrack. Union-find with path compression is hard to undo, so many EUF solvers keep a proof forest or use union by size without path compression.
- **Incremental preprocessing.** Simplifications such as variable elimination can remove a variable that a later assertion uses again. Incremental solvers must either freeze such variables or undo the step.

## Pitfalls

- **Unsound reuse.** A learned fact that depends on a popped assertion must not stay active, as the example shows. This applies also to theory facts: a bound that a theory solver derived from a popped assertion must be undone.
- **Preprocessing that is not incremental.** A solver that removes a variable by elimination before the first check can give wrong answers when a later assertion mentions that variable.
- **Too many activation literals.** Each push adds a variable, and popped clauses stay until garbage collection. Long sessions with many push and pop pairs slow down unit propagation if the solver does not clean up.
- **Lost heuristics.** Keeping learned clauses can also hurt: they may steer the search towards parts of the space that the new query does not need. Some clients prefer a new solver for unrelated queries.
- **Assumptions are not assertions.** Assumptions hold for one check only, and they never appear in the answer of `get-unsat-core`, only in that of `get-unsat-assumptions`.

## Exercises

1. Prove that the failed subset of the assumptions in line L5 makes the context unsatisfiable.
2. Show that if the activation literal $a$ also appeared positively in some clause, a learned clause could lose $\neg a$, and give an example where this makes a pop unsound.
3. A tool checks $2^k$ path conditions of a binary tree of depth $k$ by depth-first search with push and pop. How many push and pop calls does it make, and how many checks?

## References
