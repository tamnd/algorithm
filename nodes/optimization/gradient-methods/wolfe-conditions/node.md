---
tag: 0DGK2J
kind: definition
slug: wolfe-conditions
name: Wolfe conditions
aliases:
- strong Wolfe conditions
- curvature condition
- weak Wolfe conditions
area: optimization/gradient-methods
level: advanced
summary: A step passes if it gives sufficient decrease (Armijo) and the slope along d has risen enough (curvature). Such steps exist, give global convergence, and keep BFGS positive definite.
prereqs: [armijo-condition]
see_also: [armijo-condition, backtracking-line-search, bfgs, limited-memory-bfgs, nonlinear-conjugate-gradient, quasi-newton-method, step-size-selection, exact-line-search]
sources:
  - paper: doi:10.1137/1011036
    title: Philip Wolfe, Convergence conditions for ascent methods, SIAM Review 11(2), 1969
    locator: pages 226 to 235 (the conditions on the step and the convergence theorem)
  - paper: doi:10.1137/1013035
    title: Philip Wolfe, Convergence conditions for ascent methods. II, Some corrections, SIAM Review 13(2), 1971
    locator: pages 185 to 188
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 3.1, Step length (the Wolfe and strong Wolfe conditions, Lemma 3.1 on their existence), Section 3.2 (Zoutendijk's theorem, Theorem 3.2), and Section 3.5 (the line search of Algorithms 3.5 and 3.6)
  - paper: doi:10.1145/192115.192132
    title: Jorge J. Moré and David J. Thuente, Line search algorithms with guaranteed sufficient decrease, ACM Transactions on Mathematical Software 20(3), 1994
    locator: pages 286 to 307 (a line search that finds a strong Wolfe step in finitely many steps)
---

The Wolfe conditions are the standard acceptance test for a step $\alpha$ along a descent direction $d$ in line search methods. The first is the [Armijo condition](/armijo-condition/) $f(x + \alpha d) \le f(x) + c_1\alpha\nabla f(x)^\top d$, which asks for enough decrease. The second, the *curvature condition* $\nabla f(x + \alpha d)^\top d \ge c_2\nabla f(x)^\top d$ with $c_1 < c_2 < 1$, asks that the slope along $d$ has risen enough, which excludes steps that are too short. Steps that meet both always exist for a function that is bounded below, and under them every descent method with directions not too close to orthogonal to the gradient drives $\nabla f$ to zero (Zoutendijk's theorem). They also make $s^\top y > 0$, which keeps the [BFGS](/bfgs/) update positive definite.

## Definition

Let $f$ be differentiable, $d$ a descent direction at $x$, and $\varphi(\alpha) = f(x + \alpha d)$, so $\varphi'(\alpha) = \nabla f(x + \alpha d)^\top d$ and $\varphi'(0) < 0$. Fix $0 < c_1 < c_2 < 1$. A step $\alpha > 0$ satisfies the *Wolfe conditions* if

$$\text{(W1)}\quad \varphi(\alpha) \le \varphi(0) + c_1\alpha\varphi'(0), \qquad \text{(W2)}\quad \varphi'(\alpha) \ge c_2\varphi'(0).$$

It satisfies the *strong Wolfe conditions* if it satisfies (W1) and

$$\text{(W2s)}\quad |\varphi'(\alpha)| \le c_2|\varphi'(0)|.$$

(W2) says that the slope at the new point is less negative than $c_2$ times the starting slope: the line search has passed the steepest part of the descent. (W2s) also forbids a large positive slope, so the step cannot land far past a minimizer of $\varphi$. Typical constants are $c_1 = 10^{-4}$ with $c_2 = 0.9$ for Newton and quasi-Newton methods, and $c_2 = 0.1$ for [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/), which needs a more accurate step.

**Existence (Nocedal and Wright, Lemma 3.1).** Let $f$ be continuously differentiable and $\varphi$ bounded below on $[0, \infty)$. Then there are intervals of steps that satisfy the strong Wolfe conditions, and so the Wolfe conditions.

*Proof.* The line $\ell(\alpha) = \varphi(0) + c_1\alpha\varphi'(0)$ has a negative slope, so it is unbounded below, while $\varphi$ is bounded below. Since $\varphi(\alpha) < \ell(\alpha)$ for small $\alpha > 0$, the graphs cross; let $\alpha'$ be the smallest $\alpha > 0$ with $\varphi(\alpha') = \ell(\alpha')$. Then (W1) holds strictly on $(0, \alpha')$. By the mean value theorem there is $\alpha'' \in (0, \alpha')$ with $\varphi'(\alpha'')\alpha' = \varphi(\alpha') - \varphi(0) = c_1\alpha'\varphi'(0)$, so $\varphi'(\alpha'') = c_1\varphi'(0)$. Since $c_1 < c_2$ and $\varphi'(0) < 0$, $|\varphi'(\alpha'')| = c_1|\varphi'(0)| < c_2|\varphi'(0)|$, so $\alpha''$ satisfies (W1) strictly and (W2s) strictly. By continuity of $\varphi$ and $\varphi'$, all steps near $\alpha''$ satisfy them too. $\square$

**Positive curvature along the step.** If $\alpha$ satisfies (W2), let $s = \alpha d$ and $y = \nabla f(x + s) - \nabla f(x)$. Then

$$y^\top s = \alpha\left(\varphi'(\alpha) - \varphi'(0)\right) \ge \alpha(c_2 - 1)\varphi'(0) > 0.$$

This is the condition that the [BFGS](/bfgs/) and [L-BFGS](/limited-memory-bfgs/) updates need to keep their matrices positive definite, for every $f$, convex or not. The Armijo condition alone does not give it.

**Zoutendijk's theorem.** Let $f$ be bounded below, and let $\nabla f$ be $L_f$-Lipschitz on an open set that contains the level set $\{x : f(x) \le f(x_0)\}$. Let $x_{k+1} = x_k + \alpha_k d_k$, with each $d_k$ a descent direction and each $\alpha_k$ satisfying the Wolfe conditions. Let $\cos\theta_k = -\nabla f(x_k)^\top d_k / (\|\nabla f(x_k)\|\|d_k\|)$. Then

$$\sum_{k \ge 0}\cos^2\theta_k\,\|\nabla f(x_k)\|^2 < \infty.$$

*Proof.* Write $g_k = \nabla f(x_k)$. By (W2), $(g_{k+1} - g_k)^\top d_k \ge (c_2 - 1)g_k^\top d_k$. By the Lipschitz bound, $(g_{k+1} - g_k)^\top d_k \le \alpha_k L_f\|d_k\|^2$. Together,

$$\alpha_k \ge \frac{(c_2 - 1)\,g_k^\top d_k}{L_f\|d_k\|^2}.$$

Put this into (W1); since $g_k^\top d_k < 0$,

$$f(x_{k+1}) \le f(x_k) + c_1\alpha_k g_k^\top d_k \le f(x_k) - \frac{c_1(1 - c_2)}{L_f}\frac{(g_k^\top d_k)^2}{\|d_k\|^2} = f(x_k) - \frac{c_1(1 - c_2)}{L_f}\cos^2\theta_k\|g_k\|^2.$$

All iterates stay in the level set, since $f$ decreases. Add these inequalities for $k = 0, \ldots, K$: $\frac{c_1(1 - c_2)}{L_f}\sum_{k \le K}\cos^2\theta_k\|g_k\|^2 \le f(x_0) - \inf f < \infty$. $\square$

So if $\cos\theta_k \ge \delta > 0$ for all $k$, then $\|\nabla f(x_k)\| \to 0$. This holds for [gradient descent](/gradient-descent/) ($\cos\theta_k = 1$) and for $d_k = -B_k^{-1}\nabla f(x_k)$ when the matrices $B_k$ have uniformly bounded condition numbers.

## Examples and non-examples

**Example.** Take $f(x) = \frac12(x_1^2 + 10x_2^2)$, $x = (10, 1)$, $d = -\nabla f(x) = (-10, -10)$. Then $\varphi(\alpha) = 55 - 200\alpha + 550\alpha^2$ and $\varphi'(\alpha) = -200 + 1100\alpha$, with the minimizer $\alpha^* = 2/11 \approx 0.1818$. With $c_1 = 10^{-4}$:

| conditions | accepted steps |
|---|---|
| (W1) | $0 < \alpha \le 0.36360$ |
| Wolfe, $c_2 = 0.9$ | $0.01818 \le \alpha \le 0.36360$ |
| strong Wolfe, $c_2 = 0.9$ | $0.01818 \le \alpha \le 0.34545$ |
| strong Wolfe, $c_2 = 0.1$ | $0.16364 \le \alpha \le 0.2$ |

The bounds come from $-200 + 1100\alpha \ge -0.9 \cdot 200$, $|-200 + 1100\alpha| \le 180$ and $|-200 + 1100\alpha| \le 20$. Each set contains $\alpha^*$, and a smaller $c_2$ gives a narrower interval around it.

**Non-examples.**

- **Too short.** $\alpha = 0.01$ satisfies (W1), with $\varphi(0.01) = 53.055$, but $\varphi'(0.01) = -189 < -180$, so it fails (W2). The slope is still almost as steep as at the start.
- **Weak but not strong.** $\alpha = 0.36$ satisfies (W1) and (W2), since $\varphi'(0.36) = 196 \ge -180$. It fails (W2s) with $c_2 = 0.9$, since $196 > 180$. The step lands far past the minimizer, where $\varphi$ is rising steeply.
- **No Wolfe step.** If $\varphi$ is unbounded below, for example $f(x) = -x$ with $d = 1$, then $\varphi'(\alpha) = -1$ for all $\alpha$ and (W2) never holds. The existence lemma needs $\varphi$ bounded below.

## Related definitions

- The [Armijo condition](/armijo-condition/) is (W1). [Backtracking line search](/backtracking-line-search/) meets it without (W2); it avoids too-short steps by starting from a fixed trial step instead.
- The Goldstein conditions replace (W2) by the lower bound $\varphi(\alpha) \ge \varphi(0) + (1 - c)\alpha\varphi'(0)$, which does not give $y^\top s > 0$.
- A strong Wolfe line search by bracketing and zoom (Nocedal and Wright, Algorithms 3.5 and 3.6) or by the method of Moré and Thuente finds an acceptable step in finitely many evaluations. [BFGS](/bfgs/), [L-BFGS](/limited-memory-bfgs/) and [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/) use it.
- [Exact line search](/exact-line-search/) gives $\varphi'(\alpha) = 0$, so it meets (W2s) for every $c_2$, and it meets (W1) when $\varphi$ is a convex parabola and $c_1 \le \frac12$.

## References
