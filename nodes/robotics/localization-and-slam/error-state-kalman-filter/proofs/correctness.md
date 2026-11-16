---
title: The error-state Kalman filter uses the first-order model of the attitude and bias error
proves: [correctness]
status: full
---

**Setting.** The true state is a rotation $R_t = R_{sb}$ (with unit quaternion $q_t$) and a gyro bias $b_t$. The filter keeps a nominal state $(q, b)$ with rotation $R$, and a covariance $P$ of the error state $\delta x = (\delta\theta, \delta b)$, defined by

$$R_t = R \, \operatorname{Exp}(\delta\theta), \qquad b_t = b + \delta b,$$

where $\operatorname{Exp}$ is the exponential map from a rotation vector to $SO(3)$ and $\operatorname{Log}$ is its inverse near the identity. This is the local error of Sola (2017). The right Jacobian $J_r$ of $SO(3)$ is defined by $\operatorname{Exp}(\phi + \epsilon) = \operatorname{Exp}(\phi) \operatorname{Exp}(J_r(\phi) \epsilon + O(|\epsilon|^2))$, and $J_r(\phi) = I - \tfrac{1}{2} [\phi]_\times + O(|\phi|^2)$. For a rotation $Q$, $Q \operatorname{Exp}(\phi) Q^T = \operatorname{Exp}(Q \phi)$.

The models are as follows. Over one sample of length $\delta t$ the gyro reads $\omega_m = \omega + b_t + n$, where $\omega$ is the true body rate, constant over the sample, and $n$ is white with covariance $\sigma_g^2 I$. The truth moves by $R_t^+ = R_t \operatorname{Exp}(\omega \, \delta t)$ and $b_t^+ = b_t + w$ with $w$ white of covariance $\sigma_w^2 \delta t \, I$. A vector sensor reads $y = R_t^T d + v$ for a known unit direction $d$, with $v$ white of covariance $\sigma_v^2 I$.

**Assumptions.**

- (L) The error $\delta x$ and the noise are small enough that terms of second order in them can be dropped. This is the standing assumption of every extended Kalman filter.
- (W) $|(\omega_m - b) \, \delta t|$ is small, so that $J_r((\omega_m - b) \delta t) = I + O(|\omega_m - b| \, \delta t)$.

**Claim.** To first order in $\delta x$ and the noise:

1. Prediction (lines L1 to L4). With $\hat\omega = \omega_m - b$, the nominal step $R^+ = R \operatorname{Exp}(\hat\omega \, \delta t)$, $b^+ = b$ gives $\delta x^+ = F \delta x + \nu$ with
$$F = \begin{pmatrix} \operatorname{Exp}(\hat\omega \, \delta t)^T & -J_r(\hat\omega \, \delta t) \, \delta t \\ 0 & I \end{pmatrix}, \qquad \operatorname{Cov}(\nu) = \operatorname{diag}(\sigma_g^2 \delta t^2 I, \ \sigma_w^2 \delta t \, I),$$
and under (W) the code uses $-I \, \delta t$ for the top right block.
2. Measurement (lines L5 and L6). With $\hat y = R^T d$, $y = \hat y + H \delta x + v$ with $H = ([\hat y]_\times \ \ 0)$.
3. Update (lines L7 to L9). Given the linear model of Claim 2 and a prior $\delta x \sim (0, P)$, the vector $\widehat{\delta x} = K (y - \hat y)$ with $K = P H^T (H P H^T + \sigma_v^2 I)^{-1}$ is the linear minimum mean-square estimate of $\delta x$, and the Joseph form $P^+ = (I - K H) P (I - K H)^T + \sigma_v^2 K K^T$ is the covariance of its error. It is symmetric and positive semidefinite for any $K$.
4. Injection and reset (lines L10 and L11). After $R \leftarrow R \operatorname{Exp}(\widehat{\delta\theta})$ and $b \leftarrow b + \widehat{\delta b}$, the new error is $\delta x' = G (\delta x - \widehat{\delta x})$ with $G = \operatorname{diag}(J_r(\widehat{\delta\theta}), I)$, and $I - [\tfrac{1}{2} \widehat{\delta\theta}]_\times$ equals $J_r(\widehat{\delta\theta})$ up to $O(|\widehat{\delta\theta}|^2)$.

*Proof.*

*Claim 1.* The true rate over the sample is $\omega = \omega_m - b_t - n = \hat\omega - \delta b - n$. So

