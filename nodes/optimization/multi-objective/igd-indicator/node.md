---
tag: 4MNQFD
kind: concept
slug: igd-indicator
name: Inverted generational distance
aliases:
- IGD
- IGD indicator
- inverted generational distance indicator
area: optimization/multi-objective
level: advanced
summary: The average distance from each point of a reference front to the nearest point of an approximation set. It is not Pareto compliant; the IGD+ variant is weakly compliant.
prereqs: [pareto-front, pareto-dominance]
see_also: [hypervolume-indicator, epsilon-indicator, spread-indicator, approximate-pareto-set, multi-objective-evolutionary-algorithm, moea-d, nsga-iii, k-nearest-neighbors]
sources:
  - paper: doi:10.1007/978-3-540-24694-7_71
    title: Carlos A. Coello Coello and Margarita Reyes Sierra, A study of the parallelization of a coevolutionary multi-objective evolutionary algorithm, MICAI 2004, Lecture Notes in Artificial Intelligence 2972, Springer, 2004, 688-697
    locator: the inverted generational distance as a measure of the results, the source usually cited for the name
  - paper: doi:10.1109/TEVC.2003.810761
    title: Peter A. N. Bosman and Dirk Thierens, The balance between proximity and diversity in multiobjective evolutionary algorithms, IEEE Transactions on Evolutionary Computation 7(2), 2003, 174-188
    locator: the average distance from a reference front to the approximation set, used as a combined measure of proximity and diversity
  - paper: doi:10.1007/978-3-319-15892-1_8
    title: Hisao Ishibuchi, Hiroyuki Masuda, Yuki Tanigaki and Yusuke Nojima, Modified distance calculation in generational distance and inverted generational distance, EMO 2015, Lecture Notes in Computer Science 9019, Springer, 2015, 110-125
    locator: the IGD+ distance, the counterexamples to Pareto compliance of IGD, and the weak Pareto compliance of IGD+
  - paper: doi:10.1109/TEVC.2011.2161872
    title: Oliver Schütze, Xavier Esquivel, Adriana Lara and Carlos A. Coello Coello, Using the averaged Hausdorff distance as a performance measure in evolutionary multiobjective optimization, IEEE Transactions on Evolutionary Computation 16(4), 2012, 504-522
    locator: the indicator Δp as the larger of power means of GD and IGD, and its metric properties
  - paper: doi:10.1109/TEVC.2003.810758
    title: Eckart Zitzler, Lothar Thiele, Marco Laumanns, Carlos M. Fonseca and Viviane Grunert da Fonseca, Performance assessment of multiobjective optimizers, an analysis and review, IEEE Transactions on Evolutionary Computation 7(2), 2003, 117-132
    locator: the relations between approximation sets and the definition of compatible and complete indicators
---

The inverted generational distance (IGD) of an approximation set $A$ is the average, over the points $r$ of a reference set $R$ that samples the [Pareto front](/pareto-front/), of the distance from $r$ to the nearest point of $A$. A small IGD means that every part of the reference front has a point of $A$ close to it, so it measures convergence and spread at once. IGD is not Pareto compliant: a set that is better in the dominance sense can have a larger IGD. The variant IGD+ of Ishibuchi et al. (2015) counts only the coordinates in which a point is worse than the reference point, and it is weakly Pareto compliant.

## In plain words

You need a list of good trade-offs to compare against, spread along the best possible trade-offs. For each point on that list, find the nearest of your solutions and note how far away it is. Average these distances. If your solutions cover the whole list closely, the average is small. If they miss a region, the points there are far from everything and raise the average. The plain version also counts it against you when your solution is better than the list point, which can make a better set look worse. The plus version counts only the ways in which your solution is worse.

## The idea

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$. $A$ is the set to judge and $R$ a finite reference set. $\lVert \cdot \rVert$ is the Euclidean norm. Smaller values are better for every indicator on this page.

**Definitions.**

- **Generational distance** (Van Veldhuizen, 1999): $\mathrm{GD}(A, R) = \frac{1}{\lvert A \rvert} \sum_{a \in A} \min_{r \in R} \lVert a - r \rVert$. Some authors take a power mean of order $q$ instead. It measures only convergence: one point on the front gives $\mathrm{GD} = 0$.
- **Inverted generational distance:** $\mathrm{IGD}(A, R) = \frac{1}{\lvert R \rvert} \sum_{r \in R} \min_{a \in A} \lVert a - r \rVert$.
- **IGD+** (Ishibuchi, Masuda, Tanigaki and Nojima, 2015): $\mathrm{IGD}^+(A, R) = \frac{1}{\lvert R \rvert} \sum_{r \in R} \min_{a \in A} d^+(r, a)$, with $d^+(r, a) = \big(\sum_m \max(a_m - r_m, 0)^2\big)^{1/2}$.
- **Averaged Hausdorff distance** (Schütze et al., 2012): $\Delta_q(A, R) = \max(\mathrm{GD}_q, \mathrm{IGD}_q)$, with power means of order $q$.

Each costs $O(p \lvert A \rvert \lvert R \rvert)$ time by brute force; a [nearest-neighbour](/k-nearest-neighbors/) structure on $A$ speeds up IGD for small $p$.

