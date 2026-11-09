---
tag: 1B27C8
kind: technique
slug: achievement-scalarizing-function
name: Achievement scalarizing function
aliases:
- Wierzbicki achievement function
- achievement function
- order-approximating achievement function
area: optimization/multi-objective
level: advanced
summary: Scalarizing function whose minimum over the feasible set is a Pareto optimal point nearest a reference point, attainable or not. Its sign tells whether the reference point can be reached.
prereqs: [weighted-tchebycheff-method, scalarization]
see_also: [reference-point-method, preference-articulation, nadir-point, ideal-point, weighted-sum-method]
sources:
  - paper: doi:10.1007/978-3-642-48782-8_32
    title: Andrzej P. Wierzbicki, The use of reference objectives in multiobjective optimization, in Multiple Criteria Decision Making Theory and Application, Lecture Notes in Economics and Mathematical Systems 177, Springer, 1980
    locator: pages 468 to 486 (order-representing and order-approximating achievement functions, and the projection of a reference point)
  - paper: doi:10.1007/BF01719738
    title: Andrzej P. Wierzbicki, On the completeness and constructiveness of parametric characterizations to vector optimization problems, OR Spektrum 8(2), 1986
    locator: pages 73 to 87 (every properly efficient point is reached by a reference point, convex or not)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part II (achievement scalarizing functions and the reference point method)
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 4 (achievement functions and reference points)
---

An achievement scalarizing function measures how well an outcome $y$ meets a reference point $\bar{z}$ of aspiration levels: $s(y) = \max_i w_i (y_i - \bar{z}_i) + \rho \sum_i w_i (y_i - \bar{z}_i)$. Wierzbicki (1980) designed it so that its minimizer over the feasible set is always [Pareto optimal](/pareto-optimality/) (weakly for $\rho = 0$), whether $\bar{z}$ can be reached or not. If $\bar{z}$ can be reached, the answer is at least as good as $\bar{z}$; if not, the answer is a point of the front closest to $\bar{z}$. It is the engine of the [reference point method](/reference-point-method/).

## In plain words

You say what you hope for: "a price of 400 and a weight of 2 kilograms". You do not need to know whether such a choice exists.

The method looks for the choice that falls short of your hopes by the least amount, where the shortfall is the largest gap over all goals. If your hopes can be met, the gaps can be negative, and the method finds a choice that beats your hopes in every goal by as much as it can. If your hopes are too high, it finds the fair trade-off that comes closest to them.

The answer is always a fair trade-off. The sign of the best score tells you whether your hopes were realistic.

## When it applies

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, and $Y = f(X)$. The reference point $\bar{z} \in \mathbb{R}^p$ is any vector. The weights satisfy $w > 0$, and $\rho \ge 0$. The function is

$$s(y; \bar{z}, w, \rho) = \max_{i = 1, \ldots, p} w_i (y_i - \bar{z}_i) + \rho \sum_{i=1}^p w_i (y_i - \bar{z}_i),$$

and the subproblem is $\min_{x \in X} s(f(x); \bar{z}, w, \rho)$. It is the [weighted Tchebycheff method](/weighted-tchebycheff-method/) with the reference point moved from below the ideal point to any place in the space.

Use it when:

- the decision maker states aspiration levels, not weights, as in interactive methods;
- the reference point may be too optimistic or too pessimistic, and the method must still return a sensible Pareto optimal point;
- the front may be nonconvex.

**Monotonicity.** For $\rho = 0$ the function is weakly increasing: $y < y'$ gives $s(y) < s(y')$. For $\rho > 0$ it is strictly increasing: $y \prec y'$ gives $s(y) < s(y')$, because the maximum does not grow and the sum falls. So every minimizer is weakly Pareto optimal for $\rho = 0$, and Pareto optimal for $\rho > 0$ (see [scalarization](/scalarization/)). For $\rho > 0$ the optimum is also properly efficient, by the same argument as for the augmented Tchebycheff function.

