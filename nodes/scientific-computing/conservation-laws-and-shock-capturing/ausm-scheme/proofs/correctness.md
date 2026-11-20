---
title: The AUSM splits add up to the Mach number and the pressure, the AUSM flux is consistent and upwind for supersonic flow, it keeps contacts at rest exactly, and on a shock tube its first step needs a Courant number bound for positive pressure
proves: [correctness]
status: full
---

**Setting.** The scheme stores cell averages $U_j^n$ of the Euler equations with $U = (\rho, \rho u, E)$, $p = (\gamma - 1)(E - \frac12\rho u^2)$, $c = \sqrt{\gamma p/\rho}$, $H = (E + p)/\rho$ and $M = u/c$. It steps $U_j^{n+1} = U_j^n - \lambda(F_{j+1/2} - F_{j-1/2})$ with $\lambda = \Delta t/\Delta x$ (line L8). The face flux of lines L1 to L6 is

$$F_{1/2} = M_{1/2}\,\Phi_{L/R} + (0, p_{1/2}, 0), \qquad M_{1/2} = M_L^+ + M_R^-, \qquad p_{1/2} = p_L^+ + p_R^-,$$

where $\Phi = c(\rho, \rho u, \rho H)$ is taken from the left state if $M_{1/2} \ge 0$ and from the right state otherwise. For $|M| \le 1$ the splits are $M^\pm = \pm\frac14(M \pm 1)^2$ and $p^\pm = \frac p4(M \pm 1)^2(2 \mp M)$. For $|M| > 1$ they are $M^\pm = \frac12(M \pm |M|)$, and $p^+ = p$, $p^- = 0$ if $M > 1$, and $p^+ = 0$, $p^- = p$ if $M < -1$.

**Lemma 1 (the splits).** For all $M$: $M^+ + M^- = M$ and $p^+ + p^- = p$. Also $M^+ \ge 0 \ge M^-$, $p^\pm \ge 0$, $M^+$, $M^-$ and $p^+$ do not decrease in $M$, and $p^-$ does not increase. All four splits are continuous with continuous first derivatives, also at $M = \pm 1$.

*Proof.* For $|M| > 1$ the claims are direct. For $|M| \le 1$: $(M + 1)^2 - (M - 1)^2 = 4M$, so $M^+ + M^- = M$. Next, $(M + 1)^2(2 - M) = -M^3 + 3M + 2$ and $(M - 1)^2(2 + M) = M^3 - 3M + 2$, and the sum is 4, so $p^+ + p^- = p$. Since $2 \mp M \ge 1$, both $p^\pm \ge 0$. The derivatives are $\frac{d}{dM}M^\pm = \frac12(M \pm 1)$, which is $\ge 0$ on $[-1, 1]$, and $\frac{d}{dM}p^\pm = \pm\frac{3p}4(1 - M^2)$. At $M = 1$: $M^+ = 1$ with slope 1, $M^- = 0$ with slope 0, $p^+ = p$ and $p^- = 0$ with slope 0. These match the supersonic branch $M^+ = M$, $M^- = 0$, $p^+ = p$, $p^- = 0$. The point $M = -1$ is the mirror image. $\square$

The tests check the sums, the signs and the monotonicity exactly in `Fraction` arithmetic on a grid of 81 Mach numbers in $[-2.5, 2.5]$, and the matching slopes at $M = \pm 1$ by one-sided difference quotients.

**Lemma 2 (consistency).** $F_{1/2}(U, U) = F(U)$.

*Proof.* By Lemma 1, $M_{1/2} = M$ and $p_{1/2} = p$. Then $F_{1/2} = \frac uc\,c(\rho, \rho u, \rho H) + (0, p, 0) = (\rho u, \rho u^2 + p, u(E + p)) = F(U)$. $\square$

**Lemma 3 (supersonic flow).** If $M_L \ge 1$ and $M_R \ge 1$, then $F_{1/2} = F(U_L)$. If $M_L \le -1$ and $M_R \le -1$, then $F_{1/2} = F(U_R)$.

*Proof.* In the first case $M_L^+ = M_L$, $M_R^- = 0$, $p_L^+ = p_L$ and $p_R^- = 0$ (at $M = 1$ the subsonic formulas give the same values by Lemma 1). So $M_{1/2} = M_L > 0$, $\Phi$ comes from the left, and $F_{1/2} = M_L\Phi_L + (0, p_L, 0) = F(U_L)$ as in Lemma 2. The second case is the mirror image. $\square$

