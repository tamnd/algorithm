---
tag: VM52NJ
kind: technique
slug: clause-learning
name: Clause learning
aliases:
- conflict-driven learning
- nogood learning
- conflict clause learning
- conflict analysis
area: logic-and-constraints/sat-solving
level: advanced
summary: At each conflict of a SAT search, derive by resolution a new clause implied by the formula that rules out the cause of the conflict, and add it to the formula.
prereqs: [implication-graph, first-uip, binary-resolution]
see_also: [cdcl, non-chronological-backtracking, clause-minimization, literal-block-distance, clause-database, nogood-learning, drat-proof, cdcl-simulates-resolution]
sources:
  - paper: doi:10.1109/12.769433
    title: João P. Marques-Silva and Karem A. Sakallah, GRASP, a search algorithm for propositional satisfiability, IEEE Transactions on Computers 48(5), 1999
    locator: pages 506 to 521 (conflict analysis on the implication graph, conflict-induced clauses and their recording)
  - paper: "Roberto J. Bayardo Jr. and Robert C. Schrag, Using CSP look-back techniques to solve real-world SAT instances, Proceedings of AAAI 1997, pages 203 to 208"
    locator: learning in a DPLL solver, and relevance-bounded learning that keeps a learned clause only while few of its literals are unassigned
  - paper: "Lintao Zhang, Conor F. Madigan, Matthew W. Moskewicz and Sharad Malik, Efficient conflict driven learning in a Boolean satisfiability solver, Proceedings of ICCAD 2001, pages 279 to 285"
    locator: learning schemes as cuts of the implication graph and the measured comparison of the schemes
  - paper: doi:10.1613/jair.1410
    title: Paul Beame, Henry Kautz and Ashish Sabharwal, Towards understanding and harnessing the potential of clause learning, Journal of Artificial Intelligence Research 22, 2004
    locator: pages 319 to 351 (learning schemes, asserting clauses, and learned clauses as trivial resolution derivations)
  - paper: "Alexander Nadel and Vadim Ryvchin, Chronological backtracking, Theory and Applications of Satisfiability Testing (SAT 2018), Lecture Notes in Computer Science 10929, 2018"
    locator: conflict analysis and propagation when the solver backtracks chronologically after a conflict
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (conflict analysis, learning schemes and the resolution view of learning)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, 2016
    locator: Chapter 2, Section 2.2 (conflict clauses, the resolution graph of a learned clause and the termination argument)
---

Clause learning is the step of a SAT search that, at each conflict, derives a new [clause](/clause/) that is implied by the formula and false under the current assignment, and adds it to the formula. The new clause comes from a chain of [binary resolution](/binary-resolution/) steps that follow the reasons of the [implication graph](/implication-graph/) back from the false clause, and the standard choice stops at the [first unique implication point](/first-uip/). The learned clause then prevents the same combination of values from coming back, and it tells the search where to jump. Clause learning is one part of [CDCL](/cdcl/): this page covers what is derived at a conflict and why it is sound, and the CDCL page covers the whole loop of decisions, propagation, backjumps, restarts and clause deletion.

## In plain words

A solver that guesses values and then hits a dead end has learned something: some group of its choices cannot all hold at once. Plain backtracking throws this knowledge away. It undoes the last guess and may walk into the same dead end again from a different direction, many times.

Clause learning keeps it. The solver traces the dead end back through the chain of forced values, and finds a small group of values that together caused it. It writes a new rule that says "not all of these together", and adds the rule to the formula. The new rule follows from the old rules, so no solution is lost. From then on, the moment all but one of these values hold, propagation forces the last one the other way, and the dead end is avoided.

## When it applies

- The search keeps a trail of assigned literals with decision levels and a reason clause for each literal forced by [unit propagation](/unit-propagation/), so that the [implication graph](/implication-graph/) is available.
- Propagation runs to completion before each decision, and a conflict, a clause $K$ with all literals false, is handled as soon as it is found. The asserting property below needs both conditions.
- The conflict level $d$ is at least 1. A conflict at level 0 means that $F$ is unsatisfiable, and there is nothing to learn.
- The same scheme works for any propagator that explains its implications by clauses: theory solvers in [DPLL(T)](/dpll-t/), cardinality and [pseudo-Boolean](/pseudo-boolean-sat/) constraints, and finite-domain propagators in constraint solvers, where the learned clauses are called nogoods.

