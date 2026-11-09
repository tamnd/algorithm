---
tag: ZXRJVG
kind: problem
slug: partial-max-sat
name: Partial MaxSAT
aliases:
- partial maximum satisfiability
area: logic-and-constraints/sat-solving
level: core
summary: Clauses are hard or soft. Find an assignment that satisfies every hard clause and the most soft clauses (or the most soft weight). No approximation ratio is possible unless P = NP.
prereqs: [max-sat, sat, conjunctive-normal-form]
see_also: [max-sat, weighted-max-sat, core-guided-maxsat, unsat-core, hitting-set, totalizer-encoding, sat, cdcl]
sources:
  - paper: doi:10.1007/11814948_25
    title: "Zhaohui Fu and Sharad Malik, On solving the partial MAX-SAT problem, Theory and Applications of Satisfiability Testing (SAT 2006), LNCS 4121, 252 to 265"
    locator: the problem definition and the core-guided algorithm
  - paper: doi:10.1016/j.artint.2013.01.002
    title: "Carlos Ansótegui, María Luisa Bonet and Jordi Levy, SAT-based MaxSAT algorithms, Artificial Intelligence 196 (2013), 77 to 105"
    locator: weighted partial MaxSAT, WPM1 and PM2
  - paper: doi:10.1007/s10601-013-9146-2
    title: "António Morgado, Federico Heras, Mark Liffiton, Jordi Planes and Joao Marques-Silva, Iterative and core-guided MaxSAT solving, a survey and assessment, Constraints 18 (2013), 478 to 534"
    locator: linear search, core-guided search and their comparison on partial MaxSAT
  - paper: doi:10.1007/s10817-007-9084-z
    title: "Mark H. Liffiton and Karem A. Sakallah, Algorithms for computing minimal unsatisfiable subsets of constraints, Journal of Automated Reasoning 40 (2008), 1 to 33"
    locator: the hitting set duality between minimal correction sets and minimal unsatisfiable subsets
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, 2nd edition (2021)
    locator: the chapters on MaxSAT
  - url: "https://maxsat-evaluations.github.io/"
    locator: the MaxSAT Evaluations, whose unweighted and weighted tracks are partial MaxSAT
---

Partial MaxSAT splits the clauses of a CNF formula into *hard* clauses, which must be true, and *soft* clauses, which may be false at a cost. The goal is an assignment that satisfies every hard clause and as many soft clauses as possible. With weights on the soft clauses it is *weighted partial MaxSAT*, the most general form used by solvers and in the MaxSAT Evaluations. With no soft clauses it is [SAT](/sat/); with no hard clauses it is [MAX-SAT](/max-sat/). Because even finding a feasible assignment is NP-complete, no polynomial algorithm can guarantee any approximation ratio unless P = NP. Exact solvers, such as the [core-guided](/core-guided-maxsat/) algorithms that started with Fu and Malik (2006), solve many large instances from industry.

## In plain words

You have yes-or-no choices and two lists of rules. The rules on the first list are laws: every one must hold. The rules on the second list are wishes: meet as many as you can. A solution must obey all laws, and among such solutions you want the one that meets the most wishes.

If the laws alone cannot all hold, there is no solution at all. Checking that is already as hard as the satisfiability problem, so no fast method can promise even a rough answer in all cases. But real problems often have laws that are easy to satisfy, and modern solvers, which call a SAT solver many times, find the best answer for many of them.

## Definition

The input is a set $H$ of hard clauses and a list $S = (C_1, \ldots, C_s)$ of soft clauses over $x_1, \ldots, x_n$, optionally with weights $w_j > 0$ on the soft clauses. An assignment is *feasible* if it satisfies every clause of $H$. Its cost is the number, or total weight, of the soft clauses it makes false. The output is a feasible assignment of least cost, or "infeasible" when $H$ is unsatisfiable.

The set of soft clauses that an optimal assignment makes false is a minimum *correction set*: removing it from $S$ leaves $H \cup S$ satisfiable. Every [unsatisfiable core](/unsat-core/) of $H \cup S$ meets every correction set, and the minimal correction sets are exactly the minimal [hitting sets](/hitting-set/) of the minimal cores.

## Variants

