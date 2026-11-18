---
title: Properties of the one-channel principled BRDF
proves: [correctness]
status: full
---

**Setting.** The code computes, for unit $l$ and $v$ above the surface with $n = z$, the value $f = (1 - m)(f_d + s F_H) + f_s + f_c$ of the page, with $h = (l + v) / |l + v|$, $\cos\theta_d = l \cdot h$, $F_H = (1 - \cos\theta_d)^5$, $\alpha = \max(10^{-4}, r^2)$, $F_0 = (1 - m)\, 0.08\, \text{specular} + m b$ and the separable Smith G of GGX. The claims are about these formulas. How well they match measured materials is a measurement reported by Burley (2012), not a claim here.

**Claim 1 (GTR normalization).** For $0 < \alpha < 1$, with $D_2 = \alpha^2 / (\pi (1 + (\alpha^2 - 1)\cos^2\theta)^2)$ and $D_1 = (\alpha^2 - 1) / (\pi \ln(\alpha^2)(1 + (\alpha^2 - 1)\cos^2\theta))$, $\int_{H^2} D \cos\theta\, d\omega = 1$. At $\alpha = 1$ both are $1 / \pi$, and $D_1 \to 1 / \pi$ as $\alpha \to 1$.

*Proof.* First, $\alpha^2 \cos^2\theta + \sin^2\theta = 1 + (\alpha^2 - 1)\cos^2\theta$, so these are the GTR forms. With $u = \cos^2\theta$, $du = -2 \cos\theta \sin\theta\, d\theta$, so $\int_{H^2} D \cos\theta\, d\omega = 2\pi \int_0^{\pi / 2} D \cos\theta \sin\theta\, d\theta = \pi \int_0^1 D\, du$. Put $k = \alpha^2 - 1 \in (-1, 0)$. For $\gamma = 2$, $\int_0^1 (1 + k u)^{-2} du = \frac{1}{k}\big(1 - \frac{1}{1 + k}\big) = \frac{1}{1 + k} = \frac{1}{\alpha^2}$, so the integral is $\pi \cdot \frac{\alpha^2}{\pi} \cdot \frac{1}{\alpha^2} = 1$. For $\gamma = 1$, $\int_0^1 (1 + k u)^{-1} du = \ln(1 + k) / k = \ln(\alpha^2) / (\alpha^2 - 1)$, so the integral is $\pi \cdot \frac{\alpha^2 - 1}{\pi \ln \alpha^2} \cdot \frac{\ln \alpha^2}{\alpha^2 - 1} = 1$. At $\alpha = 1$, $D_2 = 1 / \pi$, and $(\alpha^2 - 1) / \ln(\alpha^2) \to 1$ because $\ln(1 + k) / k \to 1$, so $D_1 \to 1 / \pi$, the value the code returns. $\square$

**Claim 2 (reciprocity).** $f(l, v) = f(v, l)$.

*Proof.* $h$ is symmetric in $l$ and $v$, so $\theta_h$ is too. $l \cdot h = (1 + l \cdot v) / |l + v| = v \cdot h$, so $\theta_d$ and $F_H$ are symmetric, and so is $F_{D90}$. $f_d$ is a product of a factor in $\theta_l$ and the same factor in $\theta_v$, so swapping $l$ and $v$ swaps the factors. The Fresnel terms depend on $\theta_d$ only. $G = G_1(l) G_1(v)$ and the denominator $4 \cos\theta_l \cos\theta_v$ are symmetric. So every lobe is symmetric, and so is their sum. $\square$

**Claim 3 (metallic is a linear blend).** Let $f^{(0)}$ be $f$ with $m = 0$ and $f^{(1)}$ be $f$ with $m = 1$, both with $c = 0$. Then $f = (1 - m) f^{(0)} + m f^{(1)}$ for $c = 0$.

