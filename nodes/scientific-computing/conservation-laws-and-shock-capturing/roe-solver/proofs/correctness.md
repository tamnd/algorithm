---
title: The Roe matrix has property U, the Roe flux is the Godunov flux of the linearized problem, and a single discontinuity is resolved exactly
proves: [correctness]
status: full
---

**Setting.** The system is the 1D Euler equations $U_t + F(U)_x = 0$ for an ideal gas with $U = (\rho, \rho u, E)$, $F = (\rho u, \rho u^2 + p, \rho u H)$, enthalpy $H = (E + p)/\rho$ and $p = (\gamma - 1)(E - \rho u^2/2)$, so that $c^2 = \gamma p/\rho = (\gamma - 1)(H - u^2/2)$. At a face with states $U_L$, $U_R$, line L1 computes the Roe averages with $w_K = \sqrt{\rho_K}$:

$$\tilde u = \frac{w_L u_L + w_R u_R}{w_L + w_R}, \qquad \tilde H = \frac{w_L H_L + w_R H_R}{w_L + w_R}, \qquad \tilde c^2 = (\gamma - 1)(\tilde H - \tilde u^2/2).$$

Line L2 takes $\lambda_1 = \tilde u - \tilde c$, $\lambda_2 = \tilde u$, $\lambda_3 = \tilde u + \tilde c$ and

$$r_1 = (1, \tilde u - \tilde c, \tilde H - \tilde u\tilde c), \quad r_2 = (1, \tilde u, \tilde u^2/2), \quad r_3 = (1, \tilde u + \tilde c, \tilde H + \tilde u\tilde c).$$

Line L3 computes, with $\Delta = U_R - U_L = (\Delta_0, \Delta_1, \Delta_2)$,

$$\alpha_2 = \frac{\gamma - 1}{\tilde c^2}\big(\Delta_0(\tilde H - \tilde u^2) + \tilde u\Delta_1 - \Delta_2\big), \quad \alpha_1 = \frac{\Delta_0(\tilde u + \tilde c) - \Delta_1 - \tilde c\alpha_2}{2\tilde c}, \quad \alpha_3 = \Delta_0 - \alpha_1 - \alpha_2,$$

and line L4 returns $F^{roe} = \frac12(F_L + F_R) - \frac12\sum_k |\lambda_k|\alpha_k r_k$.

**Lemma 1 ($\tilde c^2 > 0$).** For any two states with positive density and pressure, $\tilde H - \tilde u^2/2 > 0$.

*Proof.* Let $\theta = w_L/(w_L + w_R) \in (0, 1)$. Since $H_K = c_K^2/(\gamma - 1) + u_K^2/2$,

$$\tilde H - \frac{\tilde u^2}{2} = \frac{\theta c_L^2 + (1 - \theta)c_R^2}{\gamma - 1} + \frac12\big(\theta u_L^2 + (1 - \theta)u_R^2 - (\theta u_L + (1 - \theta)u_R)^2\big) = \frac{\theta c_L^2 + (1 - \theta)c_R^2}{\gamma - 1} + \frac{\theta(1 - \theta)}{2}(u_L - u_R)^2,$$

which is positive. $\square$

**Lemma 2 (property U).** Let $\hat U$ be the state with velocity $\tilde u$ and enthalpy $\tilde H$ (its density does not matter), and let $\hat A$ be the Jacobian $F'(U)$ written as a function of $(u, H)$ and evaluated at $(\tilde u, \tilde H)$. Then $F(U_R) - F(U_L) = \hat A\,(U_R - U_L)$.

*Proof.* Use Roe's parameter vector $Z = \sqrt\rho\,(1, u, H) = (z_1, z_2, z_3)$. A direct computation gives

$$U = \Big(z_1^2,\ z_1 z_2,\ \frac{z_1 z_3}{\gamma} + \frac{\gamma - 1}{2\gamma}z_2^2\Big), \qquad F = \Big(z_1 z_2,\ \frac{\gamma - 1}{\gamma}z_1 z_3 + \frac{\gamma + 1}{2\gamma}z_2^2,\ z_2 z_3\Big),$$

using $p = \frac{\gamma - 1}{\gamma}(\rho H - \rho u^2/2)$. Every component of $U$ and of $F$ is a quadratic form in $Z$. For a quadratic form $q(Z) = Z^T Q Z$ with $Q$ symmetric, $q(Z_R) - q(Z_L) = (Z_R + Z_L)^T Q (Z_R - Z_L) = q'(\bar Z)(Z_R - Z_L)$ with $\bar Z = \frac12(Z_L + Z_R)$, exactly. So

