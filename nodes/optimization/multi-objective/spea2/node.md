---
tag: 3QZDDW
kind: algorithm
slug: spea2
name: SPEA2
aliases:
- strength Pareto evolutionary algorithm 2
- improved strength Pareto evolutionary algorithm
area: optimization/multi-objective
level: advanced
summary: An archive-based evolutionary algorithm. Fitness is the summed strength of a point's dominators plus a k-nearest-neighbour density; the archive keeps exactly M points, cut by distance truncation.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {N: the population size, M: the archive size, p: the number of objectives, g: the number of generations, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(g ((N + M)^3 + p (N + M)^2 + N (n + c)))}
  space: {extra: O((N + M)^2 + (N + M) n)}
properties: {deterministic: false, iterative: true, population: true, elitist: true}
history:
  year: 2001
  people: [Eckart Zitzler, Marco Laumanns, Lothar Thiele]
  note: Zitzler, Laumanns and Thiele gave SPEA2 in TIK-Report 103 of ETH Zurich in 2001 and at EUROGEN 2001, to fix the weak fitness order and the loss of boundary points of SPEA.
prereqs: [spea, pareto-dominance, k-nearest-neighbors, elitism]
see_also: [spea, nsga-ii, nsga-iii, moea-d, multi-objective-evolutionary-algorithm, crowding-distance, hypervolume-indicator, tournament-selection]
sources:
  - paper: "Eckart Zitzler, Marco Laumanns and Lothar Thiele, SPEA2, improving the strength Pareto evolutionary algorithm, TIK-Report 103, Computer Engineering and Networks Laboratory, ETH Zurich, 2001"
    locator: Section 3, the fitness assignment, the density estimation with k equal to the square root of the sample size, the environmental selection and the archive truncation
  - paper: "Eckart Zitzler, Marco Laumanns and Lothar Thiele, SPEA2, improving the strength Pareto evolutionary algorithm for multiobjective optimization, Evolutionary Methods for Design, Optimization and Control with Applications to Industrial Problems (EUROGEN 2001), CIMNE, 2002, 95-100"
    locator: the conference version of the method
  - paper: doi:10.1109/4235.797969
    title: Eckart Zitzler and Lothar Thiele, Multiobjective evolutionary algorithms, a comparative case study and the strength Pareto approach, IEEE Transactions on Evolutionary Computation 3(4), 1999, 257-271
    locator: SPEA, the method that SPEA2 replaces
---

SPEA2 is the second strength Pareto evolutionary algorithm, by Zitzler, Laumanns and Thiele (2001). It gives each point of the population and the archive a fitness $F = R + D$: $R$ sums the strengths of the points that dominate it, and $D$ is a density from the distance to its $k$-th nearest neighbour. The archive keeps exactly $M$ points: all non-dominated points if they fit, else the survivors of a truncation that removes points from the closest pairs. It is a [multi-objective evolutionary algorithm](/multi-objective-evolutionary-algorithm/) with no general guarantee to reach the [Pareto front](/pareto-front/).

## In plain words

SPEA2 keeps a population of new candidates and an archive of fixed size. Each round it puts both together. A candidate's strength is how many others it beats in every cost. A candidate's score adds up the strengths of all candidates that beat it, so a candidate that nobody beats scores zero. A small extra term, larger in crowded places, breaks ties. The archive takes all candidates that nobody beats. If there are too few, it adds the next best by score. If there are too many, it removes, one by one, a candidate from the closest pair, so the archive stays spread out. Parents for the next round come only from the archive.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$. $M$ is the archive size, written $\bar N$ by the authors. Distances are Euclidean distances between images.

The input is a search space $X$, the map $f : X \to \mathbb{R}^p$, an initialization and a variation for $X$, the sizes $N$ and $M$, and a number $g$ of generations. The output is the set of non-dominated members of the last archive, an approximation of the front of the [multi-objective optimization](/multi-objective-optimization/) problem, with no quality guarantee in general.

## The algorithm

```pseudo id=main
SPEA2(f, N, M, g)
L1  P ← N random solutions, each with its image f(x); A ← ∅; k ← ⌊√(N + M)⌋
L2  for t ← 0 to g do
L3      U ← P + A
L4      S(i) ← the number of members of U that i dominates, for each i ∈ U
L5      R(i) ← the sum of S(j) over the members j of U that dominate i
L6      F(i) ← R(i) + 1 / (σ_i + 2), where σ_i is the distance from i to its k-th nearest neighbour in U
L7      A ← the members of U with F < 1
L8      if |A| < M then add to A the M − |A| other members of U with the smallest F
L9      while |A| > M do remove the member of A whose sorted list of distances to the other members is lexicographically smallest
L10     if t = g then return the non-dominated members of A
L11     P ← crossover and mutation of the winners of N binary tournaments on A by smaller F
```

$U$ is a multiset, so a point in both $P$ and $A$ counts twice. The density term is $D(i) = 1/(\sigma_i + 2)$, in $(0, 1/2]$, and $k$ is the square root of the sample size $N + M$, after the $k$-nearest-neighbour density estimate of Silverman. Line L9 compares the distance lists from the nearest neighbour outward and removes the member with the smaller first entry, then the smaller second entry on a tie, and so on. Mating selection uses the archive only, with replacement.

## Example

Let $k = 2$ and let $U$ have the six images below, so $M + N = 6$.

