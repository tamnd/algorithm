---
tag: ZP2HYE
kind: technique
slug: clause-database-reduction
name: Clause database reduction
aliases:
- clause deletion
- learned clause deletion
- reduceDB
area: logic-and-constraints/sat-solving
level: advanced
summary: "The policy by which a CDCL solver deletes part of its learned clauses at set times, ranked by LBD, activity or size, so that propagation stays fast. Clauses that are reasons are kept."
prereqs: [clause-database, literal-block-distance]
see_also: [cdcl, clause-learning, restarts, vsids, drat-proof, two-watched-literals, incremental-sat]
sources:
  - paper: "Gilles Audemard and Laurent Simon, Predicting learnt clauses quality in modern SAT solvers, Proceedings of the 21st International Joint Conference on Artificial Intelligence (IJCAI 2009), 2009"
    locator: pages 399 to 404 (deletion of half of the learned clauses, ranked by LBD, every 20000 + 500x conflicts)
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, Lecture Notes in Computer Science 2919, 2004
    locator: pages 502 to 518 (activity of learned clauses, the limit on their number, and the rule that locked clauses are not deleted)
  - paper: "Roberto J. Bayardo Jr. and Robert C. Schrag, Using CSP look-back techniques to solve real-world SAT instances, Proceedings of the Fourteenth National Conference on Artificial Intelligence (AAAI 1997), 1997"
    locator: pages 203 to 208 (size-bounded and relevance-bounded learning)
  - paper: doi:10.1145/378239.379017
    title: Matthew W. Moskewicz, Conor F. Madigan, Ying Zhao, Lintao Zhang and Sharad Malik, Chaff, engineering an efficient SAT solver, Proceedings of the 38th Design Automation Conference, 2001
    locator: pages 530 to 535 (lazy deletion of learned clauses that are no longer relevant)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (clause deletion policies)
---

Clause database reduction is the policy by which a [CDCL](/cdcl/) solver, at set times, ranks its [learned clauses](/clause-learning/) by a score such as [LBD](/literal-block-distance/), activity or size, and deletes the worst part of them. It never deletes an input clause or a clause that is the reason of a literal on the trail. The [clause database](/clause-database/) page describes how clauses are stored and how a deletion is carried out; this page is about which clauses to delete and when. Every learned clause is implied by the input, so deleting any of them keeps the solver sound; the cost is that the solver may have to learn some of them again, and that termination needs a separate argument.

## In plain words

A solver learns a new rule at each dead end, often thousands of rules per second. Each rule makes the solver a bit slower, because it must check the rule every time a value changes. Most of these rules are never used again.

So from time to time the solver cleans up. It gives each learned rule a grade, keeps the good ones and throws away a large part of the others. The rules of the original problem always stay. A rule that is now holding up a value on the current path also stays, because the solver may need to look at it to explain the next dead end. Throwing a learned rule away is always safe, because the original rules still say the same thing. The only risk is that the solver has to learn it again.

## When it applies

- The solver learns clauses without bound, as CDCL does. Without reduction, memory grows with the number of conflicts, and [propagation](/two-watched-literals/) slows down because the watch lists grow.
- Each learned clause can be given a score that is cheap to keep: the LBD from the time of learning, an activity bumped when the clause takes part in conflict analysis, or the length.
- The solver can tell which clauses are locked, that is, the reason of a literal on the trail.

## The template

```pseudo id=main
REDUCE-IF-DUE()                                ▷ called at a decision point, after full propagation
L1  if conflicts < next then return              ▷ hole SCHEDULE
L2  K ← the learned clauses that are not locked and not PROTECTED   ▷ hole PROTECT
L3  sort K from worst to best by SCORE           ▷ hole SCORE
L4  delete the first ⌊f · |K|⌋ clauses of K       ▷ hole FRACTION
L5  k ← k + 1
L6  next ← conflicts + a + b · k                  ▷ the next interval is longer by b
L7  if much of the arena is wasted then collect garbage
```

The holes:

- **SCHEDULE.** When to reduce. In the arithmetic schedule above, the $k$th interval between reductions is $a + b(k-1)$ conflicts; Glucose (2009) used $a = 20000$ and $b = 500$. MiniSat instead reduces when the number of learned clauses passes a limit, which starts at a fixed share of the number of input clauses and grows geometrically.
- **PROTECT.** Clauses that are never deleted besides the locked ones: in many solvers, clauses with LBD at most 2 and binary clauses.
- **SCORE.** LBD, smaller is better, with ties broken by length or activity; or clause activity, larger is better, which MiniSat bumps when a clause takes part in conflict analysis and decays at each conflict, like [VSIDS](/vsids/) does for variables; or length.
- **FRACTION.** The share $f$ deleted, often $1/2$.

**Correctness.** Let $F$ be the input and $\Delta$ the learned clauses at some time.

1. *Equivalence.* Each clause of $\Delta$ is implied by $F$, as the clause learning page proves. So for every subset $S \subseteq \Delta$, the formula $F \wedge S$ has exactly the models of $F$. Deletion removes clauses of $\Delta$ only, so the solver always works on a formula equivalent to $F$, and a model it returns satisfies every clause of $F$, which it still holds.
2. *Locked clauses.* If a literal on the trail has reason clause $D$, conflict analysis may resolve on $D$ at the next conflict, and the [implication graph](/implication-graph/) must have $D$ to give the edges into that literal. Line L2 keeps every reason, so every resolution step of a later analysis uses a clause that is in $F$ or in $\Delta$, and every new learned clause is still implied by $F$.
3. *Propagation stays complete.* REDUCE runs after full propagation, when no clause is unit with an unassigned literal and no clause is false. Removing clauses keeps this true of the rest, and the watch invariant of each remaining clause does not change.
4. *Termination.* Deletion breaks the counting argument "at most $3^n$ distinct learned clauses", because a deleted clause can be learned again. The [CDCL](/cdcl/) page proves termination with deletion when the restart intervals grow without bound. With deletion and a restart policy of bounded intervals, no termination proof is known.