$$U_R - U_L = B(\bar Z)(Z_R - Z_L), \qquad F_R - F_L = C(\bar Z)(Z_R - Z_L),$$

where $B = \partial U/\partial Z$ and $C = \partial F/\partial Z$ are linear in $Z$. $B$ is lower triangular with diagonal $(2z_1, z_1, z_1/\gamma)$, so $\det B = 2z_1^3/\gamma > 0$ for $z_1 > 0$. Hence $F_R - F_L = C(\bar Z)B(\bar Z)^{-1}(U_R - U_L)$. By the chain rule $F'(U) = C(Z)B(Z)^{-1}$ at every state, so $C(\bar Z)B(\bar Z)^{-1}$ is the Jacobian at the state whose parameter vector is $\bar Z$. That state has $u = \bar z_2/\bar z_1 = \tilde u$ and $H = \bar z_3/\bar z_1 = \tilde H$. The Jacobian of the Euler equations depends on the state only through $u$ and $H$, so it is $\hat A$. $\square$

**Lemma 3 (eigenstructure and wave strengths).** $\hat A r_k = \lambda_k r_k$ for $k = 1, 2, 3$, and $\sum_k \alpha_k r_k = U_R - U_L$.

*Proof.* In terms of $u$ and $H$ the Euler Jacobian is

$$A = \begin{pmatrix} 0 & 1 & 0\\ \frac{\gamma - 3}{2}u^2 & (3 - \gamma)u & \gamma - 1\\ u\big(\frac{\gamma - 1}{2}u^2 - H\big) & H - (\gamma - 1)u^2 & \gamma u\end{pmatrix}.$$

For $r_2 = (1, u, u^2/2)$: the rows give $u$, $u^2\big(\frac{\gamma - 3}{2} + (3 - \gamma) + \frac{\gamma - 1}{2}\big) = u^2$ and $u^3\big(\frac{\gamma - 1}{2} - (\gamma - 1) + \frac{\gamma}{2}\big) = u^3/2$, which is $u\,r_2$. For $r_{1,3} = (1, u \pm c, H \pm uc)$: the first row gives $u \pm c$. The second row gives $\frac{3 - \gamma}{2}u^2 + (\gamma - 1)H \pm 2uc$, and with $(\gamma - 1)H = c^2 + \frac{\gamma - 1}{2}u^2$ this is $(u \pm c)^2$. The third row minus $(u \pm c)(H \pm uc)$ is $u\big((\gamma - 1)(H - u^2/2) - c^2\big) = 0$. So $A r = \lambda r$ at every $(u, H)$ with $c^2 = (\gamma - 1)(H - u^2/2)$, in particular at $(\tilde u, \tilde H, \tilde c)$.

For the strengths, compare components of $\sum_k \alpha_k r_k$ with $\Delta$. The first component is $\alpha_1 + \alpha_2 + \alpha_3 = \Delta_0$ by the definition of $\alpha_3$. The second is $\tilde u\Delta_0 + \tilde c(\alpha_3 - \alpha_1)$, so we need $\alpha_3 - \alpha_1 = (\Delta_1 - \tilde u\Delta_0)/\tilde c$. The third is $\tilde H(\alpha_1 + \alpha_3) + \tilde u\tilde c(\alpha_3 - \alpha_1) + \frac{\tilde u^2}{2}\alpha_2$. Put in $\alpha_1 + \alpha_3 = \Delta_0 - \alpha_2$ and the value of $\alpha_3 - \alpha_1$: the condition becomes $\alpha_2(\tilde H - \tilde u^2/2) = \tilde H\Delta_0 + \tilde u\Delta_1 - \tilde u^2\Delta_0 - \Delta_2$, which is the formula for $\alpha_2$ because $\tilde H - \tilde u^2/2 = \tilde c^2/(\gamma - 1)$ (positive by Lemma 1). Then $\alpha_1 = \frac12\big((\Delta_0 - \alpha_2) - (\Delta_1 - \tilde u\Delta_0)/\tilde c\big)$, which is the formula of line L3. $\square$

Lemmas 2 and 3 together give $F_R - F_L = \sum_k \lambda_k\alpha_k r_k$. The test checks both identities on 100 random pairs of states.

