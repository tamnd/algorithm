---
title: On SE(2) with odometry and position fixes, the invariant error propagates exactly and the gain does not depend on the estimate
proves: [correctness]
status: full
---

**Setting.** A pose is an element $\chi = (R, p)$ of the [special Euclidean group](/special-euclidean-group/) $SE(2)$, written as the $3 \times 3$ matrix $\begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix}$ with $R$ a planar rotation. A tangent vector is $\xi = (\xi_\theta, \xi_x, \xi_y)$, and $\exp$ is the matrix exponential of $\begin{pmatrix} 0 & -\xi_\theta & \xi_x \\ \xi_\theta & 0 & \xi_y \\ 0 & 0 & 0 \end{pmatrix}$. In closed form, $\exp(\xi) = (R(\xi_\theta), V(\xi_\theta) (\xi_x, \xi_y))$ with $V(t) = \frac{1}{t} \begin{pmatrix} \sin t & -(1 - \cos t) \\ 1 - \cos t & \sin t \end{pmatrix}$ and $V(0) = I$. The adjoint of $\chi$ is the $3 \times 3$ matrix $\operatorname{Ad}_\chi$ with $\chi \exp(\xi) \chi^{-1} = \exp(\operatorname{Ad}_\chi \xi)$ for all $\xi$.

The models are as follows. The robot moves by $\chi_{k+1} = \chi_k \exp(u_k)$, where $u_k$ is the body twist over one step. Odometry reads $u_m = u + n$ with $n \sim (0, Q)$. A position sensor reads $Y = p + V$ with $V \sim (0, N)$. The filter keeps $\hat\chi$ and $P$, and its error is

$$e = \hat\chi^{-1} \chi = \exp(\xi), \qquad \text{so } \chi = \hat\chi \exp(\xi).$$

This $e$ is the inverse of the left-invariant error $\eta^L = \chi^{-1} \hat\chi$ of Barrau and Bonnabel (2017); the two carry the same information.

**Assumptions.**

- (X) For Claim 1: odometry is exact, $u_m = u$.
- (L) For Claims 2 and 3: terms of second order in $\xi$ and in the noise are dropped, as in every extended Kalman filter.

**Claim.**

1. Exact propagation (lines L1 to L3). If $\hat\chi^+ = \hat\chi \exp(u_m)$ and $u_m = u$, then $\xi^+ = \operatorname{Ad}_{\exp(-u_m)} \xi$ for every $\xi$, of any size, and whatever $\hat\chi$ is. With odometry noise, $\xi^+ = F \xi - J n$ to first order, where $F = \operatorname{Ad}_{\exp(-u_m)}$ and $J = I + O(|u_m|)$.
2. Measurement (lines L4 and L5). The innovation $z = $ the first two entries of $\hat\chi^{-1} (Y, 1)$ satisfies $z = H \xi + \hat R^T V$ to first order, with the constant matrix $H = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$. The noise $\hat R^T V$ has covariance $\hat N = \hat R^T N \hat R$, which equals $N$ when $N = s^2 I$.
3. Update (lines L6 to L8). After $\hat\chi \leftarrow \hat\chi \exp(K z)$, the new error is $\xi' = (I - K H) \xi - K \hat R^T V$ to first order, so the Joseph form gives its covariance for any $K$.
4. Independence. If $N = s^2 I$, the sequences $P_k$ and $K_k$ depend only on $P_0$, $Q$, $N$ and the odometry readings $u_{m,k}$, not on the estimates $\hat\chi_k$ or on the position readings.

*Proof.*

*Claim 1.* From $\chi^+ = \chi \exp(u)$ and $\hat\chi^+ = \hat\chi \exp(u_m)$ with $u = u_m$,

$$e^+ = (\hat\chi^+)^{-1} \chi^+ = \exp(-u_m) \, \hat\chi^{-1} \chi \, \exp(u_m) = \exp(-u_m) \exp(\xi) \exp(-u_m)^{-1} = \exp(\operatorname{Ad}_{\exp(-u_m)} \xi).$$

