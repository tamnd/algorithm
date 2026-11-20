---
title: The MUSCL-Hancock scheme is conservative and consistent, and for linear advection with a TVD limiter it is TVD for Courant numbers up to 1
proves: [correctness]
status: full
---

**Setting.** The scheme stores cell averages $U_j^n$ on a uniform grid with width $\Delta x$, with $\lambda = \Delta t/\Delta x$. Lines L2 to L6 of the page compute, in each cell, a slope $\delta_j = \mathrm{lim}(U_j - U_{j-1}, U_{j+1} - U_j)$ (componentwise for systems), the boundary values $U_j^\pm = U_j \pm \frac12\delta_j$, the half step values

$$\bar U_j^\pm = U_j^\pm - \tfrac{\lambda}{2}\big(F(U_j^+) - F(U_j^-)\big),$$

the face flux $F_{j+1/2} = \mathcal R(\bar U_j^+, \bar U_{j+1}^-)$ from a two-point Riemann flux $\mathcal R$, and the update $U_j^{n+1} = U_j^n - \lambda(F_{j+1/2} - F_{j-1/2})$.

Each limiter is odd and positively homogeneous: $\mathrm{lim}(sa, sb) = s\,\mathrm{lim}(a, b)$ for every real $s$. It is $0$ when $ab \le 0$. For $a \ne 0$ write $\mathrm{lim}(a, b) = a\,\varphi(b/a)$. The three limiters of the page give

$$\varphi_{\mathrm{minmod}}(r) = \max(0, \min(1, r)), \quad \varphi_{\mathrm{vL}}(r) = \frac{r + |r|}{1 + |r|}, \quad \varphi_{\mathrm{MC}}(r) = \max\big(0, \min(2r, \tfrac{1+r}{2}, 2)\big).$$

All three satisfy

$$0 \le \varphi(r) \le \min(2, 2r) \text{ for } r > 0, \qquad \varphi(r) = 0 \text{ for } r \le 0. \tag{S}$$

This is the TVD region of Sweby (1984). The test `test_limiters` checks (S) at sample points.

**Lemma 1 (conservation and consistency).** On a periodic grid, $\sum_j U_j^{n+1} = \sum_j U_j^n$. If $U_{j-2} = \dots = U_{j+2} = U$ and $\mathcal R(U, U) = F(U)$, then $F_{j\pm1/2} = F(U)$ and $U_j^{n+1} = U$.

*Proof.* The face flux $F_{j+1/2}$ enters cell $j$ with the factor $-\lambda$ and cell $j+1$ with $+\lambda$, so the sum telescopes to zero. The test checks this exactly in `Fraction` arithmetic for Burgers' equation with all three limiters. For a constant state all differences are zero, so $\delta = 0$, $U^\pm = U$, the flux difference in the half step is zero, $\bar U^\pm = U$, and both face fluxes are $\mathcal R(U, U) = F(U)$. $\square$

So the scheme is conservative, and the [Lax-Wendroff theorem](/lax-wendroff-theorem/) applies: if the numerical solutions converge boundedly in $L^1_{loc}$ as $\Delta x, \Delta t \to 0$, the limit is a weak solution.

**Lemma 2 (the flux for linear advection).** Let $F(u) = au$ with $a > 0$, $\mathcal R$ the upwind flux $\mathcal R(u_L, u_R) = a u_L$, and $\nu = a\lambda$. Then

$$F_{j+1/2} = a\Big(u_j + \frac{1 - \nu}{2}\delta_j\Big).$$

*Proof.* $F(u_j^+) - F(u_j^-) = a\delta_j$, so $\bar u_j^+ = u_j + \frac12\delta_j - \frac{\nu}{2}\delta_j$. The upwind flux takes the left value. $\square$

With $\delta_j = 0$ this is the first order [upwind scheme](/upwind-scheme/). With the unlimited slope $\delta_j = \frac12(u_{j+1} - u_{j-1})$ it is Fromm's scheme, which is second order for smooth solutions (LeVeque 2002, Chapter 6). The limiter switches between these flux forms by the local ratio of differences, which is the flux limiter form of [flux limiter methods](/flux-limiter-methods/).

**Lemma 3 (Harten 1983).** Suppose $u_j^{n+1} = u_j - C_{j-1/2}(u_j - u_{j-1})$ on a periodic grid with $0 \le C_{j-1/2} \le 1$ for all $j$. Then $TV(u^{n+1}) \le TV(u^n)$, where $TV(u) = \sum_j |u_{j+1} - u_j|$.

