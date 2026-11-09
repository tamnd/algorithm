---
tag: W6H00E
kind: definition
slug: subdifferential
name: Subdifferential
aliases:
- subdifferential set
- convex subdifferential
area: optimization/convex-optimization
level: core
summary: The set ∂f(x) of all subgradients of a convex function f at x. It is closed and convex, and 0 ∈ ∂f(x) exactly when x minimizes f.
prereqs: [subgradient]
see_also: [convex-function, supporting-hyperplane-theorem, proximal-operator, kkt-conditions, convex-conjugate, lasso-regression, support-function, fenchel-duality]
sources:
  - book: isbn:9780691015866
    title: R. Tyrrell Rockafellar, Convex Analysis, Princeton University Press, 1970 (Princeton Landmarks in Mathematics edition, 1997)
    locator: Section 23, The subdifferential of a convex function (directional derivatives, the sum and composition rules), and Section 24 (monotonicity)
  - book: isbn:9783540422051
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Fundamentals of Convex Analysis, Springer, 2001
    locator: Chapter D, Subdifferentials of finite convex functions (calculus rules, the max rule)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 3, Subgradients (subdifferential calculus, optimality conditions with the normal cone)
---

The subdifferential $\partial f(x)$ of a [convex function](/convex-function/) $f$ at a point $x$ is the set of all [subgradients](/subgradient/) of $f$ at $x$. It is a closed convex set. It is the single point $\{\nabla f(x)\}$ where $f$ is differentiable, and a larger set at a kink. The condition $0 \in \partial f(x)$ characterizes minimizers, and calculus rules for $\partial$ turn this condition into the optimality conditions of nonsmooth problems such as the lasso.

## Definition

Let $f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$. For $x \in \operatorname{dom} f$,

$$\partial f(x) = \{ g \in \mathbb{R}^n : f(y) \ge f(x) + g^T (y - x) \text{ for all } y \},$$

and $\partial f(x) = \emptyset$ for $x \notin \operatorname{dom} f$. The map $x \mapsto \partial f(x)$ is a set-valued map from $\mathbb{R}^n$ to subsets of $\mathbb{R}^n$.

For a convex set $C$, the *indicator* $I_C$ is $0$ on $C$ and $+\infty$ outside. Its subdifferential at $x \in C$ is the *normal cone*

$$N_C(x) = \partial I_C(x) = \{ g : g^T (y - x) \le 0 \text{ for all } y \in C \}.$$

The nonzero elements of $N_C(x)$ are the normals of the supporting hyperplanes of $C$ at $x$.

### Basic properties

**Theorem 1 (closed and convex).** For each $x$, $\partial f(x)$ is a closed convex set.

*Proof.* For fixed $y$, the set $\{g : f(y) \ge f(x) + g^T (y - x)\}$ is a closed half-space, or all of $\mathbb{R}^n$ if $y = x$ or $f(y) = +\infty$. $\partial f(x)$ is the intersection of these sets over all $y$. An intersection of closed convex sets is closed and convex. $\square$

**Theorem 2 (bounded near interior points).** Let $f$ be convex, $r > 0$, and assume that $f(y) \le M$ for all $y$ with $\lVert y - x \rVert \le r$. Then every $g \in \partial f(x)$ has

$$\lVert g \rVert \le \frac{M - f(x)}{r}.$$

*Proof.* Let $g \in \partial f(x)$ with $g \ne 0$, and put $y = x + r g / \lVert g \rVert$. Then $M \ge f(y) \ge f(x) + g^T (y - x) = f(x) + r \lVert g \rVert$. $\square$

A convex function is bounded above near each point of $\operatorname{int} \operatorname{dom} f$: such a point lies in the interior of a simplex with vertices in $\operatorname{dom} f$, and on that simplex $f$ is at most the largest vertex value, by the definition of convexity. With Theorem 1 of the [subgradient](/subgradient/) page, $\partial f(x)$ is nonempty, convex and compact at each interior point of the domain.

