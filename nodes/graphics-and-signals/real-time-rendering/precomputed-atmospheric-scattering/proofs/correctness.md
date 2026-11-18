---
title: Correctness of the transmittance table and the single scattering sum
proves: [correctness]
status: full
---

**Setting.** The planet is a ball of radius $R_g$ with its center at the origin, and the atmosphere is the shell up to radius $R_t$. The extinction coefficient $\sigma(y)$ depends only on $|y|$ and is continuous and nonnegative. A view ray starts at $x$ with $|x| = r$, in the unit direction $v$ with $\mu = v \cdot x / r$; the sun is in the unit direction $\ell$ with $\mu_s = \ell \cdot x / r$ and $\nu = v \cdot \ell$. The transmittance of a segment $[y, z]$ is $T(y, z) = \exp\big(-\int_{[y, z]} \sigma\big)$, and $T(r, \mu)$ is the transmittance from $x$ to the top boundary along a ray that does not hit the ground. The claims are in exact arithmetic, except where a claim names the quadrature.

**Claim 1 (the point on the ray).** The point $y = x + s v$ has $|y| = r_s = \sqrt{r^2 + s^2 + 2 r \mu s}$, view cosine $\mu_y = (r \mu + s) / r_s$ and sun cosine $\mu_{s,y} = (r \mu_s + s \nu) / r_s$ (line L5).

*Proof.* $|y|^2 = r^2 + 2 s\, x \cdot v + s^2$ and $x \cdot v = r \mu$. The view cosine at $y$ is $v \cdot y / |y| = (r\mu + s)/r_s$, and the sun cosine is $\ell \cdot y / |y| = (\ell \cdot x + s\, \ell \cdot v)/r_s = (r \mu_s + s \nu)/r_s$. $\square$

**Claim 2 (the ground test).** For $r \ge R_g$, the ray $(r, \mu)$ meets the ground sphere at a positive distance if and only if $\mu < \mu_h(r) = -\sqrt{1 - (R_g / r)^2}$. The distances to the ground and to the top used in line L2 are $-r\mu - \sqrt{r^2(\mu^2 - 1) + R_g^2}$ and $-r\mu + \sqrt{r^2(\mu^2 - 1) + R_t^2}$.

*Proof.* By Claim 1, $|x + s v| = R$ when $s^2 + 2 r \mu s + r^2 - R^2 = 0$, so $s = -r\mu \pm \sqrt{r^2(\mu^2 - 1) + R^2}$. For $R = R_t > r$, the product of the roots $r^2 - R_t^2$ is negative, so exactly one root is positive, the one with the plus sign. For $R = R_g \le r$, the product of the roots is $r^2 - R_g^2 \ge 0$ and their sum is $-2 r\mu$. Real positive roots need a nonnegative discriminant, $\mu^2 \ge 1 - R_g^2/r^2$, and a positive sum, $\mu < 0$; together these say $\mu \le \mu_h(r)$. The tangent case $\mu = \mu_h$ only touches the sphere, which the code counts as a miss. The first hit is the smaller root, with the minus sign. $\square$

**Claim 3 (the table coordinates).** Let $H = \sqrt{R_t^2 - R_g^2}$, $\rho = \sqrt{r^2 - R_g^2}$ and $d$ the distance to the top. The map $(r, \mu) \mapsto (x_r, x_\mu) = \big(\rho/H,\ (d - (R_t - r)) / (\rho + H - (R_t - r))\big)$ is a bijection from the rays that miss the ground, $r \in [R_g, R_t]$ and $\mu \in [\mu_h(r), 1]$, onto $[0, 1]^2$ (for $r < R_t$), and its inverse is $r = \sqrt{H^2 x_r^2 + R_g^2}$, $\mu = (H^2 - \rho^2 - d^2)/(2 r d)$ with $d = (R_t - r) + x_\mu(\rho + H - (R_t - r))$.

