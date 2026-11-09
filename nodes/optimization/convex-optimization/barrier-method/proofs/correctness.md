---
title: Each centered point of the barrier method has duality gap p/t, and each centering needs a bounded number of Newton steps
proves: [correctness, termination, complexity]
status: full
---

We use the notation of the page. The program is $\min c^\top x$ subject to $F(x) = F_0 + \sum_{i=1}^n x_i F_i \succeq 0$, with symmetric $p \times p$ matrices $F_i$. The dual program is $\max -\operatorname{tr}(F_0 Z)$ subject to $\operatorname{tr}(F_i Z) = c_i$ for $i = 1, \ldots, n$ and $Z \succeq 0$. The barrier is $\phi(x) = -\log\det F(x)$ on the set $\{x : F(x) \succ 0\}$, and $\phi_t(x) = t\, c^\top x + \phi(x)$. We assume:

- (A1) a strictly feasible $x^0$ is given, that is, $F(x^0) \succ 0$;
- (A2) the matrices $F_1, \ldots, F_n$ are linearly independent;
- (A3) for each $t > 0$ the sublevel sets of $\phi_t$ are bounded (this holds, for example, when the feasible set is bounded).

**Lemma 1 (derivatives of the barrier).** At a point $x$ with $F = F(x) \succ 0$,

$$\frac{\partial \phi}{\partial x_i} = -\operatorname{tr}(F^{-1} F_i), \qquad \frac{\partial^2 \phi}{\partial x_i \partial x_j} = \operatorname{tr}(F^{-1} F_i F^{-1} F_j),$$

and the Hessian is positive definite.

*Proof.* For a small symmetric $\Delta$, $\log\det(F + \Delta) = \log\det F + \operatorname{tr}(F^{-1}\Delta) + O(\|\Delta\|^2)$, and $(F + \Delta)^{-1} = F^{-1} - F^{-1}\Delta F^{-1} + O(\|\Delta\|^2)$. Put $\Delta = \sum_i h_i F_i$ to get the two formulas. For $h \ne 0$, let $H = \sum_i h_i F_i$, which is not $0$ by (A2), and let $G = F^{-1/2} H F^{-1/2}$. Then $h^\top \nabla^2\phi\, h = \operatorname{tr}(F^{-1} H F^{-1} H) = \operatorname{tr}(G^2) = \|G\|_F^2 > 0$. $\square$

So $\phi_t$ is strictly convex, and with (A3) it has exactly one minimizer $x^*(t)$, the central point for $t$. Lines L7 and L8 compute the gradient $g$ and the Hessian $H$ of $\phi_t$ by Lemma 1, and the Newton step $\Delta x = -H^{-1} g$. The Newton decrement is $\lambda(x)^2 = g^\top H^{-1} g = -g^\top \Delta x$.

**Lemma 2 (each iterate is strictly feasible).** Every point that the method makes satisfies $F(x) \succ 0$.

*Proof.* The start satisfies it by (A1). Line L10 accepts a trial point only if $\phi_t$ at the trial point is at most a finite number. Outside the open set $F(x) \succ 0$ the code gives $\phi_t$ the value $+\infty$, so such a point is never accepted. The backtracking ends, because for a small enough step $s$ the point $x + s\Delta x$ is inside the open set, and $\phi_t(x + s\Delta x) = \phi_t(x) - s\lambda^2 + O(s^2)$, which is less than $\phi_t(x) - \alpha s \lambda^2$ for small $s$ since $\alpha < 1$ and $\lambda > 0$. $\square$

**Lemma 3 (a central point gives a dual point and the gap $p/t$).** Let $x = x^*(t)$ and $Z = F(x)^{-1}/t$. Then $Z$ is dual feasible and $c^\top x + \operatorname{tr}(F_0 Z) = p/t$. So $c^\top x - f^* \le p/t$, where $f^*$ is the optimal value.

*Proof.* $Z \succ 0$, because $F(x) \succ 0$. The gradient of $\phi_t$ is $0$ at $x$, so by Lemma 1 $t c_i = \operatorname{tr}(F(x)^{-1} F_i)$, that is, $\operatorname{tr}(F_i Z) = c_i$. Then

$$c^\top x + \operatorname{tr}(F_0 Z) = \sum_i x_i \operatorname{tr}(F_i Z) + \operatorname{tr}(F_0 Z) = \operatorname{tr}(F(x) Z) = \operatorname{tr}(I)/t = p/t.$$

