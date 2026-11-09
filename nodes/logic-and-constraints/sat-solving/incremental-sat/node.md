---
tag: WQ19T1
kind: technique
slug: incremental-sat
name: Incremental SAT solving
aliases:
- assumption-based solving
- SAT solving under assumptions
- activation literals
area: logic-and-constraints/sat-solving
level: advanced
summary: Reuse one CDCL solver for a series of related queries; clauses are added between calls, assumptions switch parts on, and a failed call returns a core of assumptions.
prereqs: [cdcl, clause-learning, unit-propagation]
see_also: [backbone, minimal-unsatisfiable-subset, minimal-correction-subset, core-guided-maxsat, bounded-model-checking, ic3-pdr, cube-and-conquer, unsat-core]
sources:
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, LNCS 2919, 502-518
    locator: the MiniSat interface with incremental clause addition and solving under assumptions, assumptions as the first decisions, and the final conflict analysis that returns the failed assumptions
  - paper: "Niklas Eén and Niklas Sörensson, Temporal induction by incremental SAT solving, Electronic Notes in Theoretical Computer Science 89(4), 2003"
    title: Temporal induction by incremental SAT solving
    locator: incremental bounded model checking and induction, with clauses switched on and off by activation literals
  - paper: "John N. Hooker, Solving the incremental satisfiability problem, Journal of Logic Programming 15(1-2), 1993, 177-186"
    title: Solving the incremental satisfiability problem
    locator: reuse of the search when clauses are added to a satisfiable formula
  - paper: "Alexander Nadel, Vadim Ryvchin and Ofer Strichman, Preprocessing in incremental SAT, SAT 2012, LNCS 7317, 256-269"
    title: Preprocessing in incremental SAT
    locator: why variable elimination conflicts with later clauses and assumptions, and how to freeze or re-eliminate variables
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4 (Marques-Silva, Lynce and Malik, Conflict-Driven Clause Learning SAT Solvers), the sections on incremental solving and assumptions
---

Incremental SAT solving uses one [CDCL](/cdcl/) solver for a sequence of related questions. Between calls the user can add clauses, and each call can carry *assumptions*: literals that must be true for this call only. The solver keeps its learned clauses, its variable scores and its saved phases from one call to the next, so the later calls are often much faster than solving each question from scratch. When a call fails, the solver returns a subset of the assumptions that is enough for the failure, a *failed-assumption core*. Clauses cannot be removed directly, but a clause $C \vee \neg s$ with a fresh *activation literal* $s$ is active only in calls that assume $s$. The interface in this form comes from MiniSat (Eén and Sörensson, 2003). It is the base of [bounded model checking](/bounded-model-checking/), [IC3](/ic3-pdr/), [core-guided MaxSAT](/core-guided-maxsat/), [MUS](/minimal-unsatisfiable-subset/) and [MCS](/minimal-correction-subset/) extraction, [backbone](/backbone/) computation and SMT.

## In plain words

Many tools ask a SAT solver hundreds of similar questions. Each question adds a few rules or tries a few fixed values. Starting a new solver each time throws away everything it found out.

An incremental solver stays alive between questions. Facts it learned stay true, because rules are only ever added. Values that hold for one question only are given as temporary assumptions, which the solver tries first and forgets afterwards. To turn a group of rules on and off, attach a switch variable to each rule in the group and assume the switch on or off. When the answer is "no", the solver also says which of the assumptions it actually needed.

## When it applies

- A series of satisfiability questions over one growing clause set $F$, where each question is $F \wedge a_1 \wedge \cdots \wedge a_k$ for literals $a_i$.
- Clause sets that must shrink as well as grow, if each removable clause is guarded by an activation literal.
- Algorithms that need to know *why* a question failed in terms of the assumptions, such as core-guided optimization or MUS extraction.

It does not apply when consecutive queries share little, or when each query must be preprocessed hard on its own. Then a fresh solver can be as fast.

## The template

Notation: $F$ is the current clause set, with $n$ variables, $m$ clauses and size $|F|$. It includes the clauses learned in earlier calls. $A = (a_1, \ldots, a_k)$ are the assumptions of this call. The assumption $a_d$ is decided at level $d$, before any free decision.

