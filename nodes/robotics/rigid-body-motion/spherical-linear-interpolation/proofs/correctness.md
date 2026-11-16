---
title: SLERP returns the point at the fraction t of the short arc
proves: [correctness]
status: full
---

We use the notation of the page.
Quaternions are in the Hamilton convention, scalar first, and we treat them also as vectors of $\mathbb{R}^4$ with the usual dot product and length.
For unit quaternions, $|pq| = |p|\,|q|$, and left or right multiplication by a unit quaternion is a linear isometry of $\mathbb{R}^4$.
A unit quaternion $q$ gives the rotation $R(q)$ with $R(q)v$ equal to the vector part of $q\,(0, v)\,q^*$, and $R(pq) = R(p)R(q)$, $R(-q) = R(q)$.

## The sign test

**Lemma 1.** After lines L1 to L3, $q_0 \cdot q_1 \ge 0$, and $q_1$ is a quaternion of the same rotation as the input $q_1$.

*Proof.*
If $d < 0$, line L3 replaces $q_1$ by $-q_1$, and $q_0 \cdot (-q_1) = -d > 0$.
Since $R(-q_1) = R(q_1)$, the rotation does not change. $\square$

## The angle

**Lemma 2.** Let $q_0$ and $q_1$ be unit vectors with $q_0 \cdot q_1 = \cos\Omega$, $\Omega \in [0, \pi]$.
Then $|q_1 - q_0| = 2\sin\frac\Omega2$, $|q_1 + q_0| = 2\cos\frac\Omega2$, and line L4 returns $\Omega$.
After Lemma 1, $\Omega \in [0, \pi/2]$.

*Proof.*
$|q_1 \mp q_0|^2 = 2 \mp 2\cos\Omega$, which is $4\sin^2\frac\Omega2$ or $4\cos^2\frac\Omega2$.
Both square roots are of numbers that are not negative, and $\frac\Omega2 \in [0, \frac\pi2]$, so $\operatorname{atan2}(2\sin\frac\Omega2, 2\cos\frac\Omega2) = \frac\Omega2$.
If $\cos\Omega \ge 0$, then $\Omega \le \pi/2$. $\square$

## The arc formula

**Lemma 3.** Let $0 < \Omega \le \pi/2$.
The great circle arc from $q_0$ to $q_1$ with constant speed, $\gamma : [0, 1] \to S^3$, is

$$\gamma(t) = \frac{\sin((1 - t)\Omega)}{\sin\Omega}\, q_0 + \frac{\sin(t\Omega)}{\sin\Omega}\, q_1,$$

and the angle between $\gamma(s)$ and $\gamma(t)$ is $|t - s|\,\Omega$.

*Proof.*
Put $p = (q_1 - \cos\Omega\, q_0)/\sin\Omega$.
Then $p \cdot q_0 = (\cos\Omega - \cos\Omega)/\sin\Omega = 0$ and $|p|^2 = (1 - 2\cos^2\Omega + \cos^2\Omega)/\sin^2\Omega = 1$.
So $q_0$ and $p$ are orthonormal, and $q_1 = \cos\Omega\, q_0 + \sin\Omega\, p$.
The great circle in their plane is $\gamma(t) = \cos(t\Omega)\, q_0 + \sin(t\Omega)\, p$, with $\gamma(0) = q_0$ and $\gamma(1) = q_1$, and $\gamma(s) \cdot \gamma(t) = \cos((t - s)\Omega)$.
Substituting $p$ gives

$$\gamma(t) = \Big(\cos(t\Omega) - \frac{\sin(t\Omega)\cos\Omega}{\sin\Omega}\Big) q_0 + \frac{\sin(t\Omega)}{\sin\Omega}\, q_1,$$

and the first coefficient is $\sin(\Omega - t\Omega)/\sin\Omega$ by the subtraction formula of the sine. $\square$

So lines L8 to L10 return $\gamma(t)$ when $\Omega \ge \delta$.

## The power form and the rotations

**Lemma 4.** Let $q_0 \cdot q_1 = \cos\Omega \ge 0$ and $\Omega > 0$.
Then $q_0^* q_1 = (\cos\Omega, \sin\Omega\,\hat u)$ for a unit $\hat u \in \mathbb{R}^3$, and $\gamma(t) = q_0\,(\cos(t\Omega), \sin(t\Omega)\,\hat u)$.
The rotation $R(\gamma(t))$ is $R_0\, e^{t[w]}$ with $w = 2\Omega\hat u = \log(R_0^{\mathsf T}R_1)$.

