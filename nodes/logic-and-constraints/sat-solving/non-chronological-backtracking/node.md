---
tag: 7B5JRJ
kind: technique
slug: non-chronological-backtracking
name: Non-chronological backtracking
aliases:
- backjumping
- conflict-directed backjumping
- conflict-driven backjumping
area: logic-and-constraints/sat-solving
level: core
summary: After a conflict, undo every decision level above the second highest level of the learned clause, possibly many, and assert the clause's one literal of the conflict level there.
prereqs: [clause-learning, chronological-backtracking]
see_also: [cdcl, first-uip, conflict-directed-backjumping, dpll, implication-graph, phase-saving, restarts, nogood-learning]
sources:
  - paper: doi:10.1109/12.769433
    title: João P. Marques-Silva and Karem A. Sakallah, GRASP, a search algorithm for propositional satisfiability, IEEE Transactions on Computers 48(5), 1999
    locator: pages 506 to 521 (non-chronological backtracking driven by the conflict-induced clause)
  - paper: "Patrick Prosser, Hybrid algorithms for the constraint satisfaction problem, Computational Intelligence 9(3), 1993, pages 268 to 299"
    locator: conflict-directed backjumping, which jumps to the latest variable of the conflict set
  - paper: "Roberto J. Bayardo Jr. and Robert C. Schrag, Using CSP look-back techniques to solve real-world SAT instances, Proceedings of AAAI 1997, pages 203 to 208"
    locator: conflict-directed backjumping and learning added to a DPLL solver
  - paper: doi:10.1145/1217856.1217859
    title: Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, Solving SAT and SAT modulo theories, from an abstract Davis-Putnam-Logemann-Loveland procedure to DPLL(T), Journal of the ACM 53(6), 2006
    locator: pages 937 to 977 (the Backjump rule of abstract DPLL, its soundness, and termination by a lexicographic order on the trail)
  - paper: "Alexander Nadel and Vadim Ryvchin, Chronological backtracking, Theory and Applications of Satisfiability Testing (SAT 2018), Lecture Notes in Computer Science 10929, 2018"
    locator: backtracking one level after some conflicts in a CDCL solver, and the changes it needs in propagation and analysis
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (non-chronological backtracking and the backtrack level of an asserting clause)
---

Non-chronological backtracking is the step of a [CDCL](/cdcl/) solver that, after it learns a clause at a conflict, undoes every decision level above the second highest level $b$ of the literals of that clause, and then assigns the clause's one literal of the conflict level at level $b$. The decisions between $b$ and the conflict level took no part in the conflict, so they are undone at once instead of one at a time. It differs from [chronological backtracking](/chronological-backtracking/), as in [DPLL](/dpll/), which undoes only the last decision and tries its complement. It needs an asserting learned clause, such as the [first UIP](/first-uip/) clause of [clause learning](/clause-learning/).

## In plain words

A solver makes guesses one after another, and each guess opens a new level. Then it hits a dead end. Plain backtracking blames the last guess: it undoes that guess and tries the other value. But often the last few guesses had nothing to do with the dead end. Then the solver will hit the same dead end again under each of their combinations.

A clause-learning solver knows which values caused the dead end: they are the values in the new rule it just learned. So it jumps back over all the guesses that do not appear in the rule, to the latest level where the rule leaves exactly one open value. There the rule forces that value, and the search goes on from that point. The skipped guesses are not marked as wrong. They are only undone, and the solver can make them again later.

## When it applies

- The search keeps a trail with decision levels, and each conflict yields a learned clause $C$ that is implied by the formula and false on the trail.
- The clause $C$ is asserting: exactly one literal $\neg u$ has the conflict level $d$, and the other literals have levels at most $b < d$. The first UIP clause and the other UIP clauses have this property. Without it, there is no level where $C$ is unit, and the solver has to backtrack in some other way.
- The goal is to decide satisfiability or find a model. The jump does not lose models, but it does not enumerate the search space in a fixed order, so it fits poorly with methods that need a systematic enumeration, such as exact model counting without other changes.

## The template

```pseudo id=main
BACKJUMP(C, d)                                ▷ C: asserting clause learned at conflict level d
L1  b ← TARGET(C, d)                            ▷ hole TARGET: the second highest level in C, or d − 1, or a mix
L2  for each literal ℓ on the trail with level(ℓ) > b, from the last to the first do
L3      unassign ℓ; KEEP(ℓ)                     ▷ hole KEEP: save its phase, return its variable to the heap
L4  remove the level starts above b; the current level is b
L5  ¬u ← the literal of C whose variable was at level d
L6  assign ¬u at level b with reason C          ▷ C is unit at level b
L7  resume unit propagation from ¬u
```

The holes:

- **TARGET.** The standard choice is $b$, the largest level of a literal of $C$ other than $\neg u$, or 0 when $C$ has one literal. Chronological backtracking takes $d - 1$. Solvers that mix the two take $d - 1$ when the jump would undo more than some number of levels.
- **KEEP.** Each unassigned variable goes back into the order of free variables used by [VSIDS](/vsids/). [Phase saving](/phase-saving/) records its last value here, so that the solver can make the same choice again when it redecides the variable.

**Correctness.** Write $F'$ for the input formula together with the clauses learned so far. Assume that $C$ is asserting with the literal $\neg u$ of level $d$.

*1. Level $b$ is the lowest level where $C$ is unit.* At the end of level $b$, every literal of $C$ other than $\neg u$ is false, since its level is at most $b$, and the variable of $u$ is unassigned, since its level is $d > b$. So $C$ is unit with $\neg u$ after line L4. If $b \ge 1$, some literal of $C$ other than $\neg u$ has level exactly $b$. At any level below $b$, that literal and $\neg u$ are both unassigned, so $C$ is not unit there and forces nothing.

*2. No model is lost.* Let $M$ be a model of $F$ that agrees with the trail up to level $b$. Then $M$ satisfies $C$, because $F \models C$ by the clause learning page. Every literal of $C$ other than $\neg u$ is false in $M$, so $\neg u$ is true in $M$, and $M$ agrees with the trail after line L6. The levels $b + 1$ to $d$ are only undone, never negated, so no model that disagrees with them is ruled out. Hence the set of models of $F$ that extend the trail is the same before the decisions of levels $b + 1$ to $d$ were made and after the jump.

*3. Progress.* Let $a_i$ be the number of literals of level $i$ on the trail, and compare the vectors $(a_0, a_1, \ldots, a_n)$ in lexicographic order, with $a_i = 0$ for levels that do not exist. Propagation increases the entry of the current level. A decision makes a new entry 1 where it was 0. A conflict followed by lines L1 to L7 keeps $a_0, \ldots, a_{b-1}$, increases $a_b$ by at least 1, because of line L6, and clears the entries above $b$. So each step makes the vector larger. Every entry lies in the range from 0 to $n$, so only $(n + 1)^{n + 1}$ vectors exist, and a search with no restarts has finitely many conflicts. This is the termination argument of Nieuwenhuis, Oliveras and Tinelli; it holds for any TARGET from $b$ to $d - 1$, since line L6 at a level $b' \ge b$ also increases $a_{b'}$, and it does not need the learned clauses to be kept. A [restart](/restarts/) clears the vector, so with restarts the argument needs restart intervals that grow without bound, or no deletion of learned clauses, as on the CDCL page.

**Cost.** Lines L2 to L4 take time linear in the number of literals removed. With [two watched literals](/two-watched-literals/), no clause has to be updated on backtrack, so a jump over many levels costs only the trail entries. The hidden cost is in the future: the literals of the skipped levels that did not depend on the conflict are propagated again when the solver redecides them. Nadel and Ryvchin measured this cost and proposed to backtrack chronologically after some conflicts to avoid it.

**Example.** Take the formula of the [CDCL](/cdcl/) page:

$$C_1 = \{x_1, x_2\},\ C_2 = \{x_1, x_3, x_7\},\ C_3 = \{\neg x_2, \neg x_3, x_4\},\ C_4 = \{\neg x_4, x_5, x_8\},\ C_5 = \{\neg x_4, x_6, x_9\},\ C_6 = \{\neg x_5, \neg x_6\}.$$

Let the decisions be $\neg x_8$, $\neg x_9$, $\neg x_7$ and $\neg x_1$, at levels 1 to 4. Then $C_1$ to $C_5$ force $x_2, x_3, x_4, x_5, x_6$ at level 4, and $C_6$ is false.

| step | event | trail, with levels | learned clause, $b$ |
|---|---|---|---|
| 1 | conflict on $C_6$ | $\neg x_8^1, \neg x_9^2, \neg x_7^3, \neg x_1^4, x_2^4, x_3^4, x_4^4, x_5^4, x_6^4$ | $\{\neg x_4, x_8, x_9\}$, $b = 2$ |
| 2 | jump to level 2, assert $\neg x_4$ | $\neg x_8^1, \neg x_9^2, \neg x_4^2$ | |
| 3 | decide $\neg x_7$, then $\neg x_1$ | $\ldots, \neg x_7^3, \neg x_1^4, x_2^4, x_3^4$ | |
| 4 | conflict on $C_3$ | | $\{x_1, x_4, x_7\}$, $b = 3$ |
| 5 | jump to level 3, assert $x_1$ | $\neg x_8^1, \neg x_9^2, \neg x_4^2, \neg x_7^3, x_1^3$ | |

