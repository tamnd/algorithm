---
title: The HLL scheme is conservative and consistent, and with speeds that bound the waves it keeps positivity and satisfies a cell entropy inequality
proves: [correctness]
status: full
---

**Setting.** A system $U_t + F(U)_x = 0$ has a convex entropy pair $(\eta, q)$, so that entropy solutions satisfy $\eta(U)_t + q(U)_x \le 0$ in the weak sense. The scheme stores cell averages $U_j^n$ on a uniform grid with width $\Delta x$ and steps $U_j^{n+1} = U_j^n - \lambda(F_{j+1/2} - F_{j-1/2})$ with $\lambda = \Delta t/\Delta x$ (line L7). At each face, with $U_L = U_j$ and $U_R = U_{j+1}$, lines L1 to L4 give

$$F^{hll} = \begin{cases} F_L & S_L \ge 0,\\ \dfrac{S_R F_L - S_L F_R + S_L S_R (U_R - U_L)}{S_R - S_L} & S_L < 0 < S_R,\\ F_R & S_R \le 0,\end{cases}$$

with $F_L = F(U_L)$ and $F_R = F(U_R)$. Let $S_L^- = \min(S_L, 0)$ and $S_R^+ = \max(S_R, 0)$. A short check shows that the middle formula with $S_L^-$ and $S_R^+$ in place of $S_L$ and $S_R$ gives all three cases: if $S_L \ge 0$ it gives $S_R F_L / S_R = F_L$, and if $S_R \le 0$ it gives $F_R$. So below we use only the middle formula, with speeds that satisfy $S_L \le 0 \le S_R$.

Define the HLL state

$$U^* = \frac{S_R U_R - S_L U_L - (F_R - F_L)}{S_R - S_L}.$$

The approximate Riemann solution is $\hat U(x/t) = U_L$ for $x/t < S_L$, $U^*$ for $S_L < x/t < S_R$, and $U_R$ for $x/t > S_R$.

We say that the speeds **bound the waves** if every wave of the exact Riemann solution with data $U_L$, $U_R$ moves at a speed in $[S_L, S_R]$. The proofs of Lemma 3 and Theorems 1 and 2 need this. The estimates of line L1 do not give it in every case (see the remark at the end).

**Lemma 1 (consistency and conservation).** $F^{hll}(U, U) = F(U)$. On a periodic grid, $\sum_j U_j^{n+1} = \sum_j U_j^n$.

*Proof.* With $U_L = U_R = U$, the middle formula is $(S_R - S_L)F(U)/(S_R - S_L) = F(U)$, and the other two cases give $F(U)$ directly. For conservation, each face flux enters cell $j$ with the factor $-\lambda$ and cell $j+1$ with $+\lambda$, so the sum telescopes. The test checks this exactly for Burgers' equation in `Fraction` arithmetic. $\square$

**Lemma 2 (the flux is the flux of the approximate solution).** $F^{hll} = F_L + S_L(U^* - U_L) = F_R + S_R(U^* - U_R)$.

*Proof.* $U^* - U_L = \big(S_R(U_R - U_L) - (F_R - F_L)\big)/(S_R - S_L)$. So

$$F_L + S_L(U^* - U_L) = \frac{(S_R - S_L)F_L + S_L S_R (U_R - U_L) - S_L F_R + S_L F_L}{S_R - S_L} = \frac{S_R F_L - S_L F_R + S_L S_R (U_R - U_L)}{S_R - S_L}.$$

The second form follows in the same way, or from the first form and the definition of $U^*$. $\square$

The two forms are the Rankine-Hugoniot conditions of the two jumps of $\hat U$, at speed $S_L$ and at speed $S_R$. So $\hat U$ is a weak solution of the conservation law in the integral sense over the fan, though not a true solution.

**Lemma 3 (the HLL state is the average of the exact fan).** If the speeds bound the waves and $U$ is the exact Riemann solution, then for every $T > 0$

$$U^* = \frac{1}{(S_R - S_L)T}\int_{S_L T}^{S_R T} U(x, T)\,dx.$$

*Proof.* Integrate $U_t + F(U)_x = 0$ over the rectangle $[S_L T, S_R T] \times [0, T]$. Because the speeds bound the waves, $U = U_L$ on the left side $x = S_L T$ and $U = U_R$ on the right side $x = S_R T$ for $0 < t < T$. The integral form of the law gives

$$\int_{S_L T}^{S_R T} U(x, T)\,dx = S_R T\, U_R - S_L T\, U_L - T(F_R - F_L).$$

Divide by $(S_R - S_L)T$. $\square$

