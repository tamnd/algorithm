---
title: Backtracking stops, returns an Armijo step that is not too short, and gives gradient descent its rates
proves: [correctness, termination]
status: full
---

**Statement.** Let $f : \mathbb{R}^n \to \mathbb{R}$ be continuously differentiable, let $g = \nabla f(x)$, and let $d$ satisfy $s = g^\top d < 0$. Let $\alpha_0 > 0$, $0 < \rho < 1$ and $0 < c < 1$. Write $\varphi(\alpha) = f(x + \alpha d)$. Then:

1. The loop of line L4 stops after finitely many trials.
2. The returned $\alpha$ satisfies $\varphi(\alpha) \le \varphi(0) + c\alpha s$.
3. If $\nabla f$ is $L_f$-Lipschitz, then every $\alpha \in (0, \bar{\alpha}]$ with $\bar{\alpha} = 2(1 - c)|s|/(L_f\|d\|^2)$ satisfies the test, and the returned step satisfies $\alpha \ge \min(\alpha_0, \rho\bar{\alpha})$.
4. Under the same assumption, the number of trials is at most $1 + \max\left(0, \lceil\log_{1/\rho}(\alpha_0/\bar{\alpha})\rceil\right)$.

For gradient descent $x_{k+1} = x_k - \alpha_k g_k$ with $g_k = \nabla f(x_k)$ and $\alpha_k$ from backtracking, let $f$ be $L_f$-smooth and bounded below with $f^* = \inf f$, and let $\alpha_{\min} = \min(\alpha_0, 2\rho(1 - c)/L_f)$. Then:

5. $\alpha_k \ge \alpha_{\min}$, $f(x_{k+1}) \le f(x_k) - c\alpha_k\|g_k\|^2$, and $\min_{i < k}\|g_i\|^2 \le (f(x_0) - f^*)/(c\sum_{i<k}\alpha_i)$.
6. If $f$ is convex with a nonempty set $X^*$ of minimizers and $c \ge \frac12$, then $\operatorname{dist}(x_{k+1}, X^*) \le \operatorname{dist}(x_k, X^*)$ and $f(x_k) - f^* \le R^2/(2\sum_{i<k}\alpha_i) \le R^2/(2k\alpha_{\min})$ for $k \ge 1$, with $R = \operatorname{dist}(x_0, X^*)$.
7. If $f$ is $\mu$-strongly convex, then $f(x_{k+1}) - f^* \le (1 - 2\mu c\alpha_k)(f(x_k) - f^*)$, with $0 \le 1 - 2\mu c\alpha_k < 1$.

**Proof of 1.** Since $\varphi'(0) = s < 0$ and $\varphi$ is differentiable at $0$, $\varphi(\alpha) - \varphi(0) - c\alpha s = (1 - c)\alpha s + o(\alpha)$ as $\alpha \to 0^+$. The term $(1 - c)\alpha s$ is negative and of order $\alpha$, so there is $\delta > 0$ with $\varphi(\alpha) \le \varphi(0) + c\alpha s$ for all $\alpha \in (0, \delta)$. The trial steps are $\alpha_0\rho^{j}$, $j = 0, 1, \ldots$, and they tend to $0$, so some trial is below $\delta$, and the loop stops at that trial or earlier. In floating point arithmetic with a deterministic $f$, the trial step underflows to $0$ after finitely many halvings at the latest, and then the test reads $f(x) > f(x)$, which is false, so the loop also stops.

**Proof of 2.** The loop of line L4 exits only when its condition is false, that is, when $\varphi(\alpha) \le \varphi(0) + c\alpha s$, and line L6 returns this $\alpha$.

**Proof of 3.** By the descent lemma ([smoothness](/smoothness/)), $\varphi(\alpha) \le \varphi(0) + \alpha s + \frac{L_f}{2}\alpha^2\|d\|^2$. The right side is at most $\varphi(0) + c\alpha s$ if and only if $(1 - c)\alpha s + \frac{L_f}{2}\alpha^2\|d\|^2 \le 0$, that is, $\alpha \le 2(1 - c)|s|/(L_f\|d\|^2) = \bar{\alpha}$. So every $\alpha \in (0, \bar{\alpha}]$ passes the test. If the first trial passes, the returned step is $\alpha_0$. Otherwise the returned step is $\alpha = \rho\alpha'$, where $\alpha'$ is the trial before it, which failed the test. A failed trial is not in $(0, \bar{\alpha}]$, so $\alpha' > \bar{\alpha}$ and $\alpha > \rho\bar{\alpha}$. In both cases $\alpha \ge \min(\alpha_0, \rho\bar{\alpha})$.

