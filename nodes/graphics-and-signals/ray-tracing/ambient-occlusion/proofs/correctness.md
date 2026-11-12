---
title: The cosine-weighted ambient occlusion estimator is unbiased, its variance, and the closed forms of the tests
proves: [correctness]
status: full
---

**Setting.** A point $x$ has the unit normal $n$, and $\Omega$ is the hemisphere of unit directions $\omega$ with $\cos\theta = \omega \cdot n \ge 0$. For a distance $d_{\max} \in (0, \infty]$, $V(\omega) = 1$ if the ray $x + t\omega$ meets no surface for $0 < t \le d_{\max}$, and $V(\omega) = 0$ if it does. The accessibility is

$$A(x) = \frac1\pi \int_\Omega V(\omega) \cos\theta \, d\omega.$$

Because $\int_\Omega \cos\theta\, d\omega = \pi$, we have $0 \le A \le 1$. The algorithm draws $u_1, u_2$ uniform in $[0, 1)$, sets $r = \sqrt{u_1}$ and $\varphi = 2\pi u_2$, and takes $\omega = r\cos\varphi\, t + r\sin\varphi\, b + \sqrt{1 - u_1}\, n$ for an orthonormal frame $(t, b, n)$. It returns the fraction $\hat A$ of $N$ such independent rays with $V = 1$.

**Lemma 1 (Malley's method).** The direction $\omega$ has the density $\cos\theta / \pi$ on $\Omega$ with respect to the solid angle. Its projection $P\omega = (\omega \cdot t, \omega \cdot b)$ is uniform on the unit disk $D$.

*Proof.* The map $(u_1, u_2) \mapsto (r\cos\varphi, r\sin\varphi)$ has the area element $r\,dr\,d\varphi = \tfrac12 du_1 \cdot 2\pi du_2 = \pi\, du_1\, du_2$, so the point is uniform on $D$ with density $1/\pi$. The projection $P$ is a bijection from $\Omega$ onto $D$ with $\omega \cdot n = \sqrt{1 - |P\omega|^2}$, and an area element $d\omega$ on the sphere projects to the area $\cos\theta\, d\omega$ in the plane. So the density over $\Omega$ is $\frac1\pi \cos\theta$. $\square$

**Theorem (unbiased, with the variance of a Bernoulli mean).** $E[\hat A] = A(x)$ and $\operatorname{Var}[\hat A] = A(1 - A)/N$.

*Proof.* By Lemma 1, $E[V(\omega)] = \int_\Omega V(\omega) \frac{\cos\theta}{\pi} d\omega = A$. So each ray is a Bernoulli variable with the mean $A$, and $\hat A$ is the mean of $N$ independent copies. $\square$

A corollary: when $V = 1$ everywhere, the estimate is exactly $1$, with no variance. This is the sense in which cosine sampling is the [importance sampling](/importance-sampling/) density for the factor $\cos\theta$. The uniform density $1 / (2\pi)$ gives the estimator $2\cos\theta\, V(\omega)$, which is also unbiased, and whose second moment is $\frac{1}{2\pi} \int_\Omega 4 \cos^2\theta\, V \, d\omega$. For $V = 1$ this is $\tfrac43$, so its variance is $\tfrac13$ per ray where the cosine estimator has $0$.

**Corollary (the area rule).** Let $B = \{\omega \in \Omega : V(\omega) = 0\}$. Then $A = 1 - |P B| / \pi$, where $|PB|$ is the area of the projection of $B$ onto the disk. This follows from Lemma 1, because $P\omega$ is uniform on $D$, which has the area $\pi$.

**The closed forms of the tests.** Let $x$ be the origin and $n = (0, 0, 1)$.

1. *A wall.* The plane $\{p_1 = a\}$ with $a > 0$. A direction with $\omega_1 > 0$ meets it at $t = a / \omega_1$. So $V(\omega) = 0$ if and only if $\omega_1 \ge c = a / d_{\max}$. The projection of this set is the part $\{p_1 \ge c\}$ of $D$, with the area $\operatorname{seg}(c) = \arccos c - c\sqrt{1 - c^2}$ for $c < 1$ and $0$ for $c \ge 1$. So $A = 1 - \operatorname{seg}(c) / \pi$, and $A = \tfrac12$ when $d_{\max} = \infty$. Two walls at $p_1 = \pm a$ block disjoint sets, so $A = 1 - 2\operatorname{seg}(c)/\pi$.
2. *A sphere.* The center is at the distance $d$ in the direction $a$, with $a \cdot n = \cos\theta_c$, and the radius is $r < d$, so the sphere subtends the cone of directions $\{\omega \cdot a \ge \cos\alpha\}$ with $\sin\alpha = r / d$. Every ray in the cone meets the sphere at a distance below $d$, so take $d_{\max} \ge d$. Suppose $\theta_c + \alpha \le \pi/2$, so that the cone lies in $\Omega$. Its boundary on the unit sphere is a circle of the radius $\sin\alpha$ in a plane with the normal $a$. The projection $P$ maps this circle to an ellipse with the area $\pi \sin^2\alpha\, |a \cdot n|$, and, because $P$ is a bijection on $\Omega$, it maps the cap inside the circle to the inside of the ellipse. So $A = 1 - (r/d)^2 \cos\theta_c$.
3. *The inside of a closed sphere.* The center is at $(0, 0, R)$ and $x$ is on the sphere with the normal pointing inward. The ray at the angle $\theta$ to $n$ meets the sphere again at the chord length $t = 2R\cos\theta$. So $V = 0$ if and only if $\cos\theta \le \beta = d_{\max} / (2R)$. By the construction, $\sin^2\theta = u_1$ is uniform on $[0, 1]$, so $P(\cos\theta \le \beta) = P(u_1 \ge 1 - \beta^2) = \beta^2$ and $A = 1 - \beta^2$ for $d_{\max} \le 2R$. For $d_{\max} = \infty$, every ray is blocked and $A = 0$.
4. *Obscurance next to the wall.* With $\rho(s) = s$ and the value $\rho(\min(t, d_{\max}) / d_{\max})$ per ray, a ray with $p_1 = \omega_1 \ge c$ has the value $c / p_1$, and every other ray has the value $1$. By Lemma 1, the mean is $1 - \operatorname{seg}(c)/\pi + \frac1\pi \int_c^1 \frac{c}{p_1} 2\sqrt{1 - p_1^2}\, dp_1$. The derivative of $s - \ln\frac{1 + s}{p}$, where $s = \sqrt{1 - p^2}$, is $s / p$. So the integral is $2c\,(\ln\frac{1 + s_c}{c} - s_c)$ with $s_c = \sqrt{1 - c^2}$.

**What the value means physically.** Suppose $d_{\max} = \infty$, every surface other than $x$ is black and emits nothing, and the radiance that comes from every open direction is the constant $L$, as from a uniform sky at infinity. Then the irradiance at $x$ is $E(x) = \int_\Omega L\, V \cos\theta\, d\omega = \pi L A(x)$, and a Lambertian surface with the albedo $\rho$ reflects the radiance $\rho L A(x)$. This is the only case in which ambient occlusion shading is exact. If the occluders reflect light, or if $d_{\max}$ is finite, the [rendering equation](/rendering-equation/) gives another value. For example, inside a closed sphere that emits $L_e$ and has the albedo $\rho < 1$ everywhere, the radiance is $L_e / (1 - \rho)$ at every point, but $A = 0$.
