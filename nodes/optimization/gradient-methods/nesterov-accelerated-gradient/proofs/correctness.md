---
title: Nesterov's method reaches 2L R^2/(k+1)^2 on smooth convex functions and the factor 1 - 1/√κ on strongly convex ones
proves: [correctness, termination, gradients.convex, gradients.strongly_convex]
status: full
---

**Setting.** Let $f : \mathbb{R}^n \to \mathbb{R}$ be convex and $L$-smooth, with a minimizer $x^*$, $f^* = f(x^*)$ and $R = \|x_0 - x^*\|$. NESTEROV-AGD has $K$ passes of the loop of line L2, so it terminates. In pass $k$ it computes, with $y_1 = x_0$, $t_1 = 1$ (line L1),

$$x_k = y_k - \tfrac1L\nabla f(y_k), \qquad t_{k+1} = \tfrac12\left(1 + \sqrt{1 + 4t_k^2}\right), \qquad y_{k+1} = x_k + \beta_k(x_k - x_{k-1}),$$

with $\beta_k = (t_k - 1)/t_{k+1}$ in the convex case and $\beta_k = (\sqrt\kappa - 1)/(\sqrt\kappa + 1)$, $\kappa = L/\mu$, in the strongly convex case.

**Lemma 1 (key inequality).** For all $y, z$, with $x^+ = y - \nabla f(y)/L$, $f(x^+) \le f(z) + \frac L2\left(\|y - z\|^2 - \|x^+ - z\|^2\right)$.

*Proof.* Let $g = \nabla f(y) = L(y - x^+)$. The descent lemma ([smoothness](/smoothness/)) gives $f(x^+) \le f(y) + g^\top(x^+ - y) + \frac L2\|x^+ - y\|^2 = f(y) - \frac{1}{2L}\|g\|^2$. Convexity gives $f(y) \le f(z) + g^\top(y - z)$. So

$$f(x^+) \le f(z) + L(y - x^+)^\top(y - z) - \frac L2\|y - x^+\|^2 = f(z) + \frac L2\left(\|y - z\|^2 - \|x^+ - z\|^2\right),$$

where the equality is the expansion of $\|x^+ - z\|^2 = \|(y - z) - (y - x^+)\|^2$. $\square$

**Lemma 2.** $t_{k+1}^2 - t_{k+1} = t_k^2$ and $t_k \ge (k + 1)/2$ for all $k \ge 1$.

*Proof.* $t_{k+1}$ is the positive root of $\tau^2 - \tau - t_k^2 = 0$. Also $t_{k+1} \ge \frac12(1 + 2t_k) = t_k + \frac12$, and $t_1 = 1 = (1 + 1)/2$, so $t_k \ge (k + 1)/2$ by induction. $\square$

**Claim 2 (convex case).** Let $v_k = f(x_k) - f^*$ and $u_k = t_kx_k - (t_k - 1)x_{k-1} - x^*$ for $k \ge 1$ (with $u_1 = x_1 - x^*$). Then $t_{k+1}^2v_{k+1} + \frac L2\|u_{k+1}\|^2 \le t_k^2v_k + \frac L2\|u_k\|^2$ for $k \ge 1$, and $t_1^2v_1 + \frac L2\|u_1\|^2 \le \frac L2R^2$. Hence $v_k \le LR^2/(2t_k^2) \le 2LR^2/(k + 1)^2$.

*Proof.* Base case: Lemma 1 with $y = y_1 = x_0$ and $z = x^*$ gives $v_1 \le \frac L2(R^2 - \|x_1 - x^*\|^2)$, which is the claim since $t_1 = 1$.

Step: write $t = t_{k+1} \ge 1$ and $z = (1 - 1/t)x_k + (1/t)x^*$. By convexity $f(z) \le (1 - 1/t)f(x_k) + (1/t)f^*$, so Lemma 1 with $y = y_{k+1}$ and $x^+ = x_{k+1}$ gives

$$v_{k+1} \le \left(1 - \tfrac1t\right)v_k + \frac L2\left(\|y_{k+1} - z\|^2 - \|x_{k+1} - z\|^2\right).$$

Multiply by $t^2$ and use $t^2 - t = t_k^2$ (Lemma 2):

$$t^2v_{k+1} \le t_k^2v_k + \frac L2\left(\|ty_{k+1} - (t - 1)x_k - x^*\|^2 - \|tx_{k+1} - (t - 1)x_k - x^*\|^2\right).$$

The second vector is $u_{k+1}$. For the first, $ty_{k+1} = tx_k + (t_k - 1)(x_k - x_{k-1})$, so $ty_{k+1} - (t - 1)x_k = t_kx_k - (t_k - 1)x_{k-1}$, and the first vector is $u_k$. This is the claimed inequality.

So the potential never exceeds its first value: $t_k^2v_k \le \frac L2R^2$, and $v_k \le LR^2/(2t_k^2) \le 2LR^2/(k + 1)^2$ by Lemma 2. $\square$