**Proof of 4.** Trial $j$ uses the step $\alpha_0\rho^{j-1}$. By claim 3 the loop stops at the first $j$ with $\alpha_0\rho^{j-1} \le \bar{\alpha}$ or earlier. If $\alpha_0 \le \bar{\alpha}$, this is $j = 1$. Otherwise $\alpha_0\rho^{j-1} \le \bar{\alpha}$ if and only if $j - 1 \ge \log_{1/\rho}(\alpha_0/\bar{\alpha})$, and the smallest such integer is $j = 1 + \lceil\log_{1/\rho}(\alpha_0/\bar{\alpha})\rceil$.

**Proof of 5.** Take $d = -g_k$, so $s = -\|g_k\|^2$ and $\bar{\alpha} = 2(1 - c)/L_f$. Claim 3 gives $\alpha_k \ge \alpha_{\min}$, and claim 2 gives $f(x_{k+1}) \le f(x_k) - c\alpha_k\|g_k\|^2$. Adding these inequalities for $i = 0, \ldots, k - 1$ gives $c\sum_{i<k}\alpha_i\|g_i\|^2 \le f(x_0) - f(x_k) \le f(x_0) - f^*$. The left side is at least $c\left(\min_{i<k}\|g_i\|^2\right)\sum_{i<k}\alpha_i$.

**Proof of 6.** Fix $k$ and let $x^*$ be any minimizer. Since $c \ge \frac12$, claim 5 gives $f(x_{k+1}) \le f(x_k) - \frac{\alpha_k}{2}\|g_k\|^2$. By convexity, $f(x_k) \le f^* + g_k^\top(x_k - x^*)$. Together,

$$f(x_{k+1}) - f^* \le g_k^\top(x_k - x^*) - \frac{\alpha_k}{2}\|g_k\|^2 = \frac{1}{2\alpha_k}\left(\|x_k - x^*\|^2 - \|x_k - x^* - \alpha_k g_k\|^2\right) = \frac{1}{2\alpha_k}\left(\|x_k - x^*\|^2 - \|x_{k+1} - x^*\|^2\right),$$

where the middle equality is the expansion of the square. Since the left side is at least $0$, $\|x_{k+1} - x^*\| \le \|x_k - x^*\|$ for every minimizer $x^*$. Taking $x^*$ as the minimizer nearest to $x_k$ (the set $X^*$ is closed and convex, since $f$ is continuous and convex), $\operatorname{dist}(x_{k+1}, X^*) \le \|x_{k+1} - x^*\| \le \|x_k - x^*\| = \operatorname{dist}(x_k, X^*)$.

Now let $x^*$ be the minimizer nearest to $x_0$, so $\|x_0 - x^*\| = R$. Multiply the display by $\alpha_k$ and add it for $i = 0, \ldots, k - 1$; the right side telescopes:

$$\sum_{i<k}\alpha_i\left(f(x_{i+1}) - f^*\right) \le \frac12\left(\|x_0 - x^*\|^2 - \|x_k - x^*\|^2\right) \le \frac{R^2}{2}.$$

By claim 5 the values $f(x_i)$ do not increase, so $f(x_{i+1}) - f^* \ge f(x_k) - f^*$ for each $i < k$. Hence $\left(\sum_{i<k}\alpha_i\right)(f(x_k) - f^*) \le R^2/2$, which is the first bound. The second follows from $\sum_{i<k}\alpha_i \ge k\alpha_{\min}$.

**Proof of 7.** A $\mu$-strongly convex differentiable $f$ satisfies $f(y) \ge f(x) + \nabla f(x)^\top(y - x) + \frac{\mu}{2}\|y - x\|^2$. Minimizing both sides over $y$ (the right side is smallest at $y = x - \nabla f(x)/\mu$) gives $f^* \ge f(x) - \frac{1}{2\mu}\|\nabla f(x)\|^2$, that is, $\|g_k\|^2 \ge 2\mu(f(x_k) - f^*)$. Put this into claim 5:

$$f(x_{k+1}) - f^* \le f(x_k) - f^* - c\alpha_k\|g_k\|^2 \le (1 - 2\mu c\alpha_k)(f(x_k) - f^*).$$

For the range of the factor: the left side is at least $0$, so if $f(x_k) > f^*$ the factor is at least $0$; and if $f(x_k) = f^*$, then $g_k = 0$ and no step is taken. The factor is below $1$ since $\mu, c, \alpha_k > 0$. $\square$

**Termination of the driver.** The gradient descent driver runs at most `iterations` passes, and each pass calls the line search, which stops by claim 1. So the driver stops.
