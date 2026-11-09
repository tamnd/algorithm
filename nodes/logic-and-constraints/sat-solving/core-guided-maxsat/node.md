---
tag: D7BD01
kind: algorithm
slug: core-guided-maxsat
name: Core-guided MaxSAT
aliases:
- core-guided search
- Fu-Malik algorithm
area: logic-and-constraints/sat-solving
level: advanced
summary: Solves MaxSAT with a SAT solver. Each unsatisfiable core of soft clauses gets relaxation variables and an exactly-one constraint, and adds 1 to a lower bound that ends at the optimum.
solves: [partial-max-sat, max-sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, s: the number of soft clauses, c: the optimal cost OPT, T: the time of one SAT call}
  time: {worst: O(c s T)}
  space: {extra: O(m + c s^2)}
properties: {deterministic: true}
history:
  year: 2006
  people: [Zhaohui Fu, Sharad Malik]
  note: Presented at SAT 2006 as a method for partial MaxSAT that calls a SAT solver and relaxes the soft clauses of each unsatisfiable core.
prereqs: [max-sat, partial-max-sat, cdcl, unsat-core]
see_also: [max-sat, partial-max-sat, weighted-max-sat, max-2-sat, unsat-core, totalizer-encoding, sequential-counter-encoding, hitting-set]
sources:
  - paper: doi:10.1007/11814948_25
    title: "Zhaohui Fu and Sharad Malik, On solving the partial MAX-SAT problem, Theory and Applications of Satisfiability Testing (SAT 2006), LNCS 4121, 252 to 265"
    locator: the core-guided algorithm with relaxation variables and one-hot constraints
  - paper: doi:10.1016/j.artint.2013.01.002
    title: "Carlos Ansótegui, María Luisa Bonet and Jordi Levy, SAT-based MaxSAT algorithms, Artificial Intelligence 196 (2013), 77 to 105"
    locator: the correctness proof of Fu-Malik, and the weighted algorithm WPM1
  - paper: doi:10.1007/s10601-013-9146-2
    title: "António Morgado, Federico Heras, Mark Liffiton, Jordi Planes and Joao Marques-Silva, Iterative and core-guided MaxSAT solving, a survey and assessment, Constraints 18 (2013), 478 to 534"
    locator: the family of core-guided algorithms and their comparison
  - paper: "Alexey Ignatiev, António Morgado and Joao Marques-Silva, RC2, an efficient MaxSAT solver, Journal on Satisfiability, Boolean Modeling and Computation 11 (2019), 53 to 64"
    locator: the OLL-based solver RC2
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, 2nd edition (2021)
    locator: the chapter on MaxSAT, core-guided algorithms
---

Core-guided MaxSAT is a family of exact algorithms for [MaxSAT](/max-sat/) that use a [SAT solver](/cdcl/) as an oracle. The first member, by Fu and Malik (2006), solves [partial MaxSAT](/partial-max-sat/): hard clauses must hold, and the goal is to make the fewest soft clauses false. It asks the solver whether all clauses can hold. If not, the solver gives an [unsatisfiable core](/unsat-core/), a set of soft clauses that cannot all hold together with the hard clauses. Each soft clause of the core gets a new relaxation variable that can switch it off, a constraint allows exactly one of these switches to be on, and a lower bound on the cost goes up by 1. When the clauses become satisfiable, the bound is the optimum, and the model is an optimal assignment.

## In plain words

You have a list of must-do rules and a list of wishes, and you want to break as few wishes as possible. First, ask a solver whether all rules and all wishes can hold at once. If yes, you are done, at cost zero.

If not, the solver points at a small group of wishes that cannot all hold together. At least one of them must break, so the cost is at least one. Give each wish of the group an "excuse" switch, and allow exactly one excuse to be used. Ask again. Each time the solver points at a new group, add excuses and add one to the cost. The first time everything holds, the number of groups you saw is the least possible cost.