**Cost.** One reduction sorts $m$ candidates in $O(m \log m)$ time and deletes in $O(1)$ each; the watch entries go at the next garbage collection or during propagation. For the size of the database, take the arithmetic schedule with interval $I_k = a + b(k-1)$, $f = 1/2$, and no protected or locked clauses. Let $D_k$ be the number of learned clauses just before reduction $k$. Then $D_1 = I_1$, and $D_{k+1} \le (D_k + 1)/2 + I_{k+1}$, so by induction $D_k \le 2 I_k + 1$, since the intervals grow. After $C$ conflicts, $k$ reductions have run with $a k + b k(k-1)/2 \le C$, so $k \le 1 + \sqrt{2C/b}$. Until the next reduction the database holds at most $D_{k+1} \le 2 I_{k+1} + 1 = 2(a + bk) + 1$ learned clauses, which is $O(a + b + \sqrt{bC})$. So the arithmetic schedule keeps the database at about the square root of the number of conflicts, while learning keeps adding clauses in proportion to them.

**Example.** Suppose six learned clauses $L_1, \ldots, L_6$ have LBD 2, 5, 3, 4, 6 and 3, and $L_5$ is locked. With PROTECT "LBD at most 2", SCORE "larger LBD is worse" and $f = 1/2$, the candidates are $L_2$, $L_3$, $L_4$ and $L_6$, sorted as $L_2$ (5), $L_4$ (4), then $L_3$ and $L_6$ (3). The first two, $L_2$ and $L_4$, are deleted. $L_5$ stays although its LBD of 6 is the worst, because it is a reason. On an unsatisfiable random 3-CNF with 200 variables and 852 clauses, the Python code of the [CDCL](/cdcl/) page, with Luby restarts, gave the following.

| schedule | conflicts | learned clauses at the end | most learned clauses at once | seconds |
|---|---|---|---|---|
| no deletion | 14627 | 14620 | 14620 | 22.6 |
| $a = 2000$, $b = 300$ | 15256 | 5146 | 5752 | 11.9 |
| $a = 300$, $b = 50$ | 17128 | 1642 | 2567 | 10.0 |

More deletion means more conflicts, since some clauses are learned again, but each conflict is cheaper, because the watch lists are shorter. Such numbers depend on the instance and on the solver.

## Classic examples

- **Size-bounded and relevance-bounded learning.** Bayardo and Schrag kept a learned clause only while it was short, or only while few of its literals were unassigned. This bounded the database by a fixed size, at the price of forgetting long clauses at once.
- **MiniSat.** It deletes about half of the learned clauses not locked, those with the lowest activity, when their number passes the limit, and it never deletes binary learned clauses.
- **Glucose.** It ranks by LBD, keeps glue clauses, and deletes half of the rest on the arithmetic schedule. Its measured effect is reported on the [LBD](/literal-block-distance/) page.

## Variations

- **Tiers.** Many recent solvers keep three groups: a core of clauses with LBD at most 2, kept for ever; a middle tier with LBD up to a second bound, kept while it is used now and then; and a local tier ranked by activity, half of which is deleted at each reduction.
- **Used flags.** A clause that took part in a conflict analysis since the last reduction is spared once, whatever its score.
- **Updated LBD.** When a clause takes part in conflict analysis, its LBD is computed again under the current trail, and the smaller value is stored; a clause can thus move to a better tier.
- **Inprocessing.** Between reductions, solvers also remove learned clauses that are subsumed by others or satisfied at level 0, which is exact and not a heuristic. See [subsumption](/clause-subsumption/).
- **Proof logging.** A solver that writes a [DRAT](/drat-proof/) proof logs each deletion as a delete line, so that the checker can drop the clause too.

## Pitfalls

- **Deleting a locked clause.** The next conflict analysis reads the reason of a literal that no longer exists. Test that the clause is the reason of its first literal, and that the literal is assigned, before deleting.
- **Deleting at the wrong time.** Reducing in the middle of propagation, while some watch lists are being walked, can drop a clause that is about to become unit and corrupts the walk.
- **Deleting input clauses.** Input clauses are needed for soundness. Only clauses proved redundant, for example by subsumption, may go.
- **Forgetting proof lines.** In DRAT logging, a deletion that is not logged makes the checker slow, and a clause logged as deleted but still used by the solver makes the proof wrong.
- **Too aggressive a policy.** Deleting most clauses after short intervals makes the solver learn the same clauses again and again; it also loses the termination guarantee unless the restart intervals grow.

## Exercises

1. Prove the bound $D_k \le 2 I_k + 1$ in detail, and extend it to the case where $P$ clauses are protected.
2. Show that a policy that deletes all learned clauses after every conflict, together with restarts after every conflict, can make CDCL run for ever on an unsatisfiable formula.
3. Give a geometric schedule with intervals $a g^{k-1}$ and find the growth of the database size in terms of the number of conflicts.

## References
