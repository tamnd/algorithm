---
tag: NDY34M
kind: technique
slug: epsilon-constraint-method
name: Epsilon-constraint method
aliases:
- epsilon constraint
- constraint method
- ε-constraint method
- augmented epsilon-constraint method
area: optimization/multi-objective
level: core
summary: Optimizes one objective while bounding the others by epsilon constraints, tracing the Pareto front.
prereqs: [scalarization, pareto-optimality]
see_also: [weighted-sum-method, weighted-tchebycheff-method, nadir-point, pareto-front, constrained-shortest-path, lexicographic-optimization]
sources:
  - paper: doi:10.1109/TSMC.1971.4308298
    title: Y. Y. Haimes, L. S. Lasdon and D. A. Wismer, On a bicriterion formulation of the problems of integrated system identification and system optimization, IEEE Transactions on Systems, Man, and Cybernetics SMC-1(3), 1971
    locator: pages 296 to 297 (one objective is minimized and the other is bounded)
  - book: isbn:9780444007100
    title: Vira Chankong and Yacov Y. Haimes, Multiobjective Decision Making, Theory and Methodology, North-Holland, 1983
    locator: Chapter 4 (the epsilon-constraint approach and its relation to efficiency)
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 4 (the epsilon-constraint method, weak efficiency and the characterization of efficient solutions)
  - paper: doi:10.1016/j.amc.2009.03.037
    title: George Mavrotas, Effective implementation of the epsilon-constraint method in multi-objective mathematical programming problems, Applied Mathematics and Computation 213(2), 2009
    locator: pages 455 to 465 (the augmented epsilon-constraint method with slack terms, and the early exit from the grid of bounds)
---

The epsilon-constraint method finds points of the [Pareto front](/pareto-front/) by minimizing one objective $f_k$ while the others are bounded: $f_j(x) \le \varepsilon_j$ for $j \ne k$. Every optimum is weakly [Pareto optimal](/pareto-optimality/), and every Pareto optimal point is the optimum for the right bounds, with no convexity needed. For two objectives the bounds can be chosen one after the other, so that the method finds the whole finite front with one solve per point plus one.

## In plain words

Pick the goal you care about most, say the cost. Turn every other goal into a limit, like "the trip takes at most 5 hours". Then find the cheapest choice that keeps within the limits.

Each set of limits gives one fair trade-off. To see them all with two goals, start with no limit and find the cheapest choice. Then ask for a choice that is strictly faster than that one, and again take the cheapest. Repeat until no faster choice exists. You walk along the front one step at a time and never miss a point.

The catch is that a limit can make the problem much harder to solve than the plain cheapest choice.

## When it applies

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, $Y = f(X)$. For an index $k$ and bounds $\varepsilon \in \mathbb{R}^p$ (the entry $\varepsilon_k$ is not used), the subproblem is

$$P_k(\varepsilon) : \quad \min_{x \in X} f_k(x) \quad \text{subject to} \quad f_j(x) \le \varepsilon_j \ \text{ for all } j \ne k.$$

Use it when:

- the front may be nonconvex, as in integer and combinatorial problems;
- the solver accepts extra constraints, and the constraints do not make the subproblem too hard;
- one objective is the natural one to optimize and the others are natural limits, such as a cost with a bound on the risk;
- there are two objectives and the whole front is wanted, since the bounds can then be set from the previous answer.

**Every optimum is weakly Pareto optimal.** Let $\hat{x}$ be optimal for $P_k(\varepsilon)$. Then $\hat{x}$ is weakly Pareto optimal. If $f(\hat{x})$ is the only optimal image, $\hat{x}$ is Pareto optimal.

*Proof.* If $f(x) < f(\hat{x})$, then $f_j(x) < f_j(\hat{x}) \le \varepsilon_j$ for $j \ne k$, so $x$ is feasible, and $f_k(x) < f_k(\hat{x})$, a contradiction. If $f(x) \prec f(\hat{x})$, then $x$ is feasible and $f_k(x) \le f_k(\hat{x})$, so $x$ is also optimal, with a different image. $\square$

The optimum can be dominated. For $Y = \{(0, 2), (0, 1), (1, 0)\}$, $k = 1$ and $\varepsilon_2 = 2$, the points $(0, 2)$ and $(0, 1)$ are both optimal, and $(0, 1)$ dominates $(0, 2)$.

