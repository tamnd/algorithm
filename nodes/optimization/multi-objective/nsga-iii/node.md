---
tag: YWZJB7
kind: algorithm
slug: nsga-iii
name: NSGA-III
aliases:
- many-objective NSGA
- reference-point-based NSGA-II
area: optimization/multi-objective
level: advanced
summary: NSGA-II for many objectives. The last front that does not fit is cut by reference lines, with normalized images attached to their nearest line and empty lines served first.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {N: the population size, p: the number of objectives, H: the number of reference points, g: the number of generations, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(g (p N^2 + p N H + H^2 + p^3 + N (n + c)))}
  space: {extra: O(N^2 + N n + p H)}
properties: {deterministic: false, iterative: true, population: true, elitist: true}
history:
  year: 2014
  people: [Kalyanmoy Deb, Himanshu Jain]
  note: Deb and Jain published NSGA-III in two parts in the IEEE Transactions on Evolutionary Computation in 2014, the second part on constraints. The reference points are the simplex lattice of Das and Dennis (1998).
prereqs: [nsga-ii, non-dominated-sorting, ideal-point, achievement-scalarizing-function]
see_also: [nsga-ii, moea-d, normal-boundary-intersection, crowding-distance, multi-objective-evolutionary-algorithm, spea2, hypervolume-indicator, reference-point-method]
sources:
  - paper: doi:10.1109/TEVC.2013.2281535
    title: Kalyanmoy Deb and Himanshu Jain, An evolutionary many-objective optimization algorithm using reference-point-based nondominated sorting approach, Part I, solving problems with box constraints, IEEE Transactions on Evolutionary Computation 18(4), 2014, 577-601
    locator: Section IV, the reference points, the normalization, the association and the niche-preservation operation, and the two-layer reference points for many objectives
  - paper: doi:10.1109/TEVC.2013.2281534
    title: Himanshu Jain and Kalyanmoy Deb, An evolutionary many-objective optimization algorithm using reference-point based nondominated sorting approach, Part II, handling constraints and extending to an adaptive approach, IEEE Transactions on Evolutionary Computation 18(4), 2014, 602-622
    locator: the constrained version and the adaptive reference points
  - paper: doi:10.1137/S1052623496307510
    title: Indraneel Das and J. E. Dennis, Normal-boundary intersection, a new method for generating the Pareto surface in nonlinear multicriteria optimization problems, SIAM Journal on Optimization 8(3), 1998, 631-657
    locator: the points of the unit simplex with coordinates in multiples of 1/h
---

NSGA-III is the many-objective form of [NSGA-II](/nsga-ii/) by Deb and Jain (2014). Survival keeps whole fronts while they fit, as in NSGA-II; the last front that does not fit is cut by a set of reference lines instead of the [crowding distance](/crowding-distance/). The images are normalized, each one is attached to its nearest reference line, and lines with fewer attached members get new members first. It has no general guarantee to reach the [Pareto front](/pareto-front/).

## In plain words

When there are many costs at once, almost every candidate is beaten by nobody, so NSGA-II has to choose almost all survivors by its crowding rule. NSGA-III fixes a set of directions spread evenly over all cost trade-offs before the run. Each round it scales the costs to a common size, and finds for each candidate the direction nearest to it. It then fills the free places so that directions with no candidate yet get one first, and only then directions with one, and so on. A direction with no candidate takes the candidate nearest to it. The directions keep the survivors spread over the trade-offs.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$.

The input is a search space $X$ (here a box in $\mathbb{R}^n$), the map $f : X \to \mathbb{R}^p$, the population size $N$, a set $Z$ of $H$ reference points and a number $g$ of generations. The default $Z$ is the Das and Dennis lattice: all points of the unit simplex $\{w \ge 0, \sum_m w_m = 1\}$ whose coordinates are multiples of $1/h$, for $h$ divisions. It has $H = \binom{h + p - 1}{p - 1}$ points. The output is a set of mutually non-dominated solutions, an approximation of the front of the [multi-objective optimization](/multi-objective-optimization/) problem, with no quality guarantee in general.

## The algorithm

