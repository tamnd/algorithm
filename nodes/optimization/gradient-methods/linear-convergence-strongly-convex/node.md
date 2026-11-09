---
tag: AEWEYN
kind: theorem
slug: linear-convergence-strongly-convex
name: Linear convergence under strong convexity
aliases:
- linear rate of gradient descent
- geometric convergence of gradient descent
area: optimization/gradient-methods
level: advanced
summary: On an L_f-smooth μ-strongly convex f, gradient descent with step 1/L_f shrinks f(x_k) - f* by 1 - μ/L_f per step, and with step 2/(μ + L_f) shrinks the distance to x* by (κ - 1)/(κ + 1).
prereqs: [gradient-descent, strong-convexity, convergence-rate]
see_also: [gradient-descent-convergence-theorem, polyak-lojasiewicz-condition, condition-number-of-an-optimization-problem, nesterov-accelerated-gradient, momentum-method, first-order-lower-bound, exact-line-search]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Section 2.1.3, The class of smooth strongly convex functions (the inequality that combines smoothness and strong convexity), and Section 2.1.5, The gradient method (the linear rate with step 2/(μ + L))
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 3.4.2, Strongly convex and smooth functions
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.3.1, Convergence analysis (gradient descent on strongly convex functions with exact and backtracking line search)
  - paper: doi:10.1016/0041-5553(63)90382-3
    title: Boris T. Polyak, Gradient methods for the minimisation of functionals, USSR Computational Mathematics and Mathematical Physics 3(4), 1963
    locator: pages 864 to 878 (linear convergence of the gradient method under the gradient dominance condition)
  - paper: doi:10.1007/978-3-319-46128-1_50
    title: Hamed Karimi, Julie Nutini and Mark Schmidt, Linear convergence of gradient and proximal-gradient methods under the Polyak-Łojasiewicz condition, ECML PKDD 2016, Lecture Notes in Computer Science 9851
    locator: pages 795 to 811 (Theorem 1, the linear rate under the PL condition)
---

If $f$ is $L_f$-[smooth](/smoothness/) and $\mu$-[strongly convex](/strong-convexity/), [gradient descent](/gradient-descent/) converges linearly: with step $1/L_f$, $f(x_k) - f^* \le (1 - \mu/L_f)^k (f(x_0) - f^*)$, and with step $2/(\mu + L_f)$, $\|x_k - x^*\| \le \left(\frac{\kappa - 1}{\kappa + 1}\right)^k \|x_0 - x^*\|$, where $\kappa = L_f/\mu$ is the [condition number](/condition-number-of-an-optimization-problem/). So about $\kappa \ln(1/\varepsilon)$ steps reach accuracy $\varepsilon$. The second factor is attained exactly on a two-dimensional quadratic, so no fixed step size gives gradient descent a better dependence on $\kappa$. The first bound needs only the [Polyak-Lojasiewicz condition](/polyak-lojasiewicz-condition/), not convexity.

## Statement

**Theorem.** Let $f : \mathbb{R}^n \to \mathbb{R}$ be differentiable with $\|\nabla f(x) - \nabla f(y)\| \le L_f\|x - y\|$, and $\mu$-strongly convex with $0 < \mu \le L_f$:

$$f(y) \ge f(x) + \nabla f(x)^\top (y - x) + \frac{\mu}{2}\|y - x\|^2 \quad \text{for all } x, y.$$

Let $x^*$ be its unique minimizer, $f^* = f(x^*)$, $\kappa = L_f/\mu$, and $x_{k+1} = x_k - \alpha\nabla f(x_k)$.

1. If $\alpha = 1/L_f$, then for all $k \ge 0$
$$f(x_k) - f^* \le \left(1 - \frac{1}{\kappa}\right)^k (f(x_0) - f^*) \quad\text{and}\quad \|x_k - x^*\|^2 \le \left(1 - \frac{1}{\kappa}\right)^k \|x_0 - x^*\|^2.$$
2. If $\alpha = 2/(\mu + L_f)$, then for all $k \ge 0$
$$\|x_k - x^*\| \le \left(\frac{\kappa - 1}{\kappa + 1}\right)^k \|x_0 - x^*\| \quad\text{and}\quad f(x_k) - f^* \le \frac{L_f}{2}\left(\frac{\kappa - 1}{\kappa + 1}\right)^{2k}\|x_0 - x^*\|^2.$$
3. The value bound of part 1 holds for every $L_f$-smooth $f$ with a minimum value $f^*$ that satisfies $\frac12\|\nabla f(x)\|^2 \ge \mu(f(x) - f^*)$ for all $x$, with or without convexity.

