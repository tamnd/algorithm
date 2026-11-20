---
title: Order, linear stability and energy of the Newmark-beta method
proves: [correctness]
status: partial
---

**Setting.** $M$ is symmetric positive definite, $K$ is symmetric and $\beta \ge 0$, so that $M + \gamma\,dt\,C + \beta\,dt^2 K$ is invertible for the problems below. Lines L1 to L7 give, for every $k \ge 0$,

$$\text{(U1)}\quad d_{k+1} = d_k + dt\,v_k + dt^2\big((\tfrac12 - \beta) a_k + \beta a_{k+1}\big), \qquad \text{(U2)}\quad v_{k+1} = v_k + dt\big((1 - \gamma) a_k + \gamma a_{k+1}\big),$$

and $M a_k + C v_k + K d_k = F(t_k)$. Indeed line L6 gives $d_{k+1} = \tilde d + \beta\,dt^2 a_{k+1}$ with $\tilde d$ from line L3, and line L7 gives $v_{k+1} = \tilde v + \gamma\,dt\,a_{k+1}$ with $\tilde v$ from line L4. The system of line L5 is $M a_{k+1} + C v_{k+1} + K d_{k+1} = F(t_{k+1})$ written with these two expressions. Line L1 gives the equation at $k = 0$. The status is partial because Theorem 9 cites, and does not prove, the convergence of the members other than the average acceleration rule.

**Lemma 1 (two-step form).** For every $k \ge 1$, whatever the equation of motion,

$$d_{k+1} - 2 d_k + d_{k-1} = dt^2\big(\beta a_{k+1} + (\tfrac12 - 2\beta + \gamma) a_k + (\tfrac12 + \beta - \gamma) a_{k-1}\big).$$

*Proof.* Subtract (U1) for the step from $k - 1$ to $k$ from (U1) for the step from $k$ to $k + 1$. This gives $d_{k+1} - 2d_k + d_{k-1} = dt\,(v_k - v_{k-1}) + dt^2\big((\tfrac12 - \beta)(a_k - a_{k-1}) + \beta(a_{k+1} - a_k)\big)$. By (U2), $v_k - v_{k-1} = dt\big((1 - \gamma) a_{k-1} + \gamma a_k\big)$. Collect the terms: $a_{k+1}$ has the coefficient $\beta$, $a_k$ has $\gamma + \tfrac12 - \beta - \beta$, and $a_{k-1}$ has $1 - \gamma - \tfrac12 + \beta$. $\square$

*Corollary (central difference).* For $\beta = 0$ and $\gamma = \tfrac12$, Lemma 1 reads $d_{k+1} - 2d_k + d_{k-1} = dt^2 a_k$. With $C = 0$ and $M a_k = F(t_k) - f_{\rm int}(d_k)$ this is the central difference method $M(d_{k+1} - 2d_k + d_{k-1})/dt^2 + f_{\rm int}(d_k) = F(t_k)$, also for a nonlinear $f_{\rm int}$.

**Lemma 2 (modal reduction).** Let $C = 0$ and $F = 0$, and let $K$ be positive semidefinite. Let $\Phi$ be the matrix of generalized eigenvectors, $K\Phi = M\Phi\,\mathrm{diag}(\omega_i^2)$ with $\Phi^\top M \Phi = I$. Write $d_k = \Phi q_k$, $v_k = \Phi p_k$ and $a_k = \Phi r_k$. Then each component $(q_{k,i}, p_{k,i}, r_{k,i})$ is the Newmark sequence of the scalar problem $\ddot q + \omega_i^2 q = 0$ with the same $dt$, $\beta$ and $\gamma$.

*Proof.* $\Phi$ is invertible, and (U1) and (U2) are linear with scalar coefficients, so they hold for $q$, $p$ and $r$ in place of $d$, $v$ and $a$. Multiply $M a_k + K d_k = 0$ by $\Phi^\top$: $\Phi^\top M \Phi r_k + \Phi^\top K \Phi q_k = r_k + \mathrm{diag}(\omega_i^2) q_k = 0$. So $r_{k,i} = -\omega_i^2 q_{k,i}$, which is the scalar equation of motion. $\square$

