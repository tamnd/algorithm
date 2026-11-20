---
title: The Yee scheme is consistent of second order, keeps the discrete divergence and a discrete energy, and is stable up to the CFL limit
proves: [correctness, termination]
status: full
---

**Setting.** The $\text{TM}_z$ scheme of the main page with constant $\varepsilon$ and $\mu$, $c = 1/\sqrt{\varepsilon\mu}$, on a rectangle with $E_z = 0$ on the walls. Write $\delta_x$ for the centred difference over one cell, $(\delta_xq)_{i} = (q_{i+1/2} - q_{i-1/2})/\Delta x$, and similarly $\delta_y$ and $\delta_t$. The scheme is

$$\mu\,\delta_tH_x = -\delta_yE_z,\qquad \mu\,\delta_tH_y = \delta_xE_z,\qquad \varepsilon\,\delta_tE_z = \delta_xH_y - \delta_yH_x,$$

where each equation is taken at the point where the updated value lives: L1 and L2 at $t_n$ and L3 at $t_{n+1/2}$.

**Lemma 1 (consistency).** For smooth solutions the local truncation error is $O(\Delta t^2 + \Delta x^2 + \Delta y^2)$.

*Proof.* Each operator is a centred difference at the point where the equation is taken. For a smooth function, $(q(s + h/2) - q(s - h/2))/h = q'(s) + \frac{h^2}{24}q'''(s) + O(h^4)$ by Taylor expansion about $s$. Inserting the exact solution into each of the three equations therefore leaves residuals of order $\Delta t^2$, $\Delta x^2$ and $\Delta y^2$. $\square$

**Lemma 2 (divergence).** Let $D_{i+1/2,j+1/2} = \delta_xH_x + \delta_yH_y$ at the cell centres. L1 and L2 do not change $D$.

*Proof.* By L1 and L2, $\mu\,\delta_tD = -\delta_x\delta_yE_z + \delta_y\delta_xE_z$. The operators $\delta_x$ and $\delta_y$ act on different indices, so they commute, and the difference is zero. Written out at one cell centre, each of the four values of $E_z$ at the corners appears twice, with opposite signs. $\square$

In three dimensions the same argument applies to each of the two curl updates, so the discrete divergences of $\mu H$ at the cell centres and of $\varepsilon E$ at the nodes stay constant when there are no currents.

**Notation for the energy.** Let $\langle\cdot,\cdot\rangle$ be the sum over the grid points of each field, times $\Delta x\Delta y$, and $\|\cdot\|$ its norm. Define $KE = (\delta_yE_z, -\delta_xE_z)$, a field at the positions of $(H_x, H_y)$, and $K^*H = \delta_xH_y - \delta_yH_x$ at the interior nodes. Then L1 and L2 read $H^{n+1/2} = H^{n-1/2} - \frac{\Delta t}{\mu}KE^n$, and L3 with L4 reads $E^{n+1} = E^n + \frac{\Delta t}{\varepsilon}K^*H^{n+1/2}$, with $E_z = 0$ on the walls.

**Lemma 3 (adjoint).** If $E_z = 0$ on the walls, $\langle KE, H\rangle = \langle E, K^*H\rangle$.

*Proof.* In one column, $\sum_j(\delta_yE_z)_{j+1/2}H_{x,j+1/2} = -\sum_jE_{z,j}(\delta_yH_x)_j$ plus terms with $E_z$ at the two walls, which are zero. This is summation by parts. The same holds in each row for $\delta_x$. So $\langle KE, H\rangle = -\langle E, \delta_yH_x\rangle + \langle E, \delta_xH_y\rangle = \langle E, K^*H\rangle$. $\square$

**Lemma 4 (energy).** $W^n = \varepsilon\|E^n\|^2 + \mu\langle H^{n-1/2}, H^{n+1/2}\rangle$ is the same for all $n$.

*Proof.* By the $E$ update,

$$\varepsilon\|E^{n+1}\|^2 - \varepsilon\|E^n\|^2 = \varepsilon\langle E^{n+1} - E^n, E^{n+1} + E^n\rangle = \Delta t\,\langle K^*H^{n+1/2}, E^{n+1} + E^n\rangle.$$

By the $H$ update at the steps $n$ and $n + 1$, $H^{n+3/2} - H^{n-1/2} = -\frac{\Delta t}{\mu}K(E^{n+1} + E^n)$, so by Lemma 3

$$\mu\langle H^{n+1/2}, H^{n+3/2}\rangle - \mu\langle H^{n-1/2}, H^{n+1/2}\rangle = -\Delta t\,\langle H^{n+1/2}, K(E^{n+1} + E^n)\rangle = -\Delta t\,\langle K^*H^{n+1/2}, E^{n+1} + E^n\rangle.$$

