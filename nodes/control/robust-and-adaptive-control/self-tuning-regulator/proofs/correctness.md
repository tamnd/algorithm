---
title: The minimum variance self-tuner has the self-tuning property
proves: [correctness]
status: full
---

Notation is that of the page. The regressor is $\varphi_t = (y_t, \dots, y_{t-n_s}, u_{t-1}, \dots, u_{t-n_r})$, the target is $z_{t+1} = y_{t+1} - \beta_0 u_t$, and the control is $u_t = -\varphi_t^T\hat\theta_t/\beta_0$ (line L8), where $\hat\theta_t$ is the estimate after the update with $(\varphi_{t-1}, z_t)$. We take $\lambda = 1$.

**Claim 1 (the residual is the output).** Line L8 gives $\beta_0 u_t = -\varphi_t^T\hat\theta_t$. So
$$z_{t+1} - \varphi_t^T \hat\theta_t = y_{t+1} - \beta_0 u_t - \varphi_t^T\hat\theta_t = y_{t+1}.$$
In closed loop, the prediction error of the model at the current estimate is the next output.

**Claim 2 (normal equations of RLS).** Line L5 to L7 with $\lambda = 1$ are the recursive form of $P_t^{-1} = P_0^{-1} + \sum_{k<t}\varphi_k\varphi_k^T$ and $P_t^{-1}\hat\theta_t = P_0^{-1}\theta_0 + \sum_{k<t}\varphi_k z_{k+1}$ (a standard identity, proved on the page [RLS algorithm](/rls-algorithm/) with the [Sherman-Morrison formula](/sherman-morrison-formula/); the tests check it exactly in rational arithmetic). By Claim 1, $z_{k+1} = y_{k+1} + \varphi_k^T\hat\theta_k$. Substitute and subtract $P_t^{-1}\hat\theta_t = P_0^{-1}\hat\theta_t + \sum_{k<t}\varphi_k\varphi_k^T\hat\theta_t$:
$$\sum_{k<t}\varphi_k y_{k+1} = P_0^{-1}(\hat\theta_t - \theta_0) + \sum_{k<t}\varphi_k\varphi_k^T(\hat\theta_t - \hat\theta_k).$$

**Claim 3 (self-tuning property).** Assume $\hat\theta_t \to \theta_\infty$ and $\frac1t\sum_{k<t}|\varphi_k|^2 \le M$ for all $t$. Then $\frac1t\sum_{k<t}\varphi_k y_{k+1} \to 0$. In terms of sample correlations, $\hat r_y(\tau) = \lim \frac1t\sum y_{k+\tau}y_k = 0$ for $\tau = 1, \dots, n_s + 1$, and $\hat r_{yu}(\tau) = \lim\frac1t\sum y_{k+\tau}u_k = 0$ for $\tau = 1, \dots, n_r$, whenever these limits exist.

*Proof.* Divide the identity of Claim 2 by $t$. The first term is $P_0^{-1}(\hat\theta_t - \theta_0)/t \to 0$ because $\hat\theta_t$ is bounded. For the second term, let $\epsilon > 0$ and choose $K$ with $|\hat\theta_k - \theta_\infty| < \epsilon$ for $k \ge K$. For $t > K$, the terms with $k \ge K$ satisfy $|\hat\theta_t - \hat\theta_k| < 2\epsilon$, so their sum divided by $t$ is at most $2\epsilon\frac1t\sum_{k<t}|\varphi_k|^2 \le 2\epsilon M$. The terms with $k < K$ are a fixed finite sum, which divided by $t$ goes to $0$. So the $\limsup$ of the norm is at most $2\epsilon M$ for every $\epsilon$, which proves the limit. The components of $\varphi_k y_{k+1}$ are $y_{k+1}y_{k-i}$ for $i = 0, \dots, n_s$ and $y_{k+1}u_{k-j}$ for $j = 1, \dots, n_r$, which give the stated correlations. $\square$

**Claim 4 (the example limit is the minimum variance law).** For the plant $y_{t+1} = p_0 y_t + b u_t + e_{t+1} + c\,e_t$ with $|c| < 1$ and $n_s = n_r = 0$, a constant gain $u_t = g y_t$ gives $y_{t+1} = p\,y_t + e_{t+1} + c\,e_t$ with $p = p_0 + b g$. For $|p| < 1$ this is a stationary ARMA(1,1) process, and its correlations are $r_y(0) = \sigma^2(1 + c^2 + 2pc)/(1 - p^2)$ and $r_y(1) = \sigma^2(1 + pc)(p + c)/(1 - p^2)$. Since $|pc| < 1$, $r_y(1) = 0$ if and only if $p = -c$, that is $g = -(p_0 + c)/b$. Then $y_{t+1} + c y_t = e_{t+1} + c e_t$, so $y_t = e_t$ up to a term $(-c)^t(y_0 - e_0)$ that goes to zero, and the variance is $\sigma^2$, the minimum: every causal law gives $y_{t+1} = e_{t+1} + (\text{a function of the data up to } t)$, whose variance is at least $\sigma^2$ because $e_{t+1}$ is independent of the data up to $t$. With $p_0 = 0.9$, $b = 0.5$, $c = 0.5$ this is $g = -2.8$, the value of the page. So by Claim 3, if the estimate converges and the loop is bounded in mean square, the limit gain is $-2.8$.

**Remark.** Claims 3 and 4 assume convergence; they do not prove it. Ljung (1977) proved convergence with probability one under a positive real condition on $C$ (a theorem not reproduced here). The tests measure convergence on fixed noise sequences.
