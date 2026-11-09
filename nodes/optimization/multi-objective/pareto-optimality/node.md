---
tag: 2KEYKE
kind: definition
slug: pareto-optimality
name: Pareto optimality
aliases:
- Pareto efficiency
- Pareto optimal solution
- efficient solution
- nondominated solution
- weak Pareto optimality
- proper Pareto optimality
area: optimization/multi-objective
level: intro
summary: A feasible solution is Pareto optimal when no other feasible solution dominates it. Weak and proper Pareto optimality are the two main variants.
prereqs: [pareto-dominance]
see_also: [pareto-front, multi-objective-optimization, weighted-sum-method, epsilon-constraint-method, weighted-tchebycheff-method, ideal-point]
sources:
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 2 (efficient, weakly and strictly efficient, and properly efficient solutions, and the existence of nondominated points)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part I, Chapter 2 (Pareto optimality, weak and proper Pareto optimality)
  - paper: doi:10.1016/0022-247X(68)90201-1
    title: Arthur M. Geoffrion, Proper efficiency and the theory of vector maximization, Journal of Mathematical Analysis and Applications 22(3), 1968
    locator: pages 618 to 630, the definition of proper efficiency and its characterization by weighted sums
---

A feasible solution of a [multi-objective optimization](/multi-objective-optimization/) problem is Pareto optimal (or efficient) when no other feasible solution [dominates](/pareto-dominance/) it: no solution is at least as good in every objective and strictly better in one. Pareto optimality replaces the single optimal value of ordinary optimization. A problem usually has many Pareto optimal solutions, and their images form the [Pareto front](/pareto-front/). Two variants matter for the methods: weak Pareto optimality, which is what many scalarizations guarantee, and proper Pareto optimality, which excludes unbounded trade-offs.

## Definition

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, the feasible set is $X$, and $y = f(x) = (f_1(x), \ldots, f_p(x))$ is the image of $x$. The image of $X$ is $Y = f(X)$. We use the relations of [Pareto dominance](/pareto-dominance/): $y \leqq y'$ (each coordinate at most), $y \prec y'$ ($y \leqq y'$ and $y \ne y'$) and $y < y'$ (each coordinate strictly smaller).

Let $\hat{x} \in X$ and $\hat{y} = f(\hat{x})$.

- $\hat{x}$ is **Pareto optimal** (efficient) when there is no $x \in X$ with $f(x) \prec \hat{y}$. Then $\hat{y}$ is a **nondominated point**. The sets are $X_E$ and $Y_N = f(X_E)$.
- $\hat{x}$ is **weakly Pareto optimal** when there is no $x \in X$ with $f(x) < \hat{y}$. The sets are $X_{wE}$ and $Y_{wN}$.
- $\hat{x}$ is **strictly Pareto optimal** when there is no $x \in X$ with $x \ne \hat{x}$ and $f(x) \leqq \hat{y}$. So $\hat{x}$ is efficient and no other solution has the same image.
- $\hat{x}$ is **properly Pareto optimal** in the sense of Geoffrion (1968) when it is Pareto optimal and there is a number $M > 0$ with this property: for each $i$ and each $x \in X$ with $f_i(x) < f_i(\hat{x})$, there is an index $j$ with $f_j(x) > f_j(\hat{x})$ and
$$\frac{f_i(\hat{x}) - f_i(x)}{f_j(x) - f_j(\hat{x})} \le M.$$
A gain in one objective must cost a loss in another objective that is at least $1/M$ times as large.
- $\hat{x}$ is **locally Pareto optimal** when $X \subseteq \mathbb{R}^n$ and some neighbourhood $U$ of $\hat{x}$ has no $x \in X \cap U$ with $f(x) \prec \hat{y}$. Local search and gradient methods usually guarantee only this.

**Inclusions.** Strictly Pareto optimal implies Pareto optimal, and Pareto optimal implies weakly Pareto optimal, because $f(x) < \hat{y}$ implies $f(x) \prec \hat{y}$. Properly Pareto optimal implies Pareto optimal by definition. None of the reverse implications holds in general; the examples below show it.

**Existence.** If $Y$ is finite and not empty, then $Y_N$ is not empty. More generally: if $Y$ is not empty and compact, then for each $y \in Y$ there is a $\hat{y} \in Y_N$ with $\hat{y} \leqq y$.

