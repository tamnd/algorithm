---
title: Gradient descent decreases f and meets the sublinear and linear rates
proves: [correctness, termination, gradients.convex, gradients.strongly_convex]
status: full
---

**Statement.** Let $f : \mathbb{R}^n \to \mathbb{R}$ be differentiable with an $L_f$-Lipschitz gradient, and bounded below with $f^* = \inf f$. Let $x_{k+1} = x_k - \alpha \nabla f(x_k)$ with $0 < \alpha \le 1/L_f$, and write $g_k = \nabla f(x_k)$. Then:

1. $f(x_{k+1}) \le f(x_k) - \frac{\alpha}{2} \|g_k\|^2$ for each $k$.
2. $\min_{0 \le i < k} \|g_i\|^2 \le 2 (f(x_0) - f^*) / (\alpha k)$ for each $k \ge 1$.
3. If $f$ is convex and $x^*$ is a minimizer, then $\|x_{k+1} - x^*\| \le \|x_k - x^*\|$ and $f(x_k) - f^* \le \|x_0 - x^*\|^2 / (2 \alpha k)$ for each $k \ge 1$.
4. If $f$ is $\mu$-strongly convex and $\alpha = 1/L_f$, then $f(x_k) - f^* \le (1 - \mu/L_f)^k (f(x_0) - f^*)$ and $\|x_k - x^*\|^2 \le (1 - \mu/L_f)^k \|x_0 - x^*\|^2$.

GRADIENT-DESCENT stops after at most $K$ passes of the loop of line L2, so it terminates, and it computes exactly the iterates $x_0, x_1, \ldots$ up to the first $k$ with $\|g_k\| \le \varepsilon_g$ or $k = K$. So the claims hold for its iterates.

**Lemma (descent lemma).** For all $x, y$, $f(y) \le f(x) + \nabla f(x)^\top (y - x) + \frac{L_f}{2} \|y - x\|^2$.

*Proof.* Let $h = y - x$ and $\varphi(t) = f(x + t h)$. Then $\varphi'(t) = \nabla f(x + th)^\top h$, and by the fundamental theorem of calculus

$$f(y) - f(x) - \nabla f(x)^\top h = \int_0^1 \left(\nabla f(x + th) - \nabla f(x)\right)^\top h \, dt \le \int_0^1 \|\nabla f(x + th) - \nabla f(x)\| \, \|h\| \, dt \le \int_0^1 L_f t \|h\|^2 dt = \frac{L_f}{2}\|h\|^2,$$

by the Cauchy-Schwarz inequality and the Lipschitz bound. $\square$

**Proof of 1.** Put $y = x_k - \alpha g_k$ in the lemma: $f(x_{k+1}) \le f(x_k) - \alpha \|g_k\|^2 + \frac{L_f \alpha^2}{2} \|g_k\|^2 = f(x_k) - \alpha \left(1 - \frac{L_f \alpha}{2}\right) \|g_k\|^2$. Since $\alpha \le 1/L_f$, the factor $1 - L_f \alpha / 2$ is at least $1/2$. $\square$

**Proof of 2.** Add claim 1 for $i = 0, \ldots, k-1$. The sum telescopes: $\frac{\alpha}{2} \sum_{i<k} \|g_i\|^2 \le f(x_0) - f(x_k) \le f(x_0) - f^*$. The smallest of the $k$ terms is at most their mean, which is at most $2 (f(x_0) - f^*)/(\alpha k)$. $\square$

**Proof of 3.** Fix $k$ and write $x = x_k$, $g = g_k$, $x^+ = x_{k+1}$.