The two changes cancel, so $W^{n+1} = W^n$. $\square$

**Theorem 1 (stability).** Let $\sigma = c\Delta t\sqrt{1/\Delta x^2 + 1/\Delta y^2}$. If $\sigma \le 1$, the fields stay bounded for all $n$, by a constant that depends on the grid but not on $n$. If $\sigma > 1$, then on fine enough grids there are initial fields that grow geometrically.

*Proof.* $K^*K = -(\delta_x^2 + \delta_y^2)$ is the five-point Laplacian with Dirichlet walls, with the eigenvectors $\sin(k_xx)\sin(k_yy)$, $k_x = m\pi/a$, $k_y = n\pi/b$, $1 \le m < N_x$, $1 \le n < N_y$, and the eigenvalues

$$\Lambda_{mn} = \frac{4}{\Delta x^2}\sin^2\frac{k_x\Delta x}{2} + \frac{4}{\Delta y^2}\sin^2\frac{k_y\Delta y}{2} < 4\Big(\frac1{\Delta x^2} + \frac1{\Delta y^2}\Big).$$

So $\|K\|^2 = \max\Lambda_{mn} < 4\sigma^2/(c\Delta t)^2$.

Bounded case. Write $W^n = \varepsilon\|E^n\|^2 + \mu\|H^{n-1/2}\|^2 - \Delta t\langle H^{n-1/2}, KE^n\rangle$. By the Cauchy-Schwarz inequality the last term is at most $\Delta t\|K\|\,\|H^{n-1/2}\|\,\|E^n\|$. The quadratic form $\varepsilon e^2 + \mu h^2 - \Delta t\|K\|eh$ is positive definite when $\Delta t^2\|K\|^2 < 4\varepsilon\mu$, that is $c^2\Delta t^2\|K\|^2 < 4$, which holds because $c^2\Delta t^2\|K\|^2 < 4\sigma^2 \le 4$. Then $W^n \ge \gamma(\|E^n\|^2 + \|H^{n-1/2}\|^2)$ with some $\gamma > 0$, and since $W^n = W^0$ by Lemma 4, the fields are bounded.

Unbounded case. Eliminating $H$ gives $E^{n+1} - 2E^n + E^{n-1} = -c^2\Delta t^2K^*KE^n$. For one eigenvector the factor $g$ per step satisfies $g + 1/g = 2 - c^2\Delta t^2\Lambda_{mn}$. If $c^2\Delta t^2\Lambda_{mn} > 4$, the right side is below $-2$, so one root is real with $|g| > 1$ and the mode grows geometrically. For $m = N_x - 1$ and $n = N_y - 1$, $c^2\Delta t^2\Lambda_{mn} \to 4\sigma^2 > 4$ as the grid is refined at fixed ratios $c\Delta t/\Delta x$ and $c\Delta t/\Delta y$. $\square$

**Dispersion.** For $c^2\Delta t^2\Lambda_{mn} < 4$ the two roots are $g = e^{\pm i\omega_h\Delta t}$ with $\sin(\omega_h\Delta t/2) = \tfrac12c\Delta t\sqrt{\Lambda_{mn}}$, which is the dispersion relation on the main page.

**Corollary (exact discrete mode).** With $\omega_h$ from the dispersion relation, $E_z = \cos(\omega_ht_n)\sin(k_xx_i)\sin(k_yy_j)$, $H_x = A_x\sin(\omega_ht_{n+1/2})\sin(k_xx_i)\cos(k_yy_{j+1/2})$ and $H_y = A_y\sin(\omega_ht_{n+1/2})\cos(k_xx_{i+1/2})\sin(k_yy_j)$, with $A_x = -\frac{\Delta t\sin(k_y\Delta y/2)}{\mu\Delta y\sin(\omega_h\Delta t/2)}$ and $A_y = \frac{\Delta t\sin(k_x\Delta x/2)}{\mu\Delta x\sin(\omega_h\Delta t/2)}$, solve the scheme exactly. Inserting them into L1 and L2 uses $\sin(s + h) - \sin(s - h) = 2\cos s\sin h$ and fixes $A_x$ and $A_y$. Inserting them into L3 uses $\cos(s + h) - \cos(s - h) = -2\sin s\sin h$ and gives the dispersion relation.

**Termination.** One step is three loops over at most $(N_x + 1)(N_y + 1)$ points each, so $N$ steps end after $\Theta(NN_xN_y)$ operations.

$\blacksquare$