*Proof.*
The scalar part of $q_0^* q_1$ is $q_0 \cdot q_1 = \cos\Omega$, and $q_0^* q_1$ has length 1, so its vector part has length $\sin\Omega$.
Let $L$ be the left multiplication by $q_0$.
$L$ is a linear isometry, $L(1) = q_0$ and $L(q_0^* q_1) = q_1$.
The isometry maps the great arc from $1$ to $q_0^* q_1$, which is $(\cos(t\Omega), \sin(t\Omega)\hat u)$ by Lemma 3, to the great arc from $q_0$ to $q_1$ with the same parameter, which is $\gamma(t)$.
The unit quaternion $(\cos(t\Omega), \sin(t\Omega)\hat u)$ is the rotation by $2t\Omega$ about $\hat u$, which is $e^{t[w]}$ by Rodrigues' formula.
So $R(\gamma(t)) = R_0 e^{t[w]}$.
At $t = 1$, $e^{[w]} = R_0^{\mathsf T}R_1$, and $|w| = 2\Omega \le \pi$, so $w$ is a value of the logarithm of $R_0^{\mathsf T}R_1$; it is the only value when $2\Omega < \pi$. $\square$

The same proof with $t\Omega$ for $\Omega$ shows that $(q_0^* q_1)^t$, defined as $(\cos(t\Omega), \sin(t\Omega)\hat u)$, is the power used in the formula $q_0(q_0^* q_1)^t$.

## The branch for small angles

**Lemma 5.** Let $0 \le \Omega < \delta$ and $t \in [0, 1]$.
The point of lines L6 and L7 lies on the great arc from $q_0$ to $q_1$, at an angle $\varphi(t)$ from $q_0$ with $|\varphi(t) - t\Omega| \le \frac{\sqrt3}{108}\Omega^3 + O(\Omega^5)$.

*Proof.*
If $\Omega = 0$, then $q_1 = q_0$ and lines L6 and L7 return $q_0$, which is $\gamma(t)$.
Otherwise, with the orthonormal $q_0, p$ of Lemma 3, $(1 - t)q_0 + t q_1 = ((1 - t) + t\cos\Omega)\, q_0 + t\sin\Omega\, p$.
For $t \in [0, 1]$ and $\Omega \le \pi/2$ both coefficients are not negative and not both zero, so the normalized point is $\cos\varphi\, q_0 + \sin\varphi\, p$ with $\varphi = \operatorname{atan2}(t\sin\Omega, 1 - t + t\cos\Omega) \in [0, \Omega]$.
The Taylor expansion in $\Omega$ is $\varphi = t\Omega - \frac16 t(1 - t)(1 - 2t)\Omega^3 + O(\Omega^5)$.
The cubic $t(1 - t)(1 - 2t)$ has the largest absolute value $\sqrt3/18$ on $[0, 1]$, at $t = (3 \mp \sqrt3)/6$, which gives the bound. $\square$

With $\delta = 10^{-6}$, the bound is about $1.6 \cdot 10^{-20}$, far below the unit roundoff.

## Conclusion

**Theorem.** For unit quaternions $q_0$, $q_1$ and $t \in [0, 1]$, SLERP returns the point at the fraction $t$ of the shorter great arc from $q_0$ to the quaternion $\pm q_1$ with a dot product that is not negative, exactly when $\Omega \ge \delta$ and within the bound of Lemma 5 when $\Omega < \delta$.
Its rotation is $R_0\, e^{t \log(R_0^{\mathsf T}R_1)}$, and it moves at the constant angular speed $2\Omega$ about a fixed axis.

*Proof.*
Lemma 1 fixes the sign, Lemma 2 gives the angle, and Lemmas 3 and 5 give the two branches.
Lemma 4 gives the rotation form.
By Lemma 3, equal steps of $t$ give equal arc angles, and by Lemma 4 the rotation angle of $R(\gamma(s))^{\mathsf T}R(\gamma(t))$ is $2|t - s|\,\Omega$, about the fixed axis $\hat u$ in the frame of $R_0$. $\square$
