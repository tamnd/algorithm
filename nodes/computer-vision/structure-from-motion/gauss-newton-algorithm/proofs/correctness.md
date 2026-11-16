---
title: The Gauss-Newton step minimizes the linear model and converges locally, quadratically when the residual at the solution is zero
proves: [correctness]
status: full
---

We use the notation of the page. The residual is $r: \mathbb{R}^n \to \mathbb{R}^m$ with $m \ge n$, the cost is $F(x) = \tfrac12 \|r(x)\|^2$, $J(x)$ is the $m \times n$ Jacobian of $r$, $A(x) = J(x)^{\mathsf T} J(x)$ and $g(x) = J(x)^{\mathsf T} r(x)$. The second derivative term is $S(x) = \sum_{i=1}^m r_i(x) \nabla^2 r_i(x)$. Then $\nabla F = g$ and $\nabla^2 F = A + S$.

**Claim.** (a) If $J(x)$ has full column rank, line L6 is well defined, its step $h$ is the unique minimizer of the linear model $L(h) = \tfrac12 \|r + J h\|^2$, and $h$ is a descent direction of $F$ whenever $g \ne 0$. (b) Let $x^*$ be a stationary point ($g(x^*) = 0$) such that $J(x^*)$ has full column rank, and let $r$ be twice differentiable with Lipschitz continuous first and second derivatives near $x^*$. Then the error $e_k = x_k - x^*$ satisfies
$$e_{k+1} = -A_*^{-1} S_* \, e_k + O(\|e_k\|^2), \qquad A_* = A(x^*), \; S_* = S(x^*).$$
(c) As a consequence, if $S_* = 0$ (in particular if $r(x^*) = 0$), the iteration converges quadratically from every start close enough to $x^*$. If $\|A_*^{-1} S_*\| < 1$ in some operator norm, it converges at least linearly. If $n = 1$ and $|A_*^{-1} S_*| > 1$, no start $x_0 \ne x^*$ gives iterates that stay in a small neighborhood of $x^*$, so the full step method does not converge to $x^*$ except by landing on it exactly.

**Proof of (a).** $L(h) = \tfrac12 r^{\mathsf T} r + h^{\mathsf T} g + \tfrac12 h^{\mathsf T} A h$ is a quadratic in $h$ with Hessian $A$. If $J$ has full column rank, then $h^{\mathsf T} A h = \|J h\|^2 > 0$ for $h \ne 0$, so $A$ is positive definite, its Cholesky factorization exists, and $L$ has the unique minimizer given by $\nabla L = g + A h = 0$, which is the system of line L6. If $g \ne 0$, then $h \ne 0$ and $\nabla F^{\mathsf T} h = g^{\mathsf T} h = -h^{\mathsf T} A h < 0$, so $h$ is a descent direction. $\square$

**Proof of (b).** Let $B$ be a closed ball around $x^*$ in which the derivatives of $r$ up to order 2 are Lipschitz. Then $A$, $S$ and $\nabla^2 F = A + S$ are Lipschitz on $B$. Because $A_*$ is positive definite and $A$ is continuous, we can shrink $B$ so that $A(x)$ is invertible on $B$ with $\|A(x)^{-1}\| \le 2 \|A_*^{-1}\|$. Then $A(x)^{-1} - A_*^{-1} = A(x)^{-1} (A_* - A(x)) A_*^{-1} = O(\|e\|)$.

Taylor's theorem with a Lipschitz Hessian gives $g(x) = g(x^*) + (A_* + S_*) e + O(\|e\|^2) = (A_* + S_*) e + O(\|e\|^2)$, with $e = x - x^*$. Lines L6 and L7 give $x_+ = x - A(x)^{-1} g(x)$, so
$$e_+ = e - A(x)^{-1} (A_* + S_*) e + O(\|e\|^2) = e - A_*^{-1} (A_* + S_*) e + O(\|e\|^2) = -A_*^{-1} S_* e + O(\|e\|^2).$$
In the second step we replaced $A(x)^{-1}$ by $A_*^{-1}$ at the cost $O(\|e\|) \cdot O(\|e\|)$. $\square$

**Proof of (c).** By (b) there are $\delta > 0$ and $C$ with $\|e_+ - M e\| \le C \|e\|^2$ for $\|e\| \le \delta$, where $M = -A_*^{-1} S_*$.

If $S_* = 0$, then $\|e_+\| \le C \|e\|^2$. For $\|e_0\| \le \min(\delta, 1/(2C))$, induction gives $\|e_{k+1}\| \le C \|e_k\|^2 \le \tfrac12 \|e_k\|$, so every iterate stays in the ball and the convergence is quadratic. If $r(x^*) = 0$, then every $r_i(x^*) = 0$ and $S_* = 0$.

If $\|M\| = c < 1$ in an operator norm, pick $\epsilon$ with $c + C \epsilon < 1$ (with $C$ taken for this norm). For $\|e_0\| \le \min(\delta, \epsilon)$, $\|e_{k+1}\| \le (c + C \|e_k\|) \|e_k\| \le (c + C\epsilon) \|e_k\|$, which is linear convergence.

If $n = 1$ and $|M| > 1$, let $q = (|M| + 1)/2 > 1$ and pick $\epsilon \le \delta$ with $C \epsilon \le |M| - q$. For $0 < |e| \le \epsilon$, $|e_+| \ge |M| |e| - C |e|^2 \ge q |e|$. So while the iterates stay in $(x^* - \epsilon, x^* + \epsilon)$ and differ from $x^*$, their distance to $x^*$ grows by the factor $q$ at each step, and after finitely many steps an iterate leaves the interval. $\square$

**The example of Madsen, Nielsen and Tingleff.** Take $n = 1$, $m = 2$ and $r(x) = (x + 1, \lambda x^2 + x - 1)$. At $x^* = 0$, $r = (1, -1)$, $J = (1, 1)^{\mathsf T}$ and $g = 1 - 1 = 0$, so $0$ is stationary, $A_* = 2$ and $S_* = 1 \cdot 0 + (-1) \cdot 2\lambda = -2\lambda$. So $M = \lambda$ and $e_{k+1} = \lambda e_k + O(e_k^2)$. Also $F''(0) = A_* + S_* = 2 - 2\lambda$, so $0$ is a strict local minimizer for every $\lambda < 1$. For $\lambda = -2$, $F'(x) = (x + 1) + (-2x^2 + x - 1)(1 - 4x) = x (8x^2 - 6x + 6)$, and $8x^2 - 6x + 6$ has a negative discriminant, so $0$ is the only stationary point and the global minimizer, with $F(0) = 1$. Yet $|M| = 2 > 1$, so by (c) the full step method does not converge to it. The tests of the reference code check both the linear rate $0.5$ for $\lambda = 0.5$ and the escape for $\lambda = -2$.

**Stopping rules.** Line L5 stops at an approximate stationary point. Line L8 stops when the step is small relative to $x$. Neither guarantees a minimizer. The method has no globalization, so far from $x^*$ the cost can increase. With a line search that satisfies the Wolfe conditions and a Jacobian whose singular values are bounded away from zero on the level set, $J_k^{\mathsf T} r_k \to 0$ (Nocedal and Wright, Theorem 10.1); that variant is not the one in the reference code.
