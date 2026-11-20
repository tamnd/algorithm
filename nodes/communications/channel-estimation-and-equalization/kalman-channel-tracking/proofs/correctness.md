---
title: Under the Gauss-Markov model with known symbols, the Kalman channel tracker gives the conditional mean and covariance of the taps, and a = J0(2 pi f_D T) is the lag-1 Yule-Walker fit of a Clarke channel
proves: [correctness]
status: full
---

The taps are $h_k \in \mathbb{C}^L$. The model is $h_k = a\, h_{k-1} + v_k$ for $k \ge 0$, with $0 \le a \le 1$, $Q = (1 - a^2) D$ and $D = \mathrm{diag}(P_0, \ldots, P_{L-1})$. The sample is $y[k] = c_k h_k + w[k]$, where $c_k$ is a known row vector. The random vectors $h_{-1} \sim \mathcal{CN}(0, D)$, $v_0, v_1, \ldots \sim \mathcal{CN}(0, Q)$ and $w[0], w[1], \ldots \sim \mathcal{CN}(0, N_0)$ are all independent, and $N_0 > 0$. Write $Y_k = (y[0], \ldots, y[k])$.

A random vector $z$ is proper complex Gaussian, $z \sim \mathcal{CN}(m, C)$, if its real and imaginary parts are jointly Gaussian and $E[(z - m)(z - m)^T] = 0$. Linear maps and sums of independent proper Gaussian vectors are proper Gaussian.

**Lemma 1 (Gaussian conditioning).** Let $(z, u)$ be jointly proper complex Gaussian, with means $m_z$, $m_u$, covariances $C_{zz}$, $C_{uu}$ (invertible) and $C_{zu} = E[(z - m_z)(u - m_u)^H]$. Then $z$ given $u$ is $\mathcal{CN}(m_z + C_{zu} C_{uu}^{-1} (u - m_u),\ C_{zz} - C_{zu} C_{uu}^{-1} C_{zu}^H)$.

*Proof.* Let $G = C_{zu} C_{uu}^{-1}$ and $e = z - m_z - G (u - m_u)$. Then $E[e (u - m_u)^H] = C_{zu} - G C_{uu} = 0$. Also $E[e (u - m_u)^T] = 0$, because the pair is proper. The real and imaginary parts of $e$ and $u$ are jointly Gaussian and uncorrelated, so $e$ is independent of $u$. Hence $z = m_z + G(u - m_u) + e$ given $u$ has the mean $m_z + G(u - m_u)$ and the covariance $E[e e^H] = C_{zz} - G C_{zu}^H$. $\square$

**Lemma 2 (stationarity).** $\mathrm{Cov}(h_k) = D$ for every $k \ge -1$.

*Proof.* True for $k = -1$. If $\mathrm{Cov}(h_{k-1}) = D$, then $\mathrm{Cov}(h_k) = a^2 D + Q = D$, because $v_k$ is independent of $h_{k-1}$. $\square$

**Theorem 1.** For every $k \ge 0$, the values $\hat h$ and $\Sigma$ after line L8 at step $k$ satisfy $\hat h = E[h_k \mid Y_k]$ and $\Sigma = \mathrm{Cov}(h_k \mid Y_k)$, and $h_k$ given $Y_k$ is proper Gaussian.

*Proof.* Use induction on $k$, with the statement for $k = -1$ read as: line L1 gives the mean $0$ and the covariance $D$ of $h_{-1}$ given no samples. This is true by the model.

Assume that $h_{k-1}$ given $Y_{k-1}$ is $\mathcal{CN}(\hat h, \Sigma)$, with the values before step $k$. The increment $v_k$ is independent of $(h_{k-1}, Y_{k-1})$, since $Y_{k-1}$ depends only on $h_{-1}, v_0, \ldots, v_{k-1}$ and $w[0], \ldots, w[k-1]$. So $h_k = a h_{k-1} + v_k$ given $Y_{k-1}$ is $\mathcal{CN}(a \hat h,\ a^2 \Sigma + Q)$. These are the values of line L3; call them $\hat h^-$ and $\Sigma^-$.

