---
tag: 0EWQ9V
kind: algorithm
slug: moga
name: MOGA
aliases:
- multi-objective genetic algorithm
- Fonseca-Fleming MOGA
area: optimization/multi-objective
level: advanced
summary: The genetic algorithm of Fonseca and Fleming (1993). Rank = 1 + number of dominators; fitness interpolated by rank, averaged per rank, shared in objective space inside each rank.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {N: the population size, p: the number of objectives, g: the number of generations, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(g (p N^2 + N (n + c)))}
  space: {extra: O(N (n + p))}
properties: {deterministic: false, iterative: true, population: true, elitist: false}
history:
  year: 1993
  people: [Carlos M. Fonseca, Peter J. Fleming]
  note: Fonseca and Fleming presented MOGA at the fifth International Conference on Genetic Algorithms in 1993. It was one of the first algorithms to use Pareto ranking, with NPGA and NSGA in 1994.
prereqs: [pareto-ranking, genetic-algorithm, roulette-wheel-selection]
see_also: [vega, npga, nsga-ii, multi-objective-evolutionary-algorithm, crowding-distance, spea]
sources:
  - paper: "Carlos M. Fonseca and Peter J. Fleming, Genetic algorithms for multiobjective optimization: formulation, discussion and generalization, Proceedings of the Fifth International Conference on Genetic Algorithms, Morgan Kaufmann, 1993, 416-423"
    locator: the rank by number of dominating individuals, the interpolation and averaging of fitness, sharing in the objective space, and the estimate of the niche size
  - paper: doi:10.1162/evco.1995.3.1.1
    title: Carlos M. Fonseca and Peter J. Fleming, An overview of evolutionary algorithms in multiobjective optimization, Evolutionary Computation 3(1), 1995, 1-16
    locator: the place of Pareto-based ranking among the fitness assignment methods
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 5, the multi-objective genetic algorithm of Fonseca and Fleming with a worked example
  - paper: "James E. Baker, Reducing bias and inefficiency in the selection algorithm, Proceedings of the Second International Conference on Genetic Algorithms, Lawrence Erlbaum, 1987, 14-21"
    locator: stochastic universal sampling
---

MOGA, the multi-objective genetic algorithm of Fonseca and Fleming (1993), is a [genetic algorithm](/genetic-algorithm/) whose fitness comes from [Pareto ranking](/pareto-ranking/): the rank of a member is one plus the number of members that dominate it. The fitness is then interpolated by rank, averaged inside each rank, and shared among members of equal rank by their distance in the objective space. Sharing moves selection pressure to less crowded parts of the front without changing the total share of each rank. MOGA has no elitism and no guarantee to reach the [Pareto front](/pareto-front/).

## In plain words

MOGA scores each candidate by how many others beat it in every cost at once. A candidate that nobody beats gets the best score, and candidates that only a few others beat come next.

All candidates with the same score get the same fitness. Then MOGA looks at where they sit among the trade-offs. If many of them sit close together, they must share their fitness, like animals that share the food of one place. A candidate alone in an empty region keeps more. So the next generation fills the gaps of the front, and the group as a whole keeps its share.

The new generation is made from these parents by the usual mixing and random changes, and it replaces the old one.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$.

The input is a search space $X$, the map $f : X \to \mathbb{R}^p$, the population size $N$, a niche radius $\sigma$ in the normalized objective space, and a number $g$ of generations. The output is a set of mutually non-dominated solutions, an approximation of the front of the [multi-objective optimization](/multi-objective-optimization/) problem.

## The algorithm

```pseudo id=main
MOGA(f, N, σ, g)
L1  P ← N random solutions, each with its image f(x)
L2  repeat g times
L3      r(x) ← 1 + the number of members of P that dominate x
L4      sort P by r; the member at position k gets the raw value N − k + 1
L5      F(x) ← the mean raw value of the members with rank r(x)
L6      m(x) ← sum of sh(d(x, z)) over members z with r(z) = r(x)
L7      φ(x) ← F(x) / m(x), scaled so that each rank keeps its total of F
L8      M ← N parents drawn by stochastic universal sampling on φ
L9      P ← offspring of M by crossover and mutation
L10 return the members of P with rank 1
```

The distance $d$ of line L6 is Euclidean after each objective is divided by its range in the population, and $\mathrm{sh}(d) = 1 - d/\sigma$ for $d < \sigma$ and $0$ otherwise. Fonseca and Fleming share in the objective space, not in the decision space, and they give a way to estimate $\sigma$ from the expected size of the front; the implementation takes $\sigma$ as a parameter. Line L4 can use another decreasing function of the position in place of the linear one. Stochastic universal sampling (Baker, 1987) gives each member the floor or the ceiling of its expected count.

## Example

Take the eight images $A = (1, 8)$, $B = (2, 5)$, $C = (3, 6)$, $D = (4, 2)$, $E = (5, 4)$, $F = (6, 7)$, $G = (7, 1)$, $H = (8, 3)$ of the [non-dominated sorting](/non-dominated-sorting/) page, and $\sigma = 4/7$. Both objectives have range $7$, so $\sigma$ is the distance $4$ in the original units.