**Every Pareto optimal point is found.** Let $\hat{x} \in X$ and $\hat{\varepsilon}_j = f_j(\hat{x})$ for all $j$. Then $\hat{x}$ is Pareto optimal if and only if $\hat{x}$ is optimal for $P_k(\hat{\varepsilon})$ for every $k = 1, \ldots, p$. Moreover, if $\hat{x}$ is Pareto optimal, then for each $k$ every optimal solution of $P_k(\hat{\varepsilon})$ has the image $f(\hat{x})$.

*Proof.* Let $\hat{x}$ be Pareto optimal and fix $k$. The point $\hat{x}$ is feasible for $P_k(\hat{\varepsilon})$. If $x$ is feasible with $f_k(x) \le f_k(\hat{x})$, then $f(x) \leqq f(\hat{x})$, so $f(x) = f(\hat{x})$ because $\hat{x}$ is Pareto optimal. So $\hat{x}$ is optimal, and every optimum has the image $f(\hat{x})$. Conversely, let $\hat{x}$ be optimal for every $P_k(\hat{\varepsilon})$. If $f(x) \prec f(\hat{x})$, choose $k$ with $f_k(x) < f_k(\hat{x})$. Then $x$ is feasible for $P_k(\hat{\varepsilon})$ with a smaller value, a contradiction. $\square$

So one $k$ and the bounds $\varepsilon = f(\hat{x})$ already give $\hat{x}$, convex or not. This is the main advantage over the [weighted sum method](/weighted-sum-method/).

**Useful bounds.** Bounds below the [ideal point](/ideal-point/) make the subproblem infeasible, and bounds above the [nadir point](/nadir-point/) are not active on the front. So it is enough to take $\varepsilon_j \in [y^I_j, y^N_j]$.

## The template

For $p = 2$ the method can walk along the front. Each step asks for the lexicographic minimum of $(f_1, f_2)$ among the points that are strictly better in $f_2$ than the last point found.

```pseudo id=main
EPSILON-CONSTRAINT-FRONT(X, f)                    ▷ p = 2, Y_N finite
L1  S ← ∅; ε ← +∞
L2  loop
L3      solve  lexmin (f_1(x), f_2(x))  over  {x ∈ X : f_2(x) < ε}
L4      if the problem is infeasible then return S
L5      x̂ ← an optimal solution; S ← S ∪ {x̂}
L6      ε ← f_2(x̂)
```

For integer objectives the strict bound of line L3 is the constraint $f_2(x) \le \varepsilon - 1$. The lexicographic minimum is two solves: minimize $f_1$, then minimize $f_2$ with $f_1$ fixed at its optimum. It can also be one solve of $f_1 + \delta f_2$ for a small enough $\delta > 0$.

**Correctness.** Each point found is Pareto optimal: if $y \prec \hat{y} = f(\hat{x})$, then $y_2 \le \hat{y}_2 < \varepsilon$, so $y$ is feasible in line L3, and it is lexicographically smaller than $\hat{y}$, a contradiction. Each nondominated point is found: let $y^* \in Y_N$ with $y^*_2 < \varepsilon$ and let $\hat{y}$ be the point found. Then $\hat{y}_1 \le y^*_1$. If $\hat{y}_1 = y^*_1$, the lexicographic order gives $\hat{y}_2 \le y^*_2$, so $\hat{y} \leqq y^*$ and $\hat{y} = y^*$. Otherwise $\hat{y}_1 < y^*_1$, and since both are nondominated, $y^*_2 < \hat{y}_2$, so $y^*$ is still feasible in the next round. The bound falls strictly in each round, and the rounds stop when no point is left.

**Cost.** One lexicographic solve per nondominated point and one more that is infeasible: $|Y_N| + 1$ lexicographic solves. For $p \ge 3$ the method needs a grid of bounds in $p - 1$ dimensions, and the number of solves grows with the grid. Different bounds often give the same point, and some give infeasible problems.

### A worked example

Take $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$.

| round | $\varepsilon$ | feasible points | lexicographic minimum | new $\varepsilon$ |
|---|---|---|---|---|
| 1 | $+\infty$ | all | $a = (2, 9)$ | 9 |
| 2 | 9 | $b, c, d, e, f, g$ | $b = (3, 6)$ | 6 |
| 3 | 6 | $d, e, f, g$ | $d = (5, 4)$ | 4 |
| 4 | 4 | $e, g$ | $e = (7, 3)$ | 3 |
| 5 | 3 | $g$ | $g = (9, 1)$ | 1 |
| 6 | 1 | none | infeasible | |

