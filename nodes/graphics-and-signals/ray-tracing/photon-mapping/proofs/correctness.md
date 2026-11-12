---
title: Photon tracing is unbiased for flux, and the fixed-radius estimate is biased by O(r^2) and not consistent
proves: [correctness]
status: full
---

We use the measure notation of light transport. Let $\mathcal{M}$ be the set of surface points with the area measure $A$, and $\Omega$ the sphere of directions. For a surface point $x$ and a direction $\omega$ that points from $x$ to where the light comes from, let $L_i(x, \omega)$ be the incident radiance, and let $L_i^{(j)}$ be the part of it carried by light that left a light source and made exactly $j - 1$ reflections before it reached $x$. Then $L_i = \sum_{j \ge 1} L_i^{(j)}$. For a set $S \subseteq \mathcal{M} \times \Omega$ and a weight $g \ge 0$ let

$$\Phi_j(g) = \int_{\mathcal{M}} \int_{\Omega} g(x, \omega)\, L_i^{(j)}(x, \omega)\, |\cos\theta|\, d\omega\, dA(x),$$

the incident flux of order $j$ weighted by $g$. Let $(x_j, \beta_j, \omega_j)$ be the $j$-th hit of one photon path of line L3 to L8, with $\beta_j = 0$ if the path ended before it.

**Lemma 1 (one order).** For each $j \ge 1$ and each measurable $g \ge 0$, $E[N \beta_j\, g(x_j, \omega_j)] = \Phi_j(g)$, where $\omega_j$ is the direction back toward the previous vertex.

*Proof.* By induction on $j$. For $j = 1$: line L3 samples $(y, \omega)$ with the density $p(y, \omega)$ with respect to $dA(y)\,d\omega$ and sets $N\beta = L_e \cos\theta / p$. So $E[N\beta_1 g(x_1, \omega_1)] = \int\int L_e(y, \omega) \cos\theta_y\, g(x_1(y, \omega), \omega_1)\, d\omega\, dA(y)$. The change of variables from $(y, \omega)$ to the hit point $x_1$ and the direction back to $y$ has the Jacobian of the geometry term, and $L_e(y, \omega)$ arrives unchanged at $x_1$, so the integral is $\int\int g\, L_i^{(1)} |\cos\theta_x|\, d\omega\, dA(x) = \Phi_1(g)$.

For $j + 1$: given the $j$-th hit $(x_j, \omega_j)$ with power $\beta_j$, line L7 samples $\omega'$ with the density $p(\omega')$, survives with probability $q$, and sets $\beta_{j+1} = \beta_j f \cos\theta' / (p q)$. So

