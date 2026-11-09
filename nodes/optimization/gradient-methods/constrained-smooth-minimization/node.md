---
tag: M6DTKT
kind: problem
slug: constrained-smooth-minimization
name: Constrained smooth minimization
aliases:
- smooth minimization over a convex set
- smooth constrained optimization
area: optimization/gradient-methods
level: core
summary: Minimize a differentiable function over a closed convex set. A point is optimal when no feasible direction is a descent direction; projected and proximal gradient methods keep the unconstrained rates.
prereqs: [unconstrained-smooth-minimization, convex-set]
see_also: [projected-gradient-descent, proximal-gradient-method, fista, kkt-conditions, composite-minimization, interior-point-method, mirror-descent, constrained-optimization]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.2.3, An optimality criterion for differentiable f, and Section 8.1, Projection on a set
  - book: isbn:9781886529052
    title: Dimitri P. Bertsekas, Nonlinear Programming, third edition, Athena Scientific, 2016
    locator: Chapter 2, Optimization over a convex set (the optimality condition, the projection theorem, the gradient projection method and the conditional gradient method)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 10, The proximal gradient method (the projected gradient method as the case of an indicator function, and its rates)
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Chapter 2, Smooth convex optimization (minimization over simple sets and the gradient mapping)
  - paper: doi:10.1090/S0002-9904-1964-11178-2
    title: A. A. Goldstein, Convex programming in Hilbert space, Bulletin of the American Mathematical Society 70(5), 1964
    locator: pages 709 to 710 (the gradient projection method)
  - paper: doi:10.1016/0041-5553(66)90114-5
    title: E. S. Levitin and B. T. Polyak, Constrained minimization methods, USSR Computational Mathematics and Mathematical Physics 6(5), 1966
    locator: pages 1 to 50 (the gradient projection method and the conditional gradient method, with rates)
  - paper: doi:10.1002/nav.3800030109
    title: Marguerite Frank and Philip Wolfe, An algorithm for quadratic programming, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 95 to 110 (the conditional gradient method)
---

Constrained smooth minimization asks for a point $x^*$ that minimizes a differentiable function $f$ over a closed [convex set](/convex-set/) $C \subseteq \mathbb{R}^n$. At an optimal point the gradient need not be zero; the condition is that no feasible direction is a descent direction: $\nabla f(x^*)^\top (x - x^*) \ge 0$ for every $x \in C$. When the Euclidean projection onto $C$ is cheap, [projected gradient descent](/projected-gradient-descent/) and its accelerated form keep the rates of the unconstrained case, $O(L_f R^2/k)$ and $O(L_f R^2/k^2)$ for convex $L_f$-smooth $f$.

## In plain words

You want the lowest point of a landscape, but you must stay inside a fenced region. The region has no dents: the straight path between any two allowed points stays inside.

If the lowest point of the whole landscape is inside the fence, the problem is the same as without a fence. If it is outside, the answer is on the fence, at the spot where the ground slopes down only toward the outside. A simple method takes a downhill step as usual, and if the step leaves the region, it moves back to the nearest allowed point. When "the nearest allowed point" is easy to find, this method is almost as fast as the method without a fence.

## Definition

**Input.** A function $f : \mathbb{R}^n \to \mathbb{R}$ with a first-order oracle for $f(x)$ and $\nabla f(x)$, a nonempty closed convex set $C$, a start point $x_0 \in C$, and an accuracy $\varepsilon > 0$. The set $C$ is given by an oracle too, most often a *projection oracle* that returns

$$\Pi_C(z) = \operatorname*{arg\,min}_{x \in C} \|x - z\|,$$

or a *linear minimization oracle* that returns a point of $\arg\min_{x \in C} g^\top x$.

**Output.** A point $x \in C$ with $f(x) - f^* \le \varepsilon$, where $f^* = \min_{x \in C} f(x)$.

**Existence.** A minimizer exists when $f$ is continuous and $C$ is bounded, or when $f$ is coercive, by the argument of [unconstrained smooth minimization](/unconstrained-smooth-minimization/) applied to the closed set $C \cap \{x : f(x) \le f(x_0)\}$.

**Optimality condition.** Let $f$ be differentiable and $C$ convex.

