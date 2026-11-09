---
tag: R2SNEM
kind: technique
slug: weighted-sum-method
name: Weighted sum method
aliases:
- linear scalarization
- weighted sum scalarization
- weighting method
- dichotomic method
area: optimization/multi-objective
level: intro
summary: Minimizes a nonnegative weighted sum of objectives; finds only supported Pareto points in nonconvex problems.
prereqs: [scalarization, pareto-optimality]
see_also: [weighted-tchebycheff-method, epsilon-constraint-method, pareto-front, multi-objective-linear-programming, parametric-linear-programming, supporting-hyperplane, separating-hyperplane-theorem]
sources:
  - paper: doi:10.1016/0022-247X(68)90201-1
    title: Arthur M. Geoffrion, Proper efficiency and the theory of vector maximization, Journal of Mathematical Analysis and Applications 22(3), 1968
    locator: pages 618 to 630 (proper efficiency, and the equivalence with weighted sums with positive weights in the convex case)
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 3 (the weighted sum method, supported points and proper efficiency)
  - paper: doi:10.1287/mnsc.25.1.73
    title: Y. P. Aneja and K. P. K. Nair, Bicriteria transportation problem, Management Science 25(1), 1979
    locator: pages 73 to 78 (the search for the extreme supported points of a bicriteria problem by weights normal to segments)
  - paper: doi:10.1007/BF01197559
    title: Indraneel Das and J. E. Dennis, A closer look at drawbacks of minimizing weighted sums of objectives for Pareto set generation in multicriteria optimization problems, Structural Optimization 14(1), 1997
    locator: pages 63 to 69 (uneven spread and missed nonconvex parts)
  - paper: doi:10.1007/s00158-003-0368-6
    title: R. T. Marler and J. S. Arora, Survey of multi-objective optimization methods for engineering, Structural and Multidisciplinary Optimization 26(6), 2004
    locator: pages 369 to 395 (the weighted sum method and the choice of weights)
---

The weighted sum method solves a [multi-objective optimization](/multi-objective-optimization/) problem by minimizing $\sum_i \lambda_i f_i(x)$ for a weight vector $\lambda$. With positive weights every optimum is [Pareto optimal](/pareto-optimality/), and even properly Pareto optimal. For convex problems the converse holds too, so a sweep of the weights traces the whole [Pareto front](/pareto-front/). For nonconvex problems it finds only the *supported* points, those on the convex hull of the front, and it misses the points in the dents.

## In plain words

Give each goal a weight that says how much it matters. Multiply each number by its weight and add them up. The choice with the smallest total wins.

If every weight is above zero, the winner is always a fair trade-off: a choice that is worse on every count has a larger total, so it cannot win.

Changing the weights moves the winner along the front. But some fair trade-offs never win for any weights. Picture the front as a bent line. A straight ruler pushed against it from below touches only the outer corners. Points that sit in a dent, above the line between two corners, are never touched.

## When it applies

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, $Y = f(X)$, and $\lambda \in \mathbb{R}^p$ is the weight vector. The problem with weights $\lambda$ is

$$P(\lambda) : \quad \min_{x \in X} \ \lambda^\top f(x) = \sum_{i=1}^p \lambda_i f_i(x).$$

Use it when:

- the problem is convex (a convex $X$ and convex $f_i$), and in particular a [multi-objective linear program](/multi-objective-linear-programming/), where every Pareto optimal point is supported;
- the single-objective problem has structure that a linear combination of costs keeps, for example a shortest path or a [minimum spanning tree](/minimum-spanning-tree/) with combined edge costs;
- the decision maker can state the relative value of the objectives, so that one solve is enough;
- only the extreme supported points are needed, for example as a first phase before a search for the rest of the front.

**Positive weights give Pareto optimal points.** Let $\lambda > 0$ (all $\lambda_i > 0$) and let $\hat{x}$ be an optimal solution of $P(\lambda)$. Then $\hat{x}$ is Pareto optimal.

*Proof.* If $f(x) \prec f(\hat{x})$ for some $x \in X$, then $f_i(x) \le f_i(\hat{x})$ for all $i$ and $f_k(x) < f_k(\hat{x})$ for some $k$. With $\lambda > 0$ this gives $\lambda^\top f(x) < \lambda^\top f(\hat{x})$, which contradicts the optimality of $\hat{x}$. $\square$