$$\operatorname{Exp}(\delta\theta^+) = (R^+)^T R_t^+ = \operatorname{Exp}(-\hat\omega \delta t) \operatorname{Exp}(\delta\theta) \operatorname{Exp}(\hat\omega \delta t - (\delta b + n) \delta t).$$

By the definition of $J_r$, the last factor is $\operatorname{Exp}(\hat\omega \delta t) \operatorname{Exp}(-J_r(\hat\omega \delta t)(\delta b + n) \delta t)$ to first order. With $Q = \operatorname{Exp}(-\hat\omega \delta t)$, $Q \operatorname{Exp}(\delta\theta) Q^T = \operatorname{Exp}(Q \delta\theta)$. So $\operatorname{Exp}(\delta\theta^+) = \operatorname{Exp}(Q \delta\theta) \operatorname{Exp}(-J_r (\delta b + n) \delta t)$, and to first order $\delta\theta^+ = Q \delta\theta - J_r \, \delta t \, \delta b - J_r \, \delta t \, n$. The bias error is $\delta b^+ = b_t^+ - b^+ = \delta b + w$. The noise term $J_r \delta t \, n$ has covariance $\sigma_g^2 \delta t^2 J_r J_r^T = \sigma_g^2 \delta t^2 I + O(\delta t^3)$. Lines L3 and L4 apply $P \leftarrow F P F^T + \operatorname{Cov}(\nu)$, which is the covariance of $F \delta x + \nu$ when $\nu$ is independent of $\delta x$. The mean of $\delta x$ stays $0$, so no mean is propagated: the nominal step of line L2 carries it.

*Claim 2.* $R_t^T d = \operatorname{Exp}(\delta\theta)^T R^T d = (I - [\delta\theta]_\times) \hat y + O(|\delta\theta|^2) = \hat y - \delta\theta \times \hat y = \hat y + \hat y \times \delta\theta = \hat y + [\hat y]_\times \delta\theta$. The bias does not enter the measurement.

*Claim 3.* For a zero-mean $\delta x$ with covariance $P$, independent noise $v$, and $y - \hat y = H \delta x + v$, the error of the estimate $K (y - \hat y)$ is $(I - K H) \delta x - K v$. Its covariance is $(I - K H) P (I - K H)^T + \sigma_v^2 K K^T$ for every $K$, which is the Joseph form; as a sum of two matrices of the form $M C M^T$ with $C \succeq 0$, it is symmetric and positive semidefinite. The $K$ that minimizes its trace is $P H^T (H P H^T + \sigma_v^2 I)^{-1}$, by the derivation of the [Kalman filter](/kalman-filter/). $H P H^T + \sigma_v^2 I$ is positive definite when $\sigma_v > 0$, so the inverse exists.

*Claim 4.* After injection, write $\delta\theta = \widehat{\delta\theta} + \epsilon$. The new error $\delta\theta'$ satisfies $\operatorname{Exp}(\delta\theta') = \operatorname{Exp}(\widehat{\delta\theta})^T \operatorname{Exp}(\widehat{\delta\theta} + \epsilon) = \operatorname{Exp}(J_r(\widehat{\delta\theta}) \epsilon + O(|\epsilon|^2))$. So $\delta\theta' = J_r(\widehat{\delta\theta}) (\delta\theta - \widehat{\delta\theta})$ to first order in $\epsilon$. For the bias, $\delta b' = \delta b - \widehat{\delta b}$ exactly. The covariance of $\delta x'$ is $G P^+ G^T$ (line L11), and the mean of $\delta x'$ is $0$ again. $\blacksquare$

**Remarks.**

- The claims are first-order statements. They do not prove that the filter converges or that $P$ matches the true error. Those are measurements in the tests: from 30 degrees of initial error the attitude error fell below 1.5 degrees within 4 s, and the mean of the normalized estimation error squared over 4 runs was between 3 and 12 for a 6-dimensional error.
- The code keeps the quaternion of $R$, multiplies by $q\{\phi\} = (\cos(|\phi|/2), \sin(|\phi|/2) \phi / |\phi|)$ for $\operatorname{Exp}(\phi)$, and renormalizes after each product. This changes nothing in exact arithmetic.
- The test of the prediction Jacobian compares $F$ with finite differences. The rotation block matches to $10^{-8}$; the bias block differs from the finite differences by about $|\hat\omega| \delta t^2 / 2$, which is the term dropped under (W).
