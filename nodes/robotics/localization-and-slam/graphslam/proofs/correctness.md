---
title: One GraphSLAM iteration is a Gauss-Newton step, and its fixed points are stationary points of the full SLAM cost
proves: [correctness]
status: full
---

**Setting.** The state is $y = (x_0, \dots, x_T, m_1, \dots, m_M)$. The cost is

$$J(y) = \tfrac{1}{2} x_0^\top \Omega_0\, x_0 + \tfrac{1}{2} \sum_{t=1}^{T} r_t^\top R^{-1} r_t + \tfrac{1}{2} \sum_{i} s_i^\top Q^{-1} s_i,$$

with the motion residuals $r_t = x_t - g(u_t, x_{t-1})$ and the measurement residuals $s_i = z_i - h(x_{t_i}, m_{j_i})$. $R$ and $Q$ are symmetric positive definite, and $\Omega_0 = \alpha I$ with $\alpha > 0$ is the anchor. $g$ and $h$ are differentiable. The angle parts of the residuals are wrapped to $[-\pi, \pi)$; near a point where no residual angle is at $\pm\pi$, the wrap adds a constant multiple of $2\pi$ and does not change the derivatives.

**Assumptions.**

- (A1) Every landmark has at least one measurement, and every block $\Omega_{jj}$ built by LINEARIZE is invertible. (A range and bearing measurement at a nonzero range has a $2 \times 2$ landmark Jacobian with determinant $-1/r$, so one measurement is enough.)
- (A2) The matrix $\Omega$ built by LINEARIZE is invertible.

**Claim 1 (linearize).** Let $\mu$ be the current estimate. Replace each residual by its first order expansion at $\mu$: $r_t \approx x_t - G_t x_{t-1} - (\hat x_t - G_t \mu_{t-1})$ with $\hat x_t = g(u_t, \mu_{t-1})$ and $G_t = \partial g / \partial x$, and $s_i \approx z_i - \hat z_i + H_i \mu_{(i)} - H_i y_{(i)}$ with $\hat z_i = h(\mu_{(i)})$ and $H_i = \partial h / \partial (x, m)$. The quadratic $\tilde J(y)$ that results is $\tfrac{1}{2} y^\top \Omega y - \xi^\top y + c$, with the $\Omega$ and $\xi$ of lines L2 to L6.

*Proof.* Each linearized residual is affine. Up to its sign, which does not change its square, it has the form $C y - b$, where $C$ is zero outside the variables of one factor. Then $\tfrac{1}{2}(C y - b)^\top W (C y - b) = \tfrac{1}{2} y^\top C^\top W C\, y - (C^\top W b)^\top y + c$. For a motion factor, $C = [-G_t \;\; I]$ on $(x_{t-1}, x_t)$ and $b = \hat x_t - G_t \mu_{t-1}$, so the terms are $C^\top R^{-1} C$ and $C^\top R^{-1} b$, which line L4 and the line after it add. For a measurement factor, $s_i \approx -(H_i y_{(i)} - b_i)$ with $b_i = z_i - \hat z_i + H_i \mu_{(i)}$, so $C = H_i$ on $(x_{t_i}, m_{j_i})$, and the terms are $H_i^\top Q^{-1} H_i$ and $H_i^\top Q^{-1} b_i$, which line L6 and the line after it add. The anchor gives $\alpha I$ on $x_0$ and no term in $\xi$, because its target is $0$. Summing over the factors gives $\Omega$ and $\xi$. $\square$

Since $\Omega$ is invertible and $\tilde J$ is a convex quadratic (a sum of squares), its unique minimizer is $y^* = \Omega^{-1} \xi$.

**Claim 2 (reduce and solve).** Order $y = (x, m)$ with $x$ the poses. Lines L7 to L14 return exactly $y^* = \Omega^{-1} \xi$, and the returned $\Sigma$ is the pose block of $\Omega^{-1}$.