**Nonnegative weights give weakly Pareto optimal points.** Let $\lambda \geqq 0$, $\lambda \ne 0$, and let $\hat{x}$ be optimal for $P(\lambda)$. Then $\hat{x}$ is weakly Pareto optimal. If moreover $f(\hat{x})$ is the only optimal image, $\hat{x}$ is Pareto optimal.

*Proof.* If $f(x) < f(\hat{x})$, then $\lambda^\top f(x) < \lambda^\top f(\hat{x})$ because some $\lambda_i > 0$. For the second claim, if $f(x) \prec f(\hat{x})$, then $\lambda^\top f(x) \le \lambda^\top f(\hat{x})$, so $x$ is also optimal with another image. $\square$

**Proper efficiency.** Geoffrion (1968) calls a Pareto optimal $\hat{x}$ *properly efficient* when there is an $M > 0$ such that for each $i$ and each $x \in X$ with $f_i(x) < f_i(\hat{x})$ there is a $j$ with $f_j(x) > f_j(\hat{x})$ and

$$\frac{f_i(\hat{x}) - f_i(x)}{f_j(x) - f_j(\hat{x})} \le M.$$

So no gain in one objective costs an unboundedly small loss in another. If $\lambda > 0$ and $\hat{x}$ is optimal for $P(\lambda)$, then $\hat{x}$ is properly efficient with $M = (p - 1) \max_j \lambda_j / \min_j \lambda_j$.

*Proof.* Let $f_i(x) < f_i(\hat{x})$. Optimality gives $\lambda_i (f_i(\hat{x}) - f_i(x)) \le \sum_{j \ne i} \lambda_j (f_j(x) - f_j(\hat{x}))$. The left side is positive. Let $k \ne i$ maximize $\lambda_j (f_j(x) - f_j(\hat{x}))$ over $j \ne i$. That term is positive, so $f_k(x) > f_k(\hat{x})$, and the sum is at most $(p - 1)$ times it. Hence $f_i(\hat{x}) - f_i(x) \le (p - 1) (\lambda_k / \lambda_i) (f_k(x) - f_k(\hat{x})) \le M (f_k(x) - f_k(\hat{x}))$. $\square$

**The converse needs convexity.** Let $X$ be convex and each $f_i$ convex. Then $Y + \mathbb{R}^p_{\ge}$ is convex, and:

1. each weakly Pareto optimal $\hat{x}$ is optimal for $P(\lambda)$ for some $\lambda \geqq 0$, $\lambda \ne 0$;
2. each properly efficient $\hat{x}$ is optimal for $P(\lambda)$ for some $\lambda > 0$ (Geoffrion, 1968).

*Proof of 1.* Let $\hat{y} = f(\hat{x})$. The convex sets $A = Y + \mathbb{R}^p_{\ge}$ and $B = \{ \hat{y} - e : e > 0 \}$ are disjoint: $y + d = \hat{y} - e$ would give $y < \hat{y}$. By the [separating hyperplane theorem](/separating-hyperplane-theorem/) there is a $\lambda \ne 0$ with $\lambda^\top (y + d) \ge \lambda^\top (\hat{y} - e)$ for all $y \in Y$, $d \geqq 0$, $e > 0$. If some $\lambda_i < 0$, a large $d_i$ breaks the inequality, so $\lambda \geqq 0$. Letting $d \to 0$ and $e \to 0$ gives $\lambda^\top y \ge \lambda^\top \hat{y}$ for all $y \in Y$. $\square$

Part 2 needs a finer separation, and we refer to Geoffrion's paper for it.

**Only supported points.** A point $\hat{y} \in Y_N$ is *supported* when it is optimal for $P(\lambda)$ for some $\lambda > 0$. By definition, the weighted sum with positive weights finds exactly the supported points, and no others. When $Y + \mathbb{R}^p_{\ge}$ is not convex, unsupported Pareto optimal points can exist.

