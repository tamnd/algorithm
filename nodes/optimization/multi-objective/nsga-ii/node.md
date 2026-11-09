---
tag: 736BVW
kind: algorithm
slug: nsga-ii
name: NSGA-II
aliases:
- non-dominated sorting genetic algorithm II
- elitist non-dominated sorting GA
- NSGA2
area: optimization/multi-objective
level: core
summary: An elitist genetic algorithm for several objectives. It sorts parents and offspring into fronts, keeps whole fronts while they fit, and fills the rest by crowding distance. O(p N^2) per generation.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {N: the population size, p: the number of objectives, g: the number of generations, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(g (p N^2 + N (n + c)))}
  space: {extra: O(N^2 + N n)}
properties: {deterministic: false, iterative: true, population: true, elitist: true}
history:
  year: 2002
  people: [Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal, T. Meyarivan]
  note: Deb and his students presented NSGA-II at PPSN VI in 2000 and in the IEEE Transactions on Evolutionary Computation in 2002. It replaced NSGA of Srinivas and Deb (1994), which had no elitism, a sharing radius and an O(p N^3) sort.
prereqs: [non-dominated-sorting, crowding-distance, genetic-algorithm, tournament-selection]
see_also: [nsga-iii, spea2, moea-d, multi-objective-evolutionary-algorithm, pareto-ranking, hypervolume-indicator, elitism, moga]
sources:
  - paper: doi:10.1109/4235.996017
    title: Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal and T. Meyarivan, A fast and elitist multiobjective genetic algorithm, NSGA-II, IEEE Transactions on Evolutionary Computation 6(2), 2002, 182-197
    locator: Section III, the fast non-dominated sort, the crowding distance, the crowded comparison operator and the main loop; Section VI, constraint handling
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 6, the elitist non-dominated sorting genetic algorithm
  - paper: doi:10.1609/aaai.v36i9.21283
    title: Weijie Zheng, Yufei Liu and Benjamin Doerr, A first mathematical runtime analysis of the non-dominated sorting genetic algorithm II (NSGA-II), Proceedings of the AAAI Conference on Artificial Intelligence 36(9), 2022, 10408-10416
    locator: the lemma that no OneMinMax or LOTZ value is lost for N at least 4(n+1), and the bounds O(N n log n) and O(N n^2)
  - paper: "Kalyanmoy Deb and Ram Bhushan Agrawal, Simulated binary crossover for continuous search space, Complex Systems 9(2), 1995, 115-148"
    locator: the simulated binary crossover and its spread factor
---

NSGA-II is an elitist [genetic algorithm](/genetic-algorithm/) for several objectives by Deb, Pratap, Agarwal and Meyarivan (2002). Each generation it joins the parents and the offspring, sorts the $2N$ members into fronts by [non-dominated sorting](/non-dominated-sorting/), keeps whole fronts while they fit in $N$ places, and fills the rest from the next front by the [crowding distance](/crowding-distance/). One generation costs $O(p N^2)$ time for $p$ objectives, plus the evaluations. It is a common baseline among [multi-objective evolutionary algorithms](/multi-objective-evolutionary-algorithm/), but it has no general guarantee to reach the [Pareto front](/pareto-front/).

## In plain words

NSGA-II keeps a fixed number of candidate answers. Each round it makes as many new candidates by mixing and changing the old ones. Then it puts old and new together and sorts them into layers. The first layer holds the candidates that nobody beats in every cost at once. The second layer holds those that only first-layer candidates beat, and so on.

It fills the next round with whole layers, best first, while they fit. When a layer does not fit, it takes the candidates of that layer that sit in the emptiest regions, so the answers stay spread out. A good candidate is kept from round to round unless the best layer itself is too big. Parents are picked by small contests: the better layer wins, and a tie goes to the less crowded candidate.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$.

The input is a search space $X$ (here a box in $\mathbb{R}^n$), the map $f : X \to \mathbb{R}^p$, the population size $N$ and a number $g$ of generations. The output is a set of mutually non-dominated solutions, an approximation of the front of the [multi-objective optimization](/multi-objective-optimization/) problem, with no quality guarantee in general.

## The algorithm

```pseudo id=main
NSGA-II(f, N, g)
L1  P ← N random solutions, each with its image f(x)
L2  compute the front number and the crowding distance of each member of P
L3  repeat g times
L4      Q ← N offspring: parents by crowded binary tournament, then crossover and mutation
L5      R ← P ∪ Q
L6      F_1, F_2, … ← NON-DOMINATED-SORT(R)
L7      P ← ∅; k ← 1
L8      while |P| + |F_k| ≤ N do
L9          P ← P ∪ F_k; k ← k + 1
L10     if |P| < N then compute CROWDING-DISTANCE(F_k)
L11         P ← P ∪ the N − |P| members of F_k with the largest crowding distance
L12 return the members of P in its first front
```

The crowded binary tournament of line L4 draws two members and keeps the one with the smaller front number; when the front numbers are equal it keeps the one with the larger crowding distance, and a full tie is broken at random. The front numbers and distances of the new population, which line L4 needs in the next generation, come from the fronts of line L6 and the distances of each kept front. On real vectors Deb et al. use the simulated binary crossover of Deb and Agrawal (1995) and polynomial mutation; the implementation uses their simple forms with clipping to the bounds.

## Example

Let $N = 4$, and let $R = P \cup Q$ be the eight images below.

| image | front | crowding distance in its front | kept |
|---|---|---|---|
| (1, 1) | $F_1$ | $\infty$ | yes, line L9 |
| (1, 9) | $F_2$ | $\infty$ | yes, line L11 |
| (2, 6) | $F_2$ | $(4 - 1)/8 + (9 - 5)/8 = 7/8$ | no |
| (4, 5) | $F_2$ | $(6 - 2)/8 + (6 - 2)/8 = 1$ | no |
| (6, 2) | $F_2$ | $(9 - 4)/8 + (5 - 1)/8 = 9/8$ | yes, line L11 |
| (9, 1) | $F_2$ | $\infty$ | yes, line L11 |
| (5, 7) | $F_3$ | | no |
| (7, 6) | $F_3$ | | no |