## The problem

The input is a set $H$ of hard clauses and a list $S$ of soft clauses over $n$ variables. The output is an assignment that satisfies $H$ and makes the fewest clauses of $S$ false, together with that number, or "no solution" when $H$ is unsatisfiable. Weighted versions are handled by the variants below.

## The algorithm

```pseudo id=main
FU-MALIK(H, S)
L1 if H is unsatisfiable then return "no solution"
L2 cost ← 0
L3 loop
L4     ask the SAT solver whether H ∪ S is satisfiable
L5     if it is, with model x, then return (cost, x restricted to the original variables)
L6     K ← the soft clauses of an unsatisfiable core of H ∪ S
L7     for each clause c in K do take a fresh variable r_c and replace c by c ∨ r_c in S
L8     add to H the clauses of "exactly one of the new r_c is true"
L9     cost ← cost + 1
```

A soft clause can be in several cores. Then it gets one relaxation variable per core, and each round's exactly-one constraint is separate. The implementation uses a small iterative [DPLL](/dpll/) solver as the oracle, finds a core by deletion (start with all soft clauses, drop each one if the rest is still unsatisfiable with $H$), which gives a minimal core, and writes "exactly one" as one clause plus all pairwise "not both" clauses. Real solvers take cores from the assumptions interface of a [CDCL](/cdcl/) solver and use compact cardinality encodings such as the [sequential counter](/sequential-counter-encoding/) or the [totalizer](/totalizer-encoding/).

## Example

Soft clauses $(x_1)$, $(x_2)$, $(x_3)$. Hard clauses $(\neg x_1 \vee \neg x_2)$, $(\neg x_1 \vee \neg x_3)$, $(\neg x_2 \vee \neg x_3)$, which say that at most one of the three is true. The optimum is 2: any assignment with one variable true breaks two wishes.

| round | soft clauses | core found | new hard clauses | cost |
|---|---|---|---|---|
| 1 | $x_1$, $x_2$, $x_3$ | $\{x_2, x_3\}$ | exactly one of $r_1, r_2$ | 1 |
| 2 | $x_1$, $x_2 \vee r_1$, $x_3 \vee r_2$ | $\{x_1, x_2 \vee r_1, x_3 \vee r_2\}$ | exactly one of $r_3, r_4, r_5$ | 2 |
| 3 | $x_1 \vee r_3$, $x_2 \vee r_1 \vee r_4$, $x_3 \vee r_2 \vee r_5$ | none: satisfiable | | |

In round 1 the deletion step first drops $x_1$, because $x_2$ and $x_3$ alone already clash with the hard clauses, and keeps the other two. In round 2, $x_1$ forces $x_2$ and $x_3$ false, so both $r_1$ and $r_2$ must be true, which the exactly-one constraint forbids: all three soft clauses are in the core, and $x_2$ and $x_3$ are relaxed a second time. In round 3 the solver finds $x = 100$ with, for example, $r_1 = r_5 = 1$ and the other relaxation variables false, which meets both exactly-one constraints. The algorithm returns cost 2 and $x = 100$.

## Correctness

The key step is Lemma 1 of the proof file. If $K$ is a core, every assignment that satisfies the hard clauses makes some clause of $K$ false. Relaxing $K$ with an exactly-one constraint lowers the optimum by exactly one: an optimal assignment of the old instance turns on the relaxation variable of one false clause of $K$ and saves exactly that clause, and in the other direction, at most one relaxation variable is on, so at most one clause is saved. So after $i$ rounds the optimum of the working instance is $\mathrm{OPT} - i$, the loop ends exactly when this reaches 0, after $\mathrm{OPT}$ rounds, and the returned model, restricted to the original variables, has cost at most $\mathrm{OPT}$, hence exactly $\mathrm{OPT}$. Any core works; minimal cores only keep the constraints small.

## Complexity