1. If $x^*$ minimizes $f$ over $C$, then $\nabla f(x^*)^\top (x - x^*) \ge 0$ for all $x \in C$.
2. If $f$ is also [convex](/convex-function/), the condition of 1 is sufficient: each $x^* \in C$ that satisfies it is a minimizer.

*Proof.* For 1, fix $x \in C$. By convexity of $C$, the point $x^* + t(x - x^*)$ lies in $C$ for $t \in [0, 1]$, so $\varphi(t) = f(x^* + t(x - x^*))$ satisfies $\varphi(t) \ge \varphi(0)$. Hence $\varphi'(0) = \nabla f(x^*)^\top (x - x^*) \ge 0$. For 2, convexity gives $f(x) \ge f(x^*) + \nabla f(x^*)^\top (x - x^*) \ge f(x^*)$ for each $x \in C$. $\square$

This condition is a *variational inequality*. If $x^*$ is in the interior of $C$, the condition with $x = x^* \pm t e_i$ gives $\nabla f(x^*) = 0$. In general it says that $-\nabla f(x^*)$ lies in the normal cone $N_C(x^*) = \{v : v^\top (x - x^*) \le 0 \text{ for all } x \in C\}$. When $C$ is described by inequalities and equalities, the normal cone is spanned by the constraint gradients under a constraint qualification, and the condition becomes the [KKT conditions](/kkt-conditions/) with [Lagrange multipliers](/lagrange-multiplier/).

**The projection and the fixed point form.** The projection $p = \Pi_C(z)$ exists and is unique, because $\frac12\|x - z\|^2$ is strongly convex. Apply the optimality condition to it, with gradient $p - z$: $p = \Pi_C(z)$ if and only if $p \in C$ and $(z - p)^\top (x - p) \le 0$ for all $x \in C$. With $z = x^* - \alpha \nabla f(x^*)$ and $p = x^*$, this inequality is $\alpha \nabla f(x^*)^\top (x - x^*) \ge 0$. So, for every $\alpha > 0$,

$$x^* \text{ satisfies the optimality condition} \iff x^* = \Pi_C\big(x^* - \alpha \nabla f(x^*)\big).$$

The *gradient mapping* $G_\alpha(x) = \frac{1}{\alpha}\left(x - \Pi_C(x - \alpha \nabla f(x))\right)$ is zero exactly at such points, and its norm replaces $\|\nabla f(x)\|$ as the measure of stationarity. For $C = \mathbb{R}^n$ it is $\nabla f(x)$.

## Variants

- **Simple sets.** The projection has a closed form or a short algorithm for a box (clip each coordinate), a Euclidean ball (scale $z$ down to the radius), an affine set, the nonnegative orthant, and the probability simplex (sorting, $O(n \log n)$).
- **Polyhedral sets with many constraints.** Projection is itself a [quadratic program](/quadratic-programming/), so methods that use the constraints directly ([interior-point methods](/interior-point-method/), active-set methods) are used.
- **Sets with a linear minimization oracle.** For sets such as the nuclear norm ball, minimizing a linear function is cheaper than projecting, and the conditional gradient method (the Frank-Wolfe method) uses only that oracle.
- **Nonconvex sets or nonconvex $f$.** The optimality condition of 1 is still necessary for convex $C$, and methods aim for points with a small gradient mapping. For nonconvex $C$, projections may not be unique.
- **Composite form.** The problem is the [composite minimization](/composite-minimization/) of $f + \iota_C$, with the indicator $\iota_C(x) = 0$ on $C$ and $+\infty$ outside. The [proximal operator](/proximal-operator/) of $\iota_C$ is $\Pi_C$.

## Examples

