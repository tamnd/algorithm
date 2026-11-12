---
title: The VPLs reproduce the light of the scene in expectation, the clamp makes the estimate low, and the furnace and sensor values are exact
proves: [correctness]
status: full
---

The scene is a set of Lambertian surfaces $\mathcal M$ with reflectance $\rho(y) < 1$ and emitted exitance $B_e(y)$, with the total emitted power $\Phi = \int_{\mathcal M} B_e\, dA$. Let $G(x, y) = \cos\theta_x \cos\theta_y / |x - y|^2$ and let $V(x, y)$ be the visibility. Let $L_0(y) = B_e(y)/\pi$ be the emitted radiance, and let

$$L_{k+1}(y') = \frac{\rho(y')}{\pi} \int_{\mathcal M} L_k(y)\, G(y, y')\, V(y, y')\, dA(y)$$

be the outgoing radiance after exactly $k + 1$ reflections. The radiance of the scene is $L = \sum_{k \ge 0} L_k$.

Line L3 samples $y$ with the density $B_e(y)/\Phi$ and sets $\beta = \Phi/N$ and $f = 1/\pi$. Line L5 lets a walk go on from a surface vertex with the probability $\rho(y) = \pi f$, and from a light vertex always, which is also $\pi f$ since $f = 1/\pi$ there. Line L6 samples $\omega$ with the density $\cos\theta_y/\pi$ about the normal.

**Lemma 1 (one depth).** For each $k \ge 0$ and each measurable $h \ge 0$ on $\mathcal M$,

$$E\Big[\sum_{v \text{ at depth } k} \beta_v f_v\, h(y_v)\Big] = \int_{\mathcal M} L_k(y)\, h(y)\, dA(y).$$

*Proof.* By induction on $k$. For $k = 0$ there are $N$ light vertices, so the left side is $N \cdot \frac{\Phi}{N} \cdot \frac{1}{\pi} \int \frac{B_e(y)}{\Phi} h(y)\, dA = \int L_0\, h\, dA$.

For $k + 1$, fix a vertex $v$ at depth $k$. The walk goes on with the probability $\pi f_v$, keeps the power $\beta_v$, and reaches the nearest hit $y'$ in the direction $\omega$. The next VPL has $f = \rho(y')/\pi$. So

