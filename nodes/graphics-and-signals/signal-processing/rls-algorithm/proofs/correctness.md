---
title: RLS gives the exact weighted, regularized least squares solution after every sample
proves: [correctness]
status: full
---

Fix $0 < \lambda \le 1$ and $\delta > 0$. Write $u_i$ for the tap vector of line L3 at time $i$ and $d_i$ for $d[i]$. For $n \ge -1$ define

$$\Phi_n = \lambda^{n+1} \delta I + \sum_{i=0}^{n} \lambda^{n-i}\, u_i u_i^T, \qquad z_n = \sum_{i=0}^{n} \lambda^{n-i}\, d_i\, u_i,$$

so $\Phi_{-1} = \delta I$ and $z_{-1} = 0$, and the cost

$$C_n(w) = \sum_{i=0}^{n} \lambda^{n-i} (d_i - w^T u_i)^2 + \lambda^{n+1} \delta\, \|w\|^2.$$

We work in exact real arithmetic, as in the real RAM. Let $w_n$ and $P_n$ be the values of $w$ and $P$ after the pass of the loop for time $n$, and $w_{-1}, P_{-1}$ the values of line L1.

**Lemma 1 (the batch answer).** $\Phi_n$ is symmetric positive definite, and $C_n$ has the unique minimizer $\Phi_n^{-1} z_n$.

*Proof.* For $v \ne 0$, $v^T \Phi_n v = \lambda^{n+1} \delta \|v\|^2 + \sum_i \lambda^{n-i} (u_i^T v)^2 > 0$. Expanding, $C_n(w) = w^T \Phi_n w - 2 z_n^T w + \sum_i \lambda^{n-i} d_i^2$, a strictly convex quadratic whose gradient $2(\Phi_n w - z_n)$ vanishes only at $w = \Phi_n^{-1} z_n$. $\square$

The two sums satisfy $\Phi_n = \lambda \Phi_{n-1} + u_n u_n^T$ and $z_n = \lambda z_{n-1} + d_n u_n$ for $n \ge 0$.

**Lemma 2 (Sherman-Morrison).** Let $A$ be symmetric positive definite, $u$ a vector and $\lambda > 0$, and let $\pi = A^{-1} u$ and $k = \pi / (\lambda + u^T \pi)$. Then $(\lambda A + u u^T)^{-1} = (A^{-1} - k \pi^T)/\lambda$, and $(\lambda A + u u^T)^{-1} u = k$.

*Proof.* The denominator is positive because $u^T \pi = u^T A^{-1} u \ge 0$. Multiply: $(\lambda A + u u^T)(A^{-1} - k\pi^T) = \lambda I - \lambda A k \pi^T + u u^T A^{-1} - u (u^T k) \pi^T$. Here $A k = u/(\lambda + u^T\pi)$ and $u^T A^{-1} = \pi^T$, because $A^{-1}$ is symmetric, and $u^T k = u^T \pi/(\lambda + u^T \pi)$. So the product is $\lambda I + u \pi^T \big(1 - \frac{\lambda}{\lambda + u^T\pi} - \frac{u^T \pi}{\lambda + u^T\pi}\big) = \lambda I$. Dividing by $\lambda$ gives the first identity. For the second, $(A^{-1} - k\pi^T) u / \lambda = (\pi - k\, \pi^T u)/\lambda = \pi \big(1 - \frac{u^T\pi}{\lambda + u^T\pi}\big)/\lambda = \pi/(\lambda + u^T \pi) = k$. $\square$

**Theorem.** For every $n \ge -1$, $P_n = \Phi_n^{-1}$ and $w_n = \Phi_n^{-1} z_n$. So after each sample, RLS holds the unique minimizer of $C_n$. For $\lambda = 1$ this is the regularized batch least squares answer $\big(\delta I + \sum_{i \le n} u_i u_i^T\big)^{-1} \sum_{i \le n} d_i u_i$, with the regularization set by the start value $P_{-1} = \delta^{-1} I$.

*Proof.* By induction on $n$. For $n = -1$, line L1 sets $P = \delta^{-1} I = \Phi_{-1}^{-1}$ and $w = 0 = \Phi_{-1}^{-1} z_{-1}$. Suppose the claim holds for $n - 1$. Lines L4 and L5 compute $\pi = P_{n-1} u_n$ and $k$ as in Lemma 2 with $A = \Phi_{n-1}$, and line L8 computes $P_n = (P_{n-1} - k\pi^T)/\lambda = (\lambda \Phi_{n-1} + u_n u_n^T)^{-1} = \Phi_n^{-1}$. For the taps,

$$\Phi_n^{-1} z_n = \Phi_n^{-1} (\lambda z_{n-1} + d_n u_n) = \frac{1}{\lambda}(P_{n-1} - k \pi^T)\, \lambda\, z_{n-1} + d_n\, k = w_{n-1} - k\, \pi^T z_{n-1} + d_n\, k,$$

using Lemma 2 for $\Phi_n^{-1} u_n = k$ and the hypothesis $P_{n-1} z_{n-1} = w_{n-1}$. Since $P_{n-1}$ is symmetric, $\pi^T z_{n-1} = u_n^T P_{n-1} z_{n-1} = u_n^T w_{n-1}$. So $\Phi_n^{-1} z_n = w_{n-1} + k\,(d_n - w_{n-1}^T u_n) = w_{n-1} + k\, \xi_n$, which is line L7 with the a priori error $\xi_n$ of line L6. Lemma 1 gives the minimizer. $\blacksquare$

**Remarks.** The error after the update is $d_n - w_n^T u_n = \xi_n - (u_n^T k)\, \xi_n = \frac{\lambda}{\lambda + u_n^T P_{n-1} u_n}\, \xi_n$, so it is never larger in size than the a priori error. As $\lambda^{n+1}\delta \to 0$ for $\lambda < 1$, the effect of the start value fades exponentially; for $\lambda = 1$ it stays, but $\Phi_n$ grows with $n$ when the input keeps exciting every direction, so the bias toward zero falls like $1/n$.