*Proof.* No factor joins two landmarks, so $\Omega_{mm}$ is block diagonal with the blocks $\Omega_{jj}$. Hence $\Omega_{mm}^{-1} = \mathrm{diag}(\Omega_{jj}^{-1})$, and

$$\Omega_{xm} \Omega_{mm}^{-1} \Omega_{mx} = \sum_j \Omega_{x j} \Omega_{jj}^{-1} \Omega_{j x}, \qquad \Omega_{xm} \Omega_{mm}^{-1} \xi_m = \sum_j \Omega_{x j} \Omega_{jj}^{-1} \xi_j.$$

The column block $\Omega_{xj}$ is zero outside the poses in $\tau(j)$, the poses that measured $m_j$, so each term changes only the rows and columns of $\tau(j)$. Lines L8 to L10 subtract exactly these terms, so $\tilde\Omega = \Omega_{xx} - \Omega_{xm}\Omega_{mm}^{-1}\Omega_{mx}$ and $\tilde\xi = \xi_x - \Omega_{xm}\Omega_{mm}^{-1}\xi_m$. Write the system $\Omega y = \xi$ in blocks:

$$\Omega_{xx} x + \Omega_{xm} m = \xi_x, \qquad \Omega_{mx} x + \Omega_{mm} m = \xi_m.$$

The second equation gives $m = \Omega_{mm}^{-1}(\xi_m - \Omega_{mx} x)$. Put it in the first: $\tilde\Omega x = \tilde\xi$. $\tilde\Omega$ is the [Schur complement](/schur-complement/) of $\Omega_{mm}$ in $\Omega$, and $\det \Omega = \det \Omega_{mm} \det \tilde\Omega$, so $\tilde\Omega$ is invertible by (A1) and (A2). Lines L11 and L12 give $x = \tilde\Omega^{-1} \tilde\xi$, the pose part of $y^*$. Since $\Omega_{mm}$ is block diagonal, the landmark equation splits into $m_j = \Omega_{jj}^{-1} (\xi_j - \Omega_{j\tau(j)} x_{\tau(j)})$, which is line L14. The block inverse formula gives $(\Omega^{-1})_{xx} = \tilde\Omega^{-1}$, which is $\Sigma$. $\square$

**Claim 3 (the iteration).** Lines L16 to L19 are Gauss-Newton on $J$. If the iteration reaches a fixed point $\mu = \mu'$, then $\nabla J(\mu) = 0$.

*Proof.* By Claims 1 and 2, the new estimate minimizes the quadratic model $\tilde J$ built at $\mu$. Write $\tilde J$ in the step $\delta = y - \mu$: each residual is $e(\mu) + D \delta$, with $e(\mu)$ the residual at $\mu$ and $D$ its Jacobian at $\mu$, and $\tilde J = \tfrac{1}{2} \sum (e + D\delta)^\top W (e + D\delta)$. This is the Gauss-Newton model of $J$, so the step is the Gauss-Newton step. The gradient of $\tilde J$ at $\delta = 0$ is $\sum D^\top W e$, which is $\nabla J(\mu)$ by the chain rule. At a fixed point the minimizer of $\tilde J$ is $\delta = 0$, so the gradient of $\tilde J$ at $\delta = 0$ is zero, and so $\nabla J(\mu) = 0$. $\square$

**Exact data.** If the controls and measurements have no noise, the true path and map $y^\dagger$ (with $x_0 = 0$) make every residual zero, so $J(y^\dagger) = 0$, the global minimum. At $y^\dagger$ the gradient is zero, so $y^\dagger$ is a fixed point. INITIALIZE composes the exact controls, so it starts at the true path; the landmark from the first measurement is exact as well. The first iteration then returns $y^\dagger$ again. The test checks this to $10^{-9}$.

**What this does not show.** Gauss-Newton converges only from a start close enough to a minimum, and the cost is not convex, so the fixed point can be a local minimum. The proof says nothing about the number of iterations. The anchor $\alpha$ is finite in the code, so $x_0$ is close to, not equal to, the initial guess.
