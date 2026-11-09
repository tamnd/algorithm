---
tag: V8N3PJ
kind: algorithm
slug: proximal-point-method
name: Proximal point method
aliases:
- proximal point algorithm
- proximal minimization algorithm
- PPA
area: optimization/convex-optimization
level: advanced
summary: Repeatedly minimize the objective plus a quadratic penalty around the current iterate.
model: real-ram
complexity:
  vars: {k: the number of iterations, n: the number of variables, p: the cost of one evaluation of the proximal map}
  time: {worst: O(k (p + n))}
  space: {extra: O(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1970
  people: [Bernard Martinet, R. Tyrrell Rockafellar, Osman Güler]
  note: Martinet (1970) introduced the method as a regularization of convex minimization. Rockafellar (1976) studied it for maximal monotone operators, with inexact steps, and showed that the method of multipliers is the proximal point method on the dual. Güler (1991) proved the O(1/k) rate and gave an accelerated O(1/k^2) version.
prereqs: [proximal-operator, convex-function]
see_also: [augmented-lagrangian-method, admm, bundle-method, proximal-gradient-method, gradient-descent, subgradient, mirror-descent, bregman-divergence]
sources:
  - paper: doi:10.1137/0314056
    title: R. Tyrrell Rockafellar, Monotone operators and the proximal point algorithm, SIAM Journal on Control and Optimization 14(5), 1976
    locator: pages 877 to 898 (convergence for maximal monotone operators with inexact steps, and finite convergence in the polyhedral case)
  - paper: doi:10.1287/moor.1.2.97
    title: R. Tyrrell Rockafellar, Augmented Lagrangians and applications of the proximal point algorithm in convex programming, Mathematics of Operations Research 1(2), 1976
    locator: pages 97 to 116 (the method of multipliers as the proximal point method on the dual)
  - paper: doi:10.1137/0329022
    title: Osman Güler, On the convergence of the proximal point algorithm for convex minimization, SIAM Journal on Control and Optimization 29(2), 1991
    locator: pages 403 to 419 (the bound f(x_k) - f* <= ||x_0 - x*||^2 / (2 sum of the step parameters), and an accelerated version)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 6 (the proximal operator and its properties), Chapter 10 (the proximal gradient method, which is the proximal point method when the smooth part is zero)
  - book: isbn:9783540568520
    title: Jean-Baptiste Hiriart-Urruty and Claude Lemaréchal, Convex Analysis and Minimization Algorithms II, Springer, 1993
    locator: Chapter XV (primal forms of bundle methods, with the Moreau-Yosida regularization and the proximal point view)
---

The proximal point method minimizes a convex function $f$ by a sequence of easier problems. At each step it adds the quadratic term $\|z - x_k\|^2/(2\lambda)$ to $f$ and moves to the minimizer, which is the [proximal map](/proximal-operator/) $\operatorname{prox}_{\lambda f}(x_k)$. Each step decreases $f$, and after $k$ steps $f(x_k) - f^* \le \|x_0 - x^*\|^2/(2\lambda k)$ for every $\lambda > 0$, with no smoothness assumption at all. The method is rarely run in its plain form, because each step is as hard as a regularized version of the original problem. Its value is as a frame: the [augmented Lagrangian method](/augmented-lagrangian-method/) is the proximal point method on the dual, [ADMM](/admm/) and the [bundle method](/bundle-method/) are inexact forms of it, and the [proximal gradient method](/proximal-gradient-method/) reduces to it when the smooth part is zero.

## In plain words

To find the lowest point of a valley, the method ties itself to its current position with an elastic band. Then it asks: where is the lowest point if I count both the height of the valley and the pull of the band? It moves there, ties the band again, and repeats.

The band keeps each move short and safe, so the method never jumps over the bottom, even when the ground has sharp corners or very steep walls. A weak band allows long moves, and the method gets close in a few steps. A strong band makes each step easy to compute but slow. The direction of each move also tells how steep the ground is at the new point, so the method knows how far it still is from the bottom.

## The problem

Minimize a closed, proper, [convex function](/convex-function/) $f: \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$. The value $+\infty$ allows constraints: $f$ can be the objective plus the indicator of a convex set. The method needs the proximal map of $f$, a step parameter $\lambda > 0$, a start $x_0$ and a tolerance $\varepsilon \ge 0$. For the rate bound, $f$ must have a minimizer $x^*$. The output is a point $x_k$ and a [subgradient](/subgradient/) $g_k \in \partial f(x_k)$ with $\|g_k\| \le \varepsilon$.

## The algorithm

```pseudo id=main
PROXIMAL-POINT(f, x, λ, ε)
L1  repeat
L2      x⁺ ← argmin_z  f(z) + ‖z − x‖² / (2λ)       ▷ the proximal map of λf at x
L3      g ← (x − x⁺) / λ                             ▷ g ∈ ∂f(x⁺)
L4      x ← x⁺
L5  until ‖g‖ ≤ ε
L6  return x
```

Line L2 has exactly one solution, because the function in it is strongly convex. Its optimality condition $0 \in \partial f(x^+) + (x^+ - x)/\lambda$ says that the vector $g$ of line L3 is a subgradient of $f$ at the new point. So the step is an implicit (backward) subgradient step, $x^+ = x - \lambda g$ with $g \in \partial f(x^+)$, while [gradient descent](/gradient-descent/) is the explicit (forward) step with the gradient at the old point. The parameter $\lambda$ can change from step to step.

## Example

Take $f(x) = \tfrac12(x_1^2 + 10x_2^2)$, $\lambda = 1$ and $x_0 = (1, 1)$. Line L2 solves $(I + \lambda Q)x^+ = x$, so $x^+ = (x_1/2, x_2/11)$, and $x_k = (2^{-k}, 11^{-k})$. The bound is $\|x_0\|^2/(2\lambda k) = 1/k$.

| $k$ | $x_k$ | $f(x_k)$ | bound $1/k$ |
|---|---|---|---|
| 0 | (1, 1) | 5.5 | |
| 1 | (0.5, 0.0909) | 0.16632 | 1 |
| 2 | (0.25, 0.00826) | 0.031592 | 0.5 |
| 3 | (0.125, 0.000751) | 0.0078153 | 0.333 |
| 4 | (0.0625, 0.0000683) | 0.0019531 | 0.25 |

The steep coordinate $x_2$ shrinks fastest. Gradient descent with the same step $1$ would multiply $x_2$ by $1 - 10 = -9$ at each step and diverge, because its step must be less than $2/10$. The proximal step is stable for every $\lambda$.

A nonsmooth example: for $f(x) = |x|$, the proximal map moves $x$ toward $0$ by $\lambda$, and stops at $0$. So the method reaches the exact minimizer after $\lceil |x_0|/\lambda \rceil$ steps.

## Correctness

The proof rests on the subgradient of line L3. Put $z = x_k$ in the subgradient inequality at $x_{k+1}$ to get $f(x_{k+1}) \le f(x_k) - \lambda\|g\|^2$, so the values never increase. Put $z = x^*$ to get

$$\lambda(f(x_{k+1}) - f^*) \le \tfrac12\|x_k - x^*\|^2 - \tfrac12\|x_{k+1} - x^*\|^2.$$

The distance to $x^*$ never grows, and the sum over $k$ steps telescopes to $\lambda k(f(x_k) - f^*) \le \tfrac12\|x_0 - x^*\|^2$. When line L5 stops, $f(x) - f^* \le \|g\|\,\|x - x^*\| \le \varepsilon\|x_0 - x^*\|$. The full proof is below.

## Complexity

**Iterations.** Let $f$ be closed, proper and convex with a minimizer $x^*$. Then for each $k \ge 1$,

$$f(x_k) - f^* \le \frac{\|x_0 - x^*\|^2}{2\lambda k}.$$

With step parameters $\lambda_j$ that change, the same proof gives $\|x_0 - x^*\|^2/(2\sum_{j<k}\lambda_j)$ (Güler, 1991). The rate is sublinear, $O(1/k)$, and it improves without limit as $\lambda$ grows: with $\lambda = \infty$ one step is the original problem. If $f$ is $\mu$-strongly convex, the distance contracts: $\|x_k - x^*\| \le (1 + \lambda\mu)^{-k}\|x_0 - x^*\|$, a linear rate. If $f$ is polyhedral (the maximum of finitely many affine functions plus the indicator of a polyhedron), the method stops at an exact minimizer after finitely many steps (Rockafellar, 1976).

**One iteration.** One evaluation of the proximal map. For a convex quadratic, it is one linear solve with $I + \lambda Q$, $O(n^3)$ for dense data or $O(n^2)$ after one factorization when $\lambda$ is fixed. For $\|x\|_1$ or the indicator of a box, it is $O(n)$. For a general $f$ it is a strongly convex problem that must be solved by another method. The extra space is $O(n)$.
## Properties

- **Monotone.** The values $f(x_k)$ decrease, and the distances $\|x_k - x^*\|$ to each minimizer do not increase (the sequence is Fejér monotone).
- **Convergent iterates.** The iterates converge to a minimizer when one exists, also with errors in line L2 whose sizes have a finite sum (Rockafellar, 1976).
- **Unconditionally stable.** Each $\lambda > 0$ works. There is no step-size limit such as $2/L$ for gradient descent.
- **Certified.** Each step gives a subgradient at the new point, so $\|g\|$ is a measure of stationarity.
- **Nonexpansive map.** $\operatorname{prox}_{\lambda f}$ is firmly nonexpansive, which is the property that the convergence theory for monotone operators uses.

## Variants and improvements

- **Inexact proximal point.** Solve line L2 only approximately, with an error $e_k$ such that $\sum_k\|e_k\| < \infty$. Rockafellar's 1976 theory covers this case.
- **Method of multipliers.** Apply the method to the negative dual function of a constrained problem. Line L2 becomes the minimization of the augmented Lagrangian, and line L4 becomes the multiplier update. This is the [augmented Lagrangian method](/augmented-lagrangian-method/).
- **Proximal bundle method.** Replace $f$ in line L2 by a piecewise-linear model built from subgradients, and move only when the model predicts a large enough decrease. This is the [bundle method](/bundle-method/).
- **Bregman proximal point.** Replace the squared distance by a [Bregman divergence](/bregman-divergence/), as in [mirror descent](/mirror-descent/).
- **Accelerated proximal point.** Güler (1991) added an extrapolation step, in the style of [Nesterov](/nesterov-accelerated-gradient/), and improved the rate to $O(1/k^2)$ for a fixed $\lambda$.
- **Monotone operators.** Replace $\partial f$ by any maximal monotone operator $T$, and solve $0 \in T(x)$ with $x^+ = (I + \lambda T)^{-1}(x)$. This covers saddle-point problems and variational inequalities, and [ADMM](/admm/) is an instance of it.

## When to use it

Use the proximal point method when the proximal map of $f$ is cheap, or when the regularized problem of line L2 is much better conditioned than the original one, for example when $f$ is convex but not strongly convex, or has sharp corners. More often, use it as a design rule: to make a method stable on a nonsmooth or ill-conditioned problem, add a proximal term. When $f = h + r$ with a smooth $h$, the [proximal gradient method](/proximal-gradient-method/) is usually cheaper, because it only needs the proximal map of $r$.

## Pitfalls

- **Line L2 is as hard as the problem.** For a general $f$, the proximal step is itself a convex minimization. The method then helps only if that minimization is easier, for example because it is strongly convex.
- **Stopping on the step length alone.** A small $\|x^+ - x\|$ means a small subgradient $g = (x - x^+)/\lambda$ only after division by $\lambda$. With a small $\lambda$, short steps do not mean that the point is close to optimal.
- **Too small $\lambda$.** The rate is in terms of $\lambda k$, so a tiny $\lambda$ gives a slow method. Choose $\lambda$ as large as the inner solver allows.
- **No minimizer.** If $f$ has no minimizer, for example $f(x) = e^{-x}$, the values still go to $\inf f$, but the iterates go to infinity and the rate bound does not apply.

## Implementations

## History

Martinet introduced the method in 1970 as a regularization of convex minimization problems, based on the proximal map that Moreau had studied in 1965. Rockafellar's two papers of 1976 made it a general tool: the first proved convergence for maximal monotone operators with inexact steps, and the second showed that the method of multipliers of Hestenes and Powell is the proximal point method applied to the dual problem. Güler (1991) proved the $O(1/k)$ rate for convex minimization and gave an accelerated version. Eckstein and Bertsekas (1992) showed that the Douglas-Rachford splitting method, and so ADMM, is a proximal point method for a suitable operator.

## References