Given $Y_{k-1}$, the pair $(h_k, y[k])$ is proper Gaussian, because $y[k] = c_k h_k + w[k]$ and $w[k]$ is independent of everything else. Its moments are $E[y[k] \mid Y_{k-1}] = c_k \hat h^-$, $\mathrm{Cov}(h_k, y[k] \mid Y_{k-1}) = \Sigma^- c_k^H$, and $\mathrm{Var}(y[k] \mid Y_{k-1}) = c_k \Sigma^- c_k^H + N_0 = s$, which is line L5 and is at least $N_0 > 0$. Lemma 1 with $z = h_k$ and $u = y[k]$ gives the conditional mean $\hat h^- + (\Sigma^- c_k^H / s)(y[k] - c_k \hat h^-)$ and the covariance $\Sigma^- - (\Sigma^- c_k^H / s)\, c_k \Sigma^-$, using $(\Sigma^- c_k^H)^H = c_k \Sigma^-$. With $g = \Sigma^- c_k^H / s$ (line L6), these are lines L7 and L8. Conditioning on $Y_{k-1}$ and then on $y[k]$ is conditioning on $Y_k$, so the statement holds for $k$. $\square$

**Corollary 1 (optimality).** $\hat h_k$ minimizes $E\|h_k - f(Y_k)\|^2$ over all measurable functions $f$, and the minimum is $\mathrm{tr}\, \Sigma_k$ in expectation over the samples. If the Gaussian assumption is dropped but the first and second moments stay the same, the same recursion gives the linear estimator with the smallest mean squared error, because lines L3 to L8 use only first and second moments and Lemma 1 holds for the best linear estimator without the Gaussian assumption.

*Proof.* The conditional mean minimizes the mean squared error, and its error covariance is the conditional covariance. For the linear case, the proof of Lemma 1 without the independence step shows that $m_z + G(u - m_u)$ makes the error uncorrelated with $u$, which is the orthogonality condition of the linear minimum mean squared error estimator. $\square$

**Corollary 2 (bounded uncertainty).** $(\Sigma_k)_{ll} \le P_l$ for every $k$ and $l$.

*Proof.* The conditional variance of a Gaussian variable never exceeds its unconditional variance, which is $P_l$ by Lemma 2. $\square$

**Lemma 3 (the lag-1 fit).** Let $(h_k)$ be a stationary process with autocorrelation $r(m) = E[h_k \bar h_{k-m}] = P\, J_0(2\pi f_D T m)$, the Clarke model sampled at the symbol time $T$. The coefficient $a$ that minimizes $E|h_k - a h_{k-1}|^2$ over real or complex $a$ is $a = r(1)/r(0) = J_0(2\pi f_D T)$, and the minimum is $P (1 - J_0(2\pi f_D T)^2)$, which is the variance of $v_k$ in the model.

*Proof.* $E|h_k - a h_{k-1}|^2 = r(0) - 2\,\mathrm{Re}(\bar a\, r(1)) + |a|^2 r(0)$. Its minimum over $a$ is at $a = r(1)/r(0)$, which is the Yule-Walker equation of order 1. The minimum value is $r(0) - |r(1)|^2 / r(0) = P(1 - J_0^2)$. $\square$

The AR(1) model with this $a$ has the same lag-0 and lag-1 correlations as the Clarke process, but its lag-$m$ correlation is $a^m$, not $J_0(2\pi f_D T m)$. So Theorem 1 states optimality for the model, not for the Clarke process.

**Remarks on the conditions.**

1. The proof uses that $c_k$ is known and independent of $h$ and $w$. Pilots and training symbols satisfy this. Decisions do not: they depend on the noise, and a wrong decision is not the transmitted symbol. In decision-directed mode, Theorem 1 holds on the event that all decisions are correct and are treated as fixed, and not in general.
2. The gain needs $s > 0$, which holds because $N_0 > 0$. With $N_0 = 0$ and $c_k = 0$, line L6 divides by 0.
3. The tests check Theorem 1 numerically: for $a = 1$ the filter equals the batch Bayesian estimate $(D^{-1} + C^H C / N_0)^{-1} C^H y / N_0$, and for $a = 0.9$ it equals Lemma 1 applied to the stacked taps $(h_0, \ldots, h_{T-1})$ with $\mathrm{Cov}(h_k, h_m) = a^{|k-m|} D$, within $10^{-9}$. A simulation checks Corollary 1: the measured mean of $\|h_k - \hat h_k\|^2$ divided by the mean of $\mathrm{tr}\, \Sigma_k$ is within 5 percent of 1.
