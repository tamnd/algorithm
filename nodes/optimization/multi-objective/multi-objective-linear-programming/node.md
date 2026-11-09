---
tag: QM45A1
kind: problem
slug: multi-objective-linear-programming
name: Multi-objective linear programming
aliases:
- MOLP
- multi-objective LP
- multiple objective linear programming
- linear vector optimization
- multicriteria linear programming
area: optimization/multi-objective
level: advanced
summary: Linear program with several linear objectives over a polyhedral feasible set.
prereqs: [linear-programming-problem, lp-duality, pareto-optimality, polyhedron]
see_also: [benson-algorithm, normal-boundary-intersection, weighted-sum-method, epsilon-constraint-method, parametric-linear-programming, goal-programming, lexicographic-optimization, simplex-method]
sources:
  - paper: doi:10.1287/opre.22.1.189
    title: H. Isermann, Technical note, Proper efficiency and the linear vector maximum problem, Operations Research 22(1), 1974
    locator: pages 189 to 191 (every efficient solution of a linear vector problem is optimal for a weighted sum with positive weights)
  - paper: doi:10.1016/0022-247X(75)90189-4
    title: P. L. Yu and M. Zeleny, The set of all nondominated solutions in linear cases and a multicriteria simplex method, Journal of Mathematical Analysis and Applications 49(2), 1975
    locator: pages 430 to 468 (the structure and connectedness of the efficient set, and a multicriteria simplex method)
  - paper: doi:10.1007/BF01580453
    title: J. G. Ecker and I. A. Kouada, Finding efficient points for linear multiple objective programs, Mathematical Programming 8(1), 1975
    locator: pages 375 to 377 (one linear program tests whether a point is efficient)
  - paper: doi:10.1007/BF01581642
    title: Katta G. Murty, Computational complexity of parametric linear programming, Mathematical Programming 19(1), 1980
    locator: pages 213 to 219 (parametric linear programs with exponentially many breakpoints)
  - paper: doi:10.1137/060674831
    title: Frank Heyde and Andreas Löhne, Geometric duality in multiple objective linear programming, SIAM Journal on Optimization 19(2), 2008
    locator: pages 836 to 845 (the duality between the facets of the upper image and the vertices of a dual polyhedron)
  - paper: doi:10.1023/A:1008215702611
    title: Harold P. Benson, An outer approximation algorithm for generating all efficient extreme points in the outcome set of a multiple objective linear programming problem, Journal of Global Optimization 13(1), 1998
    locator: pages 1 to 24
  - paper: doi:10.1007/978-3-662-48350-3_25
    title: Fritz Bökler and Petra Mutzel, Output-sensitive algorithms for enumerating the extreme nondominated points of multiobjective combinatorial optimization problems, ESA 2015, Lecture Notes in Computer Science 9294
    locator: pages 288 to 299 (output-polynomial enumeration of the extreme nondominated points of a multi-objective linear program for a fixed number of objectives)
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapters 6 and 7 (multicriteria linear programming and the multicriteria simplex method)
---

