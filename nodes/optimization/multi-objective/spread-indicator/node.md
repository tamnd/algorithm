---
tag: B4114Q
kind: concept
slug: spread-indicator
name: Spread indicator
aliases:
- Delta metric
- generalized spread
- diversity metric
- spacing
area: optimization/multi-objective
level: advanced
summary: Measures how evenly an approximation set is spaced along the front and how close its ends are to the extreme points. It is not Pareto compliant.
prereqs: [pareto-front, crowding-distance]
see_also: [hypervolume-indicator, igd-indicator, epsilon-indicator, nsga-ii, crowding-distance, multi-objective-evolutionary-algorithm, ideal-point, nadir-point]
sources:
  - paper: doi:10.1109/4235.996017
    title: Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal and T. Meyarivan, A fast and elitist multiobjective genetic algorithm, NSGA-II, IEEE Transactions on Evolutionary Computation 6(2), 2002, 182-197
    locator: the diversity metric Δ with the distances to the extreme solutions, in the section on simulation results
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 8, the performance metrics for diversity, among them Schott's spacing and the spread Δ
  - paper: "Aimin Zhou, Yaochu Jin, Qingfu Zhang, Bernhard Sendhoff and Edward Tsang, Combining model-based and genetics-based offspring generation for multi-objective optimization using a convergence criterion, IEEE Congress on Evolutionary Computation, CEC 2006, 892-899"
    locator: the generalized spread for more than two objectives, with nearest-neighbour distances and the extreme points of the reference front
  - paper: doi:10.1109/TEVC.2003.810758
    title: Eckart Zitzler, Lothar Thiele, Marco Laumanns, Carlos M. Fonseca and Viviane Grunert da Fonseca, Performance assessment of multiobjective optimizers, an analysis and review, IEEE Transactions on Evolutionary Computation 7(2), 2003, 117-132
    locator: the relations between approximation sets and the analysis of unary indicators against these relations
---

The spread indicator $\Delta$ measures how evenly the points of an approximation set lie along the front and how close its two ends are to the extreme points of the true front. Deb, Pratap, Agarwal and Meyarivan defined it for two objectives in the NSGA-II paper (2002), and Zhou et al. (2006) generalized it to any number of objectives. A value of $0$ means equal gaps and ends on the extreme points; larger is worse. The spread says nothing about convergence, and it is not Pareto compliant: adding a new non-dominated point to a set, which makes the set strictly better, can raise $\Delta$.

## In plain words

Lay out your solutions along the trade-off curve and look at the gaps between neighbours. If all gaps are equal, the set is evenly spread. Also look at the two ends: if the set stops short of the best possible value of each cost, there is a gap at the end. The spread adds up how far each gap is from the average gap, adds the two end gaps, and divides by a total so that the result is between 0 and about 1. It does not check whether the points are close to the best trade-offs at all. A set of poor solutions can be evenly spread, and adding a good solution can make the spacing uneven.

## The idea

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size (here the size of the set $A$), and $y = f(x)$ is the image of $x$. Smaller spread is better.

**Deb's $\Delta$ for $p = 2$.** Sort $A$ by the first objective, $a^1, \ldots, a^N$. Let $d_i = \lVert a^{i+1} - a^i \rVert$ for $i = 1, \ldots, N - 1$, with mean $\bar d$. Let $d_f$ and $d_l$ be the Euclidean distances from the two extreme points of the true front to $a^1$ and $a^N$. Then

$$\Delta = \frac{d_f + d_l + \sum_{i=1}^{N-1} \lvert d_i - \bar d \rvert}{d_f + d_l + (N - 1)\, \bar d}.$$

It is $0$ exactly when the gaps are equal and the ends are the extreme points. Because $\lvert d_i - \bar d \rvert \le d_i + \bar d$ and $\sum_i d_i = (N - 1) \bar d$, the numerator is at most twice the denominator, so $0 \le \Delta \le 2$.

**Generalized spread for any $p$.** Zhou et al. (2006) replace the gaps between sorted neighbours, which do not exist for $p \ge 3$, by the distance $d(x, A)$ from each $x \in A$ to its nearest other point of $A$, with mean $\bar d$, and the end gaps by the distances $d(e_m, A)$ from the extreme points $e_1, \ldots, e_p$ of a reference front:

$$\Delta^* = \frac{\sum_{m} d(e_m, A) + \sum_{x \in A} \lvert d(x, A) - \bar d \rvert}{\sum_{m} d(e_m, A) + \lvert A \rvert\, \bar d}.$$

Software differs in how it picks the extreme points; the implementation takes, for each $m$, the reference point with the largest value of objective $m$.

