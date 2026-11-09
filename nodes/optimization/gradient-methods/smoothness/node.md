---
tag: GB36N6
kind: definition
slug: smoothness
name: Smoothness (L-smoothness)
aliases:
- L-smooth function
- Lipschitz continuous gradient
- smoothness constant
area: optimization/gradient-methods
level: intro
summary: A differentiable function is L_f-smooth when its gradient is L_f-Lipschitz. Then f lies below a quadratic around each point, and the gradient step 1/L_f always decreases f.
prereqs: [gradient]
see_also: [strong-convexity, condition-number-of-an-optimization-problem, gradient-descent, gradient-descent-convergence-theorem, convex-function, lipschitz-condition, positive-definite-matrix]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Section 1.2.2, Classes of differentiable functions (the quadratic upper bound), and Section 2.1.1, Smooth convex functions (the equivalent conditions for convex functions)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 5, Smoothness and strong convexity, Section 5.1, L-smooth functions (the descent lemma and the characterizations)
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 3.2, Gradient descent for smooth functions (the lemmas on smooth convex functions)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.1.2, Strong convexity and implications (the upper bound on the Hessian)
---

A differentiable function $f : \mathbb{R}^n \to \mathbb{R}$ is $L_f$-smooth when its [gradient](/gradient/) is Lipschitz continuous with constant $L_f$: the gradient cannot change faster than $L_f$ times the distance. Then $f$ lies below the quadratic $f(x) + \nabla f(x)^\top (y - x) + \frac{L_f}{2}\|y - x\|^2$ around each point $x$. This upper bound is what makes [gradient descent](/gradient-descent/) with step $1/L_f$ decrease $f$ at each step, and $L_f$ sets the scale of all step sizes in first-order methods.

## Definition

Let $f : \mathbb{R}^n \to \mathbb{R}$ be differentiable and $L \ge 0$. The function $f$ is *$L$-smooth* if

$$\|\nabla f(x) - \nabla f(y)\| \le L \|x - y\| \qquad \text{for all } x, y \in \mathbb{R}^n,$$

with the Euclidean norm. The smallest such $L$ is the *smoothness constant* $L_f$. (Optimization pages write $L_f$, because $L$ is the bit length of the input on the linear programming pages.) The word "smooth" here does not mean "infinitely differentiable": an $L_f$-smooth function need not have a second derivative.

**The quadratic upper bound (descent lemma).** If $f$ is $L$-smooth, then for all $x, y$

$$\left| f(y) - f(x) - \nabla f(x)^\top (y - x) \right| \le \frac{L}{2} \|y - x\|^2.$$

*Proof.* Let $h = y - x$. By the fundamental theorem of calculus applied to $t \mapsto f(x + th)$, the left side is $\left|\int_0^1 (\nabla f(x + th) - \nabla f(x))^\top h \, dt\right| \le \int_0^1 L t \|h\|^2 dt = \frac{L}{2}\|h\|^2$, by the Cauchy-Schwarz inequality. $\square$

**Second-order test.** Let $f$ be twice continuously differentiable. Then $f$ is $L$-smooth if and only if $\|\nabla^2 f(x)\|_2 \le L$ for all $x$, where $\|\cdot\|_2$ is the spectral [matrix norm](/matrix-norms/). For a symmetric Hessian this means that every [eigenvalue](/eigenvalue/) of $\nabla^2 f(x)$ lies in $[-L, L]$.

*Proof.* If the Hessian bound holds, then $\nabla f(y) - \nabla f(x) = \int_0^1 \nabla^2 f(x + t(y - x)) (y - x) \, dt$, whose norm is at most $L \|y - x\|$. Conversely, $\nabla^2 f(x) d = \lim_{t \to 0} (\nabla f(x + td) - \nabla f(x))/t$, and the norm of each quotient is at most $L \|d\|$. $\square$

**A bound on the gradient.** If $f$ is $L$-smooth with $L > 0$ and bounded below by $f^* = \inf f$, then $\|\nabla f(x)\|^2 \le 2L (f(x) - f^*)$ for each $x$. *Proof.* The descent lemma at $y = x - \nabla f(x)/L$ gives $f^* \le f(y) \le f(x) - \frac{1}{2L}\|\nabla f(x)\|^2$. $\square$ Convexity is not needed here.

**Smooth convex functions.** For a convex differentiable $f$, these conditions are equivalent (Nesterov, Section 2.1.1; Beck, Section 5.1):

1. $f$ is $L$-smooth.
2. $f(y) \le f(x) + \nabla f(x)^\top (y - x) + \frac{L}{2}\|y - x\|^2$ for all $x, y$.
3. $f(y) \ge f(x) + \nabla f(x)^\top (y - x) + \frac{1}{2L}\|\nabla f(y) - \nabla f(x)\|^2$ for all $x, y$.
4. (co-coercivity) $(\nabla f(x) - \nabla f(y))^\top (x - y) \ge \frac{1}{L}\|\nabla f(x) - \nabla f(y)\|^2$ for all $x, y$.