**The sign tells attainability.** Let $\rho = 0$ and let $s^*$ be the optimal value.

1. $s(y) < 0$ exactly when $y < \bar{z}$, and $s(y) \le 0$ exactly when $y \leqq \bar{z}$.
2. So $s^* \le 0$ exactly when some $y \in Y$ satisfies $y \leqq \bar{z}$, that is, when $\bar{z}$ is attainable or dominated. In that case every optimal $\hat{y}$ satisfies $\hat{y} \leqq \bar{z}$.
3. If $s^* > 0$, no attainable point is as good as $\bar{z}$ in every objective.

*Proof.* Since $w > 0$, $\max_i w_i (y_i - \bar{z}_i) < 0$ exactly when every $y_i < \bar{z}_i$, and $\le 0$ exactly when every $y_i \le \bar{z}_i$. Parts 2 and 3 follow. $\square$

For $\rho > 0$, only one direction holds: if the max part of the optimum is $\le 0$, then $\hat{y} \leqq \bar{z}$. An attainable $\bar{z}$ can still have an optimum with a positive max part, when a large gain in the sum outweighs it.

**Every point can be reached.** Let $\hat{y} \in Y$ be weakly Pareto optimal, and set $\bar{z} = \hat{y}$ and $\rho = 0$. Then $s(\hat{y}) = 0$, and no $y \in Y$ has $s(y) < 0$, because that would mean $y < \hat{y}$. So $\hat{y}$ is optimal for any $w > 0$. If $\hat{y}$ is Pareto optimal, every optimum $y$ has $s(y) \le 0$, so $y \leqq \hat{y}$ and $y = \hat{y}$. For $\rho > 0$ and a finite $Y$, the same holds when $\rho$ is small enough, with the bound given on the [weighted Tchebycheff method](/weighted-tchebycheff-method/) page. For infinite $Y$ and $\rho > 0$, Wierzbicki (1986) studies when the reference points give a complete description of the properly efficient points.

**Geometry.** For $\rho = 0$, the level set $\{ y : s(y) = c \}$ is the boundary of the shifted cone $\bar{z} + c\, (1/w_1, \ldots, 1/w_p) - \mathbb{R}^p_{\ge}$. The minimizer is where the line $\bar{z} + t (1/w_1, \ldots, 1/w_p)$, for $t \in \mathbb{R}$ of either sign, leaves $Y + \mathbb{R}^p_{\ge}$. So the method projects $\bar{z}$ onto the front along a fixed direction, upward if $\bar{z}$ is too optimistic and downward if it is too pessimistic.

## The template

The subproblem becomes linear in the extra variable $t$, so a linear or integer program stays one.

```pseudo id=main
ACHIEVEMENT-PROJECTION(X, f, z̄, w, ρ)            ▷ w > 0, ρ ≥ 0
L1  solve  min t + ρ Σ_i w_i (f_i(x) − z̄_i)  subject to  w_i (f_i(x) − z̄_i) ≤ t for i = 1, ..., p,  x ∈ X
L2  (x̂, t*) ← an optimal solution
L3  if t* ≤ 0 then
L4      report that z̄ is attainable and f(x̂) ≦ z̄
L5  else
L6      report that f(x̂) misses z̄ by at most t*/w_i in objective i
L7  return x̂
```

At the optimum, $t^*$ equals the max part $\max_i w_i (f_i(\hat{x}) - \bar{z}_i)$, because $t$ is minimized and the sum does not depend on it. So line L4 is correct by the sign result, and line L6 holds because $w_i (f_i(\hat{x}) - \bar{z}_i) \le t^*$ for every $i$. For $\rho = 0$ add a second stage, as in the lexicographic [weighted Tchebycheff method](/weighted-tchebycheff-method/), if a weakly Pareto optimal answer is not enough.

**Cost.** One single-objective solve with one extra variable and $p$ extra constraints, per reference point.

### A worked example

Take $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$, with $w = (1, 1)$ and $\rho = 0$.

