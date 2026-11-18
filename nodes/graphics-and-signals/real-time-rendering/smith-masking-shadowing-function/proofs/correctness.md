---
title: Properties of the Smith functions for GGX
proves: [correctness]
status: full
---

**Setting.** For $\alpha > 0$ and a direction $\omega$ with $\mu = n \cdot \omega \in (0, 1]$, the code evaluates $\Lambda(\mu) = (-1 + \sqrt{1 + \alpha^2 \tan^2\theta}) / 2$ with $\tan^2\theta = (1 - \mu^2) / \mu^2$, $G_1 = \chi^+(\omega \cdot m) / (1 + \Lambda)$, $G_2^{\text{sep}} = G_1(l) G_1(v)$ and $G_2^{\text{hc}} = 1 / (1 + \Lambda(l) + \Lambda(v))$. The claims are about these formulas in exact arithmetic. That a real surface has uncorrelated heights and normals is an assumption of the model, not a claim.

**Claim 1 (range).** $\Lambda \ge 0$, so $0 < G_1 \le 1$ for $\mu > 0$, with $G_1 = 1$ at $\mu = 1$ and $G_1 \to 0$ as $\mu \to 0$.

*Proof.* $\sqrt{1 + x} \ge 1$ for $x \ge 0$, so $\Lambda \ge 0$ and $1 / (1 + \Lambda) \in (0, 1]$. At $\mu = 1$, $\tan\theta = 0$ and $\Lambda = 0$. As $\mu \to 0$, $\tan\theta \to \infty$, so $\Lambda \to \infty$ and $G_1 \to 0$. $\square$

**Claim 2 (order).** $0 \le G_2^{\text{sep}} \le G_2^{\text{hc}} \le 1$, and both are symmetric in $l$ and $v$.

*Proof.* $(1 + \Lambda_l)(1 + \Lambda_v) = 1 + \Lambda_l + \Lambda_v + \Lambda_l \Lambda_v \ge 1 + \Lambda_l + \Lambda_v \ge 1$, because both $\Lambda$ are not negative by Claim 1. Taking reciprocals reverses the order. Both expressions do not change when $l$ and $v$ are swapped. $\square$

**Claim 3 (the weak white furnace test).** For every $\omega$ with $\mu > 0$, $\int_{H^2} G_1(\omega, m) \max(0, \omega \cdot m)\, D(m)\, d\omega_m = \mu$, where $D$ is GGX with the same $\alpha$.

*Proof.* Let $A(\omega) = \int \max(0, \omega \cdot m)\, D(m)\, d\omega_m$, the projected area of the facets that face $\omega$. Since $G_1 = \chi^+ / (1 + \Lambda)$ does not depend on $m$ otherwise, the integral is $A(\omega) / (1 + \Lambda(\omega))$. So the claim is the identity $A(\omega) = \mu (1 + \Lambda(\omega))$. Write $A$ in slope space. Turn the frame so that $\omega = (\sin\theta, 0, \cos\theta)$. A facet with the slope $s = (s_x, s_y)$ has the normal $m = (-s_x, -s_y, 1) / \sqrt{1 + |s|^2}$, so $n \cdot m = 1 / \sqrt{1 + |s|^2}$ and $\omega \cdot m = (\cos\theta - s_x \sin\theta) / \sqrt{1 + |s|^2}$. The slope density $P$ is defined by $D(m)\, (n \cdot m)\, d\omega_m = P(s)\, ds$ (the GGX page, Claim 3 of its proof), so $D(m)\, d\omega_m = \sqrt{1 + |s|^2}\, P(s)\, ds$. The square roots cancel, and $A(\omega) = \int_{\mathbb{R}^2} \max(0, \cos\theta - s_x \sin\theta)\, P(s)\, ds = \mu \int_{-\infty}^{\cot\theta} (1 - q \tan\theta)\, P_1(q)\, dq$, where $P_1$ is the marginal density of $s_x$. $P_1$ integrates to 1 and has mean 0, so $\int_{-\infty}^{a} (1 - q \tan\theta) P_1\, dq = 1 + \int_a^\infty (q \tan\theta - 1) P_1\, dq$ for $a = \cot\theta$. So $A = \mu (1 + \Lambda)$ with $\Lambda = \int_{\cot\theta}^\infty (q \tan\theta - 1) P_1(q)\, dq$, which is the definition of Smith's $\Lambda$ (Heitz 2014, Section 5). For GGX, $P(s) = \alpha^2 / (\pi (\alpha^2 + |s|^2)^2)$, and the integral over $s_y$, with $\int_{\mathbb{R}} dy / (c^2 + y^2)^2 = \pi / (2 c^3)$, gives $P_1(q) = \alpha^2 / (2 (\alpha^2 + q^2)^{3/2})$. Then with $a = \cot\theta$, $\int_a^\infty q P_1 = \alpha^2 / (2 \sqrt{\alpha^2 + a^2})$ and $\int_a^\infty P_1 = (1 - a / \sqrt{\alpha^2 + a^2}) / 2$. Then $\Lambda = \tan\theta\, \alpha^2 / (2 \sqrt{\alpha^2 + a^2}) - (1 - a / \sqrt{\alpha^2 + a^2}) / 2 = (\sqrt{\alpha^2 + a^2} \tan\theta - 1) / 2$, using $\alpha^2 \tan\theta + a = \tan\theta (\alpha^2 + a^2)$. Finally $\sqrt{\alpha^2 + a^2} \tan\theta = \sqrt{1 + \alpha^2 \tan^2\theta}$, which is the closed form. $\square$

**Claim 4 (Schlick-GGX at $\alpha = 1$).** With $k = 1/2$, $\mu / (\mu (1 - k) + k) = G_1$ for $\alpha = 1$.

*Proof.* For $\alpha = 1$, $1 + \tan^2\theta = 1 / \mu^2$, so $\Lambda = (1 / \mu - 1) / 2$ and $G_1 = 2\mu / (1 + \mu)$. The Schlick form gives $\mu / (\mu / 2 + 1 / 2) = 2\mu / (1 + \mu)$. $\square$

For other $\alpha$ the Schlick form is a fit, and its largest errors on the page are measured on a grid of $10^4$ points.

**What the tests check.** Claims 1 and 2 at 2000 random inputs, Claim 3 by midpoint quadrature over the hemisphere to $2 \cdot 10^{-3}$ and by Monte Carlo with importance sampling of $D (n \cdot m)$ within four standard errors, Claim 4 on a grid, and the page values to four digits.