A multi-objective linear program minimizes several linear objectives $C x$ over a polyhedron $X$. It is the simplest continuous [multi-objective optimization](/multi-objective-optimization/) problem, and it keeps much of the structure of a [linear program](/linear-programming-problem/): the image of $X$ is a polyhedron, every point of the [Pareto front](/pareto-front/) is optimal for some weighted sum with positive weights (Isermann, 1974), the efficient set is a connected union of faces of $X$ (Yu and Zeleny, 1975), and one linear program tests whether a given point is efficient. The difficulty is size: the front can have exponentially many extreme points even for two objectives. The main exact methods are multi-objective simplex methods in the decision space and [Benson's outer approximation algorithm](/benson-algorithm/) in the objective space.

## In plain words

A factory makes several products from limited resources. Each choice of amounts has a cost and an amount of pollution, and both change in a straight-line way with the amounts. You want both to be low, and no single plan is best for both.

A plan is good if no other plan is at least as good in both measures and better in one. The good plans form a broken line of flat pieces in the cost and pollution picture. The task is to find the corners and the flat pieces of this broken line. Each corner is the best plan for some fixed mix of the two measures, so ordinary linear programming finds any one of them. The hard part is that there can be a very large number of corners.

## Definition

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p$, and $y = f(x)$ is the image of $x$.

**Input.** A matrix $A \in \mathbb{R}^{m \times n}$, a vector $b \in \mathbb{R}^m$ and an objective matrix $C \in \mathbb{R}^{p \times n}$ with rows $c_1^\top, \ldots, c_p^\top$. The feasible set is the polyhedron $X = \{x \in \mathbb{R}^n : A x \geqq b\}$, and $f(x) = C x$.

**Solutions.** A point $x^* \in X$ is *efficient* if no $x \in X$ has $C x \leqq C x^*$ and $C x \ne C x^*$. Its image is a *nondominated point*. The set of nondominated points is $Y_N$, and $X_E$ is the set of efficient points.

**Upper image.** The polyhedron $\mathcal{P} = C[X] + \mathbb{R}^p_+$. If each objective is bounded below on $X$, its recession cone is $\mathbb{R}^p_+$, its vertices are the extreme points of $Y_N$, and its nondominated points are $Y_N$.

**Output.** Different tasks ask for different outputs:

- all vertices of $\mathcal{P}$, with a description of its facets, which describe all of $Y_N$;
- all efficient vertices of $X$, or all maximal efficient faces of $X$;
- one efficient point, or one that a decision maker prefers.

**Theorem (Isermann, 1974).** Let $X$ be a nonempty polyhedron. A point $x^* \in X$ is efficient if and only if there is a weight vector $\lambda \in \mathbb{R}^p$ with $\lambda_i > 0$ for each $i$ such that $x^*$ minimizes $\lambda^\top C x$ over $X$.

*Proof.* If $x^*$ minimizes $\lambda^\top C x$ with $\lambda > 0$ and some $x \in X$ had $C x \leqq C x^*$ and $C x \ne C x^*$, then $\lambda^\top C x < \lambda^\top C x^*$, a contradiction. Conversely, let $x^*$ be efficient, and consider the linear program

$$\max\ e^\top s \quad \text{subject to} \quad C x + s = C x^*, \quad A x \geqq b, \quad s \geqq 0,$$

with $e = (1, \ldots, 1)$. It is feasible with $(x, s) = (x^*, 0)$. A feasible $(x, s)$ with $s \ne 0$ would give $C x \leqq C x^*$ and $C x \ne C x^*$, so the optimal value is $0$. With multipliers $\mu$ (free) for the equations and $w \geqq 0$ for $A x \geqq b$, the dual is: minimize $\mu^\top C x^* - b^\top w$ subject to $C^\top \mu = A^\top w$ and $\mu \geqq e$. By strong duality it has an optimal solution with the value $0$. Then for every $x \in X$, $\mu^\top C x = w^\top A x \ge w^\top b = \mu^\top C x^*$. So $x^*$ minimizes $\mu^\top C x$ over $X$, and $\mu \geqq e$ has positive entries. $\blacksquare$

So every nondominated point of a multi-objective linear program is supported, unlike in the combinatorial problems such as the [multi-objective knapsack](/multi-objective-knapsack/). The set of minimizers of $\lambda^\top C x$ is a face of $X$, so $X_E$ is a union of faces of $X$. It need not be convex, but it is connected (Yu and Zeleny, 1975).

## Variants

- **Maximization.** Change the sign of the rows of $C$ that are maximized.
- **Bi-objective.** The case $p = 2$. The front is a convex piecewise linear curve, and it is the [parametric linear program](/parametric-linear-programming/) with the objective $c_1 + \theta c_2$.
- **Integer variables.** A multi-objective integer or [mixed-integer program](/mixed-integer-programming/). Isermann's theorem fails, unsupported points appear, and the front is no longer the boundary of a polyhedron.
- **Unbounded objectives.** If some objective is not bounded below, $\mathcal{P}$ has more recession directions, and the solution concept must list them. Hamel, Löhne and Rudloff treat this case.
- **Linear vector optimization with a cone.** Replace $\mathbb{R}^p_+$ by another polyhedral ordering cone. Benson-type methods work for this general form.
- **Preference models.** [Goal programming](/goal-programming/), [lexicographic optimization](/lexicographic-optimization/) and the [weighted Tchebycheff method](/weighted-tchebycheff-method/) give one point each by a linear program or a short sequence of linear programs.

## Examples

Minimize $(x_1, x_2)$ over

$$X = \{x \in \mathbb{R}^2 : x_1 \ge 0,\ x_2 \ge 0,\ x_1 + 2 x_2 \ge 4,\ 3 x_1 + x_2 \ge 6\}.$$

Here $C$ is the identity, so $\mathcal{P} = X$. The vertices of $X$ are $(0, 6)$, $(8/5, 6/5)$ and $(4, 0)$, and all three are nondominated. The front $Y_N$ is the two edges from $(0, 6)$ to $(8/5, 6/5)$ and from $(8/5, 6/5)$ to $(4, 0)$, on the lines $3 y_1 + y_2 = 6$ and $y_1 + 2 y_2 = 4$. The normals of these edges show which weights give which vertex:

| weights $\lambda > 0$ | minimizers of $\lambda_1 x_1 + \lambda_2 x_2$ |
|---|---|
| $\lambda_1 > 3 \lambda_2$ | $(0, 6)$ |
| $\lambda_1 = 3 \lambda_2$ | the edge from $(0, 6)$ to $(8/5, 6/5)$ |
| $\lambda_2 / 2 < \lambda_1 < 3 \lambda_2$ | $(8/5, 6/5)$ |
| $\lambda_1 = \lambda_2 / 2$ | the edge from $(8/5, 6/5)$ to $(4, 0)$ |
| $\lambda_1 < \lambda_2 / 2$ | $(4, 0)$ |

The [ideal point](/ideal-point/) is $(0, 0)$ and the [nadir point](/nadir-point/) is $(4, 6)$. The point $x^* = (2, 2)$ is feasible but not efficient: the test program of Ecker and Kouada has the optimal value $6/5$, reached at $x = (8/5, 6/5)$ with $s = (2/5, 4/5)$. [Benson's algorithm](/benson-algorithm/) on this instance is traced on its own page.

**Exponentially many extreme points.** Minimize $(x_1, \ldots, x_n, -x_1, \ldots, -x_n)$ over the cube $[0, 1]^n$, so $p = 2 n$. Every point of the cube is efficient, and each of the $2^n$ vertices $v$ is the unique minimizer of a weighted sum with positive weights: put the weights $2$ and $1$ on $x_j$ and $-x_j$ if $v_j = 0$, and $1$ and $2$ if $v_j = 1$. So $\mathcal{P}$ has $2^n$ vertices. For $p = 2$, Murty (1980) gave parametric linear programs with exponentially many breakpoints, and the same holds for the vertices of a bi-objective front.

## Known algorithms

- **Scalarization.** One [weighted sum](/weighted-sum-method/), [epsilon-constraint](/epsilon-constraint-method/), Tchebycheff or [achievement](/achievement-scalarizing-function/) problem is a linear program, and gives one nondominated point. By Isermann's theorem the weighted sums with positive weights reach every nondominated point.
- **Efficiency test.** The linear program in the proof above, from Ecker and Kouada (1975), tests whether a point $x^*$ is efficient. If not, its solution is an efficient point that dominates $x^*$, provided the program is bounded.
- **Multi-objective simplex methods.** Find one efficient vertex, then move along edges of $X$ between efficient bases, and test each edge for efficiency with a linear program (Yu and Zeleny, 1975, and earlier methods of Philip and of Evans and Steuer). They list the efficient vertices of $X$. Degenerate problems and many bases with the same image make them slow.
- **Parametric simplex for $p = 2$.** Start at the lexicographic minimum of $(f_1, f_2)$ and follow the [parametric](/parametric-linear-programming/) objective $\theta c_1 + (1 - \theta) c_2$, one pivot per breakpoint.
- **Benson's algorithm.** [Benson's outer approximation](/benson-algorithm/) works in $\mathbb{R}^p$. It cuts an outer polyhedron with supporting half-spaces from one linear program per vertex until it equals $\mathcal{P}$. Its dual variant uses geometric duality (Heyde and Löhne, 2008) and needs only weighted sum problems.
- **Even spread of points.** [Normal boundary intersection](/normal-boundary-intersection/) finds points on the front along a regular grid of directions, useful when the full front is too large.

## Bounds

- **Size.** If $X$ has a vertex, every vertex of $\mathcal{P}$ is the image of a vertex of $X$, so there are at most $\binom{m}{n}$ of them. The cube example gives $2^n$ vertices with $p = 2 n$, and Murty's construction gives exponentially many for $p = 2$. So no algorithm lists all of them in time polynomial in the input size alone.
- **One point.** A single nondominated point, or a test of efficiency, takes one linear program, so it is [polynomial](/lp-in-p/).
- **Output-sensitive bounds.** For a fixed $p$, Bökler and Mutzel (2015) showed that the extreme nondominated points can be listed in time polynomial in the input size and the number of points, with the dual variant of Benson's algorithm.
- **The nondominated set is not convex.** For $p \ge 2$, $Y_N$ is a union of faces of $\mathcal{P}$, so it is connected but in general not convex. Two vertices of the example, $(0, 6)$ and $(4, 0)$, have the midpoint $(2, 3)$, which is not in $Y_N$.

## Reductions

- **To linear programming.** With $p = 1$ the problem is a linear program. The weighted sum, epsilon-constraint and Tchebycheff problems are linear programs, so any one point reduces to one LP.
- **To parametric linear programming.** The bi-objective front is the optimal value function of a parametric LP in the weight $\theta$, and its breakpoints are the vertices of $\mathcal{P}$.
- **Geometric duality.** Heyde and Löhne (2008) defined a dual polyhedron whose vertices correspond to the facets of $\mathcal{P}$ and whose facets correspond to the vertices of $\mathcal{P}$. Computing one gives the other.
- **From combinatorial problems.** The convex hull of the feasible set of a combinatorial problem, such as the spanning tree polytope, gives a multi-objective linear program whose vertices are the supported extreme points of the combinatorial problem. This is how the [multi-objective minimum spanning tree](/multi-objective-minimum-spanning-tree/) and [multi-objective shortest path](/multi-objective-shortest-path/) problems get their supported points.

## Applications

- **Production and transport planning.** Cost, time and emissions as linear objectives of the same flow or production variables.
- **Radiation therapy planning.** Dose to the tumor and to each healthy organ as objectives. Approximate Benson methods were developed for these problems.
- **Finance.** [Portfolio](/portfolio-optimization/) problems with linear risk measures, and set-valued risk measures for markets with transaction costs, which need linear vector optimization with a general cone.
- **Supported points of combinatorial problems.** As in the reductions above.

## References