| member | dominated by | $r$ | raw values of the block | $F$ | $m$ | $\varphi$ |
|---|---|---|---|---|---|---|
| A (1, 8) | | 1 | 8, 7, 6, 5 | 6.5 | 1.2094 | 6.7546 |
| B (2, 5) | | 1 | | 6.5 | 1.3080 | 6.2454 |
| D (4, 2) | | 1 | | 6.5 | 1.3080 | 6.2454 |
| G (7, 1) | | 1 | | 6.5 | 1.2094 | 6.7546 |
| C (3, 6) | B | 2 | 4, 3 | 3.5 | 1.2929 | 3.5 |
| E (5, 4) | D | 2 | | 3.5 | 1.2929 | 3.5 |
| H (8, 3) | D, G | 3 | 2 | 2 | 1 | 2 |
| F (6, 7) | B, C, D, E | 5 | 1 | 1 | 1 | 1 |

In rank 1, $A$ and $B$ are at distance $\sqrt{10} \approx 3.16$, $B$ and $D$ at $\sqrt{13} \approx 3.61$, and $D$ and $G$ at $\sqrt{10}$; the other pairs are farther than $4$. So $m(A) = 1 + (1 - \sqrt{10}/4)$ and $m(B) = 1 + (1 - \sqrt{10}/4) + (1 - \sqrt{13}/4)$. The inner points $B$ and $D$ have two close neighbors and lose fitness to the ends $A$ and $G$. The rank-1 total stays $26 = 8 + 7 + 6 + 5$, and the expected number of rank-1 parents is $8 \cdot 26 / 36 \approx 5.78$, with or without sharing.

## Correctness

MOGA has no guarantee to reach the front; the proof covers the fitness that it assigns. The rank is strictly monotone under dominance: if $z$ dominates $x$, then each dominator of $z$ also dominates $x$, and $z$ does too, so $r(z) < r(x)$. The raw values are a permutation of $1, \ldots, N$ and each rank is a block of consecutive positions, so the averaged values are equal inside a rank and strictly decrease from one rank to the next. Each niche count is at least $1$, and the scaling of line L7 keeps the total of each rank. So the expected number of parents of each rank is fixed by line L5 alone, and sharing only moves the share inside a rank. The full proof is below.

## Complexity

- **Ranking, line L3.** $O(p N^2)$ for all pairs.
- **Lines L4 and L5.** $O(N \log N)$ for the sort and $O(N)$ for the means.
- **Sharing, lines L6 and L7.** $O(p N^2)$ for the distances inside each rank.
- **Selection and variation, lines L8 and L9.** $O(N)$ for stochastic universal sampling, $O(N n)$ for the operators, and $N$ evaluations at cost $c$.

The total is $O(g (p N^2 + N (n + c)))$ time and $O(N (n + p))$ space.

## Properties

- **Not elitist.** The offspring replace the whole population, so a front point can be lost.
- **Rank pressure is fixed by the rank sizes.** By Theorem 4 of the proof, the expected share of a rank does not depend on $\sigma$.
- **Insensitive to the scale of the objectives in ranking.** The rank uses only dominance. Sharing uses normalized distances, so it is insensitive to a positive scaling of one objective.
- **Fixed population size.** $\lvert P \rvert = N$ in each generation.

## Variants and improvements

- **Mating restriction.** Fonseca and Fleming also allowed mating only between members closer than a radius $\sigma_{\text{mate}}$ in the objective space.
- **Goals and priorities.** In the same paper, a decision maker's goals change the dominance relation, so the rank prefers members that meet the goals. This is an early form of [preference articulation](/preference-articulation/).
- **Other rank rules.** Using the front number of [non-dominated sorting](/non-dominated-sorting/) in place of the dominance count gives an NSGA-like method; using the strengths of [SPEA2](/spea2/) gives another.
- **Elitism.** Adding an archive or keeping the best $N$ of parents and offspring, as in [NSGA-II](/nsga-ii/), keeps front points from one generation to the next.

## When to use it

Use MOGA for small populations and two or three objectives, where the $O(p N^2)$ cost is small and a sharing radius is easy to choose. Add an archive for the final answer. For a method without a radius, use the [crowding distance](/crowding-distance/) of NSGA-II or the nearest neighbor density of SPEA2.

## Pitfalls

- **The niche radius.** A $\sigma$ that is too small makes every niche count $1$, and sharing does nothing; one that is too large makes all counts equal inside a rank, and again sharing does nothing. Both ends give the plain averaged fitness.
- **Scaling of distances.** Sharing without normalization favors the objective with the larger range.
- **Copies.** Equal images are at distance $0$ and count fully in each other's niche, so copies share their fitness and lose share to distinct members of their rank.
- **Too many ranks.** With many objectives most members have rank $1$, and the rank gives little pressure. Sharing then decides most of the selection.

## Implementations

## History

Fonseca and Fleming presented MOGA in 1993, after Goldberg's 1989 proposal to rank by Pareto dominance. They ranked by the number of dominators, introduced the averaging by rank, shared fitness in the objective space with a rule to set $\sigma$, and added goals and priorities for the decision maker. Their 1995 survey placed Pareto ranking among the other fitness assignment methods. NPGA and NSGA followed in 1994.

## References