```pseudo id=main
NSGA-III(f, N, Z, g)
L1  P ← N random solutions, each with its image f(x)
L2  repeat g times
L3      Q ← N offspring: random parent pairs, then crossover and mutation
L4      R ← P ∪ Q; F_1, F_2, … ← NON-DOMINATED-SORT(R)
L5      S ← F_1 ∪ … ∪ F_l, where l is the first index with |F_1 ∪ … ∪ F_l| ≥ N
L6      if |S| = N then P ← S and go to the next generation
L7      P ← F_1 ∪ … ∪ F_{l−1}; K ← N − |P|
L8      normalize the images of S by the ideal point of S and the intercepts of the hyperplane through the extreme points
L9      attach each member s of S to the line through 0 and the point of Z nearest to it; d(s) ← its perpendicular distance
L10     ρ_j ← the number of members of P attached to line j, for each j
L11     while fewer than K members of F_l were added do
L12         j ← a line not excluded with the smallest ρ_j, ties at random
L13         I ← the members of F_l attached to j and not added yet
L14         if I = ∅ then exclude j
L15         else add the member of I with the smallest d if ρ_j = 0, else a random member of I; ρ_j ← ρ_j + 1
L16 return the members of P in its first front
```

Line L8 works on the images of $S$. It subtracts the [ideal point](/ideal-point/) $z$ of $S$, with $z_m = \min_{s \in S} f_m(s)$. For each axis $m$ it takes as extreme point the member of $S$ that minimizes the [achievement function](/achievement-scalarizing-function/) $\max_k (f_k - z_k)/w_k$ with $w_m = 1$ and $w_k = 10^{-6}$ for $k \ne m$. The $p$ extreme points fix a hyperplane; its intercepts $a_m$ with the axes divide the translated images. When the extreme points do not span a hyperplane with positive intercepts, the implementation uses the largest translated value of each objective instead. Deb and Jain select parents at random, because the niching already spreads the survivors, and use simulated binary crossover and polynomial mutation as in NSGA-II.

## Example

Let $p = 2$, $N = 5$, $h = 4$, so $Z = \{(0, 1), (\tfrac14, \tfrac34), (\tfrac12, \tfrac12), (\tfrac34, \tfrac14), (1, 0)\}$. The ten images of $R$ sort into $F_1 = \{(0, 10), (1, 1), (10, 0)\}$, $F_2 = \{(2, 8), (3, 6), (4, 4), (7, 2)\}$ and $F_3 = \{(5, 9), (9, 5), (8, 8)\}$. Line L5 stops at $l = 2$ with $\lvert S \rvert = 7 > 5$, so line L7 keeps $F_1$ and sets $K = 2$.

The ideal point of $S$ is $(0, 0)$. The extreme points are $(10, 0)$ and $(0, 10)$, so both intercepts are $10$ and each image is divided by $10$.

| image | front | normalized | nearest line | $d^2$ |
|---|---|---|---|---|
| (0, 10) | $F_1$ | (0, 1) | (0, 1) | 0 |
| (1, 1) | $F_1$ | (0.1, 0.1) | (1/2, 1/2) | 0 |
| (10, 0) | $F_1$ | (1, 0) | (1, 0) | 0 |
| (2, 8) | $F_2$ | (0.2, 0.8) | (1/4, 3/4) | 1/250 |
| (3, 6) | $F_2$ | (0.3, 0.6) | (1/4, 3/4) | 9/1000 |
| (4, 4) | $F_2$ | (0.4, 0.4) | (1/2, 1/2) | 0 |
| (7, 2) | $F_2$ | (0.7, 0.2) | (3/4, 1/4) | 1/1000 |

Line L10 gives the counts $1, 0, 1, 0, 1$ in the order of $Z$. The two lines with count $0$ are $(\tfrac14, \tfrac34)$ and $(\tfrac34, \tfrac14)$. Whichever line L12 picks first, $(\tfrac14, \tfrac34)$ takes its nearest member $(2, 8)$ and $(\tfrac34, \tfrac14)$ takes $(7, 2)$. The new population is $F_1 \cup \{(2, 8), (7, 2)\}$. The point $(4, 4)$ is dropped although its distance is $0$, because its line already has $(1, 1)$.

## Correctness