**Lemma 4 (states at rest).** If $u_L = u_R = 0$, then $F_{1/2} = (0, \frac12(p_L + p_R), 0)$, for any densities.

*Proof.* $M_L = M_R = 0$, so $M_{1/2} = \frac14 - \frac14 = 0$ and $p_{1/2} = \frac12 p_L + \frac12 p_R$. $\square$

**Proposition 5 (contacts at rest are kept).** If all cells have $u = 0$ and the same pressure $p$, then every face flux is $(0, p, 0)$ and one step leaves every cell unchanged. In floating point arithmetic this holds exactly: $M = 0$, $\frac14(0 + 1)^2 = 0.25$, and $\frac p4 \cdot 1 \cdot 2 + \frac p4 \cdot 1 \cdot 2 = p$ are computed without rounding.

*Proof.* Lemma 4 with $p_L = p_R = p$. All flux differences are zero. $\square$

The test runs a density jump from 1 to 0.125 at rest with $p = 1$ for 67 steps and finds every cell equal to its start value. A moving contact is not kept: with $u = 1$ on both sides, $M_L \ne M_R$ because the sound speeds differ, and the test finds $u$ and $p$ off by about 0.03 after the contact has moved 0.2.

**Proposition 6 (the first step of a shock tube).** Let the data be two states at rest, $(\rho_L, 0, p_L)$ left of a face and $(\rho_R, 0, p_R)$ right of it, with $p_L > p_R$. After one step the cell right of the face has the pressure

$$p_R - \frac{(\gamma - 1)\lambda^2(p_L - p_R)^2}{8\rho_R},$$

which is positive if and only if $\lambda < \lambda^* = \frac{2}{p_L - p_R}\sqrt{\frac{2\rho_R p_R}{\gamma - 1}}$. The cell left of the face has the same formula with $\rho_L$ and $p_L$.

*Proof.* By Lemma 4 the cell right of the face has the flux $(0, \frac12(p_L + p_R), 0)$ on its left face and $(0, p_R, 0)$ on its right face. So its density and energy do not change, and its momentum becomes $\lambda\frac12(p_L - p_R)$. The new pressure is $(\gamma - 1)\big(E_R - \frac{(\rho u)^2}{2\rho_R}\big)$ with $E_R = p_R/(\gamma - 1)$, which is the formula. For the left cell the argument is the same. $\square$

For Sod's data, $\lambda^* = \frac{2}{0.9}\sqrt{0.0625} = 0.5556$, and with the largest speed $c_L = \sqrt{1.4}$ at the start, the largest safe Courant number is $\lambda^* c_L = 0.6574$. The code fails with a negative pressure on Sod's tube for Courant numbers 0.7 to 0.9 and runs at 0.5 and 0.6. For the data $(1, 0, 1000)$ and $(1, 0, 0.01)$ the bound is $0.0167$. The test checks the formula and the sign change at $0.99\lambda^*$ and $1.01\lambda^*$. The cause is that no mass and no energy cross a face between states at rest, while the pressure jump pushes momentum across it.

**Theorem 1.** The AUSM scheme is conservative and its face flux is consistent with the Euler flux, so by the Lax-Wendroff theorem a limit of the scheme under grid refinement, if it converges boundedly almost everywhere, is a weak solution. Its flux is pure upwinding for supersonic flow and it keeps contacts at rest exactly.

*Proof.* The update is in flux form, so the sums of the cell values change only by boundary fluxes. Consistency is Lemma 2; the face flux is a continuous function of the two states, because the splits are continuous and $M_{1/2}\Phi$ is continuous where $M_{1/2}$ changes sign (both sides give 0 there). The other claims are Lemma 3 and Proposition 5. $\square$

**What is not proved here.** No entropy condition, TVD bound or positivity bound beyond Proposition 6 is proved. The order of accuracy is measured: on the smooth wave $\rho = 1 + 0.2\sin(2\pi(x - t))$, $u = 1$, $p = 1$ the measured $L^1$ orders are 0.98, 0.99 and 1.00. On Sod's tube the code shows a velocity of 1.010 in the first cell right of the initial jump, against the exact value 0.9274; this glitch is measured, not explained here.