$$E[\beta f\, h(y') \mid v] = \pi f_v\, \beta_v \int_{H^2} \frac{\cos\theta_{y_v}}{\pi} \frac{\rho(y')}{\pi} h(y')\, d\omega = \beta_v f_v\, H(y_v),$$

with $H(y) = \int_{\mathcal M} G(y, y') V(y, y') \frac{\rho(y')}{\pi} h(y')\, dA(y')$. The change of variables from $\omega$ to the visible point $y'$ uses $\cos\theta_y\, d\omega = G(y, y') V(y, y')\, dA(y')$. Sum over the vertices at depth $k$ and use the hypothesis with $H$:

$$E\Big[\sum_{\text{depth } k + 1}\beta f h\Big] = \int L_k(y) H(y)\, dA(y) = \int h(y') \frac{\rho(y')}{\pi} \int L_k(y) G V\, dA(y)\, dA(y') = \int L_{k+1} h\, dA,$$

by Fubini's theorem for nonnegative functions. $\square$

**Theorem 1 (unbiased without the clamp).** With $G_{\max} = \infty$, the estimate of line L11 at a point $x$ with the BRDF $f_r(x) = \rho_x/\pi$ has the expected value

$$E[\hat L_r(x)] = f_r(x)\int_{\mathcal M} L(y)\, G(x, y)\, V(x, y)\, dA(y) = L_r(x).$$

*Proof.* Lines L8 to L11 give $\hat L_r(x) = f_r(x) \sum_v \beta_v f_v G(x, y_v) V(x, y_v)$. Apply Lemma 1 with $h = G(x, \cdot) V(x, \cdot)$ for each $k$ and add over $k$. All the terms are nonnegative, so the sum and the expectation commute by monotone convergence. The right side is the reflected radiance at $x$ of the light that leaves all the surfaces, which is the integral of the problem. $\square$

A point light at $p$ with the power $\Phi$ fits the same proof: its vertex has the radiant intensity $\beta/(4\pi)$ in all directions, the walk leaves it in a uniform direction, and $L_0$ is replaced by the irradiance $\Phi \cos\theta_{y}/(4\pi |p - y|^2)$ at the first hits.

**Theorem 2 (the clamp makes the estimate low).** With a finite $G_{\max}$,

$$E[\hat L_r(x)] = L_r(x) - f_r(x)\int_{\mathcal M} L(y)\, \big(G(x, y) - G_{\max}\big)_+\, V(x, y)\, dA(y),$$

where $(t)_+ = \max(t, 0)$. The bias is never positive, and it is negative when $L > 0$ on a visible set of positive area where $G(x, y) > G_{\max}$.

*Proof.* Apply Lemma 1 with $h = \min(G(x, \cdot), G_{\max}) V(x, \cdot)$ and use $\min(G, G_{\max}) = G - (G - G_{\max})_+$. $\square$

The set where $G(x, y) > G_{\max}$ lies within the distance $G_{\max}^{-1/2}$ of $x$, because $G \le 1/|x - y|^2$. So the clamp removes only short-range light.

**Lemma 2 (the furnace).** Inside the unit sphere with constant $B_e$ and $\rho$, the estimate is $\hat L_r = \frac{\rho B_e}{\pi}\left(1 + \frac{\rho S}{N}\right)$, where $S$ is the number of surface VPLs. Its mean is $\frac{\rho B_e}{\pi (1 - \rho)}$ and its standard deviation is $\frac{\rho^2 B_e}{\pi}\sqrt{\rho/((1 - \rho)^2 N)}$.

*Proof.* Inside a sphere of radius 1, $G(x, y) = 1/4$ for all $x \ne y$ on the sphere (the radiosity page proves the general form $1/(4R^2)$), and $V = 1$. The total power is $\Phi = 4\pi B_e$, so a light VPL adds $\frac{4\pi B_e}{N}\cdot\frac{1}{\pi}\cdot\frac14 = \frac{B_e}{N}$ and a surface VPL adds $\frac{\rho B_e}{N}$ to the sum of line L10. Multiply by $f_r = \rho/\pi$. Each walk has a first surface vertex, since the sphere is closed, and then goes on with the probability $\rho$ at each vertex. So its number $K$ of surface vertices has $P(K \ge k) = \rho^{k - 1}$, the mean $1/(1 - \rho)$ and the variance $\rho/(1 - \rho)^2$. $S$ is the sum of $N$ independent copies of $K$. $\square$

**Lemma 3 (the sensor).** For a point light of power $\Phi$ at the height $h$ over a floor with the reflectance $\rho$, and a sensor point at the height $a$ on the axis that faces the floor and has the reflectance $\rho_x$, the one-bounce reflected radiance is

$$L_r(a) = \frac{\rho_x}{\pi}\int_0^\infty \frac{\rho}{\pi}\, \frac{\Phi h}{4\pi(h^2 + r^2)^{3/2}}\, \frac{a^2}{(a^2 + r^2)^2}\, 2\pi r\, dr.$$

For $a = h$ it is $\frac{\rho_x \rho \Phi}{10 \pi^2 a^2}$. The integral of $G^2$ over the floor is $\pi/(3a^2)$.

*Proof.* The floor point at the distance $r$ from the axis has the irradiance $\Phi h/(4\pi(h^2 + r^2)^{3/2})$ and the radiance $\rho/\pi$ times that. For the sensor, $\cos\theta_x = \cos\theta_y = a/d$ with $d^2 = a^2 + r^2$, so $G = a^2/(a^2 + r^2)^2$. For $a = h$ the integrand is $\frac{\rho\Phi a^3}{2\pi}\, r (a^2 + r^2)^{-7/2}$, and $\int_0^\infty r (a^2 + r^2)^{-7/2} dr = \frac{1}{5a^5}$. Multiply by $\rho_x/\pi$. For the second moment, $\int_0^\infty \frac{a^4}{(a^2 + r^2)^4} 2\pi r\, dr = 2\pi a^4 \cdot \frac{1}{6a^6} = \frac{\pi}{3a^2}$. $\square$

The tests check Lemma 2 with the stated standard deviation and Lemma 3 against Simpson's rule, and they check Theorems 1 and 2 in the sensor scene: the unclamped mean agrees with $L_r(a)$ and the clamped mean agrees with the clamped integral, each within four standard errors.