The descent lemma gives 1 ⇒ 2. For 2 ⇒ 3, fix $x$ and let $\varphi(z) = f(z) - \nabla f(x)^\top z$. Then $\varphi$ is convex, $\nabla \varphi(x) = 0$, so $x$ minimizes $\varphi$, and $\varphi$ also satisfies 2. Hence $\varphi(x) \le \varphi(y - \nabla\varphi(y)/L) \le \varphi(y) - \frac{1}{2L}\|\nabla \varphi(y)\|^2$, and this is 3 after the substitution $\nabla\varphi(y) = \nabla f(y) - \nabla f(x)$. Adding 3 to itself with $x$ and $y$ swapped gives 4, and 4 gives 1 by the Cauchy-Schwarz inequality. Without convexity, 2 does not imply 1: the right side of 2 is only one half of the two-sided bound.

## Examples and non-examples

**Examples.**

- **Quadratics.** $f(x) = \frac12 x^\top A x - b^\top x$ with $A$ symmetric has $\nabla f(x) - \nabla f(y) = A (x - y)$, so $L_f = \|A\|_2 = \max_i |\lambda_i(A)|$. For $A = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$ the eigenvalues are $(5 \pm \sqrt{5})/2$, so $L_f = 3.618$ to three decimals.
- **Least squares.** $f(x) = \frac12 \|Ax - b\|^2$ has Hessian $A^\top A$, so $L_f = \lambda_{\max}(A^\top A) = \sigma_{\max}(A)^2$. For the line fit with rows $(1, 0), (1, 1), (1, 2)$, $A^\top A = \begin{pmatrix} 3 & 3 \\ 3 & 5 \end{pmatrix}$ with eigenvalues $4 \pm \sqrt{10}$, so $L_f = 7.162$.
- **Logistic loss.** $\ell(t) = \log(1 + e^{-t})$ has $\ell''(t) = \sigma(t)(1 - \sigma(t)) \le 1/4$ with $\sigma(t) = 1/(1 + e^{-t})$. So the average loss $\frac{1}{m}\sum_i \ell(y_i a_i^\top x)$ of [logistic regression](/logistic-regression/) is $L$-smooth with $L = \|A\|_2^2 / (4m)$, where the rows of $A$ are the $a_i$.
- **Not twice differentiable.** The Huber function $h(t) = t^2/2$ for $|t| \le 1$ and $|t| - 1/2$ otherwise has $h'(t) = \max(-1, \min(1, t))$, which is 1-Lipschitz. So $h$ is 1-smooth, but $h''$ does not exist at $\pm 1$.
- **Not convex.** $f(x) = x^2 + 3 \sin^2 x$ has $f''(x) = 2 + 6 \cos 2x$, which takes all values in $[-4, 8]$. So $L_f = 8$, and $f$ is not convex.
- **Smooth but with no minimizer.** $f(x) = \log(1 + e^{x})$ is $\frac14$-smooth and convex, and $\inf f = 0$ is not attained.

**Non-examples.**

- $f(x) = x^4$: $f'(x) = 4x^3$ and $|f'(x) - f'(0)| / |x| = 4x^2$ is not bounded. So $f$ is not $L$-smooth on $\mathbb{R}$ for any $L$. It is smooth on each bounded set, with $L = 12 r^2$ on $[-r, r]$. The same holds for $e^x$.
- $f(x) = |x|^{3/2}$ is differentiable, with $f'(x) = \frac32 \operatorname{sign}(x) |x|^{1/2}$, but $|f'(x) - f'(0)|/|x| = \frac32 |x|^{-1/2}$ is not bounded near $0$.
- $f(x) = |x|$ and $f(x) = \|x\|$ are not differentiable at $0$, so they are not smooth for any $L$. Subgradient methods and [proximal methods](/proximal-gradient-method/) treat such terms.
- A Lipschitz function need not be smooth. $f(x) = \sin(x^2)/\sqrt{1 + x^2}$ has $f'(x) = 2x\cos(x^2)/\sqrt{1 + x^2} - x \sin(x^2)/(1 + x^2)^{3/2}$, so $|f'(x)| \le 3$ and $f$ is 3-Lipschitz. But $f''$ has the term $-4x^2 \sin(x^2)/\sqrt{1 + x^2}$, whose size grows like $4|x|$, and the other terms of $f''$ are bounded. So $f'$ is not Lipschitz, and $f$ is not $L$-smooth for any $L$.

## Related definitions

- [Strong convexity](/strong-convexity/) with constant $\mu$ is the lower quadratic bound $f(y) \ge f(x) + \nabla f(x)^\top (y - x) + \frac{\mu}{2}\|y - x\|^2$. For a twice differentiable function, smoothness and strong convexity together mean $\mu I \preceq \nabla^2 f(x) \preceq L_f I$, and the ratio $\kappa = L_f / \mu$ is the [condition number](/condition-number-of-an-optimization-problem/).
- The [Lipschitz condition](/lipschitz-condition/) of differential equations is the same inequality, applied to the right side of an equation, not to a gradient.
- A [convex function](/convex-function/) is $L$-smooth if and only if its convex conjugate is $(1/L)$-strongly convex (Beck, Chapter 5).
- The [convergence theorem of gradient descent](/gradient-descent-convergence-theorem/) and the [first-order lower bound](/first-order-lower-bound/) are stated for the class of convex $L_f$-smooth functions.
- [Polyak-Lojasiewicz condition](/polyak-lojasiewicz-condition/): a lower bound on $\|\nabla f\|^2$ that, with smoothness, gives a linear rate without convexity.

## References