*Proof.* $x_r$ is an increasing function of $r$ from 0 to 1. For fixed $r$, Claim 2 gives $d = -r\mu + \sqrt{r^2\mu^2 + R_t^2 - r^2}$, whose derivative in $\mu$ is $-r + r^2\mu / \sqrt{\cdot} = -r (1 - r\mu/\sqrt{\cdot}) < 0$ since $\sqrt{\cdot} > r|\mu|$. So $d$ decreases strictly from its value at $\mu_h$ to its value at $\mu = 1$, which is $R_t - r$. At $\mu_h$ the ray is tangent to the ground at distance $\rho$ from $x$ and then reaches the top after a further $H$, so $d = \rho + H$. Hence $x_\mu$ is a strictly monotone map onto $[0, 1]$. For the inverse, $|x + d v| = R_t$ gives $r^2 + d^2 + 2 r \mu d = R_t^2$, so $\mu = (R_t^2 - r^2 - d^2)/(2rd)$, and $R_t^2 - r^2 = (H^2 + R_g^2) - (\rho^2 + R_g^2) = H^2 - \rho^2$. $\square$

So line L1 fills the table at well defined rays, and a lookup returns the bilinear interpolation of the exact table values at the coordinates of the query.

**Claim 4 (transmittance from two lookups).** Let $y = x + s v$ with $0 \le s \le D$, where $D$ is the distance of line L2. If the ray misses the ground, $T(x, y) = T(r, \mu) / T(r_s, \mu_y)$. If it hits the ground, $T(x, y) = T(r_s, -\mu_y) / T(r, -\mu)$. This is line L6.

*Proof.* The optical depth is an integral over a segment, so it adds over consecutive segments, and $T$ multiplies: $T(x, z) = T(x, y)\, T(y, z)$ for $y$ on $[x, z]$. It depends only on the segment, not on the direction, so $T(x, y) = T(y, x)$. If the ray misses the ground, let $z$ be its exit point at the top. The ray from $y$ in direction $v$ is the rest of the same ray, with $(r_s, \mu_y)$ by Claim 1, so $T(r, \mu) = T(x, y)\, T(r_s, \mu_y)$, and $T(r_s, \mu_y) > 0$. If the ray hits the ground, the cosine $\mu_t = (r\mu + t)/r_t$ is negative for all $t < D$ (by Claim 2 the hit is before the closest approach to the center, where $r\mu + t = 0$), so $-\mu > 0$ and $-\mu_y \ge 0$, and the reversed rays from $x$ and $y$ point upward and miss the ground. The reversed ray from $y$ in direction $-v$ passes through $x$ and then reaches the top at a point $z'$, which is also the exit point of the reversed ray from $x$. So $T(r_s, -\mu_y) = T(y, x)\, T(x, z') = T(x, y)\, T(r, -\mu)$. $\square$

**Claim 5 (sun visibility).** At the point $y$, the sun is blocked by the planet exactly when $\mu_{s,y} < \mu_h(r_s)$, and otherwise the light that reaches $y$ from the sun is the sun irradiance times $T(r_s, \mu_{s,y})$. This is line L7.

*Proof.* The sunlight that reaches $y$ travels along the ray from $y$ in direction $\ell$, reversed. By Claim 1 that ray has the coordinates $(r_s, \mu_{s,y})$, and by Claim 2 it hits the ground exactly when $\mu_{s,y} < \mu_h(r_s)$. If it misses the ground, it leaves the atmosphere at the top, and the light is attenuated by the transmittance of that segment. $\square$

**Claim 6 (the single scattering sum).** Lines L3 to L9 compute the composite trapezoidal rule with $q$ intervals for

$$S = E_{\text{sun}} \int_0^D T(x, y_s)\, V(y_s)\, T(r_s, \mu_{s, y})\, \big(\beta_R(r_s) P_R(\nu) + \beta_M(r_s) P_M(\nu)\big)\, ds,$$