## The template

Write $F'$ for the clause database: the input clauses of $F$ and the clauses learned so far.

```pseudo id=main
LEARN(F', K)                                  ▷ K ∈ F' is false; d ← the largest level in K, d ≥ 1
L1  C ← K
L2  while not STOP(C, d) do                     ▷ hole STOP: first UIP, all UIP, decision
L3      t ← the latest trail literal with ¬t ∈ C and a reason
L4      C ← (C \ {¬t}) ∪ (reason(t) \ {t})      ▷ resolve on the variable of t
L5      NOTE(t, reason(t))                      ▷ hole NOTE: bump activities, mark the clause as used
L6  remove from C the literals false at level 0
L7  C ← MINIMIZE(C)                             ▷ hole MINIMIZE: none, local, recursive
L8  b ← the largest level in C below d, or 0 if there is none
L9  add C to F' with the score SCORE(C)         ▷ hole SCORE: LBD, activity
L10 return C and b                              ▷ the caller jumps to level b and asserts the UIP literal
```

The holes:

- **STOP.** The first UIP scheme stops when $C$ has exactly one literal of level $d$, as on the [first UIP](/first-uip/) page. The decision scheme goes on until the only literal of level $d$ is the negated decision. The all UIP scheme also resolves the literals of lower levels until every level in $C$ has at most one literal; it gives a clause with fewer levels but more resolution steps.
- **NOTE.** Each variable that the analysis visits gets its activity bumped by [VSIDS](/vsids/), and each reason clause used can be marked, so that [clause database reduction](/clause-database-reduction/) keeps clauses that take part in conflicts.
- **MINIMIZE.** [Clause minimization](/clause-minimization/) removes literals whose negations are implied by the other literals of $C$ through their reasons. It keeps $C$ implied and asserting.
- **SCORE.** The [literal block distance](/literal-block-distance/) of $C$, the number of distinct levels in it, is computed here, while all levels are known.

**Correctness.** Four facts hold, for any choice of the holes except where one is named.

*1. Every learned clause has a resolution derivation from $F$.* By induction over the conflicts of the run. Line L1 starts with a clause of $F'$. Each step at line L4 resolves $C$ with $\mathrm{reason}(t)$, a clause of $F'$, on the variable of $t$; the resolvent is implied by its two premises. Line L6 removes literals $q$ with $\neg q$ at level 0; each such $\neg q$ is a unit consequence of $F'$, and resolving with a derivation of the unit clause $\{\neg q\}$ removes $q$. Line L7 is a further sequence of resolution steps, as the minimization page shows. So $C$ is derived from $F'$, and each clause of $F' \setminus F$ was derived from $F$ at an earlier conflict. Joining the derivations gives one from $F$, and by the soundness of resolution, $F \models C$. Within one call, the trail position of the resolved literal drops at each step, so no variable is resolved twice; the derivation is a chain in which each step uses one new side clause, which Beame, Kautz and Sabharwal call a trivial resolution derivation.

*2. The first UIP clause is asserting.* It has exactly one literal $\neg u$ of level $d$, all its literals are false, and $b < d$. After the levels above $b$ are removed, it is unit with $\neg u$. The proof is on the [first UIP](/first-uip/) page; the same holds after MINIMIZE, which never removes $\neg u$, and for any other UIP in place of the first.