NSGA-III has no guarantee to reach the front of a general problem; the proof covers the reference points and survival. The Das and Dennis lattice has $\binom{h + p - 1}{p - 1}$ points by a stars and bars count. Survival keeps $F_1, \ldots, F_{l-1}$ whole and adds exactly $K$ members of $F_l$: each round of lines L11 to L15 adds a free member or excludes a line, and a line with a free member is never excluded, so the loop ends after at most $K + H$ rounds. If $F_1(R)$ has at most $N$ members, all of them survive. The first additions go to distinct lines that had count $0$ and a member of $F_l$, each to its nearest member, until such lines run out or $K$ is reached. The full proof is below.

## Complexity

- **Sort, line L4.** $O(p N^2)$ time and $O(N^2)$ space for the fast non-dominated sort on $2N$ members.
- **Normalization, line L8.** $O(p N)$ for the ideal point, $O(p^2 N)$ for the extreme points and $O(p^3)$ for the intercepts by Gaussian elimination.
- **Attachment, line L9.** $O(p N H)$: one distance per member and line.
- **Niching, lines L11 to L15.** At most $K + H$ rounds, each $O(H + N)$ in the simple implementation, so $O((N + H)^2)$.
- **Variation, line L3.** $O(N n)$ and $N$ evaluations at cost $c$.

The total is $O(g (p N^2 + p N H + H^2 + p^3 + N (n + c)))$ time and $O(N^2 + N n + p H)$ space. Deb and Jain take $N$ close to $H$; then a generation costs $O(p N^2 + p^3)$ plus variation and evaluations.

## Properties

- **Elitist.** As in NSGA-II, every member of $F_1(R)$ survives while $F_1(R)$ fits in $N$ places.
- **Empty lines first.** Proved in the correctness file: the first additions go to distinct lines with no member yet.
- **Scale.** The normalization removes the effect of a positive scaling of each objective on the attachment, when the extreme points span a hyperplane. NSGA-II's crowding distance divides by the range of a front, which also removes it; the two methods use different spreads.
- **The lattice grows fast.** $H = \binom{h + p - 1}{p - 1}$; for $h < p$ no lattice point is inside the simplex.
- **Proved running times on test functions.** Wietheger and Doerr (2023) proved an expected $O(n \log n)$ iterations for NSGA-III on the three-objective OneMinMax, under conditions on the number of divisions and on $N$ that their paper states. No such result exists for general problems.

## Variants and improvements

- **Two layers.** For $p \ge 8$ Deb and Jain join a boundary lattice with $h_1$ divisions and an inner lattice with $h_2$ divisions shrunk toward the centre of the simplex. For $p = 8$, $h_1 = 3$ and $h_2 = 2$ give $120 + 36 = 156$ points.
- **Constraints and adaptive points.** Part II of Deb and Jain uses constrained domination and moves reference points that attract no member, for fronts that do not cover the whole simplex.
- **User preferences.** Reference points placed only in a region of interest focus the search there, as in the [reference point method](/reference-point-method/).
- **Decomposition.** [MOEA/D](/moea-d/) uses the same kind of weight vectors, but as subproblems with neighbourhoods instead of niches in a sort.

## When to use it

Use NSGA-III for four or more objectives, when an even spread of trade-offs over the whole front is the goal and the front reaches most of the simplex of directions. For two or three objectives it behaves much like NSGA-II with a different diversity rule. Compare it with MOEA/D and indicator-based methods on the given problems; reported differences are measured results on test suites, budgets and settings.

## Pitfalls

- **Degenerate normalization.** Repeated or collinear extreme points give a singular system or negative intercepts. A fallback is needed, and the choice changes the results.
- **Fronts that miss part of the simplex.** On a disconnected or degenerate front, many lines attract no member and the survivors crowd onto the few lines that do.
- **Too few points.** With $H$ much smaller than $N$, many members share each line and the choice inside a line is at random.
- **Too many points.** With $H$ much larger than $N$, each member has its own line and the niche counts give little information.
- **Ties.** Ties in line L12 and the random choice of line L15 make the run depend on the random stream; fix the seed to reproduce it.

## Implementations

## History

Das and Dennis (1998) used the simplex lattice to place the subproblems of normal-boundary intersection. Zhang and Li used such weight vectors in MOEA/D in 2007. Deb and Jain (2014) joined the lattice with the non-dominated sort of NSGA-II, an adaptive normalization and the niching rule, and reported tests with up to 15 objectives. Jain and Deb gave the constrained and adaptive versions in the same issue.

## References
