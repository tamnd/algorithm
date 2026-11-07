---
title: Convergence of fixed-point iteration, global, local and of order q
proves: [correctness, termination]
status: full
---

We work in exact real arithmetic. The iterates are $x_{k+1} = g(x_k)$, and $e_k = x_k - x^*$.

**Theorem 1 (global).** Let $I$ be a closed interval, let $g(I) \subseteq I$, and let $|g(x) - g(y)| \le L|x - y|$ for all $x, y \in I$ with $0 \le L < 1$. Then $g$ has exactly one fixed point $x^* \in I$. For each $x_0 \in I$ the iterates stay in $I$, and for all $k \ge 1$:

1. $|e_k| \le L^k |e_0|$;
2. $|x_k - x^*| \le \frac{L}{1 - L}|x_k - x_{k-1}|$ (a posteriori bound);
3. $|x_k - x^*| \le \frac{L^k}{1 - L}|x_1 - x_0|$ (a priori bound).

*Proof.* The iterates stay in $I$ by induction, since $g(I) \subseteq I$. For $k \ge 1$, $|x_{k+1} - x_k| = |g(x_k) - g(x_{k-1})| \le L|x_k - x_{k-1}|$, so $|x_{k+1} - x_k| \le L^k|x_1 - x_0|$. For $j > k$,

$$|x_j - x_k| \le \sum_{i=k}^{j-1} |x_{i+1} - x_i| \le \sum_{i=k}^{j-1} L^i |x_1 - x_0| \le \frac{L^k}{1 - L}|x_1 - x_0|.$$

So $(x_k)$ is a Cauchy sequence. It has a limit $x^*$, which lies in $I$ because $I$ is closed. The map $g$ is continuous (it is Lipschitz), so $x^* = \lim x_{k+1} = \lim g(x_k) = g(x^*)$. If $y^* \in I$ is another fixed point, then $|x^* - y^*| = |g(x^*) - g(y^*)| \le L|x^* - y^*|$, and $L < 1$ forces $x^* = y^*$.

For item 1, $|e_{k}| = |g(x_{k-1}) - g(x^*)| \le L|e_{k-1}|$, and induction gives $|e_k| \le L^k|e_0|$. For item 2, $|x_k - x^*| \le |x_k - x_{k+1}| + |x_{k+1} - x^*| \le L|x_k - x_{k-1}| + L|x_k - x^*|$, and we solve for $|x_k - x^*|$. Item 3 follows from the display when $j \to \infty$. $\square$

**Corollary (the stop test).** Under Theorem 1, if line L1 sets $\tau = \delta(1-L)/L$ with $L > 0$ and line L6 returns $y = x_{k}$ because $|x_k - x_{k-1}| \le \tau$, then $|y - x^*| \le \frac{L}{1-L}\tau = \delta$ by item 2. The test holds at the latest when $\frac{L^{k-1}}{1}|x_1 - x_0| \le \tau$, because $|x_k - x_{k-1}| \le L^{k-1}|x_1 - x_0|$. So FIXED-POINT stops after at most $1 + \lceil \log(|x_1 - x_0|/\tau)/\log(1/L) \rceil$ steps, a finite number. If $L = 0$, $g$ is constant on $I$ and $x_1 = x^*$; the test with any $\tau \ge 0$ holds at step 2. $\square$

**Theorem 2 (local).** Let $g$ be $C^1$ on an open interval around a fixed point $x^*$, with $|g'(x^*)| < 1$. Then there is $\rho > 0$ such that, for each $x_0$ with $|x_0 - x^*| \le \rho$, the iterates converge to $x^*$, and $e_{k+1}/e_k \to g'(x^*)$ when no $e_k$ is zero.

*Proof.* Choose $L$ with $|g'(x^*)| < L < 1$. By continuity of $g'$ there is $\rho > 0$ with $|g'(x)| \le L$ for $|x - x^*| \le \rho$. Let $I = [x^* - \rho, x^* + \rho]$. For $x \in I$, the mean value theorem gives $\xi$ between $x$ and $x^*$ with $|g(x) - x^*| = |g'(\xi)||x - x^*| \le L\rho$, so $g(I) \subseteq I$. The same theorem shows $|g(x) - g(y)| \le L|x - y|$ on $I$. Theorem 1 applies. For the ratio, $e_{k+1} = g(x_k) - g(x^*) = g'(\xi_k) e_k$ with $\xi_k$ between $x_k$ and $x^*$. Since $x_k \to x^*$, also $\xi_k \to x^*$, and $g'(\xi_k) \to g'(x^*)$ by continuity. $\square$

**Theorem 3 (order $q$).** Let $q \ge 2$, let $g$ be $C^q$ near $x^*$, and let $g'(x^*) = \cdots = g^{(q-1)}(x^*) = 0$ and $g^{(q)}(x^*) \ne 0$. Then the convergence of Theorem 2 holds, and $e_{k+1}/e_k^q \to g^{(q)}(x^*)/q!$ when no $e_k$ is zero. So the order is exactly $q$ with rate constant $C = |g^{(q)}(x^*)|/q!$.

*Proof.* Since $g'(x^*) = 0$, Theorem 2 gives convergence for $x_0$ close enough. Taylor's theorem with the Lagrange remainder at $x^*$ gives $g(x_k) = g(x^*) + \frac{g^{(q)}(\xi_k)}{q!} e_k^q$ with $\xi_k$ between $x_k$ and $x^*$, because the terms of order 1 to $q - 1$ vanish. So $e_{k+1} = \frac{g^{(q)}(\xi_k)}{q!} e_k^q$, and $\xi_k \to x^*$ with continuity of $g^{(q)}$ gives the limit. $\square$

**Theorem 4 (repulsion).** Let $g$ be $C^1$ near $x^*$ with $|g'(x^*)| > 1$. If $x_k \to x^*$, then $x_k = x^*$ for all large $k$.

*Proof.* Choose $\lambda$ with $1 < \lambda < |g'(x^*)|$ and $\rho > 0$ with $|g'(x)| \ge \lambda$ for $|x - x^*| \le \rho$. If $x_k \to x^*$, then $|e_k| \le \rho$ for all $k \ge K$. For such $k$, the mean value theorem gives $|e_{k+1}| = |g'(\xi_k)||e_k| \ge \lambda|e_k|$. If $e_K \ne 0$, then $|e_{K+j}| \ge \lambda^j |e_K| \to \infty$, which contradicts $|e_k| \le \rho$. So $e_K = 0$, and then $e_k = 0$ for all $k \ge K$. $\square$

**Termination of FIXED-POINT.** The loop of lines L3 to L7 runs at most $k_{\max}$ times, and each pass either returns or goes on, so the procedure always ends. Under Theorem 1 with the scaled tolerance, the corollary shows that it returns at line L6 with error at most $\delta$ once $k_{\max}$ is at least the bound given there. $\blacksquare$