**Relations between sets.** $A \trianglelefteq B$ ($A$ weakly dominates $B$) when every $b \in B$ is weakly dominated by some $a \in A$. $A \triangleleft B$ ($A$ is better) when $A \trianglelefteq B$ but not $B \trianglelefteq A$. An indicator to minimize is *weakly Pareto compliant* when $A \trianglelefteq B$ implies $I(A) \le I(B)$, and *Pareto compliant* when $A \triangleleft B$ implies $I(A) < I(B)$.

**IGD is not even weakly compliant.** Let $R = \{(0, 10), (10, 0)\}$, $A = \{(0, 10)\}$ and $B = \{(0, 11), (10, 11)\}$. The point $(0, 10)$ weakly dominates both points of $B$, and no point of $B$ weakly dominates $(0, 10)$, so $A \triangleleft B$. But

$$\mathrm{IGD}(A, R) = \tfrac12 \big(0 + \sqrt{10^2 + 10^2}\big) = \tfrac{\sqrt{200}}{2} \approx 7.07, \qquad \mathrm{IGD}(B, R) = \tfrac12 (1 + 11) = 6,$$

so IGD prefers the worse set $B$. The reason is that the Euclidean distance also charges $a$ for coordinates where $a$ is better than $r$: $(0, 10)$ is $10$ better than $(10, 0)$ in the first objective, and that counts as distance. For the same sets $\mathrm{IGD}^+(A, R) = \frac12 (0 + 10) = 5$ and $\mathrm{IGD}^+(B, R) = \frac12 (1 + 11) = 6$, the right order.

**Theorem (IGD+ is weakly Pareto compliant).** For any finite $R$ and finite nonempty $A$, $B$, if $A \trianglelefteq B$ then $\mathrm{IGD}^+(A, R) \le \mathrm{IGD}^+(B, R)$.

*Proof.* Fix $r \in R$ and let $b \in B$ reach $\min_{b \in B} d^+(r, b)$. Some $a \in A$ has $a_m \le b_m$ for all $m$. Then $\max(a_m - r_m, 0) \le \max(b_m - r_m, 0)$ for each $m$, so $d^+(r, a) \le d^+(r, b)$, and $\min_{a \in A} d^+(r, a) \le \min_{b \in B} d^+(r, b)$. Average over $r$. $\square$

**IGD+ is not strictly compliant.** With the same $R$, $A = \{(0, 10), (10, 0), (5, 5)\}$ is better than $B = \{(0, 10), (10, 0)\}$, because no point of $B$ weakly dominates $(5, 5)$, yet IGD and IGD+ are $0$ for both. A point that adds new trade-offs between the reference points is invisible. The [hypervolume](/hypervolume-indicator/) separates these two sets.

**Dependence on the reference set.** All these values depend on $R$. A coarse or uneven $R$ rewards sets that match its points, and a set can have $\mathrm{IGD} = 0$ only when it contains every point of $R$. With an exact front, $R$ is a sample of it; otherwise it is often the non-dominated union of all the outputs being compared, which changes when one more method is added. Objectives on different scales should be normalized before distances are taken.

## Examples

**Hand values.** Let $R = \{(0, 4), (2, 2), (4, 0)\}$ and $A = \{(1, 3), (4, 1)\}$.

| $r$ | nearest $a$ | $\lVert a - r \rVert$ | $d^+(r, a)$ |
|---|---|---|---|
| (0, 4) | (1, 3) | $\sqrt 2$ | 1, from $(1, 0)$ |
| (2, 2) | (1, 3) | $\sqrt 2$ | 1, from $(0, 1)$ |
| (4, 0) | (4, 1) | 1 | 1, from $(0, 1)$ |

So $\mathrm{IGD} = (2\sqrt 2 + 1)/3 \approx 1.276$ and $\mathrm{IGD}^+ = 1$. In the other direction, $(1, 3)$ is $\sqrt 2$ from its nearest reference point and $(4, 1)$ is $1$ from $(4, 0)$, so $\mathrm{GD} = (\sqrt 2 + 1)/2 \approx 1.207$. Note that $(1, 3)$ is at $d^+ = 1$ from $(0, 4)$, not $\sqrt 2$: it is better than $(0, 4)$ in the second objective, and IGD+ does not count that.

**The counterexamples above.** The implementation checks the values $\sqrt{200}/2$ and $6$ for IGD, $5$ and $6$ for IGD+, the equal values $0$ for the sets with and without $(5, 5)$, and the weak compliance of IGD+ on random pairs $A \trianglelefteq B$ with a fixed seed.

## Where it is used

- **Benchmarks with known fronts.** Test suites such as ZDT, DTLZ and WFG have known fronts, so $R$ can be a dense sample, and IGD is reported in many studies, among them those of [MOEA/D](/moea-d/) and [NSGA-III](/nsga-iii/).
- **Many objectives.** IGD costs $O(p \lvert A \rvert \lvert R \rvert)$, while the hypervolume grows fast with $p$, so IGD is a common choice for many objectives. This cost advantage comes with the loss of compliance.
- **Indicator-based selection.** IGD+ and IGD with a reference set built during the run are used as selection criteria in some evolutionary methods.
- **With other indicators.** Because a single unary indicator cannot detect $A \triangleleft B$ in general (Zitzler et al., 2003), studies report IGD with the hypervolume or the [epsilon indicator](/epsilon-indicator/), and should report the reference set and normalization.

## References
