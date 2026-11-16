---
title: EKF SLAM is the exact Kalman filter of the joint state in the linear case
proves: [correctness]
status: full
---

**Setting.** The joint state is $y = (x, m)$, where $x \in \mathbb{R}^r$ is the robot state and $m = (m_1, \dots, m_n)$ stacks the landmarks that are already in the map, each in $\mathbb{R}^2$. The belief is $N(\mu, \Sigma)$ over $y$. We prove the claims for the *linear Gaussian SLAM model*:

- motion: $x_t = F x_{t-1} + B u_t + w_t$ with $w_t \sim N(0, R)$, and the landmarks do not move;
- a reading of landmark $j$: $z = H_x x + H_m m_j + v$ with $v \sim N(0, Q)$ and $H_m$ invertible (a reading fixes the landmark when the robot state is known);
- all noises are independent of each other and of the state, and $\Sigma$, $R$ and $Q$ are symmetric, with $Q$ positive definite.

For the planar models of the page, EKF SLAM applies the same steps to the models linearized at the current mean: $F = G_t$, $R = V_t M_t V_t^\top$, $H_x$ and $H_m$ the Jacobians of the range and bearing, and the inverse model $m_j = f(x, z)$ with Jacobians $G_x$ and $G_z$.

**Claim.** In the linear Gaussian model, if $y \sim N(\mu, \Sigma)$ before a step, then:

1. after lines L2 to L4, $N(\mu, \Sigma)$ is the exact distribution of the joint state after the motion;
2. after line L7 for a new landmark, $N(\mu, \Sigma)$ is the exact posterior over the enlarged state, for a landmark with a flat prior;
3. after lines L8 to L11 for a reading of a known landmark, $N(\mu, \Sigma)$ is the exact posterior given the reading.

So EKF SLAM computes the exact online SLAM posterior $p(x_t, m \mid z_{1:t}, u_{1:t})$ in the linear Gaussian case. For nonlinear models it computes the same quantities for the linearized models, which is an approximation with no general error bound.

*Proof.*

*Part 1, the prediction.* Write the step on the joint state as $y_t = A y_{t-1} + (B u_t, 0) + (w_t, 0)$ with $A = \begin{pmatrix} F & 0 \\ 0 & I \end{pmatrix}$, because the landmarks do not move. An affine image of a Gaussian vector plus an independent Gaussian vector is Gaussian, with mean $A \mu + (B u_t, 0)$ and covariance $A \Sigma A^\top + \mathrm{diag}(R, 0)$. In blocks,

$$A \Sigma A^\top + \mathrm{diag}(R, 0) = \begin{pmatrix} F \Sigma_{xx} F^\top + R & F \Sigma_{xm} \\ \Sigma_{mx} F^\top & \Sigma_{mm} \end{pmatrix}.$$

The mean of $x$ is $F \mu_x + B u_t$ (line L2) and the mean of $m$ does not change. The robot block is line L3, the cross block is line L4, and the map block stays as it is. This proves part 1. The code changes only the first $r$ rows and columns, which costs $O(r^2 n)$ operations, so $O(n)$ for a fixed $r$.

*Part 2, a new landmark.* Let $y$ be the state before the reading, with $y \sim N(\mu, \Sigma)$ given the past data $D$, and let the new landmark $m_{new}$ have a flat prior: its density is constant and it is independent of $y$ before the reading. The reading is $z = H_x x + H_m m_{new} + v$. By Bayes' rule,

$$p(y, m_{new} \mid D, z) \propto p(y \mid D)\, N(z;\ H_x x + H_m m_{new},\ Q).$$

