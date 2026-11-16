---
title: EKF localization is the exact Bayes filter of the linearized models
proves: [correctness]
status: full
---

**Setting.** The state is the pose $x \in \mathbb{R}^3$. One step of EKF localization takes the belief $N(\mu, \Sigma)$, a control $u$ and readings $z^1, \dots, z^k$ with known landmarks $j_1, \dots, j_k$ (line L6 with known correspondences). Let $G = \partial g / \partial x$ and $V = \partial g / \partial u$ at $(u, \mu)$, and let $M$ be the covariance of the control noise. The linearized motion model is

$$x_t = g(u, \mu) + G (x_{t-1} - \mu) + V \varepsilon, \qquad \varepsilon \sim N(0, M).$$

For a reading of landmark $j$ with the current mean $\bar\mu$ and $H = \partial h / \partial x$ at $\bar\mu$, the linearized measurement model is

$$z = h(\bar\mu, j) + H (x_t - \bar\mu) + \delta, \qquad \delta \sim N(0, Q).$$

The noises $\varepsilon$ and $\delta$ of each reading are independent of each other and of the state.

**Assumptions.**

- (A1) $\Sigma$, $Q$ and $M$ are symmetric; $\Sigma$ and $Q$ are positive definite.
- (A2) The bearing innovation is wrapped so that it represents the angle difference in $[-\pi, \pi)$. In the linearized model angles are real numbers, so this assumption only says which real number the code uses.

**Claim.**

1. If $x_{t-1} \sim N(\mu, \Sigma)$, then under the linearized motion model $x_t \sim N(\bar\mu, \bar\Sigma)$ with $\bar\mu$ and $\bar\Sigma$ of lines L3 and L4.
2. If $x_t \sim N(\bar\mu, \bar\Sigma)$, then under the linearized measurement model the posterior $p(x_t \mid z)$ is $N(\mu', \Sigma')$ with $\mu'$ and $\Sigma'$ of lines L7 to L12. Also $\Sigma'^{-1} = \bar\Sigma^{-1} + H^\top Q^{-1} H$ and $\mu' = \bar\mu + \Sigma' H^\top Q^{-1} \nu$, where $\nu = z - h(\bar\mu, j)$.
3. So one step of EKF localization is the exact [Bayes filter](/bayes-filter/) for the models that are linearized at the current mean, with the measurements of one step applied one after the other. For the nonlinear models, the result is an approximation; this proof gives no bound on its error.

*Proof.*

*Part 1.* The map $(x_{t-1}, \varepsilon) \mapsto g(u, \mu) + G (x_{t-1} - \mu) + V \varepsilon$ is affine, and $(x_{t-1}, \varepsilon)$ is jointly Gaussian because the two parts are independent and Gaussian. An affine image of a Gaussian vector is Gaussian. Its mean is $g(u, \mu) + G \cdot 0 + V \cdot 0 = g(u, \mu)$, which is line L3. Because $x_{t-1} - \mu$ and $\varepsilon$ are independent with zero mean, the covariance is $G \Sigma G^\top + V M V^\top$, which is line L4.

*Part 2.* Write $e = x_t - \bar\mu$, so $e \sim N(0, \bar\Sigma)$ and $\nu = H e + \delta$. The pair $(e, \nu)$ is an affine image of the independent Gaussians $(e, \delta)$, so it is jointly Gaussian with

$$\operatorname{Cov}(\nu) = H \bar\Sigma H^\top + Q = S, \qquad \operatorname{Cov}(e, \nu) = \bar\Sigma H^\top.$$

$S$ is positive definite because $Q$ is (A1), so $S^{-1}$ exists. The conditional distribution of one block of a jointly Gaussian vector given the other block is Gaussian with

$$E[e \mid \nu] = \bar\Sigma H^\top S^{-1} \nu = K \nu, \qquad \operatorname{Cov}(e \mid \nu) = \bar\Sigma - \bar\Sigma H^\top S^{-1} H \bar\Sigma = (I - K H) \bar\Sigma.$$

With $K$ from line L10, this gives $\mu' = \bar\mu + K \nu$ (line L11) and $\Sigma' = (I - K H) \bar\Sigma$ (line L12). Lines L7, L8 and L9 compute $h(\bar\mu, j)$, $H$ and $S$, and $\nu$ is the wrapped difference by (A2).

For the information form, let $P = \bar\Sigma^{-1} + H^\top Q^{-1} H$. Then

$$\Sigma' P = \bar\Sigma P - \bar\Sigma H^\top S^{-1} H \bar\Sigma P.$$

Here $\bar\Sigma P = I + \bar\Sigma H^\top Q^{-1} H$ and $H \bar\Sigma P = H + H \bar\Sigma H^\top Q^{-1} H = (Q + H \bar\Sigma H^\top) Q^{-1} H = S Q^{-1} H$. So

$$\Sigma' P = I + \bar\Sigma H^\top Q^{-1} H - \bar\Sigma H^\top S^{-1} S Q^{-1} H = I,$$

and $\Sigma'^{-1} = P$. For the mean, $\Sigma' H^\top Q^{-1} = (I - K H) \bar\Sigma H^\top Q^{-1}$. Since $K S = \bar\Sigma H^\top$,

$$\bar\Sigma H^\top Q^{-1} - K H \bar\Sigma H^\top Q^{-1} = K (S - H \bar\Sigma H^\top) Q^{-1} = K Q Q^{-1} = K.$$

So $\Sigma' H^\top Q^{-1} = K$ and $\mu' = \bar\mu + \Sigma' H^\top Q^{-1} \nu$. The test `test_update_equals_information_form` checks this identity in floating point.

*Part 3.* By Part 1, the prediction of lines L1 to L4 is the exact prediction step of the Bayes filter for the linearized motion model. By Part 2, each pass through lines L7 to L12 is the exact Bayes update for one linearized reading. The readings of one step are independent given the pose, so the posterior after all of them is the product of their likelihoods with the prior, and the Bayes update with several independent readings equals the updates with each reading in turn. The algorithm relinearizes $h$ at the new mean before each reading, so it applies the exact update for a model that changes with the order; for linear $h$ the model does not change and the result is independent of the order. In all cases the step equals the Bayes filter of the linearized models, and the error relative to the nonlinear models comes only from the linearization. $\blacksquare$
