---
title: The composite trapezoidal rule has error -(b - a) h^2 f''(ξ)/12, and error O(e^(-αm)) for periodic analytic f
proves: [correctness]
status: full
---

Let $a < b$, $m \ge 1$, $h = (b - a)/m$ and $x_i = a + i h$ for $i = 0, \ldots, m$. TRAPEZOID$(f, a, b, m)$ returns, in exact arithmetic,

$$T_m(f) = h \Big( \tfrac12 f(x_0) + \sum_{i=1}^{m-1} f(x_i) + \tfrac12 f(x_m) \Big),$$

because line L2 sets $s = (f(x_0) + f(x_m))/2$, the loop of lines L3 and L4 adds $f(x_1), \ldots, f(x_{m-1})$ once each, and line L5 multiplies by $h$. We write $I(f) = \int_a^b f(x)\,dx$ and $E(f) = I(f) - T_m(f)$.

**Lemma 1 (one panel).** Let $f \in C^2[c, c + h]$. Then there is $\eta \in [c, c + h]$ with

$$\int_c^{c+h} f(x)\,dx - \frac{h}{2}\big(f(c) + f(c + h)\big) = -\frac{h^3}{12} f''(\eta).$$

*Proof.* Let $p$ be the linear polynomial with $p(c) = f(c)$ and $p(c + h) = f(c + h)$. Then $\int_c^{c+h} p = \frac{h}{2}(f(c) + f(c + h))$. By the Newton form of the interpolation error, $f(x) - p(x) = g(x)\,(x - c)(x - c - h)$ with $g(x) = f[c, c + h, x]$, the second divided difference. For $f \in C^2$, $g$ is continuous on $[c, c + h]$, and by the mean value theorem for divided differences each value $g(x)$ equals $f''(\zeta)/2$ for some $\zeta \in [c, c + h]$. The factor $(x - c)(x - c - h)$ is at most 0 on the panel, so it does not change sign. The mean value theorem for integrals gives $x^* \in [c, c + h]$ with

$$\int_c^{c+h} (f - p) = g(x^*) \int_c^{c+h} (x - c)(x - c - h)\,dx = g(x^*) \cdot \Big( -\frac{h^3}{6} \Big).$$

With $g(x^*) = f''(\eta)/2$ this is $-h^3 f''(\eta)/12$. $\square$

**Theorem 1 (composite error).** Let $f \in C^2[a, b]$. Then there is $\xi \in [a, b]$ with

$$E(f) = -\frac{(b - a)\, h^2}{12} f''(\xi).$$

*Proof.* $T_m(f)$ is the sum over $j = 0, \ldots, m - 1$ of the one-panel rules on $[x_j, x_{j+1}]$: each interior node $x_i$ gets $h/2$ from the panel on its left and $h/2$ from the panel on its right, and each endpoint gets $h/2$ once. By Lemma 1, $E(f) = -\frac{h^3}{12} \sum_{j=0}^{m-1} f''(\eta_j)$ with $\eta_j \in [x_j, x_{j+1}]$. The average $\frac{1}{m} \sum_j f''(\eta_j)$ lies between the minimum and the maximum of the continuous $f''$ on $[a, b]$, so by the intermediate value theorem it equals $f''(\xi)$ for some $\xi \in [a, b]$. Then $E(f) = -\frac{h^3 m}{12} f''(\xi) = -\frac{(b - a) h^2}{12} f''(\xi)$. $\square$

**Corollary (degree of exactness).** If $f$ is a polynomial of degree at most 1, then $f'' = 0$ and $E(f) = 0$. For $f(x) = x^2$, $f'' = 2$ and $E(f) = -(b - a) h^2/6 \ne 0$. So the degree of exactness is exactly 1.

**Theorem 2 (periodic analytic integrands).** Let $f$ be $2\pi$-periodic on $\mathbb{R}$, and let $f$ extend to a function that is analytic in the strip $S_\alpha = \{ z : |\operatorname{Im} z| < \alpha \}$ for some $\alpha > 0$, with $|f(z)| \le M$ there. Take $[a, b] = [0, 2\pi]$. Then for every $m \ge 1$,

$$|E(f)| \le \frac{4 \pi M}{e^{\alpha m} - 1}.$$

*Proof.* Step 1 (the rule). Because $f(0) = f(2\pi)$, $T_m(f) = h \sum_{j=0}^{m-1} f(jh)$ with $h = 2\pi/m$.

Step 2 (Fourier coefficients decay). Let $c_k = \frac{1}{2\pi} \int_0^{2\pi} f(\theta) e^{-ik\theta}\,d\theta$. Take $k > 0$ and $0 < \beta < \alpha$. The function $f(z) e^{-ikz}$ is analytic on the closed rectangle with corners $0$, $2\pi$, $2\pi - i\beta$, $-i\beta$, so its integral around the boundary is 0 by Cauchy's theorem. The two vertical sides cancel because the integrand has period $2\pi$. So $c_k = \frac{1}{2\pi} \int_0^{2\pi} f(t - i\beta) e^{-ik(t - i\beta)}\,dt$. Here $|e^{-ik(t - i\beta)}| = e^{-k\beta}$, so $|c_k| \le M e^{-k\beta}$. Letting $\beta \to \alpha$ gives $|c_k| \le M e^{-\alpha k}$. For $k < 0$ shift the line up instead, and get $|c_k| \le M e^{-\alpha |k|}$.

Step 3 (aliasing). By Step 2, $\sum_k |c_k| < \infty$, and $f$ is continuous and $C^1$, so its Fourier series converges to $f$ at every point. Then $T_m(f) = h \sum_{j=0}^{m-1} \sum_k c_k e^{ikjh} = 2\pi \sum_k c_k \cdot \frac{1}{m} \sum_{j=0}^{m-1} e^{2\pi i k j/m}$. The inner average is 1 when $m$ divides $k$ and 0 otherwise (a geometric sum of an $m$-th root of unity other than 1). So $T_m(f) = 2\pi \sum_{\ell \in \mathbb{Z}} c_{\ell m}$, while $I(f) = 2\pi c_0$.

Step 4 (bound). $|E(f)| = 2\pi \big|\sum_{\ell \ne 0} c_{\ell m}\big| \le 2\pi \cdot 2 \sum_{\ell \ge 1} M e^{-\alpha \ell m} = \frac{4\pi M e^{-\alpha m}}{1 - e^{-\alpha m}} = \frac{4\pi M}{e^{\alpha m} - 1}$. $\blacksquare$

**Termination and cost.** The loop of lines L3 and L4 runs $m - 1$ times. Lines L2 and L4 evaluate $f$ at $x_0, x_m$ and at $x_1, \ldots, x_{m-1}$, so the algorithm makes exactly $m + 1$ evaluations.
