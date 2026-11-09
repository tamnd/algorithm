---
tag: T3EJBM
kind: algorithm
slug: walksat
name: WalkSAT
aliases:
- WSAT
area: logic-and-constraints/sat-solving
level: core
summary: Local search for SAT. Pick a random false clause and flip one of its variables, a free one if some flip breaks no clause, else with noise p a random one, else the one that breaks fewest.
solves: [sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, k: the largest clause size, d: the largest number of clauses that contain one variable, t: MAX-TRIES, f: MAX-FLIPS}
  time: {worst: O(t (f k d + m k))}
  space: {extra: O(n + m k)}
properties: {deterministic: false, exact: false}
history:
  year: 1994
  people: [Bart Selman, Henry A. Kautz, Bram Cohen]
  note: Presented at AAAI-94 as a noise strategy for local search, in which every flip is restricted to a variable of a false clause.
prereqs: [sat, local-search, conjunctive-normal-form]
see_also: [gsat, probsat, schoning-algorithm, survey-propagation, satisfiability-threshold, max-sat, cdcl, min-conflicts]
sources:
  - paper: "Bart Selman, Henry A. Kautz and Bram Cohen, Noise strategies for improving local search, Proceedings of the 12th National Conference on Artificial Intelligence (AAAI-94), 337 to 343"
    locator: the WalkSAT procedure with the freebie, noise and greedy moves, and the experiments
  - paper: "Bart Selman, Henry A. Kautz and Bram Cohen, Local search strategies for satisfiability testing, in Cliques, Coloring, and Satisfiability, DIMACS Series in Discrete Mathematics and Theoretical Computer Science 26 (1996), 521 to 532"
    locator: the description of WSAT and the comparison with GSAT
  - paper: "David McAllester, Bart Selman and Henry Kautz, Evidence for invariants in local search, Proceedings of the 14th National Conference on Artificial Intelligence (AAAI-97), 321 to 326"
    locator: the Novelty and R-Novelty rules and the noise tuning experiments
  - paper: "Holger H. Hoos, An adaptive noise mechanism for WalkSAT, Proceedings of the 18th National Conference on Artificial Intelligence (AAAI-02), 655 to 660"
    locator: adaptive noise
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications (2004)
    locator: Chapter 6, the WalkSAT family
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, 2nd edition (2021)
    locator: the chapter on stochastic local search
---

WalkSAT is a [local search](/local-search/) method for the [satisfiability problem](/sat/), by Selman, Kautz and Cohen (1994). At each step it picks a random false clause and flips one of its variables. If some variable of that clause can be flipped without making any true clause false, it flips such a variable. If not, with a fixed probability $p$, the noise, it flips a random variable of the clause, and otherwise the variable whose flip makes the fewest true clauses false. Every flip makes the chosen clause true. WalkSAT is incomplete: it finds models, often much faster than [GSAT](/gsat/), but it cannot prove that a formula has none. Its speed is measured by experiment, not proved.

## In plain words

You want to set many switches so that a list of rules all hold. Set them at random. Now pick one broken rule at random. Each rule names a few switches, and flipping any of them fixes this rule. But a flip can break other rules that now depend on that switch alone.

If one of the switches can be flipped without breaking any other rule, flip it. If not, toss a biased coin. On heads, flip a random switch of the rule. On tails, flip the switch that breaks the fewest other rules. Repeat until no rule is broken, and start again from a new random setting if it takes too long. The coin tosses keep the search from getting stuck in one place.

## The problem

The input is a CNF formula $F$ with $n$ variables and $m$ clauses, a noise value $p$ between 0 and 1, and two limits, MAX-TRIES and MAX-FLIPS. The output is a model of $F$, or "no model found". WalkSAT does not decide satisfiability: "no model found" is also the output on some satisfiable formulas.

## The algorithm

