---
tag: QJW02J
kind: algorithm
slug: normal-boundary-intersection
name: Normal boundary intersection
aliases:
- NBI method
- Das-Dennis normal boundary intersection
- NBI
area: optimization/multi-objective
level: advanced
summary: Generates evenly spread Pareto points by intersecting the feasible boundary with normals to the convex hull of individual minima.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {M: "the number of weight vectors, which is binom(H + p - 1, p - 1) for the grid with step 1/H", L: the cost of one single-objective subproblem, p: the number of objectives}
  time: {worst: O((M + p) L)}
  space: {extra: O(p^2)}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1998
  people: [Indraneel Das, John E. Dennis]
  note: Das and Dennis showed in 1997 that an even spread of weights in the weighted sum method gives an uneven spread of points and misses nonconvex parts of the front, and proposed normal boundary intersection in 1998 as a remedy.
prereqs: [pareto-front, ideal-point, scalarization, convex-hull]
see_also: [weighted-sum-method, epsilon-constraint-method, achievement-scalarizing-function, weighted-tchebycheff-method, nsga-iii, benson-algorithm, multi-objective-linear-programming, reference-point-method]
sources:
  - paper: doi:10.1137/S1052623496307510
    title: Indraneel Das and J. E. Dennis, Normal-boundary intersection, A new method for generating the Pareto surface in nonlinear multicriteria optimization problems, SIAM Journal on Optimization 8(3), 1998
    locator: pages 631 to 657 (the convex hull of individual minima, the NBI subproblem, the quasi-normal direction, and the remark that NBI points need not be Pareto optimal)
  - paper: doi:10.1007/BF01197559
    title: I. Das and J. E. Dennis, A closer look at drawbacks of minimizing weighted sums of objectives for Pareto set generation in multicriteria optimization problems, Structural Optimization 14(1), 1997
    locator: pages 63 to 69 (an even spread of weights does not give an even spread of points)
  - paper: doi:10.1007/s00158-002-0276-1
    title: A. Messac, A. Ismail-Yahaya and C. A. Mattson, The normalized normal constraint method for generating the Pareto frontier, Structural and Multidisciplinary Optimization 25(2), 2003
    locator: pages 86 to 98 (a variant with inequality constraints on a normalized plane)
  - paper: doi:10.1007/BF00934564
    title: A. Pascoletti and P. Serafini, Scalarizing vector optimization problems, Journal of Optimization Theory and Applications 42(4), 1984
    locator: pages 499 to 524 (the scalarization along a direction from a reference point)
---

Normal boundary intersection (NBI) computes a set of points spread over the [Pareto front](/pareto-front/) by solving one single-objective subproblem per point. It finds the minimizer of each objective, takes the simplex spanned by their images, called the convex hull of individual minima (CHIM), places base points on a regular grid of this simplex, and from each base point moves in a fixed direction toward the [ideal point](/ideal-point/) as far as the feasible image allows. Das and Dennis (1998) designed it so that an even grid on the CHIM gives a more even spread of points than the [weighted sum method](/weighted-sum-method/), and so that it reaches nonconvex parts of the front. The price is that for three or more objectives a point found by NBI can be dominated, so the output must be checked.

## In plain words

You want a fair picture of all the best trade-offs, not a crowd of points in one corner. First, find the best plan for each goal alone. Draw the flat surface through their results: a line for two goals, a triangle for three. Put evenly spaced marks on it.

From each mark, walk straight toward the corner where every goal is at its best, and stop at the last point that some plan can still reach. Each stopping point is a candidate trade-off. Because the marks are evenly spaced, the stopping points are usually spread out too.

With two goals, every stopping point is a true best trade-off. With three or more, a stopping point can sometimes be beaten, so check each one.

## The problem

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p$, and $y = f(x)$ is the image of $x$.

The input is a [multi-objective optimization](/multi-objective-optimization/) problem $\min F(x) = (f_1(x), \ldots, f_p(x))$ over $x \in X$, and a grid size $H \ge 1$. The output is a list of points $F(x)$, one for each weight vector $\beta$ in the grid

$$B_H = \{\beta \in \mathbb{R}^p : \beta \ge 0,\ \textstyle\sum_i \beta_i = 1,\ H \beta_i \text{ integer}\},$$

which has $\binom{H + p - 1}{p - 1}$ elements. The aim is a *representation* of the front, a finite set of points spread over it, not the whole front.

Let $x_i^*$ be a Pareto optimal minimizer of $f_i$, the *anchor* of objective $i$. Let $F^*$ be the ideal point, with $F^*_i = f_i(x_i^*)$, and let the pay-off matrix $\Phi$ have the columns $F(x_i^*) - F^*$. Its diagonal is zero and its entries are nonnegative. The CHIM is the set $\{F^* + \Phi \beta : \beta \ge 0,\ \sum_i \beta_i = 1\}$, the simplex spanned by the images of the anchors.

## The algorithm

For each $\beta$, the *NBI subproblem* is

