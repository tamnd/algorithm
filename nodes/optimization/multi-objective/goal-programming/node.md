---
tag: VDX8ND
kind: technique
slug: goal-programming
name: Goal programming
aliases:
- goal programming method
- weighted goal programming
- preemptive goal programming
- lexicographic goal programming
area: optimization/multi-objective
level: intro
summary: Minimizes deviations from target goal levels set by the decision maker. The answer can be dominated when the goals are easy, and a second stage restores Pareto optimality.
prereqs: [scalarization, linear-programming-problem]
see_also: [lexicographic-optimization, weighted-sum-method, achievement-scalarizing-function, preference-articulation, utility-function]
sources:
  - paper: doi:10.1287/mnsc.1.2.138
    title: A. Charnes, W. W. Cooper and R. O. Ferguson, Optimal estimation of executive compensation by linear programming, Management Science 1(2), 1955
    locator: pages 138 to 151 (minimization of the absolute deviations from goals by a linear program, the origin of goal programming)
  - paper: doi:10.1016/S0377-2217(97)00317-2
    title: Mehrdad Tamiz, Dylan Jones and Carlos Romero, Goal programming for decision making, An overview of the current state-of-the-art, European Journal of Operational Research 111(3), 1998
    locator: pages 569 to 581 (weighted, lexicographic and minmax variants, and Pareto efficiency of the solutions)
  - book: isbn:9781441957702
    title: Dylan Jones and Mehrdad Tamiz, Practical Goal Programming, Springer, 2010
    locator: the chapters on the variants of goal programming and on the restoration of Pareto efficiency
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part II, Chapter 4 (a priori methods, goal programming)
---

Goal programming solves a [multi-objective optimization](/multi-objective-optimization/) problem by asking the decision maker for a goal $g_i$ for each objective and then minimizing a weighted sum of the deviations from the goals. It goes back to Charnes, Cooper and Ferguson (1955), and it stays a [linear program](/linear-programming-problem/) when the objectives and constraints are linear. It is popular because goals are easy to state. Its weak point is that a point that meets every goal scores zero, even if another point is better in every objective, so the answer need not be [Pareto optimal](/pareto-optimality/) unless the goals are ambitious or a second stage is added.

## In plain words

Say what you are aiming for in each goal: "cost at most 400, delivery in at most 3 days". The method then looks for a choice that misses these targets by as little as possible. Missing a target by a lot is worse than missing it by a little, and you can say which misses hurt more.

If no choice meets all targets, the method finds a good compromise. But if some choices meet all targets, the method is happy with any of them, even a poor one that another choice beats on every count. So after the first step, ask for the best choice among those that are at least as good as the answer.

## When it applies

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, $Y = f(X)$, and $y^I$ is the [ideal point](/ideal-point/). The goals are $g \in \mathbb{R}^p$, and the weights $u > 0$.

For a minimized objective, only a value above the goal is a miss. The deviation variable $d_i^+ \ge 0$ measures it, with $f_i(x) - d_i^+ \le g_i$. The weighted goal program is

$$\min_{x \in X,\ d^+ \geqq 0} \ \sum_{i=1}^p u_i d_i^+ \quad \text{subject to} \quad f_i(x) - d_i^+ \le g_i, \quad i = 1, \ldots, p.$$

At an optimum $d_i^+ = \max(0, f_i(x) - g_i)$, so the problem is $\min_{x \in X} \sum_i u_i \max(0, f_i(x) - g_i)$.

Use it when:

- the decision maker thinks in targets, such as budgets or deadlines, and can state them before the search (an a priori method; see [preference articulation](/preference-articulation/));
- the problem is linear and must stay linear;
- it is enough to reach the goals, and the quality beyond the goals does not matter.

**Ambitious goals give Pareto optimal points.** Let $g \leqq y^I$ and $u > 0$. Then every optimal solution of the weighted goal program is Pareto optimal.

*Proof.* For every $x$, $f_i(x) \ge y^I_i \ge g_i$, so $\max(0, f_i(x) - g_i) = f_i(x) - g_i$. The objective is $\sum_i u_i f_i(x) - \sum_i u_i g_i$, a weighted sum with positive weights plus a constant. Its optima are Pareto optimal by the theorem of the [weighted sum method](/weighted-sum-method/). $\square$

**Easy goals can give dominated points.** If some $x$ meets all goals, $f(x) \leqq g$, then the optimal value is 0, and every point that meets all goals is optimal, including points that are dominated, and even points that are not weakly Pareto optimal.

**But some optimum is Pareto optimal.** The function $\phi(y) = \sum_i u_i \max(0, y_i - g_i)$ satisfies $y \leqq y' \Rightarrow \phi(y) \le \phi(y')$. Let $x^\circ$ be optimal, and let $\hat{x}$ minimize $\sum_i f_i(x)$ over $\{x \in X : f(x) \leqq f(x^\circ)\}$. Then $\hat{x}$ is Pareto optimal (the cleanup lemma of [scalarization](/scalarization/)), and $\phi(f(\hat{x})) \le \phi(f(x^\circ))$, so $\hat{x}$ is also optimal for the goal program.