No term was dropped, so $\xi^+ = \operatorname{Ad}_{\exp(-u_m)} \xi$ holds exactly whenever the logarithm is taken in the range where $\exp$ is one to one, and $\hat\chi$ does not appear. This is the log-linear property of Barrau and Bonnabel (2017), Theorem 2, for this system; the dynamics $\chi \mapsto \chi \exp(u)$ are group affine. With noise, $u = u_m - n$ and $e^+ = \exp(\operatorname{Ad}_{\exp(-u_m)} \xi) \exp(u_m)^{-1} \exp(u_m - n)$. The last two factors equal $\exp(-J n + O(|n|^2))$, where $J$ is the right Jacobian of $SE(2)$ at $u_m$, which is $I + O(|u_m|)$. Combining the two exponentials to first order gives $\xi^+ = F \xi - J n$. The code uses $J = I$ and adds $Q$ (line L3), which is the first-order covariance for a short step.

*Claim 2.* From $\chi = \hat\chi \exp(\xi)$, the position is $p = \hat p + \hat R \, V(\xi_\theta) (\xi_x, \xi_y)$. The inverse of $\hat\chi$ maps $(Y, 1)$ to $(\hat R^T (Y - \hat p), 1)$, so

$$z = \hat R^T (Y - \hat p) = V(\xi_\theta) (\xi_x, \xi_y) + \hat R^T V.$$

Since $V(\xi_\theta) = I + O(|\xi_\theta|)$, $z = (\xi_x, \xi_y) + \hat R^T V + O(|\xi|^2)$, which is $H \xi + \hat R^T V$. The covariance of $\hat R^T V$ is $\hat R^T N \hat R$, and for $N = s^2 I$ it is $s^2 \hat R^T \hat R = N$.

*Claim 3.* The new error is $\exp(\xi') = \exp(K z)^{-1} \hat\chi^{-1} \chi = \exp(-K z) \exp(\xi)$. By the Baker-Campbell-Hausdorff formula, $\xi' = \xi - K z + O(|\xi| |K z|)$, and with Claim 2, $\xi' = (I - K H) \xi - K \hat R^T V$ to first order. As for any linear Kalman update, its covariance is $(I - K H) P (I - K H)^T + K \hat N K^T$ for every $K$, and $K = P H^T (H P H^T + \hat N)^{-1}$ minimizes its trace. This is the [Kalman filter](/kalman-filter/) step on $\xi$, done by lines L6 and L8, and line L7 applies the estimate of $\xi$ to $\hat\chi$.

*Claim 4.* By induction on $k$. $P_0$ is given. Line L3 computes $P$ from $P$, $F = \operatorname{Ad}_{\exp(-u_m)}$ and $Q$; $F$ depends only on $u_m$. Lines L5, L6 and L8 compute $K$ and $P$ from $P$, $H$ and $\hat N$; $H$ is constant, and $\hat N = N$ under the hypothesis. No line that changes $P$ or $K$ reads $\hat\chi$ or $Y$. $\blacksquare$

**Remarks.**

- Claim 4 is the main difference from the [extended Kalman filter](/extended-kalman-filter/) on the same system. There, $F$ and $H$ are evaluated at the estimate, so a wrong estimate gives a wrong gain, which can make the error worse. Here the gain is the same as it would be at the true pose. The tests check this: two runs from different estimates on the same data gave the same $P$ and $K$ to $10^{-12}$.
- The convergence of the filter is not part of these claims. Barrau and Bonnabel (2017) prove a stability result for the deterministic invariant filter under observability conditions; the tests measure convergence from a heading error of 143 degrees and a position error of 12.8 m.
- With an anisotropic $N$, $\hat N$ depends on $\hat R$, and Claim 4 holds only in the weaker sense that $P$ depends on the heading estimate, not on the position estimate.