*Counterexample.* Let $Y = \{(0, 1), (1, 0), (0.6, 0.6)\}$. All three points are nondominated. For $\lambda = (t, 1 - t)$ with $0 \le t \le 1$, the values are $1 - t$, $t$ and $0.6$. Since $\min(t, 1 - t) \le 0.5 < 0.6$, the point $(0.6, 0.6)$ never wins. For a continuous example, minimize $f_1(x) = x$ and $f_2(x) = 1 - x^2$ over $[0, 1]$. Every $x$ is Pareto optimal, but $\lambda_1 x + \lambda_2 (1 - x^2)$ is concave in $x$, so its minimum over $[0, 1]$ is at $x = 0$ or $x = 1$. Only the two end points of the front are supported.

## The template

For two objectives, the weights need not be fixed in advance. The dichotomic method of Aneja and Nair (1979) chooses each weight vector as the normal of the segment between two points already found. It returns the extreme supported points, the vertices of the lower-left boundary of the convex hull of $Y$.

```pseudo id=main
DICHOTOMIC(X, f)                                   ▷ p = 2
L1  y^a ← image of a lexicographic minimizer of (f_1, f_2)
L2  y^b ← image of a lexicographic minimizer of (f_2, f_1)
L3  S ← {y^a, y^b}; push the pair (y^a, y^b) onto a stack
L4  while the stack is not empty do
L5      pop a pair (y^l, y^r)                       ▷ y^l_1 < y^r_1 and y^l_2 > y^r_2
L6      λ ← (y^l_2 − y^r_2, y^r_1 − y^l_1)          ▷ normal of the segment, λ > 0
L7      y ← image of an optimal solution of P(λ)
L8      if λᵀy < λᵀy^l then
L9          S ← S ∪ {y}; push (y^l, y) and (y, y^r)
L10 return S
```

The weight in line L6 makes $\lambda^\top y^l = \lambda^\top y^r$, so line L8 asks whether some point of $Y$ lies strictly below the line through $y^l$ and $y^r$.

**Correctness.** Assume $Y$ is compact and $y^a \ne y^b$. Let $H$ be the lower-left boundary of the convex hull of $Y$, from $y^a$ to $y^b$. It is a convex chain, and its vertices are the extreme supported points. Every point added to $S$ is supported, because it is optimal for $P(\lambda)$ with $\lambda > 0$, so it lies on $H$. Keep the invariant that each pair $(y^l, y^r)$ on the stack has both points on $H$. Because the chain is convex, the points of $H$ between $y^l$ and $y^r$ lie on or below the line through them, and the other points of $Y$ lie on or above it. So if a vertex of $H$ lies strictly between $y^l$ and $y^r$, it is strictly below the line, the test of line L8 succeeds, and the new point $y$ is on $H$ strictly between $y^l$ and $y^r$. Every vertex between $y^l$ and $y^r$ is then $y$ itself or lies in one of the two new pairs. If the test fails, the part of $H$ from $y^l$ to $y^r$ is a straight edge with no vertex inside. By induction every extreme supported point ends in $S$. Each success adds a new point of $H$. So the method stops when $H$ has finitely many vertices, as for a finite set or the image of a linear program.

**Cost.** Let $s = |S|$ at the end. There are $s - 2$ successful solves, and each pair that is popped and fails is a final pair, $s - 1$ of them. So the method makes $2s - 3$ weighted sum solves and 2 lexicographic solves. For $p \ge 3$ the same idea needs the facets of a convex hull in $p$ dimensions, and the weights come from the normals of those facets.

### A worked example

Take $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$.

| step | pair | $\lambda$ | best value | value at $y^l$ | result |
|---|---|---|---|---|---|
| 1 | $(a, g)$ | $(8, 7)$ | $b$: 66 | 79 | add $b$ |
| 2 | $(b, g)$ | $(5, 6)$ | $d$: 49 | 51 | add $d$ |
| 3 | $(d, g)$ | $(3, 4)$ | $d$ and $g$: 31 | 31 | edge |
| 4 | $(b, d)$ | $(2, 2)$ | $b$ and $d$: 18 | 18 | edge |
| 5 | $(a, b)$ | $(3, 1)$ | $a$ and $b$: 15 | 15 | edge |