## The template

```pseudo id=main
GOAL-PROGRAMMING(X, f, g, u)                       ▷ u > 0
L1  solve  min Σ_i u_i d_i^+  subject to  f_i(x) − d_i^+ ≤ g_i,  d_i^+ ≥ 0,  i = 1, ..., p,  x ∈ X
L2  x° ← an optimal solution
L3  solve  min Σ_i f_i(x)  subject to  f_i(x) ≤ f_i(x°),  i = 1, ..., p,  x ∈ X     ▷ restore Pareto optimality
L4  x̂ ← an optimal solution
L5  return x̂
```

By the result above, $\hat{x}$ is Pareto optimal and is still optimal for the goal program of line L1. The second stage is skipped in many applications, which is the main source of dominated answers in practice.

**Cost.** Two single-objective solves. For a linear problem, line L1 adds $p$ variables and $p$ constraints, and line L3 adds $p$ constraints.

### A worked example

Take $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$, with the weights $u = (1, 1)$ unless stated.

| goals | values at $a, b, c, d, e, f, g$ | optima of line L1 | after line L3 |
|---|---|---|---|
| $(4, 5)$ | $4, 1, 2, 1, 3, 4, 5$ | $b$, $d$ | $b$, $d$ |
| $(8, 7)$ | $2, 0, 0, 0, 0, 0, 1$ | $b, c, d, e, f$ | from $c$: $b$; from $f$: $d$ |
| $(2, 1)$, $u = (1, 2)$ | $16, 11, 14, 9, 9, 14, 7$ | $g$ | $g$ |

With the goals $(8, 7)$, the dominated points $c$ and $f$ are optimal for line L1, and $f = (8, 5)$ is not even weakly Pareto optimal: $d = (5, 4)$ is better in both objectives. Line L3 starting from $f$ looks at $d$, $e$ and $f$, the points at least as good as $f$, and picks $d$ with the least sum 9. With the goals at the ideal point and $u = (1, 2)$, the values are $y_1 + 2 y_2 - 4$, the weighted sum shifted by a constant.

## Classic examples

- **Charnes, Cooper and Ferguson (1955)** estimated executive pay by a linear program that minimizes the sum of absolute deviations from target values. The name goal programming came later, with Charnes and Cooper.
- **Production and workforce planning.** Goals for output, overtime and cost, with weights or priorities, in one linear program.
- **[Lexicographic optimization](/lexicographic-optimization/) of goals.** Preemptive goal programming puts the goals into priority levels and minimizes the deviations of level 1 first, then of level 2 with level 1 fixed, and so on.

## Variations

- **Two-sided goals.** For a target value, not a bound, both $d_i^+$ and $d_i^-$ are penalized, with $f_i(x) - d_i^+ + d_i^- = g_i$. The method then prefers values close to $g_i$ from both sides. This is a different preference, not a minimization of $f_i$. The function is not monotone, so the answer of line L1 can be dominated, and line L3 can return a point that is no longer optimal for the goal program.
- **Preemptive (lexicographic) goal programming.** Priority levels $P_1 \gg P_2 \gg \cdots$ replace the weights between levels. It is the [lexicographic optimization](/lexicographic-optimization/) of the deviation sums.
- **Minmax (Chebyshev) goal programming.** Minimize $\max_i u_i d_i^+$. This is the [achievement scalarizing function](/achievement-scalarizing-function/) with the reference point $g$ and $\rho = 0$, except that misses below zero are cut to zero.
- **Normalized deviations.** Divide $d_i^+$ by $g_i$ or by the range of objective $i$, so that misses in different units can be added.

## Pitfalls

- **Dominated answers.** With goals that can be met, line L1 alone can return a point that is worse in every objective than another feasible point. Always run line L3, or set the goals at or below the ideal point.
- **Units.** The sum adds misses in different units. Without normalization, the objective with the largest numbers controls the answer.
- **Weights versus priorities.** Preemptive priorities and weights give different answers, and very large weights used to imitate priorities cause numerical trouble.
- **Goals beyond the front.** Very ambitious goals make the method a weighted sum, which cannot reach unsupported points.

## Exercises

1. For the example points with goals $(4, 5)$, find weights $u > 0$ for which only $d$ is optimal. *Answer:* $u = (1, 2)$: the values are $8, 2, 4, 1, 3, 4, 5$.
2. Prove that the set of optimal solutions of line L1 is the set of $x$ with $f(x) \leqq g$ when this set is not empty.
3. Show that with goals at or below the ideal point, the minmax goal program is the [weighted Tchebycheff method](/weighted-tchebycheff-method/) with the reference point $g$.

## References
