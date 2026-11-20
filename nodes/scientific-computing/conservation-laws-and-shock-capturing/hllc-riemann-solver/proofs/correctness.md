---
title: The HLLC flux is consistent and conservative, its middle states satisfy the jump conditions, and it resolves an isolated contact exactly
proves: [correctness]
status: full
---

**Setting.** The system is the 1D Euler equations $U_t + F(U)_x = 0$ with $U = (\rho, \rho u, E)$, $F = (\rho u, \rho u^2 + p, u(E + p))$ and $p = (\gamma - 1)(E - \rho u^2/2)$. At a face with states $U_L$ and $U_R$, line L1 gives speeds $S_L < S_R$. If $S_L \ge 0$ or $S_R \le 0$, lines L2 and L3 return the upwind flux. Otherwise lines L4 to L7 use the contact speed

$$S^* = \frac{p_R - p_L + \rho_L u_L(S_L - u_L) - \rho_R u_R(S_R - u_R)}{\rho_L(S_L - u_L) - \rho_R(S_R - u_R)},$$

the middle states, for $K = L, R$,

$$U^*_K = \rho_K\frac{S_K - u_K}{S_K - S^*}\Big(1,\ S^*,\ \frac{E_K}{\rho_K} + (S^* - u_K)\Big(S^* + \frac{p_K}{\rho_K(S_K - u_K)}\Big)\Big),$$

and the flux $F^*_K = F_K + S_K(U^*_K - U_K)$ with $K = L$ if $S^* \ge 0$ and $K = R$ if $S^* < 0$. The approximate Riemann solution $\hat U(x/t)$ is $U_L$, $U^*_L$, $U^*_R$, $U_R$ on the four intervals cut by $S_L$, $S^*$, $S_R$. The scheme is $U_j^{n+1} = U_j^n - \lambda(F_{j+1/2} - F_{j-1/2})$ with $\lambda = \Delta t/\Delta x$ (line L10).

We assume $S_L < u_L$, $u_R < S_R$ and $S_L < S^* < S_R$. The Einfeldt speeds of line L1 give the first two, since $S_L \le u_L - c_L$ and $S_R \ge u_R + c_R$. Batten, Clarke, Lambert and Causon (1997) discuss the third. The denominator of $S^*$ is then $\rho_L(S_L - u_L) - \rho_R(S_R - u_R) < 0$, so $S^*$ is defined.

**Lemma 1 (the middle states are the unique solution of the jump conditions).** Look for two middle states $U^*_L$, $U^*_R$ with the same velocity $S^*$ and the same pressure $p^*$, such that the Rankine-Hugoniot conditions

$$F(U^*_K) - F(U_K) = S_K\big(U^*_K - U_K\big), \qquad K = L, R,$$

hold, where $F(U^*_K)$ means $(\rho^*_K S^*,\ \rho^*_K S^{*2} + p^*,\ S^*(E^*_K + p^*))$. Then $S^*$, $\rho^*_K$ and $E^*_K$ are the ones above, and

$$p^* = p_K + \rho_K(S_K - u_K)(S^* - u_K) \quad\text{for both } K = L \text{ and } K = R.$$

*Proof.* The mass condition is $\rho^*_K S^* - \rho_K u_K = S_K(\rho^*_K - \rho_K)$, so $\rho^*_K(S_K - S^*) = \rho_K(S_K - u_K)$, which gives $\rho^*_K$. The momentum condition is $\rho^*_K S^{*2} + p^* - \rho_K u_K^2 - p_K = S_K(\rho^*_K S^* - \rho_K u_K)$. Use $\rho^*_K(S_K - S^*) = \rho_K(S_K - u_K)$:

$$p^* = p_K + \rho^*_K S^*(S_K - S^*) - \rho_K u_K(S_K - u_K) = p_K + \rho_K(S_K - u_K)(S^* - u_K).$$

The two values of $p^*$, for $K = L$ and $K = R$, must be equal. This is one linear equation in $S^*$:

$$p_L + \rho_L(S_L - u_L)S^* - \rho_L u_L(S_L - u_L) = p_R + \rho_R(S_R - u_R)S^* - \rho_R u_R(S_R - u_R),$$

whose solution is the formula for $S^*$. The energy condition is $S^*(E^*_K + p^*) - u_K(E_K + p_K) = S_K(E^*_K - E_K)$, so

$$E^*_K = \frac{(S_K - u_K)E_K - p_K u_K + p^* S^*}{S_K - S^*}.$$

Put in $p^* S^* = p_K S^* + \rho_K(S_K - u_K)(S^* - u_K)S^*$. The numerator becomes $(S_K - u_K)E_K + p_K(S^* - u_K) + \rho_K(S_K - u_K)(S^* - u_K)S^*$, and dividing by $S_K - S^*$ gives the third component of $U^*_K$ above. $\square$

The test checks the equal velocity, the equal $p^*$ and the jump conditions on 50 random pairs of states.

Note that $p^*$ is the pressure in the momentum flux, not the pressure that the equation of state gives for $U^*_K$. The two differ in general.

**Lemma 2 (consistency with the integral form).** $(S^* - S_L)U^*_L + (S_R - S^*)U^*_R = S_R U_R - S_L U_L - (F_R - F_L)$. So the average of $\hat U$ over the fan $[S_L, S_R]$ is the HLL state.

