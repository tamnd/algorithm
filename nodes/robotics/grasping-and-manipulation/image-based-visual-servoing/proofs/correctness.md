---
title: IBVS makes the image error decrease and converges locally at the rate lambda
proves: [correctness]
status: full
---

The camera moves with the body twist $V = (\omega, v)$, angular part first, expressed in the camera frame. A point fixed in the world has camera coordinates $P = (X, Y, Z)$ with $Z > 0$ and image coordinates $x = X/Z$, $y = Y/Z$. The feature vector $s$ stacks the image coordinates of $k$ points, $e = s - s^*$, and $L$ is the stacked interaction matrix. We assume that $L$ has full column rank 6 along the motion, so $L^+ = (L^T L)^{-1}L^T$, and that the depths in $L$ are exact.

**Lemma 1 (interaction matrix of a point).** $\dot x = xy\,\omega_x - (1 + x^2)\omega_y + y\,\omega_z - v_x/Z + x v_z/Z$ and $\dot y = (1 + y^2)\omega_x - xy\,\omega_y - x\,\omega_z - v_y/Z + y v_z/Z$.

*Proof.* A point fixed in the world moves in the camera frame as $\dot P = -v - \omega \times P$. So $\dot X = -v_x - \omega_y Z + \omega_z Y$, $\dot Y = -v_y - \omega_z X + \omega_x Z$ and $\dot Z = -v_z - \omega_x Y + \omega_y X$. Then $\dot x = \dot X/Z - x\dot Z/Z$. Putting in the three derivatives and $X = xZ$, $Y = yZ$ gives $\dot x = -v_x/Z - \omega_y + y\omega_z + x v_z/Z + x(y\omega_x - x\omega_y)$, which is the first formula. The second follows in the same way from $\dot y = \dot Y/Z - y\dot Z/Z$. $\square$

So $\dot s = LV$, and under the law $V = -\lambda L^+ e$ the error obeys $\dot e = -\lambda L L^+ e$.

**Theorem 1 (the image error does not grow).** Along the closed loop, $\frac{d}{dt}\tfrac12\|e\|^2 = -\lambda\|L L^+ e\|^2 \le 0$. It is zero exactly when $L^T e = 0$.

*Proof.* $P = L L^+ = L(L^T L)^{-1}L^T$ is symmetric and $P^2 = P$, so it is the orthogonal projection onto the range of $L$. Then $\frac{d}{dt}\tfrac12\|e\|^2 = e^T\dot e = -\lambda e^T P e = -\lambda e^T P^T P e = -\lambda\|Pe\|^2$. The projection $Pe$ is zero if and only if $e$ is orthogonal to the range of $L$, that is $L^T e = 0$. $\square$

With three points, $L$ is square and $P = I$, so $\dot e = -\lambda e$ and $e(t) = e^{-\lambda t}e(0)$ while $L$ stays invertible. With four or more points, $2k > 6$, and the set $L^T e = 0$ with $e \ne 0$ contains the local minima of IBVS: the camera stops at a pose that is not the goal.

**Theorem 2 (local exponential convergence of the pose).** Let the goal pose be the identity, let $s(T)$ be the features at the camera pose $T$, and let $L_0$, the interaction matrix at the goal, have rank 6. Write $T = \exp([\xi])$. Then the linearization of the closed loop at $\xi = 0$ is $\dot\xi = -\lambda\xi$, so the goal is locally exponentially stable with rate $\lambda$.

*Proof.* Near the identity, $\dot\xi = V + O(\|\xi\|\,\|V\|)$, because the right Jacobian of the exponential map is $I + O(\|\xi\|)$. By Lemma 1, $s(\exp([\xi])) = s^* + L_0\xi + O(\|\xi\|^2)$. The matrices $L$ and $L^+$ depend smoothly on $\xi$ near 0, so $V = -\lambda L^+ e = -\lambda L_0^+ L_0\xi + O(\|\xi\|^2) = -\lambda\xi + O(\|\xi\|^2)$, since $L_0^+ L_0 = I$ for full column rank. So $\dot\xi = -\lambda\xi + O(\|\xi\|^2)$, and Lyapunov's indirect method gives local exponential stability. $\square$

**Proposition 3 (rotation about the optical axis).** Let all points have the same depth $Z$ in both poses, with the target plane parallel to the image plane, and let the camera be rotated by an angle $\theta \in (-\pi, \pi]$ about its optical axis, so that every current feature is $s_i = R(-\theta)s_i^*$, with $R(\cdot)$ the plane rotation. With $L$ at the current features, the first twist is $\omega_z = -\lambda\sin\theta$, $v_z = -\lambda Z(1 - \cos\theta)$, and all other components are zero.

*Proof.* Write $J$ for the rotation of the plane by $\pi/2$. For one point, the $\omega_z$ column of Lemma 1 is $(y, -x) = -Js_i$ and the $v_z$ column is $s_i/Z$. Since $s_i^* = R(\theta)s_i$ and $R(\theta) = \cos\theta\,I + \sin\theta\,J$, we get $e_i = s_i - s_i^* = (1 - \cos\theta)s_i - \sin\theta\,Js_i$. The candidate twist gives $LV = -\omega_z Js_i + v_z s_i/Z = \lambda\sin\theta\,Js_i - \lambda(1 - \cos\theta)s_i = -\lambda e_i$ for every point. So $-\lambda e$ is in the range of $L$, and since $L$ has full column rank, $L^+(-\lambda e)$ is the unique $V$ with $LV = -\lambda e$, which is the candidate. $\square$

For $\theta \ne 0$, $v_z < 0$, so the camera first moves backward along its optical axis. With $L$ at the desired features, the same computation with $s_i^*$ in place of $s_i$ gives $v_z = +\lambda Z(1 - \cos\theta)$, a forward motion.

**Corollary 4 (half turn).** Let the target be at depth 1 in the goal pose, and let the camera start rotated by $\pi$ about its optical axis at depth $Z_0$. Then the law is a pure backward translation for all time, and the depth is $Z(t) = Z_0 e^{\lambda t}/(1 + Z_0 - Z_0 e^{\lambda t})$, which is infinite at $t = \ln(1 + 1/Z_0)/\lambda$.

*Proof.* While the rotation is $\pi$ and the camera has only moved along its optical axis, the current features are $s_i = -s_i^*/Z$. Then $e_i = -(1 + 1/Z)s_i^*$, and $V = (0, 0, 0, 0, 0, -\lambda Z(1 + Z))$ gives $LV = -\lambda Z(1 + Z)\,s_i/Z = \lambda(1 + Z)s_i^*/Z = -\lambda e_i$. By full column rank this is the twist of the law. It has $\omega = 0$ and moves the camera only along its optical axis, so the form $s_i = -s_i^*/Z$ stays valid, and $\dot Z = -v_z = \lambda Z(1 + Z)$. Separating variables, $\ln\frac{Z}{1 + Z} = \lambda t + \ln\frac{Z_0}{1 + Z_0}$, which solves to the formula. Its denominator vanishes at the stated time. $\blacksquare$

In this case the image error is $e(t) = e^{-\lambda t}e(0)$ exactly, as Theorem 1 with $Pe = e$ predicts, but the features reach the image center when the camera is infinitely far away. This is the classical failure of IBVS for a half turn about the optical axis.