**Lemma 4 (Jensen).** Let $\eta$ be convex on a convex set $G$ and let $V$ be an integrable function on an interval $I$ with values in $G$. Then the average $\bar V$ is in $G$ and $\eta(\bar V) \le \frac{1}{|I|}\int_I \eta(V)\,dx$.

*Proof.* This is Jensen's inequality for the uniform probability measure on $I$. $\bar V$ is in the closed convex hull of the values of $V$. $\square$

**Lemma 5 (the admissible set is convex).** For the Euler equations, the set $G = \{(\rho, m, E) : \rho > 0,\ E - m^2/(2\rho) > 0\}$ of states with positive density and pressure is convex, and the pressure $p = (\gamma - 1)(E - m^2/(2\rho))$ is a concave function on $\rho > 0$.

*Proof.* The function $\phi(\rho, m) = m^2/\rho$ is convex on $\rho > 0$: its Hessian is $\frac{2}{\rho^3}\begin{pmatrix} m^2 & -m\rho \\ -m\rho & \rho^2\end{pmatrix}$, which has determinant 0 and trace $2(m^2 + \rho^2)/\rho^3 > 0$, so it is positive semidefinite. Then $E - \phi/2$ is concave, and $G$ is the intersection of the half space $\rho > 0$ with the set where a concave function is positive. Both are convex. $\square$

**Theorem 1 (positivity).** For the Euler equations, let every face use speeds that bound the waves, and let $\lambda \max |S| \le \frac12$. If every $U_j^n$ is in $G$, then every $U_j^{n+1}$ is in $G$.

*Proof.* Put the approximate solution $\hat U$ of each face at the face, and run it for the time $\Delta t$. Because $\lambda\max|S| \le \frac12$, each fan stays in the half cells next to its face, and the fans do not meet. Let $W(x)$ be the function so made on cell $j$ at time $\Delta t$. It is $U_j$ except on the part $[x_{j-1/2}, x_{j-1/2} + S_R\Delta t]$, where it is the state $U^*$ of the left face, and on the part $[x_{j+1/2} + S_L\Delta t, x_{j+1/2}]$, where it is the state $U^*$ of the right face. By Lemma 2 its cell average is

$$\frac{1}{\Delta x}\int_{C_j} W\,dx = U_j - \lambda\big(F_{j+1/2} - F_{j-1/2}\big) = U_j^{n+1},$$