*Proof.* Write $F^*_K = F(U^*_K)$ as in Lemma 1. The jump across $S^*$ also satisfies the Rankine-Hugoniot condition: $F^*_R - F^*_L = \big(S^*(\rho^*_R - \rho^*_L),\ S^{*2}(\rho^*_R - \rho^*_L),\ S^*(E^*_R - E^*_L)\big) = S^*(U^*_R - U^*_L)$, because the velocity and $p^*$ are the same on both sides. Add the three conditions across $S_L$, $S^*$ and $S_R$:

$$F_R - F_L = S_L(U^*_L - U_L) + S^*(U^*_R - U^*_L) + S_R(U_R - U^*_R).$$

Collect the terms. $\square$

**Lemma 3 (the flux).** The flux of $\hat U$ at $x/t = 0$ is $F^*_L = F_L + S_L(U^*_L - U_L)$ if $S_L < 0 \le S^*$ and $F^*_R = F_R + S_R(U^*_R - U_R)$ if $S^* < 0 < S_R$. At $S^* = 0$ the two are equal, so the flux is a continuous function of the data across the switch of line L5.

*Proof.* The first two statements are the jump conditions of Lemma 1. At $S^* = 0$, the condition across $S^*$ of Lemma 2 gives $F^*_R - F^*_L = 0$. $\square$

**Theorem 1 (consistency and conservation).** $F^{hllc}(U, U) = F(U)$, and on a periodic grid $\sum_j U_j^{n+1} = \sum_j U_j^n$.

*Proof.* With $U_L = U_R = U$, the formula gives $S^* = u$, since numerator and denominator both reduce to a multiple of $\rho(S_L - S_R)$: the numerator is $\rho u(S_L - S_R)$ and the denominator is $\rho(S_L - S_R)$. Then $\rho^*_K = \rho$, the velocity is $u$, and the energy is $E$, so $U^*_K = U$ and the flux is $F(U)$. In the supersonic cases the flux is $F(U)$ directly. Conservation: each face flux enters two cells with opposite signs, and the sum telescopes. $\square$

**Theorem 2 (an isolated contact is exact).** Let $u_L = u_R = v$ and $p_L = p_R = p$, with any densities, and $S_L < v < S_R$. Then $S^* = v$, $U^*_L = U_L$ and $U^*_R = U_R$. So the HLLC flux is $F(U_L)$ if $v \ge 0$ and $F(U_R)$ if $v < 0$, which is the exact Godunov flux of this Riemann problem. In particular, for $v = 0$ every face flux of the scheme is $(0, p, 0)$, and a contact at rest is a steady solution of the scheme.

*Proof.* With equal $u$ and $p$, the numerator of $S^*$ is $v\big(\rho_L(S_L - v) - \rho_R(S_R - v)\big)$, which is $v$ times the denominator. So $S^* = v$. Then $\rho^*_K = \rho_K(S_K - v)/(S_K - v) = \rho_K$, the velocity is $v = u_K$, and the energy component is $\rho_K\big(E_K/\rho_K + 0\big) = E_K$. So $U^*_K = U_K$, and Lemma 3 gives $F^*_K = F_K$. The exact solution of this Riemann problem is the contact moving at speed $v$, and its flux at $x = 0$ is $F(U_L)$ for $v > 0$ and $F(U_R)$ for $v < 0$. For $v = 0$ both are $(0, p, 0)$. In the scheme every face then has the flux $(0, p, 0)$, so every flux difference is zero. $\square$

**Theorem 3 (positive density and convex averages).** Assume the speeds satisfy the conditions of the setting at every face and $\lambda \max|S| \le \frac12$. Then (1) every middle density $\rho^*_K$ is positive, and (2) $U_j^{n+1}$ is the average over cell $j$ of the approximate solutions $\hat U$ of its two faces. So if all the states $U_j$, $U^*_L$ and $U^*_R$ have positive density and pressure, so does $U_j^{n+1}$.

*Proof.* (1) $\rho^*_L = \rho_L(S_L - u_L)/(S_L - S^*)$ is a ratio of two negative numbers, and $\rho^*_R = \rho_R(S_R - u_R)/(S_R - S^*)$ is a ratio of two positive numbers. (2) With $\lambda\max|S| \le \frac12$ the fans of two faces do not meet inside a cell. By Lemma 3 and the jump conditions, the integral of $\hat U$ over the part of each fan inside cell $j$ changes $\Delta x\, U_j$ by exactly $-\Delta t$ times the flux difference across that part. Summing the two parts gives $\int_{C_j}\hat U\,dx = \Delta x\,U_j - \Delta t(F_{j+1/2} - F_{j-1/2})$. The set of states with positive density and pressure is convex (the pressure is a concave function of $U$ for $\rho > 0$, see Lemma 5 of the proof on the [HLL](/hll-riemann-solver/) page), so an average of such states is such a state. $\square$

**Remark.** Theorem 3 does not prove that the pressures of $U^*_L$ and $U^*_R$ are positive. Batten, Clarke, Lambert and Causon (1997) show that HLLC with the Einfeldt speeds is positively conservative. The proof here does not repeat their argument, and the test checks positivity only on the 123 problem. Unlike HLL, the HLLC middle states are not averages of the exact solution, so the cell entropy inequality of the HLL proof does not carry over.
