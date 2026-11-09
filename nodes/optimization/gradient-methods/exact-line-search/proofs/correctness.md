---
title: Exact line search brackets and locates the minimizer, and steepest descent with exact steps meets the Kantorovich rate
proves: [correctness, termination]
status: full
---

**Statement.** Let $\varphi : [0, \infty) \to \mathbb{R}$ be strictly unimodal with minimizer $a^* \ge 0$: strictly decreasing on $[0, a^*]$ and strictly increasing on $[a^*, \infty)$. Let $h > 0$ and $\tau > 0$. Then, in exact arithmetic:

1. The loop of line L4 runs its body at most $\max(0, \lceil\log_2(a^*/h)\rceil)$ times, and after line L5 (or after line L1) $a^* \in [lo, hi]$.
2. Each pass of lines L8 and L9 keeps $a^* \in [lo, hi]$ and multiplies $hi - lo$ by $r = (\sqrt5 - 1)/2$. The loop of L7 stops after $\max(0, \lceil\log_{1/r}(w/\tau)\rceil)$ passes, where $w$ is the width after bracketing, and the returned $\hat{\alpha}$ satisfies $|\hat{\alpha} - a^*| \le \tau/2$.
3. If $f(x) = \frac12x^\top Ax - b^\top x$, $g = Ax - b$, $g^\top d < 0$ and $d^\top Ad > 0$, then $\varphi(\alpha) = f(x + \alpha d)$ has the unique minimizer $\alpha^* = -g^\top d/(d^\top Ad) > 0$ on $[0, \infty)$.
4. If $f$ is differentiable and $\alpha^* > 0$ minimizes $\varphi$, then $\nabla f(x + \alpha^*d)^\top d = 0$.

Let $x_{k+1} = x_k - \alpha_k g_k$ with $g_k = \nabla f(x_k)$ and $\alpha_k$ a minimizer of $\varphi_k(\alpha) = f(x_k - \alpha g_k)$ over $\alpha \ge 0$.

5. If $f(x) = \frac12(x - x^*)^\top A(x - x^*) + f^*$ with $A$ symmetric and its eigenvalues in $[\mu, L]$, $0 < \mu \le L$, then $f(x_{k+1}) - f^* \le \left(\frac{L - \mu}{L + \mu}\right)^2(f(x_k) - f^*)$.
6. If $f$ is $\mu$-strongly convex and $L_f$-smooth, then $f(x_{k+1}) - f^* \le (1 - \mu/L_f)(f(x_k) - f^*)$.
7. If $f$ is convex and $L_f$-smooth with a minimizer $x^*$, and $\|x - x^*\| \le D_0$ for all $x$ with $f(x) \le f(x_0)$, then $f(x_k) - f^* \le 2L_fD_0^2/k$ for $k \ge 1$.

**Proof of 1.** If line L1 finds $\varphi(h) \ge \varphi(0)$, then $a^* < h$ or $a^* = 0$: if $a^* \ge h > 0$, $\varphi$ is strictly decreasing on $[0, h]$ and $\varphi(h) < \varphi(0)$. So $a^* \in [0, h] = [lo, hi]$. Otherwise $\varphi(h) < \varphi(0)$, and before each test of L4 the invariant $\varphi(mid) < \varphi(lo)$ holds with $lo < mid < hi$: it holds at L3, and a pass of L5 is taken only when $\varphi(hi) < \varphi(mid)$, which is the invariant for the new $(mid, hi)$. The invariant gives $a^* > lo$, since $a^* \le lo$ would make $\varphi$ strictly increasing on $[lo, mid]$. When the loop stops, $\varphi(hi) \ge \varphi(mid)$, which gives $a^* < hi$, since $a^* \ge hi$ would make $\varphi$ strictly decreasing on $[mid, hi]$. So $a^* \in (lo, hi)$. After $j$ passes of L5, $mid = 2^jh$. If $mid \ge a^*$, then $\varphi$ is strictly increasing on $[mid, hi]$ and the loop stops. So the body runs only while $2^jh < a^*$, that is, at most $\max(0, \lceil\log_2(a^*/h)\rceil)$ times.

**Proof of 2.** Let $lo < u < v < hi$ as computed at L8 (since $r > \frac12$, $u = hi - r(hi - lo) < lo + r(hi - lo) = v$). If $\varphi(u) < \varphi(v)$, then $a^* < v$: otherwise $a^* \ge v$ and $\varphi$ is strictly decreasing on $[u, v]$, so $\varphi(u) > \varphi(v)$. So $a^* \in [lo, v]$, and L9 sets $hi \leftarrow v$. If $\varphi(u) \ge \varphi(v)$, then $a^* > u$: otherwise $a^* \le u$ and $\varphi$ is strictly increasing on $[u, v]$, so $\varphi(u) < \varphi(v)$. So $a^* \in [u, hi]$, and L9 sets $lo \leftarrow u$. In both cases the new width is $v - lo = hi - u = r(hi - lo)$. After $j$ passes the width is $r^jw$, which is at most $\tau$ once $j \ge \log_{1/r}(w/\tau)$. Finally $a^* \in [lo, hi]$ with $hi - lo \le \tau$, so the midpoint $\hat{\alpha}$ is within $\tau/2$ of $a^*$.