## In plain words

Take a bowl that is curved at least a little in every direction and at most a fixed amount in every direction. Walk downhill with a fixed step. Then each step removes at least a fixed fraction of the remaining height, the same fraction every time. So the height shrinks like repeated halving, and each new correct digit costs the same number of steps.

That fraction depends on the ratio of the strongest curve to the weakest curve. If the ratio is ten, each step keeps at most nine tenths of the height. If it is a thousand, each step keeps almost all of it, and the walk is slow. A well chosen step size cannot repair this: a simple valley shaped like a stretched bowl makes every fixed step that slow.

## Proof

Write $g_k = \nabla f(x_k)$, and recall that $\nabla f(x^*) = 0$.

**Step 1 (descent).** By the descent lemma of [smoothness](/smoothness/), $f(x - g/L_f) \le f(x) - \frac{1}{2L_f}\|g\|^2$ with $g = \nabla f(x)$.

**Step 2 (gradient dominance).** The right side of the strong convexity inequality is a quadratic in $y$, minimized at $y = x - g/\mu$ with value $f(x) - \|g\|^2/(2\mu)$. So $f^* \ge f(x) - \|g\|^2/(2\mu)$, that is,

$$\tfrac12\|\nabla f(x)\|^2 \ge \mu(f(x) - f^*) \quad \text{for all } x.$$

**Part 3, and the values of part 1.** Steps 1 and 2 give $f(x_{k+1}) - f^* \le f(x_k) - f^* - \frac{1}{2L_f}\|g_k\|^2 \le (1 - \mu/L_f)(f(x_k) - f^*)$. Induction on $k$ gives the bound. Step 2 was the only use of convexity, so the same proof gives part 3.

**The distances of part 1.** By step 1 and $f(x_{k+1}) \ge f^*$, $\|g_k\|^2 \le 2L_f(f(x_k) - f^*)$. Strong convexity at $x = x_k$, $y = x^*$ gives $g_k^\top(x_k - x^*) \ge f(x_k) - f^* + \frac{\mu}{2}\|x_k - x^*\|^2$. Then

$$\|x_{k+1} - x^*\|^2 = \|x_k - x^*\|^2 - \frac{2}{L_f}g_k^\top(x_k - x^*) + \frac{1}{L_f^2}\|g_k\|^2 \le \left(1 - \frac{\mu}{L_f}\right)\|x_k - x^*\|^2 - \frac{2}{L_f}(f(x_k) - f^*) + \frac{2}{L_f}(f(x_k) - f^*),$$

and the last two terms cancel. Induction on $k$ gives the bound.

**Step 3 (a combined inequality).** For all $x, y$, with $u = x - y$ and $v = \nabla f(x) - \nabla f(y)$,

$$v^\top u \ge \frac{\mu L_f}{\mu + L_f}\|u\|^2 + \frac{1}{\mu + L_f}\|v\|^2.$$

*Proof.* If $\mu = L_f$, strong convexity added to itself with $x, y$ swapped gives $v^\top u \ge \mu\|u\|^2$, and the Lipschitz bound gives $\|v\| \le \mu\|u\|$, so the right side is at most $\frac{\mu}{2}\|u\|^2 + \frac{\mu}{2}\|u\|^2 \le v^\top u$. If $\mu < L_f$, let $\varphi(x) = f(x) - \frac{\mu}{2}\|x\|^2$. Strong convexity of $f$ is the convexity inequality $\varphi(y) \ge \varphi(x) + \nabla\varphi(x)^\top(y - x)$, so $\varphi$ is convex. The descent lemma for $f$ and the identity $-\frac{\mu}{2}\|y\|^2 + \frac{\mu}{2}\|x\|^2 + \mu x^\top(y - x) = -\frac{\mu}{2}\|y - x\|^2$ give $\varphi(y) \le \varphi(x) + \nabla\varphi(x)^\top(y - x) + \frac{L_f - \mu}{2}\|y - x\|^2$. For a convex function this upper bound implies co-coercivity ([smoothness](/smoothness/), conditions 2 and 4): $(\nabla\varphi(x) - \nabla\varphi(y))^\top u \ge \frac{1}{L_f - \mu}\|\nabla\varphi(x) - \nabla\varphi(y)\|^2$. Here $\nabla\varphi(x) - \nabla\varphi(y) = v - \mu u$, so

$$(L_f - \mu)(v^\top u - \mu\|u\|^2) \ge \|v\|^2 - 2\mu v^\top u + \mu^2\|u\|^2,$$

