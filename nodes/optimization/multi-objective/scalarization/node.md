---
tag: YDZF9D
kind: technique
slug: scalarization
name: Scalarization
aliases:
- scalarizing function
- aggregation of objectives
- scalarization method
area: optimization/multi-objective
level: intro
summary: Reduces several objectives to one real-valued function so single-objective methods apply. Monotone functions give Pareto optimal answers, and a sweep of the parameters traces the front.
prereqs: [pareto-optimality, multi-objective-optimization]
see_also: [weighted-sum-method, weighted-tchebycheff-method, epsilon-constraint-method, achievement-scalarizing-function, goal-programming, lexicographic-optimization, normal-boundary-intersection, utility-function]
sources:
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 3 (the weighted sum method) and Chapter 4 (the epsilon-constraint method, compromise solutions and the Tchebycheff norm, achievement functions)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part II, Chapters 2 to 4 (the weighting method, the epsilon-constraint method, the weighted metrics and the achievement scalarizing functions)
  - paper: doi:10.1007/978-3-642-48782-8_32
    title: Andrzej P. Wierzbicki, The use of reference objectives in multiobjective optimization, in Multiple Criteria Decision Making Theory and Application, Lecture Notes in Economics and Mathematical Systems 177, Springer, 1980
    locator: pages 468 to 486 (order-representing and order-approximating achievement functions)
  - paper: doi:10.1016/0022-247X(68)90201-1
    title: Arthur M. Geoffrion, Proper efficiency and the theory of vector maximization, Journal of Mathematical Analysis and Applications 22(3), 1968
    locator: pages 618 to 630 (weighted sums with positive weights and proper efficiency)
---

Scalarization turns a [multi-objective optimization](/multi-objective-optimization/) problem into a single-objective one: it chooses a function $s : \mathbb{R}^p \to \mathbb{R}$ and minimizes $s(f(x))$ over the feasible set. Each choice of the parameters of $s$ gives one point. If $s$ is monotone in the right sense, that point is [Pareto optimal](/pareto-optimality/), and if the family of functions is rich enough, every Pareto optimal point is the optimum for some parameter. So a sweep over the parameters traces the [Pareto front](/pareto-front/) with any single-objective solver.

## In plain words

You cannot ask a solver to make several numbers small at once. A solver wants one number. So you invent a rule that turns each choice into one score, and you ask the solver for the choice with the best score.

The simplest rule adds the numbers with weights. Other rules look only at the worst number, or keep one number and turn the others into limits, like "cost below 100".

A good rule never gives a better score to a choice that is worse on every count. Then the winner is always a fair trade-off.

To see many fair trade-offs, run the solver many times with different weights or limits. Some rules can reach every fair trade-off. The weighted sum cannot reach the ones in the dents of the front.

## When it applies

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, $Y = f(X)$, $y^I$ is the [ideal point](/ideal-point/), and $y \leqq y'$, $y \prec y'$ and $y < y'$ mean componentwise $\le$, dominance and componentwise $<$.

Use scalarization when:

- a good solver exists for the single-objective version, such as a [linear programming](/linear-programming-problem/) or integer programming code, and you want to reuse it;
- the decision maker gives weights, goals or a reference point, so that one solve answers the question (an a priori or interactive method; see [preference articulation](/preference-articulation/));
- you want a set of exact Pareto optimal points with a guarantee, not an approximation from an evolutionary method such as [NSGA-II](/nsga-ii/).

Each subproblem has the same constraints as the original problem, plus at most $p$ new constraints or variables. For a combinatorial problem, a weighted sum keeps the structure (a shortest path stays a shortest path), but a constraint $f_j(x) \le \varepsilon_j$ can make it [NP-hard](/np-hard/), as for the [constrained shortest path](/constrained-shortest-path/).

## The template

The input is the problem $(X, f)$, a family of scalarizing functions $s(\cdot\,; \theta)$ and a finite list $\Theta$ of parameters. The output is a set of Pareto optimal solutions.

```pseudo id=main
SCALARIZATION-SWEEP(X, f, s, Θ)
L1  S ← ∅
L2  for each parameter θ in Θ do
L3      x ← a minimizer of s(f(x); θ) over X                   ▷ one single-objective solve
L4      if s(·; θ) is only weakly increasing then
L5          x ← a minimizer of f_1 + ... + f_p over {x' ∈ X : f(x') ≦ f(x)}   ▷ the cleanup solve
L6      S ← S ∪ {x}
L7  return S
```

The holes are the function $s$ in line L3 and the parameter list in line L2. The next two results decide whether line L5 is needed and whether a sweep can reach every point.

**Monotone functions give Pareto optimal points.** Call $s$ *strictly increasing* when $y \prec y'$ implies $s(y) < s(y')$, and *weakly increasing* when $y < y'$ implies $s(y) < s(y')$.