*Proof.* $F = F_0 + (1 - F_0) F_H = F_H + F_0 (1 - F_H)$ is affine in $F_0$, and $D$, $G$ and the denominator do not depend on $m$, so $f_s$ is affine in $F_0$. An affine function $g$ has $g((1 - m) x + m y) = (1 - m) g(x) + m g(y)$. With $x = 0.08\, \text{specular}$ and $y = b$, $f_s = (1 - m) f_s^{(0)} + m f_s^{(1)}$. The diffuse and sheen terms are $(1 - m)$ times their value at $m = 0$, and their value at $m = 1$ is 0. Adding the two parts gives the claim. $\square$

**Claim 4 (the diffuse and sheen lobes).** (a) If $F_{D90} = 1$, then $f_d = b / \pi$. (b) For $m = 0$, increasing $s$ by 1 adds exactly $F_H$ to $f$. (c) For $m = 1$, $f$ does not depend on $s$.

*Proof.* (a) Both factors are $1 + 0 \cdot (\ldots) = 1$. (b) and (c) $s$ appears only in the term $(1 - m) s F_H$. $\square$

**Claim 5 (the furnace estimator).** For $b = 1$, $m = 1$ and $c = 0$, $F = 1$ and the directional albedo is $E(v) = \int f_s \cos\theta_l\, d\omega_l$. If $h$ is drawn with the density $D(h) \cos\theta_h$ and $l = 2 (v \cdot h) h - v$, then the expectation of $w = G\, (v \cdot h) / (\cos\theta_v \cos\theta_h)$, with $w = 0$ when $v \cdot h \le 0$ or $\cos\theta_l \le 0$, is $E(v)$.

*Proof.* $F = F_0 + (1 - F_0) F_H$ with $F_0 = b = 1$ gives $F = 1$. The map $h \mapsto l$ is the reflection of $v$ about $h$; its Jacobian is $d\omega_h / d\omega_l = 1 / (4\, v \cdot h)$, so $l$ has the density $p(l) = D \cos\theta_h / (4\, v \cdot h)$ where $v \cdot h > 0$. The samples with $v \cdot h \le 0$ give no $l$ in the support, and the samples with $\cos\theta_l \le 0$ have $f = 0$. Elsewhere $f_s \cos\theta_l / p = \frac{D G}{4 \cos\theta_l \cos\theta_v} \cos\theta_l \cdot \frac{4\, v \cdot h}{D \cos\theta_h} = w$. Each $l$ in the upper hemisphere comes from exactly one $h$, the half vector of $l$ and $v$, so $E[w] = \int f_s \cos\theta_l\, d\omega_l$. $\square$

**Claim 6 (the 2012 G remap masks more).** For $0 \le r < 1$, $\alpha_g = (0.5 + r / 2)^2 > r^2$, so $G_1$ with $\alpha_g$ is smaller than with $r^2$ at every $\theta_w \in (0, \pi / 2)$.

*Proof.* $0.5 + r / 2 - r = 0.5 (1 - r) > 0$, and both sides are nonnegative, so squaring keeps the order. $G_1 = 2 / (1 + \sqrt{1 + \alpha^2 \tan^2\theta_w})$ decreases in $\alpha$ when $\tan\theta_w > 0$. The specular lobe has $G = G_1(l) G_1(v)$ with all other factors unchanged and positive, so it is smaller. $\square$

**What the tests check.** Claim 1 by quadrature in $u = \cos^2\theta$ for five values of $\alpha$, and the longer tail of $D_1$. Claim 2 and $f \ge 0$ at 1000 random inputs. Claim 3 at 500 random inputs. Claim 4 at fixed directions. The diffuse albedo table and the white dielectric albedo of the page against 2D quadrature. Claim 5 by comparing the Monte Carlo estimate with deterministic quadrature at roughness 0.5 and 1, with the page values and with the bound $E \le 1$ within four standard errors. Claim 6 at three roughness values for a grazing mirror configuration.