For an assignment $x$ and a variable $v$, $\mathrm{break}(v)$ is the number of clauses that are true under $x$ and become false when $v$ is flipped. A clause becomes false exactly when its only true literal is on $v$.

```pseudo id=main
WALKSAT(F, n, p, MAX-TRIES, MAX-FLIPS)
L1 for t ← 1 to MAX-TRIES do
L2     x ← a uniformly random assignment
L3     for f ← 0 to MAX-FLIPS do
L4         if x satisfies F then return x
L5         C ← a uniformly random false clause
L6         if some variable of C has break 0 then v ← a random one of them           ▷ freebie move
L7         else with probability p: v ← a uniformly random variable of C          ▷ noise move
L8         else v ← a variable of C with the least break, ties at random          ▷ greedy move
L9         flip v in x
L10 return "no model found"
```

This is the SKC rule, named after the three authors. Three things make it differ from [GSAT](/gsat/).

- **Focus.** Only variables of one false clause are candidates, so each flip fixes at least that clause. GSAT considers all $n$ variables.
- **Break, not score.** The greedy move looks only at the break count, not at the make count. Selman, Kautz and Cohen reported that this works better.
- **Noise.** The random move of line L7 lets the search leave a local minimum without a restart.

The implementation keeps, for each clause, the number of its true literals, and keeps the false clauses in a list with a position index, so that line L5 takes $O(1)$ time and a flip of $v$ updates only the clauses that contain $v$. The break count of a variable is computed from these counts. The default noise is $p = 0.5$ and the default MAX-FLIPS is $100n$.

## Example

Take the six clauses

$$(x_2 \vee x_3 \vee \neg x_4) \wedge (x_1 \vee x_3 \vee x_4) \wedge (x_1 \vee \neg x_3) \wedge (\neg x_1 \vee x_3) \wedge (\neg x_1 \vee x_2) \wedge (\neg x_3 \vee x_4),$$

which have the two models $0101$ and $1111$. Start from $x = 0000$. Only $(x_1 \vee x_3 \vee x_4)$ is false, so line L5 picks it.

| variable | break | clauses that become false |
|---|---|---|
| $x_1$ | 2 | $(\neg x_1 \vee x_3)$ and $(\neg x_1 \vee x_2)$, whose only true literal is $\neg x_1$ |
| $x_3$ | 2 | $(x_1 \vee \neg x_3)$ and $(\neg x_3 \vee x_4)$ |
| $x_4$ | 1 | $(x_2 \vee x_3 \vee \neg x_4)$ |

No break is 0, so there is no freebie move. With probability $p$ line L7 flips a random one of the three; otherwise line L8 flips $x_4$, the unique least. Say $x_4$ is flipped. Now $x = 0001$ and the only false clause is $(x_2 \vee x_3 \vee \neg x_4)$.

| variable | break | clauses that become false |
|---|---|---|
| $x_2$ | 0 | none: $\neg x_2$ occurs nowhere |
| $x_3$ | 1 | $(x_1 \vee \neg x_3)$ |
| $x_4$ | 1 | $(x_1 \vee x_3 \vee x_4)$ |

Line L6 finds the freebie move $x_2$ and flips it, whatever the noise. Now $x = 0101$, which satisfies all six clauses, and line L4 returns it.

## Correctness

Line L4 returns only an assignment with no false clause, so each answer is a model. Each try makes at most MAX-FLIPS flips, so WalkSAT stops after at most MAX-TRIES $\times$ MAX-FLIPS flips. Each flip is on a variable of a false clause, so it makes that clause true, and a freebie move increases the number of true clauses by at least one. The proof file of this page shows these facts, and that the true-literal counts, the false-clause list and the break counts stay correct after each flip.