The method finds the whole front $\{a, b, d, e, g\}$ with $6 = 5 + 1$ solves, including the unsupported point $e$. The dominated points $c$ and $f$ are feasible in some rounds, but they never win. With fixed bounds and $k = 1$, the subproblem $\min y_1$ subject to $y_2 \le \varepsilon$ returns $a$ for $\varepsilon = 9$, $b$ for $\varepsilon \in \{6, 7, 8\}$, $d$ for $\varepsilon \in \{4, 5\}$, $e$ for $\varepsilon = 3$, $g$ for $\varepsilon \in \{1, 2\}$, and nothing for $\varepsilon = 0$.

## Classic examples

- **Haimes, Lasdon and Wismer (1971)** introduced the bicriterion form, with one objective minimized and the other bounded.
- **Bicriteria integer programs.** The walk of the template is the standard exact method for two objectives when a good integer solver is at hand. It finds all nondominated points, supported or not.
- **Risk and cost.** In portfolio and engineering problems, a cost is minimized subject to a bound on the risk, and the bound is varied to show the trade-off.
- **[Constrained shortest path](/constrained-shortest-path/).** The subproblem of the [multi-objective shortest path](/multi-objective-shortest-path/) with one bounded cost is the constrained shortest path problem, which is [NP-hard](/np-hard/), while the plain shortest path is easy.

## Variations

- **The augmented epsilon-constraint method.** Mavrotas (2009) turns the bounds into equations with slack variables $s_j \ge 0$, $f_j(x) + s_j = \varepsilon_j$, and adds a small reward $\delta \sum_j s_j / r_j$ to the objective, where $r_j$ is the range of objective $j$. The optimum is then Pareto optimal, not only weakly, in one solve. When a bound makes the problem infeasible, all tighter bounds in the same row of the grid are infeasible too, and they are skipped.
- **Elastic bounds.** The bounds may be broken at a penalty. This avoids infeasible subproblems and keeps the structure of some combinatorial problems.
- **A grid for $p \ge 3$.** Divide each range $[y^I_j, y^N_j]$, $j \ne k$, into steps and solve one problem per cell. Smaller steps find more points at a higher cost. Exact methods for three objectives split the search region into boxes and remove the box of each new point.

## Pitfalls

- **Weak optima.** A solver may return a weakly Pareto optimal point that is dominated, as in the example with $(0, 2)$. Use the lexicographic form of line L3, the augmented form, or a second stage.
- **Hard subproblems.** A bound on a second objective can turn a polynomial problem into an NP-hard one, as for shortest paths and spanning trees. A weighted sum keeps the structure, a bound does not.
- **The choice of bounds.** Bounds outside $[y^I_j, y^N_j]$ waste solves. For $p \ge 3$ the [nadir point](/nadir-point/) is itself hard to compute, so the grid may cover the wrong region.
- **Repeated points.** On a coarse grid, many bounds return the same point. On a fine grid, many solves are wasted. The walk of the template avoids both, but only for $p = 2$.
- **Floating point bounds.** The strict bound $f_2(x) < \varepsilon$ must be implemented as $f_2(x) \le \varepsilon - \delta$. A $\delta$ that is too large skips points; one that is too small finds the same point again.

## Exercises

1. Let $p = 2$ and let $Y$ be compact. Show that $P_1(\varepsilon)$ is infeasible when $\varepsilon_2 < y^I_2$, and that its optimal value is $y^I_1$ when $\varepsilon_2 \ge y^N_2$. *Answer:* no point has $y_2 < y^I_2$. The lexicographic minimizer of $(f_1, f_2)$ has the second entry $y^N_2$, so it is feasible when $\varepsilon_2 \ge y^N_2$, and its first entry is $y^I_1$.
2. For the example points, find all bounds $\varepsilon$ such that $\min y_2$ subject to $y_1 \le \varepsilon$ returns $d$. *Answer:* $5 \le \varepsilon < 7$.
3. Show that the walk of the template, run on a set where several points have the same $f_1$ value, never returns a dominated point, but that a version which only minimizes $f_1$ in line L3 can. *Answer:* for $\{(0, 2), (0, 1)\}$, the first solve of the plain version may return $(0, 2)$.

## References
