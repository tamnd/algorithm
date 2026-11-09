---
tag: Q24YCK
kind: definition
slug: armijo-condition
name: Armijo condition
aliases:
- sufficient decrease condition
- Armijo rule
- first Wolfe condition
area: optimization/gradient-methods
level: core
summary: "A step α along a descent direction d is acceptable if f(x + αd) ≤ f(x) + c α ∇f(x)ᵀd: the decrease is at least a fixed fraction c of the decrease that the tangent line predicts."
prereqs: [step-size-selection]
see_also: [backtracking-line-search, wolfe-conditions, exact-line-search, gradient-descent, step-size-selection, smoothness]
sources:
  - paper: doi:10.2140/pjm.1966.16.1
    title: Larry Armijo, Minimization of functions having Lipschitz continuous first partial derivatives, Pacific Journal of Mathematics 16(1), 1966
    locator: pages 1 to 3 (the step size rule and the convergence theorem)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 3.1, Step length (the sufficient decrease condition, and Algorithm 3.1, backtracking line search)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.2, Descent methods (backtracking line search and the parameters α and β)
  - paper: doi:10.1137/0303013
    title: A. A. Goldstein, On steepest descent, Journal of the Society for Industrial and Applied Mathematics, Series A, Control 3(1), 1965
    locator: pages 147 to 151 (the two-sided step condition now called the Goldstein conditions)
---

The Armijo condition is the test that a line search uses to accept a step. A step $\alpha > 0$ along a descent direction $d$ at $x$ is acceptable if $f(x + \alpha d) \le f(x) + c\,\alpha\,\nabla f(x)^\top d$ for a fixed $c \in (0, 1)$, that is, if the actual decrease is at least the fraction $c$ of the decrease predicted by the linear model. All small enough steps pass it, so [backtracking line search](/backtracking-line-search/) always stops. With an $L_f$-[smooth](/smoothness/) $f$ and $d = -\nabla f(x)$, every $\alpha \le 2(1 - c)/L_f$ passes. It is the first of the two [Wolfe conditions](/wolfe-conditions/).

## Definition

Let $f : \mathbb{R}^n \to \mathbb{R}$ be differentiable, $x \in \mathbb{R}^n$, and $d$ a descent direction, $\nabla f(x)^\top d < 0$. Let $\varphi(\alpha) = f(x + \alpha d)$, so $\varphi'(0) = \nabla f(x)^\top d$. For a constant $c \in (0, 1)$, a step $\alpha > 0$ satisfies the *Armijo condition* (or *sufficient decrease condition*) if

$$\varphi(\alpha) \le \varphi(0) + c\,\alpha\,\varphi'(0).$$

The right side is a line through $(0, \varphi(0))$ with the slope $c\varphi'(0)$, which is less steep than the tangent. The condition asks that the graph of $\varphi$ lie on or below this line at $\alpha$. Typical values are $c = 10^{-4}$ (Nocedal and Wright) and $c \in [0.01, 0.3]$ (Boyd and Vandenberghe). Armijo's 1966 rule used $c = \frac12$ with $d = -\nabla f(x)$ and trial steps $\alpha_0, \alpha_0/2, \alpha_0/4, \ldots$.

**Small steps pass.** Since $\varphi(\alpha) = \varphi(0) + \alpha\varphi'(0) + o(\alpha)$ and $(1 - c)\varphi'(0) < 0$, there is $\bar{\alpha} > 0$ such that $\varphi(\alpha) - \varphi(0) - c\alpha\varphi'(0) = (1 - c)\alpha\varphi'(0) + o(\alpha) < 0$ for all $\alpha \in (0, \bar{\alpha})$.

**An explicit range under smoothness.** If $\nabla f$ is $L_f$-Lipschitz, then

