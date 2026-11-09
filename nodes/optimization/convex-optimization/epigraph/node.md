---
tag: 3R5BAA
kind: concept
slug: epigraph
name: Epigraph
aliases:
- supergraph
area: optimization/convex-optimization
level: intro
summary: The set of points on or above the graph of a function. A function is convex exactly when its epigraph is a convex set.
prereqs: [convex-set]
see_also: [convex-function, convex-optimization-problem, subgradient, convex-envelope, supporting-hyperplane-theorem, linear-programming-problem, polyhedron]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 3.1.7 (epigraph), Section 3.2.3 (pointwise maximum), Section 4.1.3 (equivalent problems, with the epigraph form) and Section 6.1 (norm approximation, with Chebyshev approximation)
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 4 (a convex function is defined by a convex epigraph) and Section 7 (closed functions and closed epigraphs)
  - book: isbn:9783540422051
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Fundamentals of Convex Analysis, Springer, 2001
    locator: Chapter B, Section B.1 (epigraph, closed convex functions and their lower semicontinuity)
---

The epigraph of a function $f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ is the set $\operatorname{epi} f = \{(x, t) \in \mathbb{R}^n \times \mathbb{R} : f(x) \le t\}$ of points on or above its graph. It turns a function into a set. A function is a [convex function](/convex-function/) exactly when its epigraph is a [convex set](/convex-set/), and many facts about convex functions are facts about convex sets read through this map. In optimization, the epigraph gives the *epigraph form* of a problem, which moves a hard objective into a constraint.

## In plain words

Draw the graph of a function on paper. Shade everything above the curve, together with the curve itself. The shaded region is the epigraph. If the function is a bowl, the shaded region has no dents: a straight line between two shaded points stays in the shaded region. If the curve has a hump, a line between two points on either side of the hump passes below the curve, so it leaves the shaded region.

Many questions about a function become questions about its shaded region. The lowest point of the function is the lowest point of the region. The tangent lines that stay under the curve are the lines that touch the region from below.

## The idea

We use $n$ for the number of variables. For $f : \mathbb{R}^n \to \overline{\mathbb{R}} = \mathbb{R} \cup \{+\infty\}$,

$$\operatorname{epi} f = \{(x, t) \in \mathbb{R}^{n+1} : x \in \operatorname{dom} f, \ f(x) \le t\}.$$

The function is recovered from its epigraph by $f(x) = \inf\{t : (x, t) \in \operatorname{epi} f\}$, with $\inf \emptyset = +\infty$. The *strict epigraph* uses $f(x) < t$. The *hypograph* $\{(x, t) : t \le f(x)\}$ plays the same role for concave functions.

### Convexity

**Theorem.** A function $f : \mathbb{R}^n \to \overline{\mathbb{R}}$ is convex if and only if $\operatorname{epi} f$ is a convex set.

*Proof.* Assume that $f$ is convex. Take $(x, s)$ and $(y, t)$ in $\operatorname{epi} f$ and $\theta \in [0, 1]$. Then $x, y \in \operatorname{dom} f$, which is convex, and $f(\theta x + (1-\theta) y) \le \theta f(x) + (1 - \theta) f(y) \le \theta s + (1 - \theta) t$. So $\theta (x, s) + (1 - \theta)(y, t) \in \operatorname{epi} f$.

Conversely, assume that $\operatorname{epi} f$ is convex. Take $x, y \in \operatorname{dom} f$ and $\theta \in [0, 1]$. The points $(x, f(x))$ and $(y, f(y))$ are in $\operatorname{epi} f$, so their combination $(\theta x + (1-\theta) y, \ \theta f(x) + (1-\theta) f(y))$ is in $\operatorname{epi} f$. By the definition of the epigraph, $\theta x + (1-\theta)y \in \operatorname{dom} f$ and $f(\theta x + (1 - \theta) y) \le \theta f(x) + (1-\theta) f(y)$. The projection of a convex set on the first $n$ coordinates is convex, so $\operatorname{dom} f$ is convex as well. $\square$

### Closedness

**Theorem.** $\operatorname{epi} f$ is closed if and only if $f$ is lower semicontinuous, that is, $f(x) \le \liminf_{k} f(x_k)$ whenever $x_k \to x$.

*Proof.* Assume that $f$ is lower semicontinuous, and let $(x_k, t_k) \in \operatorname{epi} f$ tend to $(x, t)$. Then $f(x) \le \liminf f(x_k) \le \lim t_k = t$, so $(x, t) \in \operatorname{epi} f$. Conversely, assume that $\operatorname{epi} f$ is closed, let $x_k \to x$, and let $\ell = \liminf f(x_k)$. If $\ell = +\infty$ there is nothing to show. Otherwise take a subsequence with $f(x_{k_j}) \to \ell$. For each real $t > \ell$, the points $(x_{k_j}, t)$ lie in $\operatorname{epi} f$ for large $j$, and they tend to $(x, t)$. So $(x, t) \in \operatorname{epi} f$ and $f(x) \le t$. Since $t > \ell$ is arbitrary, $f(x) \le \ell$. If $\ell = -\infty$ the same argument gives $f(x) \le t$ for each real $t$, which is impossible for a function with values in $\overline{\mathbb{R}}$, so this case does not occur. $\square$

A convex function with a closed epigraph is called *closed*. Closed proper convex functions are the functions that are the supremum of their affine minorants. This is the subject of the [convex conjugate](/convex-conjugate/) and the [convex envelope](/convex-envelope/).

