---
tag: 00CG0J
kind: concept
slug: nadir-point
name: Nadir point
aliases:
- nadir vector
- nadir objective vector
area: optimization/multi-objective
level: intro
summary: The vector whose i-th entry is the worst value of the i-th objective over the Pareto front. With the ideal point it bounds the front, but it is hard to compute when there are three or more objectives.
prereqs: [ideal-point]
see_also: [pareto-front, pareto-front-computation, weighted-tchebycheff-method, achievement-scalarizing-function, hypervolume-indicator]
sources:
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 2 (bounds on the nondominated set, the ideal and nadir points, and the payoff table)
  - paper: doi:10.1016/0377-2217(88)90257-3
    title: Heinz Isermann and Ralph E. Steuer, Computational experience concerning payoff tables and minimum criterion values over the efficient set, European Journal of Operational Research 33(1), 1988
    locator: pages 91 to 97 (the payoff table can be far from the true nadir values)
  - paper: doi:10.1016/S0377-2217(02)00595-7
    title: Matthias Ehrgott and Dagmar Tenfelde-Podehl, Computation of ideal and Nadir values and implications for their use in MCDM methods, European Journal of Operational Research 151(1), 2003
    locator: pages 119 to 139
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part I, Chapter 2 (the nadir objective vector and its estimation)
---

The nadir point of a [multi-objective optimization](/multi-objective-optimization/) problem is the vector $y^N$ whose $i$-th entry is the worst value of the $i$-th objective over the [Pareto front](/pareto-front/), not over the whole feasible set. Together with the [ideal point](/ideal-point/) it gives the smallest box that holds the front, so it is used to normalize the objectives and to set reference points. For two objectives it costs two lexicographic single-objective solves. For three or more objectives it is an optimization over the efficient set, and the cheap payoff table estimate can be wrong in both directions.

## In plain words

Look only at the fair trade-offs, the choices that no other choice beats on every count. Among them, find the worst price, the worst weight and the worst speed. Put these three worst numbers together, and you have the nadir point.

It is a pessimistic corner: no fair trade-off is worse than it in any measure. Choices that are worse are wasteful, so they do not count.

With the ideal point, the best corner, the nadir point marks a box. Every fair trade-off lies in the box. The size of the box in each direction tells you how much each measure can change among the fair choices, so you can put measures with different units on one scale.

## The idea

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, $Y = f(X)$, and $Y_N$ is the front.

**Definition.**

$$y^N_i = \sup_{y \in Y_N} y_i, \qquad i = 1, \ldots, p.$$

The supremum is over the front only. The worst value over all of $Y$ is often much larger, or infinite, and it says nothing about the trade-offs. By the definition and by the [ideal point](/ideal-point/), $y^I \leqq y \leqq y^N$ for each $y \in Y_N$.

**Two objectives.** Let $p = 2$, let $Y$ be compact and not empty, and let $a$ be the lexicographic minimizer of $(y_1, y_2)$ over $Y$ and $b$ the lexicographic minimizer of $(y_2, y_1)$. Then $y^N = (b_1, a_2)$.

*Proof.* The point $a$ minimizes $y_1$ and, among those points, $y_2$. No point dominates $a$: a point with a smaller first entry does not exist, and a point with the same first entry and a smaller second entry contradicts the second step. So $a \in Y_N$, and likewise $b \in Y_N$. For two objectives the front is monotone: if $y, y' \in Y_N$ and $y_2 < y'_2$ then $y_1 > y'_1$. Let $y \in Y_N$. Since $b$ has the least second entry in $Y$, $y_2 \ge b_2$. If $y_2 > b_2$ then $y_1 < b_1$ by monotonicity, and if $y_2 = b_2$ then $y_1 = b_1$ by the definition of $b$. So $y_1 \le b_1$, with equality at $y = b$. Thus $y^N_1 = b_1$, and $y^N_2 = a_2$ by symmetry. $\square$

**The payoff table.** For $p \ge 3$, a common estimate solves $\min_{x \in X} f_k(x)$ for each $k$, with a solution $x^k$, and writes the $p \times p$ table of the values $f_i(x^k)$. The diagonal is the ideal point. The estimate is $\tilde{y}^N_i = \max_k f_i(x^k)$, the largest entry of column $i$. It can fail in two ways.