$$\mathrm{NBI}(\beta): \quad \max_{x,\, t}\ t \quad \text{subject to} \quad F(x) = F^* + \Phi \beta + t \hat n, \quad x \in X,$$

where $\hat n = -\Phi e$ with $e = (1, \ldots, 1)$. Das and Dennis define NBI with a unit normal to the CHIM that points toward the ideal point. The direction $-\Phi e$ is their *quasi-normal*, which is easy to compute and is the same for all $\beta$. It is the direction used here.

```pseudo id=main
NBI(F, X, H)                    ▷ minimize F = (f_1, ..., f_p) over X; H is the grid size
L1  for i ← 1 to p do x_i* ← a minimizer of f_i over X that is Pareto optimal
L2  F* ← (f_1(x_1*), ..., f_p(x_p*));  Φ ← the matrix with the columns F(x_i*) − F*
L3  n ← −Φ e                                       ▷ the quasi-normal direction
L4  for each β ≥ 0 with Σ β_i = 1 and H β integer do
L5      solve max t subject to F(x) = F* + Φ β + t n, x ∈ X; let (x, t) be optimal
L6      output F(x)
L7  return the outputs
```

Line L1 needs care when $f_i$ has several minimizers. The implementation minimizes $f_i$, then minimizes the sum of the other objectives with $f_i$ fixed at its minimum, which gives a Pareto optimal anchor. The implementation solves the case of a [multi-objective linear program](/multi-objective-linear-programming/), where line L5 is one linear program in $(x, t)$, with exact arithmetic.

## Example

Minimize $(x_1, x_2)$ over $X = \{x : x_1 \ge 0,\ x_2 \ge 0,\ x_1 + 2 x_2 \ge 4,\ 3 x_1 + x_2 \ge 6\}$, with $H = 4$. The front is the two edges from $(0, 6)$ to $(8/5, 6/5)$ and from $(8/5, 6/5)$ to $(4, 0)$. The anchors are $(0, 6)$ and $(4, 0)$, so

$$F^* = (0, 0), \quad \Phi = \begin{pmatrix} 0 & 4 \\ 6 & 0 \end{pmatrix}, \quad \hat n = -(4, 6).$$

The base point for $\beta$ is $(4 \beta_2, 6 \beta_1)$, on the segment between the two anchors, and the subproblem moves it along $-(4, 6)$ until it reaches the front.

| $\beta$ | base point | edge reached | $t$ | NBI point |
|---|---|---|---|---|
| $(1, 0)$ | $(0, 6)$ | none | $0$ | $(0, 6)$ |
| $(3/4, 1/4)$ | $(1, 9/2)$ | $3 y_1 + y_2 = 6$ | $1/12$ | $(2/3, 4)$ |
| $(1/2, 1/2)$ | $(2, 3)$ | $3 y_1 + y_2 = 6$ | $1/6$ | $(4/3, 2)$ |
| $(1/4, 3/4)$ | $(3, 3/2)$ | $y_1 + 2 y_2 = 4$ | $1/8$ | $(5/2, 3/4)$ |
| $(0, 1)$ | $(4, 0)$ | none | $0$ | $(4, 0)$ |

For $\beta = (1/2, 1/2)$, the point $(2 - 4t, 3 - 6t)$ is on the line $3 y_1 + y_2 = 6$ when $9 - 18 t = 6$, so $t = 1/6$. The five points lie on the front, two on each edge plus the corner anchors. Every weighted sum with positive weights finds one of only three points, $(0, 6)$, $(8/5, 6/5)$ or $(4, 0)$, unless its weights are exactly normal to an edge.

## Correctness

NBI is a method for a representation, so its guarantees are about the points it returns. The proofs are below.

- **Anchors.** The two-step rule of line L1 gives Pareto optimal anchors.
- **Well posed for linear programs.** If $X$ is a nonempty polyhedron, the objectives are linear and bounded below, and $\Phi \ne 0$, then each subproblem has an optimal solution with $0 \le t \le 1$. The point $x = \sum_j \beta_j x_j^*$ is feasible with $t = 0$.
- **Two objectives.** If $p = 2$ and $F[X] + \mathbb{R}^2_+$ is closed and convex, every NBI point is Pareto optimal, and it is the point where the line through the base point in the direction $\hat n$ meets the front. The proof uses the convex function whose graph is the lower boundary of $F[X] + \mathbb{R}^2_+$.
- **Three or more objectives.** The output can be dominated. In the tetrahedron $X \subset \mathbb{R}^3$ with the vertices $(0, 2, 2)$, $(2, 0, 2)$, $(2, 2, 0)$ and $(1, 1, 1)$, with $F(x) = x$, the subproblem for $\beta = (1/2, 1/2, 0)$ returns $(1, 1, 2)$, which $(1, 1, 1)$ dominates.
- **Scale invariance.** If each objective is multiplied by a positive constant and shifted, the subproblems have the same solutions. So the result does not depend on the units of the objectives.

## Complexity