- **Unweighted partial MaxSAT.** All soft clauses have weight 1. The [Fu-Malik algorithm](/core-guided-maxsat/) was designed for this case.
- **Weighted partial MaxSAT.** Soft clauses carry weights; see [weighted MaxSAT](/weighted-max-sat/).
- **Group MaxSAT.** Soft constraints are groups of clauses that are satisfied or relaxed together.
- **MaxSAT with assumptions and incremental MaxSAT.** Solve a sequence of related instances, reusing the work.
- **Minimal correction sets.** Find a subset-minimal, not minimum, set of soft clauses to drop. This is easier and is used in diagnosis.

## Examples

Hard clauses $(\neg x_1 \vee \neg x_2)$ and $(x_1 \vee x_3)$; soft clauses $(x_1)$, $(x_2)$, $(\neg x_3)$.

- The hard clauses forbid $x_1 = x_2 = 1$, and require $x_1$ or $x_3$.
- If $x_1 = 0$, then $x_3 = 1$, so $(x_1)$ and $(\neg x_3)$ are both false: cost at least 2.
- If $x_1 = 1$, then $x_2 = 0$, and $(x_2)$ is false; $x_3 = 0$ satisfies $(\neg x_3)$: cost 1.

So the optimum is cost 1, reached only by $x = 100$, which a brute-force check over all 8 assignments confirms. The soft clauses $(x_1)$ and $(\neg x_3)$ together with the hard clause $(x_1 \vee x_3)$ are not a core, but $(x_1), (x_2)$ with $(\neg x_1 \vee \neg x_2)$ are: one of $x_1$ and $x_2$ must give way.

## Known algorithms

- **Check the hard clauses first.** If $H$ is unsatisfiable, answer "infeasible". This is one SAT call.
- **Core-guided search.** Find a core of soft clauses with a [CDCL](/cdcl/) solver, relax it, and raise a lower bound, until the formula becomes satisfiable: Fu and Malik (2006), WPM1, PM2, OLL and the RC2 solver. See [core-guided MaxSAT](/core-guided-maxsat/), whose correctness proof covers this problem.
- **Linear search, SAT-UNSAT.** Add a relaxation variable $b_j$ to each soft clause, find a model, and add a constraint "fewer than $c$ of the $b_j$ are true", where $c$ is the current cost, with an encoding such as the [totalizer](/totalizer-encoding/); repeat until unsatisfiable. The last model is optimal.
- **Implicit hitting sets.** Alternate between finding cores and computing a minimum-cost hitting set of them.
- **Branch and bound.** Search with lower bounds from inconsistent subsets, treating hard clauses as constraints of infinite weight.
- **Local search.** Keep the hard clauses satisfied, or weight them heavily, and use local moves; this gives good feasible solutions without a proof of optimality.

## Bounds

- **NP-hard to solve.** It contains MAX-SAT.
- **No approximation.** Suppose a polynomial algorithm returned a feasible assignment whenever one exists, with any guarantee on the cost. Run it on $H$ with no soft clauses: it would decide [SAT](/sat/). So no polynomial approximation algorithm with any ratio exists unless P = NP. This is why partial MaxSAT is studied with exact solvers, not with approximation algorithms.
- **Easy hard parts.** When $H$ is in a tractable class, such as [Horn](/horn-sat/) or [2-CNF](/2-sat/), feasibility is easy, but optimization stays NP-hard in general, since MAX-2-SAT is already hard with $H$ empty.
- **Number of SAT calls.** Core-guided search makes $\mathrm{OPT} + 1$ calls that find a core or a model, plus the work of finding cores; linear search makes at most $s + 1$ calls.

## Reductions

- **To weighted MaxSAT.** Give each hard clause weight $1 + \sum_j w_j$. An optimal weighted solution satisfies all hard clauses when they are satisfiable.
- **From MAX-SAT and from SAT.** No hard clauses, and no soft clauses, respectively.
- **To pseudo-Boolean optimization and integer programming.** Hard clauses are constraints, and soft clauses get indicator variables in the objective.
- **Minimal correction sets and cores.** By the hitting set duality, a minimum-cost hitting set of all minimal cores is an optimal correction set; this is the basis of implicit hitting set solvers.

## Applications

Partial MaxSAT is the form in which most practical MaxSAT problems are stated. Hard clauses encode the rules of the domain and soft clauses the preferences. Examples are software package upgrades (install what is requested, change as little as possible), design debugging and fault localization (explain a failing test with the fewest faulty gates or statements), course timetabling, scheduling with soft deadlines, and planning with preferences.

## References