*Proof.* Write $\Delta_{j-1/2} = u_j - u_{j-1}$. Then

$$u_{j+1}^{n+1} - u_j^{n+1} = (1 - C_{j+1/2})\Delta_{j+1/2} + C_{j-1/2}\Delta_{j-1/2}.$$

Both coefficients are in $[0, 1]$. Take absolute values, sum over $j$ and shift the index of the second sum:

$$TV(u^{n+1}) \le \sum_j (1 - C_{j+1/2})|\Delta_{j+1/2}| + \sum_j C_{j+1/2}|\Delta_{j+1/2}| = TV(u^n). \quad\square$$

**Theorem 1 (TVD for linear advection).** For $F(u) = au$ with $a > 0$, the upwind flux, any limiter that satisfies (S), and $0 \le \nu \le 1$, the scheme is TVD and creates no new extrema: $\min_k u_k^n \le u_j^{n+1} \le \max_k u_k^n$.

*Proof.* By Lemma 2,

$$u_j^{n+1} = u_j - \nu\Big(\Delta_{j-1/2} + \frac{1 - \nu}{2}(\delta_j - \delta_{j-1})\Big).$$

If $\Delta_{j-1/2} \ne 0$, write $\delta_j = \varphi(r_j)\Delta_{j-1/2}$ with $r_j = \Delta_{j+1/2}/\Delta_{j-1/2}$, because $\delta_j = \mathrm{lim}(\Delta_{j-1/2}, \Delta_{j+1/2})$. Also $\delta_{j-1} = \mathrm{lim}(\Delta_{j-3/2}, \Delta_{j-1/2}) = \psi_j\Delta_{j-1/2}$ with $\psi_j = \varphi(r_{j-1})/r_{j-1}$ when $r_{j-1} > 0$, and $\psi_j = 0$ when $\delta_{j-1} = 0$. By (S), $0 \le \varphi(r_j) \le 2$ and $0 \le \psi_j \le 2$. So

$$u_j^{n+1} = u_j - C_{j-1/2}\Delta_{j-1/2}, \qquad C_{j-1/2} = \nu\Big(1 + \frac{1 - \nu}{2}\big(\varphi(r_j) - \psi_j\big)\Big).$$

The bracket lies in $[1 - (1 - \nu), 1 + (1 - \nu)] = [\nu, 2 - \nu]$, so $\nu^2 \le C_{j-1/2} \le \nu(2 - \nu) \le 1$. If $\Delta_{j-1/2} = 0$, then $\delta_{j-1} = 0$ and $\delta_j = 0$ by the definition of the limiter, so $u_j^{n+1} = u_j$ and any $C_{j-1/2} \in [0, 1]$ works. Lemma 3 gives TVD. For the extrema, $u_j^{n+1} = (1 - C_{j-1/2})u_j + C_{j-1/2}u_{j-1}$ is a convex combination of two old values. $\square$

For $a < 0$ the same proof works with the mirror image. The test `test_tvd_and_no_new_extrema_for_advection` checks Theorem 1 for the three limiters at $\nu = 0.3$, $0.9$ and $1$.

**Theorem 2 (a stationary contact is kept).** For the Euler equations with a Riemann flux $\mathcal R$ that keeps an isolated stationary contact exactly (HLLC does, by the result on the HLLC page), let the data be $(\rho_L, 0, p)$ for $j < k$ and $(\rho_R, 0, p)$ for $j \ge k$. Then $U^{n+1} = U^n$.

*Proof.* Every component of $U$ is piecewise constant with one jump, between cells $k - 1$ and $k$. In each cell at least one of the two one-sided differences is zero, so every slope is zero. Then $\bar U_j^\pm = U_j$ and the face fluxes are $\mathcal R(U_j, U_{j+1})$. The faces away from $k - 1/2$ see equal states and give $F(U_j) = (0, p, 0)$. At the contact face the flux of a contact preserving solver is also $(0, p, 0)$. So every flux difference is zero. $\square$

**What is not proved here.** For Burgers' equation and for the Euler equations, the page does not prove TVD or positivity. The test checks the TVD property for Burgers' equation on one step problem, which is a measurement. Second order accuracy away from extrema is a classical result for the unlimited scheme (Fromm's scheme for linear advection); with a limiter, the order at smooth extrema drops, because (S) sets the slope to zero in a cell where the two differences have opposite signs. The test measures it: about 2 in $L^1$ and between 1.1 and 1.6 in the max norm on a sine wave.
