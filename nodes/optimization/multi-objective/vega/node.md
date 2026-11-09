---
tag: 3S4BQF
kind: algorithm
slug: vega
name: VEGA
aliases:
- vector evaluated genetic algorithm
- Schaffer's VEGA
area: optimization/multi-objective
level: advanced
summary: Schaffer's 1985 genetic algorithm that fills each part of the mating pool by selection on one objective alone. Its expected selection equals that of a weighted sum with weights 1/S_i.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {N: the population size, p: the number of objectives, g: the number of generations, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(g N (n + c) + p N^2)}
  space: {extra: O(N (n + p))}
properties: {deterministic: false, iterative: true, population: true, elitist: false}
history:
  year: 1985
  people: [J. David Schaffer]
  note: Schaffer proposed VEGA in his 1984 doctoral thesis at Vanderbilt University and presented it at the first International Conference on Genetic Algorithms in 1985. It is the first genetic algorithm for several objectives.
prereqs: [genetic-algorithm, pareto-dominance, roulette-wheel-selection]
see_also: [multi-objective-evolutionary-algorithm, moga, npga, nsga-ii, weighted-sum-method, tournament-selection]
sources:
  - paper: "J. David Schaffer, Multiple objective optimization with vector evaluated genetic algorithms, Proceedings of the First International Conference on Genetic Algorithms and Their Applications, Lawrence Erlbaum, 1985, 93-100"
    locator: the vector evaluated selection, the test functions, and the remarks on speciation toward the extremes
  - paper: "Jon T. Richardson, Mark R. Palmer, Gunar E. Liepins and Mike R. Hilliard, Some guidelines for genetic algorithms with penalty functions, Proceedings of the Third International Conference on Genetic Algorithms, Morgan Kaufmann, 1989, 191-197"
    locator: the remark that VEGA selection is equivalent in expectation to a weighted sum of the objectives
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 5, the vector evaluated genetic algorithm among the non-elitist methods
  - book: isbn:9780387332543
    title: Carlos A. Coello Coello, Gary B. Lamont and David A. Van Veldhuizen, Evolutionary Algorithms for Solving Multi-Objective Problems, second edition, Springer, 2007
    locator: Chapter 2, the description of VEGA and its bias
---

VEGA, the vector evaluated genetic algorithm, is the first [genetic algorithm](/genetic-algorithm/) for several objectives: it splits the mating pool into $p$ parts and fills part $i$ by selection on objective $i$ alone. Schaffer presented it in 1985. It uses no [Pareto dominance](/pareto-dominance/) and no elitism, and Richardson et al. (1989) observed that its expected selection is the same as selection on a weighted sum of the objectives with weights that depend on the population. So it tends to keep the extremes of the front and to lose the compromise points in non-convex parts.

## In plain words

Imagine a team that must pick good designs, where each design has a price and a weight. VEGA gives half of the places in the breeding pool to the cheapest designs and half to the lightest ones. Then it shuffles the pool and lets the designs mate at random, so a cheap parent often mates with a light one.

This is simple and needs no new idea beyond a normal genetic algorithm. But a design that is fairly cheap and fairly light, and best at nothing, wins few places in either half. So the population drifts to the two ends, the very cheap and the very light designs, and the good middle designs can die out.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$.

The input is a search space $X$ (here a box in $\mathbb{R}^n$), the map $f : X \to \mathbb{R}^p$, $N$ and a budget of $g$ generations. The output is a set of mutually non-dominated solutions, an approximation of the [Pareto front](/pareto-front/) of the [multi-objective optimization](/multi-objective-optimization/) problem. No quality guarantee comes with it.

## The algorithm

```pseudo id=main
VEGA(f, N, p, g)
L1  P ← N random solutions, each with its image f(x)
L2  repeat g times
L3      M ← an empty pool
L4      for i ← 1 to p do
L5          append N/p members of P, chosen by selection on f_i alone
L6      shuffle M
L7      Q ← offspring of consecutive pairs of M, by crossover and mutation
L8      P ← Q
L9  return the members of P that no member of P dominates
```

Line L5 is the only change from a single-objective genetic algorithm. Schaffer used proportional selection; the implementation of this page uses a binary [tournament](/tournament-selection/) on $f_i$, which needs no positive fitness. When $p$ does not divide $N$, the first $N \bmod p$ parts get one more member. Line L6 matters: after the shuffle, a parent chosen for $f_1$ mates with a parent chosen for $f_2$ as often as with its own kind.

## Example

Take $N = 4$ and $p = 2$, with images $A = (1, 9)$, $B = (6, 6)$, $C = (9, 1)$ and $D = (7, 7)$. The points $A$, $B$, $C$ are non-dominated, and $B$ dominates $D$. For proportional selection set $g_i = 10 - f_i$, which is positive. Then $S_1 = S_2 = 17$, and each part has two slots.