because the integral over each half fan changes by exactly $-\Delta t$ times the flux difference across it. By Lemma 3, each $U^*$ is the average of an exact Riemann solution with data in $G$. That solution has positive density and pressure except in a vacuum region, if the data make one, where $\rho = m = E = 0$. It equals $U_L$ or $U_R$ near the two sides of the fan. So the average density is positive, and by the concavity of Lemma 5 (Jensen's inequality for the concave pressure, with $p = 0$ in the vacuum) the pressure of the average is at least the average pressure, which is positive. So $U^*$ is in $G$. Then $U_j^{n+1}$ is the average of $W$, whose values are in $G$, so by Lemma 4 again it is in $G$. $\square$

**Theorem 2 (cell entropy inequality).** Let every face use speeds that bound the waves, and let $\lambda \max|S| \le \frac12$. Define the numerical entropy flux at each face by

$$Q_{j+1/2} = q_L + S_L\big(\eta(U^*) - \eta_L\big),$$

with $\eta_L = \eta(U_L)$ and $q_L = q(U_L)$. Then $Q(U, U) = q(U)$ and

$$\eta(U_j^{n+1}) \le \eta(U_j^n) - \lambda\big(Q_{j+1/2} - Q_{j-1/2}\big).$$

*Proof.* Consistency: with $U_L = U_R = U$, the state $U^*$ is $U$, so $Q = q(U)$.

Fix a face and use local coordinates with the face at $x = 0$. The exact Riemann solution satisfies the integral form of the entropy inequality over the rectangle $[S_L \Delta t, S_R \Delta t] \times [0, \Delta t]$, and its side values are $U_L$ and $U_R$, so

$$\int_{S_L\Delta t}^{S_R\Delta t} \eta(U(x, \Delta t))\,dx \le S_R\Delta t\,\eta_R - S_L\Delta t\,\eta_L - \Delta t(q_R - q_L).$$

By Lemma 3 and Lemma 4, the left side is at least $(S_R - S_L)\Delta t\,\eta(U^*)$. So

$$(S_R - S_L)\,\eta(U^*) \le S_R\eta_R - S_L\eta_L - (q_R - q_L). \tag{1}$$

Now split the fan of $\hat U$ at $x = 0$. On the left half, by the definition of $Q$ (with equality),

$$\int_{S_L\Delta t}^{0} \eta(\hat U)\,dx = -S_L\Delta t\,\eta(U^*) = -S_L\Delta t\,\eta_L - \Delta t(Q - q_L).$$

On the right half, (1) and the definition of $Q$ give

$$\int_0^{S_R\Delta t} \eta(\hat U)\,dx = S_R\Delta t\,\eta(U^*) \le S_R\Delta t\,\eta_R - \Delta t(q_R - Q).$$

Now take cell $j$ and the function $W$ of the proof of Theorem 1. Its integral of $\eta(W)$ has three parts: the right half of the fan of the face $j - 1/2$ (where $U_R = U_j$), the middle part where $W = U_j$, and the left half of the fan of the face $j + 1/2$ (where $U_L = U_j$). Add the two bounds above and $\eta(U_j)$ times the length of the middle part, $\Delta x - S_R^{(j-1/2)}\Delta t + S_L^{(j+1/2)}\Delta t$:

$$\int_{C_j}\eta(W)\,dx \le \Delta x\,\eta(U_j) - \Delta t\big(q_j - Q_{j-1/2}\big) - \Delta t\big(Q_{j+1/2} - q_j\big) = \Delta x\,\eta(U_j) - \Delta t\big(Q_{j+1/2} - Q_{j-1/2}\big).$$

By Lemma 4, $\eta(U_j^{n+1}) = \eta(\text{average of } W) \le \frac{1}{\Delta x}\int_{C_j}\eta(W)\,dx$. Divide by $\Delta x$. $\square$

With Lemma 1, this gives the conclusion of Harten, Lax and van Leer (1983): if the scheme converges boundedly in $L^1_{loc}$, the [Lax-Wendroff theorem](/lax-wendroff-theorem/) makes the limit a weak solution, and the same argument applied to the cell entropy inequality makes it satisfy $\eta(U)_t + q(U)_x \le 0$.

**Theorem 3 (TVD for a convex scalar law).** For a scalar law with convex $f$, let line L1 take $S_L = \min(f'(u_L), f'(u_R))$ and $S_R = \max(f'(u_L), f'(u_R))$. If $\lambda \max(|S_L|, |S_R|) \le 1$ at every face, the scheme is TVD.

*Proof.* Let $a = (f(u_R) - f(u_L))/(u_R - u_L)$ when $u_R \ne u_L$. Since $f'$ is nondecreasing, $a$ is a mean of $f'$ over the interval between the states, so $S_L \le a \le S_R$. Take the case $S_L < 0 < S_R$. From the middle formula,

$$F^{hll} - f_L = \frac{S_L(S_R - a)}{S_R - S_L}(u_R - u_L), \qquad F^{hll} - f_R = \frac{S_R(S_L - a)}{S_R - S_L}(u_R - u_L).$$

Write $U_j^{n+1} = U_j - \lambda(F_{j+1/2} - f_j) + \lambda(F_{j-1/2} - f_j)$. This is Harten's incremental form $U_j + C_{j+1/2}\Delta_{j+1/2} - D_{j-1/2}\Delta_{j-1/2}$, with

$$C = -\lambda\frac{S_L(S_R - a)}{S_R - S_L} \ge 0, \qquad D = \lambda\frac{S_R(a - S_L)}{S_R - S_L} \ge 0.$$

The sum $C + D = \lambda\,\frac{a(S_L + S_R) - 2S_L S_R}{S_R - S_L}$ is linear in $a$. At $a = S_R$ it is $\lambda S_R$, and at $a = S_L$ it is $-\lambda S_L$. So $C + D \le \lambda\max(|S_L|, |S_R|) \le 1$. In the case $S_L \ge 0$ the flux is $f_L$, so $C = 0$ and $D = \lambda a \in [0, 1]$. The case $S_R \le 0$ is the mirror case. Harten's lemma (proved on the [Rusanov flux](/rusanov-flux/) page, Lemma 3 of its proof) gives $TV(u^{n+1}) \le TV(u^n)$. $\square$

**Remark (the speed estimates are not proven bounds).** For Sod's data, the right shock moves at 1.75216. The Davis estimate gives $S_R = \max(u_L + c_L, u_R + c_R) = 1.18322$, and the Einfeldt estimate gives $S_R = 1.15190$. Neither bounds the shock, so Theorems 1 and 2 do not apply to these faces. The scheme still runs well in the tests, but its positivity and entropy properties then rest on the analysis of Einfeldt (1988) and Einfeldt, Munz, Roe and Sjögreen (1991), not on the proof above. Bounds that are proven, such as those built from the two-rarefaction or the two-shock pressure estimates (Toro 2009, Chapter 10), make the theorems apply.
