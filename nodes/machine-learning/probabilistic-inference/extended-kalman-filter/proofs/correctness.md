---
title: What the extended Kalman filter computes, and when it is exact
proves: [correctness]
status: full
---

We use the model and the pseudocode of the page: $x_0 \sim \mathcal N(m_0, P_0)$, $x_t = f(x_{t-1}) + q_t$ with $q_t \sim \mathcal N(0, Q)$, $y_t = h(x_t) + r_t$ with $r_t \sim \mathcal N(0, R)$, all noise terms independent, $f$ and $h$ differentiable with Jacobians $F$ and $H$, and $R$ positive definite. The extended Kalman filter (EKF) is not exact in general, so there is no theorem that it returns $p(x_t \mid y_{1:t})$. What we can prove is the following three statements.

**Two facts about Gaussians.** (G1) If $(u, v)$ is jointly Gaussian with means $(a, b)$ and covariance blocks $\Sigma_{uu}, \Sigma_{uv}, \Sigma_{vv}$, and $\Sigma_{vv}$ is invertible, then $u \mid v \sim \mathcal N\bigl(a + \Sigma_{uv}\Sigma_{vv}^{-1}(v - b),\ \Sigma_{uu} - \Sigma_{uv}\Sigma_{vv}^{-1}\Sigma_{vu}\bigr)$. (G2) If $u \sim \mathcal N(\mu, \Sigma)$ and $v = c + G u + e$ with $e \sim \mathcal N(0, \Lambda)$ independent of $u$, then $(u, v)$ is jointly Gaussian with $\mathbb E v = c + G \mu$, $\mathrm{Cov}(v) = G \Sigma G^\top + \Lambda$ and $\mathrm{Cov}(u, v) = \Sigma G^\top$.

**Claim 1 (one step is the exact Bayes step of a linearized model).** Suppose the current estimate is $x_{t-1} \sim \mathcal N(m, P)$. Replace $f$ by its first-order expansion at $m$, $\tilde f(x) = f(m) + F(m)(x - m)$, and $h$ by its expansion at $m^- = f(m)$, $\tilde h(x) = h(m^-) + H(m^-)(x - m^-)$. Then lines L3 to L7 return the exact mean and covariance of $x_t \mid y_t$ in the model $x_t = \tilde f(x_{t-1}) + q_t$, $y_t = \tilde h(x_t) + r_t$.

*Proof.* By (G2) with $c = f(m) - F m$ and $G = F$, the predicted state is $\mathcal N(f(m), F P F^\top + Q)$; this is line L4. By (G2) again, $(x_t, y_t)$ is jointly Gaussian with $\mathbb E y_t = \tilde h(m^-) = h(m^-)$, $\mathrm{Cov}(y_t) = H P^- H^\top + R = S$ and $\mathrm{Cov}(x_t, y_t) = P^- H^\top$. By (G1) the conditional law has mean $m^- + P^- H^\top S^{-1}(y_t - h(m^-))$ and covariance $P^- - P^- H^\top S^{-1} H P^-$. With $K = P^- H^\top S^{-1}$ the covariance is $P^- - K S K^\top$, since $K S K^\top = P^- H^\top S^{-1} S S^{-1} H P^-$. These are lines L6 and L7. $\square$

**Claim 2 (exact for linear models).** If $f(x) = A x$ and $h(x) = H x$, the EKF returns $x_t \mid y_{1:t} \sim \mathcal N(m_t, P_t)$ exactly for every $t$, and its output equals the Kalman filter output.

*Proof.* For affine maps the expansions of Claim 1 are the maps themselves, and the Jacobians are the constants $A$ and $H$. So each EKF step is the exact Bayes step for the true model. By induction on $t$, with the prior as the base case, the input of step $t$ is the exact law of $x_{t-1} \mid y_{1:t-1}$, which is Gaussian, and Claim 1 then gives the exact law of $x_t \mid y_{1:t}$. Lines L3 to L7 with constant $A$ and $H$ are the Kalman filter equations word for word. $\square$

**Claim 3 (the size of the error in the prediction).** Let $x \sim \mathcal N(m, P)$ and let each component $f_i$ be four times continuously differentiable with bounded fourth derivatives. Then
$$\mathbb E f_i(x) = f_i(m) + \tfrac12\, \mathrm{tr}\bigl(\nabla^2 f_i(m)\, P\bigr) + O(\|P\|^{2}),$$
so the EKF predicted mean $f(m)$ misses a bias term of order $\|P\|$.

*Proof.* Expand $f_i$ around $m$ to third order with a fourth-order remainder $\rho_i$. Take expectations. The linear term has mean zero. The quadratic term $\tfrac12 (x - m)^\top \nabla^2 f_i(m) (x - m)$ has mean $\tfrac12 \mathrm{tr}(\nabla^2 f_i(m) P)$. The cubic term has mean zero, because the odd central moments of a Gaussian are zero. The remainder is bounded by a constant times $\|x - m\|^4$, whose mean is $O(\|P\|^2)$. $\square$

For a scalar example, $f(x) = x^2$ gives $\mathbb E f(x) = m^2 + P$, while the EKF predicts $m^2$, and the true variance is $4 m^2 P + 2 P^2$, while the EKF gives $4 m^2 P$. At $m = 0$ the EKF predicts a point mass at $0$ for a random variable with mean $P$ and variance $2P^2$. This is why the EKF has no general guarantee: the error terms it drops can be as large as the quantities it keeps, and over many steps they can make the estimate diverge.

**Cost.** Each step does a constant number of products of $n \times n$, $n \times m$ and $m \times m$ matrices and one $m \times m$ solve, which is $O(n^3 + n^2 m + n m^2 + m^3)$, plus one evaluation each of $f$, $F$, $h$ and $H$. The state at each step takes $O(n^2)$ memory.
