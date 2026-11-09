---
tag: X557ES
kind: concept
slug: hypervolume-indicator
name: Hypervolume indicator
aliases:
- S-metric
- hypervolume
- size of the dominated space
- Lebesgue measure indicator
area: optimization/multi-objective
level: advanced
summary: The volume of the region that a set of images dominates and that a reference point bounds. If one set is better than another, it has a larger hypervolume.
prereqs: [pareto-dominance, pareto-front]
see_also: [hypervolume-computation, epsilon-indicator, igd-indicator, spread-indicator, klee-measure-problem, multi-objective-evolutionary-algorithm, approximate-pareto-set, spea]
sources:
  - paper: doi:10.1007/BFb0056872
    title: Eckart Zitzler and Lothar Thiele, Multiobjective optimization using evolutionary algorithms, a comparative case study, Parallel Problem Solving from Nature, PPSN V, Lecture Notes in Computer Science 1498, Springer, 1998, 292-301
    locator: the size of the space covered as a measure of a front, on the multi-objective 0/1 knapsack problem
  - paper: doi:10.1109/TEVC.2003.810758
    title: Eckart Zitzler, Lothar Thiele, Marco Laumanns, Carlos M. Fonseca and Viviane Grunert da Fonseca, Performance assessment of multiobjective optimizers, an analysis and review, IEEE Transactions on Evolutionary Computation 7(2), 2003, 117-132
    locator: the relations between approximation sets, the compatibility and completeness of indicators, and the limits of unary indicators
  - paper: doi:10.1007/3-540-36970-8_37
    title: Mark Fleischer, The measure of Pareto optima, applications to multi-objective metaheuristics, Evolutionary Multi-Criterion Optimization, EMO 2003, Lecture Notes in Computer Science 2632, Springer, 2003, 519-533
    locator: the theorem that the measure is maximal exactly for sets that contain the Pareto optima
  - paper: doi:10.1145/1527125.1527138
    title: Anne Auger, Johannes Bader, Dimo Brockhoff and Eckart Zitzler, Theory of the hypervolume indicator, optimal μ-distributions and the choice of the reference point, Foundations of Genetic Algorithms, FOGA 2009, ACM, 87-102
    locator: the optimal μ-distributions on biobjective fronts and the reference point that keeps the extreme points
  - paper: doi:10.1016/j.ejor.2006.08.008
    title: Nicola Beume, Boris Naujoks and Michael Emmerich, SMS-EMOA, multiobjective selection based on dominated hypervolume, European Journal of Operational Research 181(3), 2007, 1653-1669
    locator: the steady-state selection that removes the point with the smallest exclusive contribution in the last front
  - paper: doi:10.1145/3453474
    title: Andreia P. Guerreiro, Carlos M. Fonseca and Luís Paquete, The hypervolume indicator, computational problems and algorithms, ACM Computing Surveys 54(6), 2021, article 119
    locator: the definitions, the properties of the indicator, and the survey of the computational problems
---

The hypervolume indicator of a finite set $A$ of images is the volume of the part of objective space that $A$ dominates and that a reference point $r$ bounds. Zitzler and Thiele used it in 1998 as the size of the space covered. It is strictly Pareto compliant, unlike IGD and spread: if $A$ is better than $B$ in the dominance sense and the points of $A$ strictly dominate $r$, then $A$ has a strictly larger hypervolume. The price is the cost of computing it, which grows fast with the number of objectives (see [hypervolume computation](/hypervolume-computation/)).

## In plain words

Draw a corner point that is worse than every solution you care about. Each solution then marks a box between itself and that corner. The hypervolume is the size of the area, or volume, that these boxes cover together. Better solutions sit further from the corner and make bigger boxes, and solutions spread along the trade-off cover more ground than solutions in one clump. If one set of solutions beats another set, it always covers more. The value depends on the corner you choose, so two sets that do not beat each other can swap order when you move the corner.

## The idea

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size (here the number of points in a set), and $y = f(x)$ is the image of $x$. Write $a \preceq b$ when $a$ weakly dominates $b$, that is $a_m \le b_m$ for all $m$, and $a < r$ when $a_m < r_m$ for all $m$.

**Definition.** For a finite $A \subset \mathbb{R}^p$ and a reference point $r \in \mathbb{R}^p$,

$$\mathrm{HV}(A; r) = \lambda\Big(\bigcup_{a \in A,\ a < r} [a_1, r_1] \times \cdots \times [a_p, r_p]\Big),$$

