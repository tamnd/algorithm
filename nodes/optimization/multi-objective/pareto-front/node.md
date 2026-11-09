---
tag: Q4WYTC
kind: concept
slug: pareto-front
name: Pareto front
aliases:
- Pareto frontier
- Pareto set
- trade-off surface
- nondominated set
- efficient frontier
area: optimization/multi-objective
level: intro
summary: The set of images of the Pareto optimal solutions, that is, the nondominated points of the objective space. It shows every best trade-off between the objectives.
prereqs: [pareto-optimality]
see_also: [pareto-dominance, ideal-point, nadir-point, pareto-front-computation, weighted-sum-method, hypervolume-indicator, approximate-pareto-set]
sources:
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 2 (nondominated points and the set Y plus the nonnegative orthant), Chapter 3 (supported points and connectedness) and Chapter 6 (the nondominated set of a multicriteria linear program)
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 2 (the non-dominated front and the shapes of fronts)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part I, Chapter 2 (the Pareto optimal set and its ranges)
---

The Pareto front of a [multi-objective optimization](/multi-objective-optimization/) problem is the set of images $f(x)$ of its [Pareto optimal](/pareto-optimality/) solutions, that is, the points of the objective space that no other attainable point [dominates](/pareto-dominance/). It shows every best trade-off: along the front, one objective can improve only when another gets worse. The set of the Pareto optimal solutions themselves, in the decision space, is the Pareto set; many authors use the two names loosely.

## In plain words

Draw each possible solution as a dot, with its cost on one axis and its weight on the other. Lower is better on both axes. A dot is on the front when no other dot lies below it and to its left at the same time.

For a finite list, the front looks like a staircase that goes down from the left to the right. Each step down costs a step to the right. Dots above the staircase are wasteful: some dot on the staircase is at least as good in both measures.

The front is the menu of honest choices. Every dot on it is a defensible answer, and the choice between them depends on what the person who decides cares about more.

## The idea

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of a solution $x$, and $Y = f(X)$ is the set of attainable images. The front is

$$Y_N = \{\, y \in Y : \text{there is no } y' \in Y \text{ with } y' \prec y \,\}.$$

**The front depends only on the lower-left part of $Y$.** Let $\mathbb{R}^p_{\ge} = \{ d : d \geqq 0 \}$ be the nonnegative orthant, and let $Y + \mathbb{R}^p_{\ge}$ be the set of all points $y + d$. Then $(Y + \mathbb{R}^p_{\ge})_N = Y_N$.

*Proof.* Let $y \in Y_N$. If some $y' + d \prec y$ with $y' \in Y$ and $d \geqq 0$, then $y' \leqq y' + d \prec y$, so $y' \prec y$, which is false. So $y$ is nondominated in the larger set. Conversely, let $z = y + d$ be nondominated in $Y + \mathbb{R}^p_{\ge}$. If $d \ne 0$, then $y \prec z$ with $y$ in the larger set, which is false; so $z = y \in Y$. No point of $Y$ dominates $y$, because $Y$ is a subset of the larger set. So $z \in Y_N$. $\square$

This is why methods for linear and convex problems work with the *upper image* $Y + \mathbb{R}^p_{\ge}$: it is convex when $Y$ is convex, and it is a polyhedron when $Y$ is a polytope. [Benson's algorithm](/benson-algorithm/) approximates it from outside.

**Two objectives give a monotone curve.** For $p = 2$, if $y, y' \in Y_N$ and $y_1 < y'_1$, then $y_2 > y'_2$, since $y_2 \le y'_2$ would mean $y \prec y'$. So the points of the front sorted by $f_1$ are also sorted by $f_2$ in reverse. A finite front is a staircase, and [Kung's algorithm](/kung-algorithm/) for $p = 2$ is a sort followed by one scan. For larger $p$ the front of a continuous problem is typically a surface of dimension $p - 1$, but it can have lower dimension, and it can have gaps.

**Supported and unsupported points.** A point $\hat{y} \in Y_N$ is *supported* when it minimizes $\lambda^\top y$ over $Y$ for some weight vector $\lambda$ with all $\lambda_i > 0$. Geometrically, a supporting hyperplane with a positive normal touches $Y + \mathbb{R}^p_{\ge}$ at $\hat{y}$. When $Y + \mathbb{R}^p_{\ge}$ is convex, every properly nondominated point is supported. When it is not convex, the front can have unsupported points in its "dents", and the [weighted sum method](/weighted-sum-method/) cannot find them. Supported points that are vertices of the convex hull of $Y + \mathbb{R}^p_{\ge}$ are called *extreme supported*.

