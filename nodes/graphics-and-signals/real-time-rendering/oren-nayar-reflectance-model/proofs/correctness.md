---
title: Properties of the qualitative Oren-Nayar model
proves: [correctness]
status: full
---

**Setting.** For $\sigma \ge 0$, $\rho \ge 0$ and directions with $\theta_l, \theta_v \in [0, \pi / 2)$, the code computes $f = \frac{\rho}{\pi}(A + B \max(0, \cos\Delta\phi) \sin\alpha \tan\beta)$ with $A = 1 - 0.5 \sigma^2 / (\sigma^2 + 0.33)$, $B = 0.45 \sigma^2 / (\sigma^2 + 0.09)$, $\alpha = \max(\theta_l, \theta_v)$, $\beta = \min(\theta_l, \theta_v)$ and $\Delta\phi = \phi_v - \phi_l$. A second function computes the same value from unit vectors. The claims are about these formulas. That they match the full V-cavity model or a real surface is a measurement reported by Oren and Nayar (1994), not a claim here.

**Claim 1 (Lambert limit).** At $\sigma = 0$, $f = \rho / \pi$.

*Proof.* $A = 1 - 0 = 1$ and $B = 0$. $\square$

**Claim 2 (the vector form).** With $c_l = n \cdot l$, $c_v = n \cdot v$, $\sin\alpha \tan\beta = \sin\theta_l \sin\theta_v / \max(c_l, c_v)$ and $\cos\Delta\phi \sin\theta_l \sin\theta_v = l \cdot v - c_l c_v$.

*Proof.* Cosine is decreasing on $[0, \pi / 2)$, so $\cos\beta = \max(c_l, c_v)$. Then $\sin\alpha \tan\beta = \sin\alpha \sin\beta / \cos\beta = \sin\theta_l \sin\theta_v / \max(c_l, c_v)$. In a frame with $n = z$, $l = (\sin\theta_l \cos\phi_l, \sin\theta_l \sin\phi_l, c_l)$ and the same for $v$, so $l \cdot v = \sin\theta_l \sin\theta_v (\cos\phi_l \cos\phi_v + \sin\phi_l \sin\phi_v) + c_l c_v = \sin\theta_l \sin\theta_v \cos\Delta\phi + c_l c_v$. Since $\sin\theta_l \sin\theta_v \ge 0$, $\max(0, \cos\Delta\phi) \sin\theta_l \sin\theta_v = \max(0, l \cdot v - c_l c_v)$. $\square$

**Claim 3 (reciprocity).** $f(l, v) = f(v, l)$.

*Proof.* $\max$, $\min$ and $\cos\Delta\phi$ do not change when $l$ and $v$ are swapped. $\square$

**Claim 4 (backscatter).** For fixed $\theta_l, \theta_v$, $f$ is largest at $\Delta\phi = 0$ and equals $\rho A / \pi$ whenever $\cos\Delta\phi \le 0$.

*Proof.* $B \ge 0$ and $\sin\alpha \tan\beta \ge 0$, so $f$ increases with $\max(0, \cos\Delta\phi)$, which is largest at $\Delta\phi = 0$ and 0 when $\cos\Delta\phi \le 0$. $\square$

**Claim 5 (the albedo).** The directional albedo is $E(\theta_l) = \rho \big(A + \frac{2B}{\pi} \int_0^{\pi / 2} \sin\alpha \tan\beta \cos\theta \sin\theta\, d\theta\big)$ with $\alpha, \beta$ formed from $\theta_l$ and $\theta$. In particular $E(0) = \rho A$.

*Proof.* $E = \int_0^{2\pi} \int_0^{\pi / 2} f \cos\theta \sin\theta\, d\theta\, d\phi$. The $A$ term gives $\frac{\rho A}{\pi} \cdot 2\pi \cdot \frac12 = \rho A$. In the $B$ term only $\max(0, \cos\Delta\phi)$ depends on $\phi$, and its integral over a full turn is 2. At $\theta_l = 0$, $\beta = 0$ for every $\theta$, so the $B$ term is 0. $\square$

**Claim 6 (the sphere lit from the viewer).** With $l = v$ at the angle $\theta$ from the normal, the radiance for unit irradiance at normal incidence is $\frac{\rho}{\pi} \cos\theta (A + B \sin\theta \tan\theta)$.

*Proof.* $\Delta\phi = 0$ and $\alpha = \beta = \theta$, and the irradiance is $\cos\theta$. $\square$

**What the tests check.** Claim 1 at random directions, Claims 2 and 3 at 2000 random inputs, Claim 4 and Claim 6 at the page values, and Claim 5 by comparing the 2D midpoint quadrature with the 1D integral of the claim and both with the page values.
