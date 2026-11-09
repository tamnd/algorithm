---
tag: 5GSPJN
kind: definition
slug: polyak-lojasiewicz-condition
name: Polyak-Lojasiewicz condition
aliases:
- PL inequality
- Polyak-Lojasiewicz inequality
- gradient dominance condition
- PL condition
area: optimization/gradient-methods
level: research
summary: "f satisfies the PL condition with μ > 0 if ½‖∇f(x)‖² ≥ μ(f(x) - f*) for all x. It gives gradient descent a linear rate without convexity; every stationary point is a global minimizer."
prereqs: [gradient-descent, strong-convexity]
see_also: [linear-convergence-strongly-convex, strong-convexity, smoothness, gradient-descent, least-squares-problem, condition-number-of-an-optimization-problem, stochastic-gradient-descent]
sources:
  - paper: doi:10.1016/0041-5553(63)90382-3
    title: Boris T. Polyak, Gradient methods for the minimisation of functionals, USSR Computational Mathematics and Mathematical Physics 3(4), 1963
    locator: pages 864 to 878 (the condition and the linear convergence of the gradient method under it)
  - paper: doi:10.1007/978-3-319-46128-1_50
    title: Hamed Karimi, Julie Nutini and Mark Schmidt, Linear convergence of gradient and proximal-gradient methods under the Polyak-Łojasiewicz condition, ECML PKDD 2016, Lecture Notes in Computer Science 9851
    locator: pages 795 to 811 (Theorem 1, linear convergence under PL; Theorem 2, the relations among PL, error bounds, quadratic growth and weaker forms of strong convexity; the example x^2 + 3 sin^2 x)
---

A differentiable function $f$ with minimum value $f^*$ satisfies the *Polyak-Lojasiewicz (PL) condition* with constant $\mu > 0$ if $\frac12\|\nabla f(x)\|^2 \ge \mu(f(x) - f^*)$ for all $x$: the gradient is large wherever the function value is far from optimal. Every [strongly convex](/strong-convexity/) function satisfies it, but so do some nonconvex functions and some convex functions with many minimizers, such as least squares with a rank-deficient matrix. For an $L_f$-[smooth](/smoothness/) function with this condition, [gradient descent](/gradient-descent/) with step $1/L_f$ has $f(x_k) - f^* \le (1 - \mu/L_f)^k(f(x_0) - f^*)$, the same rate as under strong convexity.

## Definition

Let $f : \mathbb{R}^n \to \mathbb{R}$ be differentiable, and let its minimum value $f^* = \min_x f(x)$ be attained, with the set of minimizers $X^*$. For $\mu > 0$, $f$ satisfies the *PL condition with constant $\mu$* if

$$\frac12\|\nabla f(x)\|^2 \ge \mu\left(f(x) - f^*\right) \qquad \text{for all } x \in \mathbb{R}^n.$$

Polyak introduced it in 1963 as a sufficient condition for the linear convergence of the gradient method. It is the global form, with exponent $\frac12$, of the *Łojasiewicz inequality* $|f(x) - f^*|^{\theta} \le C\|\nabla f(x)\|$, which Łojasiewicz proved near each critical point of a real analytic function, with an exponent $\theta \in [\frac12, 1)$ that depends on the function.

**Direct consequences.**

- *Every stationary point is a global minimizer.* If $\nabla f(x) = 0$, the condition gives $f(x) - f^* \le 0$, so $x \in X^*$. So the condition rules out saddle points and local minimizers that are not global.
- *Smoothness bounds the constant.* If $f$ is also $L_f$-smooth, then $\|\nabla f(x)\|^2 \le 2L_f(f(x) - f^*)$ ([smoothness](/smoothness/)), so $\mu \le L_f$ whenever $f$ is not constant.
- *Uniqueness is not required.* The set $X^*$ can be a line, a subspace or a nonconvex set.

**Linear convergence of gradient descent.** Let $f$ be $L_f$-smooth with the PL constant $\mu$, and $x_{k+1} = x_k - \frac{1}{L_f}\nabla f(x_k)$. Then $f(x_k) - f^* \le (1 - \mu/L_f)^k(f(x_0) - f^*)$.

*Proof.* The descent lemma gives $f(x_{k+1}) \le f(x_k) - \frac{1}{2L_f}\|\nabla f(x_k)\|^2$. The PL condition bounds the last term: $\frac{1}{2L_f}\|\nabla f(x_k)\|^2 \ge \frac{\mu}{L_f}(f(x_k) - f^*)$. Subtract $f^*$ and use induction on $k$. $\square$

The proof uses no convexity. Karimi, Nutini and Schmidt proved that for $L_f$-smooth functions the PL condition also implies *quadratic growth*, $f(x) - f^* \ge \frac{\mu}{2}\operatorname{dist}(x, X^*)^2$, and that the iterates converge to a point of $X^*$ at a linear rate. They also proved that PL is equivalent to the error bound condition and is implied by the weaker forms of strong convexity used in earlier work (essential strong convexity, weak strong convexity and the restricted secant inequality). Those results are stated here as theirs and are not proved on this page.

