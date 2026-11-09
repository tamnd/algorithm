---
title: Dual ascent with step alpha <= mu/||A||^2 gives an O(1/k) dual gap and an O(1/k^(1/2)) primal error
proves: [correctness, convergence-rate]
status: full
---

The problem is $\min f(x)$ subject to $a_i^\top x = b_i$ for $i \notin I$ and $a_i^\top x \le b_i$ for $i \in I$. Write $A$ for the matrix with rows $a_i^\top$, $L(x, y) = f(x) + y^\top(Ax - b)$, $Y = \{y \in \mathbb{R}^m : y_i \ge 0 \text{ for } i \in I\}$ and $d(y) = \inf_x L(x, y)$. The method sets $x_k = \operatorname{argmin}_x L(x, y_k)$, $g_k = Ax_k - b$ and $y_{k+1} = P_Y(y_k + \alpha g_k)$, where $P_Y$ sets the negative entries with index in $I$ to zero. We assume:

- (A1) $f: \mathbb{R}^n \to \mathbb{R}$ is $\mu$-strongly convex with $\mu > 0$: $f - \tfrac{\mu}{2}\|\cdot\|^2$ is convex;
- (A2) the problem is feasible. Then it has a unique solution $x^*$, and since the constraints are linear and $f$ is finite on $\mathbb{R}^n$, strong duality holds and a dual solution $y^* \in Y$ exists (the refined [Slater condition](/slater-condition/) for affine constraints, Boyd and Vandenberghe, Section 5.2.3);
- (A3) $0 < \alpha \le \mu/\|A\|^2$, where $\|A\|$ is the spectral norm, and $y_0 \in Y$.

Write $\Lambda = \|A\|^2/\mu$, so $\alpha \le 1/\Lambda$. Since $\|A\| \le \|A\|_F$, the step $\alpha = \mu/\|A\|_F^2$ satisfies (A3).

**Lemma 1 (the dual is smooth).** For each $y$, $L(\cdot, y)$ has a unique minimizer $x(y)$. The function $d$ is finite and concave, $g(y) = Ax(y) - b$ is a supergradient of $d$ at $y$, $\|g(y) - g(y')\| \le \Lambda\|y - y'\|$, and for all $y, y'$:

$$d(y') \ge d(y) + g(y)^\top(y' - y) - \tfrac{\Lambda}{2}\|y' - y\|^2. \tag{S}$$

*Proof.* $L(\cdot, y)$ is $\mu$-strongly convex and finite, so it has a unique minimizer, and $d$ is finite. As an infimum of affine functions of $y$, $d$ is concave. For each $y'$, $d(y') \le L(x(y), y') = d(y) + g(y)^\top(y' - y)$, so $g(y)$ is a supergradient. Let $x = x(y)$ and $x' = x(y')$. The optimality conditions say $-A^\top y \in \partial f(x)$ and $-A^\top y' \in \partial f(x')$. Strong convexity makes $\partial f$ strongly monotone, so