*Proof.* Let $y \in Y$ and $S = \{ y' \in Y : y' \leqq y \}$. The set $S$ contains $y$, and it is compact, because it is the intersection of the compact set $Y$ with a closed set. So the continuous function $s(y') = y'_1 + \cdots + y'_p$ has a minimizer $\hat{y}$ on $S$. Assume that some $y'' \in Y$ has $y'' \prec \hat{y}$. Then $y'' \leqq \hat{y} \leqq y$, so $y'' \in S$, and $s(y'') < s(\hat{y})$ because $y'' \leqq \hat{y}$ with at least one strict coordinate. This contradicts the choice of $\hat{y}$. So $\hat{y} \in Y_N$ and $\hat{y} \leqq y$. A finite set is compact. $\square$

Without compactness, $Y_N$ can be empty. For $Y = \{ y \in \mathbb{R}^2 : y_1 + y_2 > 0 \}$, each $y \in Y$ with $s = y_1 + y_2$ is dominated by $y - (s/2, 0) \in Y$.

## Examples and non-examples

**A finite example.** For the seven images $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$, the Pareto optimal points are $a, b, d, e, g$. The point $c$ is not Pareto optimal and not even weakly Pareto optimal, because $b < c$. The point $f$ is not weakly Pareto optimal either, since $d < f$. In a finite set every Pareto optimal point is also properly Pareto optimal, because the finitely many ratios in the definition have a maximum.

**Weakly but not Pareto optimal.** Let $Y = [0, 1]^2$. The point $(0, 1/2)$ is weakly Pareto optimal: no point of $Y$ has a first coordinate below $0$. It is not Pareto optimal, because $(0, 0) \prec (0, 1/2)$. Here $Y_N = \{(0, 0)\}$, while $Y_{wN}$ is the union of the two edges $\{0\} \times [0, 1]$ and $[0, 1] \times \{0\}$.

**Pareto optimal but not properly Pareto optimal.** Let $X$ be the disc of radius 1 around $(1, 1)$ in $\mathbb{R}^2$, and $f(x) = x$. The front is the quarter circle $\{ (1 - \sin t, 1 - \cos t) : t \in [0, \pi/2] \}$. The end point $\hat{y} = (1, 0)$, at $t = 0$, is Pareto optimal, since it is the only point of $X$ with $y_2 = 0$. But the point of the circle at a small angle $t > 0$ improves $f_1$ by $\sin t$ and worsens $f_2$ by $1 - \cos t$. The ratio $\sin t / (1 - \cos t)$ tends to infinity as $t \to 0$, so no bound $M$ exists. Every point with $0 < t < \pi/2$ is properly Pareto optimal. This is Geoffrion's standard example of an improper efficient point.

**Strict optimality fails with ties.** If two solutions $x \ne x'$ have the same nondominated image, both are Pareto optimal and neither is strictly Pareto optimal. The two paths from $s$ to $t$ of equal cost in a graph are a common case.

**A non-example: the best of each objective.** A minimizer of one objective $f_k$ alone is weakly Pareto optimal, but it need not be Pareto optimal. In $Y = [0, 1]^2$, each point $(0, t)$ minimizes $f_1$, and only $(0, 0)$ is Pareto optimal. The lexicographic minimizer, which minimizes $f_k$ first and then the other objectives in turn, is Pareto optimal (see [lexicographic optimization](/lexicographic-optimization/)).

## Related definitions

- [Pareto dominance](/pareto-dominance/) is the order behind each of these notions.
- The [Pareto front](/pareto-front/) is $Y_N$. Its bounds are the [ideal point](/ideal-point/) and the [nadir point](/nadir-point/).
- **What each scalarization finds.** An optimum of the [weighted sum method](/weighted-sum-method/) with positive weights is Pareto optimal, and in fact properly Pareto optimal. With nonnegative weights it is only weakly Pareto optimal. For a convex problem, Geoffrion's theorem says that the properly Pareto optimal solutions are exactly the optima of weighted sums with positive weights. Each optimum of the [epsilon-constraint method](/epsilon-constraint-method/) and of the [weighted Tchebycheff method](/weighted-tchebycheff-method/) is weakly Pareto optimal, and each Pareto optimal solution is an optimum of both for suitable parameters. The augmented Tchebycheff and [achievement scalarizing functions](/achievement-scalarizing-function/) give properly Pareto optimal points.
- **Supported points.** A nondominated point is supported when it minimizes a weighted sum with positive weights over $Y$. On a nonconvex front some nondominated points are not supported, and the weighted sum method cannot find them.
- [Approximate Pareto sets](/approximate-pareto-set/) and [epsilon-dominance](/epsilon-dominance/) relax the definition by a factor $1 + \varepsilon$.

## References