**Theorem 3 (monotonicity).** If $g \in \partial f(x)$ and $h \in \partial f(y)$, then $(g - h)^T (x - y) \ge 0$.

*Proof.* Add $f(y) \ge f(x) + g^T (y - x)$ and $f(x) \ge f(y) + h^T (x - y)$, and cancel $f(x) + f(y)$: $0 \ge (g - h)^T (y - x)$. $\square$

In one variable, monotonicity says that the subdifferential is a nondecreasing "staircase": the derivative is nondecreasing, and at a kink it fills the vertical gap between the left and right derivatives.

**Theorem 4 (Fermat's rule).** $x^*$ minimizes $f$ if and only if $0 \in \partial f(x^*)$. The proof is on the [subgradient](/subgradient/) page.

### Calculus rules

The following rules hold for proper convex functions. The inclusions marked $\supseteq$ hold with no further assumption, and they follow by adding or composing subgradient inequalities. The equalities need a constraint qualification. Proofs are in Rockafellar Section 23 and Hiriart-Urruty and Lemaréchal Chapter D.

- **Scaling.** $\partial (\alpha f)(x) = \alpha\, \partial f(x)$ for $\alpha > 0$.
- **Sum.** $\partial (f_1 + f_2)(x) \supseteq \partial f_1(x) + \partial f_2(x)$, with equality if $\operatorname{ri} \operatorname{dom} f_1 \cap \operatorname{ri} \operatorname{dom} f_2 \ne \emptyset$, in particular if one of the functions is finite everywhere.
- **Affine composition.** For $h(x) = f(Ax + b)$, $\partial h(x) \supseteq A^T \partial f(Ax + b)$, with equality if the range of $A x + b$ meets $\operatorname{ri} \operatorname{dom} f$.
- **Pointwise maximum.** For finite convex $f_1, \dots, f_m$ and $f = \max_i f_i$, $\partial f(x) = \operatorname{conv} \bigcup_{i \in I(x)} \partial f_i(x)$, where $I(x) = \{i : f_i(x) = f(x)\}$ is the set of active indices.
- **Constrained minimum.** If $f$ is finite everywhere and $C$ is a nonempty convex set, then $x^*$ minimizes $f$ over $C$ if and only if $0 \in \partial f(x^*) + N_C(x^*)$. This is Fermat's rule for $f + I_C$ with the sum rule. When $C$ is given by convex inequalities with a [Slater point](/slater-condition/), $N_C(x^*)$ is the cone spanned by the gradients of the active constraints, and the rule becomes the [KKT conditions](/kkt-conditions/).
- **Directional derivative.** For $x \in \operatorname{int} \operatorname{dom} f$ and each $d$, $f'(x; d) = \lim_{t \to 0^+} (f(x + t d) - f(x)) / t = \max_{g \in \partial f(x)} g^T d$. So $f'(x; \cdot)$ is the [support function](/support-function/) of $\partial f(x)$.
- **Conjugate.** For a closed proper convex $f$, $g \in \partial f(x)$ if and only if $x \in \partial f^*(g)$, where $f^*$ is the [convex conjugate](/convex-conjugate/).

## Examples and non-examples

- **Absolute value.** $\partial \lvert x \rvert = \{-1\}$ for $x < 0$, $[-1, 1]$ at $x = 0$, and $\{1\}$ for $x > 0$.
- **The $\ell_1$ norm.** By the sum rule, $\partial \lVert x \rVert_1$ is the box of vectors $g$ with $g_i = \operatorname{sign}(x_i)$ where $x_i \ne 0$ and $g_i \in [-1, 1]$ where $x_i = 0$.
- **The Euclidean norm.** $\partial \lVert x \rVert_2 = \{x / \lVert x \rVert_2\}$ for $x \ne 0$, and the closed unit ball at $x = 0$.
- **A maximum of affine functions.** For $f(x) = \max(x_1, x_2)$ at a point with $x_1 = x_2$, the max rule gives the segment between $(1, 0)$ and $(0, 1)$.
- **Theorem 2 can be tight.** Let $f(x) = \lvert x_1 \rvert + 2 \lvert x_2 \rvert$ and $x = 0$. Then $\partial f(0) = [-1, 1] \times [-2, 2]$, and its largest norm is $\sqrt{5}$, at $(\pm 1, \pm 2)$. On the unit ball the maximum of $f$ is $M = \max_\phi (\lvert \cos\phi \rvert + 2 \lvert \sin\phi \rvert) = \sqrt{5}$. With $r = 1$ and $f(0) = 0$, the bound of Theorem 2 is $\sqrt{5}$, which is reached.
- **Soft thresholding.** Let $\lambda > 0$ and $a \in \mathbb{R}$, and minimize $\frac{1}{2}(x - a)^2 + \lambda \lvert x \rvert$. By the sum rule and Fermat's rule, $x^*$ is optimal if and only if $0 \in x^* - a + \lambda\, \partial \lvert x^* \rvert$. For $\lvert a \rvert \le \lambda$, $x^* = 0$ works because $a \in [-\lambda, \lambda]$. For $\lvert a \rvert > \lambda$, $x^* = a - \lambda \operatorname{sign}(a)$. For $\lambda = 1$: $a = 3$ gives $x^* = 2$, since $0 = 2 - 3 + 1$; $a = 0.5$ gives $x^* = 0$, since $0 \in -0.5 + [-1, 1]$; and $a = -1.2$ gives $x^* = -0.2$. This map is the [proximal operator](/proximal-operator/) of $\lambda \lvert \cdot \rvert$, and it solves [lasso](/lasso-regression/) problems coordinate by coordinate.
- **Normal cone of a box.** For $C = [0, 1]^2$ and $x = (1, 1)$, $N_C(x) = \{(\alpha, \beta) : \alpha, \beta \ge 0\}$. At $(1, 0.5)$ it is the ray $\{(\alpha, 0) : \alpha \ge 0\}$, and at an interior point it is $\{0\}$.
- **Unbounded at the boundary of the domain.** For $I_{[0, 1]}$, the subdifferential at 0 is $(-\infty, 0]$. Theorem 2 does not apply, because $f$ is not bounded on any ball around 0.
- **Empty at the boundary of the domain.** For $f(x) = -\sqrt{x}$ on $[0, \infty)$, $\partial f(0) = \emptyset$.
- **The sum rule needs a qualification.** Let $f_1(x) = -\sqrt{x}$ for $x \ge 0$ and $+\infty$ otherwise, and $f_2 = I_{(-\infty, 0]}$. Then $f_1 + f_2 = I_{\{0\}}$, and $\partial (f_1 + f_2)(0) = \mathbb{R}$. But $\partial f_1(0) = \emptyset$, so $\partial f_1(0) + \partial f_2(0) = \emptyset$. The relative interiors of the domains are $(0, \infty)$ and $(-\infty, 0)$, which do not meet.
- **Non-example: a nonconvex function.** For $f(x) = -\lvert x \rvert$, the convex subdifferential at 0 is empty, although 0 is a local maximum and $f$ is Lipschitz. The Clarke generalized gradient there is $[-1, 1]$.

## Related definitions

- A [subgradient](/subgradient/) is an element of $\partial f(x)$.
- The normal cone $N_C(x)$ is the subdifferential of the indicator of $C$. It contains the normals of the [supporting hyperplanes](/supporting-hyperplane-theorem/) of $C$ at $x$.
- A set-valued map $T$ is *monotone* if $(g - h)^T (x - y) \ge 0$ for $g \in T(x)$, $h \in T(y)$. Theorem 3 says that $\partial f$ is monotone. For closed proper convex $f$ it is maximal monotone, and the resolvent $(I + \lambda \partial f)^{-1}$ is the [proximal operator](/proximal-operator/) of $\lambda f$.
- The $\varepsilon$-subdifferential $\partial_\varepsilon f(x)$ is the set of $\varepsilon$-subgradients. It is used by [bundle methods](/bundle-method/).

## References