$$\mu\|x - x'\|^2 \le (A^\top y' - A^\top y)^\top(x - x') = (y' - y)^\top A(x - x') \le \|y' - y\|\,\|A\|\,\|x - x'\|.$$

So $\|x - x'\| \le \|A\|\,\|y - y'\|/\mu$ and $\|g(y) - g(y')\| = \|A(x - x')\| \le \Lambda\|y - y'\|$. For (S), let $h = y' - y$ and $\varphi(t) = d(y + th)$, a finite concave function on $\mathbb{R}$. It is locally Lipschitz, so it is absolutely continuous, and at each $t$ where it is differentiable, $\varphi'(t) = g(y + th)^\top h$ because this number is a supergradient of $\varphi$ at $t$. So

$$\varphi(1) - \varphi(0) = \int_0^1 g(y + th)^\top h\,dt \ge \int_0^1 \big(g(y)^\top h - t\Lambda\|h\|^2\big)\,dt = g(y)^\top h - \tfrac{\Lambda}{2}\|h\|^2. \qquad \square$$

**Lemma 2 (one step).** Let $y \in \mathbb{R}^m$, $g = g(y)$ and $y^+ = P_Y(y + \alpha g)$. For each $z \in Y$,

$$d(y^+) \ge d(z) + \frac{1}{2\alpha}\big(\|y^+ - z\|^2 - \|y - z\|^2\big).$$

*Proof.* $Y$ is a closed convex set, so the projection satisfies $(y + \alpha g - y^+)^\top(z - y^+) \le 0$, that is, $g^\top(z - y^+) \le \tfrac1\alpha(y^+ - y)^\top(z - y^+)$. By (S) with $\Lambda \le 1/\alpha$, and by the supergradient inequality $d(z) \le d(y) + g^\top(z - y)$,

$$d(y^+) \ge d(y) + g^\top(y^+ - y) - \tfrac{1}{2\alpha}\|y^+ - y\|^2 \ge d(z) - g^\top(z - y^+) - \tfrac{1}{2\alpha}\|y^+ - y\|^2.$$

With the projection inequality, $d(y^+) \ge d(z) - \tfrac1\alpha\big[(y^+ - y)^\top(z - y^+) + \tfrac12\|y^+ - y\|^2\big]$. Expand $\|y - z\|^2 = \|(y - y^+) + (y^+ - z)\|^2$ to see that the bracket equals $\tfrac12(\|y - z\|^2 - \|y^+ - z\|^2)$. $\square$

**Theorem 1 (dual rate).** For each $k \ge 1$, $d(y_k)$ does not decrease with $k$, $\|y_k - y^*\|$ does not increase, and

$$d^* - d(y_k) \le \frac{\|y_0 - y^*\|^2}{2\alpha k}, \qquad d^* = d(y^*) = f(x^*).$$

*Proof.* Lemma 2 with $y = y_j$ and $z = y_j \in Y$ gives $d(y_{j+1}) \ge d(y_j) + \tfrac{1}{2\alpha}\|y_{j+1} - y_j\|^2$, so $d$ does not decrease. With $z = y^*$ it gives

$$d^* - d(y_{j+1}) \le \frac{1}{2\alpha}\big(\|y_j - y^*\|^2 - \|y_{j+1} - y^*\|^2\big),$$

and the left side is at least $0$, so $\|y_j - y^*\|$ does not increase. Add these for $j = 0, \ldots, k - 1$. The right side telescopes to at most $\|y_0 - y^*\|^2/(2\alpha)$, and each term on the left is at least $d^* - d(y_k)$ because $d$ does not decrease. $\square$

**Theorem 2 (primal error).** For each $k$, $\tfrac{\mu}{2}\|x_k - x^*\|^2 \le d^* - d(y_k)$. So $\|x_k - x^*\|^2 \le \|y_0 - y^*\|^2/(\alpha\mu k)$ for $k \ge 1$.

*Proof.* $L(\cdot, y_k)$ is $\mu$-strongly convex with minimizer $x_k$, so $L(x^*, y_k) \ge L(x_k, y_k) + \tfrac\mu2\|x^* - x_k\|^2 = d(y_k) + \tfrac\mu2\|x^* - x_k\|^2$. Also $L(x^*, y_k) = f(x^*) + \sum_i y_{k,i}(a_i^\top x^* - b_i) \le f(x^*)$: the terms with $i \notin I$ are $0$, and the terms with $i \in I$ are a product of $y_{k,i} \ge 0$ and $a_i^\top x^* - b_i \le 0$. So $\tfrac\mu2\|x_k - x^*\|^2 \le f(x^*) - d(y_k) = d^* - d(y_k)$. Theorem 1 gives the second claim. $\blacksquare$

**Remark (stopping).** If the method stops at line L5, then $\|y^+ - y\| \le \alpha\varepsilon$. When $I$ is empty this is $\|Ax - b\| \le \varepsilon$, and then $f(x) - d^* \ge -\|y^*\|\varepsilon$ and $f(x) - d(y) = -y^\top(Ax - b) \le \|y\|\varepsilon$, so the gap is known.