*3. An asserting learned clause is new.* Let $C$ be learned at a conflict of level $d$, with the literal $\neg u$ of level $d$ and all other literals of level at most $b < d$. Then $C$ is not in $F'$ before line L9. *Proof.* Let $T$ be the moment when the decision of level $d$ now on the trail was made. Each literal of $C$ other than $\neg u$ was false at $T$, because its level is at most $b < d$, and no backjump below level $d$ has happened since $T$. The variable of $u$ was unassigned at $T$, because its level is $d$. Propagation was complete at $T$ without a conflict, so no clause of $F'$ was unit at $T$, and $C$ was not in $F'$ at $T$. Suppose that $C$ was learned at a later conflict, with its own asserting literal and jump level $b'$. The decision of level $d$ is still on the trail, so $b' \ge d$. The literals of $C$ other than $\neg u$ were false at that conflict with levels at most $b$, so the one literal of the highest level was $\neg u$, and $b'$, the largest level of the others, was at most $b < d$. This is a contradiction. $\blacksquare$

*4. No repeat while the clause is kept.* As long as $C$ stays in $F'$, whenever all literals of $C$ except one are false and propagation is complete without a conflict, the last literal is true. So the combination of values that this conflict blamed never holds again at a decision point. With fact 3, if the solver deletes no learned clause, the clauses learned in one run are pairwise distinct and differ from the input clauses. A clause over $n$ variables picks for each variable one of three options (absent, positive, negative), so a run without deletion has at most $3^n$ conflicts. This gives a termination proof for CDCL without clause deletion; with deletion, the [CDCL](/cdcl/) page gives the argument.

**UNSAT answers.** When a conflict occurs at level 0, every literal of the false clause $K$ is false at level 0, and the complement of each one has a reason clause or is a learned unit clause. Resolving $K$ with these clauses, latest first, removes every literal and yields the empty clause. Together with fact 1, this is a resolution refutation of $F$ with at most as many steps as the solver performed resolutions in the whole run. So the number of resolution steps in a CDCL run on an unsatisfiable formula is at least the size of its shortest resolution refutation, and the exponential [lower bounds for resolution](/haken-resolution-lower-bound/) apply to CDCL.

**Cost.** The analysis visits each literal of the conflict level at most once, and reads each reason once. With one mark per variable for the literals already in $C$ and a counter of the level-$d$ literals, lines L1 to L5 take time linear in the total length of the clauses read. Line L9 adds $|C|$ literals to the database. Each conflict adds one clause, so memory grows with the number of conflicts until [clause database reduction](/clause-database-reduction/) removes some.

**Example.** Take the formula $C_1 = \{x_1, x_2\}$, $C_2 = \{x_1, \neg x_2\}$, $C_3 = \{\neg x_1, x_2\}$, $C_4 = \{\neg x_1, \neg x_2\}$, which is unsatisfiable.

| step | event | trail | clause $C$ |
|---|---|---|---|
| 1 | decide $\neg x_1$ at level 1 | $\neg x_1$ | |
| 2 | $C_1$ is unit, force $x_2$ | $\neg x_1, x_2$ | |
| 3 | $C_2$ is false at level 1 | $\neg x_1, x_2$ | $\{x_1, \neg x_2\}$ |
| 4 | resolve on $x_2$ with $C_1$ | | $\{x_1\}$, one literal of level 1, stop |
| 5 | learn $\{x_1\}$, $b = 0$, jump to level 0, assert $x_1$ | $x_1$ | |
| 6 | $C_3$ is unit, force $x_2$ | $x_1, x_2$ | |
| 7 | $C_4$ is false at level 0 | $x_1, x_2$ | $\{\neg x_1, \neg x_2\}$ |
| 8 | resolve on $x_2$ with $C_3$, then on $x_1$ with $\{x_1\}$ | | the empty clause |

The learned clause $\{x_1\}$ is the resolvent of $C_2$ and $C_1$. The refutation has three steps: $C_2$ and $C_1$ give $\{x_1\}$, $C_4$ and $C_3$ give $\{\neg x_1\}$, and these two give the empty clause. For a larger trace with two conflicts, see the [first UIP](/first-uip/) page, where the first conflict learns $\{\neg x_4, x_8, x_9\}$ and the decision scheme would learn the longer $\{x_1, x_7, x_8, x_9\}$.

## Classic examples

