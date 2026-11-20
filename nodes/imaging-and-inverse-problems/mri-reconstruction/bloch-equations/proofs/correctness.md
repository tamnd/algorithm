---
title: Closed form solutions of the Bloch equation used to check the integrator
proves: [correctness]
status: full
---

The equation is, with $M = (M_x, M_y, M_z)$ and the angular frequency vector $\omega(t) = \gamma B(t)$,

$$\frac{dM}{dt} = M \times \omega - \Bigl(\frac{M_x}{T_2}, \frac{M_y}{T_2}, \frac{M_z - M_0}{T_1}\Bigr), \tag{1}$$

where $1/T_1$ or $1/T_2$ is read as 0 when the time is infinite. The right side is linear in $M$ plus a constant, with coefficients that are continuous in $t$ when $\omega$ is continuous, so it is Lipschitz in $M$. By the Picard-Lindelöf theorem, (1) has exactly one solution for each start $M(0)$. So any function that satisfies (1) and the start is the solution. The integrator of the page is the classical Runge-Kutta method, whose global error is $O(h^4)$ for a smooth right side; the tests compare it with the closed forms below.

**Theorem 1 (free precession and relaxation).** Let $\omega = (0, 0, \omega_0)$ be constant. Write $M_{xy} = M_x + i M_y$. Then

$$M_{xy}(t) = M_{xy}(0)\, e^{-i \omega_0 t}\, e^{-t/T_2}, \qquad M_z(t) = M_0 + (M_z(0) - M_0)\, e^{-t/T_1}.$$

*Proof.* With $\omega = (0, 0, \omega_0)$, the cross product is $M \times \omega = (M_y \omega_0, -M_x \omega_0, 0)$. So (1) reads $\dot M_x = \omega_0 M_y - M_x/T_2$, $\dot M_y = -\omega_0 M_x - M_y/T_2$ and $\dot M_z = -(M_z - M_0)/T_1$. Then

$$\dot M_{xy} = \omega_0 M_y - i \omega_0 M_x - \frac{M_{xy}}{T_2} = -i \omega_0 (M_x + i M_y) - \frac{M_{xy}}{T_2} = -\Bigl(i \omega_0 + \frac{1}{T_2}\Bigr) M_{xy}.$$

This linear equation with constant coefficient has the stated solution, and so does the equation for $M_z - M_0$. $\square$

For a proton, $\gamma > 0$, so with $B_0$ along $+z$ the transverse magnetization turns clockwise when seen from $+z$.

**Corollary (two check values).** With $M(0) = (1, 0, 0)$ and no field, $|M_{xy}(t)| = e^{-t/T_2}$, which is $e^{-1/2}$ at $t = T_2/2$. With $M(0) = (0, 0, -M_0)$, $M_z(t) = M_0 (1 - 2 e^{-t/T_1})$, which is zero at $t = T_1 \ln 2$.

*Proof.* Put the starts into Theorem 1. For the second, $1 - 2 e^{-t/T_1} = 0$ gives $e^{-t/T_1} = 1/2$. $\square$

**Theorem 2 (rotation without relaxation).** Let $T_1 = T_2 = \infty$ and let $\omega \ne 0$ be constant, with $|\omega| = w$ and $u = \omega / w$. Then $M(t) = R_u(-w t)\, M(0)$, where $R_u(\theta)$ is the rotation by the angle $\theta$ about $u$ by the right-hand rule, given by the formula of Rodrigues

$$R_u(\theta)\, v = v \cos\theta + (u \times v) \sin\theta + u\, (u \cdot v)(1 - \cos\theta).$$

In particular $|M(t)| = |M(0)|$ for all $t$.

*Proof.* Put $N(t) = R_u(-w t) M(0)$, so $N(0) = M(0)$. Write $v = M(0)$ and $\theta = -w t$. Differentiating the formula in $\theta$ gives

$$\frac{d}{d\theta} R_u(\theta) v = -v \sin\theta + (u \times v)\cos\theta + u (u \cdot v) \sin\theta.$$

On the other side, $u \times R_u(\theta) v = (u \times v)\cos\theta + u \times (u \times v)\sin\theta$, because $u \times u = 0$. With $u \times (u \times v) = u (u \cdot v) - v$ for a unit vector $u$, the two expressions are equal. So $\frac{d}{d\theta} R_u(\theta) v = u \times R_u(\theta) v$, and by the chain rule

$$\dot N = -w\, u \times N = -\omega \times N = N \times \omega,$$

which is (1) without relaxation. By uniqueness, $M = N$. A rotation keeps the length. $\square$

**Corollary (a hard pulse).** On resonance in the rotating frame, with $B_1$ along $x$, $\omega = (\omega_1, 0, 0)$. Starting from $M(0) = (0, 0, 1)$, after the time $\tau$ with $\omega_1 \tau = \pi/2$ the magnetization is $(0, 1, 0)$: a 90 degree pulse about $x$ puts it along $+y$.

*Proof.* Theorem 2 with $u = (1, 0, 0)$, $v = (0, 0, 1)$ and $\theta = -\pi/2$: $u \cdot v = 0$, $u \times v = (0, -1, 0)$, so $R_u(\theta) v = v \cdot 0 + (0, -1, 0)(-1) = (0, 1, 0)$. $\blacksquare$

**Remarks.**

- The tests run the integrator with $h = 10^{-4}$ s for 0.05 s of free precession, and with $h = 10^{-6}$ s for the pulse, and compare with these formulas.
- Without relaxation the exact solution keeps $|M|$. The classical Runge-Kutta method does not keep it exactly, but with a small step the change is far below the test tolerance.
