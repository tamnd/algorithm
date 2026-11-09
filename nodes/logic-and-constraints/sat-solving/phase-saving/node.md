---
tag: 8QJZVM
kind: technique
slug: phase-saving
name: Phase saving
aliases:
- polarity caching
- progress saving
- saved phases
area: logic-and-constraints/sat-solving
level: advanced
summary: When a backtrack unassigns a variable, store its value; when the solver later decides that variable, give it the stored value. Backjumps and restarts then lose less work.
prereqs: [cdcl, non-chronological-backtracking]
see_also: [vsids, restarts, clause-learning, connected-components, stochastic-local-search, walksat, dpll, model-counting]
sources:
  - paper: doi:10.1007/978-3-540-72788-0_28
    title: Knot Pipatsrisawat and Adnan Darwiche, A lightweight component caching scheme for satisfiability solvers, Theory and Applications of Satisfiability Testing (SAT 2007), Lecture Notes in Computer Science 4501, 2007
    locator: pages 294 to 299 (the loss of solved components by backjumping, phase saving as a fix, and the measured comparison with MiniSat)
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, Lecture Notes in Computer Science 2919, 2004
    locator: pages 502 to 518 (the MiniSat solver that served as the base of the comparison, with the decision polarity fixed to false)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (phase saving among the techniques of modern CDCL solvers)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (the polarity of decisions in the CDCL algorithm)
---

Phase saving is the polarity rule of [CDCL](/cdcl/) solvers that stores the value of each variable when a backtrack unassigns it, and that gives a variable this stored value, its saved phase, when the solver next picks it for a decision. The decision heuristic, such as [VSIDS](/vsids/), still chooses which variable to decide; phase saving chooses only its sign. Pipatsrisawat and Darwiche introduced it in 2007 to stop [backjumps](/non-chronological-backtracking/) and [restarts](/restarts/) from throwing away the solutions of independent parts of the formula. It is a heuristic with one exact property, proved below: a part of the formula that shares no variable with the rest and that has once been fully satisfied is never again the site of a conflict.

## In plain words

A solver that hits a dead end jumps back, sometimes far back, and undoes many values that had nothing to do with the dead end. A restart undoes all of them. Some of these values may have solved a whole separate part of the problem. Without care, the solver may later choose other values for them and have to solve that part again.

Phase saving is a small memory. Each time a value is undone, the solver writes down what it was. When it next has to guess that value, it guesses what it had before. So the values that were fine come back as they were, and a part of the problem that was solved stays solved. The solver still decides in its own order which value to guess next; the memory only says which way to guess.

## When it applies

- The search undoes assignments that are not to blame for the conflict: [non-chronological backtracking](/non-chronological-backtracking/) undoes whole levels, and [restarts](/restarts/) undo everything above level 0.
- The decision heuristic chooses a variable but not a sign. With VSIDS, the order of variables changes often, so the same variables come back in a new order after each backjump.
- The formula has parts that are only loosely connected, as in industrial instances from hardware or software verification. For a formula whose variables all interact, the saved phases carry less useful information.
- The aim is to find one model or prove that none exists. For [model counting](/model-counting/) or enumeration, the solver must visit other models, and saved phases steer it back to the old ones.

## The template

Each variable $v$ has a saved phase $\mathrm{phase}(v) \in \{\text{true}, \text{false}\}$, set at the start by the hole INITIAL.

```pseudo id=main
ON-UNASSIGN(v)                                ▷ called for each variable a backtrack frees
L1  phase(v) ← the value v had                  ▷ hole WHEN: on every unassign, or only some

PICK-POLARITY(v)                              ▷ v: the variable chosen by the decision heuristic
L2  s ← phase(v)
L3  s ← OVERRIDE(v, s)                          ▷ hole OVERRIDE: none, random flips, target phases
L4  return v if s is true, else ¬v
```

The holes:

- **INITIAL.** MiniSat starts with all phases false, so the first decisions are negative. Other choices are all true, or the sign that occurs more often in the input.
- **WHEN.** The rule of Pipatsrisawat and Darwiche saves the value of every variable when it is unassigned, whether it was a decision or a forced literal. A limited variant saves only the variables of the last decision level.
- **OVERRIDE.** Plain phase saving returns $s$. Some solvers flip the phase with a small probability, or replace it at times by a stored assignment that was good by some measure, to move the search away from a fixed region.

**Correctness.** The polarity of a decision has no effect on soundness or completeness. Any sign keeps the invariants of CDCL, and its termination proof does not use the sign. What can be proved exactly is what phase saving keeps.

Let $F = G \wedge H$, where $G$ and $H$ share no variable, and let $V_G$ be the variables of $G$. Assume OVERRIDE is "none" and WHEN is "every unassign".

*Lemma 1 (learned clauses stay on one side).* Every clause that CDCL learns on $F$ has all its variables in $V_G$ or all outside $V_G$, and a learned clause over $V_G$ is implied by $G$ alone. *Proof.* By induction over the conflicts. A conflict starts from a false clause, which is an input clause or an earlier learned clause, so it is on one side. Each resolution step of the analysis resolves the current clause with the reason clause of one of its variables, which by induction is on the side of that variable, so the side does not change. Removing literals of level 0 and [clause minimization](/clause-minimization/) only remove literals. A clause derived from clauses over $V_G$ that are implied by $G$ is implied by $G$. $\blacksquare$

