---
title: Second order, high frequency limit and the trapezoidal case of the generalized-alpha method
proves: [correctness]
status: partial
---

**Setting.** $M$ is symmetric positive definite, $\beta > 0$, $\alpha_m < 1$, $\alpha_f < 1$, and $L = (1 - \alpha_m) M + (1 - \alpha_f)(\gamma\,dt\,C + \beta\,dt^2 K)$ is invertible. Lines L3 to L8 give, for every $k \ge 0$,

$$\text{(U1)}\quad d_{k+1} = d_k + dt\,v_k + dt^2\big((\tfrac12 - \beta) a_k + \beta a_{k+1}\big), \qquad \text{(U2)}\quad v_{k+1} = v_k + dt\big((1 - \gamma) a_k + \gamma a_{k+1}\big),$$

$$\text{(B)}\quad M\big((1 - \alpha_m) a_{k+1} + \alpha_m a_k\big) + C\big((1 - \alpha_f) v_{k+1} + \alpha_f v_k\big) + K\big((1 - \alpha_f) d_{k+1} + \alpha_f d_k\big) = F(t_k + (1 - \alpha_f)\,dt).$$

Indeed lines L7 and L8 give $d_{k+1} = \tilde d + \beta\,dt^2 a_{k+1}$ and $v_{k+1} = \tilde v + \gamma\,dt\,a_{k+1}$, which are (U1) and (U2). Put them into (B): the terms in $a_{k+1}$ are $L a_{k+1}$ and the other terms are those of the right side $r$ of line L5, so (B) is the system of line L6. Write $\delta = \alpha_f - \alpha_m$. The status is partial because the unconditional stability (Theorem 4) and the global convergence are cited, not proved.

**Theorem 1 (consistency and the second order condition).** Let $d$ be a smooth solution of $M\ddot d + C\dot d + K d = F$, with $v = \dot d$ and $a = \ddot d$. Insert the shifted exact values $D_k = d(t_k)$, $V_k = v(t_k)$, $A_k = a(t_k - \delta\,dt)$ into (U1), (U2) and (B). Then the defect of (U1) is $O(dt^3)$, the defect of (B) is $O(dt^2)$, and the defect of (U2) is

$$(\tfrac12 + \delta - \gamma)\,dt^2\,\dot a(t_k) + O(dt^3).$$

*Proof.* Write $a$, $\dot a$ for the values at $t_k$. Then $A_k = a - \delta\,dt\,\dot a + O(dt^2)$ and $A_{k+1} = a + (1 - \delta)\,dt\,\dot a + O(dt^2)$.

(U1): $d(t_k + dt) - d - dt\,v = \tfrac12 dt^2 a + O(dt^3)$, and $dt^2((\tfrac12 - \beta)A_k + \beta A_{k+1}) = \tfrac12 dt^2 a + O(dt^3)$.

(U2): $v(t_k + dt) - v = dt\,a + \tfrac12 dt^2 \dot a + O(dt^3)$, and $dt((1 - \gamma) A_k + \gamma A_{k+1}) = dt\,a + dt^2\dot a\,\big(-(1 - \gamma)\delta + \gamma(1 - \delta)\big) + O(dt^3) = dt\,a + (\gamma - \delta)\,dt^2\dot a + O(dt^3)$. The difference is $(\tfrac12 - \gamma + \delta)\,dt^2 \dot a + O(dt^3)$.

(B): put $s = t_k + (1 - \alpha_f)\,dt$. A weighted mean $(1 - \alpha) g(t + dt) + \alpha g(t)$ of a smooth $g$ equals $g(t + (1 - \alpha)\,dt) + O(dt^2)$. So $(1 - \alpha_m)A_{k+1} + \alpha_m A_k = a(t_k - \delta\,dt + (1 - \alpha_m)\,dt) + O(dt^2) = a(s) + O(dt^2)$, because $-\delta + 1 - \alpha_m = 1 - \alpha_f$. In the same way the $v$ and $d$ terms equal $v(s) + O(dt^2)$ and $d(s) + O(dt^2)$. The exact equation at $s$ gives a defect $O(dt^2)$. $\square$

