---
tag: S2VN4N
kind: technique
slug: weighted-tchebycheff-method
name: Weighted Tchebycheff method
aliases:
- Tchebycheff scalarization
- weighted max-min
- Chebyshev scalarization
- augmented Tchebycheff method
- lexicographic Tchebycheff method
area: optimization/multi-objective
level: core
summary: Minimizes the maximum weighted deviation from an ideal point; can reach nonconvex Pareto points.
prereqs: [scalarization, ideal-point]
see_also: [weighted-sum-method, epsilon-constraint-method, achievement-scalarizing-function, reference-point-method, moea-d, minimax]
sources:
  - paper: doi:10.1007/978-3-642-87563-2_5
    title: V. Joseph Bowman, On the relationship of the Tchebycheff norm and the efficient frontier of multiple-criteria objectives, in Multiple Criteria Decision Making, Lecture Notes in Economics and Mathematical Systems 130, Springer, 1976
    locator: pages 76 to 86 (every efficient point minimizes a weighted Tchebycheff distance to a utopia point)
  - paper: doi:10.1007/BF02591870
    title: Ralph E. Steuer and Eng-Ung Choo, An interactive weighted Tchebycheff procedure for multiple objective programming, Mathematical Programming 26(3), 1983
    locator: pages 326 to 344 (the lexicographic and augmented weighted Tchebycheff programs, and the interactive procedure)
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 4 (compromise solutions, the weighted Tchebycheff norm and its augmented form)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part II, Chapter 3 (the method of weighted metrics and its Tchebycheff case)
---

The weighted Tchebycheff method finds a point of the [Pareto front](/pareto-front/) by minimizing $\max_i w_i (f_i(x) - z_i)$, the largest weighted distance to a reference point $z$ below the [ideal point](/ideal-point/). Unlike the [weighted sum method](/weighted-sum-method/), it reaches every Pareto optimal point, also the unsupported ones in the dents of a nonconvex front: for each Pareto optimal point there are weights that make it optimal. The price is that some optima are only weakly Pareto optimal. A second stage, or a small added sum $\rho \sum_i f_i(x)$, removes them.

## In plain words

Pick a dream point that is better than anything you can reach in every goal. Now draw a box with its corner at the dream point and grow it slowly. The first choice that the box touches is the answer.

The weights set the shape of the box. A box that is long in one direction and short in the other reaches out along a line from the dream point, and it finds the fair trade-off where that line meets the front. Every fair trade-off sits on some such line, so every one can be found, even the ones in a dent.

The box can first touch a flat side of the front, where one choice is no better than another in one goal. A second, small step then picks the best choice on that side.

## When it applies

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, $Y = f(X)$, and $y^I$ is the ideal point. The weights satisfy $w > 0$. The reference point $z$ is a *utopia point*, $z < y^I$, for example $z = y^I - \mathbf{1}$. The problem is

$$T(w) : \quad \min_{x \in X} \ \max_{i = 1, \ldots, p} w_i (f_i(x) - z_i).$$

Use it when:

- the front may be nonconvex, as in integer and combinatorial problems, and all Pareto optimal points must be reachable;
- the solver accepts extra linear constraints, because $T(w)$ is the same as $\min t$ subject to $w_i (f_i(x) - z_i) \le t$ for all $i$, which is linear when the $f_i$ are linear;
- the decision maker thinks in terms of a direction from the ideal point, as in interactive methods.

**Every optimum is weakly Pareto optimal.** Let $w > 0$ and let $\hat{x}$ be optimal for $T(w)$. Then $\hat{x}$ is weakly Pareto optimal. If $f(\hat{x})$ is the only optimal image, $\hat{x}$ is Pareto optimal.

*Proof.* If $f(x) < f(\hat{x})$, then $w_i (f_i(x) - z_i) < w_i (f_i(\hat{x}) - z_i)$ for every $i$, so the maximum is smaller at $x$, a contradiction. If $f(x) \prec f(\hat{x})$, then each term at $x$ is at most the term at $\hat{x}$, so $x$ is also optimal, with a different image. $\square$

The optimum can be dominated. For $Y = \{(0, 2), (0, 1), (1, 0), (3, 0)\}$, $z = (-1, -1)$ and $w = (1, 1/3)$, the values are $1, 1, 2, 4$. Both $(0, 2)$ and $(0, 1)$ are optimal, and $(0, 1)$ dominates $(0, 2)$.

**Every Pareto optimal point is found.** Let $z < y^I$, and let $\hat{x}$ be weakly Pareto optimal with $\hat{y} = f(\hat{x})$. Set $w_i = 1 / (\hat{y}_i - z_i)$, which is positive and finite. Then $\hat{x}$ is optimal for $T(w)$ with the value 1. If $\hat{x}$ is Pareto optimal, every optimal solution has the image $\hat{y}$.