So the sequence $(d_k, v_k)$ is bounded for all initial data exactly when each scalar mode is bounded for all initial data.

**Lemma 3 (scalar step and its eigenvalues).** For $\ddot d + \omega^2 d = 0$ put $\Omega = \omega\,dt$ and $D = 1 + \beta\Omega^2 > 0$. The step is a linear map $x_{k+1} = A x_k$ of $x_k = (d_k, dt\,v_k)$. Its eigenvalues are the roots of

$$p(\lambda) = \lambda^2 + b\lambda + c, \qquad b = -\frac{2 - (\tfrac12 - 2\beta + \gamma)\Omega^2}{D}, \qquad c = \frac{1 + (\tfrac12 + \beta - \gamma)\Omega^2}{D}.$$

*Proof.* With $a_k = -\omega^2 d_k$, Lemma 1 becomes $D d_{k+1} - \big(2 - (\tfrac12 - 2\beta + \gamma)\Omega^2\big) d_k + \big(1 + (\tfrac12 + \beta - \gamma)\Omega^2\big) d_{k-1} = 0$, that is $d_{k+1} + b\,d_k + c\,d_{k-1} = 0$ for $k \ge 1$. Put $y_k = (d_k, d_{k+1})$. Then $y_{k+1} = P y_k$ for all $k \ge 0$, where $P$ is the companion matrix of $p$, with rows $(0, 1)$ and $(-c, -b)$. By (U1) with $a = -\omega^2 d$, $D d_{k+1} = (1 - (\tfrac12 - \beta)\Omega^2) d_k + dt\,v_k$, so $y_k = T x_k$ with $T$ lower triangular with diagonal entries $1$ and $1/D$, so $T$ is invertible. Since every $x_0$ is a possible initial value, $T A x = P T x$ for all $x$, and $A = T^{-1} P T$ has the same eigenvalues as $P$, the roots of $p$. $\square$

**Lemma 4 (roots in the unit disk).** Let $b$ and $c$ be real. Both roots of $\lambda^2 + b\lambda + c$ have modulus at most 1 exactly when $|c| \le 1$ and $|b| \le 1 + c$.

*Proof.* If the roots are not real, they are conjugate, $|\lambda|^2 = c$, and $b^2 < 4c$. Then $c > 0$ and $|b| < 2\sqrt c \le 1 + c$, so the condition holds exactly when $c \le 1$, which is exactly when $|\lambda| \le 1$. If the roots $\lambda_1 \le \lambda_2$ are real, then $p(1) = 1 + b + c = (1 - \lambda_1)(1 - \lambda_2)$, $p(-1) = 1 - b + c = (1 + \lambda_1)(1 + \lambda_2)$ and $c = \lambda_1\lambda_2$. If both roots are in $[-1, 1]$, all three facts give $p(\pm1) \ge 0$ and $|c| \le 1$, and $p(\pm 1) \ge 0$ is $|b| \le 1 + c$. Conversely let $p(\pm 1) \ge 0$ and $|c| \le 1$. If $\lambda_2 > 1$, then $p(1) \ge 0$ forces $\lambda_1 \ge 1$, and $c = \lambda_1 \lambda_2 > 1$, a contradiction. If $\lambda_1 < -1$, then $p(-1) \ge 0$ forces $\lambda_2 \le -1$ and again $c > 1$. $\square$

**Theorem 5 (linear stability).** Let $\Omega > 0$. The scalar sequence $x_k$ is bounded for all initial data exactly when $\gamma \ge \tfrac12$ and either $2\beta \ge \gamma$, or $\Omega^2 \le 2/(\gamma - 2\beta)$ with strict inequality when $\gamma = \tfrac12$.