**Bounds.** The [ideal point](/ideal-point/) $y^I$ and the [nadir point](/nadir-point/) $y^N$ are the componentwise minimum and maximum over $Y_N$. Each nondominated point lies in the box $[y^I, y^N]$. They are used to normalize objectives with different units.

**Structure for linear problems.** For a [multi-objective linear program](/multi-objective-linear-programming/), the upper image is a polyhedron, every nondominated point is supported, and $Y_N$ is a connected union of faces of the upper image (Ehrgott, Chapter 6). So the front is described by finitely many extreme points.

**Size for combinatorial problems.** For a finite $X$, the front is finite, but it can have exponentially many points in the input size; see the [multi-objective shortest path](/multi-objective-shortest-path/) and the [multi-objective minimum spanning tree](/multi-objective-minimum-spanning-tree/). In practice one computes a subset or an [approximate Pareto set](/approximate-pareto-set/), and measures its quality by indicators such as the [hypervolume indicator](/hypervolume-indicator/) or the [IGD indicator](/igd-indicator/).

## Examples

**A finite staircase.** The images $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$ have the front $Y_N = \{a, b, d, e, g\}$, sorted by $f_1$ with $f_2$ falling: $9, 6, 4, 3, 1$. The supported points are $a, b, d, g$, the vertices of the lower left convex hull. The point $e = (7, 3)$ is unsupported: the segment from $d = (5, 4)$ to $g = (9, 1)$ passes through $(7, 2.5)$, which lies below $e$. The ideal point is $(2, 1)$, and the nadir point is $(9, 9)$.

**A convex front.** Minimize $f_1 = x^2$ and $f_2 = (x - 2)^2$ over $x \in \mathbb{R}$. The Pareto set is $[0, 2]$, and the front is the convex curve $y_2 = (2 - \sqrt{y_1})^2$, $0 \le y_1 \le 4$. Every point is supported: the weights $(\lambda, 1 - \lambda)$ with $0 < \lambda < 1$ give the minimizer $x = 2(1 - \lambda)$.

**A concave front.** Minimize $f_1 = x$ and $f_2 = 1 - x^2$ over $x \in [0, 1]$. All points are Pareto optimal, and the front is the curve $y_2 = 1 - y_1^2$. For weights $\lambda > 0$, the function $\lambda_1 x + \lambda_2 (1 - x^2)$ is concave in $x$, so its minimum over $[0, 1]$ is at an end point. Only $(0, 1)$ and $(1, 0)$ are supported.

**A front with a gap.** Minimize $f_1(x) = x$ and the continuous function $f_2$ over $x \in [0, 1]$, where $f_2(x) = 1 - 2x$ on $[0, 0.25]$, $f_2(x) = 2x$ on $[0.25, 0.5]$ and $f_2(x) = 2 - 2x$ on $[0.5, 1]$. Since $f_1$ increases with $x$, a point $x$ is Pareto optimal exactly when $f_2(x) < f_2(x')$ for every $x' < x$. This holds on $[0, 0.25]$, where $f_2$ falls from 1 to 0.5. It fails on $(0.25, 0.75]$, where $f_2 \ge 0.5 = f_2(0.25)$. It holds again on $(0.75, 1]$, where $f_2 < 0.5$. So the front is $\{(t, 1 - 2t) : 0 \le t \le 0.25\} \cup \{(t, 2 - 2t) : 0.75 < t \le 1\}$. It has two pieces, and the second piece is not closed: the point $(0.75, 0.5)$ is dominated by $(0.25, 0.5)$. The test problem ZDT3 of evolutionary computation has a front in several pieces for the same reason: its second objective rises and falls as the first one grows.

## Where it is used

- [Pareto front computation](/pareto-front-computation/) and [Kung's algorithm](/kung-algorithm/) find the front of a finite list of vectors.
- The [weighted sum method](/weighted-sum-method/), the [epsilon-constraint method](/epsilon-constraint-method/), the [weighted Tchebycheff method](/weighted-tchebycheff-method/) and [normal boundary intersection](/normal-boundary-intersection/) each find one point of the front per subproblem, and trace the front by a sweep of their parameters.
- [Benson's algorithm](/benson-algorithm/) finds the extreme points of the front of a linear problem.
- [Non-dominated sorting](/non-dominated-sorting/) in [NSGA-II](/nsga-ii/) peels off one front after the other from a population.
- The [hypervolume indicator](/hypervolume-indicator/) measures the region that a front dominates up to a reference point.

## References