- *Overestimate.* If a minimizer $x^k$ is only weakly Pareto optimal, its other entries can be larger than every value on the front. Lexicographic minimizers remove this error, because they are Pareto optimal, so then $\tilde{y}^N \leqq y^N$.
- *Underestimate.* Even with Pareto optimal minimizers, a point of the front that minimizes no single objective can have a larger entry than all rows of the table. The example below shows it. So for $p \ge 3$ the payoff table gives only a lower bound, and the error can be large (Isermann and Steuer, 1988).

**Exact computation.** In general $y^N_i = \max \{ f_i(x) : x \in X_E \}$, an optimization over the efficient set. This set is not convex, even for a linear program, so the problem is a hard global optimization. For a finite set of vectors one computes the front first, for example with [Kung's algorithm](/kung-algorithm/), and then takes $p$ maxima. Ehrgott and Tenfelde-Podehl (2003) study exact methods for combinatorial problems.

**Uses.**

- **Normalization.** $\bar{y}_i = (y_i - y^I_i) / (y^N_i - y^I_i)$ maps the front into $[0, 1]^p$. With a wrong nadir point, some objectives get too much or too little weight.
- **Reference points.** Interactive methods such as the [reference point method](/reference-point-method/) show the decision maker the ranges $[y^I_i, y^N_i]$, so that the aspiration levels are realistic.
- **Quality indicators.** The reference point of the [hypervolume indicator](/hypervolume-indicator/) is often set slightly worse than the nadir point.

## Examples

**A finite set with two objectives.** For the images $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$, the lexicographic minimizers are $a$ for $f_1$ and $g$ for $f_2$. So $y^N = (g_1, a_2) = (9, 9)$. The worst values over all of $Y$ are the same here, but only by chance. With one more image $h = (10, 10)$, the worst values over $Y$ become $(10, 10)$, while $h$ is dominated and $y^N$ stays $(9, 9)$.

**An overestimate.** Let $Y = \{(0, 3), (0, 5), (4, 0)\}$. Both $(0, 3)$ and $(0, 5)$ minimize $f_1$. If a solver returns $(0, 5)$, the payoff table gives $\tilde{y}^N = (4, 5)$. The front is $\{(0, 3), (4, 0)\}$, so $y^N = (4, 3)$.

**An underestimate with three objectives.** Let $Y = \{A, B, C, D\}$ with $A = (0, 5, 5)$, $B = (5, 0, 5)$, $C = (5, 5, 0)$ and $D = (1, 1, 9)$. The point $D$ is nondominated: it is better than $A$ in the second entry, and better than $B$ and $C$ in the first. The single-objective minimizers are $A$, $B$ and $C$, each unique, so the payoff table is

| minimizer of | $f_1$ | $f_2$ | $f_3$ |
|---|---|---|---|
| $f_1$: $A$ | 0 | 5 | 5 |
| $f_2$: $B$ | 5 | 0 | 5 |
| $f_3$: $C$ | 5 | 5 | 0 |

and it gives $\tilde{y}^N = (5, 5, 5)$. The true nadir point is $(5, 5, 9)$, because of $D$.

**A continuous problem.** For $f_1(x) = x^2$ and $f_2(x) = (x - 2)^2$ on $\mathbb{R}$, the front ends at the images of $x = 0$ and $x = 2$, which are $(0, 4)$ and $(4, 0)$. So $y^N = (4, 4)$, while the worst values over the whole feasible set are infinite.

## Where it is used

- The [ideal point](/ideal-point/) and the nadir point normalize the objectives of the [weighted Tchebycheff method](/weighted-tchebycheff-method/), the [achievement scalarizing function](/achievement-scalarizing-function/) and [NSGA-III](/nsga-iii/).
- The [epsilon-constraint method](/epsilon-constraint-method/) chooses its bounds $\varepsilon_j$ in the range $[y^I_j, y^N_j]$; values outside this range give no new points.
- The [reference point method](/reference-point-method/) shows the ranges of the front to the decision maker.
- The [hypervolume indicator](/hypervolume-indicator/) needs a reference point at or beyond the nadir point.

## References