```pseudo id=main
SOLVE(F, A = (a_1, …, a_k))
L1  clear the trail; keep F and every learned clause
L2  propagate; if there is no conflict then go to L6
L3      if the decision level is 0 then return UNSAT with the core ∅
L4      learn an asserting clause C by conflict analysis and add it to F
L5      backjump to the second highest level in C, and go to L2
L6  if the decision level d is less than k then a ← a_{d+1}
L7      if a is false then
L8          return UNSAT with the core ANALYZE-FINAL(a)
L9      open level d + 1; if a is free then make a its decision; go to L2
L10 if all variables are set then return SAT with the model
L11 open a new level, decide a free variable, and go to L2
```

ANALYZE-FINAL($a$) starts from the variable of $a$ and walks the trail backward, as in [conflict analysis](/clause-learning/). For each marked literal with a reason clause, it marks the other variables of that reason. Each marked literal without a reason is a decision, and below level $k$ all decisions are assumptions, so it adds that literal to the core. Literals of level 0 are skipped. The core is $a$ together with these assumptions.

### Why it is correct

**Lemma 1 (learned clauses stay valid).** Every clause learned in any call is implied by the clauses added before it was learned.

*Proof.* A learned clause is a resolvent chain of clauses in $F$ at that time, which includes earlier learned clauses. The assumptions are only decisions: the clause learned at line L4 does not depend on them, though it may contain their negations. Since clauses are never removed, every later clause set implies all earlier learned clauses. $\square$

So a later call on $F'$ with $F \subseteq F'$ may keep everything it learned on $F$.

**Theorem.** If SOLVE returns SAT, the model satisfies $F$ and every $a_i$. If it returns UNSAT with core $K$, then $K \subseteq A$ and $F \wedge \bigwedge_{a \in K} a$ is unsatisfiable. In particular, the core $\emptyset$ means that $F$ itself is unsatisfiable.

*Proof.* SAT: all variables are set and propagation found no false clause, and line L9 makes every assumption true or finds it already true. UNSAT at line L3: a conflict at level 0 uses only clauses of $F$, so $F$ is unsatisfiable by Lemma 1 and the soundness of [unit propagation](/unit-propagation/). UNSAT at line L8: each literal on the trail at level at least 1 is a decision, or is forced by its reason clause and earlier trail literals. By induction along the trail, every marked literal is implied by $F$ together with the decisions that ANALYZE-FINAL marks; level-0 literals are implied by $F$ alone. Below level $k$ the decisions are assumptions. So $F \wedge \bigwedge (K \setminus \{a\})$ implies $\neg a$, and $F \wedge \bigwedge K$ is unsatisfiable. $\blacksquare$

The core is not minimal in general, and it depends on the order of the assumptions. A smaller core costs more calls; see [minimal unsatisfiable subset](/minimal-unsatisfiable-subset/).

### Cost

One call costs the same as a CDCL run, with no worst-case gain. The gain is in practice: learned clauses, VSIDS scores and saved phases carry over. Assumptions cost one decision level each, and re-deciding them after every restart or backjump below level $k$ costs $O(k)$ decisions plus their propagation. With many assumptions this overhead matters, and some solvers then add the assumptions as unit clauses guarded by one activation literal.

## Classic examples

**Activation literals.** Let $x_1, x_2, x_6$ be problem variables and $s_3, s_4, s_5$ activation literals (variables 3, 4 and 5). The clauses are
$$(\neg s_3 \vee x_1),\quad (\neg s_4 \vee \neg x_1),\quad (\neg s_5 \vee x_2),\quad (\neg x_1 \vee \neg x_2 \vee x_6).$$

- `solve([3, 4, 5])`: level 1 decides $s_3$, and propagation sets $x_1$ and then $\neg s_4$. At level 2 the assumption $s_4$ is false. ANALYZE-FINAL($s_4$) marks $x_1$ through the reason $(\neg s_4 \vee \neg x_1)$, then $s_3$ through $(\neg s_3 \vee x_1)$, and returns the core $\{s_4, s_3\}$. The assumption $s_5$ is not in it.
- `solve([3, 5])`: SAT, with $x_1 = x_2 = x_6 = 1$.
- After `add_clause([-6])`, `solve([3, 5])` fails with the core $\{s_5, s_3\}$: $s_3$ forces $x_1$, then $(\neg x_1 \vee \neg x_2 \vee x_6)$ with $\neg x_6$ forces $\neg x_2$, and $(\neg s_5 \vee x_2)$ forces $\neg s_5$. The unit $\neg x_6$ is at level 0 and does not appear in the core.