*Theorem (a solved part stays solved).* Suppose that at some decision point $T$, with propagation complete and no conflict, every variable of $V_G$ is assigned. Let $\beta$ be the assignment of $V_G$ at $T$. Then $\beta$ satisfies $G$, and at every later time: every assigned variable of $V_G$ has its value in $\beta$, every variable of $V_G$ that was unassigned since $T$ has its $\beta$ value as saved phase, and no clause over $V_G$ is false.

*Proof.* At $T$, no clause is false and every clause of $G$ has all its variables assigned, so $\beta$ satisfies $G$. By Lemma 1, $\beta$ also satisfies every learned clause over $V_G$. Now go through the later events in order and assume the claim before each one. A backtrack saves the current value of each freed variable, which is its $\beta$ value. A decision on $v \in V_G$ happens only when $v$ is unassigned, so $v$ was unassigned after $T$ and its saved phase is $\beta(v)$, which PICK-POLARITY returns. A literal $u$ on a variable of $V_G$ forced by propagation has a reason clause over $V_G$, by Lemma 1, whose other literals are false now and so false in $\beta$; since $\beta$ satisfies the clause, $u$ is true in $\beta$. Finally, a clause over $V_G$ false now has all its literals false in $\beta$, which contradicts that $\beta$ satisfies it. $\blacksquare$

So after $T$, every conflict is in $H$, however often the solver jumps back or restarts. Without phase saving, a backjump that unassigns $V_G$ can lead to new decisions on $V_G$ with other signs and to new conflicts in $G$. Pipatsrisawat and Darwiche called the method a lightweight form of component caching for this reason. The theorem is about exact phase saving; random flips or other overrides break it.

**Cost.** One store per unassigned variable and one load per decision, so $O(1)$ time per assignment, and one bit or byte per variable of space.

**Example.** Let $G$ be a random satisfiable 3-CNF with 80 variables and 336 clauses, built around a hidden model, and let $H$ be the [pigeonhole](/pigeonhole-principle/) formula with 6 pigeons and 5 holes, on 30 other variables, so that $F = G \wedge H$ is unsatisfiable. A CDCL solver with VSIDS and Luby restarts with unit 4 was run on 10 such formulas, once with phase saving and once with all decisions negative. The table counts the conflicts on clauses over the variables of $G$, before and after the first decision point at which all of $G$ is assigned.

| run | all conflicts | conflicts in $G$ before that point | conflicts in $G$ after it |
|---|---|---|---|
| with phase saving | 2236 | 446 | 0 |
| always false | 2071 | 477 | 72, in 6 of the 10 runs |

The 0 is the theorem. The other numbers are only measurements: here most conflicts come from $H$, which phase saving does not help, and the totals are close.

## Classic examples

- **The original measurement.** Pipatsrisawat and Darwiche added phase saving to MiniSat and ran both versions on 1251 industrial instances with a limit of 1800 seconds. The version with phase saving solved 21 more instances, and it was slower on some instances. They also used it in their solver RSat.
- **Later solvers.** Phase saving became the default polarity rule of later MiniSat versions and of almost every later CDCL solver.
- **Restarts that are cheap.** With saved phases, a restart often rebuilds much the same assignment, so solvers can restart often, as the glucose-style [restart](/restarts/) policy does, without losing the assignment.

## Variations

- **Target and best phases.** Some solvers keep, besides the last value, the assignment of the longest trail without conflict seen so far, and use it in place of the saved phase for stretches of the search.
- **Rephasing.** At set intervals, the solver resets all saved phases to some other source: all true, all false, random, the best assignment so far, or the result of a run of [local search](/stochastic-local-search/) such as [WalkSAT](/walksat/).
- **In DPLL.** With chronological backtracking, a backtrack frees only the variables of one level and the next decision flips the last one, so saving phases changes less than in CDCL.

## Pitfalls

- **A restart that skips the save.** If the restart code clears the trail by its own loop and not through the backtrack routine, the saved phases keep stale values and the theorem fails. Every unassignment must go through ON-UNASSIGN.
- **Stuck in one region.** Phase saving pulls the search back to the same assignment after each restart. On satisfiable formulas where that region has no model, this can slow the search; this is why solvers add rephasing.
- **Model enumeration.** After a model is found and a blocking clause is added, saved phases steer the solver toward the old model. Reset or randomize the phases between models.
- **Expecting fewer conflicts in general.** The theorem holds only for parts with disjoint variables. On formulas without such structure, the effect is an empirical question, and it can be negative.

## Exercises

1. Show that Lemma 1 fails for a solver that adds clauses over both $V_G$ and other variables, for example by a preprocessing step, and give a run in which the theorem then fails.
2. Extend the theorem to $k$ parts $G_1, \ldots, G_k$ with pairwise disjoint variables: once a part has been fully assigned at a decision point, it never has a conflict again.
3. Give a satisfiable formula and a run with restarts in which phase saving makes the solver return to the same failed region after every restart, while all-false decisions find a model at once.

## References