$$E[\beta_{j+1}\, g(x_{j+1}, \omega_{j+1}) \mid x_j, \omega_j, \beta_j] = \beta_j \int f(x_j, \omega_j, \omega') \cos\theta'\, g(x_{j+1}(\omega'), -\omega')\, d\omega',$$

where the factors $p$ and $q$ cancel. This is $\beta_j\, h(x_j, \omega_j)$ for a nonnegative function $h$, so by the hypothesis for $j$, $E[N \beta_{j+1} g] = \Phi_j(h)$. Now $\Phi_j(h) = \int\int\int L_i^{(j)}(x, \omega) |\cos\theta| f(x, \omega, \omega') \cos\theta'\, g(\ldots)\, d\omega'\, d\omega\, dA$. The integral over $\omega$ of $f L_i^{(j)} \cos$ is the radiance of order $j$ that leaves $x$ in the direction $\omega'$, and it arrives unchanged at $x_{j+1}(\omega')$. The same change of variables as for $j = 1$ turns the result into $\Phi_{j+1}(g)$. $\square$

**Theorem 1 (flux).** For each measurable $g \ge 0$, the photons of $N$ independent paths satisfy $E\left[\sum_p g(x_p, \omega_p)\,\Delta\Phi_p\right] = \sum_j \Phi_j(g) = \int\int g\, L_i\, |\cos\theta|\, d\omega\, dA$, where the sum is over the stored hits.

*Proof.* Sum Lemma 1 over $j$ and over the $N$ paths, each of which has the factor $1/N$ in its power. All terms are nonnegative, so the expectations add by monotone convergence. If photons are stored only on some surfaces, take $g = 0$ elsewhere. $\square$

**Theorem 2 (the expected estimate).** Let $x$ lie on a flat part of the surface that contains the disc $D_r(x)$, and let the estimate with fixed radius be $\hat L_r(x) = \frac{1}{\pi r^2}\sum_{p : x_p \in D_r(x)} f_r(x, \omega_p, \omega_o)\, \Delta\Phi_p$. Then

$$E[\hat L_r(x)] = \frac{1}{\pi r^2} \int_{D_r(x)} \int_{H^2} f_r(x, \omega, \omega_o)\, L_i(x', \omega) \cos\theta\, d\omega\, dA(x').$$

*Proof.* Apply Theorem 1 with $g(x', \omega) = \mathbf{1}\{x' \in D_r(x)\}\, f_r(x, \omega, \omega_o)/(\pi r^2)$. $\square$

For a Lambertian surface with reflectance $\rho$ this is $\frac{\rho}{\pi} \bar E_r(x)$, where $\bar E_r(x)$ is the mean of the irradiance $E$ over the disc, while the true value is $\frac{\rho}{\pi} E(x)$.

**Theorem 3 (not consistent).** Fix $r$ and $x$, and let the variance of one path's contribution to $\hat L_r(x)$ be finite. As $N \to \infty$, $\hat L_r(x) \to E[\hat L_r(x)]$ almost surely. If $\bar E_r(x) \ne E(x)$, the limit is not the true value.

*Proof.* $\hat L_r(x)$ is the mean of $N$ independent copies of $N \cdot$(the contribution of one path), and each copy has the mean $E[\hat L_r(x)]$, which does not depend on $N$. The strong law of large numbers gives the limit. $\square$

**Theorem 4 (the bias is $O(r^2)$).** Let $E$ be twice continuously differentiable near $x$ on the plane. Then $\bar E_r(x) = E(x) + \frac{r^2}{8}\Delta E(x) + o(r^2)$.

*Proof.* In coordinates $(u, v)$ centered at $x$, Taylor's theorem gives $E(u, v) = E(x) + E_u u + E_v v + \frac{1}{2}(E_{uu} u^2 + 2E_{uv} uv + E_{vv} v^2) + o(u^2 + v^2)$. Over the disc, the integrals of $u$, $v$ and $uv$ are 0 by symmetry, and $\int_{D_r} u^2\, dA = \int_{D_r} v^2\, dA = \frac{1}{2}\int_0^r \rho^2 \cdot 2\pi\rho\, d\rho = \frac{\pi r^4}{4}$. Dividing by $\pi r^2$ gives $E(x) + \frac{1}{2}(E_{uu} + E_{vv})\frac{r^2}{4} + o(r^2)$. $\square$

For a point light of power $\Phi$ at height $h$, $E(s) = \frac{\Phi h}{4\pi}(h^2 + s^2)^{-3/2} = E(0)(1 - \frac{3s^2}{2h^2} + O(s^4))$, so $\Delta E(0) = -6E(0)/h^2$ and the relative bias is $-\frac{3r^2}{4h^2} + o(r^2)$.

**Theorem 5 (the furnace sphere is unbiased).** Inside a sphere of radius $R$ with constant irradiance, the estimate with the region $\{x' : \|x' - x\| < r\}$, $r < 2R$, and the divisor $\pi r^2$, is unbiased.

*Proof.* The region is a spherical cap. Its height is $h = r^2/(2R)$, because a point at the polar angle $\theta$ from $x$ has the chord distance $2R\sin(\theta/2)$ and the height $R(1 - \cos\theta) = 2R\sin^2(\theta/2)$. By Archimedes, a cap of height $h$ has area $2\pi R h = \pi r^2$. With constant irradiance $E$, Theorem 1 gives the expected flux $E \pi r^2$ in the cap, and the estimate divides by $\pi r^2$. $\square$
