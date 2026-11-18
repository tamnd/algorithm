---
title: The slice integral of ground-truth ambient occlusion and its closed form
proves: [correctness]
status: full
---

**Setting.** The camera is orthographic and looks along $-z$, so the view vector is $v = (0, 0, 1)$ at every pixel, as in the code. A pixel has the point $P$ and the unit normal $n$ with $n \cdot v > 0$. For $\varphi \in [0, \pi)$ let $c(\varphi) = (\cos\varphi, \sin\varphi, 0)$. The slice $\varphi$ is the plane spanned by $v$ and $c$, and a direction in it is $\omega(h, \varphi) = \cos h \, v + \sin h \, c$ with $h \in (-\pi, \pi]$, measured from $v$ and positive toward $c$. The projection of $n$ into the slice is $n_p = (n \cdot c)\, c + (n \cdot v)\, v$, with the length $|n_p|$ and the angle $\gamma = \operatorname{atan2}(n \cdot c, n \cdot v) \in (-\pi/2, \pi/2)$ from $v$. The height-field assumption: in each slice, the directions between the two horizons $h_1 \le 0 \le h_2$ are open and the others are blocked, where the horizons are clamped to $[\gamma - \pi/2, \gamma + \pi/2]$. The [ambient occlusion](/ambient-occlusion/) visibility is $A = \frac{1}{\pi} \int_{n \cdot \omega > 0} V(\omega)\, (n \cdot \omega)\, d\omega$.

**Lemma 1 (slice coordinates).** The map $(h, \varphi) \mapsto \omega(h, \varphi)$ on $(-\pi, \pi] \times [0, \pi)$ covers the unit sphere once, apart from the two directions $\pm v$, with $d\omega = |\sin h| \, dh \, d\varphi$. In it, $n \cdot \omega = |n_p| \cos(h - \gamma)$.

*Proof.* With $v$ as the polar axis, a direction with $h > 0$ has the polar angle $h$ and the azimuth $\varphi$, and one with $h < 0$ has the polar angle $-h$ and the azimuth $\varphi + \pi$. As $\varphi$ runs over $[0, \pi)$ the two cases cover all azimuths once, and the spherical element is $\sin(\text{polar}) \, d(\text{polar}) \, d(\text{azimuth}) = |\sin h| \, dh \, d\varphi$. Next, $n \cdot \omega = (n \cdot v) \cos h + (n \cdot c) \sin h = |n_p| (\cos\gamma \cos h + \sin\gamma \sin h) = |n_p| \cos(h - \gamma)$. $\square$

**Theorem 1 (the slice integral).** Under the height-field assumption,

$$A = \frac{1}{\pi} \int_0^\pi |n_p| \, \hat a(\varphi) \, d\varphi, \qquad \hat a = \int_{h_1}^{h_2} \cos(h - \gamma)\, |\sin h| \, dh.$$

*Proof.* By Lemma 1, $n \cdot \omega > 0$ in the slice exactly for $h \in (\gamma - \pi/2, \gamma + \pi/2)$, and the open part of it is $[h_1, h_2]$ because of the clamp. Substituting Lemma 1 into the definition of $A$ gives the formula. $\square$

**Theorem 2 (closed form).** For $h_1 \le 0 \le h_2$,

$$\hat a = \tfrac14 \big( -\cos(2h_1 - \gamma) + \cos\gamma + 2 h_1 \sin\gamma \big) + \tfrac14 \big( -\cos(2h_2 - \gamma) + \cos\gamma + 2 h_2 \sin\gamma \big).$$

*Proof.* On $[0, h_2]$, $|\sin h| = \sin h$ and $\sin h \cos(h - \gamma) = \tfrac12 (\sin(2h - \gamma) + \sin\gamma)$, so

$$\int_0^{h_2} \sin h \cos(h - \gamma)\, dh = \tfrac12 \Big[ -\tfrac12 \cos(2h - \gamma) + h \sin\gamma \Big]_0^{h_2} = \tfrac14 \big( -\cos(2h_2 - \gamma) + \cos\gamma + 2 h_2 \sin\gamma \big),$$

using $\cos(-\gamma) = \cos\gamma$. On $[h_1, 0]$, $|\sin h| = -\sin h$, and the same antiderivative gives $-\tfrac12 \big[ -\tfrac12 \cos(2h - \gamma) + h \sin\gamma \big]_{h_1}^{0} = \tfrac14 \big( -\cos(2h_1 - \gamma) + \cos\gamma + 2 h_1 \sin\gamma \big)$. $\square$

The tests compare this form with Simpson's rule at random arguments and find agreement to $10^{-10}$. This page derives the formula itself; it is not copied from the report of Jimenez and others.

