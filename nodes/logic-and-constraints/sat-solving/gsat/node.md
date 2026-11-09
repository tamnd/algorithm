---
tag: BW0R7G
kind: algorithm
slug: gsat
name: GSAT
aliases:
- greedy SAT
area: logic-and-constraints/sat-solving
level: core
summary: Greedy local search for SAT. From a random assignment, flip the variable that most increases the number of satisfied clauses, even if no flip helps; restart after MAX-FLIPS flips.
solves: [sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, k: the largest clause size, t: MAX-TRIES, f: MAX-FLIPS}
  time: {worst: O(t f m k)}
  space: {extra: O(n + m)}
properties: {deterministic: false, exact: false}
history:
  year: 1992
  people: [Bart Selman, Hector Levesque, David Mitchell]
  note: Presented at AAAI-92 as a greedy local search that solved hard random 3-CNF formulas beyond the reach of the DPLL solvers of the time.
prereqs: [sat, local-search, conjunctive-normal-form]
see_also: [walksat, probsat, schoning-algorithm, min-conflicts, tabu-search, simulated-annealing, satisfiability-threshold, max-sat]
sources:
  - paper: "Bart Selman, Hector Levesque and David Mitchell, A new method for solving hard satisfiability problems, Proceedings of the 10th National Conference on Artificial Intelligence (AAAI-92), 440 to 446"
    locator: the GSAT procedure and the experiments on random 3-SAT and graph coloring
  - paper: "Bart Selman and Henry A. Kautz, Domain-independent extensions to GSAT, solving large structured satisfiability problems, Proceedings of the 13th International Joint Conference on Artificial Intelligence (IJCAI-93), 290 to 295"
    locator: GSAT with random walk, clause weights and averaging in
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, 2nd edition (2021)
    locator: the chapter on stochastic local search (GSAT and its variants)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2 (2022)
    locator: Section 7.2.2.2, Satisfiability (random walks and local search)
---

GSAT is a greedy [local search](/local-search/) method for the [satisfiability problem](/sat/), by Selman, Levesque and Mitchell (1992). It starts from a random assignment and repeatedly flips the variable whose flip gives the largest number of satisfied clauses, even when that number goes down or stays the same. After MAX-FLIPS flips without a model it restarts, up to MAX-TRIES times. GSAT is incomplete: it finds models, often fast, but it cannot prove that a formula has none, and no general bound on its chance of success is known. Its results are measured, not proved. Its successor [WalkSAT](/walksat/) adds random moves restricted to false clauses and usually does better.

## In plain words

You want to set many switches so that a list of rules all hold. Set them at random. Now look at each switch in turn and count how many rules would hold if you flipped it. Flip the switch with the best count, and repeat.

Sometimes no flip makes things better. GSAT flips the best switch anyway, even if this makes no change or one more rule fails, because this lets it move across flat regions instead of getting stuck. If after many flips the rules still do not all hold, it starts over from a new random setting. When all rules hold, it stops. If no setting works, it keeps trying until its budget runs out, and so its "no" is only a guess.

## The problem

The input is a CNF formula $F$ with $n$ variables and $m$ clauses, and two limits, MAX-TRIES and MAX-FLIPS. The output is a model of $F$, or "no model found". GSAT does not decide satisfiability: "no model found" is also the output on some satisfiable formulas.

## The algorithm

For an assignment $x$ and a variable $v$, $\mathrm{make}(v)$ is the number of false clauses that flipping $v$ makes true, and $\mathrm{break}(v)$ is the number of true clauses that flipping $v$ makes false. The *score* $\mathrm{make}(v) - \mathrm{break}(v)$ is the change in the number of satisfied clauses.

```pseudo id=main
GSAT(F, n, MAX-TRIES, MAX-FLIPS)
L1 for t ← 1 to MAX-TRIES do
L2     x ← a uniformly random assignment
L3     for f ← 0 to MAX-FLIPS do
L4         if x satisfies F then return x
L5         compute make(v) − break(v) for each variable v
L6         v ← a variable with the largest score, ties broken uniformly at random
L7         flip v in x                         ▷ also when the largest score is ≤ 0
L8 return "no model found"
```

The flip of line L7 is made after the check of line L4, so each try makes at most MAX-FLIPS flips. Moves with score 0 are called *sideways* moves, and Selman, Levesque and Mitchell reported that allowing them matters a lot: GSAT spends much of its time on plateaus where many assignments have the same number of false clauses. Good values of MAX-FLIPS and MAX-TRIES are found by experiment; the implementation uses MAX-FLIPS $= 5n$ by default.

The implementation recomputes all scores in one pass over the clauses at each flip, using the rule that a false clause adds 1 to the make count of each of its variables, and a clause with exactly one true literal adds 1 to the break count of that literal's variable.

## Example

Take the five clauses

$$(x_1 \vee x_2) \wedge (\neg x_1 \vee x_3) \wedge (\neg x_3 \vee \neg x_2) \wedge (x_2 \vee x_3) \wedge (\neg x_1 \vee \neg x_2 \vee \neg x_3),$$