*Proof.* At $\hat{x}$ each term is $w_i (\hat{y}_i - z_i) = 1$. If some $x$ had a value below 1, then $w_i (f_i(x) - z_i) < 1 = w_i (\hat{y}_i - z_i)$ for every $i$, so $f(x) < \hat{y}$, which contradicts weak Pareto optimality. If $x$ is optimal, its value is 1, so $f_i(x) \le \hat{y}_i$ for every $i$. When $\hat{x}$ is Pareto optimal this forces $f(x) = \hat{y}$. $\square$

Geometrically, the optimum is the point where the ray $z + t (1/w_1, \ldots, 1/w_p)$, $t \ge 0$, first meets $Y + \mathbb{R}^p_{\ge}$. The weights above aim the ray at $\hat{y}$. No convexity is needed. This is Bowman's theorem (1976).

**The augmented form gives proper efficiency.** For $\rho > 0$ let

$$T_\rho(w) : \quad \min_{x \in X} \ \max_i w_i (f_i(x) - z_i) + \rho \sum_{i=1}^p (f_i(x) - z_i).$$

Each optimum $\hat{x}$ is Pareto optimal and properly efficient in the sense of Geoffrion, with the trade-off bound $M = (W + \rho (p - 1)) / \rho$, where $W = \max_i w_i$.

*Proof.* The function is strictly increasing, so $\hat{x}$ is Pareto optimal (see [scalarization](/scalarization/)). Let $f_i(x) < f_i(\hat{x})$, and let $\Delta = f(x) - f(\hat{x})$. Since $\max_k (a_k + b_k) \le \max_k a_k + \max_k b_k$, optimality gives $0 \le \max_k w_k \Delta_k + \rho \sum_k \Delta_k$. Let $D = \max_k \Delta_k$, attained at $j$. If $D \le 0$, then $f(x) \prec f(\hat{x})$, which is false, so $D > 0$ and $f_j(x) > f_j(\hat{x})$. Then $\max_k w_k \Delta_k \le W D$ and $\sum_k \Delta_k \le \Delta_i + (p - 1) D$. So $0 \le W D + \rho \Delta_i + \rho (p - 1) D$, that is, $f_i(\hat{x}) - f_i(x) \le M (f_j(x) - f_j(\hat{x}))$. $\square$

**For a finite set, the augmented form still finds every point.** Let $Y$ be finite, $\hat{y} \in Y_N$, and $w_i = 1 / (\hat{y}_i - z_i)$. Let $\delta = \min_{y \in Y, y \ne \hat{y}} \max_k w_k (y_k - \hat{y}_k)$ and $C = \max_{y \in Y} \sum_k \max(0, \hat{y}_k - y_k)$. Then $\delta > 0$, and for $0 < \rho < \delta / C$ (any $\rho > 0$ if $C = 0$), $\hat{y}$ is the only optimal image of $T_\rho(w)$.

*Proof.* Each $y \ne \hat{y}$ has some $y_k > \hat{y}_k$, or it would dominate $\hat{y}$, so $\delta > 0$. Since $w_k (\hat{y}_k - z_k) = 1$ for all $k$, the value of $y$ minus the value of $\hat{y}$ is $\max_k w_k (y_k - \hat{y}_k) + \rho \sum_k (y_k - \hat{y}_k) \ge \delta - \rho C > 0$. $\square$

For an infinite $Y$, a fixed $\rho$ finds only points whose trade-offs are bounded by $M$. Pareto optimal points that are not properly efficient are never found by the augmented form, so a sweep should let $\rho$ shrink or use the two-stage form below.

## The template

The two-stage form of Steuer and Choo (1983), also called the lexicographic weighted Tchebycheff program, solves $T(w)$ and then picks the best point among its optima.

```pseudo id=main
WEIGHTED-TCHEBYCHEFF(X, f, w, z)                  ▷ w > 0, z < y^I
L1  solve  min t  subject to  w_i (f_i(x) − z_i) ≤ t for i = 1, ..., p,  x ∈ X
L2  t* ← the optimal value
L3  solve  min f_1(x) + ... + f_p(x)  subject to  w_i (f_i(x) − z_i) ≤ t* for i = 1, ..., p,  x ∈ X
L4  x̂ ← an optimal solution
L5  return x̂
```

**Correctness.** The feasible set of line L3 is the set of optimal solutions of $T(w)$. If some $x$ had $f(x) \prec f(\hat{x})$, then $w_i (f_i(x) - z_i) \le w_i (f_i(\hat{x}) - z_i) \le t^*$ for all $i$, so $x$ is feasible for line L3 with a smaller sum, a contradiction. So $\hat{x}$ is Pareto optimal. With the weights $w_i = 1/(\hat{y}_i - z_i)$ of a Pareto optimal $\hat{y}$, the feasible set of line L3 has only the image $\hat{y}$, so the template returns it. So the template finds exactly the Pareto optimal points, with no weak ones.

**Cost.** Two single-objective solves per weight vector, with $p$ extra constraints and one extra variable. To trace the front, run the template for a list of weight vectors, often normalized so that $\sum_i w_i = 1$.

### A worked example

Take $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$. The ideal point is $(2, 1)$; take $z = (1, 0)$. For each front point $\hat{y}$ the weights $w_i = 1/(\hat{y}_i - z_i)$ are:

| target | $w$ | value at $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ | optimum |
|---|---|---|---|---|---|---|---|---|---|
| $a$ | $(1, 1/9)$ | **1** | 2 | 3 | 4 | 6 | 7 | 8 | $a$ |
| $b$ | $(1/2, 1/6)$ | 3/2 | **1** | 3/2 | 2 | 3 | 7/2 | 4 | $b$ |
| $d$ | $(1/4, 1/4)$ | 9/4 | 3/2 | 7/4 | **1** | 3/2 | 7/4 | 2 | $d$ |
| $e$ | $(1/6, 1/3)$ | 3 | 2 | 7/3 | 4/3 | **1** | 5/3 | 4/3 | $e$ |
| $g$ | $(1/8, 1)$ | 9 | 6 | 7 | 4 | 3 | 5 | **1** | $g$ |

Each front point is the unique optimum for its weights, with the value 1. In particular the unsupported point $e$, which no weighted sum finds, is optimal for $w = (1/6, 1/3)$: the ray from $(1, 0)$ in the direction $(6, 3)$ passes through $e = (7, 3)$.

For the weak case, take $Y = \{(0, 2), (0, 1), (1, 0), (3, 0)\}$, $z = (-1, -1)$ and $w = (1, 1/3)$. Line L1 gives $t^* = 1$, attained by $(0, 2)$ and $(0, 1)$. Line L3 keeps these two and picks $(0, 1)$, with the smaller sum.

## Classic examples

- **Bowman (1976)** showed that the Tchebycheff distance to a utopia point generates the whole efficient set, convex or not.
- **The interactive procedure of Steuer and Choo (1983).** In each round it samples weight vectors in a shrinking region, solves the augmented or two-stage problems, and shows the decision maker a few spread points.
- **[MOEA/D](/moea-d/).** It decomposes a problem into many Tchebycheff subproblems with fixed weight vectors and solves them together with an evolutionary algorithm, with $z$ set to the best values found so far.
- **Integer programs.** For bicriteria integer programs, the Tchebycheff subproblem keeps linearity with one extra variable, and it reaches the unsupported points that the weighted sum misses.

## Variations

- **Weighted $L_q$ metrics.** Minimize $(\sum_i (w_i (f_i(x) - z_i))^q)^{1/q}$. For $q = 1$ this is a weighted sum; for $q = \infty$ it is the Tchebycheff method. For $1 \le q < \infty$ the optima are Pareto optimal, but only for $q = \infty$ is every Pareto optimal point guaranteed to be reachable.
- **The augmented form.** Add $\rho \sum_i (f_i(x) - z_i)$ with a small $\rho > 0$. One solve, no weak optima, but some points can be missed for an infinite $Y$.
- **The [achievement scalarizing function](/achievement-scalarizing-function/).** The same function with a reference point that need not be a utopia point. It projects any aspiration level onto the front.

## Pitfalls

- **Dominated optima.** A plain solve of $T(w)$ can return a weakly Pareto optimal point that is dominated, as in the example with $(0, 2)$. Use line L3 or the augmented form.
- **A reference point that is not a utopia point.** If $z_i = y^I_i$ for some $i$, the weight $1/(\hat{y}_i - z_i)$ is infinite for points with $\hat{y}_i = y^I_i$. If $z$ is above some points, the function no longer measures a distance. Use $z < y^I$.
- **The size of $\rho$.** A $\rho$ that is too large acts like a weighted sum and hides unsupported points; a $\rho$ that is too small causes numerical trouble in a floating point solver.
- **Weights and spread.** Even steps in the weights give rays that are evenly spaced in angle, not points evenly spaced on the front. Normalize the objectives with the [nadir point](/nadir-point/) first.
- **Hard subproblems.** For combinatorial problems, the max function or the extra constraints destroy the structure. A Tchebycheff shortest path is not a shortest path problem any more.

## Exercises

1. For $Y = \{(0, 1), (1, 0), (0.6, 0.6)\}$ and $z = (-1, -1)$, find weights for which $(0.6, 0.6)$ is the only optimum. *Answer:* $w = (1/1.6, 1/1.6)$, or simply $w = (1, 1)$: the values are $2, 2, 1.6$.
2. Show that the optimal solutions of $T(w)$ do not change when $w$ is multiplied by a positive constant, but that they depend on $z$. *Answer:* scaling $w$ scales every value by the same factor. For $Y = \{(0, 4), (3, 0)\}$ and $w = (1, 1)$, the reference point $z = (-1, -1)$ gives the values 5 and 4, so $(3, 0)$ wins, while $z = (-10, -1)$ gives 10 and 13, so $(0, 4)$ wins.
3. For the seven example points, $z = (1, 0)$ and $w = (1, 1)$, find the optimum of $T(w)$. *Answer:* the values are $9, 6, 7, 4, 6, 7, 8$ for $a$ to $g$, so the optimum is $d$, the front point nearest to $z$ in the maximum norm.

## References