1. If $s$ is strictly increasing on $Y$, each minimizer of $s \circ f$ over $X$ is Pareto optimal.
2. If $s$ is weakly increasing on $Y$, each minimizer is weakly Pareto optimal.
3. If $s$ is weakly increasing and also satisfies $y \leqq y' \Rightarrow s(y) \le s(y')$, a minimizer whose image is the only optimal image is Pareto optimal.

*Proof.* For 1: if $f(x') \prec f(\hat{x})$, then $s(f(x')) < s(f(\hat{x}))$, so $\hat{x}$ is not a minimizer. For 2, the same with $f(x') < f(\hat{x})$. For 3: if $f(x') \prec f(\hat{x})$, then $s(f(x')) \le s(f(\hat{x}))$, so $x'$ is also a minimizer, with a different image. $\square$

**The cleanup solve.** Let $\hat{x}$ be any feasible point and let $x^*$ minimize $\sum_i f_i$ over $\{x \in X : f(x) \leqq f(\hat{x})\}$. Then $x^*$ is Pareto optimal and $f(x^*) \leqq f(\hat{x})$.

*Proof.* If $f(x') \prec f(x^*)$, then $f(x') \leqq f(x^*) \leqq f(\hat{x})$, so $x'$ is feasible for the cleanup problem, and $\sum_i f_i(x') < \sum_i f_i(x^*)$, which is a contradiction. $\square$

So line L5 replaces a weakly Pareto optimal point with a Pareto optimal point that is at least as good in every objective. It costs one more solve per parameter.

**Which family reaches every point.** A family is *complete* when each Pareto optimal $\hat{x}$ minimizes $s(\cdot\,; \theta)$ for some $\theta$. The table lists the main families, with the theorems proved on their pages.

| method | $s(y; \theta)$ | monotone | complete |
|---|---|---|---|
| [weighted sum](/weighted-sum-method/) | $\sum_i \lambda_i y_i$, $\lambda > 0$ | strictly | only for supported points |
| [weighted Tchebycheff](/weighted-tchebycheff-method/) | $\max_i w_i (y_i - z_i)$, $w > 0$, $z < y^I$ | weakly | yes |
| augmented Tchebycheff | the same plus $\rho \sum_i (y_i - z_i)$, $\rho > 0$ | strictly | properly Pareto optimal points; all points of a finite $Y$ for small $\rho$ |
| [epsilon-constraint](/epsilon-constraint-method/) | $y_k$ if $y_j \le \varepsilon_j$ for $j \ne k$, else $+\infty$ | weakly | yes |
| [achievement function](/achievement-scalarizing-function/) | $\max_i w_i (y_i - \bar{z}_i) + \rho \sum_i w_i (y_i - \bar{z}_i)$ | strictly if $\rho > 0$ | yes for $\rho = 0$, with $\bar{z} = \hat{y}$ |
| [goal programming](/goal-programming/) | $\sum_i w_i \max(0, y_i - g_i)$ | not monotone in general | no |
| [lexicographic](/lexicographic-optimization/) | the order of $(y_{\pi(1)}, \ldots, y_{\pi(p)})$ | strictly | no: at most $p!$ points |

A strictly increasing family can still reach unsupported points: the augmented Tchebycheff function does. The weighted sum misses them because it is linear, not because it is strictly increasing.

**Cost.** One sweep with $|\Theta|$ parameters costs $|\Theta|$ single-objective solves, and up to $2|\Theta|$ with line L5. Different parameters can return the same point, so $|S| \le |\Theta|$. For two objectives the [epsilon-constraint method](/epsilon-constraint-method/) can choose each bound from the previous answer and so finds the whole finite front with $|Y_N| + 1$ solves.

### A worked example

Take the seven images $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$. The front is $\{a, b, d, e, g\}$, and $e$ is unsupported: the segment from $d$ to $g$ passes through $(7, 2.5)$, below $e$.

| method and parameter | values | optimum |
|---|---|---|
| weighted sum, $\lambda = (1/2, 1/2)$ | $a{:}\ 5.5$, $b{:}\ 4.5$, $d{:}\ 4.5$, $e{:}\ 5$, $g{:}\ 5$ | $b$ and $d$ |
| weighted sum, $\lambda = (1/3, 2/3)$ | $a{:}\ 20/3$, $b{:}\ 5$, $d{:}\ 13/3$, $e{:}\ 13/3$, $g{:}\ 11/3$ | $g$ |
| Tchebycheff, $z = (1, 0)$, $w = (1/6, 1/3)$ | $a{:}\ 3$, $b{:}\ 2$, $d{:}\ 4/3$, $e{:}\ 1$, $g{:}\ 4/3$ | $e$ |
| epsilon-constraint, $\min y_1$ with $y_2 \le 3$ | feasible: $e{:}\ 7$, $g{:}\ 9$ | $e$ |
| achievement, $\bar{z} = (6, 2)$, $w = (1, 1)$ | $a{:}\ 7$, $b{:}\ 4$, $d{:}\ 2$, $e{:}\ 1$, $g{:}\ 3$ | $e$ |
| lexicographic, $y_2$ first | $g$ has the least $y_2$ | $g$ |

The dominated points $c$ and $f$ never win, as the monotonicity results require. The point $e$ is reached by the Tchebycheff, epsilon-constraint and achievement functions. No weighted sum with $\lambda = (t, 1 - t)$, $0 \le t \le 1$, reaches it. The value of $e$ is $3 + 4t$, the value of $d$ is $4 + t$ and the value of $g$ is $1 + 8t$. So $e$ is better than $d$ only when $t < 1/3$, and better than $g$ only when $t > 1/2$, and never both.

## Classic examples

- **The [weighted sum method](/weighted-sum-method/).** The oldest scalarization. Geoffrion (1968) proved that for convex problems its optima with positive weights are exactly the properly Pareto optimal points.
- **The [epsilon-constraint method](/epsilon-constraint-method/).** Keep one objective and bound the others (Haimes, Lasdon and Wismer, 1971). It is complete for any problem, convex or not.
- **The [weighted Tchebycheff method](/weighted-tchebycheff-method/).** Minimize the weighted largest distance to a utopia point. It is complete, and the augmented form removes the weakly Pareto optimal answers.
- **The [achievement scalarizing function](/achievement-scalarizing-function/) and the [reference point method](/reference-point-method/).** Wierzbicki (1980) designed these functions so that a reference point, attainable or not, is projected onto the front.
- **[Normal boundary intersection](/normal-boundary-intersection/).** It maximizes the distance along a fixed direction from the hull of the individual minima, to get evenly spread points.
- **[MOEA/D](/moea-d/).** An evolutionary method that solves many Tchebycheff or weighted sum subproblems at once, one per weight vector.

## Variations

- **Exact sweeps for two objectives.** For $p = 2$ the parameters need not be fixed in advance. The weighted sum can find all extreme supported points by bisection on the weights (the dichotomic method), and the epsilon-constraint method can step from one front point to the next.
- **Normalization.** Most functions depend on the units of the objectives. Dividing each objective by the range $y^N_i - y^I_i$, with the [nadir point](/nadir-point/), makes equal weights mean equal importance.
- **Two-stage instead of augmented.** Line L5 of the template is the two-stage form. The augmented form adds a small multiple of $\sum_i y_i$ to $s$ and needs only one solve, but a too small $\rho$ causes numerical trouble and a too large $\rho$ hides some points.
- **The hybrid method.** Minimize a weighted sum with positive weights subject to bounds $f_j(x) \le \varepsilon_j$ on all objectives. Line L5 is the special case with all weights 1 and $\varepsilon = f(x)$. Every optimum is Pareto optimal, because the objective is strictly increasing and a point that dominates a feasible point is also feasible.

## Pitfalls

- **Weak optima.** The Tchebycheff, epsilon-constraint and plain achievement functions can return weakly Pareto optimal points that are dominated. A solver returns any optimum, not the best one. Use line L5 or the augmented form.
- **Missing points with the weighted sum.** On a nonconvex front, no weights reach the unsupported points, however fine the sweep. In the example, $e$ is never found.
- **Uneven spread.** Evenly spaced weights do not give evenly spaced points. A whole interval of weights can return one vertex, and a small change of weights can jump over a long part of the front.
- **Hard subproblems.** Bounds on objectives can destroy structure that the solver needs. A shortest path with a bound on a second cost is NP-hard, while a weighted sum of two costs is still a shortest path.
- **Infeasible subproblems.** In the epsilon-constraint method, bounds below the ideal point make the subproblem infeasible. Choose bounds inside $[y^I_j, y^N_j]$.
- **Goals that are too easy.** In goal programming, a point that meets every goal has the value zero, even when another point is better in every objective. Set the goals at or below the ideal point, or add a second stage.

## Exercises

1. Show that the weighted sum $\sum_i \lambda_i y_i$ with $\lambda \geqq 0$, $\lambda \ne 0$ is weakly increasing, and give a set $Y$ and such a $\lambda$ with a minimizer that is not Pareto optimal. *Answer:* if $y < y'$, then $\lambda^\top y < \lambda^\top y'$ because some $\lambda_i > 0$. For $Y = \{(0, 0), (0, 1)\}$ and $\lambda = (1, 0)$, both points are minimizers, and $(0, 1)$ is dominated.
2. Prove that when $\hat{x}$ is already Pareto optimal, the cleanup solve of line L5 returns a point with the image $f(\hat{x})$. *Answer:* a feasible point of the cleanup problem with an image other than $f(\hat{x})$ would dominate $\hat{x}$, so every feasible point has the image $f(\hat{x})$.
3. For the example set, find all $\varepsilon$ such that $\min y_1$ subject to $y_2 \le \varepsilon$ returns $d$. *Answer:* $4 \le \varepsilon < 6$.

## References
