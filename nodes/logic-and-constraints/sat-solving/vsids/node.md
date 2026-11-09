---
tag: XMSZXA
kind: technique
slug: vsids
name: VSIDS branching heuristic
aliases:
- variable state independent decaying sum
- activity-based branching
- EVSIDS
area: logic-and-constraints/sat-solving
level: advanced
summary: Branch on the free variable with the highest activity. Each conflict raises the activity of the variables involved in it, and old increments fade by a constant factor.
prereqs: [cdcl, clause-learning]
see_also: [phase-saving, restarts, indexed-priority-queue, binary-heap, exponential-moving-average, first-uip, two-watched-literals, dpll]
sources:
  - paper: doi:10.1145/378239.379017
    title: Matthew W. Moskewicz, Conor F. Madigan, Ying Zhao, Lintao Zhang and Sharad Malik, Chaff, engineering an efficient SAT solver, Proceedings of the 38th Design Automation Conference, 2001
    locator: pages 530 to 535 (the five rules of the VSIDS decision heuristic and the measured comparison with GRASP and SATO)
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, Lecture Notes in Computer Science 2919, 2004
    locator: pages 502 to 518 (variable activities bumped during conflict analysis, the growing increment that stands for decay, and the activity heap)
  - paper: "Jia Hui Liang, Vijay Ganesh, Ed Zulkoski, Atulan Zaman and Krzysztof Czarnecki, Understanding VSIDS branching heuristics in conflict-driven clause-learning SAT solvers, Hardware and Software, Verification and Testing (HVC 2015), Lecture Notes in Computer Science 9434, 2015"
    locator: VSIDS activity as an exponential moving average, and experiments on which variables VSIDS selects
  - paper: "Armin Biere and Andreas Fröhlich, Evaluating CDCL variable scoring schemes, Theory and Applications of Satisfiability Testing (SAT 2015), Lecture Notes in Computer Science 9340, 2015"
    locator: the variants of VSIDS, their decay and bump rules, and the move-to-front alternative VMTF
  - paper: "Evguenii Goldberg and Yakov Novikov, BerkMin, a fast and robust SAT-solver, Proceedings of Design, Automation and Test in Europe (DATE 2002), pages 142 to 149"
    locator: the decision rule that picks a variable from the most recent learned clause that is not satisfied
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (decision heuristics, VSIDS and its implementation)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (activity scores, their damping factor and the heap of free variables in the CDCL algorithm)
---

VSIDS (variable state independent decaying sum) is the decision heuristic of [CDCL](/cdcl/) solvers that keeps an activity score for each variable, adds to the score of the variables that take part in each conflict, lets all scores fade by a constant factor over time, and branches on the free variable with the highest score. It was introduced in Chaff (2001), and MiniSat's form of it, sometimes called EVSIDS, is still the base of the default heuristic in most solvers. It is a heuristic: it does not change soundness or completeness, it has no proved bound on the search size, and its benefit is known only from measurements.

## In plain words

At each guess, the solver must choose which open value to guess next. VSIDS keeps a score for each value. Every time the solver hits a dead end, the values that were involved in it get points. Points from long ago count for less and less, because all scores slowly shrink. At each guess, the solver picks the open value with the most points.

The effect is that the solver keeps working on the part of the problem where it has recently hit dead ends. It does not spread its effort over the whole problem. The score does not depend on whether the value is set at the moment, so it does not have to be recomputed when the solver backtracks. A heap keeps the open values ordered by score, so the choice is fast.

## When it applies

- The search learns clauses at conflicts, as in [clause learning](/clause-learning/), so that each conflict names a set of variables that took part in it.
- Decisions are frequent and must be cheap. The score is updated only at conflicts, and the choice costs a heap operation, so the heuristic adds little to the cost of a conflict.
- The formula is large and structured, as in hardware and software verification, where the variables of a conflict tend to be related. On small random formulas, [lookahead](/lookahead-sat/) heuristics, which measure the effect of each choice by propagation, are often better.

## The template

Each variable $v$ has an activity $\mathrm{act}(v) \ge 0$, at first 0. The solver keeps an increment $\mathrm{inc}$, at first 1, a decay factor $0 < \rho < 1$, and a max-heap $H$ of variables ordered by activity.

```pseudo id=main
BUMP-AND-DECAY(S)                             ▷ called after each conflict; S: hole BUMPSET
L1  for each variable v in S do
L2      act(v) ← act(v) + inc; restore the heap order at v
L3      if act(v) > LIMIT then                   ▷ hole LIMIT: MiniSat uses 10^100
L4          for each variable u do act(u) ← act(u) / LIMIT
L5          inc ← inc / LIMIT
L6  inc ← inc / ρ                                ▷ hole DECAY: MiniSat uses ρ = 0.95

ON-UNASSIGN(v)                                ▷ called for each variable that a backtrack frees
L7  if v is not in H then insert v into H

PICK-BRANCH()                                 ▷ called at each decision
L8  repeat
L9      v ← remove the top of H
L10 until v is unassigned or H is empty
L11 return the literal of v with sign POLARITY(v) ▷ hole POLARITY: false first, or phase saving
```

