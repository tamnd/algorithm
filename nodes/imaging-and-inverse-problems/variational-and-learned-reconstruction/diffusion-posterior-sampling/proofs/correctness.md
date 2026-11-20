---
title: "Each DPS step is the DDPM step plus the exact gradient of the DPS data term, and for a Gaussian prior the output law is known in closed form and is not the posterior"
proves: [correctness]
status: partial
---

**Setting.** The forward diffusion is $x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1 - \bar\alpha_t}\,\varepsilon$ with $\varepsilon \sim N(0, I)$, for $t = 1, \ldots, N$, where $\bar\alpha_t = \prod_{s \le t}(1 - \beta_s)$, $\alpha_t = 1 - \beta_t$ and $\bar\alpha_0 = 1$. Let $p_t$ be the density of $x_t$. The data are $y = Ax_0 + n$ with $n \sim N(0, \sigma^2 I)$. The score network $s(x, t)$ is a given function; the statements below say what the algorithm does with it, and the exactness results assume $s(x, t) = \nabla\log p_t(x)$.

The status is partial on purpose. DPS does not sample the posterior $p(x_0 \mid y)$, even with the exact score and infinitely many steps; Part 4 shows this on a Gaussian example. What can be proved is that each line computes what it claims to compute.

**Part 1 (Tweedie's formula, Proposition 1 of Chung et al.).** $E[x_0 \mid x_t] = \big(x_t + (1 - \bar\alpha_t)\nabla\log p_t(x_t)\big)/\sqrt{\bar\alpha_t}$.

*Proof.* Write $k(x_t \mid x_0)$ for the density of $N(\sqrt{\bar\alpha_t}x_0, (1 - \bar\alpha_t)I)$. Then $p_t(x_t) = \int k(x_t \mid x_0)p_0(x_0)\,dx_0$ and $\nabla_{x_t}k(x_t \mid x_0) = -\frac{x_t - \sqrt{\bar\alpha_t}x_0}{1 - \bar\alpha_t}k(x_t \mid x_0)$. Differentiating under the integral sign and dividing by $p_t(x_t)$ gives

$$\nabla\log p_t(x_t) = -\frac{x_t - \sqrt{\bar\alpha_t}\,E[x_0 \mid x_t]}{1 - \bar\alpha_t},$$

because $k(x_t \mid x_0)p_0(x_0)/p_t(x_t)$ is the conditional density of $x_0$ given $x_t$. Solving for $E[x_0 \mid x_t]$ gives the formula. So with the exact score, line L4 computes $\hat x_0 = E[x_0 \mid x_t]$.

**Part 2 (the DDPM step).** Given both $x_t$ and $x_0$, the variable $x_{t-1}$ is Gaussian with mean $\frac{\sqrt{\alpha_t}(1 - \bar\alpha_{t-1})}{1 - \bar\alpha_t}x_t + \frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1 - \bar\alpha_t}x_0$ and variance $\tilde\beta_t = \frac{1 - \bar\alpha_{t-1}}{1 - \bar\alpha_t}\beta_t$ (Ho, Jain and Abbeel 2020; it follows from Bayes' rule for two Gaussian factors). Line L5 is a draw from this law with $x_0$ replaced by $\hat x_0$. With the exact score, its mean equals the mean of the true reverse step $E[x_{t-1} \mid x_t]$, since that mean is linear in $x_0$ and $\hat x_0 = E[x_0 \mid x_t]$. Its variance is too small by the term $\big(\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1 - \bar\alpha_t}\big)^2\operatorname{Var}(x_0 \mid x_t)$, which is why the unguided sampler in the tests ends with variance 0.92 instead of 1 for $N = 100$ and 0.99 for $N = 1000$. At $t = 1$, $\bar\alpha_0 = 1$ gives $\tilde\beta_1 = 0$ and a mean of exactly $\hat x_0$; the test `test_schedule_and_last_step` checks this.

The paper writes the noise of this step as $\tilde\sigma_i z$ without a formula for $\tilde\sigma_i$; the code uses $\tilde\beta_t$, the choice of Ho et al.

**Part 3 (the guidance gradient).** Let $\hat x_0(x) = \big(x + (1 - \bar\alpha_t)s(x, t)\big)/\sqrt{\bar\alpha_t}$ and $\phi(x) = \|y - A\hat x_0(x)\|^2$. If $s(\cdot, t)$ is differentiable with Jacobian $J$, then

$$\nabla\phi(x) = \frac{2}{\sqrt{\bar\alpha_t}}\big(I + (1 - \bar\alpha_t)J^T\big)A^T\big(A\hat x_0(x) - y\big).$$

*Proof.* The Jacobian of $\hat x_0$ is $(I + (1 - \bar\alpha_t)J)/\sqrt{\bar\alpha_t}$, and the chain rule for $\|A\hat x_0 - y\|^2$ gives twice its transpose applied to $A^T(A\hat x_0 - y)$. The code computes $u = A^T r$ once and $J^Tu$ by one call of the given vector-Jacobian product, so line L6 is this formula; the test compares it with central differences for a nonlinear score. Line L8 subtracts $\zeta_t\nabla\phi$, with $\zeta_t = \zeta'/\|y - A\hat x_0\|$ in the normalized form of Algorithm 1 of Chung et al.

**Why this is the DPS approximation.** By Bayes' rule $\nabla\log p_t(x_t \mid y) = \nabla\log p_t(x_t) + \nabla\log p(y \mid x_t)$, and $p(y \mid x_t) = E[p(y \mid x_0) \mid x_t]$. DPS replaces this by $p(y \mid \hat x_0) = p(y \mid E[x_0 \mid x_t])$, so it moves the expectation inside a nonlinear function. For Gaussian noise $\nabla\log p(y \mid \hat x_0(x_t)) = -\frac{1}{2\sigma^2}\nabla\phi(x_t)$. In a reverse step of length $\beta_t$ the score enters with the factor $\beta_t/\sqrt{\alpha_t}$, so the step $\zeta_t = \beta_t/(2\sigma^2\sqrt{\alpha_t})$ follows the approximate posterior score; the normalized step of the paper is a tuned replacement. Theorem 1 of Chung et al. bounds the error of the swap, the Jensen gap, by a constant times the posterior mean absolute deviation $\int\|x_0 - \hat x_0\|p(x_0 \mid x_t)\,dx_0$. This deviation is large at large $t$, so the bound does not make the method exact.

**Part 4 (closed form for a Gaussian prior, and the gap).** Let $x_0 \sim N(0, v_0)$ in one dimension, $A = a$ a scalar, and the steps $\zeta_t$ not normalized. Then $p_t = N(0, \bar\alpha_tv_0 + 1 - \bar\alpha_t)$, the exact score is $-x/v_t$ with $v_t = \bar\alpha_tv_0 + 1 - \bar\alpha_t$, and $\hat x_0 = c_tx_t$ with $c_t = \sqrt{\bar\alpha_t}v_0/v_t$. Line L6 gives $2c_ta(ac_tx_t - y)$, so a whole step is

$$x_{t-1} = k_tx_t + b_t + \sqrt{\tilde\beta_t}\,z_t,\qquad k_t = \tfrac{\sqrt{\alpha_t}(1 - \bar\alpha_{t-1})}{1 - \bar\alpha_t} + \tfrac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1 - \bar\alpha_t}c_t - 2\zeta_tc_t^2a^2,\qquad b_t = 2\zeta_tc_tay.$$