*Why this is the order condition.* Subtract the scheme from the shifted exact values. In one step from exact data, the defect $O(dt^2)$ of (B) changes $a_{k+1}$ by $L^{-1} O(dt^2)$, and $L^{-1}M$ stays bounded as $dt \to 0$ because $L \to (1 - \alpha_m) M$. Through (U1) and (U2) this changes $d_{k+1}$ by $O(dt^4)$ and $v_{k+1}$ by $O(dt^3)$. The defect of (U1) changes $d_{k+1}$ by $O(dt^3)$. So the local error of one step in $(d, v)$ is $O(dt^3)$, that is $O(dt^2)$ per unit time, exactly when $\gamma = \tfrac12 + \delta = \tfrac12 - \alpha_m + \alpha_f$. For other $\gamma$ the velocity has the local error $(\tfrac12 + \delta - \gamma)\,dt^2\dot a$ and the method is first order. With the uniform stability of Theorem 4, a local error $O(dt^3)$ gives a global error $O(dt^2)$ on a fixed interval (Chung and Hulbert 1993). The shifted value $A_0 = a(-\delta\,dt)$ differs from the $a_0$ of line L1 by $O(dt)$. This start error enters $d_1$ through $dt^2 a_0$ and $v_1$ through $dt\,a_0$, so it adds $O(dt^2)$ to the global error.

The same computation shows the role of the load time: if the load is taken at $t_{k+1}$ in place of $s$, the defect of (B) becomes $F(t_{k+1}) - F(s) + O(dt^2) = O(dt)$, which changes $v_{k+1}$ by $O(dt^2)$ per step, and the method is first order. The reference test `test_load_at_the_shifted_time` measures orders 2 and 1 for the two choices.

**Theorem 2 (high frequency limit).** For the mode $\ddot d + \omega^2 d = 0$ put $\Omega = \omega\,dt$ and $x_k = (d_k, dt\,v_k, dt^2 a_k)$, so that $x_{k+1} = A(\Omega) x_k$. As $\Omega \to \infty$, $A(\Omega)$ converges to a matrix $A_\infty$ with the eigenvalues

$$\lambda_1 = -\frac{\alpha_f}{1 - \alpha_f}, \qquad \lambda_2 + \lambda_3 = 2 - \frac{\gamma + \tfrac12}{\beta}, \qquad \lambda_2\lambda_3 = 1 - \frac{\gamma - \tfrac12}{\beta}.$$

*Proof.* Write $D, V, A$ for the three components of $x_k$ and $D', V', A'$ for those of $x_{k+1}$. Multiply (B) by $dt^2$ and use $dt^2 a = -\Omega^2 d$ for the stiffness term:

$$(1 - \alpha_m) A' + \alpha_m A + \Omega^2\big((1 - \alpha_f) D' + \alpha_f D\big) = 0, \qquad D' = D + V + (\tfrac12 - \beta)A + \beta A'.$$

Put the second relation into the first and divide by $\Omega^2$. As $\Omega \to \infty$ the coefficients converge, and the limit is $(1 - \alpha_f)\beta A' = -D - (1 - \alpha_f)V - (1 - \alpha_f)(\tfrac12 - \beta)A$. The coefficient of $A'$ before the limit is $(1 - \alpha_m)/\Omega^2 + (1 - \alpha_f)\beta$, which stays away from 0, so the entries of $A(\Omega)$ converge. In the limit, $D' = D + V + (\tfrac12 - \beta)A + \beta A' = D - D/(1 - \alpha_f) = \lambda_1 D$. So the first row of $A_\infty$ is $(\lambda_1, 0, 0)$, $\lambda_1$ is an eigenvalue, and the other two are those of the block for $(V, A)$. From $A' = -\tfrac1\beta V - \tfrac{1}{\beta}(\tfrac12 - \beta)A + (\cdot)D$ and $V' = V + (1 - \gamma)A + \gamma A'$ this block is

$$B = \begin{pmatrix} 1 - \gamma/\beta & 1 - \gamma/(2\beta) \\ -1/\beta & 1 - 1/(2\beta) \end{pmatrix},$$

with trace $2 - (\gamma + \tfrac12)/\beta$ and determinant $1 + \tfrac{1}{2\beta} - \tfrac{\gamma}{\beta} = 1 - (\gamma - \tfrac12)/\beta$. $\square$