The holes:

- **BUMPSET.** Chaff increments the counters of the literals of each added clause, that is, of the learned clause. MiniSat bumps every variable that the conflict analysis visits: the variables of the learned clause and the variables resolved away on the way to the [first UIP](/first-uip/).
- **DECAY.** Chaff divides all counters by a constant from time to time. MiniSat divides $\mathrm{inc}$ by $\rho$ after each conflict, which has the same effect as multiplying every activity by $\rho$, as Lemma 2 shows.
- **LIMIT.** Floating-point activities grow without bound when $\mathrm{inc}$ grows; lines L3 to L5 scale everything down before an overflow.
- **POLARITY.** Chaff keeps one counter per literal and picks the literal with the highest counter. MiniSat scores variables and picks the sign separately, at first always false, and later by [phase saving](/phase-saving/).

**Correctness.** The heuristic has no effect on soundness: any choice of an unassigned variable keeps CDCL sound and, under the hypotheses of its termination proof, complete. What has to be proved is that PICK-BRANCH finds a free variable when one exists, and what the scores mean.

*Lemma 1 (heap invariant).* Before each call of PICK-BRANCH, every unassigned variable is in $H$. *Proof.* At the start, all variables are in $H$ and none is assigned. A variable leaves $H$ only at line L9. If it is unassigned there, PICK-BRANCH returns it and the solver assigns it. If it is assigned, it stays out of $H$ while it is assigned. A variable becomes unassigned only by a backtrack, and line L7 puts it back. $\blacksquare$

So line L10 stops at an unassigned variable whenever one exists, and since the heap orders by activity, it is the free variable of largest activity. Each assigned variable that line L9 discards was inserted once at line L7 or at the start, so the discards are paid for by the inserts.

*Lemma 2 (the growing increment is a decay).* Consider two solvers that see the same bump sets. Solver A multiplies every activity by $\rho$ after each conflict and always bumps by 1. Solver B bumps by $\mathrm{inc}$ and divides $\mathrm{inc}$ by $\rho$ after each conflict. Then after every conflict, $\mathrm{act}_B(v) = \mathrm{act}_A(v) / \rho^t$ for all $v$, where $t$ is the number of conflicts so far. *Proof.* By induction on $t$. At $t = 0$ both are 0. At conflict $t + 1$, B adds $\mathrm{inc} = \rho^{-t}$ to the bumped variables and then has $\mathrm{inc} = \rho^{-(t+1)}$. A adds 1 and multiplies by $\rho$. So $\mathrm{act}_A'(v) = \rho(\mathrm{act}_A(v) + [v \in S])$ and $\mathrm{act}_B'(v) = \rho^{-t}\mathrm{act}_A(v) + \rho^{-t}[v \in S] = \rho^{-(t+1)}\mathrm{act}_A'(v)$. $\blacksquare$

All activities of B are those of A times one common positive factor, so both rank the variables the same, and they make the same decisions. The rescaling at lines L3 to L5 also multiplies all activities by a common factor and keeps the ranking, except that very small activities can round to 0. B does $O(|S|)$ work per conflict, where A does $O(n)$.

*Lemma 3 (activity is a moving average).* Let $b_i(v) = 1$ if $v$ was bumped at conflict $i$, else 0. After $t$ conflicts, in the form of solver A,

$$\mathrm{act}(v) = \sum_{i=1}^{t} \rho^{\,t-i+1}\, b_i(v),$$

which is $\rho / (1 - \rho)$ times an [exponential moving average](/exponential-moving-average/) of the sequence $b_1(v), \ldots, b_t(v)$ with weight $1 - \rho$, started at 0. *Proof.* Unfold $\mathrm{act}_t = \rho(\mathrm{act}_{t-1} + b_t)$. $\blacksquare$

With $\rho = 0.95$, a bump from $k$ conflicts ago has weight $0.95^k$, so about 0.36 after 20 conflicts and 0.006 after 100. The score thus measures how often a variable took part in recent conflicts. Liang, Ganesh, Zulkoski, Zaman and Czarnecki stated this view and used it to study which variables VSIDS picks.

**Cost.** A bump costs $O(\log n)$ for the heap update, so a conflict costs $O(|S| \log n)$. A decision costs $O(\log n)$ for each variable removed from the heap, and over a run each removal matches an earlier insertion. Chaff's periodic division costs $O(n)$ each time. The space is $O(n)$.

