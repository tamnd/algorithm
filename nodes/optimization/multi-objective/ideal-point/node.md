---
tag: N2XCRN
kind: concept
slug: ideal-point
name: Ideal point
aliases:
- utopia point
- ideal vector
- ideal objective vector
area: optimization/multi-objective
level: intro
summary: The vector whose i-th entry is the best value of the i-th objective alone. It is a lower bound for the whole Pareto front, and it is usually not attainable.
prereqs: [pareto-front]
see_also: [nadir-point, weighted-tchebycheff-method, achievement-scalarizing-function, normal-boundary-intersection, scalarization]
sources:
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 2 (bounds on the nondominated set, the ideal and nadir points) and Chapter 4 (compromise solutions as approximations of the ideal point)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part I, Chapter 2 (ranges of the Pareto optimal set, ideal and utopian objective vectors)
  - paper: doi:10.1016/S0377-2217(02)00595-7
    title: Matthias Ehrgott and Dagmar Tenfelde-Podehl, Computation of ideal and Nadir values and implications for their use in MCDM methods, European Journal of Operational Research 151(1), 2003
    locator: pages 119 to 139
---

The ideal point of a [multi-objective optimization](/multi-objective-optimization/) problem is the vector $y^I$ whose $i$-th entry is the minimum of the $i$-th objective alone, over the whole feasible set. It is a componentwise lower bound for every point of the [Pareto front](/pareto-front/). It costs one single-objective solve per objective, and it is the usual reference point of the [weighted Tchebycheff method](/weighted-tchebycheff-method/) and of the normalization of objectives. With the [nadir point](/nadir-point/) as the upper bound, it gives the box that holds the front.

## In plain words

Imagine a car that is the cheapest of all cars, also the fastest, and also the safest. That car would be ideal. You find each of its three numbers by looking at one measure at a time: the lowest price of any car, the best speed of any car, the best safety of any car.

Such a car almost never exists, because the cheapest car is not the fastest. The ideal car is still useful. It tells you how good each measure can ever get, and it gives you a target. Many methods look for the real car that comes closest to the ideal one.

## The idea

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of a solution $x \in X$, $Y = f(X)$, and $Y_N$ is the set of nondominated points.

**Definition.** The ideal point is $y^I = (y^I_1, \ldots, y^I_p)$ with

$$y^I_i = \inf_{x \in X} f_i(x) = \inf_{y \in Y} y_i, \qquad i = 1, \ldots, p.$$

Some authors define it with $Y_N$ instead of $Y$. The two agree when $Y$ is compact and not empty: for each $y \in Y$ there is then a $\hat{y} \in Y_N$ with $\hat{y} \leqq y$ (see [Pareto optimality](/pareto-optimality/)), so the infimum over $Y_N$ is not larger than the infimum over $Y$, and it is not smaller because $Y_N \subseteq Y$.

**A utopia point** is a point $y^U = y^I - \varepsilon \mathbf{1}$ for a small $\varepsilon > 0$, where $\mathbf{1} = (1, \ldots, 1)$. It is strictly better than every point of $Y$ in every objective. The theorem of the [weighted Tchebycheff method](/weighted-tchebycheff-method/) needs such a point, because the weights $1/(\hat{y}_i - y^U_i)$ must be finite.

**Properties.**

1. $y^I \leqq y$ for each $y \in Y$, and so for each point of the front.
2. If $y^I \in Y$, then $Y_N = \{ y^I \}$. *Proof.* For $y \in Y$ with $y \ne y^I$, we have $y^I \leqq y$ by property 1, so $y^I \prec y$ and $y$ is dominated. The point $y^I$ itself is not dominated, because no $y \in Y$ has a coordinate below $y^I$. $\square$ So an attainable ideal point means that the objectives do not conflict.
3. Each coordinate $y^I_i$ is attained by a weakly Pareto optimal point when the minimum of $f_i$ exists, and by a Pareto optimal point when one takes a lexicographic minimizer, which minimizes $f_i$ first and then the other objectives in turn.

**Computation.** The ideal point needs $p$ single-objective problems $\min_{x \in X} f_i(x)$. Each one is as hard as the single-objective version of the problem: a linear program for a [multi-objective linear program](/multi-objective-linear-programming/), a shortest path for the [multi-objective shortest path](/multi-objective-shortest-path/). For a finite list of $N$ vectors it costs $p (N - 1)$ comparisons. This is in contrast to the [nadir point](/nadir-point/), which needs the front and is hard to compute for $p \ge 3$.

**Uses.**

- **Normalization.** With the nadir point, the map $y_i \mapsto (y_i - y^I_i) / (y^N_i - y^I_i)$ sends the front into $[0, 1]^p$, so objectives in different units become comparable.
- **Reference point.** The weighted Tchebycheff method minimizes $\max_i w_i (f_i(x) - y^U_i)$, and compromise programming minimizes a distance $\| f(x) - y^I \|$. Both look for the attainable point nearest to the ideal.
- [Normal boundary intersection](/normal-boundary-intersection/) and [MOEA/D](/moea-d/) shift the objective space by $y^I$, so that the minimizers of the single objectives span a simplex.

## Examples

**A finite set.** For the images $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$, the least first entry is $2$, at $a$, and the least second entry is $1$, at $g$. So $y^I = (2, 1)$. No image equals $(2, 1)$, so the ideal point is not attainable, and the front $\{a, b, d, e, g\}$ has more than one point.

**A continuous problem.** For $f_1(x) = x^2$ and $f_2(x) = (x - 2)^2$ on $\mathbb{R}$, each objective alone has the minimum 0, at $x = 0$ and at $x = 2$. So $y^I = (0, 0)$, and no solution attains it. The squared Euclidean distance from $f(x)$ to $y^I$ is $x^4 + (x - 2)^4$. Its derivative $4x^3 + 4(x - 2)^3$ is zero only where $x = 2 - x$, so the front point nearest to the ideal point is $(1, 1)$, at $x = 1$, at distance $\sqrt{2}$.

**Attainable ideal point.** Minimize $f_1(x) = x^2$ and $f_2(x) = |x|$ over $x \in [-1, 1]$. Both are minimal at $x = 0$, so $y^I = (0, 0) \in Y$ and the front is the single point $(0, 0)$.

**An infimum that is not a minimum.** For $X = (0, 1]$ and $f(x) = (x, 1/x)$, the first entry of the ideal point is $\inf x = 0$, which no solution attains. The second is $\min 1/x = 1$, at $x = 1$. Every point is Pareto optimal here, and $y^I = (0, 1)$.

## Where it is used

- The [weighted Tchebycheff method](/weighted-tchebycheff-method/) uses a utopia point as its reference.
- The [achievement scalarizing function](/achievement-scalarizing-function/) and the [reference point method](/reference-point-method/) measure the distance from a reference point, which is often set relative to the ideal point.
- [Normal boundary intersection](/normal-boundary-intersection/) shifts the objectives by the ideal point and builds the convex hull of the individual minima.
- The [nadir point](/nadir-point/) and the ideal point together normalize the objectives, for example in [NSGA-III](/nsga-iii/) and [MOEA/D](/moea-d/).
- The [hypervolume indicator](/hypervolume-indicator/) is often computed in the box between them.

## References