## Examples and non-examples

**Examples.**

- **Strongly convex functions.** If $f$ is $\mu$-strongly convex, minimize both sides of $f(y) \ge f(x) + \nabla f(x)^\top(y - x) + \frac{\mu}{2}\|y - x\|^2$ over $y$: the left side gives $f^*$, the right side gives $f(x) - \frac{1}{2\mu}\|\nabla f(x)\|^2$. So $f$ is PL with the same $\mu$.
- **Least squares with any matrix.** Let $f(x) = \frac12\|Ax - b\|^2$, and let $\sigma_+$ be the smallest nonzero singular value of $A$. Then $f$ is PL with $\mu = \sigma_+^2$, even if $A$ has a nontrivial null space and $f$ has a whole affine set of minimizers. *Proof.* Let $x^* \in X^*$ and $r^* = Ax^* - b$; then $A^\top r^* = 0$ by the [normal equations](/normal-equations/). For each $x$ let $w = A(x - x^*)$, which lies in the range of $A$. Then $\nabla f(x) = A^\top(w + r^*) = A^\top w$, and $\|A^\top w\| \ge \sigma_+\|w\|$ for $w$ in the range of $A$. Since $w \perp r^*$, $f(x) - f^* = \frac12\|w + r^*\|^2 - \frac12\|r^*\|^2 = \frac12\|w\|^2$. So $\frac12\|\nabla f(x)\|^2 \ge \sigma_+^2 \cdot \frac12\|w\|^2 = \sigma_+^2(f(x) - f^*)$. $\square$ For $A = \begin{pmatrix} 1 & 1 \\ 1 & 1\end{pmatrix}$, $A^\top A$ has eigenvalues $4$ and $0$, so $f$ is PL with $\mu = 4$ and $4$-smooth, and gradient descent with step $\frac14$ reaches $X^*$ in one step, although $f$ is not strongly convex.
- **Strongly convex function of a linear map.** More generally, $f(x) = g(Ax)$ with $g$ strongly convex and smooth is PL (Karimi, Nutini and Schmidt). This covers [logistic regression](/logistic-regression/) on a bounded set and least squares.
- **A nonconvex function.** $f(x) = x^2 + 3\sin^2 x$ has $f''(x) = 2 + 6\cos 2x$, which is negative near $x = \pi/2$, so $f$ is not convex. Its only stationary point is $x = 0$, with $f^* = 0$, and it is PL: Karimi, Nutini and Schmidt give $\mu = \frac{1}{32}$, and the best constant, the minimum of $\frac{f'(x)^2}{2f(x)}$, is about $0.1755$, near $x = 2.20$. It is $8$-smooth, so gradient descent with step $\frac18$ converges linearly from every start.

**Non-examples.**

- $f(x) = x^4$ is convex with $f^* = 0$, but $\frac12 f'(x)^2 = 8x^6$ is smaller than $\mu x^4$ for $|x| < \sqrt{\mu/8}$. Gradient descent on $x^4$ converges only sublinearly. (It is also not $L$-smooth on $\mathbb{R}$, but the PL failure is near $0$.)
- $f(x) = (x^2 - 1)^2$ has the stationary point $0$ with $f(0) = 1 > f^* = 0$, so it is not PL for any $\mu$. Each function with a saddle point or a local minimizer that is not global fails the condition in the same way.
- $f(x) = \log(1 + e^{x})$ has no minimizer, and $\frac12 f'(x)^2 / f(x) \to 0$ as $x \to -\infty$, so no $\mu > 0$ works with $f^* = \inf f = 0$ either.
- Convex functions with a minimizer can fail it: $f(x) = |x|^{3/2}$ has $\frac12 f'(x)^2 = \frac98|x|$, which is smaller than $\mu|x|^{3/2}$ for large $|x|$.

## Related definitions

- [Strong convexity](/strong-convexity/) implies PL with the same constant; PL does not imply convexity.
- *Quadratic growth*, $f(x) - f^* \ge \frac{\mu}{2}\operatorname{dist}(x, X^*)^2$, follows from PL for smooth functions, and is equivalent to PL for convex smooth functions (Karimi, Nutini and Schmidt).
- The *error bound* condition, $\|\nabla f(x)\| \ge c\operatorname{dist}(x, X^*)$, is equivalent to PL for smooth functions, up to the constants.
- The [linear convergence theorem](/linear-convergence-strongly-convex/) states the rates of gradient descent under strong convexity, with the PL form as part 3.
- With [stochastic gradient descent](/stochastic-gradient-descent/) and a decreasing step, the PL condition gives the rate $O(1/k)$ for $f(x_k) - f^*$ in expectation, as strong convexity does.
- The [condition number](/condition-number-of-an-optimization-problem/) $L_f/\mu$ with the PL constant in place of the strong convexity constant sets the step count of gradient descent.

## References