*Proof.* A direct computation from Lemma 3 gives

$$p(1) = \frac{\Omega^2}{D}, \qquad p(-1) = \frac{4 + (4\beta - 2\gamma)\Omega^2}{D}, \qquad 1 - c = \frac{(\gamma - \tfrac12)\Omega^2}{D}, \qquad 1 + c = \frac{p(1) + p(-1)}{2}.$$

The powers $A^k$ stay bounded exactly when the roots of $p$ are in the closed unit disk and a root of modulus 1 is not a double root, because a $2 \times 2$ matrix with a double eigenvalue $\lambda$ is either $\lambda I$ or similar to a Jordan block, and $A = T^{-1} P T$ is not $\lambda I$ (the companion matrix $P$ has the entry $1$ off the diagonal).

By Lemma 4 the roots are in the closed disk exactly when $c \le 1$, $1 + c \ge 0$ and $p(\pm 1) \ge 0$. Here $p(1) > 0$ always. The condition $c \le 1$ is $\gamma \ge \tfrac12$. The condition $p(-1) \ge 0$ is $2\beta \ge \gamma$ or $\Omega^2 \le 2/(\gamma - 2\beta)$. It implies $1 + c \ge 0$ by the last identity.

Double roots on the circle: a double root $1$ needs $p(1) = 0$, which is impossible for $\Omega > 0$. A double root $-1$ needs $p(-1) = 0$ and $c = 1$. If $p(-1) = 0$, then $1 + c = \Omega^2/(2D)$, and $c = 1$ means $\Omega^2(1 - 4\beta) = 4$. With $\Omega^2 = 2/(\gamma - 2\beta)$ this is $2 - 8\beta = 4\gamma - 8\beta$, that is $\gamma = \tfrac12$. Non-real roots are distinct. So the only bad case inside the closed disk is $\gamma = \tfrac12$ with $\Omega^2 = 2/(\gamma - 2\beta)$. $\square$

*Corollaries.* For $C = 0$, by Lemma 2 the full system is stable for every $dt$ when $2\beta \ge \gamma \ge \tfrac12$, and otherwise (for $\gamma \ge \tfrac12$) when $\omega_{\max} dt < (\gamma/2 - \beta)^{-1/2}$. This limit is $2$ for $\beta = 0$, $\sqrt 6$ for $\beta = \tfrac1{12}$ and $\sqrt{12}$ for $\beta = \tfrac16$, all with $\gamma = \tfrac12$. For $\gamma > \tfrac12$ and $\beta = \tfrac14(\gamma + \tfrac12)^2$ we have $2\beta - \gamma = \tfrac12(\gamma - \tfrac12)^2 \ge 0$, so the damped member is unconditionally stable. For a rigid body mode, $\Omega = 0$, $p(\lambda) = (\lambda - 1)^2$ and $d_k = d_0 + k\,dt\,v_0$, which is the exact free motion.

*Phase of the average acceleration rule.* For $\beta = \tfrac14$ and $\gamma = \tfrac12$, $c = 1$ and $-b/2 = (1 - \Omega^2/4)/(1 + \Omega^2/4)$. With $\varphi = \arctan(\Omega/2)$ this is $(1 - \tan^2\varphi)/(1 + \tan^2\varphi) = \cos 2\varphi$, so the roots are $e^{\pm 2 i \varphi}$: modulus 1 and the angle $2\arctan(\Omega/2)$ per step in place of the exact $\Omega$.

**Lemma 6 (consistency).** Let $d$ be a smooth exact solution with $a = \ddot d$. Define the defects $\tau^v_k = v(t_{k+1}) - v(t_k) - dt\big((1 - \gamma)a(t_k) + \gamma a(t_{k+1})\big)$ and $\tau^d_k = d(t_{k+1}) - d(t_k) - dt\,v(t_k) - dt^2\big((\tfrac12 - \beta)a(t_k) + \beta a(t_{k+1})\big)$. Then