| reference point $\bar{z}$ | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ | optimum | meaning |
|---|---|---|---|---|---|---|---|---|---|
| $(4, 4)$ | 5 | 2 | 3 | **1** | 3 | 4 | 5 | $d$ | too optimistic: $d$ misses each aspiration by at most 1 |
| $(6, 2)$ | 7 | 4 | 5 | 2 | **1** | 3 | 3 | $e$ | too optimistic: $e$ misses by 1 |
| $(8, 8)$ | 1 | $-2$ | $-1$ | **$-3$** | $-1$ | 0 | 1 | $d$ | attainable: $d = (5, 4)$ beats it by 3 in the first objective and 4 in the second |

The second line reaches the unsupported point $e$, which no weighted sum finds.

A weak optimum: for $Y = \{(0, 2), (0, 1), (1, 0)\}$, $\bar{z} = (0, 5)$, $w = (1, 1)$ and $\rho = 0$, the values are $0, 0, 1$. Both $(0, 2)$ and $(0, 1)$ are optimal, and $(0, 2)$ is dominated. With $\rho = 0.1$ the values are $-0.3$, $-0.4$ and $0.6$, and the only optimum is $(0, 1)$.

## Classic examples

- **The [reference point method](/reference-point-method/).** In each round the decision maker gives $\bar{z}$, and one solve of the template gives a Pareto optimal point. The decision maker then moves $\bar{z}$.
- **Projection of a whole direction.** Moving $\bar{z}$ along a line and solving at each step gives a path of points on the front. Visual interactive methods use this to let the decision maker steer along the front.
- **Satisficing.** When $t^* \le 0$, the answer satisfies every aspiration, and the size of $-t^*$ shows how much room is left.

## Variations

- **Weights from the ranges.** A common choice is $w_i = 1 / (y^N_i - y^I_i)$ with the [nadir point](/nadir-point/) and the [ideal point](/ideal-point/), so that a gap of one range counts the same in each objective.
- **Separate aspiration and reservation levels.** Some versions take two points, what the decision maker hopes for and what they accept at worst, and use a piecewise linear function of each objective between them.
- **The plain Tchebycheff case.** With $\bar{z}$ below the ideal point, the function is the weighted Tchebycheff function, and the sign test always reports "not attainable".

## Pitfalls

- **Weak optima with $\rho = 0$.** The answer can be dominated, as in the example with $(0, 2)$. Use a small $\rho > 0$ or a second stage.
- **The sign test with $\rho > 0$.** A positive max part does not prove that $\bar{z}$ is unattainable when $\rho > 0$. Read the max part, not the whole value, and use $\rho = 0$ when the test matters.
- **Units.** Without good weights, one objective with large numbers controls the maximum. Normalize with the ideal and nadir points.
- **Too large $\rho$.** A large $\rho$ turns the function into a weighted sum, and the projection loses the unsupported points.

## Exercises

1. For the example points and $w = (1, 1)$, $\rho = 0$, find a reference point whose optimum is $b$ and is attainable. *Answer:* $\bar{z} = (3, 7)$: the values are $2, 0, 1, 2, 4, 5, 6$, and $b \leqq \bar{z}$.
2. Show that for $\rho = 0$ the optimal value is a continuous function of $\bar{z}$, with Lipschitz constant $\max_i w_i$ in the maximum norm. *Answer:* each term $w_i (y_i - \bar{z}_i)$ changes by at most $w_i \|\Delta\|_\infty$ when $\bar{z}$ moves by $\Delta$, and so do the maximum and the minimum over $Y$.
3. Give a two-point set where $\bar{z}$ is attainable but the optimum for $\rho = 1/2$ does not satisfy $\hat{y} \leqq \bar{z}$. *Answer:* $Y = \{(0, 0), (1, -10)\}$, $\bar{z} = (0, 0)$, $w = (1, 1)$: the values are $0$ and $1 + (1/2)(-9) = -3.5$.

## References
