---
tag: NQC7CW
kind: concept
slug: convex-envelope
name: Convex envelope
aliases:
- convex hull of a function
- convex minorant
- lower convex envelope
area: optimization/convex-optimization
level: advanced
summary: The largest convex function that lies below a given function. Its epigraph is the convex hull of the epigraph, and its closure is the biconjugate f**.
prereqs: [convex-function, convex-hull]
see_also: [convex-conjugate, convex-relaxation, upper-and-lower-hull, caratheodory-theorem, lasso-regression, global-optimization, epigraph, lp-relaxation]
sources:
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 5 (the convex hull of a function), Section 12 (the closed convex hull as the biconjugate) and Section 17 (Carathéodory's theorem applied to convex hulls of functions)
  - book: isbn:9783540422051
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Fundamentals of Convex Analysis, Springer, 2001
    locator: Chapter B, Convex functions (the closed convex hull of a function), and Chapter E, Conjugacy in convex analysis
  - paper: "Garth P. McCormick, Computability of global solutions to factorable nonconvex programs, Part I, Convex underestimating problems, Mathematical Programming 10, 1976, 147-175"
    locator: convex underestimators of products of bounded variables
---

The convex envelope of a function $f$ is the largest [convex function](/convex-function/) that lies below $f$ everywhere. Its [epigraph](/epigraph/) is the [convex hull](/convex-hull/) of the epigraph of $f$, and its value at $x$ is the smallest average of values of $f$ at points whose average is $x$. The envelope has the same minimum value as $f$, so it is the tightest convex relaxation of a minimization problem, and its closure is the biconjugate $f^{**}$ of the [convex conjugate](/convex-conjugate/).

## In plain words

Draw the graph of a function with several valleys. Stretch a string under the graph so that it touches from below and never bends downward. Where the graph is already bowl-shaped, the string follows it. Where the graph has a hump between two valleys, the string jumps across in a straight line.

The shape of the string is the convex envelope. Its lowest point is as low as the lowest point of the graph. So replacing a hard function by its envelope does not change the best value, and it removes the false valleys. The hard part is that the envelope is often as hard to compute as the original minimum.

## The idea

### Definition

Let $f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$. Its *convex envelope* is

$$\operatorname{conv} f(x) = \sup \{ h(x) : h \text{ convex},\ h \le f \}.$$

A pointwise supremum of convex functions is convex, so $\operatorname{conv} f$ is itself convex and below $f$, and it is the largest such function. If $f$ has no affine minorant, $\operatorname{conv} f$ takes the value $-\infty$, as for $f(x) = -x^2$. The *closed convex envelope* $\overline{\operatorname{conv}} f$ is the largest closed convex function below $f$.

### Convex combinations

**Theorem 1.** For each $x$,

$$\operatorname{conv} f(x) = \inf \left\{ \sum_{i=1}^k \theta_i f(x_i) : k \ge 1,\ \theta_i \ge 0,\ \sum_i \theta_i = 1,\ \sum_i \theta_i x_i = x \right\},$$

and the infimum can be restricted to $k \le n + 2$.

*Proof.* Call the right side $F(x)$.

1. *$F \le f$*: take $k = 1$ and $x_1 = x$.
2. *$F$ is convex.* Let $x, y \in \operatorname{dom} F$, $\theta \in [0, 1]$ and $\varepsilon > 0$. Pick combinations $\sum_i \alpha_i x_i = x$ with $\sum_i \alpha_i f(x_i) \le F(x) + \varepsilon$, and $\sum_j \beta_j y_j = y$ with $\sum_j \beta_j f(y_j) \le F(y) + \varepsilon$. The weights $\theta \alpha_i$ and $(1 - \theta) \beta_j$ give a combination with mean $\theta x + (1 - \theta) y$, so $F(\theta x + (1 - \theta) y) \le \theta F(x) + (1 - \theta) F(y) + \varepsilon$. Let $\varepsilon \to 0$.
3. *$F$ is the largest.* If $h$ is convex and $h \le f$, then for each combination, [Jensen's inequality](/jensens-inequality/) gives $h(x) = h(\sum_i \theta_i x_i) \le \sum_i \theta_i h(x_i) \le \sum_i \theta_i f(x_i)$. So $h \le F$.

By 1 to 3, $F = \operatorname{conv} f$. For the bound on $k$, the point $(x, \sum_i \theta_i f(x_i)) \in \mathbb{R}^{n+1}$ is a convex combination of the points $(x_i, f(x_i))$. By [Carathéodory's theorem](/caratheodory-theorem/) in $\mathbb{R}^{n+1}$, it is a convex combination of at most $n + 2$ of them, with the same mean and the same value. $\square$

A finer argument reduces the bound to $n + 1$ points (Rockafellar, Section 17). In one variable, two points suffice, so $\operatorname{conv} f(x)$ is the lowest chord of $f$ over $x$.

### The minimum is kept

**Theorem 2.** $\inf_x \operatorname{conv} f(x) = \inf_x f(x)$. If $x^*$ minimizes $f$, it also minimizes $\operatorname{conv} f$.

*Proof.* Let $m = \inf f$. The constant function $m$ is convex and below $f$, so $m \le \operatorname{conv} f$. And $\operatorname{conv} f \le f$ gives $\inf \operatorname{conv} f \le m$. If $f(x^*) = m$, then $m \le \operatorname{conv} f(x^*) \le f(x^*) = m$. $\square$

So minimizing $\operatorname{conv} f$, a convex problem, gives the minimum value of $f$. The difficulty has moved into computing $\operatorname{conv} f$, which for general $f$ is as hard as the original problem. Useful [convex relaxations](/convex-relaxation/) are envelopes that have closed forms, as in the examples below.

### The biconjugate

**Theorem 3.** If $f$ is proper and has an affine minorant, then $\overline{\operatorname{conv}} f = f^{**}$.

*Proof.* By Theorems 1 and 3 on the [convex conjugate](/convex-conjugate/) page, $f^{**}$ is closed, convex and below $f$, so $f^{**} \le \overline{\operatorname{conv}} f$. Conversely, $g = \overline{\operatorname{conv}} f$ is closed and convex, it lies above the affine minorant of $f$, so it is proper, and $g \le f$. Conjugation reverses inequalities: $g \le f$ gives $g^* \ge f^*$, which gives $g^{**} \le f^{**}$. By the Fenchel-Moreau theorem, $g^{**} = g$. So $\overline{\operatorname{conv}} f \le f^{**}$. $\square$

Both $f$ and its envelope have the same affine minorants, so $f^* = (\operatorname{conv} f)^*$. In one variable with samples, $f^{**}$ can be computed by applying the discrete Legendre transform twice.

### Computing the envelope of a sampled function

For a function of one variable known at $n$ points $(x_i, f_i)$, and $+\infty$ elsewhere, the envelope is the piecewise linear function through the vertices of the lower convex hull of the points, and $+\infty$ outside $[\min x_i, \max x_i]$. The implementation in `impl/python/convex_envelope.py` computes the hull with the monotone chain in $O(n \log n)$ time, as for the lower part of the [upper and lower hulls](/upper-and-lower-hull/), and evaluates the envelope at a query point by binary search in $O(\log n)$. With rational data it is exact. The tests compare it with the formula of Theorem 1 restricted to pairs of samples, which is exact in one variable.

## Examples

**The double well.** Let $f(x) = \min((x - 1)^2, (x + 1)^2)$. Its envelope is 0 on $[-1, 1]$ and equals $f$ outside. Indeed, 0 is a chord value between the two minimizers $\pm 1$, so $\operatorname{conv} f \le 0$ there; the constant 0 is below $f$, so $\operatorname{conv} f \ge 0$; and outside $[-1, 1]$, $f$ coincides with a convex quadratic that is below $f$ everywhere on that side. Sampling $f$ at the 17 points $x = -2, -\frac{7}{4}, \dots, 2$ gives a lower hull with 10 vertices: the seven samples in $(-1, 1)$, where $f$ has its hump, are dropped. The sampled envelope is $1, \frac{1}{4}, 0, 0, 0, \frac{1}{4}$ at $x = -2, -\frac{3}{2}, -1, 0, \frac{1}{2}, \frac{3}{2}$, while $f(0) = 1$ and $f(\frac{1}{2}) = \frac{1}{4}$.

**McCormick's envelope of a product.** On the square $[0, 1]^2$, the convex envelope of $f(x, y) = xy$ is $\max(0, x + y - 1)$.

- *It is below $f$:* $xy \ge 0$ and $xy - (x + y - 1) = (1 - x)(1 - y) \ge 0$.
- *It is the largest:* let $h$ be convex with $h \le xy$ on the square. If $x + y \le 1$, then $(x, y) = (1 - x - y)(0, 0) + x(1, 0) + y(0, 1)$, and $f$ is 0 at these three corners, so $h(x, y) \le 0$. If $x + y \ge 1$, then $(x, y) = (x + y - 1)(1, 1) + (1 - y)(1, 0) + (1 - x)(0, 1)$, so $h(x, y) \le x + y - 1$.

At the center the envelope is 0, while $f = \frac{1}{4}$. In the same way the concave envelope is $\min(x, y)$. On a general box $[\ell_x, u_x] \times [\ell_y, u_y]$ the envelope is $\max(\ell_y x + \ell_x y - \ell_x \ell_y,\ u_y x + u_x y - u_x u_y)$. These four inequalities are the McCormick relaxation of a bilinear term, used in spatial branch and bound for [global optimization](/global-optimization/).

**Cardinality and the $\ell_1$ norm.** On the box $[-1, 1]^n$, the convex envelope of the number of nonzero entries $\operatorname{card}(x)$ is $\lVert x \rVert_1$. The norm is convex and at most $\operatorname{card}(x)$ on the box, since each $\lvert x_i \rvert \le 1$. For the other direction, round each coordinate independently to $\operatorname{sign}(x_i)$ with probability $\lvert x_i \rvert$ and to 0 otherwise. The result has mean $x$ and expected cardinality $\lVert x \rVert_1$. It has finitely many values, so this is a convex combination, and Theorem 1 gives $\operatorname{conv} \operatorname{card}(x) \le \lVert x \rVert_1$. This is one justification for the $\ell_1$ penalty of the [lasso](/lasso-regression/) as a stand-in for a sparsity constraint. In one variable, the envelope of the function that is 0 at 0 and 1 at $\pm 1$ is $\lvert x \rvert$, for example $\frac{1}{3}$ at $x = \frac{1}{3}$.

**Indicators.** For a set $S$, the envelope of its indicator is the indicator of the convex hull of $S$. Minimizing a linear function over $S$ and over $\operatorname{conv} S$ gives the same value, which is why the [LP relaxation](/lp-relaxation/) over the convex hull of the integer points of an integer program would be exact.

**A function with no convex minorant.** For $f(x) = -x^2$, every convex $h$ below $f$ would have to grow at most like $-x^2$, which no function with finite values can do, so $\operatorname{conv} f \equiv -\infty$.

## Where it is used

- **Global optimization.** Spatial branch and bound relaxes each nonconvex term by its envelope over the current box, as in McCormick's relaxation, and tightens the boxes by branching.
- **Sparse and low-rank recovery.** The $\ell_1$ norm is the envelope of cardinality on a box, and the nuclear norm plays the same role for the rank of a matrix on the spectral-norm unit ball. Both lead to convex problems such as the [lasso](/lasso-regression/).
- **Duality gaps.** For a problem with a separable objective, the Lagrange dual equals the primal problem with each term replaced by its convex envelope. So the duality gap measures the nonconvexity of the terms.
- **Physics and economics.** In thermodynamics, the convex envelope of the free energy explains phase coexistence: a straight segment of the envelope corresponds to a mixture of two phases. In economics, the convex hull of preferences and production sets is used to study markets with nonconvexities.
- **Computational geometry.** The envelope of a sampled function is a lower convex hull, and the [convex hull trick](/convex-hull-trick/) evaluates such envelopes and their conjugates quickly.

## References
