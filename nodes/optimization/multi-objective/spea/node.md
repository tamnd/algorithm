---
tag: Y5WMKW
kind: algorithm
slug: spea
name: SPEA
aliases:
- strength Pareto evolutionary algorithm
- SPEA1
area: optimization/multi-objective
level: advanced
summary: An evolutionary algorithm with an external archive of non-dominated points, cut by clustering. Archive members get a strength; population members get 1 plus the strengths of those that cover them.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {N: the population size, M: the archive bound, p: the number of objectives, g: the number of generations, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(g ((N + M)^3 + p (N + M)^2 + N (n + c)))}
  space: {extra: O((N + M)^2 + (N + M) n)}
properties: {deterministic: false, iterative: true, population: true, elitist: true}
history:
  year: 1999
  people: [Eckart Zitzler, Lothar Thiele]
  note: Zitzler and Thiele presented SPEA at PPSN V in 1998 and in the IEEE Transactions on Evolutionary Computation in 1999. Zitzler, Laumanns and Thiele replaced it with SPEA2 in 2001.
prereqs: [pareto-dominance, genetic-algorithm, agglomerative-clustering, elitism]
see_also: [spea2, nsga-ii, multi-objective-evolutionary-algorithm, pareto-ranking, moga, paes, approximate-pareto-set, tournament-selection]
sources:
  - paper: doi:10.1109/4235.797969
    title: Eckart Zitzler and Lothar Thiele, Multiobjective evolutionary algorithms, a comparative case study and the strength Pareto approach, IEEE Transactions on Evolutionary Computation 3(4), 1999, 257-271
    locator: Section III, the strength and fitness assignment, the external set and its reduction by clustering
  - paper: "Eckart Zitzler and Lothar Thiele, Multiobjective optimization using evolutionary algorithms, a comparative case study, Parallel Problem Solving from Nature V, LNCS 1498, Springer, 1998, 292-301"
    locator: the first presentation of the strength Pareto approach
---

SPEA, the strength Pareto evolutionary algorithm of Zitzler and Thiele (1999), was one of the first [multi-objective evolutionary algorithms](/multi-objective-evolutionary-algorithm/) with an external archive of non-dominated solutions. Each archive member gets a strength, the share of the population that it covers, and each population member gets $1$ plus the strengths of the archive members that cover it. Parents come from the population and the archive together, and the archive is cut to its bound by average-linkage clustering. It has no general guarantee to reach the [Pareto front](/pareto-front/).

## In plain words

SPEA keeps two groups. The population holds the current candidates. The archive holds the best trade-offs found so far, those that no other candidate beats in every cost. Each archive member scores how many population members it is at least as good as everywhere. A population member then gets a worse score the more strong archive members stand over it. Parents are picked by small contests with lower scores winning, and the archive members always win against the population. When the archive gets too big, close members are grouped and each group keeps only its most central member, so the archive stays spread out.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$. We write $a \preceq b$ when $a$ weakly dominates $b$ (Zitzler and Thiele say that $a$ covers $b$), and $M$ for the archive bound, which they write $\bar N$.

The input is a search space $X$, the map $f : X \to \mathbb{R}^p$, an initialization and a variation for $X$, the sizes $N$ and $M$, and a number $g$ of generations. The output is the archive: at most $M$ mutually non-dominated solutions, an approximation of the front of the [multi-objective optimization](/multi-objective-optimization/) problem, with no quality guarantee in general.

## The algorithm

```pseudo id=main
SPEA(f, N, M, g)
L1  P ← N random solutions, each with its image f(x); A ← ∅
L2  repeat g times
L3      A ← A ∪ the non-dominated members of P
L4      remove from A each member that another member dominates, and each repeated image
L5      if |A| > M then cut A to M members by average-linkage clustering
L6      s(a) ← |{x ∈ P : f(a) ⪯ f(x)}| / (N + 1), for each a ∈ A
L7      F(x) ← 1 + the sum of s(a) over the a ∈ A with f(a) ⪯ f(x), for each x ∈ P
L8      pool ← the winners of N binary tournaments on P + A, where a smaller s or F wins
L9      P ← crossover and mutation of the pool, with images
L10 update A by lines L3 to L5 with the last P, and return A
```

Line L5 is [agglomerative clustering](/agglomerative-clustering/) with average linkage in objective space. It starts with one cluster per member, merges the two clusters with the smallest average distance between their members until $M$ clusters are left, and keeps from each cluster the member with the smallest sum of distances to the others in it. Line L8 draws both entrants with replacement from the multiset union of $P$ and $A$; ties are broken at random. Zitzler and Thiele used bit strings, one-point crossover and bit-flip mutation on knapsack problems; the implementation takes the variation as a parameter.

## Example

Let $N = 6$ and let the archive after line L5 be $A = \{(1, 7), (3, 4), (6, 2)\}$.

| member | image | covered by | value |
|---|---|---|---|
| archive | (1, 7) | | $s = 4/7$ |
| archive | (3, 4) | | $s = 4/7$ |
| archive | (6, 2) | | $s = 3/7$ |
| population | (2, 8) | (1, 7) | $F = 1 + 4/7 = 11/7$ |
| population | (4, 5) | (3, 4) | $F = 11/7$ |
| population | (4, 8) | (1, 7), (3, 4) | $F = 15/7$ |
| population | (7, 3) | (6, 2) | $F = 10/7$ |
| population | (7, 7) | all three | $F = 18/7$ |
| population | (8, 9) | all three | $F = 18/7$ |