$F_1 = \{(1, 1)\}$ fits, so line L9 takes it. $F_2$ has five members and only three places are left, so line L10 computes its crowding distances. Both objectives have range $8$ on $F_2$. Line L11 takes the two extremes and $(6, 2)$, the inner point with the largest distance. $F_3$ is not reached. With $N = 6$, $F_1$ and $F_2$ would fit exactly and line L10 would not run.

## Correctness

NSGA-II has no guarantee to reach the front of a general problem; the proof covers the invariants of survival. The loop of lines L8 and L9 adds whole fronts while they fit, so it stops at a front $F_k$ with $0 \le N - \lvert P \rvert < \lvert F_k \rvert$, and line L11 takes exactly the missing number. So $\lvert P \rvert = N$ after each generation, the kept set is $F_1 \cup \cdots \cup F_{k-1}$ plus the least crowded part of $F_k$, and every member of $F_1(R)$ survives when $\lvert F_1(R) \rvert \le N$. On OneMinMax with $N \ge 4(n+1)$, each front has at most $4(n+1)$ members with a positive crowding distance, and these include one member of each value, so no value is lost (Zheng, Liu and Doerr). The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Sort, line L6.** $R$ has $2N$ members, so the fast non-dominated sort costs $O(p (2N)^2) = O(p N^2)$ time and $O(N^2)$ space.
- **Crowding, lines L2 and L10.** $O(p N \log N)$, from one sort per objective per front.
- **Selection and variation, line L4.** $O(N)$ for the tournaments, $O(N n)$ for the operators and $N$ evaluations at cost $c$.

The total is $O(g (p N^2 + N (n + c)))$ time and $O(N^2 + N n)$ space. For $p = 2$ the sort can be done in $O(N \log N)$ by the sweep on the [non-dominated sorting](/non-dominated-sorting/) page, and Jensen's method gives $O(N \log^{p-1} N)$ for a fixed $p$; then the generation costs $O(N \log^{p-1} N + p N \log N)$ plus variation and evaluations.

## Properties

- **Elitist.** Parents compete with offspring for survival, so a non-dominated member survives as long as the first front of $R$ fits in $N$ places.
- **No niche parameter.** The crowding distance replaces the sharing radius of NSGA and MOGA.
- **Fixed population size.** $\lvert P \rvert = N$ in each generation.
- **Invariant to increasing transforms in ranking, not in crowding.** Fronts depend only on dominance; the crowding distance depends on the scale, through the gaps divided by the range.
- **Proved running times on test functions.** For $N \ge 4(n+1)$, Zheng, Liu and Doerr (2022) prove $O(N n \log n)$ expected evaluations on OneMinMax and $O(N n^2)$ on LOTZ, with bit-wise mutation and their selection rules. These bounds hold only on those two functions under those hypotheses.

## Variants and improvements

- **Constraints.** Deb et al. use constrained domination: a feasible solution beats an infeasible one, two infeasible solutions compare by their total constraint violation, and two feasible ones by dominance. Then the same sort and survival apply.
- **Faster sorts.** The 2D sweep and Jensen's divide and conquer replace the $O(p N^2)$ sort; see [non-dominated sorting](/non-dominated-sorting/).
- **Recomputed crowding.** Remove the most crowded member of $F_k$ one at a time and recompute the distances, as on the [crowding distance](/crowding-distance/) page.
- **Many objectives.** [NSGA-III](/nsga-iii/) keeps the sort and replaces the crowding distance with reference directions.
- **Steady state.** Make one offspring per step and remove one member of the last front.
- **Archive.** An external archive, as in the [MOEA template](/multi-objective-evolutionary-algorithm/), keeps front points that survival drops when the first front is larger than $N$.

## When to use it

Use NSGA-II for two or three objectives and an evaluation budget of thousands of evaluations or more. It is a common baseline, and libraries implement it. For four or more objectives most of $R$ is often in $F_1$, and the crowding distance decides almost all survival; [NSGA-III](/nsga-iii/), [MOEA/D](/moea-d/) or indicator-based methods are the usual choices there. Report results as measured on given test problems, budgets and settings.

## Pitfalls

- **A first front larger than $N$.** Then survival is by crowding distance alone, and a non-dominated member can be lost, after which a dominated point can come back (see [the MOEA template](/multi-objective-evolutionary-algorithm/)).
- **Ties in the crowding sort.** Members with equal distances, such as several extremes with $\infty$, are kept in an order that depends on the sort. State the tie rule when results must be reproduced.
- **Copies.** Copies of one image share the crowding distance of the image badly: inner copies get gaps of $0$ in each objective. Remove copies, or accept that they take places.
- **Crowding of the new population.** Line L4 needs the distances of the new $P$; computing them on $R$ and reusing them is a different method.
- **Many objectives.** See When to use it.

## Implementations

## History

Srinivas and Deb proposed NSGA in 1994, with fronts found by repeated scans, fitness sharing with a radius, and no elitism. Deb, Agrawal, Pratap and Meyarivan presented NSGA-II at PPSN VI in 2000, and Deb, Pratap, Agarwal and Meyarivan published it in the IEEE Transactions on Evolutionary Computation in 2002 with the $O(p N^2)$ sort, the crowding distance and elitist survival. Deb and Jain gave NSGA-III for many objectives in 2014. Zheng, Liu and Doerr gave the first runtime analysis of NSGA-II in 2022.

## References