| member | $f$ | $g$ | expected copies from part 1 | from part 2 | total |
|---|---|---|---|---|---|
| A | (1, 9) | (9, 1) | $2 \cdot 9/17$ | $2 \cdot 1/17$ | $20/17 \approx 1.18$ |
| B | (6, 6) | (4, 4) | $2 \cdot 4/17$ | $2 \cdot 4/17$ | $16/17 \approx 0.94$ |
| C | (9, 1) | (1, 9) | $2 \cdot 1/17$ | $2 \cdot 9/17$ | $20/17 \approx 1.18$ |
| D | (7, 7) | (3, 3) | $2 \cdot 3/17$ | $2 \cdot 3/17$ | $12/17 \approx 0.71$ |

The totals sum to $4 = N$. The weighted sum $h = g_1/17 + g_2/17$ gives $10/17$, $8/17$, $10/17$, $6/17$, and proportional selection of four parents on $h$ gives the same totals. The dominated $D$ gets fewer copies than $B$, as Corollary 4 of the proof says. But $B$, a non-dominated compromise, gets fewer than the average of one copy, because it lies below the line from $A$ to $C$ in the $g$ plane and maximizes no weighted sum.

## Correctness

VEGA has no guarantee to reach the front, so the proof covers what the code keeps. Each generation makes exactly $N$ offspring, because the part sizes of line L5 sum to $N$ and line L7 makes one offspring per pool member. Line L9 returns the minimal elements of the final population under dominance, which are mutually non-dominated and nonempty. With proportional selection, the expected number of copies of $x$ is $(N/p) \sum_i g_i(x)/S_i$, which equals the expected number under proportional selection on the weighted sum with $w_i = 1/S_i$, because the weighted fitness sums to $p$ over the population. The details are in the proof file.

## Complexity

- **Selection, lines L3 to L6.** A binary tournament takes $O(1)$ time, so the pool costs $O(N)$. Proportional selection with prefix sums and binary search costs $O(p N + N \log N)$ per generation.
- **Variation and evaluation, lines L7 and L8.** $O(N n)$ for the operators on vectors of length $n$, and $N$ evaluations of $f$ at cost $c$ each.
- **Output, line L9.** $O(p N^2)$ for the pairwise dominance tests.

The total is $O(g N (n + c) + p N^2)$ time, and the population and pool take $O(N (n + p))$ space.

## Properties

- **Not elitist.** The population is replaced in full, so a front point found in one generation can be lost in the next.
- **Fixed population size.** $\lvert P \rvert = N$ in each generation.
- **No dominance test during the run.** Dominance is used only in line L9. So the method runs in $O(N)$ time per generation plus the evaluations.
- **Scale.** With proportional selection the weights $1/S_i$ make the method insensitive to a positive scaling of one $g_i$. A tournament on $f_i$ is insensitive to any increasing transform of $f_i$.

## Variants and improvements

- **Schaffer's heuristics.** Schaffer discussed a bonus for non-dominated members and a preference for mating between parts, to counter the drift to the extremes.
- **Tournament selection per objective.** Used here; it removes the need for positive fitness values.
- **Random objective per slot.** Each slot of the pool picks an objective at random, so the expected part sizes are $N/p$.
- **Pareto-based successors.** [MOGA](/moga/), [NPGA](/npga/) and NSGA replace the per-objective selection with a [Pareto rank](/pareto-ranking/) and fitness sharing; [NSGA-II](/nsga-ii/) adds elitism.

## When to use it

Use VEGA as a baseline, or for teaching, when $p$ is small and the extremes of the front are of most interest. For a spread along the whole front, and especially for a non-convex front, use a Pareto-based method with a density term and an archive.

## Pitfalls

- **Speciation toward the extremes.** The expected share of a member is a weighted sum of its fitness values (Theorem 3 of the proof), so compromise points in non-convex parts of the front get small shares, as $B$ in the example.
- **No shuffle.** Without line L6, crossover pairs come from one part only, and the parts evolve as separate single-objective searches.
- **Negative fitness in proportional selection.** $g_i$ must be positive. Shift each objective, and note that the shift changes the weights $1/S_i$.
- **Reporting the last population only.** Front points found earlier are not kept. Add an external archive, as in the [MOEA template](/multi-objective-evolutionary-algorithm/), if they matter.

## Implementations

## History

J. David Schaffer developed VEGA in his 1984 doctoral thesis at Vanderbilt University and presented it at the first International Conference on Genetic Algorithms in 1985. Richardson, Palmer, Liepins and Hilliard (1989) noted that its selection acts as a weighted sum of the objectives. Goldberg's 1989 book proposed Pareto ranking in its place, and the methods of the early 1990s (MOGA, NPGA and NSGA) followed that proposal.

## References