The result is $S = \{a, b, d, g\}$ after $2 \cdot 4 - 3 = 5$ weighted solves. The point $e$ has value $3 \cdot 7 + 4 \cdot 3 = 33 > 31$ in step 3: it lies above the edge from $d$ to $g$, which passes through $(7, 2.5)$. With the normalized weights $(t, 1 - t)$, the optimum is $a$ for $t > 3/4$, $b$ for $1/2 < t < 3/4$, $d$ for $3/7 < t < 1/2$ and $g$ for $t < 3/7$, with ties at the breakpoints. The value of $e$ is $3 + 4t$; it is below the value $4 + t$ of $d$ only for $t < 1/3$, and below the value $1 + 8t$ of $g$ only for $t > 1/2$, so $e$ never wins.

## Classic examples

- **[Multi-objective linear programming](/multi-objective-linear-programming/).** Every nondominated point is supported, so the weighted sum with all $\lambda > 0$ finds the whole front. The weight space splits into regions with one optimal vertex each, as in [parametric linear programming](/parametric-linear-programming/).
- **Bicriteria combinatorial problems.** For the [multi-objective shortest path](/multi-objective-shortest-path/), the [multi-objective minimum spanning tree](/multi-objective-minimum-spanning-tree/) and the bicriteria transportation problem, the dichotomic method finds the extreme supported points with a fast single-objective algorithm. The two-phase method then searches the triangles between them for the unsupported points.
- **Portfolio selection.** The mean-variance problem of Markowitz minimizes $\lambda \cdot \text{risk} - (1 - \lambda) \cdot \text{return}$. The problem is convex, so the weights trace the whole efficient frontier.

## Variations

- **Normalized weights.** One can assume $\sum_i \lambda_i = 1$, because $P(\lambda)$ and $P(c \lambda)$ have the same optima for $c > 0$. With normalized objectives, divided by the range between the [ideal point](/ideal-point/) and the [nadir point](/nadir-point/), equal weights mean equal importance.
- **Weight space decomposition.** For a finite or polyhedral $Y$, the set of normalized weights for which a given extreme point is optimal is a convex polytope. These polytopes cover the weight simplex. The dichotomic method computes this decomposition for $p = 2$.
- **Weighted sum with extra constraints.** The hybrid method adds the bounds $f(x) \leqq f(x^0)$ to $P(\lambda)$. It finds every Pareto optimal point, at the cost of the structure of the problem.

## Pitfalls

- **Missing unsupported points.** On a nonconvex front, no sweep of the weights finds the points in the dents. For combinatorial problems, the unsupported points are often most of the front.
- **Zero weights.** With some $\lambda_i = 0$, an optimum can be dominated: for $Y = \{(0, 0), (0, 1)\}$ and $\lambda = (1, 0)$ both points are optimal. Use positive weights, or keep only one optimum with the best other objectives.
- **Uneven spread.** Even steps in the weights give uneven points on the front (Das and Dennis, 1997). A whole interval of weights returns the same vertex, and a tiny change of weights can jump over a long flat part.
- **Units.** The weights mix units. If one objective is in dollars and the other in grams, the same weights mean different things after a change of units. Normalize first.
- **Weights are not priorities.** A weight of 0.9 on the first objective does not mean that the answer is close to the optimum of the first objective. In the example, $t = 0.7$ gives $b$, the second point of five.

## Exercises

1. Show that $Y_N$ of a finite set with $p = 2$ always contains the two lexicographic minimizers, and that they are both supported. *Answer:* the first is optimal for $\lambda = (1, \delta)$ for small $\delta > 0$, since it has the least $y_1$ and, among those, the least $y_2$; the second likewise.
2. Give a set of four points in $\mathbb{R}^2$, all nondominated, of which only two are supported. *Answer:* $(0, 3)$, $(1, 2.5)$, $(2.5, 1)$, $(3, 0)$; both inner points lie above the segment $y_1 + y_2 = 3$.
3. Run the dichotomic method on $(0, 4)$, $(1, 2)$, $(2, 1.5)$, $(3, 0)$ and count the solves. *Answer:* the pair $((0, 4), (3, 0))$ gives $\lambda = (4, 3)$, values $12, 10, 12.5, 12$, so $(1, 2)$ is added. The pair $((1, 2), (3, 0))$ gives $\lambda = (2, 2)$, values $8, 6, 7, 6$, so it is an edge, and $(2, 1.5)$, with the value 7, is unsupported. The pair $((0, 4), (1, 2))$ gives $\lambda = (2, 1)$ and is an edge. That is $3 = 2 \cdot 3 - 3$ weighted solves.

## References