**Example.** Take the run of the [first UIP](/first-uip/) page, with MiniSat's rule and $\rho = 0.95$. The first conflict, on $C_6$, visits $x_5, x_6$, then the reason $C_5$ adds $x_4, x_9$, and the reason $C_4$ adds $x_8$. Each of these gets $+1$, and $\mathrm{inc}$ becomes $1/0.95 \approx 1.0526$. The second conflict, on $C_3$, visits $x_2, x_3, x_4$, then the reason $C_2$ adds $x_1, x_7$. Each gets $+1.0526$.

| variable | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ | $x_7$ | $x_8$ | $x_9$ |
|---|---|---|---|---|---|---|---|---|---|
| after conflict 1 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 1 |
| after conflict 2 | 1.0526 | 1.0526 | 1.0526 | 2.0526 | 1 | 1 | 1.0526 | 1 | 1 |

After the second conflict, the trail is $\neg x_7, \neg x_8, \neg x_9, \neg x_4, x_1$, and the free variables are $x_2, x_3, x_5, x_6$. The next decision takes $x_2$ or $x_3$, at 1.0526, over $x_5$ and $x_6$, at 1: the most recent conflict counts more. Chaff's rule would instead have added 1 only to the literals of the learned clauses, $\neg x_4, x_8, x_9$ and then $x_1, x_4, x_7$.

## Classic examples

- **Chaff.** Moskewicz, Madigan, Zhao, Zhang and Malik gave VSIDS as five rules: a counter for each literal, initially 0; an increment of the counter of each literal of each added clause; the choice of the free literal with the highest counter; random tie-breaking; and periodic division of all counters by a constant. They report that Chaff, with VSIDS and [two watched literals](/two-watched-literals/), was one to two orders of magnitude faster than GRASP and SATO on their benchmarks; the paper does not separate the effect of VSIDS from that of the other parts.
- **MiniSat.** Eén and Sörensson moved the score to variables, bumped all variables seen in conflict analysis, replaced the periodic division by the growing increment of Lemma 2, and kept the free variables in a binary heap. This is the template above.
- **Knuth's CDCL algorithm.** The CDCL algorithm in Section 7.2.2.2 of TAOCP uses the same activity scores with a damping factor and a heap of free variables.

## Variations

- **Changing the decay during the run.** Some solvers start with a smaller $\rho$, which forgets faster, and raise it over time.
- **Variable move-to-front (VMTF).** A bumped variable moves to the front of a list, and the decision takes the first free variable in the list. Biere and Fröhlich compared it with the VSIDS variants; it costs $O(1)$ per bump with a queue and no floating point.
- **Clause-based choice.** Goldberg and Novikov's BerkMin chooses a variable from the most recent learned clause that is not yet satisfied, with activities to choose inside it.
- **Learning-rate scores.** Later heuristics, such as CHB and LRB, score a variable by how often it took part in conflicts while it was assigned, and some solvers switch between them and VSIDS during the run.
- **Ties and the start.** All activities are 0 at the start, so the first decisions follow the heap order of the variables, often their index. Some solvers break ties at random, as Chaff did, or start from a score computed from the input, such as the number of occurrences.

## Pitfalls

- **Overflow.** With $\rho = 0.95$, the growing increment passes $10^{100}$ after about 4500 conflicts and would pass the largest double, about $1.8 \cdot 10^{308}$, after about 13800. Rescale before that, as in lines L3 to L5.
- **Not putting variables back into the heap.** If a backtrack does not reinsert the freed variables, Lemma 1 fails, and the solver can claim that no free variable is left when one is.
- **Decaying all scores at each conflict.** Multiplying $n$ activities after every conflict costs $O(n)$ per conflict. Use the growing increment.
- **Reading too much into the scores.** VSIDS has no proved effect on the search size. Measured gains depend on the benchmarks and on the other parts of the solver, such as [restarts](/restarts/) and [phase saving](/phase-saving/).
- **Mixing up the bump sets.** Bumping only the learned clause and bumping every visited variable give different solvers. Compare heuristics only with the rest of the solver fixed.

## Exercises

1. Show that VSIDS with $\rho$ close to 1 approaches a count of all past conflicts in which a variable took part, and with $\rho$ close to 0 approaches "bumped in the last conflict or not".
2. With $\rho = 0.95$, a variable bumped once in the last conflict and never before competes with a variable bumped in every one of the $k$ conflicts before that, and in none since. For which $k$ does the second variable still have the higher activity?
3. Prove that the rescaling at lines L3 to L5 keeps the order of any two activities in exact arithmetic, and give two doubles whose order it changes in floating point.
4. Give a family of formulas on which the input order of the variables, used to break ties among zero scores, makes the difference between a run with no conflict and a run with many conflicts.

## References