$$\text{every } \alpha \in \left(0, \frac{2(1 - c)\,|\varphi'(0)|}{L_f\|d\|^2}\right] \text{ satisfies the Armijo condition.}$$

*Proof.* The descent lemma gives $\varphi(\alpha) \le \varphi(0) + \alpha\varphi'(0) + \frac{L_f\|d\|^2}{2}\alpha^2$. The right side is at most $\varphi(0) + c\alpha\varphi'(0)$ exactly when $\frac{L_f\|d\|^2}{2}\alpha \le (1 - c)|\varphi'(0)|$. $\square$ For the gradient direction $d = -\nabla f(x)$, $|\varphi'(0)| = \|d\|^2$, and the range is $\alpha \le 2(1 - c)/L_f$. An accepted step along $-\nabla f(x)$ then gives the decrease $f(x) - f(x + \alpha d) \ge c\alpha\|\nabla f(x)\|^2$.

**The constant must be less than 1.** If $c = 1$ and $\varphi$ is strictly convex, then $\varphi(\alpha) > \varphi(0) + \alpha\varphi'(0)$ for every $\alpha > 0$, so no step passes.

**The constant decides whether the exact step passes.** If $\varphi$ is a convex parabola, its minimizer is $\alpha^* = -\varphi'(0)/\varphi''$ and $\varphi(\alpha^*) = \varphi(0) + \frac12\alpha^*\varphi'(0)$. So $\alpha^*$ passes if and only if $c \le \frac12$. This is why $c < \frac12$ is required for Newton and quasi-Newton methods: their unit step must pass near the solution to keep the fast local rate.

## Examples and non-examples

**Example.** Let $f(x) = \frac12(x_1^2 + 10x_2^2)$, $x = (10, 1)$ and $d = -\nabla f(x) = (-10, -10)$. Then

$$\varphi(\alpha) = 50(1 - \alpha)^2 + 5(1 - 10\alpha)^2 = 55 - 200\alpha + 550\alpha^2,$$

with $\varphi(0) = 55$ and $\varphi'(0) = -200$. The Armijo condition is $550\alpha^2 \le (1 - c)200\alpha$, that is, $\alpha \le \frac{(1 - c)200}{550}$.

| $c$ | accepted steps | note |
|---|---|---|
| $10^{-4}$ | $0 < \alpha \le 0.36360$ | almost every step up to where $\varphi$ returns to $\varphi(0)$, at $\alpha = 4/11$ |
| $\frac12$ | $0 < \alpha \le 2/11 \approx 0.1818$ | the largest accepted step is the exact minimizer of $\varphi$ |
| $0.9$ | $0 < \alpha \le 0.03636$ | only short steps |

The smoothness range $2(1 - c)/L_f$ with $L_f = 10$ gives $\alpha \le 0.19998$ for $c = 10^{-4}$, a smaller but valid range. Backtracking from $\alpha_0 = 1$ with the factor $\frac12$ and $c = 10^{-4}$ rejects $1$ and $0.5$ and accepts $0.25$, with $\varphi(0.25) = 39.375$.

**Non-examples.**

- **A step that decreases $f$ but fails the test.** For $c = \frac12$ in the example, $\alpha = 0.3$ gives $\varphi(0.3) = 44.5 < 55$, so $f$ decreases, but $55 - \frac12 \cdot 0.3 \cdot 200 = 25$, and $44.5 > 25$. The decrease is too small for the step length.
- **The Armijo condition does not exclude tiny steps.** Every $\alpha$ near $0$ passes. So the condition alone does not ensure progress; a line search must also start from a reasonable trial step and shrink it by a bounded factor ([backtracking](/backtracking-line-search/)), or add the curvature condition of the [Wolfe conditions](/wolfe-conditions/).
- **Not a descent direction.** If $\nabla f(x)^\top d \ge 0$, the right side is at least $\varphi(0)$, and a step can pass while $f$ increases or stays the same. The condition is meant for descent directions only.

## Related definitions

- The [Wolfe conditions](/wolfe-conditions/) add the curvature condition $\varphi'(\alpha) \ge c_2\varphi'(0)$ with $c < c_2 < 1$, which excludes steps that are too short.
- The *Goldstein conditions* $\varphi(0) + (1 - c)\alpha\varphi'(0) \le \varphi(\alpha) \le \varphi(0) + c\alpha\varphi'(0)$, with $c \in (0, \frac12)$, add a lower bound on $\varphi(\alpha)$ for the same purpose. They can exclude every minimizer of $\varphi$, which makes them less suited to quasi-Newton methods.
- [Backtracking line search](/backtracking-line-search/) finds a step that meets the Armijo condition in finitely many trials.
- [Exact line search](/exact-line-search/) picks the minimizer of $\varphi$, which meets the Armijo condition for every $c \le \frac12$ when $\varphi$ is a convex parabola.
- [Step size selection](/step-size-selection/) lists the other step rules.

## References
