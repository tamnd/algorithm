---
title: The jump conditions of the thin flame, the exactness of the planar flame, and the bounds of the step
proves: [correctness]
status: full
---

We use the line numbers of the page. $\varphi > 0$ in the fuel, $\mathbf n = \nabla \varphi / |\nabla \varphi|$ points into the fuel, and $\mathbf m = -\mathbf n$ points from the fuel to the products. For the jumps, a normal velocity $V$ is the component along $\mathbf m$. Let $J = (\rho_f / \rho_h - 1) S$ and $P = (\rho_f / \rho_h - 1) \rho_f S^2$.

**Lemma 1 (the jump conditions).** Let the front move with the normal speed $D = V_f - S$ (the fuel crosses it at the speed $S$). Then conservation of mass, $\rho_h (V_h - D) = \rho_f (V_f - D)$, and of normal momentum, $\rho_h (V_h - D)^2 + p_h = \rho_f (V_f - D)^2 + p_f$, hold exactly when

$$V_h = V_f + J, \qquad p_h = p_f - P.$$

The tangential velocity is the same on both sides.

*Proof.* $V_f - D = S$, so mass gives $V_h - D = \rho_f S / \rho_h$ and $V_h = V_f - S + \rho_f S / \rho_h = V_f + J$. Momentum gives $p_h = p_f + \rho_f S^2 - \rho_h (\rho_f S / \rho_h)^2 = p_f - (\rho_f / \rho_h - 1) \rho_f S^2$. The tangential momentum flux is the mass flux times the tangential velocity on each side, and the mass flux is the same, so the tangential velocities are equal. $\square$

Since $\rho_f > \rho_h$, $J > 0$ and $P > 0$: the products leave the front faster than the fuel arrives, and the pressure drops across the front. The test file checks both equations exactly with `Fraction` for $\rho_f = 1$, $\rho_h = 1/5$, $S = 1/2$, $V_f = 3/2$ and $p_f = 7$, which give $D = 1$, $V_h = 7/2$ and $p_h = 6$. In the same way, mass alone at the surface of a solid fuel with $D = V_s - S$ gives the gas speed $V_s + (\rho_s / \rho_f - 1) S$, the paper's equation 5.

The paper writes $\mathbf n = \nabla \varphi / |\nabla \varphi|$ in its section 4.1 and $D = V_f - S$ in section 3.2. These two agree only if $V$ is measured along $-\mathbf n$, as here. With $V$ along $\mathbf n$, the signs of $S$ and $J$ in the jump formulas change.

**Lemma 2 (ghost velocities, line L3).** The map from a fuel velocity $\mathbf u$ to its ghost product velocity is $\mathbf u \mapsto \mathbf u + J \mathbf m$, and its inverse is $\mathbf u \mapsto \mathbf u - J \mathbf m$. It keeps the tangential part and adds $J$ to the normal part, as Lemma 1 requires. On a face, the code applies the same map to the face component, with the face component $m_n$ of $\mathbf m$. A constant field of one material maps to a constant field of the other if $\mathbf m$ is constant.

*Proof.* Direct. $\square$

**Lemma 3 (the front in still fuel, lines L1 and L2).** Let $\rho_f = \rho_h$, so $J = 0$, let the fuel be at rest, and let $\varphi(x, y) = x_0 - x$. Then one substep of length $h$ gives $\varphi - S h$ at every cell, so the front moves into the fuel at the speed $S$ exactly.

*Proof.* The central differences of a linear function are exact, so $\mathbf n = (-1, 0)$ and $\mathbf w = (-S, 0)$ at every cell. The upwind difference for $w_1 < 0$ is the forward difference, which is $-1$ for this $\varphi$, also at the last cell, where the code uses the other one-sided difference. So $\varphi \leftarrow \varphi - h (-S)(-1)$. The redistancing keeps a linear function of $x$ on each row, because the distance to the nearest crossing point on the row is $|x - x_c|$. $\square$

For a curved front the upwind scheme is first order. The test file burns a disk of fuel at rest with radius 0.35 m for 0.3 s at $S = 0.5$ m/s. The front on the middle row ends at a radius of $0.2 - 0.00346$ m on a 16 by 16 grid and $0.2 - 0.00080$ m on a 32 by 32 grid.

**Theorem 1 (the projection, lines L7 and L8).** Let each connected group of FLUID cells touch an AIR cell. Then the linear system of line L7 is symmetric positive definite, so it has one solution. After line L8, every FLUID cell has zero divergence, where each face velocity is taken as the velocity of the cell's own material (Lemma 2).

*Proof.* For cell $a$ and each neighbor $b$ that is not SOLID, the code uses the face coefficient $c_{ab} = 1 / \hat\rho_{ab}$, where $\hat\rho_{ab}$ depends only on the two cells, so $c_{ab} = c_{ba} > 0$. The pressure of $b$ as seen from the material of $a$ is $p_b + \pi_{ba}$, with $\pi_{ba} = P$ if $b$ is products and $a$ fuel, $-P$ in the other mixed case, and 0 otherwise. The equation of $a$ is

