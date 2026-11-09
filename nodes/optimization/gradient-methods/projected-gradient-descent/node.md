---
tag: XQJ388
kind: algorithm
slug: projected-gradient-descent
name: Projected gradient descent
aliases:
- projected gradient method
- gradient projection method
- projected subgradient method
area: optimization/gradient-methods
level: core
summary: Gradient step followed by Euclidean projection back onto the feasible convex set.
solves: [constrained-smooth-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, g: the cost of one gradient of f, p: the cost of one projection onto C, ε: "the target accuracy f(x_k) - f* ≤ ε", R: "the distance from x_0 to a minimizer", β: "the smoothness constant L_f of f (the step is 1/L_f)"}
  time: {worst: O(k (g + p + n))}
  space: {extra: Θ(n)}
  steps: {worst: "⌈β R^2 / (2ε)⌉"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1964
  people: [A. A. Goldstein, E. S. Levitin, Boris Polyak]
  note: Goldstein (1964) and Levitin and Polyak (1966) proposed the gradient step followed by a projection onto a convex set.
prereqs: [gradient-descent, constrained-smooth-minimization, convex-set]
see_also: [proximal-gradient-method, fista, mirror-descent, subgradient, quadratic-programming, kkt-conditions, portfolio-optimization, gradient-descent-convergence-theorem]
sources:
  - paper: doi:10.1090/S0002-9904-1964-11178-2
    title: A. A. Goldstein, Convex programming in Hilbert space, Bulletin of the American Mathematical Society 70(5), 1964
    locator: pages 709 to 710, the gradient projection iteration
  - paper: doi:10.1016/0041-5553(66)90114-5
    title: E. S. Levitin and B. T. Polyak, Constrained minimization methods, USSR Computational Mathematics and Mathematical Physics 6(5), 1966
    locator: pages 1 to 50, the gradient projection method
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 3.1 (projected subgradient descent) and Section 3.2 (gradient descent for smooth functions over a convex set)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 8 (the projected subgradient method) and Chapter 10 (the proximal gradient method, with the projected gradient method as the case of an indicator)
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Chapter 2, Section 2.2 (minimization over simple sets and the gradient mapping)
  - paper: doi:10.1145/1390156.1390191
    title: John Duchi, Shai Shalev-Shwartz, Yoram Singer and Tushar Chandra, Efficient projections onto the l1-ball for learning in high dimensions, ICML 2008
    locator: Section 3, projection onto the simplex by sorting in O(n log n)
  - paper: doi:10.1137/0108011
    title: J. B. Rosen, The gradient projection method for nonlinear programming, Part I, Linear constraints, Journal of the Society for Industrial and Applied Mathematics 8(1), 1960
    locator: pages 181 to 217, projection of the gradient onto the active constraints
---

Projected gradient descent minimizes a function $f$ over a closed [convex set](/convex-set/) $C$. Each step takes a [gradient descent](/gradient-descent/) step and then replaces the result by the nearest point of $C$, its Euclidean projection. For a convex $f$ with an $L_f$-Lipschitz gradient ([smoothness](/smoothness/)) and the step $1/L_f$, it has the same guarantees as unconstrained gradient descent: $f(x_k) - f^* \le L_f\lVert x_0 - x^*\rVert^2/(2k)$, and a linear rate when $f$ is strongly convex. With a [subgradient](/subgradient/) in place of the gradient, it is the projected subgradient method for nonsmooth $f$.

## In plain words

You want the lowest point of a valley, but you must stay inside a fenced field. Take a normal downhill step. If the step takes you over the fence, walk straight back to the nearest point inside the field. Then repeat.

This is useful when it is easy to find the nearest point of the field, for example when the field is a box, a ball or the set of probability vectors. The method then costs almost the same as plain gradient descent, and it is as fast.

## The problem

The input is a [constrained smooth minimization](/constrained-smooth-minimization/) problem: minimize $f(x)$ over $x \in C$, where $C \subseteq \mathbb{R}^n$ is nonempty, closed and convex, and $f$ is convex and differentiable with an $L_f$-Lipschitz gradient. A minimizer $x^*$ exists, and $f^* = f(x^*)$. The method needs an oracle for $\nabla f$ and for the projection

$$P_C(v) = \operatorname*{argmin}_{z \in C} \lVert z - v\rVert.$$

Notation: $R = \lVert x_0 - x^*\rVert$, $\mu \ge 0$ is the strong convexity constant of $f$, $\kappa = L_f/\mu$, and $\varepsilon$ is the target accuracy. For the subgradient version, $f$ is only convex and each subgradient has norm at most $G$.

## The algorithm

```pseudo id=main
PROJECTED-GD(∇f, P_C, x₀, t, K)        ▷ t_k ≤ 1/L_f for smooth f
L1  x ← P_C(x₀)                        ▷ start inside C
L2  for k ← 0 to K − 1 do
L3      y ← x − t_k ∇f(x)              ▷ a gradient step
L4      x ← P_C(y)                     ▷ back to the nearest point of C
L5  return x
```

The projection has a closed form for many sets:

| set $C$ | $P_C(v)$ | cost |
|---|---|---|
| box $\{l \le x \le u\}$ | clip each $v_i$ to $[l_i, u_i]$ | $O(n)$ |
| ball $\{\lVert x - c\rVert \le r\}$ | $c + r(v - c)/\max(r, \lVert v - c\rVert)$ | $O(n)$ |
| probability simplex | $\max(v_i - \theta, 0)$, with $\theta$ such that the entries sum to $1$ | $O(n \log n)$ by sorting |
| affine set $\{Ax = b\}$ | $v - A^\top(AA^\top)^{-1}(Av - b)$ | one linear solve |

For a general polyhedron the projection is itself a [quadratic program](/quadratic-programming/), and the method is then a poor choice.

## Example

Minimize $f(x) = \frac{1}{2}x^\top Qx - c^\top x$ with $Q = \begin{pmatrix} 2 & 1 \\ 1 & 2\end{pmatrix}$ and $c = (3, -1)$ over the box $[0, 1]^2$. The eigenvalues of $Q$ are $1$ and $3$, so $L_f = 3$ and $t = 1/3$. The unconstrained minimizer $Q^{-1}c = (7/3, -5/3)$ is outside the box. The constrained minimizer is $x^* = (1, 0)$ with $f^* = -2$: there $\nabla f(x^*) = (-1, 2)$, which points out of the box at the upper bound of $x_1$ and at the lower bound of $x_2$, as the [KKT conditions](/kkt-conditions/) require. Start at $x_0 = (0, 1)$, so $R^2 = 2$.

| $k$ | $\nabla f(x_k)$ | $y = x_k - \nabla f(x_k)/3$ | $x_{k+1} = P_C(y)$ | $f(x_{k+1}) - f^*$ | bound $L_fR^2/(2(k+1))$ |
|---|---|---|---|---|---|
| 0 | $(-2, 3)$ | $(0.66667, 0)$ | $(0.66667, 0)$ | 0.44444 | 3.0 |
| 1 | $(-1.66667, 1.66667)$ | $(1.22222, -0.55556)$ | $(1, 0)$ | 0 | 1.5 |

The gap at $x_0$ is $4$. At $k = 1$ both coordinates leave the box and are clipped back, and the method lands exactly on $x^*$. Finite termination of this kind is common when $x^*$ is a vertex of a box, but the theory gives only the bound in the last column.

## Correctness

The key fact is the obtuse angle property of the projection: $\langle v - P_C(v), z - P_C(v)\rangle \le 0$ for every $z \in C$. It shows that $P_C$ does not increase distances, and that $x^*$ is a fixed point: $x^* = P_C(x^* - t\nabla f(x^*))$ exactly when $\langle \nabla f(x^*), z - x^*\rangle \ge 0$ for all $z \in C$, which is the optimality condition. Combined with the descent lemma, the obtuse angle property gives the one-step inequality

$$f(x_{k+1}) \le f(z) + \frac{1}{2t}\Big((1 - \mu t)\lVert x_k - z\rVert^2 - \lVert x_{k+1} - z\rVert^2\Big) \quad \text{for all } z \in C.$$

The choice $z = x_k$ gives monotone decrease, and $z = x^*$ gives a telescoping sum. The full proofs are below.

## Complexity

Each iteration costs one gradient, one projection and $O(n)$ vector work. The memory is $\Theta(n)$.

- **Smooth convex.** With $t = 1/L_f$, $f(x_k) - f^* \le L_fR^2/(2k)$, so $\lceil L_fR^2/(2\varepsilon)\rceil$ iterations give accuracy $\varepsilon$.
- **Strongly convex.** With $t = 1/L_f$, $\lVert x_k - x^*\rVert^2 \le (1 - 1/\kappa)^k R^2$, so $O(\kappa\log(R^2/\varepsilon))$ iterations give $\lVert x_k - x^*\rVert^2 \le \varepsilon$.
- **Nonsmooth convex (projected subgradient).** With $\lVert g_k\rVert \le G$, $\min_{k<K} f(x_k) - f^* \le (R^2 + G^2\sum_k t_k^2)/(2\sum_k t_k)$. The constant step $R/(G\sqrt{K})$ gives $RG/\sqrt{K}$, so $O(R^2G^2/\varepsilon^2)$ iterations.

These rates match those of unconstrained gradient descent, and the [first-order lower bound](/first-order-lower-bound/) applies in the same way. The cost of the projection $p$ decides whether the method is practical.

## Properties

- **Feasible iterates.** Every $x_k$ with $k \ge 0$ lies in $C$, so the method can stop at any time with a feasible point.
- **Monotone and Fejér monotone.** For smooth $f$ and $t \le 1/L_f$, $f(x_k)$ and $\lVert x_k - x^*\rVert$ never increase. The subgradient version has neither property, which is why its bound is on the best iterate.
- **Stopping test.** The gradient mapping $G_t(x) = (x - P_C(x - t\nabla f(x)))/t$ is zero exactly at minimizers. Use $\lVert G_t(x_k)\rVert$, not $\lVert\nabla f(x_k)\rVert$, which need not be zero at $x^*$.
- **A special case.** It is the [proximal gradient method](/proximal-gradient-method/) with $h$ the indicator of $C$, because the [proximal operator](/proximal-operator/) of an indicator is the projection.

## Variants and improvements

- **Acceleration.** [FISTA](/fista/) with $h = \iota_C$ is accelerated projected gradient, with the rate $2L_fR^2/(k+1)^2$.
- **Line search.** Backtracking along the projection arc, $x(t) = P_C(x - t\nabla f(x))$, finds a step when $L_f$ is unknown.
- **Non-Euclidean geometry.** [Mirror descent](/mirror-descent/) replaces the projection by a Bregman projection. On the simplex with the entropy, it needs no sort and for gradients bounded in the max norm its rate depends on $\sqrt{\log n}$ instead of a power of $n$.
- **Rosen's method.** Rosen (1960) projected the gradient onto the subspace of active linear constraints, which is a different method with the same name in older texts.
- **Stochastic version.** Replace $\nabla f$ by an unbiased estimate, as in [stochastic gradient descent](/stochastic-gradient-descent/).

## When to use it

Use it when the projection onto $C$ is cheap: box constraints (bound-constrained least squares, nonnegative least squares), a norm ball (constrained regression, adversarial training), or the simplex (mixture weights, [portfolio optimization](/portfolio-optimization/) without leverage). If the projection needs a solver, use an interior point method, [ADMM](/admm/), or a method that only needs a linear minimization over $C$.

## Pitfalls

- **Projecting the gradient instead of the point.** The method projects $x - t\nabla f(x)$, not $\nabla f(x)$. Projecting only the direction does not keep the iterates feasible for a nonlinear set.
- **Stopping on the gradient norm.** At a boundary minimizer $\nabla f(x^*) \ne 0$. Stop on the gradient mapping or on $\lVert x_{k+1} - x_k\rVert$.
- **A non-Euclidean projection.** The proofs need the Euclidean projection. Clipping in a scaled norm, or an approximate projection that is not the nearest point, can break the obtuse angle property.
- **A nonconvex set.** For a nonconvex $C$ the projection can be set-valued, and the guarantees do not hold.

## Implementations

## History

Goldstein (1964) and Levitin and Polyak (1966) proposed the iteration $x_{k+1} = P_C(x_k - t\nabla f(x_k))$ for convex sets and proved its convergence. Rosen (1960) had earlier used the name for a method that projects the gradient onto active linear constraints. Duchi, Shalev-Shwartz, Singer and Chandra (2008) gave the sort-based projection onto the simplex and the $\ell_1$ ball that many implementations use.

## References
