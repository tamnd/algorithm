---
title: The EIF is the EKF in information form
proves: [correctness]
status: full
---

**Setting.** The belief at time $t-1$ is $N(\mu, \Sigma)$ with $\Sigma$ positive definite, stored as $\Omega = \Sigma^{-1}$ and $\xi = \Omega \mu$. The motion is $x_t = g(u_t, x_{t-1}) + w$ with $w \sim N(0, R)$, and the readings are $z^i = h_i(x_t) + v_i$ with $v_i \sim N(0, Q_i)$, $Q_i$ positive definite, all noises independent. The EKF linearizes $g$ at $\mu$ with $G = \partial g / \partial x$, and linearizes each $h_i$ at the predicted mean $\bar\mu$ with $H_i = \partial h_i / \partial x$. We compare the EIF with the EKF that processes all readings of a step in one update at $\bar\mu$.

**Claim.** If $G \Sigma G^\top + R$ is invertible, then after lines L1 to L9 the pair $(\xi, \Omega)$ is the information form of the EKF belief: $\Omega^{-1}$ is the EKF covariance and $\Omega^{-1} \xi$ is the EKF mean. For linear models with Gaussian noise, the EKF is the Kalman filter, so the EIF gives the exact posterior.

## Prediction (lines L1 to L5)

Line L1 computes $\mu = \Omega^{-1} \xi$, the mean of the belief. The EKF prediction is $\bar\mu = g(u_t, \mu)$ and $\bar\Sigma = G \Sigma G^\top + R$ with $\Sigma = \Omega^{-1}$. Line L3 sets $\bar\Omega = \bar\Sigma^{-1}$, line L4 sets $\bar\mu$, and line L5 sets $\bar\xi = \bar\Omega \bar\mu$. This is the information form of $N(\bar\mu, \bar\Sigma)$ by definition.

## One reading (lines L7 to L9)

Let $\bar\Sigma = \bar\Omega^{-1}$, let $H$ and $Q$ be the Jacobian and the noise of the reading, and let $\nu = z - h(\bar\mu)$ (with the angle wrapped, if any). The EKF computes $S = H \bar\Sigma H^\top + Q$, $K = \bar\Sigma H^\top S^{-1}$, $\mu' = \bar\mu + K \nu$ and $\Sigma' = (I - K H) \bar\Sigma$. Lines L8 and L9 compute

$$\Omega' = \bar\Omega + H^\top Q^{-1} H, \qquad \xi' = \bar\xi + H^\top Q^{-1} (\nu + H \bar\mu).$$

$\Omega'$ is positive definite, as the sum of a positive definite and a positive semidefinite matrix.

**The gain.** $\Omega' \bar\Sigma H^\top = H^\top + H^\top Q^{-1} H \bar\Sigma H^\top = H^\top Q^{-1} (Q + H \bar\Sigma H^\top) = H^\top Q^{-1} S$. Multiply by $\Omega'^{-1}$ on the left and by $S^{-1}$ on the right: $K = \bar\Sigma H^\top S^{-1} = \Omega'^{-1} H^\top Q^{-1}$.

**The covariance.** $\bar\Sigma = \Omega'^{-1} \Omega' \bar\Sigma = \Omega'^{-1} (\bar\Omega + H^\top Q^{-1} H) \bar\Sigma = \Omega'^{-1} + \Omega'^{-1} H^\top Q^{-1} H \bar\Sigma = \Omega'^{-1} + K H \bar\Sigma$. So $\Omega'^{-1} = (I - K H) \bar\Sigma = \Sigma'$.

**The mean.** $\Omega'^{-1} \xi' = \Omega'^{-1} (\bar\Omega + H^\top Q^{-1} H) \bar\mu + \Omega'^{-1} H^\top Q^{-1} \nu = \bar\mu + K \nu = \mu'$.

## Several readings

Stack the readings of one step: $H = (H_1; \dots; H_k)$ and $Q = \mathrm{diag}(Q_1, \dots, Q_k)$, all linearized at $\bar\mu$. Then $H^\top Q^{-1} H = \sum_i H_i^\top Q_i^{-1} H_i$ and $H^\top Q^{-1} (\nu + H \bar\mu) = \sum_i H_i^\top Q_i^{-1} (\nu_i + H_i \bar\mu)$. So the loop of line L6, which adds the terms one by one, gives the stacked update of the previous section. Addition is commutative, so the order of the readings does not change the result, up to rounding.

## Locality

If $H$ is zero outside a set $C$ of columns, then $H^\top Q^{-1} H$ is zero outside the rows and columns in $C$, and $H^\top Q^{-1} (\nu + H \bar\mu)$ is zero outside the entries in $C$. So the update changes only the block $C \times C$ of $\Omega$ and the entries $C$ of $\xi$. The code computes only these entries. For a SLAM reading of one landmark, $C$ holds the pose and that landmark.

## A flat prior

Lines L8 and L9 do not need $\bar\Sigma$. They are the product of the prior density $\exp(-\tfrac12 x^\top \bar\Omega x + \bar\xi^\top x)$ and the Gaussian likelihood of the linearized reading, written in the exponent. This product is defined also when $\bar\Omega$ is singular, for example with zero information on a landmark that has not been seen. When the result $\Omega'$ is positive definite, it is the information form of the posterior of the improper prior. The algebra above does not hold in this case, but the claim about the product does, which is all that the later steps use.

## Tests

`test_extended_information_filter.py` runs the EIF and a dense EKF on 12 steps of a planar SLAM problem with range and bearing readings of two landmarks, and checks that the means agree within $10^{-8}$ and the covariances within $10^{-9}$ at every step. It checks locality on a random $\Omega$ (entries outside the block are bit for bit unchanged), the independence of the order, the round trip between the two forms, the numbers of the example of the page, and that a linear run with a flat prior on two landmarks equals the batch least squares solution within $10^{-9}$.