$$\tau^v_k = (\tfrac12 - \gamma)\,dt^2\,\dot a(t_k) + O(dt^3), \qquad \tau^d_k = (\tfrac16 - \beta)\,dt^3\,\dot a(t_k) + O(dt^4).$$

*Proof.* Insert the Taylor expansions $v(t + dt) = v + dt\,a + \tfrac12 dt^2 \dot a + O(dt^3)$, $a(t + dt) = a + dt\,\dot a + O(dt^2)$ and $d(t + dt) = d + dt\,v + \tfrac12 dt^2 a + \tfrac16 dt^3 \dot a + O(dt^4)$. In $\tau^v$ the terms in $dt\,a$ cancel and $\tfrac12 dt^2\dot a - \gamma\,dt^2 \dot a$ remains. In $\tau^d$ the terms in $dt\,v$ and $dt^2 a$ cancel and $\tfrac16 dt^3 \dot a - \beta\,dt^3\dot a$ remains. $\square$

So the defect per unit time, $\tau/dt$, is $O(dt)$ for $\gamma \ne \tfrac12$ (its leading term is not zero when $\dot a \ne 0$) and $O(dt^2)$ for $\gamma = \tfrac12$. For $\gamma = \tfrac12$, $\tau^v_k$ is the error of the trapezoidal rule for $\int a$, so $|\tau^v_k| \le \tfrac1{12} dt^3 \max |d^{(4)}|$ for each component, and $|\tau^d_k| \le \tfrac{1}{12} dt^3 \max|d^{(3)}| + \tfrac{1}{6} dt^4 \max|d^{(4)}|$ for $\beta = \tfrac14$.

**Theorem 7 (energy of the average acceleration rule).** Let $\beta = \tfrac14$, $\gamma = \tfrac12$, $C = 0$, $F = 0$ and $K$ symmetric. Then $E_k = \tfrac12 v_k^\top M v_k + \tfrac12 d_k^\top K d_k$ is the same for all $k$, for every $dt > 0$.

*Proof.* (U2) gives $v_{k+1} - v_k = \tfrac{dt}2(a_k + a_{k+1})$, and (U1) then gives $d_{k+1} - d_k = dt\,v_k + \tfrac{dt}{2}(v_{k+1} - v_k) = \tfrac{dt}2(v_k + v_{k+1})$. The equation of motion gives $M(v_{k+1} - v_k) = -\tfrac{dt}2 K(d_k + d_{k+1})$. For a symmetric matrix $S$, $x^\top S x - y^\top S y = (x - y)^\top S (x + y)$. So

$$E_{k+1} - E_k = -\tfrac{dt}{4}(d_k + d_{k+1})^\top K (v_k + v_{k+1}) + \tfrac{dt}{4}(v_k + v_{k+1})^\top K (d_k + d_{k+1}) = 0,$$

because $K$ is symmetric. $\square$

The two relations of the proof are the trapezoidal rule for $\dot d = v$ and $M\dot v = -K d$. With a load and damping the same steps give the trapezoidal rule for $\dot d = v$, $M \dot v = F - C v - K d$. For a nonlinear $f_{\rm int}$ the last step fails, because $f_{\rm int}(d_k) + f_{\rm int}(d_{k+1})$ is not a gradient difference, and the energy is not conserved (the reference test `test_nonlinear_energy_is_not_exact` measures a change of more than $10^{-4}$).

*Remark (conserved quadratic form for $\gamma = \tfrac12$).* For $\gamma = \tfrac12$ the scalar recurrence of Lemma 3 has $c = 1$, so it reads $D d_{k+1} - B d_k + D d_{k-1} = 0$ with $B = -bD$. Then $Q_k = D d_{k+1}^2 - B d_{k+1} d_k + D d_k^2$ satisfies $Q_k - Q_{k-1} = (d_{k+1} - d_{k-1})\big(D(d_{k+1} + d_{k-1}) - B d_k\big) = 0$. So every member with $\gamma = \tfrac12$ conserves a quadratic form for linear undamped problems, and by Lemma 2 this holds mode by mode.