At step 1, the conflict depends on $\neg x_8$ and $\neg x_9$ but not on $\neg x_7$, which is at level 3. The jump undoes level 3 along with level 4, and $\neg x_4$ goes to level 2, where it belongs. A DPLL solver would keep $\neg x_7$ and flip $x_1$ at level 4. At step 4, the first UIP is the decision $\neg x_1$, and the jump to level 3 undoes one level only, as chronological backtracking would.

**Example with irrelevant decisions.** Take the [pigeonhole formula](/sat/) with $h + 1$ pigeons and $h$ holes, and add $k$ variables $y_1, \ldots, y_k$ that occur in no clause. Number the $y$ variables first, and let both solvers decide the smallest free variable, false first, without restarts. A DPLL solver with unit propagation and chronological backtracking refutes the pigeonhole part once for each of the $2^k$ values of the $y$ variables. The CDCL solver never learns a clause with a $y$ literal, so no jump lands on a level of a $y$ variable, and its number of conflicts does not depend on $k$.

| $h$ | $k$ | DPLL conflicts | CDCL conflicts |
|---|---|---|---|
| 3 | 0 | 9 | 6 |
| 3 | 2 | 36 | 6 |
| 3 | 4 | 144 | 6 |
| 4 | 0 | 52 | 18 |
| 4 | 2 | 208 | 18 |
| 4 | 4 | 832 | 18 |

## Classic examples

- **Conflict-directed backjumping for CSPs.** Prosser's [conflict-directed backjumping](/conflict-directed-backjumping/) keeps a conflict set for each variable and jumps to its latest variable when all values fail. It jumps but does not keep a clause; CDCL keeps the clause as well.
- **GRASP.** Marques-Silva and Sakallah used the conflict-induced clause both to learn and to compute the jump level, which brought non-chronological backtracking to SAT solvers.
- **relsat.** Bayardo and Schrag added conflict-directed backjumping and learning to a DPLL solver for SAT.
- **CDCL solvers.** Chaff, MiniSat and their successors jump to the second highest level of the first UIP clause after every conflict, as in the template.
- **Abstract DPLL.** In the transition system of Nieuwenhuis, Oliveras and Tinelli, the rule Backjump does lines L2 to L6 in one step for any clause $C$ implied by $F'$ that is unit at the target level.

## Variations

- **Chronological backtracking in CDCL.** Nadel and Ryvchin backtrack to $d - 1$ when the jump would undo more than a set number of levels. The asserting literal is then given its real implication level $b$, so the trail is no longer sorted by level, and propagation and conflict analysis must take the largest level of a clause instead of the current level.
- **Partial restarts and trail reuse.** A [restart](/restarts/) jumps to level 0. A solver can instead jump only to the lowest level whose decision would change under the current variable order, since the levels below it would be redone the same way.
- **Backjumping without learning.** In DPLL, the conflict set of the last decision can be kept for one backtrack only and then discarded. This is Prosser's scheme, and it already removes the factor $2^k$ of the example above.
- **Other jump targets.** Any level from $b$ to $d - 1$ makes $C$ unit, and line L6 is sound at each. The lowest one, $b$, is the standard choice, because the new literal then propagates under the fewest decisions.

## Pitfalls

- **A clause that is not asserting.** If $C$ has two literals of the conflict level, it is unit at no level below $d$. Jumping to its second highest level then assigns nothing, and the search can repeat the conflict. This happens when propagation was not complete before a decision.
- **Wrong level for the asserted literal.** The literal $\neg u$ must get level $b$, not the old level $d$ and not the current level of a chronological variant. A wrong level breaks the next conflict analysis and the [watch invariant](/two-watched-literals/).
- **Unit learned clauses.** For a clause of one literal, $b = 0$. The literal is assigned at level 0 and holds for the rest of the search, so its reason can be dropped.
- **Lost phase.** The jump discards the values of many variables that had nothing to do with the conflict. Without [phase saving](/phase-saving/), the solver may choose other values when it redecides them and lose a good partial assignment.
- **Watches pointing at the wrong literal.** The learned clause must watch $\neg u$ and a literal of level $b$. If it watches a literal of a lower level, a later jump above that level leaves the clause unit without the solver noticing.

## Exercises

1. Prove that for every jump target $b'$ with $b \le b' < d$, asserting $\neg u$ at level $b'$ is sound and keeps the progress argument.
2. Show that the vector order in the progress argument is a well-founded order, and use it to bound the number of conflicts of a run without restarts by $(n + 1)^{n + 1}$. Find a better bound when the learned clauses are never deleted.
3. In the example with irrelevant decisions, prove that the CDCL run with $k$ extra variables has exactly as many conflicts as the run with $k = 0$, for any formula in which the $y$ variables occur in no clause.
4. Give a formula and a run where the first UIP clause has $b = d - 1$, so that backjumping and chronological backtracking jump to the same level.

## References