**Theorem 1 (the Roe flux is the Godunov flux of the linearized problem).** Let $V$ solve the linear Riemann problem $V_t + \hat A V_x = 0$ with data $U_L$, $U_R$. Then $F_L + \hat A\big(V(0^+) - U_L\big) = F^{roe}$, so the Roe flux is the flux of the linearized solution at the face, made consistent with $F$ by property U.

*Proof.* The solution of the linear problem is $V(x/t) = U_L + \sum_{\lambda_k < x/t}\alpha_k r_k$. So

$$F_L + \hat A(V(0) - U_L) = F_L + \sum_{\lambda_k < 0}\lambda_k\alpha_k r_k = F_R - \sum_{\lambda_k > 0}\lambda_k\alpha_k r_k,$$

where the second form uses $F_R - F_L = \sum_k\lambda_k\alpha_k r_k$. The mean of the two forms is $\frac12(F_L + F_R) - \frac12\sum_k|\lambda_k|\alpha_k r_k$. $\square$

**Theorem 2 (consistency and conservation).** $F^{roe}(U, U) = F(U)$, and on a periodic grid the scheme keeps $\sum_j U_j$.

*Proof.* With $U_L = U_R$, $\Delta = 0$, so all $\alpha_k = 0$, and the flux is $F(U)$. The update is in conservation form, so the sum telescopes. $\square$

**Theorem 3 (a single discontinuity is exact).** Let $U_L \ne U_R$ satisfy the Rankine-Hugoniot condition $F_R - F_L = s(U_R - U_L)$ for some speed $s$. Then $U_R - U_L$ is an eigenvector of $\hat A$ with eigenvalue $s$, and $F^{roe} = F_L$ if $s \ge 0$ and $F^{roe} = F_R$ if $s < 0$, the flux of the moving discontinuity. If $s = 0$, a grid with $U_L$ on the left and $U_R$ on the right of one face is a steady solution of the scheme. This holds whether or not the discontinuity satisfies the entropy condition.

*Proof.* By Lemma 2, $\hat A\Delta = F_R - F_L = s\Delta$. The eigenvalues of $\hat A$ are distinct (Lemma 1 gives $\tilde c > 0$), so $\Delta$ is a multiple of one eigenvector $r_k$ with $\lambda_k = s$, and by Lemma 3, $\alpha$ has only that component. Then $\sum_k|\lambda_k|\alpha_k r_k = |s|\Delta$, and

$$F^{roe} = \tfrac12(F_L + F_R) - \tfrac12|s|\Delta = \tfrac12(F_L + F_R) \mp \tfrac12(F_R - F_L),$$

which is $F_L$ for $s \ge 0$ and $F_R$ for $s < 0$. For $s = 0$, $F_L = F_R$. Every other face has equal states and the flux $F_L$ or $F_R$. All flux differences are zero. $\square$

The tests check this for a contact at rest, a Mach 2 shock at rest, and the same pair of states swapped, which is an expansion shock at rest. The scheme keeps all three to $10^{-12}$. The last one is not an entropy solution: this is why Roe's scheme needs an [entropy fix](/harten-hyman-entropy-fix/).

**Theorem 4 (a scalar law).** For $u_t + f(u)_x = 0$ the Roe flux is $\frac12(f_L + f_R) - \frac12|a|(u_R - u_L)$ with $a = (f_R - f_L)/(u_R - u_L)$. If $\lambda\max|a| \le 1$ the scheme is TVD.

*Proof.* The scheme is $u_j^{n+1} = u_j + C_{j+1/2}\Delta_{j+1/2} - D_{j-1/2}\Delta_{j-1/2}$ with $C = \frac{\lambda}{2}(|a| - a) \ge 0$ and $D = \frac{\lambda}{2}(|a| + a) \ge 0$, since $F_{j+1/2} - f_j = \frac12(a - |a|)\Delta_{j+1/2}$ and $F_{j-1/2} - f_j = -\frac12(a + |a|)\Delta_{j-1/2}$. So $C + D = \lambda|a| \le 1$, and Harten's lemma (Lemma 3 of the proof on the [Rusanov flux](/rusanov-flux/) page) applies. $\square$

**Remark (what is not true).** The Roe scheme does not satisfy the entropy condition (Theorem 3 with an expansion shock), and it is not positively conservative. Einfeldt, Munz, Roe and Sjögreen (1991) showed that schemes based on linearized Riemann solvers, Roe's among them, are not positive for all data. The test shows it on the 123 problem: after one step, the two center cells have negative pressure.