where $V$ is 1 if the sun is visible at $y_s$ and 0 otherwise, with the transmittances replaced by the table lookups of Claims 3 and 4. With exact transmittances the sum converges to $S$ as $q \to \infty$, with error $O(1/q^2)$ when the integrand is twice continuously differentiable on $[0, D]$.

*Proof.* Line L4 visits the $q + 1$ points $s_k = kD/q$ with weights $1/2$ at the ends and 1 elsewhere, line L8 adds the weighted integrand per channel (zero when line L7 finds the sun blocked), and line L9 multiplies by $D/q$; this is the trapezoidal rule. The integrand is bounded, and it is continuous except where $V$ jumps, which happens at most at finitely many points of the segment. A bounded function with finitely many discontinuities is Riemann integrable, and the trapezoidal sums converge to its integral. When the integrand is $C^2$, the standard error bound of the composite trapezoidal rule is $D^3 \max|f''| / (12 q^2)$. The single scattering integrand itself is the definition: light from the sun, attenuated to $y$, scattered toward $-v$ with the probability density of each phase function times its scattering coefficient, and attenuated back to $x$. $\square$

**Claim 7 (the phase functions).** $2\pi \int_{-1}^1 P_R(\nu)\, d\nu = 1$, and $2\pi \int_{-1}^1 P_M(\nu)\, d\nu = 1$ for every $g \in (-1, 1)$.

*Proof.* For Rayleigh, $2\pi \cdot \frac{3}{16\pi} (2 + \frac{2}{3}) = \frac{3}{8} \cdot \frac{8}{3} = 1$. For Cornette-Shanks, $P_M = k (1 + \nu^2) (1 + g^2 - 2g\nu)^{-3/2}$ with $k = \frac{3}{8\pi} \frac{1 - g^2}{2 + g^2}$. For $g = 0$, $P_M = P_R$. For $g < 0$, the substitution $\nu \to -\nu$ reduces to $|g|$. For $0 < g < 1$, set $a = 1 + g^2$, $b = 2g$ and $w = a - b\nu$, which runs over $[(1 - g)^2, (1 + g)^2]$, so $\sqrt w$ runs over $[1 - g, 1 + g]$. Then $\int_{-1}^1 (1 + \nu^2) w^{-3/2} d\nu = \frac{1}{b} \int \big(1 + (a - w)^2 / b^2\big) w^{-3/2} dw$, and the three needed integrals are $\int w^{-3/2} dw = \frac{4g}{1 - g^2}$, $\int w^{-1/2} dw = 4g$ and $\int w^{1/2} dw = \frac{4g}{3}(3 + g^2)$. Expanding $(a - w)^2 = a^2 - 2aw + w^2$,

$$\int_{-1}^1 \frac{1 + \nu^2}{w^{3/2}}\, d\nu = \frac{2}{1 - g^2} + \frac{1}{2g^2} \Big(\frac{a^2}{1 - g^2} - 2a + 1 + \frac{g^2}{3}\Big) = \frac{2}{1 - g^2} + \frac{2(1 + 2g^2)}{3(1 - g^2)} = \frac{4(2 + g^2)}{3(1 - g^2)},$$

where the bracket simplifies with $a^2 - (1 + \frac{5}{3} g^2)(1 - g^2) = \frac{4}{3} g^2 (1 + 2g^2)$. Multiplying by $2\pi k$ gives 1. $\square$

**What is not proved.** The bilinear interpolation of the table adds an error that the claims do not bound; the tests measure it against direct quadrature. The coefficients of the toy atmosphere are data, and the page labels them.

**Cost.** Line L1 computes $t = n_r n_\mu$ table entries with $q$ quadrature steps each, $\Theta(t q)$ work once. One view ray costs $\Theta(q)$ with three table lookups per step, $O(1)$ each, independent of $t$. $\blacksquare$