### Operations on functions are operations on sets

- *Pointwise maximum:* $\operatorname{epi}(\max_i f_i) = \bigcap_i \operatorname{epi} f_i$, because $\max_i f_i(x) \le t$ exactly when $f_i(x) \le t$ for each $i$. An intersection of convex sets is convex, so a maximum of convex functions is convex.
- *Infimal convolution:* $(f \,\square\, g)(x) = \inf_y (f(y) + g(x - y))$ has strict epigraph equal to the Minkowski sum of the strict epigraphs of $f$ and $g$.
- *Convex envelope:* the epigraph of the closed [convex envelope](/convex-envelope/) of $f$ is the closed convex hull of $\operatorname{epi} f$.
- *Sublevel sets:* $\{x : f(x) \le \alpha\}$ is the slice of $\operatorname{epi} f$ at height $t = \alpha$, projected to $\mathbb{R}^n$. A slice of a convex set is convex, so the sublevel sets of a convex function are convex. The converse fails, and the functions with convex sublevel sets are the [quasiconvex functions](/quasiconvex-function/).

### Supporting hyperplanes are subgradients

A non-vertical hyperplane $t = f(x_0) + g^T(x - x_0)$ that supports $\operatorname{epi} f$ at $(x_0, f(x_0))$ is exactly a tangent plane that stays below the graph. Its slope $g$ is a [subgradient](/subgradient/) of $f$ at $x_0$. The [supporting hyperplane theorem](/supporting-hyperplane-theorem/) applied to the epigraph shows that a convex function has a subgradient at each interior point of its domain.

### The epigraph form of a problem

The problem "minimize $f_0(x)$ subject to $x \in X$" has the same optimal value and the same optimal $x$ as

$$\text{minimize } t \quad \text{subject to } f_0(x) \le t, \ x \in X,$$

over the variables $(x, t) \in \mathbb{R}^{n+1}$. If $(x^*, t^*)$ solves the second problem then $t^* = f_0(x^*)$, since a larger $t$ could be lowered. The objective is now linear. When $f_0$ is a maximum of simple functions, the constraint $f_0(x) \le t$ splits into one simple constraint for each of them.

## Examples

**The absolute value.** For $f(x) = \lvert x \rvert$, $\operatorname{epi} f = \{(x, t) : -t \le x \le t\}$, a convex cone in the plane bounded by the two rays $t = x$ and $t = -x$ for $t \ge 0$.

**A non-convex function.** For $f(x) = \min(x^2, (x - 2)^2)$, the points $(0, 0)$ and $(2, 0)$ are in the epigraph, but their midpoint $(1, 0)$ is not, because $f(1) = 1 > 0$. So the epigraph is not convex, and neither is $f$.

**A piecewise linear minimax problem.** Minimize $f(x) = \max(2x - 1, \ -x + 2, \ \tfrac12 x)$ over $x \in \mathbb{R}$. The epigraph form is the linear program

$$\text{minimize } t \quad \text{subject to } 2x - 1 \le t, \ -x + 2 \le t, \ \tfrac12 x \le t.$$

Its feasible set is $\operatorname{epi} f$, a polyhedron. The lowest point is where the two lines $t = 2x - 1$ and $t = -x + 2$ meet: $x^* = 1$, $t^* = 1$. The third constraint has $\frac12 \cdot 1 = \frac12 < 1$, so it is not tight. A dual check: the multipliers $\frac13$ and $\frac23$ on the first two constraints give $\frac13 (2x - 1) + \frac23 (-x + 2) = 1$ for every $x$, so $t \ge 1$ on the whole feasible set.

**Chebyshev fitting.** To fit $Ax \approx b$ in the max norm, minimize $\lVert Ax - b \rVert_\infty = \max_i \lvert a_i^T x - b_i \rvert$. The epigraph form gives the linear program: minimize $t$ subject to $-t \le a_i^T x - b_i \le t$ for each row $i$.

**A closed and a non-closed epigraph.** The function that is $1$ for $x \le 0$ and $0$ for $x > 0$ is lower semicontinuous at 0 only if $f(0) \le \liminf_{x \to 0^+} f(x) = 0$. Since $f(0) = 1$, the epigraph misses the limit point $(0, 0)$ of the points $(1/k, 0)$, so it is not closed. Setting $f(0) = 0$ closes it.

## Where it is used

- **Proofs about convex functions.** Separation and support theorems for sets become existence theorems for [subgradients](/subgradient/), for the [convex conjugate](/convex-conjugate/) and for [Lagrangian duality](/lagrangian-duality/).
- **Modeling.** The epigraph form turns maxima, norms and piecewise linear objectives into [linear programs](/linear-programming-problem/) and conic programs, which a solver accepts.
- **Cutting-plane and bundle methods.** These methods build an outer approximation of $\operatorname{epi} f$ by half-spaces from subgradients, and minimize over the approximation. See the [cutting-plane method](/cutting-plane-method/) and the [bundle method](/bundle-method/).
- **Convex relaxation.** The [convex envelope](/convex-envelope/) of a non-convex function comes from the convex hull of its epigraph. It gives lower bounds in the branch and bound methods of [global optimization](/global-optimization/).
- **Interior-point methods.** Conic solvers write a convex constraint $f(x) \le t$ as membership of $(x, t)$ in a closed convex cone, for example the second-order cone for $f(x) = \lVert x \rVert_2$.

## References