By induction from $x_N \sim N(0, 1)$, every $x_t$ is Gaussian, with the mean $\mu_{t-1} = k_t\mu_t + b_t$ and the variance $V_{t-1} = k_t^2V_t + \tilde\beta_t$. The function `linear_dps_moments` computes this recursion, and the test draws 1500 samples from the code and checks that the sample mean and variance agree with it within 4 and 5 standard errors.

Now take $v_0 = 1$, $a = 1$, $\sigma^2 = 0.25$ and $y = 1$. The posterior is $N(0.8, 0.2)$. With the DDPM schedule ($N = 1000$, $\beta$ from $10^{-4}$ to $0.02$) and $\zeta_t = \beta_t/(2\sigma^2\sqrt{\alpha_t})$, the recursion gives the output law $N(0.98197, 0.12167)$. The exact likelihood here is $p(y \mid x_t) = N(y;\ c_tx_t,\ \sigma^2 + 1 - \bar\alpha_t)$, since $\operatorname{Var}(x_0 \mid x_t) = 1 - \bar\alpha_t$ for $v_0 = 1$. Using its gradient instead, that is $\zeta_t = \beta_t/(2(\sigma^2 + 1 - \bar\alpha_t)\sqrt{\alpha_t})$, gives $N(0.79999, 0.19657)$, close to the posterior. The difference between the two is exactly the term $\operatorname{Var}(x_0 \mid x_t)$ that the swap $p(y \mid x_t) \approx p(y \mid \hat x_0)$ drops. So, even with the exact score, DPS with the natural step trusts the data too much: its mean is near $y$ and its variance is about 0.6 of the posterior variance. This is a theorem about this example, computed in closed form, not a measurement.
