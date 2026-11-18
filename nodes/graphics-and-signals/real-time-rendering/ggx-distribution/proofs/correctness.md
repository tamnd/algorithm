---
title: Properties of the GGX distribution
proves: [correctness]
status: full
---

**Setting.** For $\alpha > 0$ and a unit vector $m$ with $\mu = n \cdot m = \cos\theta$, the code evaluates $D(m) = \alpha^2 / (\pi (\mu^2 (\alpha^2 - 1) + 1)^2)$ for $\mu > 0$ and $D(m) = 0$ otherwise. It also evaluates the slope form, the anisotropic form and a sampler. The claims are about these formulas in exact arithmetic. Whether GGX fits a given material is a measurement and is not claimed here.

**Claim 1 (normalization).** $\int_{H^2} D(m)\, (n \cdot m)\, d\omega_m = 1$ for every $\alpha > 0$.

*Proof.* $D$ does not depend on the azimuth, and $d\omega_m = \sin\theta\, d\theta\, d\phi$, so with $\mu = \cos\theta$ the integral is $2\pi \int_0^1 D \mu\, d\mu = \int_0^1 2 \alpha^2 \mu / (\mu^2 (\alpha^2 - 1) + 1)^2\, d\mu$. With $u = \mu^2$, $du = 2\mu\, d\mu$, this is $\alpha^2 \int_0^1 du / (u (\alpha^2 - 1) + 1)^2$. For $\alpha \ne 1$ an antiderivative is $-1 / ((\alpha^2 - 1)(u (\alpha^2 - 1) + 1))$, so the integral is $\alpha^2 (1 - 1 / \alpha^2) / (\alpha^2 - 1) = 1$. For $\alpha = 1$ the integrand is 1 and the integral is $\alpha^2 = 1$. $\square$

**Claim 2 (the slope form).** For $0 < \mu \le 1$, $D = \alpha^2 / (\pi \mu^4 (\alpha^2 + \tan^2\theta)^2)$.

*Proof.* $\mu^2 (\alpha^2 - 1) + 1 = \mu^2 \alpha^2 + (1 - \mu^2) = \mu^2 (\alpha^2 + \tan^2\theta)$, since $1 - \mu^2 = \mu^2 \tan^2\theta$. Squaring gives $\mu^4 (\alpha^2 + \tan^2\theta)^2$. $\square$

**Claim 3 (the anisotropic form).** $D_a(m) = 1 / (\pi \alpha_x \alpha_y ((m_x / \alpha_x)^2 + (m_y / \alpha_y)^2 + m_z^2)^2)$ equals $D$ when $\alpha_x = \alpha_y = \alpha$, and it is normalized for all $\alpha_x, \alpha_y > 0$.

*Proof.* With $\alpha_x = \alpha_y = \alpha$, $m_x^2 + m_y^2 = 1 - \mu^2$, so the bracket is $(1 - \mu^2) / \alpha^2 + \mu^2 = (\mu^2 (\alpha^2 - 1) + 1) / \alpha^2$, and $D_a = \alpha^4 / (\pi \alpha^2 (\mu^2 (\alpha^2 - 1) + 1)^2) = D$. For normalization, map a normal to its slope $s = (-m_x / m_z, -m_y / m_z)$. Then $D(m)\, (n \cdot m)\, d\omega_m = P(s)\, ds$ with $P(s) = D(m) \mu^4$, because $d\omega_m = \mu^3\, ds$. For $D_a$ this gives $P(s) = 1 / (\pi \alpha_x \alpha_y (1 + s_x^2 / \alpha_x^2 + s_y^2 / \alpha_y^2)^2)$. The substitution $s_x = \alpha_x t_x$, $s_y = \alpha_y t_y$ turns $\int P\, ds$ into $\int_{\mathbb{R}^2} dt / (\pi (1 + |t|^2)^2) = \int_0^\infty 2 \rho\, d\rho / (1 + \rho^2)^2 = 1$. $\square$

**Claim 4 (sampling).** If $u$ is uniform in $[0, 1)$ and $\tan^2\theta = \alpha^2 u / (1 - u)$, with an independent uniform azimuth, then $m$ has the density $D(m)\, (n \cdot m)$ on the hemisphere.

*Proof.* By Claim 1 and the substitution there, the probability that the angle of a normal drawn with the density $D \mu$ is at most $\theta$ is $F(\theta) = \alpha^2 \int_{\cos^2\theta}^1 du / (u (\alpha^2 - 1) + 1)^2$. Computing it with the antiderivative of Claim 1 gives $F(\theta) = \tan^2\theta / (\alpha^2 + \tan^2\theta)$. This $F$ is continuous and increasing from 0 to 1, and solving $F(\theta) = u$ gives $\tan^2\theta = \alpha^2 u / (1 - u)$. So $\theta = F^{-1}(u)$ has the distribution $F$, by the inverse transform method. The density does not depend on the azimuth, so a uniform azimuth completes the sample. $\square$

**Claim 5 (peak and tail).** $D(n) = 1 / (\pi \alpha^2)$, and $D \sin^4\theta \to \alpha^2 / \pi$ as $\theta \to \pi / 2$.

*Proof.* At $\mu = 1$ the bracket is $\alpha^2$. As $\mu \to 0$ the bracket tends to 1 and $\sin^4\theta \to 1$, so $D \sin^4\theta \to \alpha^2 / \pi$. $\square$

**What the tests check.** Claims 1 and 3 by Gauss-Legendre quadrature, Claims 2 and 3 at random points, Claim 4 by a Kolmogorov test of 20000 samples per $\alpha$, and Claim 5 at sample points. The page table of GGX and Beckmann values is checked to five digits.
