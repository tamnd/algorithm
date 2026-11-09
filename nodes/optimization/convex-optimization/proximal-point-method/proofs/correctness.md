---
title: The proximal point method decreases f monotonically and reaches f(x_k) - f* <= ||x_0 - x*||^2 / (2 lambda k)
proves: [correctness, convergence-rate]
status: full
---

Let $f: \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ be closed, proper and convex, let $\lambda > 0$, and let $x_{k+1} = \operatorname{prox}_{\lambda f}(x_k)$, where

$$\operatorname{prox}_{\lambda f}(v) = \operatorname*{argmin}_z\ f(z) + \frac{1}{2\lambda}\|z - v\|^2.$$

**Step 0 (the map is well defined).** The function $z \mapsto f(z) + \|z - v\|^2/(2\lambda)$ is closed, proper and $1/\lambda$-strongly convex, so it has exactly one minimizer. So each iterate exists and is unique.

**Lemma 1 (the step gives a subgradient).** Let $g_{k+1} = (x_k - x_{k+1})/\lambda$. Then $g_{k+1} \in \partial f(x_{k+1})$.

*Proof.* $x_{k+1}$ minimizes $f(z) + \|z - x_k\|^2/(2\lambda)$. The quadratic term is differentiable everywhere, so the optimality condition is $0 \in \partial f(x_{k+1}) + (x_{k+1} - x_k)/\lambda$, by the sum rule for subdifferentials (one term is finite and differentiable on all of $\mathbb{R}^n$). $\square$

So line L3 computes a subgradient of $f$ at the new point, and for each $z$,

$$f(z) \ge f(x_{k+1}) + g_{k+1}^\top(z - x_{k+1}). \tag{S}$$

**Lemma 2 (descent).** $f(x_{k+1}) \le f(x_k) - \lambda\|g_{k+1}\|^2$. So the values are nonincreasing.

*Proof.* Put $z = x_k$ in (S): $f(x_k) \ge f(x_{k+1}) + g_{k+1}^\top(x_k - x_{k+1}) = f(x_{k+1}) + \lambda\|g_{k+1}\|^2$. $\square$

**Lemma 3 (one-step inequality).** For each $z$,

$$\lambda\big(f(x_{k+1}) - f(z)\big) \le \tfrac12\|x_k - z\|^2 - \tfrac12\|x_{k+1} - z\|^2 - \tfrac12\|x_k - x_{k+1}\|^2.$$

*Proof.* Multiply (S) by $\lambda$: $\lambda(f(x_{k+1}) - f(z)) \le (x_k - x_{k+1})^\top(x_{k+1} - z)$. With $a = x_k - z$ and $b = x_{k+1} - z$, the right side is $(a - b)^\top b = \tfrac12\|a\|^2 - \tfrac12\|b\|^2 - \tfrac12\|a - b\|^2$. $\square$

**Theorem.** Assume that $f$ has a minimizer $x^*$, and let $f^* = f(x^*)$. Then for each $k \ge 1$,

$$f(x_k) - f^* \le \frac{\|x_0 - x^*\|^2}{2\lambda k},$$

and $\|x_{k+1} - x^*\| \le \|x_k - x^*\|$ for each $k$.

*Proof.* Lemma 3 with $z = x^*$ gives $\lambda(f(x_{j+1}) - f^*) \le \tfrac12\|x_j - x^*\|^2 - \tfrac12\|x_{j+1} - x^*\|^2$. The left side is $\ge 0$, which gives the second claim. Add the inequalities for $j = 0, \ldots, k - 1$. The right side telescopes:

$$\lambda\sum_{j=1}^k\big(f(x_j) - f^*\big) \le \tfrac12\|x_0 - x^*\|^2 - \tfrac12\|x_k - x^*\|^2 \le \tfrac12\|x_0 - x^*\|^2.$$

By Lemma 2, $f(x_k)$ is the smallest of $f(x_1), \ldots, f(x_k)$, so the left side is at least $\lambda k(f(x_k) - f^*)$. Divide by $\lambda k$. $\square$

**Corollary (the certificate of line L5).** By (S) with $z = x^*$ and the Cauchy-Schwarz inequality, $f(x_k) - f^* \le g_k^\top(x_k - x^*) \le \|g_k\|\,\|x_k - x^*\| \le \|g_k\|\,\|x_0 - x^*\|$. So when the test $\|g_k\| \le \varepsilon$ of line L5 passes, $f(x_k) - f^* \le \varepsilon\|x_0 - x^*\|$. If $\varepsilon = 0$ and the test passes, then $0 \in \partial f(x_k)$ and $x_k$ is a minimizer.

**Theorem (strongly convex case).** If $f$ is $\mu$-strongly convex, then $\|x_{k+1} - x^*\| \le \|x_k - x^*\|/(1 + \lambda\mu)$, so $\|x_k - x^*\| \le (1 + \lambda\mu)^{-k}\|x_0 - x^*\|$.

*Proof.* Let $u, v$ be two points, $p = \operatorname{prox}_{\lambda f}(u)$ and $q = \operatorname{prox}_{\lambda f}(v)$. By Lemma 1, $(u - p)/\lambda \in \partial f(p)$ and $(v - q)/\lambda \in \partial f(q)$. Strong convexity makes the subdifferential strongly monotone: $\big((u - p) - (v - q)\big)^\top(p - q) \ge \lambda\mu\|p - q\|^2$. So $(u - v)^\top(p - q) \ge (1 + \lambda\mu)\|p - q\|^2$, and the Cauchy-Schwarz inequality gives $\|p - q\| \le \|u - v\|/(1 + \lambda\mu)$. The minimizer is a fixed point, $\operatorname{prox}_{\lambda f}(x^*) = x^*$, because $z = x^*$ satisfies the optimality condition $0 \in \partial f(z) + (z - x^*)/\lambda$, and by Step 0 the minimizer is unique. Put $u = x_k$ and $v = x^*$. $\blacksquare$