| image | dominates | $S$ | dominated by | $R$ | $\sigma$ | $F$ |
|---|---|---|---|---|---|---|
| (1, 5) | (6, 6) | 1 | | 0 | $\sqrt{10}$ | 0.194 |
| (2, 2) | (3, 3), (4, 4), (6, 6) | 3 | | 0 | $\sqrt{8}$ | 0.207 |
| (5, 1) | (6, 6) | 1 | | 0 | $\sqrt{10}$ | 0.194 |
| (3, 3) | (4, 4), (6, 6) | 2 | (2, 2) | 3 | $\sqrt{2}$ | 3.293 |
| (4, 4) | (6, 6) | 1 | (2, 2), (3, 3) | 5 | $\sqrt{8}$ | 5.207 |
| (6, 6) | | 0 | all others | 8 | $\sqrt{18}$ | 8.160 |

$R$ of $(4, 4)$ is $S(2, 2) + S(3, 3) = 3 + 2$. The three non-dominated points have $F < 1$. With $M = 4$, line L8 adds $(3, 3)$, the dominated point with the smallest $F$. With $M = 2$, line L9 must remove one of the three. Their distance lists are $(\sqrt{10}, \sqrt{32})$ for $(1, 5)$ and $(5, 1)$, and $(\sqrt{10}, \sqrt{10})$ for $(2, 2)$. The first entries tie, the second entry of $(2, 2)$ is smaller, so $(2, 2)$ goes and the archive is $\{(1, 5), (5, 1)\}$.

## Correctness

SPEA2 has no guarantee to reach the front of a general problem; the proof covers the fitness and the archive. A dominator $j$ of $i$ has $S(j) \ge 1$, so $R(i) = 0$ for a non-dominated $i$ and $R(i) \ge 1$ otherwise; with $D \in (0, 1/2]$ this gives $F < 1$ exactly for non-dominated points. If $i$ dominates $j$, then every dominator of $i$ dominates $j$ and so does $i$, so $R(j) \ge R(i) + 1$ and $F(i) < F(j)$. The archive has exactly $M$ members when $\lvert U \rvert \ge M$. When at most $M$ points of $U$ are non-dominated in every generation, every non-dominated point seen stays in the archive. The full proof is below.

## Complexity

Let $K = N + M$ be the size of $U$.

- **Strength and raw fitness, lines L4 and L5.** $O(p K^2)$ for all dominance tests.
- **Density, line L6.** $O(p K^2)$ for the distances and $O(K^2 \log K)$ to sort each row.
- **Truncation, line L9.** Each member keeps its sorted list of distances. A removal finds the smallest list in $O(K^2)$ and deletes one entry from each list in $O(K)$ each. At most $K$ removals give $O(K^3)$.
- **Selection and variation, line L11.** $O(N)$ for the tournaments, $O(N n)$ for the operators and $N$ evaluations at cost $c$.

The total is $O(g ((N + M)^3 + p (N + M)^2 + N (n + c)))$ time and $O((N + M)^2 + (N + M) n)$ space for the distance lists and the solutions. The authors give the same $O((N + M)^3)$ worst case for the truncation and note that it is much faster on average.

## Properties

- **Strict fitness order.** If $i$ dominates $j$, then $F(i) < F(j)$. In SPEA two such points can tie.
- **Fixed archive size.** $\lvert A \rvert = M$ in each generation once $\lvert U \rvert \ge M$.
- **Elitist while the front fits.** Non-dominated points always enter the archive, and they all stay while at most $M$ are non-dominated.
- **Every point gets information.** The strength is computed on all of $U$, so dominated points in the population are ranked against each other, and the density separates equal $R$.
- **Scale.** Dominance, $S$ and $R$ do not change under increasing transforms of each objective; the distances in $D$ and line L9 do. Normalize the objectives when their scales differ.

## Variants and improvements

- **Normalized distances.** Divide each objective by its range in $U$ before lines L6 and L9.
- **Shift-based density.** Li, Yang and Liu (2014) shift other points toward the point being rated before the distance count, for many objectives; this is SPEA2+SDE.
- **Other truncations.** Truncation by [crowding distance](/crowding-distance/), by grid cells as in [PAES](/paes/), or by a [hypervolume](/hypervolume-indicator/) contribution gives other trade-offs between cost and spread.
- **Indicator-based selection.** IBEA of Zitzler and Künzli (2004) replaces the fitness with a sum of indicator values, for example of the [epsilon indicator](/epsilon-indicator/).

## When to use it

Use SPEA2 for two or three objectives, when a fixed archive with good spread is wanted and the cubic truncation cost is small next to the evaluations. Its fitness ranks all points, so it gives selection pressure even when most of the population is dominated. Zitzler, Laumanns and Thiele reported results against SPEA, NSGA-II and PESA on their test problems; these are measured results on those instances, budgets and settings.

## Pitfalls

- **Boundary points are not safe.** The truncation can remove the only point with the best value of an objective. With $M = 4$ and the points $(0, 2, 3)$, $(1, 0, 5)$, $(1, 3, 2)$, $(4, 0, 4)$, $(6, 1, 3)$, it removes $(0, 2, 3)$ and keeps $(6, 1, 3)$, which is extreme in no objective. The proof file checks the distances.
- **Multiset.** A point in both $P$ and $A$ counts twice in $S$, $R$ and the distances; its copy is at distance $0$.
- **Cubic truncation.** With large $M$ the truncation dominates the cost of a generation.
- **Scale.** Without normalization, an objective with a large range decides all distances.
- **Bounded archive is not monotone.** When more than $M$ points are non-dominated, a later archive can hold a point that a removed point dominates.

## Implementations

## History

Zitzler and Thiele gave SPEA in 1998 and 1999. Its fitness gave equal values to points covered by the same archive members, and its clustering could cut the extremes of the front. Zitzler, Laumanns and Thiele gave SPEA2 in 2001, with the strength computed over all points, the density from the $k$-th nearest neighbour, a fixed archive size and the truncation by nearest distances. SPEA2 and NSGA-II became the usual baselines for two and three objectives in the following decade.

## References