$$\sum_b c_{ab} \left(p_a - p_b - \pi_{ba}\right) = -\frac{\Delta x^2}{\Delta t} \operatorname{div}^*_a,$$

with $p_b = 0$ for an AIR cell. The known terms $\pi_{ba}$ go to the right side, so the matrix is $\sum_b c_{ab}$ on the diagonal and $-c_{ab}$ for each FLUID neighbor. This is a weighted graph Laplacian plus a positive diagonal term for each AIR neighbor. Then $x^\mathsf{T} A x = \sum_{\text{FLUID pairs}} c_{ab} (x_a - x_b)^2 + \sum_{\text{AIR faces}} c_{ab} x_a^2$, which is zero only if $x$ is constant on each group and zero next to an AIR cell, so $x = 0$. Line L8 subtracts $\Delta t\, c_{ab} (p_b + \pi_{ba} - p_a) / \Delta x$ from the face velocity. The conversion of Lemma 2 adds a constant, so the face value in the material of $a$ changes by the same amount. Summed over the faces of $a$, the change of $\operatorname{div}_a$ is $(\Delta t / \Delta x^2) \sum_b c_{ab} (p_a - p_b - \pi_{ba})$, which is $-\operatorname{div}^*_a$ by the equation. $\square$

The test file checks the divergence with ghost values after every step of a nozzle flame: it stays below $10^{-8}$.

**Theorem 2 (the planar flame is kept exactly).** Take a channel with walls on its long sides, an injector that moves at $S$ into the fuel at one end, and AIR cells at the other end. Let $\varphi$ be linear across the channel with its zero between two face rows, let the fuel velocity be $S$ along the channel and the product velocity $S + J$, and let $\alpha = 0$. Then one step leaves $\varphi$ and the velocity unchanged, and the pressure is $P$ in the fuel cells and 0 in the product cells.

*Proof.* Lemma 3's argument gives $\mathbf n = -\mathbf m$ constant. The fuel field of line L3 is $S$ on every face along the channel and the product field is $S + J$ on every face (Lemma 2), and both are 0 across the channel. (L1) In every cell, $\mathbf w = S \mathbf m - S \mathbf m = 0$, so line L2 does not change $\varphi$, and the redistancing keeps it. (L4) Semi-Lagrangian advection keeps a constant field exactly, so each face gets back the value of its material. (L5, L6) The temperature does not act on the velocity when $\alpha = 0$. (L7) With ghost values, every cell has zero divergence: inside one material the face values are equal, and at the front face the conversion gives the cell's own constant. So the right side is only the jump terms. Set $p = P$ in the fuel and $p = 0$ in the products. For a fuel cell next to a product cell, $c (p_a - p_b - \pi_{ba}) = c (P - 0 - P) = 0$, and for a product cell next to a fuel cell, $c (0 - P + P) = 0$. Inside one material the differences are zero. So this $p$ solves the system, and by Theorem 1 it is the only solution. (L8) Every face has $p_b + \pi_{ba} - p_a = 0$, so no velocity changes. $\square$

The test file checks this for a front that faces $+x$, $-x$ and $+y$, with $\rho_f = 1$, $\rho_h = 0.2$ and $S = 0.5$ m/s. The products move at 2.5 m/s, the fuel pressure is $P = 1$ Pa, and the errors are below $10^{-9}$.

**Theorem 3 (the expansion in a channel).** In the channel of Theorem 2, start from any velocity along the channel that is the same across it. After one step, the fuel moves at $S$ and the products at $S + J$, wherever line L2 puts the front.

*Proof.* Line L7 gives zero divergence with ghost values in each cell (Theorem 1). With no flow across the channel, the divergence of a cell is the difference of its two face values in its material divided by $\Delta x$. So the face values are equal along each material, and the first one is the injector speed $S$. At the front face, the product cell sees the fuel value plus $J$. So the products move at $S + J$. $\square$

In the test, a uniform start of 0.5 m/s gives 0.5 m/s in the fuel and 2.5 m/s in the products after one step. The pressure then also holds the impulse that accelerates the products: it falls by 1 Pa per cell over the 8 product cells.

**Lemma 4 (the temperature, line L5).** The code replaces $T$ by the exact solution of $T' = -c_T ((T - T_{air}) / (T_{max} - T_{air}))^4$ over $\Delta t$:

$$\theta(\Delta t) = \theta_0 \left(1 + 3 c_T \Delta t\, \theta_0^3 / (T_{max} - T_{air})\right)^{-1/3}, \qquad \theta = \frac{T - T_{air}}{T_{max} - T_{air}}.$$

If every $T$ starts in $[T_{air}, T_{max}]$, it stays there.

*Proof.* With $\theta' = -k \theta^4$ and $k = c_T / (T_{max} - T_{air})$, $(\theta^{-3})' = 3k$, which integrates to the formula. The advection takes convex combinations of values in $[T_{air}, T_{max}]$, because the ghost value in the fuel is $T_{max}$. The fuel gets $T_{ign} \le T_{max}$. The cooling map is increasing in $\theta_0$, sends 0 to 0, and is at most $\theta_0$. $\square$

The test file checks two half steps against one full step and against 20000 Euler steps, and the range after a nozzle flame.