**Theorem 3 (open surfaces).** If every slice is open, $h_1 = \gamma - \pi/2$ and $h_2 = \gamma + \pi/2$, then $\hat a = \cos\gamma + \gamma \sin\gamma$ and $A = 1$. In particular, a plane gives $A = 1$, and a frontal plane gives $\hat a = 1$ in every slice.

*Proof.* With $h_{1,2} = \gamma \mp \pi/2$, $\cos(2h_{1,2} - \gamma) = \cos(\gamma \mp \pi) = -\cos\gamma$, and Theorem 2 gives $\tfrac14 (4 \cos\gamma + 4\gamma \sin\gamma)$. The integral of Theorem 1 is then $\frac1\pi \int_{n \cdot \omega > 0} n \cdot \omega \, d\omega = 1$, the cosine integral over a hemisphere. On a plane, every sample lies in the tangent plane, so no horizon rises above the clamp. For $n = v$, $\gamma = 0$ and $\hat a = 1$. $\square$

The code sums $m$ equally spaced slices, the rectangle rule for an integrand that is smooth and periodic in $\varphi$ with period $\pi$. For a tilted plane the sum is not exactly 1, but the error falls fast with $m$: the tests measure an error below $10^{-9}$ with 16 slices for slopes up to 1.3.

**Theorem 4 (the wall).** Let $P$ lie on a frontal floor, $n = v$, at the distance $\delta > 0$ from the foot of an infinite straight wall that rises by $H$ toward the camera, with a flat top. With no radius limit,

$$A = \frac12 \Big( 1 + \frac{\delta}{\sqrt{\delta^2 + H^2}} \Big).$$

*Proof.* Here $\gamma = 0$ and $|n_p| = 1$. Put the wall at $x \ge \delta$. In the slice $\varphi$ with $\cos\varphi \ne 0$, the side that points to $+x$ reaches the foot at the horizontal distance $\delta / |\cos\varphi|$, and the top edge has the elevation $e$ above the view plane with $\tan e = H |\cos\varphi| / \delta$, which is the largest elevation on that side. So that horizon is $\pi/2 - e$ in absolute value, and the other side is open with the horizon $\pi/2$. By Theorem 2 with $\gamma = 0$, the open side gives $\tfrac14 (1 - \cos\pi) = \tfrac12$, and the wall side gives $\tfrac14 (1 - \cos(\pi - 2e)) = \tfrac14 (1 + \cos 2e) = \tfrac12 \cos^2 e$. So $\hat a = 1 - \tfrac12 \sin^2 e$ with $\sin^2 e = H^2 \cos^2\varphi / (\delta^2 + H^2 \cos^2\varphi)$, and

$$1 - A = \frac{1}{2\pi} \int_0^\pi \frac{H^2 \cos^2\varphi}{\delta^2 + H^2 \cos^2\varphi} \, d\varphi = \frac{1}{2\pi} \Big( \pi - \delta^2 \int_0^\pi \frac{d\varphi}{\delta^2 + H^2 \cos^2\varphi} \Big).$$

The standard integral $\int_0^\pi d\varphi / (a + b \cos^2\varphi) = \pi / \sqrt{a (a + b)}$ for $a > 0$, $b \ge 0$ gives $\pi / (\delta \sqrt{\delta^2 + H^2})$, so $1 - A = \tfrac12 (1 - \delta / \sqrt{\delta^2 + H^2})$. $\square$

This is the view factor of an infinite strip seen from a point, which also follows from the crossed-strings rule. The same wall gives $1 - \arctan(H/\delta)/\pi$ under the solid-angle measure of horizon-based ambient occlusion. The tests check the formula by cosine-weighted Monte Carlo rays and the code against it within 0.01.

**Theorem 5 (range).** In the integral of Theorem 1, $0 \le A \le 1$, and the occlusion grows when a horizon rises.

*Proof.* On $[h_1, h_2] \subseteq [\gamma - \pi/2, \gamma + \pi/2]$ the integrand $\cos(h - \gamma) |\sin h|$ is non-negative, so $\hat a \ge 0$ and $\hat a$ shrinks when $[h_1, h_2]$ shrinks. The largest value is the open case of Theorem 3. $\square$

**What is not a theorem.** The match of $A$ with ray traced ambient occlusion holds under the height-field assumption, that is, for the scene as the one layer of the depth buffer shows it. A real scene can have open space behind the visible surface. The tests render a plate of thickness 1 whose bottom is 4 units above the floor: the depth buffer sees only its top, as if it were a solid block, and the code gives $A = 0.792$ at a floor point 3.5 units from the plate, while cosine-weighted rays against the true plate give $0.828$. Any statement about how close GTAO comes to ray traced ambient occlusion in real scenes is a measurement.

**Theorem 6 (cost).** For $p$ pixels, $m$ slices and $s$ steps per side, the cost is $O(p m s)$.

*Proof.* Each slice marches $2s$ steps of $O(1)$ work and evaluates Theorem 2 once. $\square$
