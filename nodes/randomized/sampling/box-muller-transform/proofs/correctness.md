---
title: The Box-Muller transform gives two independent standard normal variates
proves: [correctness]
status: full
---

Write $\varphi(x) = (2\pi)^{-1/2} e^{-x^2/2}$ for the standard normal density. The input is a pair $(U_1, U_2)$ of independent uniform reals, $U_1$ on $(0, 1]$ and $U_2$ on $[0, 1)$. The output is $Z_1 = R \cos \Theta$ and $Z_2 = R \sin \Theta$ with $R = \sqrt{-2 \ln U_1}$ and $\Theta = 2\pi U_2$.

**Theorem.** $Z_1$ and $Z_2$ are independent, and each has the density $\varphi$.

*Proof.* We use the [change of variables](/change-of-variables/) formula for densities: if $U$ has density $f_U$ on an open set $D \subseteq \mathbb{R}^2$ and $T : D \to E$ is a bijection onto an open set $E$, continuously differentiable with a continuously differentiable inverse, then $Z = T(U)$ has density $f_U(T^{-1}(z)) \, |\det J_{T^{-1}}(z)|$ on $E$, where $J$ is the Jacobian matrix.

*Step 1: the sets.* Let $D = (0, 1) \times (0, 1)$. The event $(U_1, U_2) \notin D$ is $U_1 = 1$ or $U_2 = 0$, which has probability 0, so we may assume $(U_1, U_2) \in D$, with density $f_U = 1$ on $D$. Let $E = \mathbb{R}^2 \setminus \{(x, 0) : x \ge 0\}$, the plane without the closed positive $x$-axis. For $z \in E$, write $\rho = |z| > 0$ and let $\arg z \in (0, 2\pi)$ be its polar angle, which is unique and continuously differentiable on $E$.

*Step 2: the bijection.* Define $T(u_1, u_2) = (r \cos \theta, r \sin \theta)$ with $r = \sqrt{-2 \ln u_1}$ and $\theta = 2\pi u_2$. For $(u_1, u_2) \in D$, $r \in (0, \infty)$ and $\theta \in (0, 2\pi)$, so $T(u) \in E$. The inverse is

$$T^{-1}(z_1, z_2) = \Bigl( e^{-(z_1^2 + z_2^2)/2},\ \frac{\arg z}{2\pi} \Bigr),$$

because $e^{-r^2/2} = u_1$ and $\arg(r \cos\theta, r \sin\theta) = \theta$ for $r > 0$ and $\theta \in (0, 2\pi)$. Each $z \in E$ has $T^{-1}(z) \in D$, since $e^{-\rho^2/2} \in (0, 1)$ for $\rho > 0$. So $T$ is a bijection from $D$ onto $E$, and both $T$ and $T^{-1}$ are continuously differentiable.

*Step 3: the Jacobian.* Let $u_1 = e^{-\rho^2/2}$ and $u_2 = \arg z / (2\pi)$, with $\rho^2 = z_1^2 + z_2^2$. Then

$$\frac{\partial u_1}{\partial z_1} = -z_1 u_1, \quad \frac{\partial u_1}{\partial z_2} = -z_2 u_1, \quad \frac{\partial u_2}{\partial z_1} = \frac{-z_2}{2\pi \rho^2}, \quad \frac{\partial u_2}{\partial z_2} = \frac{z_1}{2\pi \rho^2},$$

where the last two use $\partial \arg z / \partial z_1 = -z_2/\rho^2$ and $\partial \arg z / \partial z_2 = z_1/\rho^2$. So

$$\det J_{T^{-1}}(z) = (-z_1 u_1) \frac{z_1}{2\pi\rho^2} - (-z_2 u_1) \frac{-z_2}{2\pi\rho^2} = -\frac{u_1 (z_1^2 + z_2^2)}{2\pi \rho^2} = -\frac{u_1}{2\pi} = -\frac{1}{2\pi} e^{-(z_1^2 + z_2^2)/2}.$$

*Step 4: the density.* By the formula, $Z = (Z_1, Z_2)$ has the density

$$f_Z(z_1, z_2) = 1 \cdot \frac{1}{2\pi} e^{-(z_1^2 + z_2^2)/2} = \varphi(z_1)\, \varphi(z_2)$$

on $E$. The set $\mathbb{R}^2 \setminus E$ is a half-line, which has area 0, so this is a density of $Z$ on all of $\mathbb{R}^2$. A joint density that is a product of a function of $z_1$ and a function of $z_2$, each of which integrates to 1, means that $Z_1$ and $Z_2$ are independent with those densities. So $Z_1$ and $Z_2$ are independent standard normal variates. $\blacksquare$

**The radius and the angle.** The proof also shows the structure behind the method. $R^2 = -2 \ln U_1$ satisfies $\Pr[R^2 > s] = \Pr[U_1 < e^{-s/2}] = e^{-s/2}$ for $s \ge 0$, so $R^2$ is exponential with mean 2 (a chi-squared variate with 2 degrees of freedom), and $\Theta$ is uniform on $[0, 2\pi)$ and independent of $R$. These are exactly the polar coordinates of a pair of independent standard normals.

**Floating point.** The theorem is about exact uniform reals and exact functions. A float $U_1$ is a multiple of $2^{-53}$ with the usual generators, so $U_1 \ge 2^{-53}$ and $R \le \sqrt{106 \ln 2} \approx 8.5717$. The output never falls in the region $|z| > 8.5717$, whose probability under the normal law is $e^{-53 \ln 2} = 2^{-53}$. The output is a discrete distribution on at most $2^{106}$ points, and the rounding of $\ln$, $\cos$ and $\sin$ moves each point by a few units in the last place.
