---
tag: N9CFZ7
kind: definition
slug: gradient
name: Gradient
aliases:
- gradient vector
- first derivative of a multivariate function
area: optimization/gradient-methods
level: intro
summary: The vector of partial derivatives of a differentiable function. It gives the best linear approximation of the function and points in the direction of steepest local increase.
see_also: [smoothness, gradient-descent, convex-function, subgradient, automatic-differentiation, backpropagation, natural-gradient-descent, unconstrained-smooth-minimization]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Appendix A.4, Derivatives (A.4.1, Derivative and gradient, and A.4.2, Chain rule)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 2.1, What is a solution? (Taylor's theorem and the first-order necessary condition, Theorem 2.2)
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Section 1.2.1, Relaxation and approximation (the gradient as the direction of fastest local increase, and the antigradient)
---

The gradient of a differentiable function $f : \mathbb{R}^n \to \mathbb{R}$ at a point $x$ is the vector $\nabla f(x)$ of its partial derivatives. It is the vector that gives the best linear approximation $f(x + h) \approx f(x) + \nabla f(x)^\top h$, and among all unit directions it points in the direction of fastest local increase of $f$. [Gradient descent](/gradient-descent/) and every other first-order method of [unconstrained smooth minimization](/unconstrained-smooth-minimization/) use only values of $f$ and of $\nabla f$.

## Definition

Let $U \subseteq \mathbb{R}^n$ be open, $f : U \to \mathbb{R}$ and $x \in U$. The function $f$ is *differentiable at $x$* if there is a vector $g \in \mathbb{R}^n$ such that

$$\lim_{h \to 0} \frac{f(x + h) - f(x) - g^\top h}{\|h\|} = 0.$$

The vector $g$ is unique. It is the *gradient* of $f$ at $x$, written $\nabla f(x)$, and its coordinates are the partial derivatives:

$$\nabla f(x) = \left( \frac{\partial f}{\partial x_1}(x), \ldots, \frac{\partial f}{\partial x_n}(x) \right).$$

The function is differentiable on $U$ if it is differentiable at each point of $U$, and then $\nabla f : U \to \mathbb{R}^n$ is a vector field. A point with $\nabla f(x) = 0$ is a *stationary point* (or critical point).

Uniqueness holds because two such vectors $g, g'$ give $(g - g')^\top h / \|h\| \to 0$; with $h = t (g - g')$ and $t \downarrow 0$ this ratio is the constant $\|g - g'\|$, so $g = g'$. With $h = t e_i$ for the $i$-th unit vector, the limit gives $g_i = \partial f / \partial x_i (x)$.

**Directional derivative.** If $f$ is differentiable at $x$, then for each $d \in \mathbb{R}^n$

$$D_d f(x) = \lim_{t \to 0} \frac{f(x + t d) - f(x)}{t} = \nabla f(x)^\top d.$$

**Direction of steepest increase.** Let $\nabla f(x) \ne 0$. Over all $d$ with $\|d\| = 1$, the Cauchy-Schwarz inequality gives $-\|\nabla f(x)\| \le \nabla f(x)^\top d \le \|\nabla f(x)\|$. The upper bound holds with equality only for $d = \nabla f(x)/\|\nabla f(x)\|$ and the lower one only for $d = -\nabla f(x)/\|\nabla f(x)\|$. So the gradient is the direction of steepest ascent, the negative gradient is the direction of steepest descent, and $\|\nabla f(x)\|$ is the largest rate of change. Each $d$ with $\nabla f(x)^\top d < 0$ is a *descent direction*: $f(x + td) < f(x)$ for all small $t > 0$.

**First-order necessary condition.** If $x$ is a local minimizer of $f$ in the open set $U$ and $f$ is differentiable at $x$, then $\nabla f(x) = 0$. *Proof.* If $g = \nabla f(x) \ne 0$, take $d = -g$. Then $D_d f(x) = -\|g\|^2 < 0$, so $f(x + td) < f(x)$ for all small $t > 0$, and $x$ is not a local minimizer. $\square$ For a [convex function](/convex-function/) the condition is also sufficient: $f(y) \ge f(x) + \nabla f(x)^\top (y - x)$ for all $y$, so $\nabla f(x) = 0$ makes $x$ a global minimizer.

**Rules.** The gradient is linear: $\nabla (af + bh) = a \nabla f + b \nabla h$. The chain rule for an affine map is $\nabla (h \circ A)(x) = A^\top \nabla h(Ax + c)$ when $f(x) = h(Ax + c)$. For $f = \psi \circ h$ with $\psi : \mathbb{R} \to \mathbb{R}$ it is $\nabla f(x) = \psi'(h(x)) \nabla h(x)$.

**Dependence on the inner product.** The gradient is defined by the Euclidean inner product $g^\top h$. With the inner product $\langle u, v \rangle_P = u^\top P v$ for a symmetric [positive definite](/positive-definite-matrix/) matrix $P$, the vector $g_P$ with $f(x + h) = f(x) + \langle g_P, h \rangle_P + o(\|h\|)$ is $g_P = P^{-1} \nabla f(x)$. Preconditioned and [natural gradient](/natural-gradient-descent/) methods use such a $g_P$.

## Examples and non-examples

**Examples.** Here $A$ is an $m \times n$ or $n \times n$ matrix, $b$ and $c$ are vectors, and $\sigma(t) = 1/(1 + e^{-t})$.

| $f(x)$ | $\nabla f(x)$ |
|---|---|
| $c^\top x$ | $c$ |
| $\frac12 x^\top A x - b^\top x$, $A$ symmetric | $Ax - b$ |
| $\frac12 x^\top A x$, any square $A$ | $\frac12 (A + A^\top) x$ |
| $\frac12 \|Ax - b\|^2$ (least squares) | $A^\top (Ax - b)$ |
| $\log(1 + e^{-y a^\top x})$, $y \in \{-1, 1\}$ (logistic loss) | $-y \, \sigma(-y a^\top x) \, a$ |
| $\log \sum_i e^{x_i}$ (log-sum-exp) | the softmax vector $\left(e^{x_i} / \sum_j e^{x_j}\right)_i$ |
| $\|x\|$, at $x \ne 0$ | $x / \|x\|$ |

The least squares row follows from the chain rule with $h(r) = \frac12 \|r\|^2$, $\nabla h(r) = r$. It is the gradient that [linear regression](/linear-regression/) sets to zero, which gives the [normal equations](/normal-equations/) $A^\top A x = A^\top b$.

- For $f(x_1, x_2) = x_1^2 x_2 + \sin x_2$, $\nabla f(x) = (2 x_1 x_2, \; x_1^2 + \cos x_2)$, so $\nabla f(1, 0) = (0, 2)$. In the unit direction $d = (0.6, 0.8)$ the rate of change is $\nabla f(1,0)^\top d = 1.6$, and in the direction $(0, 1)$ of the gradient it is the maximum, $\|\nabla f(1,0)\| = 2$.
- For $A = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$, $b = (1, 1)$ and $x = (1, 2)$, the quadratic row gives $\nabla f(x) = Ax - b = (3, 6)$.
- For log-sum-exp at $x = (0, \ln 3)$, the gradient is $(1/4, 3/4)$. Its entries are positive and add up to 1.
- **The gradient does not point to the minimizer.** For $f(x) = \frac12 (x_1^2 + 10 x_2^2)$ at $x = (10, 1)$, the steepest descent direction is $-\nabla f(x) = (-10, -10)$, but the minimizer $0$ lies in the direction $(-10, -1)$. The angle between them is about $39.3$ degrees. This is the source of the zigzag of [gradient descent](/gradient-descent/) on ill-conditioned functions.

**Non-examples.**

- $f(x) = |x|$ on $\mathbb{R}$ has no gradient at $0$: the one-sided derivatives are $-1$ and $1$. It has [subgradients](/subgradient/), every $g \in [-1, 1]$, and the [subdifferential](/subdifferential/) replaces the gradient for nonsmooth convex functions.
- Partial derivatives can exist where the gradient does not. Let $f(x_1, x_2) = x_1 x_2 / (x_1^2 + x_2^2)$ for $x \ne 0$ and $f(0) = 0$. Both partial derivatives at $0$ are $0$, since $f$ is $0$ on both axes. But $f(t, t) = 1/2$ for every $t \ne 0$, so $f$ is not even continuous at $0$, and it is not differentiable there. The vector $(0, 0)$ of partial derivatives is not a gradient.
- Directional derivatives in all directions are not enough either. For $f(x_1, x_2) = x_1^2 x_2 / (x_1^2 + x_2^2)$ with $f(0) = 0$, the directional derivative at $0$ is $D_d f(0) = d_1^2 d_2 / (d_1^2 + d_2^2)$ for $d \ne 0$. This is not linear in $d$, so no $g$ satisfies $D_d f(0) = g^\top d$, and $f$ is not differentiable at $0$.
- A stationary point need not be a minimizer: $f(x) = x_1^2 - x_2^2$ has $\nabla f(0) = 0$ at a saddle point, and $f(x) = -\|x\|^2$ has it at the maximizer.

## Related definitions

- The *Hessian* $\nabla^2 f(x)$ is the matrix of second partial derivatives, the derivative of $\nabla f$. Newton's method ([Newton's method for systems](/newton-method-for-systems/), applied to $\nabla f(x) = 0$) uses it.
- The *Jacobian* of a map $F : \mathbb{R}^n \to \mathbb{R}^m$ is the $m \times n$ matrix of partial derivatives. The gradient of $f$ is the transpose of the $1 \times n$ Jacobian.
- [Smoothness](/smoothness/) bounds how fast the gradient changes: $\|\nabla f(x) - \nabla f(y)\| \le L_f \|x - y\|$.
- A [subgradient](/subgradient/) of a convex function at $x$ is any $g$ with $f(y) \ge f(x) + g^\top (y - x)$ for all $y$. For a differentiable convex function the gradient is the only subgradient.
- [Automatic differentiation](/automatic-differentiation/) computes $\nabla f$ exactly from a program for $f$. Its reverse mode, called [backpropagation](/backpropagation/) for neural networks, gives the full gradient at a cost that is a small constant multiple of the cost of $f$.
- A [convex function](/convex-function/) lies above each of its tangent planes $f(x) + \nabla f(x)^\top (y - x)$.

## References