- Step 1. Convexity gives $f^* = f(x^*) \ge f(x) + g^\top (x^* - x)$, so $f(x) \le f^* + g^\top (x - x^*)$.
- Step 2. With claim 1, $f(x^+) \le f^* + g^\top (x - x^*) - \frac{\alpha}{2}\|g\|^2$.
- Step 3. Expand the square: $\|x^+ - x^*\|^2 = \|x - x^*\|^2 - 2\alpha g^\top (x - x^*) + \alpha^2 \|g\|^2$. So $g^\top (x - x^*) - \frac{\alpha}{2}\|g\|^2 = \frac{1}{2\alpha}\left(\|x - x^*\|^2 - \|x^+ - x^*\|^2\right)$, and step 2 becomes
$$f(x_{k+1}) - f^* \le \frac{1}{2\alpha}\left(\|x_k - x^*\|^2 - \|x_{k+1} - x^*\|^2\right).$$
- Step 4. The left side is at least $0$, so $\|x_{k+1} - x^*\| \le \|x_k - x^*\|$.
- Step 5. Add step 3 for $k = 0, \ldots, K' - 1$. The right side telescopes: $\sum_{i=1}^{K'} (f(x_i) - f^*) \le \frac{1}{2\alpha}\left(\|x_0 - x^*\|^2 - \|x_{K'} - x^*\|^2\right) \le \frac{\|x_0 - x^*\|^2}{2\alpha}$.
- Step 6. By claim 1 the values $f(x_i)$ do not increase, so each of the $K'$ terms is at least $f(x_{K'}) - f^*$. Hence $K' (f(x_{K'}) - f^*) \le \|x_0 - x^*\|^2/(2\alpha)$. $\square$

**Proof of 4.** Let $\alpha = 1/L_f$, and let $f$ be $\mu$-strongly convex: $f(y) \ge f(x) + \nabla f(x)^\top (y - x) + \frac{\mu}{2}\|y - x\|^2$ for all $x, y$. Then $f$ has a unique minimizer $x^*$ ([strong convexity](/strong-convexity/)).

- Step 1 (gradient dominance). Minimize the right side of the strong convexity inequality over $y$. The minimum is at $y = x - g/\mu$, with value $f(x) - \|g\|^2/(2\mu)$. So $f(y) \ge f(x) - \|g\|^2/(2\mu)$ for every $y$. Take $y = x^*$: $f^* \ge f(x) - \|g\|^2/(2\mu)$, that is, $\|g\|^2 \ge 2\mu (f(x) - f^*)$.
- Step 2 (values). By claim 1 with $\alpha = 1/L_f$ and step 1, $f(x_{k+1}) - f^* \le f(x_k) - f^* - \frac{1}{2L_f}\|g_k\|^2 \le \left(1 - \frac{\mu}{L_f}\right)(f(x_k) - f^*)$. Induction on $k$ gives the first bound.
- Step 3 (an upper bound on the gradient). By claim 1, $f^* \le f(x_{k+1}) \le f(x_k) - \frac{1}{2L_f}\|g_k\|^2$, so $\|g_k\|^2 \le 2 L_f (f(x_k) - f^*)$.
- Step 4 (distances). Strong convexity at $x = x_k$ and $y = x^*$ gives $g_k^\top (x_k - x^*) \ge f(x_k) - f^* + \frac{\mu}{2}\|x_k - x^*\|^2$. Put this and step 3 into the expanded square:
$$\|x_{k+1} - x^*\|^2 \le \|x_k - x^*\|^2 - \frac{2}{L_f}\left(f(x_k) - f^* + \frac{\mu}{2}\|x_k - x^*\|^2\right) + \frac{2 L_f}{L_f^2}(f(x_k) - f^*) = \left(1 - \frac{\mu}{L_f}\right)\|x_k - x^*\|^2.$$
Induction on $k$ gives the second bound. $\blacksquare$

**Iteration counts.** Claims 3 and 4 with $\alpha = 1/L_f$ give the iteration counts of the page. For claim 4, $1 - \mu/L_f \le e^{-\mu/L_f}$, so $(1 - \mu/L_f)^k (f(x_0) - f^*) \le \varepsilon$ when $k \ge \kappa \ln((f(x_0) - f^*)/\varepsilon)$.