which have the two models $010$ and $101$. Start from $x = 000$. The clauses $(x_1 \vee x_2)$ and $(x_2 \vee x_3)$ are false.

| variable | make | break | score | why |
|---|---|---|---|---|
| $x_1$ | 1 | 1 | 0 | it fixes $(x_1 \vee x_2)$ but breaks $(\neg x_1 \vee x_3)$, whose only true literal is $\neg x_1$ |
| $x_2$ | 2 | 0 | 2 | it fixes both false clauses; $(\neg x_3 \vee \neg x_2)$ keeps $\neg x_3$ |
| $x_3$ | 1 | 0 | 1 | it fixes $(x_2 \vee x_3)$ only |

Line L6 picks $x_2$, and after the flip $x = 010$ satisfies all five clauses, so line L4 returns it at the next step. Had the start been a local maximum, with every score at most 0, line L7 would still flip a variable of score 0 or the least bad one.

## Correctness

Line L4 returns only an assignment that satisfies every clause, so each answer is a model. The loops are bounded, so GSAT stops after at most MAX-TRIES $\times$ MAX-FLIPS flips. The score is exactly the change in the number of satisfied clauses: a clause without $v$ keeps its value, and a clause with $v$ either gains, which make counts, or loses, which break counts. The proof file of this page gives the details, including the rules that the implementation uses to compute make and break.

No completeness is claimed. On a formula with no model, GSAT reports "no model found", which is not a proof. On a formula with a model, it may also report "no model found": no general lower bound on its chance of success is known, and the greedy rule can cycle among a few assignments. For a method with a proved bound, see [Schöning's algorithm](/schoning-algorithm/), which flips a random variable of a false clause instead of the best one.

## Complexity

One pass over the clauses computes all scores in $O(mk)$ time, where $k$ is the largest clause size, so the worst case time is $O(t f m k)$ for $t$ tries of $f$ flips. Real implementations keep the scores up to date: a flip of $v$ changes only the scores of variables that share a clause with $v$, and a bucket structure gives the best score quickly. The extra space is $O(n + m)$, or $O(mk)$ with lists of occurrences.

These bounds say nothing about the number of flips needed to find a model, which is the real cost. That number is measured by experiment.

## Properties

- **Incomplete.** It cannot prove unsatisfiability, and it may miss models.
- **Greedy with sideways moves.** It always takes the best flip, even when the best is not an improvement.
- **Global choice.** Unlike [WalkSAT](/walksat/), it considers all $n$ variables at each step, including those in no false clause.
- **Anytime.** The best assignment seen so far is a heuristic answer for [MAX-SAT](/max-sat/).

## Variants and improvements

- **GSAT with random walk (GWSAT).** With probability $p$, flip a random variable of a random false clause instead of the best variable (Selman and Kautz 1993). This led to [WalkSAT](/walksat/).
- **Clause weights.** Give each clause a weight, increase the weights of clauses that stay false at the end of a try, and use weighted scores. This helps on structured formulas.
- **Tabu GSAT.** Forbid flipping a variable again for a fixed number of steps, as in [tabu search](/tabu-search/).
- **HSAT.** Break ties in favor of the variable flipped longest ago.
- **Min-conflicts.** For general constraint problems, the [min-conflicts heuristic](/min-conflicts/) uses the same greedy idea, usually restricted to variables in violated constraints.

## When to use it

GSAT is now mostly of historical and teaching value. For satisfiable random formulas, [WalkSAT](/walksat/) and [probSAT](/probsat/) are faster in reported experiments. For structured formulas from industry, and for any need to prove unsatisfiability, use a [CDCL](/cdcl/) solver. A greedy step like that of GSAT is still a common part of [MAX-SAT](/max-sat/) heuristics.

## Pitfalls

- **Treating "no model found" as UNSAT.** GSAT never proves unsatisfiability.
- **Forbidding sideways moves.** If line L7 flips only when the score is positive, GSAT stops at the first plateau, which is common on hard formulas.
- **Deterministic ties.** Breaking ties always toward the smallest index can make GSAT cycle among the same assignments. Break ties at random.
- **Repeated literals.** A clause such as $(x_1 \vee x_1 \vee x_2)$ must be reduced first, or a true $x_1$ is counted twice and the break counts are wrong.
- **Too few restarts or flips.** The right limits depend on the formula and are found by experiment.

## Implementations

## History

Selman, Levesque and Mitchell introduced GSAT at AAAI-92. They reported that it found models of hard random 3-CNF formulas near the ratio of 4.3 clauses per variable, with several hundred variables, which a DPLL-based solver of the time could not solve, and that it also worked on encoded graph coloring and N-queens problems. These are measured results. Gu also studied local search for SAT around the same time. Selman and Kautz added random walk moves in 1993, and Selman, Kautz and Cohen turned them into WalkSAT in 1994.

## References