**Claim 3 (strongly convex case).** Let $f$ also be $\mu$-strongly convex, $0 < \mu \le L$, $s = \sqrt{\mu/L} = 1/\sqrt\kappa$ and $\beta = (1 - s)/(1 + s)$. Set $x_{-1} = x_0$ and $w_k = x_k + \beta(x_k - x_{k-1})$ for $k \ge 0$, so $w_0 = x_0 = y_1$, $w_k = y_{k+1}$ and $x_{k+1} = w_k - \nabla f(w_k)/L$. Let $z_k = x_k + (\sqrt\kappa - 1)(x_k - x_{k-1})$ and $\Phi_k = f(x_k) - f^* + \frac\mu2\|z_k - x^*\|^2$. Then $\Phi_{k+1} \le (1 - s)\Phi_k$ for $k \ge 0$, so $f(x_k) - f^* \le (1 - s)^k\Phi_0$ with $\Phi_0 = f(x_0) - f^* + \frac\mu2R^2 \le \frac{L + \mu}{2}R^2$.

*Proof.* First, the three points are related by $w_k = (x_k + sz_k)/(1 + s)$: indeed $x_k + sz_k = (1 + s)x_k + (1 - s)(x_k - x_{k-1})$, since $s(\sqrt\kappa - 1) = 1 - s$, and dividing by $1 + s$ gives $x_k + \beta(x_k - x_{k-1})$. Second, with $g = \nabla f(w_k)$,

$$z_{k+1} = (1 - s)z_k + sw_k - \frac s\mu g.$$

To check it, multiply both sides by $s$. Since $s^2/\mu = 1/L$, $sz_k = (1 + s)w_k - x_k$ and $g/L = w_k - x_{k+1}$, $s$ times the right side is $(1 - s)\left((1 + s)w_k - x_k\right) + s^2w_k - (w_k - x_{k+1}) = x_{k+1} - (1 - s)x_k$. Since $s(\sqrt\kappa - 1) = 1 - s$, $s$ times the left side is $sx_{k+1} + (1 - s)(x_{k+1} - x_k) = x_{k+1} - (1 - s)x_k$, which is the same.

Write $w = w_k$, $a = z_k - x^*$ and $b = w - x^* - g/\mu$, so $z_{k+1} - x^* = (1 - s)a + sb$. For any vectors, $\|(1 - s)a + sb\|^2 = (1 - s)\|a\|^2 + s\|b\|^2 - s(1 - s)\|a - b\|^2$. We use three inequalities:

- (a) the descent lemma: $f(x_{k+1}) \le f(w) - \frac{1}{2L}\|g\|^2$;
- (b) strong convexity at $w$: $f^* \ge f(w) + g^\top(x^* - w) + \frac\mu2\|x^* - w\|^2$;
- (c) convexity at $w$: $f(x_k) \ge f(w) + g^\top(x_k - w)$.

Expanding $\|b\|^2 = \|w - x^*\|^2 - \frac2\mu g^\top(w - x^*) + \frac{1}{\mu^2}\|g\|^2$ and using (b),

$$\frac\mu2s\|b\|^2 \le s(f^* - f(w)) + \frac{s}{2\mu}\|g\|^2.$$

Add (a) minus $f^*$. Since $\frac{s}{2\mu} - \frac{1}{2L} = \frac{1 - s}{2Ls}$ (because $\frac{s}{\mu} = \frac{1}{Ls}$),

$$\Phi_{k+1} \le (1 - s)\frac\mu2\|a\|^2 + (1 - s)(f(w) - f^*) + \frac{1 - s}{2Ls}\|g\|^2 - s(1 - s)\frac\mu2\|a - b\|^2.$$

By (c), $f(w) - f^* \le f(x_k) - f^* + g^\top(w - x_k)$, and $w - x_k = s(z_k - w)$ by the first relation. So it remains to show

$$s\,g^\top(z_k - w) + \frac{1}{2Ls}\|g\|^2 \le \frac{s\mu}{2}\|a - b\|^2.$$

Here $a - b = (z_k - w) + g/\mu$, so the right side is $\frac{s\mu}{2}\|z_k - w\|^2 + s\,g^\top(z_k - w) + \frac{s}{2\mu}\|g\|^2$. Since $\frac{s}{2\mu} = \frac{1}{2Ls}$, the inequality reduces to $0 \le \frac{s\mu}{2}\|z_k - w\|^2$, which is true. Hence $\Phi_{k+1} \le (1 - s)\left(\frac\mu2\|a\|^2 + f(x_k) - f^*\right) = (1 - s)\Phi_k$.

Finally $z_0 = x_0$, so $\Phi_0 = f(x_0) - f^* + \frac\mu2R^2$, and $f(x_0) - f^* \le \frac L2R^2$ by the descent lemma at $x^*$. Since $\frac\mu2\|z_k - x^*\|^2 \ge 0$, $f(x_k) - f^* \le \Phi_k \le (1 - s)^k\Phi_0$. $\square$
