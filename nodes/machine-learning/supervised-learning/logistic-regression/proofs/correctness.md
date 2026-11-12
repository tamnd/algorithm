---
title: Damped Newton (IRLS) converges to the logistic regression estimate when it exists
proves: [correctness, termination]
status: full
---

Let $J(\theta) = \sum_i[\log(1 + e^{z_i}) - y_i z_i] + \frac{\lambda}{2}\|w\|^2$ with $z_i = \tilde x_i^\top\theta$ and $\theta = (b, w)$. Let $g(\theta) = \nabla J = \tilde X^\top(p - y) + \lambda(0, w)$ and $H(\theta) = \nabla^2 J = \tilde X^\top S\tilde X + \lambda\operatorname{diag}(0, I)$. Arithmetic is exact in this proof.

**Assumption.** The sublevel set $\mathcal{S} = \{\theta : J(\theta) \le J(0)\}$ is bounded, and $H(\theta)$ is positive definite on it. This holds in two cases. (i) $\lambda > 0$ and both labels occur: each direction $(u_b, u_w)$ with $u_w \ne 0$ makes the penalty grow quadratically, and the direction $(u_b, 0)$ makes $\log(1 + e^{z_i}) - y_iz_i$ grow linearly for some $i$ of the label opposite to the sign of $u_b$. Also $u^\top H u \ge \sum_i s_i u_b^2 + \lambda\|u_w\|^2 > 0$. (ii) $\lambda = 0$, $\tilde X$ has full column rank and the data overlap in the sense of Albert and Anderson (1984): then $J$ grows linearly along every direction (Albert and Anderson, Section 3), and $\tilde X^\top S\tilde X$ is positive definite because $S$ has positive entries.

**Lemma 1 (convexity and bounds).** $J$ is convex. There are constants $0 < m \le M$ with $u^\top H(\theta)u \ge m\|u\|^2$ for $\theta \in \mathcal{S}$ and $u^\top H(\theta) u \le M\|u\|^2$ for all $\theta$.

*Proof.* $p_i(1 - p_i) \in (0, 1/4]$, so $H(\theta) \succeq 0$ everywhere, and $H(\theta) \preceq M I$ with $M = \frac14\|\tilde X\|_2^2 + \lambda$. $\mathcal{S}$ is closed and bounded, and the smallest eigenvalue of $H$ is a continuous positive function on it, so it has a positive minimum $m$. $\square$

**Lemma 2 (each step).** Let $\theta \in \mathcal{S}$ with $g \ne 0$, and let $\delta = H(\theta)^{-1}g$. Then $g^\top\delta \ge \|g\|^2/M > 0$ and $\|\delta\|^2 \le g^\top\delta/m$. The loop of line L7 stops with $t \ge t_{\min} = \min(1, 3m/(4M))$, and the new point has $J(\theta - t\delta) \le J(\theta) - \frac{t_{\min}}{4M}\|g\|^2$.

*Proof.* $g^\top\delta = g^\top H^{-1}g \ge \|g\|^2/M$, since the eigenvalues of $H^{-1}$ are at least $1/M$. Also $g^\top\delta = \delta^\top H\delta \ge m\|\delta\|^2$. By Taylor's theorem with the bound $H \preceq MI$ along the segment, $J(\theta - t\delta) \le J(\theta) - t g^\top\delta + \frac{M t^2}{2}\|\delta\|^2 \le J(\theta) - t g^\top\delta\left(1 - \frac{Mt}{2m}\right)$. For $t \le 3m/(2M)$ the factor is at least $1/4$, so the test of line L7 passes. The loop halves $t$ from 1, so it stops at some $t \ge \min(1, \frac12\cdot\frac{3m}{2M}) = t_{\min}$. The accepted step lowers $J$ by at least $\frac{t}{4}g^\top\delta \ge \frac{t_{\min}}{4M}\|g\|^2$. $\square$

Since $J$ never increases, all iterates stay in $\mathcal{S}$, and Lemma 2 applies at each of them.

**Termination.** Adding Lemma 2 over the steps gives $\frac{t_{\min}}{4M}\sum_k \|g_k\|^2 \le J(0) - \inf J < \infty$, because $J \ge 0$. So $\|g_k\| \to 0$, and $\|\delta_k\| \le \|g_k\|/m \to 0$ by Lemma 2. The step length $t_k\|\delta_k\| \le \|\delta_k\|$ falls below $\text{tol}\,(1 + \|\theta_k\|)$ for some $k$, and line L8 stops.

**Theorem.** Under the assumption, $J$ has exactly one minimizer $\hat\theta$, and without the stopping test the iterates converge to it. With tol $> 0$, the output has $\|g\| \le M\,\text{tol}\,(1 + \|\theta\|)/t_{\min}$ at the previous iterate, so it solves the score equations up to an error of order tol.

*Proof.* $J$ is continuous on the compact set $\mathcal{S}$, so it has a minimizer there, which is a global minimizer. $J$ is strictly convex on the convex set $\mathcal{S}$ by Lemma 1, so the minimizer is unique, and it is the only point of $\mathcal{S}$ with $g = 0$. The iterates lie in the compact $\mathcal{S}$ and $g$ is continuous, so every limit point $\theta^\star$ has $g(\theta^\star) = 0$, hence $\theta^\star = \hat\theta$. A bounded sequence whose limit points are all $\hat\theta$ converges to $\hat\theta$. At the stop, $t\|\delta\| \le \text{tol}(1 + \|\theta\|)$ with $t \ge t_{\min}$, and $\|g\| \le M\|\delta\|$, which gives the bound. $\blacksquare$

**Remark (separable data).** If the data are completely separated by some $\theta_s$, then $J$ with $\lambda = 0$ has no minimizer: $J(t\theta_s) \to 0 = \inf J$ while $J > 0$. Then $\mathcal{S}$ is not bounded, the assumption fails, and the stopping test of line L8 need not be met, which is why the implementation also has a limit on the number of steps.