which rearranges to $(L_f + \mu)v^\top u \ge \|v\|^2 + \mu L_f\|u\|^2$. $\square$

**Part 2.** Apply step 3 with $x = x_k$, $y = x^*$, so $u = x_k - x^*$ and $v = g_k$. With $\alpha = 2/(\mu + L_f)$,

$$\|x_{k+1} - x^*\|^2 = \|u\|^2 - 2\alpha v^\top u + \alpha^2\|v\|^2 \le \left(1 - \frac{2\alpha\mu L_f}{\mu + L_f}\right)\|u\|^2 + \alpha\left(\alpha - \frac{2}{\mu + L_f}\right)\|v\|^2.$$

The second coefficient is $0$, and the first is $1 - \frac{4\mu L_f}{(\mu + L_f)^2} = \left(\frac{L_f - \mu}{L_f + \mu}\right)^2 = \left(\frac{\kappa - 1}{\kappa + 1}\right)^2$. Induction gives the distance bound. The value bound follows from the descent lemma at $x^*$: $f(x) - f^* \le \frac{L_f}{2}\|x - x^*\|^2$, since $\nabla f(x^*) = 0$. $\blacksquare$

## Consequences

- **Iteration counts.** Part 1 and $1 - 1/\kappa \le e^{-1/\kappa}$ give $f(x_k) - f^* \le \varepsilon$ for $k \ge \kappa\ln((f(x_0) - f^*)/\varepsilon)$. Part 2 gives $\|x_k - x^*\| \le \varepsilon$ for $k \ge \frac{\kappa + 1}{2}\ln(\|x_0 - x^*\|/\varepsilon)$, since $\ln\frac{\kappa + 1}{\kappa - 1} \ge \frac{2}{\kappa + 1}$.
- **Line searches.** With [exact line search](/exact-line-search/) or [backtracking](/backtracking-line-search/), the argument of part 1 still gives a linear rate, with $L_f$ replaced by a constant that depends on the line search parameters (Boyd and Vandenberghe, Section 9.3.1).
- **Without convexity.** Part 3 gives linear convergence for nonconvex functions with the [Polyak-Lojasiewicz condition](/polyak-lojasiewicz-condition/), such as $x^2 + 3\sin^2 x$ and least squares with a rank-deficient matrix.
- **Acceleration.** [Nesterov's method](/nesterov-accelerated-gradient/) and, on quadratics, [heavy ball momentum](/momentum-method/) improve $\kappa$ to $\sqrt{\kappa}$ in the step count, and the [first-order lower bound](/first-order-lower-bound/) shows that $\sqrt{\kappa}$ cannot be improved.
- **Iterates converge.** Unlike the convex case, the distance to $x^*$ falls at a linear rate, so the iterates themselves converge at a known speed.

## Tightness

Take $f(x) = \frac12(\mu x_1^2 + L_f x_2^2)$ on $\mathbb{R}^2$, with $x^* = 0$. Gradient descent with step $\alpha$ multiplies $x_1$ by $1 - \alpha\mu$ and $x_2$ by $1 - \alpha L_f$.

- **Part 2 is tight.** For $\alpha = 2/(\mu + L_f)$ both factors have the absolute value $\frac{L_f - \mu}{L_f + \mu} = \frac{\kappa - 1}{\kappa + 1}$, so from every start $\|x_k - x^*\| = \left(\frac{\kappa - 1}{\kappa + 1}\right)^k\|x_0 - x^*\|$ with equality. For every other constant step, $\max(|1 - \alpha\mu|, |1 - \alpha L_f|)$ is larger, so $2/(\mu + L_f)$ is the best constant step on this function, and no constant step gives a factor better than $1 - 2/(\kappa + 1)$.
- **Part 1 is tight up to a square.** For $\alpha = 1/L_f$ and $x_0 = (R, 0)$, $f(x_k) - f^* = (1 - 1/\kappa)^{2k}(f(x_0) - f^*)$ exactly. So the step count of part 1 is at most a factor of about $2$ larger than the true one on this function, and the step count of gradient descent grows linearly in $\kappa$ in all cases.

## History

Polyak proved in 1963 that the gradient method converges linearly when $\frac12\|\nabla f\|^2 \ge \mu(f - f^*)$, a condition that holds for strongly convex functions and that is now called the [Polyak-Lojasiewicz condition](/polyak-lojasiewicz-condition/). The rate with step $2/(\mu + L_f)$ and the combined inequality of step 3 are in Nesterov's lectures (Sections 2.1.3 and 2.1.5). Karimi, Nutini and Schmidt brought part 3 back to attention in 2016 for machine learning problems that are not strongly convex.

## References