**Corollary 3 (the Chung-Hulbert parameters).** Let $\gamma = \tfrac12 + \delta$ and $\beta = \tfrac14(1 + \delta)^2$. Then $\lambda_2 = \lambda_3 = (\delta - 1)/(\delta + 1)$. With $\alpha_m = (2\rho_\infty - 1)/(\rho_\infty + 1)$ and $\alpha_f = \rho_\infty/(\rho_\infty + 1)$, all three eigenvalues of $A_\infty$ equal $-\rho_\infty$, so the spectral radius of $A(\Omega)$ tends to $\rho_\infty$.

*Proof.* The trace is $2 - (1 + \delta)/\beta = 2 - 4/(1 + \delta)$ and the determinant is $1 - \delta/\beta = 1 - 4\delta/(1 + \delta)^2 = \big((1 - \delta)/(1 + \delta)\big)^2$. A pair with sum $2\mu$ and product $\mu^2$, $\mu = 1 - 2/(1 + \delta) = (\delta - 1)/(\delta + 1)$, is the double root $\mu$. Now $\delta = \alpha_f - \alpha_m = (1 - \rho_\infty)/(1 + \rho_\infty)$, so $\mu = \big((1 - \rho_\infty) - (1 + \rho_\infty)\big)/\big((1 - \rho_\infty) + (1 + \rho_\infty)\big) = -\rho_\infty$, and $\lambda_1 = -\alpha_f/(1 - \alpha_f) = -\rho_\infty$. The eigenvalues of a matrix depend continuously on its entries, so the spectral radius of $A(\Omega)$ converges to that of $A_\infty$. $\square$

The parameter $\beta$ of the corollary is the one that makes the two roots of $B$ equal. For a larger $\beta$ the pair is complex with modulus $\sqrt{1 - \delta/\beta}$, which is larger than $|\mu|$, so a larger $\beta$ damps the highest modes less.

**Theorem 4 (unconditional stability, cited).** For a linear undamped problem the method is unconditionally stable when $\alpha_m \le \alpha_f \le \tfrac12$ and $\beta \ge \tfrac14 + \tfrac12(\alpha_f - \alpha_m)$ (Chung and Hulbert 1993). The Chung-Hulbert parameters satisfy these conditions: $\alpha_f - \alpha_m = (1 - \rho_\infty)/(1 + \rho_\infty) \ge 0$, $\alpha_f = \rho_\infty/(\rho_\infty + 1) \le \tfrac12$, and $\tfrac14(1 + \delta)^2 - \tfrac14 - \tfrac12\delta = \tfrac14\delta^2 \ge 0$. The reference test `test_unconditional_stability` measures a spectral radius at most $1 + 10^{-6}$ for $\rho_\infty \in \{0, 0.3, 0.6, 0.9, 1\}$ and $\omega\,dt$ from $10^{-2}$ to $10^3$.

**Theorem 5 (the case $\rho_\infty = 1$).** For $\rho_\infty = 1$, $\alpha_m = \alpha_f = \tfrac12$, $\gamma = \tfrac12$ and $\beta = \tfrac14$. If the load $F$ is affine in $t$ (for example zero), the method produces the same $(d_k, v_k, a_k)$ as the average acceleration Newmark method, and $M a_k + C v_k + K d_k = F(t_k)$ for every $k$.

*Proof.* By induction on $k$. For $k = 0$ the equation holds by line L1. If it holds at $k$, then (B) with $\alpha_m = \alpha_f = \tfrac12$ says that the mean of $M a + C v + K d$ at $k$ and $k + 1$ equals $F(t_k + \tfrac12 dt)$, which is the mean of $F(t_k)$ and $F(t_{k+1})$ because $F$ is affine. So the equation holds at $k + 1$. Then (U1), (U2) and the equation at $k + 1$ are the defining equations of the Newmark step with $\beta = \tfrac14$, $\gamma = \tfrac12$, which has a unique solution. $\square$

So for $\rho_\infty = 1$ and a linear undamped problem the energy $\tfrac12 v^\top M v + \tfrac12 d^\top K d$ is conserved exactly, by the energy theorem of the [Newmark-beta method](/newmark-beta-method/). The reference test `test_rho_one_is_the_trapezoidal_rule` checks both facts in exact rational arithmetic.