- **A box.** Minimize $f(x) = \frac12\left((x_1 - 2)^2 + (x_2 - 2)^2\right)$ over $C = [0, 1]^2$. The unconstrained minimizer $(2, 2)$ is outside. At $x^* = (1, 1)$, $\nabla f(x^*) = (-1, -1)$, and $\nabla f(x^*)^\top (x - x^*) = (1 - x_1) + (1 - x_2) \ge 0$ for every $x \in C$. So $x^* = (1, 1)$ is the minimizer, with $f^* = 1$ and $\nabla f(x^*) \ne 0$. One projected gradient step with $\alpha = 1$ from any point of $C$ goes to $(2, 2)$ and is projected to $(1, 1)$.
- **Nonnegative least squares.** Minimize $\frac12\|Ax - b\|^2$ over $x \ge 0$. The projection is $\max(z, 0)$ coordinatewise, and the optimality condition is $x \ge 0$, $A^\top(Ax - b) \ge 0$, and $x_i (A^\top(Ax - b))_i = 0$ for each $i$.
- **The probability simplex.** Minimizing a smooth loss over $\{x \ge 0, \sum_i x_i = 1\}$ appears in portfolio selection and in mixture weights. [Mirror descent](/mirror-descent/) with the entropy suits this set.
- **A ball.** [Ridge regression](/ridge-regression/) in its constrained form minimizes $\frac12\|Ax - b\|^2$ over $\|x\| \le r$, with $\Pi_C(z) = z \min(1, r/\|z\|)$.

## Known algorithms

| algorithm | oracle for $C$ | rate on convex $L_f$-smooth $f$ |
|---|---|---|
| [projected gradient descent](/projected-gradient-descent/), step $1/L_f$ | projection | $f(x_k) - f^* \le L_f R^2/(2k)$ |
| [FISTA](/fista/) (accelerated projected or proximal gradient) | projection | $f(x_k) - f^* \le 2 L_f R^2/(k+1)^2$ |
| [projected gradient descent](/projected-gradient-descent/) on $\mu$-strongly convex $f$ | projection | linear, factor $1 - \mu/L_f$ per step |
| conditional gradient (Frank-Wolfe) | linear minimization | $O(L_f \operatorname{diam}(C)^2/k)$ |
| [mirror descent](/mirror-descent/) | Bregman projection | geometry-adapted rates |
| [interior-point method](/interior-point-method/), [barrier method](/barrier-method/) | constraint functions and their derivatives | $O(\sqrt{\nu}\log(1/\varepsilon))$ Newton steps for a $\nu$-self-concordant barrier |
| [augmented Lagrangian method](/augmented-lagrangian-method/), [penalty method](/penalty-method/) | constraint functions | reduce to a sequence of unconstrained problems |

The [proximal gradient method](/proximal-gradient-method/) contains projected gradient descent as the case $h = \iota_C$, and its rates are proved there (Beck, Chapter 10).

## Bounds

- **Lower bounds.** The unconstrained problem is the case $C = \mathbb{R}^n$, so the [first-order lower bound](/first-order-lower-bound/) $\Omega(\sqrt{L_f R^2/\varepsilon})$ for convex $f$ and $\Omega(\sqrt{\kappa}\log(1/\varepsilon))$ for strongly convex $f$ hold here too, for methods with a projection oracle.
- **Upper bounds.** FISTA meets them: $O(\sqrt{L_f R^2/\varepsilon})$ projections and gradient calls. The constraint costs one projection per step and does not change the count.
- **Conditional gradient.** The Frank-Wolfe method has the rate $O(1/k)$, slower than FISTA. This is the price of the cheaper linear minimization oracle.

## Reductions

- **To composite minimization.** $\min_{x \in C} f(x) = \min_x f(x) + \iota_C(x)$, and each proximal method applies with $\operatorname{prox}_{\alpha\iota_C} = \Pi_C$.
- **To unconstrained problems.** Penalty and barrier methods replace the constraint by a term that grows near or outside the boundary of $C$, and solve a sequence of [unconstrained smooth minimization](/unconstrained-smooth-minimization/) problems.
- **Equality constraints.** For $C = \{x : Ax = b\}$, write $x = x_0 + Nz$ with the columns of $N$ a basis of the null space of $A$, and minimize $f(x_0 + Nz)$ over all $z$ without constraints.
- **To a variational inequality.** For convex $f$, the problem is the variational inequality with the monotone operator $\nabla f$ over $C$.

## Applications

- [Quadratic programming](/quadratic-programming/) with simple constraints, such as the dual of the support vector machine with box constraints.
- Nonnegative least squares and nonnegative matrix factorization.
- Portfolio selection over the simplex, and other problems with weights that add up to 1.
- Constrained regression ([ridge](/ridge-regression/) and lasso in their constrained forms) and the training of models with norm constraints on the weights.

## References