**Schott's spacing.** The spacing $S$ (Schott, 1995) is the sample standard deviation of the nearest-neighbour distances, measured in the $L_1$ norm. It has no end terms, so it does not even see whether the set reaches the ends of the front.

**Cost.** Deb's $\Delta$ takes $O(N \log N)$ time to sort. The generalized spread and the spacing take $O(p N^2)$ by brute force, or less with a nearest-neighbour structure.

**Relations between sets.** $A \trianglelefteq B$ when every point of $B$ is weakly dominated by a point of $A$, and $A \triangleleft B$ ($A$ is better) when $A \trianglelefteq B$ but not $B \trianglelefteq A$. An indicator to minimize is weakly Pareto compliant when $A \trianglelefteq B$ implies $I(A) \le I(B)$, and Pareto compliant when $A \triangleleft B$ implies $I(A) < I(B)$.

**Counterexample: the spread is not even weakly compliant.** Take the front $y_1 + y_2 = 4$ with extreme points $(0, 4)$ and $(4, 0)$. Let $B = \{(0, 4), (2, 2), (4, 0)\}$ and $A = B \cup \{(1, 3)\}$. All points lie on the front, and no point of $B$ weakly dominates $(1, 3)$, so $A \triangleleft B$. For $B$, $d_f = d_l = 0$ and both gaps are $\sqrt 8$, so $\Delta(B) = 0$. For $A$ the gaps are $\sqrt 2, \sqrt 2, \sqrt 8$ with mean $\bar d = 4\sqrt 2 / 3$, the deviations are $\sqrt 2/3, \sqrt 2/3, 2\sqrt 2/3$, and

$$\Delta(A) = \frac{4\sqrt 2 / 3}{3 \cdot 4\sqrt 2 / 3} = \frac13 > 0 = \Delta(B).$$

The generalized spread gives $\Delta^*(B) = 0$ and $\Delta^*(A) = 3/10$ on the same sets. So the better set gets the worse value under both forms. The reason is the design: the indicator rewards equal gaps, and a new point between two old ones breaks the equality even though it adds a new trade-off.

**No convergence information.** Shift $B$ by $(1, 1)$ to $C = \{(1, 5), (3, 3), (5, 1)\}$. Every point of $C$ is dominated by a point of $B$, yet the spacing of $C$ is $0$ like that of $B$, and $\Delta(C) = 2\sqrt 2 / (2\sqrt 2 + 2\sqrt 8) = 1/3$, the same value as the better set $A$ above. Spread must be read together with an indicator of convergence, or replaced by a compliant one such as the [hypervolume](/hypervolume-indicator/).

**Invariance.** Multiplying all objectives by the same factor does not change $\Delta$, $\Delta^*$ or the ratio of $S$ to the mean gap. Scaling one objective alone changes all of them, so objectives on different scales should be normalized first, for example by the [ideal](/ideal-point/) and [nadir](/nadir-point/) points.

## Examples

**Equal gaps reaching the ends.** $B = \{(0, 4), (2, 2), (4, 0)\}$ on the front above: $\Delta = 0$ and $S = 0$.

**Equal gaps, short ends.** $A = \{(1, 3), (3, 1)\}$: one gap $\sqrt 8$, so $\bar d = \sqrt 8$ and the gap term is $0$; $d_f = d_l = \sqrt 2$. Then $\Delta = 2\sqrt 2 / (2\sqrt 2 + 2\sqrt 2) = 1/2$.

**Uneven gaps.** $A = \{(0, 4), (1, 3), (2, 2), (4, 0)\}$: $\Delta = 1/3$ as above. The $L_1$ nearest-neighbour distances are $2, 2, 2, 4$ with mean $5/2$, so $S^2 = (3 \cdot \tfrac14 + \tfrac94)/3 = 1$ and $S = 1$.

The implementation checks these values, the counterexample, the dominated set $C$, and the invariance under a common scale on random sets with a fixed seed.

## Where it is used

- **The NSGA-II study.** Deb et al. (2002) reported $\Delta$ with a convergence metric for [NSGA-II](/nsga-ii/), PAES and SPEA on their test problems; these are measured values on those problems and settings. [Crowding distance](/crowding-distance/) in NSGA-II aims at the same kind of even spacing.
- **Diversity in benchmarks.** $\Delta$, $\Delta^*$ and the spacing are still reported next to convergence measures, mostly for two and three objectives.
- **Diagnosis.** A good hypervolume with a bad spread points to clusters or missing ends, so spread is useful to explain results, not to rank sets.
- **Caution.** The counterexample above shows that a pure diversity indicator does not respect dominance between sets. Zitzler et al. (2003) give the general analysis of unary indicators and the dominance relations between sets.

## References