There are exactly $\mathrm{OPT}$ rounds that find a core, plus the final call and the call of line L1. With cores found by deletion, each round makes at most $s + 1$ SAT calls, so there are $O(\mathrm{OPT} \cdot s)$ calls in all. Each call is NP-hard in general, so $T$ is exponential in the worst case. The pairwise exactly-one encoding adds $O(|K|^2)$ clauses per core, so the formula grows by $O(\mathrm{OPT} \cdot s^2)$ clauses at most. Real solvers take a core from one CDCL call with assumptions, without deletion, and use encodings of linear size.

The number of rounds being exactly $\mathrm{OPT}$ is a weakness when $\mathrm{OPT}$ is large: core-guided methods do best when only a few soft clauses must be false.

## Properties

- **Exact.** It returns an optimal assignment, and a proof of optimality in the form of $\mathrm{OPT}$ disjoint relaxation steps.
- **Lower bounds first.** The cost rises from 0 to the optimum; each intermediate value is a valid lower bound, while the first model found is already optimal.
- **Oracle-based.** All search happens in the SAT solver, so improvements in SAT solvers carry over.
- **Unweighted.** In the basic form each soft clause has weight 1.

## Variants and improvements

- **WPM1 (Ansótegui, Bonet and Levy 2009).** For weighted soft clauses: take the least weight $w$ in the core, split each clause of weight more than $w$ into a copy of weight $w$, which is relaxed, and a copy with the rest of the weight, and add $w$ to the cost.
- **PM2.** Use one relaxation variable per soft clause and add "at least $j$ of these are true" constraints over unions of cores.
- **MSU3.** Relax all clauses of all cores seen so far with one growing "at most $j$" constraint.
- **OLL and RC2.** Add, for each core, new soft clauses that count how many of its relaxation variables are on, and grow the counters lazily. The RC2 solver, based on OLL, did well in MaxSAT evaluations.
- **Stratification and hardening.** Treat large weights first, and make soft clauses hard when breaking them would cost more than a known upper bound.
- **Hybrids.** Combine with linear search that lowers an upper bound (SAT-UNSAT search), or with an [integer programming](/binary-integer-programming/) solver for the minimum [hitting set](/hitting-set/) of the cores (implicit hitting set methods).

## When to use it

Use a core-guided solver for partial or weighted MaxSAT from industry, such as scheduling, planning, debugging and software package problems, when the optimum is small compared with the number of soft clauses. When the optimum is large, a linear search from an upper bound or an implicit hitting set solver may do better. For a quick, good but not optimal answer on large formulas, use local search such as [WalkSAT](/walksat/) adapted to weights.

## Pitfalls

- **Forgetting the hard check.** If $H$ alone is unsatisfiable, every round finds a core with no soft clause, and the loop never ends. Check $H$ first, as line L1 does.
- **At most one only, with a wrong cost.** "At most one" is enough for correctness, but leaving out the constraint altogether lets every clause of the core switch off for a cost of 1, which gives a wrong, too small, answer.
- **Weights in the basic algorithm.** Fu-Malik counts each core as 1; with weights, use WPM1 or a stratified method.
- **Reusing relaxation variables.** A clause that is in two cores needs a fresh variable for each.
- **Big cores.** A large core makes the pairwise encoding quadratic; minimize cores or use a linear encoding.

## Implementations

## History

MaxSAT was first solved exactly by branch and bound. Fu and Malik introduced the core-guided approach in 2006 for partial MaxSAT, motivated by design debugging and other problems from electronic design automation. Marques-Silva and coworkers developed the MSU family soon after, and Ansótegui, Bonet and Levy gave the weighted algorithm WPM1 in 2009, the PM2 algorithm, and a correctness proof of Fu-Malik based on MaxSAT resolution. Later methods such as OLL and the RC2 solver made core-guided search the main approach of exact MaxSAT solvers, together with implicit hitting set methods.

## References