The method solves $p$ problems for the ideal point, up to $p$ more for Pareto optimal anchors, and one subproblem for each of the $M = \binom{H + p - 1}{p - 1}$ grid points. So the time is $O((M + p) L)$, where $L$ is the cost of one subproblem. The subproblems are independent and can run in parallel. The extra space is $O(p^2)$ for $F^*$, $\Phi$ and $\hat n$, plus the output.

The number $M$ grows fast with $p$: for $H = 10$ it is $11$ for $p = 2$, $66$ for $p = 3$ and $1001$ for $p = 5$. For a nonlinear problem, each subproblem is a nonconvex program in general, and a local solver returns a local solution, so $L$ is the cost of that solver.

## Properties

- **Even spread.** The base points are evenly spread on the CHIM. For many problems this gives a fairly even spread on the front, much better than evenly spread weights in a weighted sum. It is not a guarantee: steep parts of the front still get fewer points.
- **Nonconvex fronts.** The subproblem is a constrained problem along a line, not a weighted sum, so it can reach points in nonconvex parts of the front, which no weighted sum reaches.
- **Not always Pareto optimal.** For $p \ge 3$, and for nonconvex problems with any $p \ge 2$, the line from a base point can leave the image at a dominated point. A filter step, such as [Pareto front computation](/pareto-front-computation/) on the output or one efficiency test per point, removes such points.
- **Incomplete coverage.** For $p \ge 3$, parts of the front that no line from the CHIM reaches are never found, because the base points use only $\beta \ge 0$.
- **Scale invariance.** Unlike a weighted sum, the result does not change if an objective is measured in different units.
- **Equality constraints.** The constraint $F(x) = F^* + \Phi \beta + t \hat n$ is $p$ equations. For a nonlinear $F$ these are nonlinear equality constraints, which make the subproblem harder for local solvers.

## Variants and improvements

- **Relaxed subproblem.** Replace the equation by $F(x) \le F^* + \Phi \beta + t \hat n$. This is a Pascoletti and Serafini scalarization. Its solutions are weakly Pareto optimal, and the feasible set is larger, so local solvers have an easier problem. For two objectives it gives the same points as NBI on a convex problem.
- **Normal constraint method.** Messac, Ismail-Yahaya and Mattson (2003) normalize the objectives, keep the base points on the plane of the anchors, and add inequality constraints that cut the image by hyperplanes normal to the plane. Each subproblem minimizes one objective. It avoids the equality constraints of NBI.
- **Exact use of the normal.** With the unit normal of the CHIM instead of the quasi-normal, the lines are perpendicular to the CHIM. For $p = 2$ both directions give points on the front, at different places.
- **Grid of reference directions.** The same simplex grid $B_H$, called the Das and Dennis points, is used to place reference directions in [NSGA-III](/nsga-iii/) and in decomposition methods such as [MOEA/D](/moea-d/).
- **Other scalarizations with a grid.** The [epsilon-constraint method](/epsilon-constraint-method/) with an even grid of bounds, and the [achievement scalarizing function](/achievement-scalarizing-function/) with reference points on the CHIM, also give spread-out points, and always give weakly Pareto optimal points.

## When to use it

Use NBI when a decision maker wants a picture of the whole front of a continuous problem with two or three objectives, each point is costly, and the weighted sum method gives a poor spread or misses nonconvex parts. For two convex objectives it is a reliable way to get evenly spread Pareto points. For three or more objectives, add a check that removes dominated points. For a [multi-objective linear program](/multi-objective-linear-programming/) where the exact front is wanted, [Benson's algorithm](/benson-algorithm/) gives all vertices instead of a sample.

## Pitfalls

- **Anchors that are only weakly Pareto optimal.** If an objective has several minimizers and line L1 takes any one, the CHIM can be wrong and the edge points can be dominated. Use a lexicographic step.
- **Dominated output for $p \ge 3$.** Do not report the NBI points as Pareto optimal without a check.
- **Local solutions.** For a nonconvex problem, a local solver may stop at a point that is not on the boundary at all. Start each subproblem from the solution of a neighboring one.
- **Grid size.** The number of subproblems grows as $\binom{H + p - 1}{p - 1}$, so a fine grid is not affordable for many objectives.
- **Degenerate pay-off matrix.** If all anchors have the same image, $\Phi = 0$ and the subproblem is unbounded in $t$. Then the ideal point is attainable and is the only nondominated point.

## Implementations

## History

Das and Dennis (1997) showed that minimizing weighted sums with evenly spread weights gives an uneven spread of points, and cannot find points in nonconvex parts of the front. In 1998 they proposed normal boundary intersection as a geometric remedy, with the CHIM, the normal lines and the quasi-normal, for nonlinear engineering design problems. They noted that NBI points need not be Pareto optimal. Messac, Ismail-Yahaya and Mattson (2003) gave the normal constraint method, which keeps the idea of evenly spread base points but uses inequality constraints. The simplex grid of Das and Dennis later became a standard way to place reference directions in evolutionary methods.

## References