**Proof of 3.** Expanding, $\varphi(\alpha) = f(x) + \alpha g^\top d + \frac{\alpha^2}{2}d^\top Ad$, a parabola with positive leading coefficient. Its only stationary point is $\alpha^* = -g^\top d/(d^\top Ad)$, which is positive because $g^\top d < 0 < d^\top Ad$. It is the minimizer over $\mathbb{R}$ and so over $[0, \infty)$.

**Proof of 4.** $\alpha^*$ is an interior minimizer of the differentiable function $\varphi$ on $[0, \infty)$, so $\varphi'(\alpha^*) = \nabla f(x + \alpha^*d)^\top d = 0$.

**Proof of 5.** Write $e = x_k - x^*$ and $g = g_k = Ae$, and let $E(x) = f(x) - f^*$, so $E(x_k) = \frac12e^\top Ae = \frac12g^\top A^{-1}g$. If $g = 0$ there is nothing to prove. By claim 3 with $d = -g$, $\alpha_k = g^\top g/(g^\top Ag)$, and

$$E(x_{k+1}) = E(x_k) - \alpha_kg^\top g + \frac{\alpha_k^2}{2}g^\top Ag = E(x_k) - \frac{(g^\top g)^2}{2g^\top Ag} = E(x_k)\left(1 - \frac{(g^\top g)^2}{(g^\top Ag)(g^\top A^{-1}g)}\right).$$

*Kantorovich inequality.* For every $z \ne 0$, $\frac{(z^\top z)^2}{(z^\top Az)(z^\top A^{-1}z)} \ge \frac{4\mu L}{(\mu + L)^2}$. To see it, write $z$ in an orthonormal basis of eigenvectors of $A$, $z = \sum_i z_iq_i$ with eigenvalues $\lambda_i \in [\mu, L]$. For each $\lambda \in [\mu, L]$, $(\lambda - \mu)(\lambda - L) \le 0$, that is, $\lambda + \mu L/\lambda \le \mu + L$. Multiply by $z_i^2$ and add over $i$:

$$z^\top Az + \mu L\,z^\top A^{-1}z \le (\mu + L)\,z^\top z.$$

By the inequality of the arithmetic and geometric means, the left side is at least $2\sqrt{\mu L\,(z^\top Az)(z^\top A^{-1}z)}$. Squaring gives $4\mu L(z^\top Az)(z^\top A^{-1}z) \le (\mu + L)^2(z^\top z)^2$, which is the claim.

With $z = g$, $E(x_{k+1}) \le E(x_k)\left(1 - \frac{4\mu L}{(\mu + L)^2}\right) = E(x_k)\frac{(L - \mu)^2}{(L + \mu)^2}$.

*Equality.* For $A = \operatorname{diag}(\mu, L)$ and $x_k - x^* = (L, \pm\mu)$, $g = (\mu L, \pm\mu L)$, and $g^\top g = 2\mu^2L^2$, $g^\top Ag = \mu^2L^2(\mu + L)$, $g^\top A^{-1}g = \mu L(\mu + L)$, so the ratio is $4\mu L/(\mu + L)^2$ and the bound holds with equality. The worked example is this case with $\mu = 1$, $L = 10$ and $x_0 = (10, 1)$.

**Proof of 6.** Since $\alpha_k$ minimizes $\varphi_k$, $f(x_{k+1}) \le \varphi_k(1/L_f) = f(x_k - g_k/L_f) \le f(x_k) - \frac{1}{2L_f}\|g_k\|^2$ by the descent lemma ([smoothness](/smoothness/)). Strong convexity gives $f^* \ge f(x_k) - \frac{1}{2\mu}\|g_k\|^2$ (minimize the lower bound $f(x_k) + g_k^\top(y - x_k) + \frac{\mu}{2}\|y - x_k\|^2$ over $y$), so $\|g_k\|^2 \ge 2\mu(f(x_k) - f^*)$. Together, $f(x_{k+1}) - f^* \le (1 - \mu/L_f)(f(x_k) - f^*)$.

**Proof of 7.** Write $\Delta_k = f(x_k) - f^*$. As in the proof of claim 6, $\Delta_{k+1} \le \Delta_k - \frac{1}{2L_f}\|g_k\|^2$, so the values decrease and every $x_k$ lies in the level set, where $\|x_k - x^*\| \le D_0$. By convexity and the Cauchy-Schwarz inequality, $\Delta_k \le g_k^\top(x_k - x^*) \le \|g_k\|D_0$. So $\Delta_{k+1} \le \Delta_k - \Delta_k^2/(2L_fD_0^2)$. If some $\Delta_j = 0$, then $\Delta_k = 0$ for $k \ge j$ and the claim holds. Otherwise divide by $\Delta_k\Delta_{k+1} > 0$ and use $\Delta_{k+1} \le \Delta_k$:

$$\frac{1}{\Delta_{k+1}} - \frac{1}{\Delta_k} \ge \frac{\Delta_k}{2L_fD_0^2\,\Delta_{k+1}} \ge \frac{1}{2L_fD_0^2}.$$

Adding for $0, \ldots, k - 1$ gives $1/\Delta_k \ge 1/\Delta_0 + k/(2L_fD_0^2) > k/(2L_fD_0^2)$. $\square$

**Floating point.** The proofs above are in exact arithmetic. In floating point the comparisons at L1, L4 and L9 are exact for exactly computed values, but near $a^*$ the values of $\varphi$ differ by less than their rounding errors, so the bracket can be wrong by about $\sqrt{u}$ times the scale of the problem, where $u = 2^{-53}$.