$(1, 7)$ covers $(2, 8)$, $(4, 8)$, $(7, 7)$ and $(8, 9)$, so $s = 4/(6 + 1)$. All strengths are below $1$ and all $F$ are at least $1$, so every archive member beats every population member in line L8. The point $(7, 7)$ dominates $(8, 9)$, but both get $18/7$: the fitness of SPEA does not separate them.

For line L5, let the archive images be $(0, 10), (1, 9), (2, 8), (8, 2), (9, 1), (10, 0)$ and $M = 2$. Neighbours inside each group of three are $\sqrt{2}$ apart, and the groups are more than $8$ apart, so average linkage ends with the two groups. In each group the middle point has the smallest sum of distances, $2\sqrt{2}$ against $3\sqrt{2}$, so the archive becomes $\{(1, 9), (9, 1)\}$.

## Correctness

SPEA has no guarantee to reach the front of a general problem; the proof covers the archive and the fitness. After line L4 the archive is mutually non-dominated with distinct images, and after line L5 it has at most $M$ members. If line L5 never cuts, the archive images after generation $t$ are exactly the non-dominated images of all points seen so far, by induction: a non-dominated point is in the old archive or in the current population, and a kept point that some seen point dominates would be dominated by a non-dominated seen point, which is a candidate. Strengths are in $[0, N/(N+1)]$ and fitness is at least $1$, and $f(x) \preceq f(x')$ implies $F(x) \le F(x')$. The full proof is below.

## Complexity

Let $k \le N + M$ be the number of candidates in line L4.

- **Archive update, lines L3 and L4.** $O(p N^2)$ for the non-dominated members of $P$ and $O(p k^2)$ for the dominance tests among the candidates.
- **Clustering, line L5.** $O(p k^2)$ for the distances, then at most $k$ merges, each $O(k^2)$ to find the closest pair and $O(k)$ to update the averages, so $O(k^3)$.
- **Fitness, lines L6 and L7.** $O(p N M)$.
- **Selection and variation, lines L8 and L9.** $O(N)$ for the tournaments, $O(N n)$ for the operators and $N$ evaluations at cost $c$.

The total is $O(g ((N + M)^3 + p (N + M)^2 + N (n + c)))$ time and $O((N + M)^2 + (N + M) n)$ space for the distances and the solutions. A priority queue of cluster distances lowers the clustering step to $O(k^2 \log k)$.

## Properties

- **Elitist by its archive.** Without cuts the archive is exactly the front of all points seen. With cuts it holds at most $M$ points, but a point can then enter that a removed point dominates.
- **Archive members always win.** Every strength is below $1$ and every population fitness is at least $1$.
- **Weak fitness order.** A population member that dominates another has a fitness no larger, but it can be equal, as in the example.
- **No niche radius.** Diversity comes from the clustering of the archive and from the strengths, which punish members covered by many crowded archive points.
- **Depends on the scale in line L5 only.** Dominance and strengths do not change under increasing transforms of each objective; the Euclidean distances of the clustering do.

## Variants and improvements

- **[SPEA2](/spea2/).** Zitzler, Laumanns and Thiele (2001) give each point a strength computed from all points, add a density term from the $k$-th nearest neighbour, keep the archive size fixed, and cut by nearest-neighbour truncation, which keeps boundary points.
- **Other cuts.** Grid-based cuts as in [PAES](/paes/) or box cuts as in [approximate Pareto sets](/approximate-pareto-set/) bound the archive with other guarantees.
- **Real-coded variation.** Replace bit operators with simulated binary crossover and polynomial mutation, as in [NSGA-II](/nsga-ii/).

## When to use it

SPEA is mostly of historical and teaching interest, since SPEA2 fixes its known weaknesses with the same structure. Use it to study archive-based fitness. On their knapsack problems with two to four objectives, Zitzler and Thiele (1999) measured that SPEA's sets covered those of the other methods in their study, among them VEGA, NPGA and NSGA, more than the reverse in their coverage measure; these are measured results on those instances and settings.

## Pitfalls

- **Equal fitness for dominated pairs.** Population members covered by the same archive members get equal fitness, whatever their relation to each other.
- **One archive point.** If the archive has one member, all population members it covers get the same fitness, and selection pressure inside the population is lost.
- **Boundary points lost by clustering.** The cluster representative is the central member, so the extremes of the front can be cut.
- **Bounded archive is not monotone.** After cuts, a later archive can hold a point that an earlier, removed point dominates.
- **Repeated images.** Line L4 must keep one copy of equal images; the rule "remove every member covered by another" read literally removes both.

## Implementations

## History

Zitzler and Thiele presented the strength Pareto approach at PPSN V in 1998 in a comparison on multi-objective knapsack problems, and gave the full method and the comparison in the IEEE Transactions on Evolutionary Computation in 1999. The external archive and the clustering came from earlier work on archives of non-dominated points; the strength replaced the rank of [MOGA](/moga/) and the fronts of NSGA. Zitzler, Laumanns and Thiele gave SPEA2 in 2001.

## References
