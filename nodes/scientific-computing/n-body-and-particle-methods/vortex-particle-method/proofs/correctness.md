---
title: The blob velocity is the exact velocity of the blob vorticity, and the particle equations conserve circulation, linear impulse and angular impulse
proves: [correctness]
status: full
---

We work in the plane with $x^\perp = (-x_2, x_1)$, the Gaussian core $\zeta_\delta(x) = e^{-|x|^2/\delta^2} / (\pi \delta^2)$ and the kernel

$$K_\delta(x) = \frac{x^\perp}{2 \pi |x|^2} \bigl(1 - e^{-|x|^2/\delta^2}\bigr), \qquad K_\delta(0) = 0.$$

Write $q(r) = (1 - e^{-r^2/\delta^2}) / (2 \pi r^2)$, so $K_\delta(x) = q(|x|)\, x^\perp$. As $r \to 0$, $q(r) \to 1 / (2 \pi \delta^2)$, so $K_\delta$ is continuous and smooth at 0.

**Claim 1 (the velocity of one blob).** $u = K_\delta$ is divergence free, and its curl is $\zeta_\delta$.

*Proof.* $K_\delta = \nabla^\perp \psi$ with $\nabla^\perp \psi = (-\partial_2 \psi, \partial_1 \psi)$ for any radial $\psi$ with $\psi'(r) = r\, q(r)$, since $\nabla \psi = \psi'(r)\, x / r$. A field of the form $\nabla^\perp \psi$ has divergence $-\partial_1 \partial_2 \psi + \partial_2 \partial_1 \psi = 0$ and curl $\partial_1 \partial_1 \psi + \partial_2 \partial_2 \psi = \Delta \psi$. For a radial function, $\Delta \psi = \frac{1}{r} (r \psi')'$, and $r \psi' = r^2 q(r) = (1 - e^{-r^2/\delta^2}) / (2\pi)$, whose derivative is $\frac{2 r}{\delta^2} e^{-r^2/\delta^2} / (2 \pi)$. Dividing by $r$ gives $e^{-r^2/\delta^2} / (\pi \delta^2) = \zeta_\delta$. $\square$

By linearity, $u(x) = \sum_q \Gamma_q K_\delta(x - x_q)$ is divergence free with curl $\omega_h = \sum_q \Gamma_q \zeta_\delta(\cdot - x_q)$. It also tends to 0 at infinity, like $1/|x|$, so it is the velocity that the Biot-Savart law gives for $\omega_h$.

**Claim 2 (the Lamb-Oseen check).** If $\omega$ is the Lamb-Oseen vorticity $\Gamma \zeta_a$ with $a^2 = 4 \nu t$, then $\omega * \zeta_\delta = \Gamma \zeta_b$ with $b^2 = a^2 + \delta^2$, whose velocity is the Lamb-Oseen velocity at time $t + \delta^2 / (4 \nu)$.

*Proof.* $\zeta_a$ is the density of a 2D normal law with variance $a^2 / 2$ in each coordinate. The convolution of two such densities is the density of the sum of independent variables, which is normal with variance $(a^2 + \delta^2)/2$, that is $\zeta_b$. By Claim 1 with $\delta$ replaced by $b$, its velocity is $\Gamma K_b$, with azimuthal component $\Gamma (1 - e^{-r^2/b^2}) / (2 \pi r)$, and $b^2 = 4 \nu (t + \delta^2/(4\nu))$. $\square$

So the lattice sum on the page approximates $\Gamma K_b$ with no smoothing error, and only the quadrature and truncation errors remain; the test checks this to $10^{-4}$.

**Claim 3 (invariants).** Let $x_p(t)$ solve $\dot x_p = \sum_{q} \Gamma_q K_\delta(x_p - x_q)$ with constant $\Gamma_p$. Then the circulation $\sum_p \Gamma_p$, the linear impulse $I = \sum_p \Gamma_p x_p$ and the angular impulse $A = \sum_p \Gamma_p |x_p|^2$ are constant.

*Proof.* The circulations do not change, so neither does their sum. Write $K_{pq} = K_\delta(x_p - x_q)$. The kernel is odd, $K_{qp} = -K_{pq}$, so
$$\dot I = \sum_p \sum_q \Gamma_p \Gamma_q K_{pq} = 0,$$
because the terms $(p, q)$ and $(q, p)$ cancel and the terms with $p = q$ are 0. For $A$,
$$\dot A = 2 \sum_{p, q} \Gamma_p \Gamma_q\, x_p \cdot K_{pq}.$$
Swapping the names $p$ and $q$ and using $K_{qp} = -K_{pq}$ shows that the same sum equals $-2 \sum_{p, q} \Gamma_p \Gamma_q\, x_q \cdot K_{pq}$. Adding the two forms, $\dot A = \sum_{p, q} \Gamma_p \Gamma_q (x_p - x_q) \cdot K_{pq} = 0$, since $K_\delta(x)$ is a multiple of $x^\perp$ and $x \cdot x^\perp = 0$. $\square$

**Claim 4 (the midpoint rule keeps the linear impulse).** One step of lines L1 to L5 leaves $I$ unchanged in exact arithmetic.

*Proof.* Line L3 changes $I$ by $\frac{h}{2} \sum_p \Gamma_p u_p = \frac{h}{2} \dot I = 0$ for the old positions, and line L5 changes it by $h \sum_p \Gamma_p u_p^*$, which is the same antisymmetric double sum at the midpoint positions, and so is 0 as in Claim 3. $\blacksquare$

The midpoint rule does not keep $A$ exactly, since the second form of $\dot A$ uses the positions at which the velocity was computed; its error per step is the local error $O(h^3)$ of the method.