For each feasible $x'$, the same computation gives $c^\top x' + \operatorname{tr}(F_0 Z) = \operatorname{tr}(F(x') Z) \ge 0$, because the trace of a product of two positive semidefinite matrices is nonnegative. So $-\operatorname{tr}(F_0 Z) \le f^*$, and $c^\top x - f^* \le c^\top x + \operatorname{tr}(F_0 Z) = p/t$. $\square$

If the centering is not exact, the same computation with the residual $r_i = c_i - \operatorname{tr}(F_i Z)$ gives $c^\top x + \operatorname{tr}(F_0 Z) = p/t + \sum_i x_i r_i$. The residual is $g/t$, so it goes to $0$ with the gradient.

**Theorem 1 (the outer loop).** Let $t_k = \mu^k t_0$ for $k = 0, 1, \ldots$ with $\mu > 1$. The test of line L4 passes for the first time at

$$k^* = \max\left(0, \left\lceil \frac{\log(p/(t_0\varepsilon))}{\log\mu} \right\rceil\right),$$

so the method makes $k^* + 1$ centerings. If each centering is exact, the returned $x$ and $Z$ are feasible and $c^\top x - f^* \le c^\top x + \operatorname{tr}(F_0 Z) = p/t_{k^*} \le \varepsilon$.

*Proof.* Line L4 tests $p/t_k \le \varepsilon$, that is, $k \log\mu \ge \log(p/(t_0\varepsilon))$, and $k^*$ is the least such $k \ge 0$. The bound on the gap is Lemma 3 at $t = t_{k^*}$. $\square$

**Lemma 4 (how far the old center is from the new one).** Let $x = x^*(t)$ and $x^+ = x^*(\mu t)$. Then

$$\phi_{\mu t}(x) - \phi_{\mu t}(x^+) \le p(\mu - 1 - \log\mu).$$

*Proof.* Let $Z = F(x)^{-1}/t$. By Lemma 3, $c^\top x = p/t - \operatorname{tr}(F_0 Z)$ and $c^\top x^+ = \operatorname{tr}(F(x^+) Z) - \operatorname{tr}(F_0 Z)$. So $\mu t(c^\top x - c^\top x^+) = \mu p - \mu t \operatorname{tr}(F(x^+) Z)$. Let $W = F(x)^{-1/2} F(x^+) F(x)^{-1/2}$, which is positive definite with eigenvalues $w_1, \ldots, w_p > 0$. Then $t \operatorname{tr}(F(x^+) Z) = \operatorname{tr}(W)$ and $\log\det F(x^+) - \log\det F(x) = \log\det W$. So

$$\phi_{\mu t}(x) - \phi_{\mu t}(x^+) = \mu p - \sum_{j=1}^p (\mu w_j - \log w_j).$$

The function $w \mapsto \mu w - \log w$ has its minimum $1 + \log\mu$ at $w = 1/\mu$. So the right side is at most $\mu p - p(1 + \log\mu)$. $\square$

**Lemma 5 (Newton's method on a self-concordant function).** We use this theorem without proof (Boyd and Vandenberghe, Section 9.6.4). Let $f$ be strictly convex and self-concordant with a minimum $f^*$, and run Newton's method with backtracking parameters $0 < \alpha < 1/2$ and $0 < \beta < 1$, from $x_0$, and stop when $\lambda^2/2 \le \varepsilon_{nt}$. Then the number of Newton steps is at most

$$\frac{f(x_0) - f^*}{\gamma} + \log_2\log_2\frac{1}{\varepsilon_{nt}}, \qquad \gamma = \frac{\alpha\beta(1 - 2\alpha)^2}{20 - 8\alpha}.$$

The book states the count for the test $f(x) - f^* \le \varepsilon_{nt}$. Its proof bounds $\lambda^2$ in the quadratic phase by the same quantity that bounds $f(x) - f^*$, so the count also holds for the test of line L9.

The function $-\log\det F(x)$ is self-concordant: its restriction to a line is $-\sum_j \log(1 + s\,\sigma_j) + \text{const}$, a sum of self-concordant functions of $s$ (here $\sigma_j$ are the eigenvalues of $F^{-1/2} H F^{-1/2}$). Adding the linear term $t c^\top x$ keeps self-concordance, so Lemma 5 applies to $\phi_t$.

**Theorem 2 (Newton steps).** Under (A1) to (A3), each centering after the first starts at $x^*(t)$ and needs at most

$$N = \frac{p(\mu - 1 - \log\mu)}{\gamma} + \log_2\log_2\frac{1}{\varepsilon_{nt}}$$

Newton steps. The total number of Newton steps after the first centering is at most $k^* N$.

*Proof.* Apply Lemma 5 to $f = \phi_{\mu t}$ from $x_0 = x^*(t)$, and bound $f(x_0) - f^*$ by Lemma 4. There are $k^*$ centerings after the first one by Theorem 1. $\square$

**Corollary (the short-step choice).** With $\mu = 1 + 1/\sqrt{p}$, $\mu - 1 - \log\mu \le (\mu - 1)^2/2 = 1/(2p)$, because $\log(1 + u) \ge u - u^2/2$ for $u \ge 0$. So $N \le 1/(2\gamma) + \log_2\log_2(1/\varepsilon_{nt})$ is a constant, and $\log\mu \ge 1/(2\sqrt{p})$ for $p \ge 1$ (since $\log(1 + u) \ge u/2$ on $[0, 1]$), so $k^* \le \lceil 2\sqrt{p}\log(p/(t_0\varepsilon)) \rceil$. The total number of Newton steps after the first centering is $O(\sqrt{p}\log(p/(t_0\varepsilon)))$. $\blacksquare$