No completeness is claimed. If the freebie rule is removed and $p = 1$, WalkSAT is the random walk of [Schöning's algorithm](/schoning-algorithm/), which has a proved bound: on a satisfiable $k$-CNF formula one try of $3n$ flips succeeds with probability at least about $(k/(2(k-1)))^n$, and on 2-CNF the walk of Papadimitriou finds a model in $O(n^2)$ expected flips. The greedy and freebie moves of the SKC rule break this proof, and no general bound is known for them.

## Complexity

Line L2 costs $O(mk)$ to set up the counts. In the implementation each flip computes up to $k$ break counts, each by a scan of the at most $d$ clauses of one variable, and the flip itself updates at most $d$ clauses, so a try costs $O(fkd + mk)$ and the worst case time is $O(t(fkd + mk))$. Solvers that store the break count of each variable and update it at each flip make the choice $O(k)$ per flip. The space is $O(n + mk)$ for the clauses, the lists of occurrences and the counts.

These bounds say nothing about the number of flips needed to find a model, which is the real cost. That number depends strongly on $p$ and is measured.

## Properties

- **Incomplete.** It cannot prove unsatisfiability, and it may miss models.
- **Focused.** Each flip fixes the clause that was chosen.
- **One parameter.** The noise $p$ controls the trade-off between greedy descent and random exploration.
- **Anytime.** The assignment with the fewest false clauses seen so far is a heuristic answer for [MAX-SAT](/max-sat/), and weighted versions are common MaxSAT heuristics.

## Variants and improvements

- **Novelty and R-Novelty.** Sort the variables of the chosen clause by score and avoid the variable flipped most recently, unless a noise coin says otherwise (McAllester, Selman and Kautz 1997).
- **Novelty+ and adaptive noise.** Add a small random walk probability to Novelty, and raise or lower $p$ during the search according to progress (Hoos 1999 and 2002), which removes the need to tune $p$ by hand.
- **Tabu.** Do not flip a variable again for a fixed number of steps.
- **Clause weighting.** Raise the weights of clauses that stay false and use weighted break counts, as in SAPS and PAWS.
- **probSAT.** Drop the freebie and greedy cases and pick each variable of the clause with probability that falls with its break count: see [probSAT](/probsat/).
- **After survey propagation.** [Survey propagation](/survey-propagation/) fixes many variables of a large random formula and hands the rest to WalkSAT.

## When to use it

Use WalkSAT, or a newer relative such as [probSAT](/probsat/), on large satisfiable random formulas and on some combinatorial problems where a model is expected and only a model is needed. It needs little memory and is easy to run in parallel with different seeds. For industrial formulas, and whenever an answer of "unsatisfiable" must be proved, use a [CDCL](/cdcl/) solver.

## Pitfalls

- **Treating "no model found" as UNSAT.** WalkSAT never proves unsatisfiability.
- **Bad noise.** With $p$ near 0 the search stalls in local minima, and with $p$ near 1 it is a slow random walk. Values near 0.5 are common for random 3-SAT in reported experiments, but the best value depends on the formula.
- **Random variable from all variables.** The noise move must pick a variable of the chosen false clause, not any variable, or the flip may not fix any clause.
- **Repeated literals.** A clause such as $(x_1 \vee x_1 \vee x_2)$ must be reduced first, or its true-literal count is wrong and so are the break counts.
- **Choosing the false clause by index.** Always taking the first false clause biases the search. Keep a list of false clauses so that a uniform choice is cheap.

## Implementations

## History

Selman and Kautz added random walk moves to [GSAT](/gsat/) in 1993: with probability $p$, flip a variable of a false clause. Selman, Kautz and Cohen then presented WalkSAT at AAAI-94, in which every flip is chosen from one false clause. They reported that it was faster than GSAT with random walk, and much faster than plain GSAT, on hard random 3-CNF formulas and on encoded planning and circuit problems. These are measured results. McAllester, Selman and Kautz introduced the Novelty rules in 1997, and Hoos added Novelty+ and adaptive noise. Balint and Schöning's [probSAT](/probsat/) of 2012 showed that a simple rule based only on break counts can be faster still on random formulas.

## References