where $\lambda$ is the Lebesgue measure. The union is the *dominated region* $D(A) = \{z \le r : a \preceq z \text{ for some } a \in A\}$, up to a set of measure zero. A point that does not strictly dominate $r$ adds nothing. For $p = 2$, with the points of $A$ that are not dominated sorted by the first objective, $a^1, \ldots, a^k$, the region is a staircase and $\mathrm{HV} = \sum_i (r_1 - a^i_1)(h_{i} - a^i_2)$, where $h_1 = r_2$ and $h_i = a^{i-1}_2$.

**Relations between sets.** Following Zitzler et al. (2003), $A$ weakly dominates $B$, written $A \trianglelefteq B$, when every $b \in B$ is weakly dominated by some $a \in A$. $A$ is *better* than $B$, written $A \triangleleft B$, when $A \trianglelefteq B$ but not $B \trianglelefteq A$. An indicator $I$ to maximize is *Pareto compliant* when $A \triangleleft B$ implies $I(A) > I(B)$.

**Theorem (Pareto compliance).** Let $A$ and $B$ be finite.

1. If $A \trianglelefteq B$, then $\mathrm{HV}(A; r) \ge \mathrm{HV}(B; r)$.
2. If $A \triangleleft B$ and every point of $A$ strictly dominates $r$, then $\mathrm{HV}(A; r) > \mathrm{HV}(B; r)$.

*Proof.* (1) Let $z \in D(B)$, with $b \preceq z \le r$. Some $a \in A$ has $a \preceq b$, so $a \preceq z$ and $z \in D(A)$. So $D(B) \subseteq D(A)$, and the measure is monotone. (2) Since $B \trianglelefteq A$ fails, some $a \in A$ is weakly dominated by no $b \in B$. For each $b \in B$ there is then a coordinate $m$ with $b_m > a_m$. Let $\delta > 0$ be the smaller of $\min_{b \in B} \max_m (b_m - a_m)$ and $\min_m (r_m - a_m)$; both are positive because $B$ is finite and $a < r$. The box $Q = [a_1, a_1 + \delta) \times \cdots \times [a_p, a_p + \delta)$ lies in $D(A)$. For any $z \in Q$ and $b \in B$, take $m$ with $b_m - a_m \ge \delta$; then $z_m < a_m + \delta \le b_m$, so $b \not\preceq z$. So $Q$ misses $D(B)$, and $\mathrm{HV}(A; r) \ge \mathrm{HV}(B; r) + \delta^p$. $\square$

The hypothesis in (2) is needed: with $r = (5, 5)$, $A = \{(1, 1), (6, 0)\}$ is better than $B = \{(1, 1)\}$, but $(6, 0)$ does not dominate $r$, and both sets have hypervolume $16$.

**Corollary (maximal sets).** Let $Y$ be a finite set of feasible images and $F$ its Pareto-optimal points that strictly dominate $r$. A subset $A \subseteq Y$ has the largest hypervolume among the subsets of $Y$ if and only if $F \subseteq A$. This is the finite form of Fleischer's theorem (2003).

*Proof.* Let $A' = \{a \in A : a < r\}$, which has the same hypervolume as $A$. Each $a \in A'$ is weakly dominated by a Pareto-optimal $y \in Y$, and $y \preceq a < r$ puts $y$ in $F$. So $F \trianglelefteq A'$ and $\mathrm{HV}(F) \ge \mathrm{HV}(A)$ by (1). If $F \subseteq A$, then $F \subseteq A'$, so also $A' \trianglelefteq F$, and (1) both ways gives $\mathrm{HV}(A) = \mathrm{HV}(F)$. If some $y \in F$ is not in $A$, then no point of $A'$ weakly dominates $y$: such a point would equal $y$, because $y$ is Pareto-optimal. So $A' \trianglelefteq F$ fails, $F \triangleleft A'$, and (2) gives $\mathrm{HV}(F) > \mathrm{HV}(A)$. $\square$

**What one value cannot say.** $\mathrm{HV}(A) > \mathrm{HV}(B)$ implies, by (1), only that $B \trianglelefteq A$ fails. It does not imply $A \triangleleft B$: for two sets that do not dominate each other, the order depends on $r$. Zitzler et al. (2003) showed that no unary indicator, and no finite combination of unary indicators, can detect $A \triangleleft B$ for all pairs; a binary indicator such as the [epsilon indicator](/epsilon-indicator/) can. Other common indicators are not Pareto compliant: the [IGD](/igd-indicator/) and [spread](/spread-indicator/) pages give counterexamples.