- **GRASP.** Marques-Silva and Sakallah analyzed each conflict on the implication graph, recorded clauses at UIPs, and used them to jump back.
- **relsat.** Bayardo and Schrag added learning and backjumping to a DPLL solver in 1997 and kept a learned clause only while few of its literals were unassigned, which they called relevance-bounded learning.
- **Chaff and MiniSat.** Chaff learned the first UIP clause after Zhang, Madigan, Moskewicz and Malik found it the best of the schemes they measured. MiniSat added recursive [clause minimization](/clause-minimization/), and almost every later CDCL solver follows this design.
- **[Nogood learning](/nogood-learning/) in constraint solvers.** The same idea in constraint satisfaction: a conflict explained by the constraints yields a nogood, a set of variable assignments that cannot be extended to a solution.
- **[DPLL(T)](/dpll-t/).** In SMT solvers, a theory solver explains each theory propagation and theory conflict by a clause over the atoms, and the SAT solver learns from these explanations by the same loop.

## Variations

- **Learning schemes.** The first UIP, second UIP, all UIP and decision schemes differ only in STOP. GRASP could learn several clauses per conflict, one at each UIP. Any scheme that yields an asserting clause keeps facts 2 and 3.
- **Bounded learning.** Keep only clauses up to some size, or only while they are relevant, as in relsat. Modern solvers keep all learned clauses at first and remove the weak ones later by [clause database reduction](/clause-database-reduction/), ranked by the [literal block distance](/literal-block-distance/) or by activity.
- **Learning without backjumping.** A DPLL solver can learn the clause and still backtrack chronologically; the clause then prunes later branches. Nadel and Ryvchin (2018) showed that a CDCL solver can backtrack chronologically after some conflicts and still learn first UIP clauses, with changes to propagation and analysis.
- **Strengthening on the fly.** During the analysis, an intermediate resolvent that is a subset of a reason clause can replace that clause, which removes a literal from the database for free.
- **Proof output.** The solver writes each learned clause to a [DRAT](/drat-proof/) proof, or with its resolution chain to an [LRAT](/lrat-proof/) proof, so an independent checker can confirm an UNSAT answer.

## Pitfalls

- **Incomplete propagation before a decision.** If a clause was unit at a lower level but its literal was assigned later at level $d$, the analysis can stop at a node that is not a UIP, and the learned clause need not be asserting. Propagate to completion before each decision.
- **The wrong conflict level.** After a chronological backtrack the false clause may have no literal at the current level. Take $d$ as the largest level in $K$.
- **Wrong watches for the new clause.** With [two watched literals](/two-watched-literals/), the new clause must watch the asserting literal and a literal of level $b$. Watching a literal of a lower level breaks the watch invariant after a later backjump, and propagation can miss that the clause is unit.
- **Forgetting level 0.** A literal false at level 0 holds in every model of $F'$. Leaving it in the clause makes the clause longer and can make $b$ wrong for a clause whose other literals are all at level 0.
- **Visiting a variable twice.** A variable can appear in several reasons. Without a mark per variable, the count of level-$d$ literals is wrong and the loop stops at the wrong place.
- **Deleting a reason.** A learned clause that is the reason of a literal on the trail must not be deleted, since the next analysis reads it.
- **Unbounded growth.** One clause per conflict over millions of conflicts slows propagation and fills memory. A solver needs a deletion policy.

## Exercises

1. Prove that in one call of LEARN, no variable is resolved on twice, and that the derivation uses each side clause once.
2. Give a run where the first UIP clause is longer than the clause of the all-decision cut, which holds only the negations of decision literals. (Let one decision at a low level force several literals that each feed the conflict.)
3. Show that the all UIP scheme can need more resolution steps than the first UIP scheme, and that its clause has at most one literal per decision level.
4. Prove that with clause deletion allowed, a CDCL solver can learn the same clause twice, by giving a run where a learned clause is deleted and then derived again.
5. Turn the analysis of the example into an LRAT proof: for each learned clause, list the clauses whose unit propagation refutes its negation, in order.

## References