As a function of $m_{new}$ for fixed $y$, the Gaussian factor equals $|\det H_m|^{-1} N(m_{new};\ H_m^{-1}(z - H_x x),\ H_m^{-1} Q H_m^{-\top})$. Its integral over $m_{new}$ is $|\det H_m|^{-1}$, which does not depend on $y$. Hence the marginal of $y$ is still $N(\mu, \Sigma)$: the first reading of a landmark carries no information about the rest of the state. The conditional of $m_{new}$ given $y$ is $N(G_x x + G_z z,\ G_z Q G_z^\top)$ with $G_x = -H_m^{-1} H_x$ and $G_z = H_m^{-1}$, which is the linear inverse model $m_{new} = G_x x + G_z (z - v)$. A Gaussian marginal times a linear Gaussian conditional gives a joint Gaussian with

$$E[m_{new}] = G_x \mu_x + G_z z, \qquad \mathrm{Cov}(m_{new}, y) = G_x \Sigma_{x\cdot}, \qquad \mathrm{Cov}(m_{new}) = G_x \Sigma_{xx} G_x^\top + G_z Q G_z^\top.$$

These are the new mean, the new rows and the new diagonal block that line L7 (the function augment) appends. This proves part 2. The new rows cost $O(r n)$ to compute.

*Part 3, a reading of a known landmark.* The reading of landmark $j$ is $z = H y + v$, where the full Jacobian $H$ has the block $H_x$ in the robot columns, $H_m$ in the columns of $m_j$, and zeros elsewhere. The Kalman update for a linear measurement of a Gaussian state gives the exact posterior (see [the Kalman filter](/kalman-filter/)):

$$S = H \Sigma H^\top + Q, \quad K = \Sigma H^\top S^{-1}, \quad \mu' = \mu + K (z - H \mu), \quad \Sigma' = (I - K H) \Sigma.$$

The code computes the same quantities in a cheaper order. Let $\mathrm{idx}$ be the columns where $H$ is not zero, and $h$ the matrix of those columns. Then $\Sigma H^\top = \Sigma_{:,\mathrm{idx}}\, h^\top$, an $n \times 2$ matrix that costs $O(n)$, and $S = h\, (\Sigma H^\top)_{\mathrm{idx},:} + Q$. Line L9 forms $S^{-1}$ and $K = (\Sigma H^\top) S^{-1}$, and line L10 adds $K \nu$ with $\nu = z - H \mu$. Because $\Sigma$ is symmetric, $K H \Sigma = K (\Sigma H^\top)^\top$, so line L11 computes $\Sigma'_{rc} = \Sigma_{rc} - \sum_a K_{ra} (\Sigma H^\top)_{ca}$, which is $(I - K H)\Sigma$. The matrix $K (\Sigma H^\top)^\top = (\Sigma H^\top) S^{-1} (\Sigma H^\top)^\top$ is symmetric, so the code computes each entry once for $c \ge r$ and copies it. This proves part 3. Every entry of $\Sigma$ changes, which costs $O(n^2)$.

*The whole step.* By induction over the steps and the readings, parts 1 to 3 keep the invariant "$N(\mu, \Sigma)$ is the exact posterior over the robot state and all landmarks seen so far". The readings of one step are independent given the state, so applying them one after the other is the same as one update with all of them stacked. $\square$

**The nonlinear case.** For the planar models, lines L1, L7 and L8 evaluate the Jacobians at the current mean. Parts 1 to 3 then hold for the linearized models, and not for the true ones. The linearization point moves with the estimate, so the filter can believe it has information that it does not have, for example about the heading. Julier and Uhlmann (2001) and Huang and Dissanayake (2007) show that this makes the nonlinear EKF SLAM inconsistent over long runs: the covariance becomes too small compared with the real error. The tests measure the normalized error on short runs only.

**What the tests check.** Part 1: the map block does not change and the cross block is $G \Sigma_{xm}$. Part 2: the new block equals the joint Gaussian of the inverse model. Part 3: the sparse update equals the dense Kalman update within $10^{-12}$. The whole claim: on a linear model with three landmarks, the filter equals the marginal of the batch weighted least squares solution over all poses and landmarks within $10^{-9}$, for the mean and the covariance.