**Exclusive contribution.** The contribution of $a \in A$ is $\mathrm{HV}(A) - \mathrm{HV}(A \setminus \{a\})$, the volume that only $a$ dominates. For $p = 2$ and the sorted points above, it is $(a^{i+1}_1 - a^i_1)(a^{i-1}_2 - a^i_2)$, with $a^{k+1}_1 = r_1$ and $a^0_2 = r_2$. A dominated point has contribution $0$.

**Invariance and bias.** Multiplying objective $m$ and $r_m$ by $c > 0$ multiplies every hypervolume by $c$, so the order of sets does not change. A nonlinear monotone change of an objective can change the order. Auger, Bader, Brockhoff and Zitzler (2009) studied the sets of $\mu$ points with the largest hypervolume on biobjective fronts: on a linear front the points are evenly spaced, and in general their density depends on the slope of the front. They also gave reference points that make the extreme points of the front part of such sets.

**Cost.** For $p = 2$ the sweep above takes $O(N \log N)$ time. For $p = 3$, Beume et al. gave $O(N \log N)$. In general the problem is #P-hard in $p$, and the best general bounds come from the [Klee measure problem](/klee-measure-problem/); see [hypervolume computation](/hypervolume-computation/).

## Examples

**A biobjective set.** Let $r = (5, 5)$ and $A = \{(1, 4), (2, 2), (4, 1)\}$. The staircase gives $(5 - 1)(5 - 4) + (5 - 2)(4 - 2) + (5 - 4)(2 - 1) = 4 + 6 + 1 = 11$. The exclusive contributions are $(2 - 1)(5 - 4) = 1$, $(4 - 2)(4 - 2) = 4$ and $(5 - 4)(2 - 1) = 1$.

**A better set has more volume.** Replace $(2, 2)$ by $(3, 3)$: $B = \{(1, 4), (3, 3), (4, 1)\}$. Then $A \triangleleft B$, and $\mathrm{HV}(B) = 4 + 2 \cdot 1 + 1 \cdot 2 = 8 < 11$. The contributions in $B$ are $2$, $1$ and $2$.

**Three objectives.** Let $r = (4, 4, 4)$ and $C = \{(1, 2, 3), (2, 3, 1), (3, 1, 2)\}$. Each box has volume $3 \cdot 2 \cdot 1 = 6$. Each pair of boxes meets in a box of volume $2$, for example $[(2, 3, 3), r]$ has volume $2 \cdot 1 \cdot 1$, and all three meet in $[(3, 3, 3), r]$ of volume $1$. By inclusion and exclusion, $\mathrm{HV}(C) = 18 - 6 + 1 = 13$, and each point contributes $3$.

**The reference point changes the order.** Take $A = \{(0, 2)\}$ and $B = \{(1, 1)\}$, which do not dominate each other.

| $r$ | $\mathrm{HV}(A)$ | $\mathrm{HV}(B)$ | larger |
|---|---|---|---|
| (3, 3) | 3 · 1 = 3 | 2 · 2 = 4 | B |
| (3, 10) | 3 · 8 = 24 | 2 · 9 = 18 | A |

The implementation checks these values and checks the general formula against inclusion and exclusion with exact fractions and against a count of unit cells on a grid. It also checks both parts of the compliance theorem on random pairs with fixed seeds.

## Where it is used

- **Benchmarking.** It is a standard indicator for comparing the output of [multi-objective evolutionary algorithms](/multi-objective-evolutionary-algorithm/) and other methods, often with the epsilon indicator, as Zitzler et al. (2003) recommend. The reference point and any normalization must be reported.
- **Selection.** SMS-EMOA of Beume, Naujoks and Emmerich (2007) removes the point of the last front with the smallest exclusive contribution. MO-CMA-ES and HypE also select by contributions, HypE with Monte Carlo estimates for many objectives.
- **Archiving.** Bounded archives can keep the subset with the largest hypervolume, which by the corollary keeps Pareto-optimal points when there is room.
- **Set-based search.** Because it is compliant, the hypervolume turns a multi-objective problem into the single-objective problem of finding a set with maximal volume; Fleischer (2003) used it as the objective of a simulated annealing over sets.

## References