**Reuse of learned clauses.** Put the pigeonhole formula with 5 pigeons and 4 holes, 45 clauses, behind one activation literal $s$. In the implementation, the first call `solve([s])` needs 18 conflicts and learns 18 clauses, and returns the core $\{s\}$. The second identical call needs no conflict at all: the learned clauses force $\neg s$ by unit propagation at level 0. A call without assumptions is then satisfiable, with $s$ false.

**Users of the interface.**

- [Bounded model checking](/bounded-model-checking/) adds one copy of the transition relation per step and asks, under an assumption, whether the bad state is reachable at the current depth. Eén and Sörensson also used activation literals for the induction step.
- [Backbone](/backbone/) computation asks for each candidate literal $l$ whether $F \wedge \neg l$ is satisfiable, with $\neg l$ as an assumption.
- [Core-guided MaxSAT](/core-guided-maxsat/) assumes all soft clauses through their activation literals and relaxes the core it gets back.
- [MUS](/minimal-unsatisfiable-subset/) and [MCS](/minimal-correction-subset/) algorithms switch clauses on and off by assumptions in one solver.
- [IC3/PDR](/ic3-pdr/) makes many small queries of the form "is this cube reachable in one step from frame $i$", with the cube as assumptions.
- [Cube-and-conquer](/cube-and-conquer/) can solve all cubes in one incremental solver, each cube as a set of assumptions.
- In [lazy SMT](/lazy-smt/) the theory solver adds conflict clauses to the SAT solver between checks.

## Variations

- **Clause groups.** Some interfaces let the user name a group of clauses and drop it later. Internally this is the same as an activation literal per group, plus a unit $\neg s$ when the group is dropped for good.
- **The IPASIR interface.** The standard C interface of incremental solvers, used in the SAT Race 2015 and later competitions, has the calls `add`, `assume`, `solve`, `val` and `failed`. `failed` reports whether an assumption is in the final core.
- **Incremental preprocessing.** [Variable elimination](/bounded-variable-elimination/) removes variables that a later clause or assumption may use. Solvers *freeze* the variables that the user may refer to, or put the removed clauses back when such a variable comes back (Nadel, Ryvchin and Strichman).
- **Hooker's incremental satisfiability.** The older form of the problem adds clauses to a satisfiable formula and asks whether it stays satisfiable, reusing the search tree of the last call.
- **Core shrinking.** Many applications improve the core by solving again under the core alone, which often returns a smaller one, or by full MUS extraction.

## Pitfalls

- **Do not remove original clauses.** Learned clauses may depend on them. Use activation literals, and never delete a clause that learned clauses may rest on.
- **Clean up disabled groups.** A group that is no longer needed should get the unit $\neg s$. Otherwise its clauses stay active in propagation for every call that does not assume $\neg s$, and they slow the solver down.
- **Preprocessing and later clauses.** If the solver has eliminated a variable, later clauses or assumptions over that variable are wrong unless it was frozen or restored.
- **The model is for one call.** Read the model before the next call or clause addition.
- **Cores are not minimal.** The final conflict analysis gives a sufficient set, not a minimal one, and the result depends on the order of the assumptions.
- **An assumption may already be false at level 0.** Then the core is the assumption alone, and $F \wedge a$ is unsatisfiable. The empty core means $F$ is unsatisfiable, and every later call fails too.

## Exercises

1. Show that a clause learned in a call under assumptions can contain the negations of assumptions, and explain why it stays valid when the assumptions change.
2. Give a formula and an order of assumptions for which ANALYZE-FINAL returns a core that is not minimal, and a better order for which it is minimal.
3. Use activation literals to compute, with one solver, for which subsets of three clause groups the formula is satisfiable. How many calls are needed, and how can the cores cut this number?
4. Write the backbone algorithm with model filtering for an incremental solver. Which learned clauses help later calls?
5. Explain why an unsatisfiable call that returns the empty core makes all later calls on the same solver unsatisfiable.

## References