**Theorem 8 (second order convergence of the average acceleration rule).** Let $\beta = \tfrac14$, $\gamma = \tfrac12$, $C = 0$, $K$ symmetric positive definite, and let the exact solution have a bounded fourth derivative on $[0, T]$. Start from the exact $d_0$ and $v_0$. Let $e_k = d(t_k) - d_k$ and $f_k = v(t_k) - v_k$. Then for $k\,dt \le T$,

$$\big(f_k^\top M f_k + e_k^\top K e_k\big)^{1/2} \le C_0\,T\,dt^2,$$

where $C_0$ depends on $M$, $K$ and the bounds of the third and fourth derivatives of $d$.

*Proof.* The exact solution satisfies (U1) and (U2) with the defects $\tau^d_k$ and $\tau^v_k$ added, and $M a(t) + K d(t) = F(t)$. Subtract the numerical scheme. The errors satisfy the scheme for $F = 0$ with the defects added: $f_{k+1} - f_k = \tfrac{dt}2(\alpha_k + \alpha_{k+1}) + \tau^v_k$ and $e_{k+1} - e_k = dt\,f_k + \tfrac{dt^2}4(\alpha_k + \alpha_{k+1}) + \tau^d_k$, with $M\alpha_k = -K e_k$. As in Theorem 7, $e_{k+1} - e_k = \tfrac{dt}2(f_k + f_{k+1}) + \rho_k$ with $\rho_k = \tau^d_k - \tfrac{dt}2\tau^v_k$, and $M(f_{k+1} - f_k) = -\tfrac{dt}2 K(e_k + e_{k+1}) + M\tau^v_k$. The same computation as in Theorem 7 gives, for $\mathcal E_k = \tfrac12(f_k^\top M f_k + e_k^\top K e_k)$,

$$\mathcal E_{k+1} - \mathcal E_k = \tfrac12 (\tau^v_k)^\top M (f_k + f_{k+1}) + \tfrac12 \rho_k^\top K (e_k + e_{k+1}).$$

Write $\|x\|_M = (x^\top M x)^{1/2}$, $\|x\|_K = (x^\top K x)^{1/2}$ and $s_k = (2\mathcal E_k)^{1/2}$. By the Cauchy-Schwarz inequality in these inner products, $\|f_k\|_M \le s_k$ and $\|e_k\|_K \le s_k$, so $\tfrac12(s_{k+1}^2 - s_k^2) \le \tfrac12 \delta_k (s_k + s_{k+1})$ with $\delta_k = \|\tau^v_k\|_M + \|\rho_k\|_K$. Divide by $\tfrac12(s_k + s_{k+1})$ (if it is $0$ the claim $s_{k+1} \le s_k + \delta_k$ is trivial) to get $s_{k+1} \le s_k + \delta_k$. With $s_0 = 0$, $s_k \le \sum_{j < k} \delta_j$. By Lemma 6, $\delta_j \le C_0\,dt^3$, and there are $k \le T/dt$ terms. $\square$

**Theorem 9 (convergence of the other members, cited).** For fixed $\beta$ and $\gamma$ in the stable set of Theorem 5, with the inequality strict, a linear problem and a smooth solution, the global error on $[0, T]$ is $O(dt^2)$ for $\gamma = \tfrac12$ and $O(dt)$ for $\gamma > \tfrac12$. This follows from Lemma 6 and a bound on the powers of the step matrix that is uniform in $dt$ (Hughes 2000, Chapter 9). We do not repeat that bound here. The reference tests measure the orders 2 for $\beta \in \{0, \tfrac1{12}, \tfrac16, \tfrac14\}$ and 1 for $\gamma = 0.6$.
