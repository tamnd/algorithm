---
title: MacCormack's scheme is conservative, consistent and second order, and it is not monotone
proves: [correctness]
status: full
---

**Setting.** The law is $U_t + F(U)_x = 0$ with a smooth flux $F$ and Jacobian $A(U) = F'(U)$. The grid has spacing $\Delta x$, the time step is $\Delta t$, and $\lambda = \Delta t/\Delta x$. One step of MACCORMACK computes, for every cell $j$,

$$U^*_j = U_j - \lambda\big(F(U_{j+1}) - F(U_j)\big) \quad \text{(line L2)}, \qquad U^{\text{new}}_j = \tfrac12(U_j + U^*_j) - \tfrac{\lambda}{2}\big(F(U^*_j) - F(U^*_{j-1})\big) \quad \text{(line L3)}.$$

The neighbours of the end cells come from the boundary condition (periodic or transmissive ghost cells).

**Termination.** The loop of line L1 runs the given number of steps $K$. Each step evaluates $F$ at $2M$ states (plus the ghost states) and does $O(M)$ further arithmetic.

**Lemma 1 (conservation form).** Let $H_{j+1/2} = \frac12\big(F(U_{j+1}) + F(U^*_j)\big)$. Then $U^{\text{new}}_j = U_j - \lambda(H_{j+1/2} - H_{j-1/2})$, and $H(V, V) = F(V)$ when all the arguments are equal to $V$.

*Proof.* Insert $U^*_j$ in the first term of line L3:

$$U^{\text{new}}_j = U_j - \tfrac{\lambda}{2}\big(F(U_{j+1}) - F(U_j)\big) - \tfrac{\lambda}{2}\big(F(U^*_j) - F(U^*_{j-1})\big) = U_j - \lambda\Big(\tfrac{F(U_{j+1}) + F(U^*_j)}{2} - \tfrac{F(U_j) + F(U^*_{j-1})}{2}\Big).$$

If $U_j = U_{j+1} = V$, then $U^*_j = V$ and $H_{j+1/2} = F(V)$. $\square$

So with periodic boundaries $\sum_jU^{\text{new}}_j = \sum_jU_j$ exactly, and by the [Lax-Wendroff theorem](/lax-wendroff-theorem/), if the scheme converges boundedly almost everywhere as $\Delta x \to 0$ with fixed $\lambda$, the limit is a weak solution, so its shocks move at the Rankine-Hugoniot speed. The theorem does not say that the scheme converges, or that the limit is the entropy solution.

**Lemma 2 (linear systems).** If $F(U) = AU$ with a constant matrix $A$, one step equals the [Lax-Wendroff method](/lax-wendroff-method/):

$$U^{\text{new}}_j = U_j - \tfrac{\lambda}{2}A(U_{j+1} - U_{j-1}) + \tfrac{\lambda^2}{2}A^2(U_{j+1} - 2U_j + U_{j-1}).$$

*Proof.* Write $\delta_+V_j = V_{j+1} - V_j$ and $\delta_-V_j = V_j - V_{j-1}$, which commute. Then $U^* = U - \lambda A\delta_+U$ and $\delta_-U^* = \delta_-U - \lambda A\delta_-\delta_+U$. So

$$U^{\text{new}} = U - \tfrac{\lambda}{2}A\delta_+U - \tfrac{\lambda}{2}A\delta_-U + \tfrac{\lambda^2}{2}A^2\delta_-\delta_+U,$$

and $\delta_+ + \delta_-$ is the central difference $U_{j+1} - U_{j-1}$, while $\delta_-\delta_+U_j = U_{j+1} - 2U_j + U_{j-1}$. $\square$

**Theorem 1 (second order).** Let $u$ be a smooth solution and $\lambda$ fixed. Insert $U_j = u(x_j, t_n)$ in one step. Then $U^{\text{new}}_j = u(x_j, t_n + \Delta t) + O(\Delta x^3)$, so the local truncation error is $O(\Delta x^2)$.

*Proof.* Write $k = \Delta t$, $h = \Delta x$, $D_\pm$ for the divided differences $\delta_\pm/h$, and $a = A(u)$. The predictor is the smooth grid function $u^* = u - kD_+F(u)$, so $F(u^*) = F(u) - k\,a\,D_+F(u) + O(k^2)$, where the remainder is a smooth function of $x$. Then $D_-$ of the remainder is also $O(k^2)$, and

$$U^{\text{new}} = u - \tfrac{k}{2}(D_+ + D_-)F(u) + \tfrac{k^2}{2}D_-\big(a\,D_+F(u)\big) + O(k^3).$$

Here $\frac12(D_+ + D_-)F = F_x + O(h^2)$ and $D_-(aD_+F) = (aF_x)_x + O(h)$. The exact solution satisfies $u_t = -F_x$ and $u_{tt} = -(F_t)_x = -(a u_t)_x = (aF_x)_x$, so $u(t_n + k) = u - kF_x + \frac{k^2}{2}(aF_x)_x + O(k^3)$. The difference is $O(kh^2) + O(k^2h) + O(k^3) = O(h^3)$ for fixed $\lambda$. $\square$

**Theorem 2 (linear stability).** For $u_t + au_x = 0$ with $\nu = a\lambda$ on a periodic grid, the amplification factor is $g(\theta) = 1 - i\nu\sin\theta - \nu^2(1 - \cos\theta)$, and $|g(\theta)| \le 1$ for all $\theta$ if and only if $|\nu| \le 1$.

*Proof.* By Lemma 2, insert $U_j = e^{ij\theta}$ in the Lax-Wendroff formula. With $s = 1 - \cos\theta \in [0, 2]$ and $\sin^2\theta = s(2 - s)$,

$$|g|^2 = (1 - \nu^2s)^2 + \nu^2s(2 - s) = 1 - \nu^2(1 - \nu^2)s^2.$$

This is at most 1 for all $s$ exactly when $\nu^2 \le 1$. By the [Lax equivalence theorem](/lax-equivalence-theorem/), the scheme then converges for this linear problem. $\square$

**Theorem 3 (not monotone, not TVD).** For $0 < \nu < 1$ the scheme for linear advection is not monotone, and it can increase the total variation.

*Proof.* By Lemma 2, $U^{\text{new}}_j = \frac{\nu(1 + \nu)}{2}U_{j-1} + (1 - \nu^2)U_j - \frac{\nu(1 - \nu)}{2}U_{j+1}$, and the last coefficient is negative. So raising $U_{j+1}$ lowers $U^{\text{new}}_j$. A concrete case: with $\nu = \frac12$ and periodic data $(1, 1, 1, 0, 0, 0)$, one step gives $(\frac58, 1, \frac98, \frac38, 0, -\frac18)$. The new values leave the range $[0, 1]$, and the total variation grows from $2$ to $\frac52$. $\square$

Theorem 3 agrees with [Godunov's order barrier](/godunov-order-barrier/): a linear scheme that is second order cannot be monotone. For a nonlinear flux the scheme is also not TVD; near a shock it gives oscillations unless viscosity is added. $\blacksquare$
