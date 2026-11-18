---
title: Horizon-based ambient occlusion measures the blocked solid angle
proves: [correctness]
status: full
---

**Setting.** The camera is orthographic and looks along $-z$, so the view vector is $v = (0, 0, 1)$ at every pixel. A pixel has the point $P$ and the unit normal $n$ with $n_z > 0$. A direction $\omega$ has the azimuth $\theta$ in the screen plane and the elevation $\alpha \in [-\pi/2, \pi/2]$ above the view plane, so $\omega = (\cos\alpha \cos\theta, \cos\alpha \sin\theta, \sin\alpha)$ and $d\omega = \cos\alpha \, d\alpha \, d\theta$. The tangent angle $t(\theta)$ is the elevation of the tangent plane of $n$ in the azimuth $\theta$, so $\tan t(\theta) = -(n_x \cos\theta + n_y \sin\theta) / n_z$. The horizon $h(\theta) \ge t(\theta)$ is the largest elevation of a point of the depth buffer seen from $P$ in the azimuth $\theta$, or $t(\theta)$ if no point is higher. The method of the page computes

$$1 - A = \frac{1}{m} \sum_{k=0}^{m-1} \sum_{i} W(r_{k,i}) \big(\sin h_{k,i} - \sin h_{k,i-1}\big),$$

where, in the direction $\theta_k = 2\pi (k + \xi) / m$, $h_{k,0} = t(\theta_k)$ and $h_{k,i}$ is the running horizon after the $i$-th rise, found at the distance $r_{k,i}$.

**Lemma 1 (telescoping).** If $W \equiv 1$, the inner sum of a direction equals $\sin h - \sin t$, where $h$ is the largest elevation of its samples within the radius, or $t$ if there is none above $t$.

*Proof.* The running horizon only rises, and each rise adds $\sin h_{k,i} - \sin h_{k,i-1}$. The sum telescopes to the sine of the last value minus the sine of the first. $\square$

**Theorem 1 (the solid angle).** Assume that, seen from $P$, every direction below the horizon is blocked and every direction above it is open (the height-field view of the depth buffer). Then for $W \equiv 1$ and in the limit of many directions and exact horizons,

$$1 - A = \frac{1}{2\pi} \int_0^{2\pi} \big(\sin h(\theta) - \sin t(\theta)\big)\, d\theta$$

is the blocked part of the solid angle of the hemisphere above the tangent plane, divided by its total $2\pi$.

*Proof.* Since $\cos\alpha > 0$ and $n_z > 0$, $n \cdot \omega > 0$ holds if and only if $\tan\alpha > \tan t(\theta)$, that is $\alpha > t(\theta)$. So the hemisphere above the tangent plane is $\{(\theta, \alpha) : t(\theta) < \alpha \le \pi/2\}$, a half of the sphere, with solid angle $2\pi$. The blocked part is $\{t(\theta) < \alpha < h(\theta)\}$, with the solid angle $\int_0^{2\pi} \int_{t}^{h} \cos\alpha \, d\alpha \, d\theta = \int_0^{2\pi} (\sin h - \sin t)\, d\theta$. The sum over $m$ equally spaced directions is the rectangle rule for this integral, and by Lemma 1 the inner sums are the integrand. $\square$

So HBAO with $W \equiv 1$ measures solid angle without the cosine weight of the [ambient occlusion](/ambient-occlusion/) integral. The page on ground-truth ambient occlusion adds the cosine.

**Theorem 2 (planes are open).** If the depth buffer holds a plane and the lookup is exact on it, and $n$ is the normal of the plane, then $A = 1$ for every falloff $W$.

*Proof.* Every sample $S$ lies on the plane, so $S - P$ is a tangent vector and its elevation in its azimuth is $t(\theta)$. No sample rises above $h_{k,0} = t(\theta_k)$, so every inner sum is empty. $\square$

In floating point the elevation of a sample can exceed $t$ by a rounding error, so the tests allow $10^{-9}$.

**Theorem 3 (the wall).** Let $P$ lie on a frontal floor, $n = v$, at the distance $\delta > 0$ from the foot of an infinite straight wall that rises by $H$ toward the camera, with a flat top. With $W \equiv 1$ and no radius limit,

$$1 - A = \frac{1}{\pi} \arctan\frac{H}{\delta}.$$

*Proof.* Here $t \equiv 0$. Put the wall at $x \ge \delta$. In an azimuth with $\cos\theta > 0$, the ray in the screen plane reaches the wall at the horizontal distance $\rho = \delta / \cos\theta$, and the points of the top have the elevation $\arctan(H / \rho')$ for $\rho' \ge \rho$, which is largest at $\rho' = \rho$. So $\sin h = H / \sqrt{\rho^2 + H^2} = H \cos\theta / \sqrt{\delta^2 + H^2 \cos^2\theta}$. In the other azimuths $h = 0$. With $u = \sin\theta$, $du = \cos\theta \, d\theta$ and $\cos^2\theta = 1 - u^2$,

$$\frac{1}{2\pi} \int_{-\pi/2}^{\pi/2} \frac{H \cos\theta \, d\theta}{\sqrt{\delta^2 + H^2 \cos^2\theta}} = \frac{1}{2\pi} \int_{-1}^{1} \frac{du}{\sqrt{a^2 - u^2}} = \frac{1}{\pi} \arcsin\frac{1}{a}, \qquad a^2 = \frac{\delta^2 + H^2}{H^2}.$$

Finally $\arcsin(H / \sqrt{\delta^2 + H^2}) = \arctan(H / \delta)$. $\square$

At the foot of the wall, $\delta \to 0$ gives $1/2$, and far from it the value goes to 0. The tests compare the code with 64 directions and steps of 0.25 units with this formula within 0.02, and they check the formula itself by a Monte Carlo estimate with uniform directions.

**Theorem 4 (falloff and range).** If $0 \le W \le 1$, then $A$ with the falloff is at least $A$ with $W \equiv 1$. If $m$ is even, the directions come in opposite pairs and $0 \le A \le 1$.

*Proof.* Every term $\sin h_{k,i} - \sin h_{k,i-1}$ is positive, and the falloff multiplies it by at most 1, so the occlusion does not grow. For the range, by Lemma 1 the inner sum of a direction is at most $1 - \sin t(\theta)$, and $t(\theta + \pi) = -t(\theta)$ because $\tan t$ is linear in $(\cos\theta, \sin\theta)$. A pair of opposite directions thus adds at most $(1 - \sin t) + (1 + \sin t) = 2$, with or without the falloff, so $1 - A \le (1/m) \cdot (m/2) \cdot 2 = 1$. The terms are positive, so $A \le 1$. $\square$

**Theorem 5 (cost).** For $p$ pixels, $m$ directions and $s$ steps per direction, the cost is $O(p m s)$ lookups and $O(p m s)$ arithmetic.

*Proof.* Each step does one lookup, one arctangent and at most one sine. $\square$
