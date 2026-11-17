---
title: The Gerstner wave is an exact rotational solution, and a sum with small steepness has no loops
proves: [correctness]
status: full
---

We use the notation of the page.
For one wave, write $E = Ae^{kb}$, $s = kE$ and $\theta = ka - \omega t + \varphi$, so that $x = a - E\sin\theta$ and $z = b + E\cos\theta$.
The derivatives with respect to the labels are

$$x_a = 1 - s\cos\theta, \quad x_b = -s\sin\theta, \quad z_a = -s\sin\theta, \quad z_b = 1 + s\cos\theta,$$

because $\partial E/\partial b = kE$.
The velocity is $u = \dot x = E\omega\cos\theta$ and $w = \dot z = E\omega\sin\theta$, and the acceleration is $\ddot x = E\omega^2\sin\theta$ and $\ddot z = -E\omega^2\cos\theta$.

## Area and orbits

**Claim 1.** The Jacobian is $J = x_a z_b - x_b z_a = 1 - s^2$. It does not depend on $t$, so the flow keeps the area of every part of the water. For $kA < 1$ the map from the labels $b \le 0$ to the positions is one to one at every time.

*Proof.*
$J = (1 - s\cos\theta)(1 + s\cos\theta) - s^2\sin^2\theta = 1 - s^2$.
Area preservation is the statement that $J$ is constant in time.
For one to one, note that $(x, z) = \nabla\Psi$ for $\Psi(a, b) = \frac12(a^2 + b^2) + (A/k)e^{kb}\cos\theta$.
Its Hessian is the symmetric matrix with the entries $x_a$, $x_b = z_a$ and $z_b$, with trace 2 and determinant $1 - s^2$, so its eigenvalues are $1 \pm s \ge 1 - kA > 0$ on $b \le 0$.
The half plane $b \le 0$ is convex, so for two labels $P \ne P'$ in it, $(\nabla\Psi(P) - \nabla\Psi(P'))\cdot(P - P') = \int_0^1 (P - P')^{\mathsf T}\nabla^2\Psi(P' + r(P - P'))(P - P')\, dr \ge (1 - kA)|P - P'|^2 > 0$, and the two positions differ. $\square$

**Claim 2.** Each particle moves on the circle of radius $E = Ae^{kb}$ about $(a, b)$, once per period $2\pi/\omega$.

*Proof.*
$(x - a)^2 + (z - b)^2 = E^2(\sin^2\theta + \cos^2\theta) = E^2$, and $\theta$ changes by $2\pi$ in the time $2\pi/\omega$. $\square$

## The exact solution

**Claim 3.** If $\omega^2 = gk$ and $s < 1$, the motion satisfies the Euler equations of an incompressible ideal fluid under gravity, with the pressure

$$\frac{p}{\rho} = \frac{p_0}{\rho} - g b + \frac{g k A^2}{2} e^{2kb},$$

which is constant on the surface $b = 0$. If $\omega^2 \ne gk$, no pressure that is constant on the surface fits the motion.

*Proof.*
The Euler equations are $\ddot x = -p_x/\rho$ and $\ddot z = -p_z/\rho - g$, and incompressibility holds by Claim 1.
By the chain rule $p_a = p_x x_a + p_z z_a$ and $p_b = p_x x_b + p_z z_b$, so in the labels the equations are

$$-\frac{p_a}{\rho} = \ddot x\, x_a + (\ddot z + g) z_a, \qquad -\frac{p_b}{\rho} = \ddot x\, x_b + (\ddot z + g) z_b.$$

The first right side is $E\omega^2\sin\theta(1 - s\cos\theta) + (g - E\omega^2\cos\theta)(-s\sin\theta) = E\sin\theta\,(\omega^2 - gk)$, since the terms $\pm sE\omega^2\sin\theta\cos\theta$ cancel and $s = kE$.
The second right side is $-sE\omega^2\sin^2\theta + (g - E\omega^2\cos\theta)(1 + s\cos\theta) = g - sE\omega^2 + E\cos\theta\,(gk - \omega^2)$.
With $\omega^2 = gk$, the first is 0 and the second is $g - gk^2A^2e^{2kb}$, and these are $-\partial/\partial a$ and $-\partial/\partial b$ of the pressure above divided by $\rho$.
With $\omega^2 \ne gk$, the first right side is not 0 at $b = 0$ for $\sin\theta \ne 0$, so $p_a \ne 0$ along the surface and the pressure there is not constant. $\square$

## Vorticity

**Claim 4.** The vorticity is $\partial w/\partial x - \partial u/\partial z = 2\omega s^2/(1 - s^2)$, which is positive, while the particles turn clockwise.

*Proof.*
Inverting the label map gives $\partial a/\partial x = z_b/J$, $\partial b/\partial x = -z_a/J$, $\partial a/\partial z = -x_b/J$ and $\partial b/\partial z = x_a/J$.
With $w_a = s\omega\cos\theta$, $w_b = s\omega\sin\theta$, $u_a = -s\omega\sin\theta$ and $u_b = s\omega\cos\theta$:
$J\,\partial w/\partial x = w_a z_b - w_b z_a = s\omega\cos\theta + s^2\omega$ and $J\,\partial u/\partial z = u_b x_a - u_a x_b = s\omega\cos\theta - s^2\omega$.
The difference is $2s^2\omega/J$.
The position on the circle is $E(-\sin\theta, \cos\theta)$, at the angle $\theta + \pi/2$, which decreases in time, so the particles turn clockwise. $\square$

## Shape of the surface

Take $b = 0$, $t = 0$ and $\varphi = 0$, so $\theta = ka$, $s = kA$, and the surface is $x(a) = a - A\sin ka$, $z(a) = A\cos ka$. Other times and phases only shift it.

**Claim 5.** The crest is at $z = A$ and the trough at $z = -A$. The surface is stretched by $x_a = 1 - kA$ at the crest and $1 + kA$ at the trough. For $kA \le 1$ the mean height over $x$ is $-kA^2/2$. At $kA = 1$ the crest is a cusp, and for $kA > 1$ the surface crosses itself.

*Proof.*
The values of $z$ and $x_a$ at $\theta = 0$ and $\theta = \pi$ are direct.
For $kA \le 1$, $x$ is nondecreasing and $x(a + \lambda) = x(a) + \lambda$, so the mean over one wavelength is $\frac1\lambda\int_0^\lambda z\, x_a\, da = \frac1\lambda\int_0^\lambda (A\cos ka - kA^2\cos^2 ka)\, da = -kA^2/2$.
At $kA = 1$, both $x_a$ and $z_a = -kA\sin ka$ are 0 at $a = 0$, and near it $x - x(0) \approx k^2 a^3/6$ while $z - A \approx -Ak^2a^2/2$, so $|x - x(0)|$ grows like $|z - A|^{3/2}$: a cusp.
For $kA > 1$, $f(\theta) = k(x - x(0)) = \theta - kA\sin\theta$ is negative for small $\theta > 0$ and equals $\pi$ at $\theta = \pi$, so $f(\theta_0) = 0$ for some $\theta_0 \in (0, \pi)$.
Since $f$ is odd and $z$ is even in $\theta$, the points $\theta_0$ and $-\theta_0$ have the same $x$ and the same $z$, and they are different points of the curve. $\square$

**Claim 6.** At the crest the surface particle moves forward at $A\omega$, and this equals the phase speed $\omega/k$ exactly when $kA = 1$.

*Proof.*
At $\theta = 0$, $u = A\omega$ and $w = 0$. $A\omega = \omega/k$ if and only if $kA = 1$. $\square$

## A sum of waves

**Claim 7.** Let $\mu = 1 - Q\sum_i k_iA_i > 0$. Then at every time the horizontal map $p \mapsto x(p) = p - Q\sum_i \hat d_iA_i\sin\theta_i$ satisfies $(x(p) - x(q))\cdot(p - q) \ge \mu|p - q|^2$, so it is one to one, and its Jacobian matrix is symmetric with eigenvalues at least $\mu$.

*Proof.*
$x = \nabla\Phi$ for $\Phi(p) = \frac12|p|^2 + Q\sum_i (A_i/k_i)\cos\theta_i$, because $\nabla\cos\theta_i = -k_i\hat d_i\sin\theta_i$.
The Hessian is $I - Q\sum_i k_iA_i\cos\theta_i\, \hat d_i\hat d_i^{\mathsf T}$, which is the Jacobian matrix of $x$ and is symmetric.
For a unit vector $v$, $v^{\mathsf T}\hat d_i\hat d_i^{\mathsf T}v \in [0, 1]$, so $v^{\mathsf T}(\nabla^2\Phi)v \ge 1 - Q\sum_i k_iA_i = \mu$.
Then $(x(p) - x(q))\cdot(p - q) = \int_0^1 (p - q)^{\mathsf T}\nabla^2\Phi(q + r(p - q))(p - q)\, dr \ge \mu|p - q|^2$, which is positive for $p \ne q$, so $x(p) \ne x(q)$. $\blacksquare$

The test checks Claims 1 to 7 with the code, by finite differences for Claims 1, 3 and 4 and on random sums of waves for Claim 7.
