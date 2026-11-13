---
title: LMS is a stochastic gradient step and converges in the mean for 0 < mu < 2/lambda_max
proves: [correctness]
status: full
---

Write $u_n$ for the tap vector of line L3 at time $n$, $w_n$ for the taps before the update of time $n$, so $w_0$ is the value of line L1, and $e_n = d_n - w_n^T u_n$ for the error of line L5. Line L6 gives

$$w_{n+1} = w_n + \mu\, e_n\, u_n. \tag{1}$$

We work in exact real arithmetic, as in the real RAM.

**Lemma 1 (a stochastic gradient step).** Let $J(w) = E[(d_n - w^T u_n)^2]$, with $R = E[u_n u_n^T]$ and $p = E[d_n u_n]$. Then $\nabla J(w) = -2(p - R w)$, and $-2 e_n u_n$ is the gradient of the instantaneous square error $e_n^2$ as a function of $w_n$. So (1) is a step of length $\mu/2$ against the gradient of $e_n^2$, whose expectation, for $w_n$ fixed, is $\nabla J(w_n)$.

*Proof.* $J(w) = E[d_n^2] - 2 p^T w + w^T R w$, so $\nabla J = -2p + 2Rw$. The derivative of $(d_n - w^T u_n)^2$ with respect to $w$ is $-2 (d_n - w^T u_n)\, u_n$. For a fixed $w$, $E[-2 (d_n - w^T u_n) u_n] = -2(p - R w)$. $\square$

**Lemma 2 (one step, without statistics).** The error after the update, $e_n^+ = d_n - w_{n+1}^T u_n$, satisfies $e_n^+ = (1 - \mu \|u_n\|^2)\, e_n$. So for $u_n \ne 0$, the update reduces the error on the current sample if and only if $0 < \mu < 2/\|u_n\|^2$, and the normalized step $\mu = 1/\|u_n\|^2$ makes it zero.

*Proof.* $w_{n+1}^T u_n = w_n^T u_n + \mu e_n u_n^T u_n$, so $e_n^+ = e_n - \mu \|u_n\|^2 e_n$. $\square$

**Theorem (convergence in the mean).** Assume that the pairs $(u_n, d_n)$ are independent and identically distributed, with $R = E[u_n u_n^T]$ positive definite and $p = E[d_n u_n]$, and that $w_0$ is fixed. Let $w^\ast = R^{-1} p$, the Wiener solution, and let $\lambda_{\max}$ be the largest eigenvalue of $R$. Then

$$E[w_n] - w^\ast = (I - \mu R)^n (w_0 - w^\ast) \quad \text{for all } n \ge 0,$$

and $E[w_n] \to w^\ast$ for every $w_0$ if and only if $0 < \mu < 2/\lambda_{\max}$.

*Proof.* By (1), $w_n$ is a function of $w_0$ and of $(u_i, d_i)$ for $i < n$, so it is independent of $(u_n, d_n)$. Take expectations in (1):

$$E[w_{n+1}] = E[w_n] + \mu\, E[d_n u_n] - \mu\, E[u_n u_n^T w_n] = E[w_n] + \mu\, p - \mu\, R\, E[w_n],$$

where $E[u_n u_n^T w_n] = E[u_n u_n^T]\, E[w_n]$ by independence. With $v_n = E[w_n] - w^\ast$ and $p = R w^\ast$, this is $v_{n+1} = (I - \mu R)\, v_n$, and induction on $n$ gives the formula.

The matrix $R$ is symmetric and positive definite, so $R = Q \Lambda Q^T$ with $Q$ orthogonal and $\Lambda = \operatorname{diag}(\lambda_1, \ldots, \lambda_M)$, all $\lambda_i > 0$. Then $Q^T v_n = (I - \mu \Lambda)^n Q^T v_0$, so coordinate $i$ of $Q^T v_n$ is $(1 - \mu \lambda_i)^n$ times coordinate $i$ of $Q^T v_0$. If $|1 - \mu \lambda_i| < 1$ for all $i$, every coordinate tends to $0$, and so does $v_n$, since $Q$ preserves the norm. If $|1 - \mu\lambda_i| \ge 1$ for some $i$, take $w_0 = w^\ast + q_i$, where $q_i$ is column $i$ of $Q$; then $\|v_n\| = |1 - \mu \lambda_i|^n \ge 1$ for all $n$, so $v_n$ does not tend to $0$. Finally, $|1 - \mu\lambda_i| < 1$ is $0 < \mu \lambda_i < 2$, and this holds for every $i$ if and only if $0 < \mu < 2/\lambda_{\max}$, because all $\lambda_i > 0$. $\blacksquare$

**Remarks.** The theorem is exact for independent regressors, as in the tests. For a tapped delay line, successive vectors $u_n$ share $M - 1$ samples and are not independent; the theorem is then the classical independence approximation, which describes the mean behavior well when $\mu$ is small. Convergence of $E[w_n]$ does not imply that $w_n$ stays near $w^\ast$: the second moment $E\|w_n - w^\ast\|^2$ obeys a different linear recursion, which depends on the fourth moments of $u_n$ and needs a smaller step. The texts that write the update as $w + 2\mu e u$, the gradient step of length $\mu$, get the bound $0 < \mu < 1/\lambda_{\max}$ for the same filter.
